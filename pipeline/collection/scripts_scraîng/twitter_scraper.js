#!/usr/bin/env node
/*
 * Twitter scraping pipeline using Nitter mirrors (via Puppeteer).
 *
 * 1. Charge les intervenants pertinents depuis le JSONL enrichi Assembl?e.
 * 2. Associe chaque intervenant ? un compte Twitter (override manuel ou recherche multi-instances Nitter).
 * 3. Collecte les tweets contenant des mots-cl?s (Gaza / Palestine / Isra?l / Hamas ?) avec stats & commentaires.
 * 4. Sauvegarde les r?sultats au format JSONL.
 */

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const DEFAULT_INPUT = path.resolve(__dirname, "../data/processed/interventions_enriched.jsonl");
const DEFAULT_OUTPUT = path.resolve(__dirname, "../data/processed/twitter_scrape.jsonl");
const DEFAULT_HANDLES_FILE = path.resolve(__dirname, "../config/twitter_handles.json");

const KEYWORDS = [
  "gaza",
  "palestine",
  "israel",
  "israeli",
  "cisjordanie",
  "rafah",
  "hamas",
  "hezbollah",
  "colonisation",
  "cessez le feu",
  "otage",
  "otages",
  "apartheid",
];

const NITTER_INSTANCES = [
  "https://nitter.net",
  "https://nitter.pufe.org",
  "https://nitter.privacydev.net",
  "https://nitter.fdn.fr",
  "https://nitter.unixfox.eu",
];

const CONFIG = {
  maxTweetsPerAccount: 80,
  maxScrollsPerAccount: 20,
  scrollDelayMs: 2500,
  searchDelayMs: 1800,
  threadDelayMs: 1500,
  headless: true,
  navigationTimeout: 45000,
  retriesPerInstance: 2,
};

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    input: DEFAULT_INPUT,
    output: DEFAULT_OUTPUT,
    handles: [],
    handlesFile: DEFAULT_HANDLES_FILE,
  };
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if ((arg === "--input" || arg === "-i") && args[i + 1]) {
      options.input = path.resolve(args[i + 1]);
      i += 1;
    } else if ((arg === "--output" || arg === "-o") && args[i + 1]) {
      options.output = path.resolve(args[i + 1]);
      i += 1;
    } else if (arg === "--handles" && args[i + 1]) {
      options.handles = args[i + 1].split(",").map((v) => v.trim()).filter(Boolean);
      i += 1;
    } else if (arg === "--handles-file" && args[i + 1]) {
      options.handlesFile = path.resolve(args[i + 1]);
      i += 1;
    }
  }
  return options;
}

function loadSpeakers(inputPath) {
  const entries = new Map();
  const lines = fs.readFileSync(inputPath, "utf-8").split(/\r?\n/);
  lines.forEach((line) => {
    if (!line.trim()) return;
    try {
      const record = JSON.parse(line);
      const key = record.matched_name || record.speaker_name;
      if (!key || entries.has(key)) return;
      entries.set(key, {
        displayName: key,
        speakerName: record.speaker_name,
        matchedName: record.matched_name,
        group: record.matched_group,
        legislature: record.matched_legislature,
        metadata: record.matched_metadata || {},
      });
    } catch (err) {
      console.warn("[WARN] Ligne JSON invalide", err.message);
    }
  });
  return Array.from(entries.values());
}

function loadHandleOverrides(filePath) {
  if (!fs.existsSync(filePath)) {
    return {};
  }
  try {
    const text = fs.readFileSync(filePath, "utf-8");
    const json = JSON.parse(text);
    return json;
  } catch (err) {
    console.warn(`[WARN] Impossible de parser ${filePath}: ${err.message}`);
    return {};
  }
}

function simplify(text) {
  return (text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function buildQueries(person) {
  const queries = new Set();
  const baseName = person.matchedName || person.displayName || "";
  const speakerName = person.speakerName || "";
  const slug = (person.metadata.slug || "").replace(/-/g, " ");
  const lastname = (baseName || speakerName).split(" ").pop() || "";
  [
    baseName,
    speakerName,
    slug,
    `${baseName} d?put?`,
    `${speakerName} d?put?`,
    `${baseName} assembl?e nationale`,
    `${speakerName} assembl?e nationale`,
    lastname,
  ].forEach((candidate) => {
    const clean = (candidate || "").trim();
    if (clean.length > 0) queries.add(clean);
  });
  return Array.from(queries);
}

function shuffle(array) {
  const copy = array.slice();
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

async function navigate(page, url, timeout, retries = CONFIG.retriesPerInstance) {
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      await page.goto(url, { waitUntil: "domcontentloaded", timeout });
      return true;
    } catch (err) {
      console.warn(`[WARN] Navigation ?chou?e (${attempt}/${retries}) vers ${url}: ${err.message}`);
      await delay(1200 * attempt);
    }
  }
  return false;
}

function mergeHandle(overrides, person) {
  const keys = [person.matchedName, person.displayName, person.speakerName];
  for (const key of keys) {
    if (!key) continue;
    const exact = overrides[key];
    if (exact) {
      return exact;
    }
    const simplified = overrides[simplify(key)];
    if (simplified) {
      return simplified;
    }
  }
  return null;
}

async function resolveHandle(browser, person, overrides) {
  const explicit = mergeHandle(overrides, person);
  if (explicit) {
    return {
      handle: explicit.replace(/^@/, ""),
      displayName: explicit.replace(/^@/, ""),
      profileUrl: `${NITTER_INSTANCES[0]}/${explicit.replace(/^@/, "")}`,
      instanceBase: NITTER_INSTANCES[0],
      matchedVia: "override",
    };
  }

  const page = await browser.newPage();
  try {
    const queries = buildQueries(person);
    const shuffledInstances = shuffle(NITTER_INSTANCES);
    for (const query of queries) {
      for (const instance of shuffledInstances) {
        const searchUrl = `${instance}/search?f=users&q=${encodeURIComponent(query)}`;
        const success = await navigate(page, searchUrl, CONFIG.navigationTimeout);
        if (!success) {
          continue;
        }
        await delay(CONFIG.searchDelayMs);
        const results = await page.evaluate(() => {
          const cards = Array.from(document.querySelectorAll(".user-card"));
          return cards.map((card) => {
            const name = card.querySelector(".fullname")?.innerText || "";
            const username = card.querySelector(".username")?.innerText || "";
            const bio = card.querySelector(".bio")?.innerText || "";
            const link = card.querySelector("a")?.getAttribute("href") || "";
            return { name, username, bio, link };
          });
        });
        if (!results || results.length === 0) {
          console.warn(`[WARN] Aucun r?sultat pour "${query}" sur ${instance}`);
          continue;
        }
        const tokens = simplify(person.displayName || person.speakerName || "")
          .split(" ")
          .filter((token) => token.length > 2);
        const best = results.find((candidate) => {
          const uname = simplify(candidate.username || "");
          const fullname = simplify(candidate.name || "");
          const bio = simplify(candidate.bio || "");
          return tokens.some((token) => fullname.includes(token) || bio.includes(token) || uname.includes(token));
        }) || results[0];
        if (best && best.username) {
          const handle = best.username.replace(/^@/, "");
          const pathPart = best.link && best.link.startsWith("/") ? best.link : `/${handle}`;
          return {
            handle,
            displayName: best.name || handle,
            profileUrl: `${instance}${pathPart}`,
            instanceBase: instance,
            matchedVia: `search:${query}`,
          };
        }
      }
    }
    return null;
  } finally {
    await page.close();
  }
}

async function scrapeTweets(browser, account) {
  const page = await browser.newPage();
  const tweets = [];
  const seen = new Set();
  try {
    const profileUrl = `${account.instanceBase}/${account.handle}`;
    const success = await navigate(page, profileUrl, CONFIG.navigationTimeout);
    if (!success) {
      return tweets;
    }
    await delay(CONFIG.scrollDelayMs);
    let lastHeight = 0;
    for (let scroll = 0; scroll < CONFIG.maxScrollsPerAccount; scroll += 1) {
      const batch = await page.evaluate((kw) => {
        const entries = [];
        const cards = Array.from(document.querySelectorAll(".timeline-item"));
        cards.forEach((card) => {
          const contentNode = card.querySelector(".tweet-content");
          if (!contentNode) return;
          const content = contentNode.innerText || "";
          const lower = content.toLowerCase();
          if (!kw.some((word) => lower.includes(word))) return;
          const link = card.querySelector("a.tweet-link")?.getAttribute("href") || "";
          const date = card.querySelector(".tweet-date a")?.getAttribute("title") || "";
          const stats = Array.from(card.querySelectorAll(".tweet-stats .icon-container"));
          function valueByIcon(className) {
            const node = stats.find((icon) => icon.querySelector(`i.${className}`));
            if (!node) return 0;
            const text = node.innerText || "0";
            const digits = text.replace(/[^0-9]/g, "");
            return Number(digits || 0);
          }
          const username = card.querySelector(".username")?.innerText || "";
          const fullname = card.querySelector(".fullname")?.innerText || "";
          entries.push({
            tweetPath: link,
            url: link ? link : "",
            postedAt: date,
            content,
            username,
            fullname,
            stats: {
              replies: valueByIcon("icon-comment"),
              retweets: valueByIcon("icon-retweet"),
              quotes: valueByIcon("icon-quote"),
              likes: valueByIcon("icon-heart"),
            },
          });
        });
        return entries;
      }, KEYWORDS);
      for (const tweet of batch) {
        if (tweets.length >= CONFIG.maxTweetsPerAccount) break;
        if (tweet.tweetPath && !seen.has(tweet.tweetPath)) {
          seen.add(tweet.tweetPath);
          tweets.push(tweet);
        }
      }
      if (tweets.length >= CONFIG.maxTweetsPerAccount) break;
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await delay(CONFIG.scrollDelayMs);
      const newHeight = await page.evaluate(() => document.body.scrollHeight);
      if (newHeight === lastHeight) break;
      lastHeight = newHeight;
    }
  } finally {
    await page.close();
  }
  return tweets;
}

async function scrapeThread(browser, base, tweetPath) {
  const comments = [];
  if (!tweetPath) return comments;
  const page = await browser.newPage();
  try {
    const url = tweetPath.startsWith("http") ? tweetPath : `${base}${tweetPath}`;
    const success = await navigate(page, url, CONFIG.navigationTimeout);
    if (!success) {
      return comments;
    }
    await delay(CONFIG.threadDelayMs);
    const data = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(".timeline-item"));
      return rows.slice(1).map((item) => {
        const content = item.querySelector(".tweet-content")?.innerText || "";
        const username = item.querySelector(".username")?.innerText || "";
        const fullname = item.querySelector(".fullname")?.innerText || "";
        const date = item.querySelector(".tweet-date a")?.getAttribute("title") || "";
        const stats = Array.from(item.querySelectorAll(".tweet-stats .icon-container"));
        function valueByIcon(className) {
          const node = stats.find((icon) => icon.querySelector(`i.${className}`));
          if (!node) return 0;
          const text = node.innerText || "0";
          const digits = text.replace(/[^0-9]/g, "");
          return Number(digits || 0);
        }
        return {
          username,
          fullname,
          postedAt: date,
          content,
          stats: {
            replies: valueByIcon("icon-comment"),
            retweets: valueByIcon("icon-retweet"),
            quotes: valueByIcon("icon-quote"),
            likes: valueByIcon("icon-heart"),
          },
        };
      });
    });
    comments.push(...data);
  } catch (err) {
    console.warn(`[WARN] Impossible de r?cup?rer les commentaires ${tweetPath}: ${err.message}`);
  } finally {
    await page.close();
  }
  return comments;
}

async function main() {
  const options = parseArgs();
  if (!fs.existsSync(options.input)) {
    throw new Error(`Fichier introuvable: ${options.input}`);
  }
  const handleOverrides = loadHandleOverrides(options.handlesFile);
  const persons = loadSpeakers(options.input);
  const totalPersons = persons.length;
  let processedCount = 0;
  if (totalPersons === 0) {
    console.error("Aucun intervenant d?tect? dans le fichier source");
    process.exit(1);
  }
  const outputStream = fs.createWriteStream(options.output, { flags: "w", encoding: "utf-8" });
  const browser = await puppeteer.launch({ headless: CONFIG.headless, args: ["--no-sandbox"] });
  try {
    for (const person of persons) {
      processedCount += 1;
      const personLabel = person.displayName || person.speakerName || person.matchedName || (person.metadata && person.metadata.slug) || "Unknown";
      console.log(`[PROGRESS] ${processedCount}/${totalPersons} ${personLabel}`);
      let handleInfo = null;
      if (options.handles.length > 0) {
        const explicit = options.handles.shift();
        handleInfo = {
          handle: explicit.replace(/^@/, ""),
          displayName: explicit.replace(/^@/, ""),
          profileUrl: `${NITTER_INSTANCES[0]}/${explicit.replace(/^@/, "")}`,
          instanceBase: NITTER_INSTANCES[0],
          matchedVia: "cli",
        };
      } else {
        handleInfo = await resolveHandle(browser, person, handleOverrides);
      }
      if (!handleInfo) {
        console.warn(`[WARN] Aucun compte trouv? pour ${personLabel}`);
        continue;
      }
      console.log(`[INFO] ${personLabel} -> @${handleInfo.handle} (${handleInfo.matchedVia || "search"})`);
      const tweets = await scrapeTweets(browser, handleInfo);
      console.log(`[INFO] ${tweets.length} tweets pertinents r?cup?r?s pour @${handleInfo.handle}`);
      for (const tweet of tweets) {
        let comments = [];
        if (tweet.tweetPath) {
          comments = await scrapeThread(browser, handleInfo.instanceBase, tweet.tweetPath);
        }
        const fullUrl = tweet.tweetPath && !tweet.tweetPath.startsWith("http")
          ? `${handleInfo.instanceBase}${tweet.tweetPath}`
          : tweet.url;
        const record = {
          scraped_at: new Date().toISOString(),
          keyword_hits: KEYWORDS.filter((kw) => (tweet.content || "").toLowerCase().includes(kw)),
          speaker: person,
          account: handleInfo,
          tweet: { ...tweet, url: fullUrl },
          comments,
        };
        outputStream.write(`${JSON.stringify(record)}\n`);
      }
    }
  } finally {
    await browser.close();
    outputStream.end();
  }
}

main().catch((err) => {
  console.error("[ERROR]", err);
  process.exit(1);
});

