#!/usr/bin/env node
/*
 * Scraper Twitter (via Nitter) pour les d?put?s AN : Gaza/Palestine
 * Adaptation de la logique syria-monitor.
 */

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const CONFIG = {
  nitterInstances: [
    "https://nitter.poast.org",
    "https://nitter.host",
    "https://nitter.cz",
    "https://nitter.fdn.fr",
    "https://nitter.net",
  ],
  keywords: [
    "gaza",
    "palestine",
    "israel",
    "isra?l",
    "hamas",
    "otage",
    "otages",
    "cessez-le-feu",
    "rafah",
    "cisjordanie",
    "apartheid",
  ],
  maxTweetsPerUser: 80,
  scrollDelayMs: 2500,
  timeoutMs: 40000,
  delayBetweenUsersMs: 2000,
};

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function loadJson(pathname) {
  const abs = path.resolve(pathname);
  return JSON.parse(await fs.promises.readFile(abs, "utf-8"));
}

async function loadInterventions() {
  const enrichedPath = path.resolve("FINAL/data/processed/interventions_enriched.jsonl");
  const content = await fs.promises.readFile(enrichedPath, "utf-8");
  return content.trim().split(/\r?\n/).map((line) => JSON.parse(line));
}

function containsKeyword(text) {
  const lower = (text || "").toLowerCase();
  return CONFIG.keywords.some((kw) => lower.includes(kw.toLowerCase()));
}

async function navigate(page, url) {
  try {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: CONFIG.timeoutMs });
    return true;
  } catch (err) {
    console.warn(`[WARN] Navigation ?chou?e ${url}: ${err.message}`);
    return false;
  }
}

async function scrapeTimeline(browser, instance, username) {
  const page = await browser.newPage();
  const collected = [];
  const seen = new Set();
  try {
    const profileUrl = `${instance.replace(/\/$/, "")}/${username}`;
    const ok = await navigate(page, profileUrl);
    if (!ok) {
      return [];
    }
    await delay(CONFIG.scrollDelayMs);
    let lastHeight = 0;
    for (let i = 0; i < CONFIG.maxTweetsPerUser; i += 1) {
      const { tweets, reachedEnd } = await page.evaluate(() => {
        const items = document.querySelectorAll(".timeline-item");
        const results = [];
        items.forEach((item) => {
          const contentNode = item.querySelector(".tweet-content");
          const dateNode = item.querySelector(".tweet-date a");
          if (!contentNode || !dateNode) return;
          const stats = Array.from(item.querySelectorAll(".tweet-stats .icon-container"));
          const pick = (klass) => {
            const target = stats.find((node) => node.querySelector(`i.${klass}`));
            if (!target) return 0;
            const digits = (target.innerText || "0").replace(/[^0-9]/g, "");
            return Number(digits || 0);
          };
          results.push({
            url: dateNode.getAttribute("href") || "",
            content: contentNode.innerText || "",
            date: dateNode.getAttribute("title") || "",
            stats: {
              replies: pick("icon-comment"),
              retweets: pick("icon-retweet"),
              quotes: pick("icon-quote"),
              likes: pick("icon-heart"),
            },
          });
        });
        const endReached = document.body.scrollHeight === window.scrollY + window.innerHeight;
        return { tweets: results, reachedEnd: endReached };
      });
      for (const tweet of tweets) {
        if (!tweet.url || seen.has(tweet.url)) continue;
        if (!containsKeyword(tweet.content)) continue;
        collected.push({ ...tweet, fullUrl: tweet.url.startsWith("http") ? tweet.url : `${instance}${tweet.url}` });
        seen.add(tweet.url);
        if (collected.length >= CONFIG.maxTweetsPerUser) break;
      }
      if (collected.length >= CONFIG.maxTweetsPerUser || reachedEnd) break;
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await delay(CONFIG.scrollDelayMs);
      const newHeight = await page.evaluate(() => document.body.scrollHeight);
      if (newHeight === lastHeight) break;
      lastHeight = newHeight;
    }
  } finally {
    await page.close();
  }
  return collected;
}

async function scrapeDeputes() {
  const mapping = await loadJson("FINAL/config/twitter_handles.json");
  const interventions = await loadInterventions();

  const speakers = new Set();
  interventions.forEach((item) => {
    const name = item.matched_name || item.speaker_name;
    if (name) speakers.add(name);
  });

  const toScrape = Array.from(speakers)
    .map((name) => ({ name, handle: mapping[name] }))
    .filter((entry) => entry.handle);

  console.log(`[INFO] ${toScrape.length} intervenants avec handle Twitter.`);

  const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox"] });
  const results = [];
  let processed = 0;

  try {
    for (const entry of toScrape) {
      processed += 1;
      console.log(`[PROGRESS] ${processed}/${toScrape.length} ${entry.name} (@${entry.handle})`);
      let tweets = [];
      for (const instance of CONFIG.nitterInstances) {
        tweets = await scrapeTimeline(browser, instance, entry.handle);
        if (tweets.length > 0) {
          console.log(`[INFO] ${entry.name}: ${tweets.length} tweets depuis ${instance}`);
          break;
        }
        await delay(1200);
      }
      results.push({
        speaker: entry.name,
        handle: entry.handle,
        scraped_at: new Date().toISOString(),
        tweets,
      });
      await delay(CONFIG.delayBetweenUsersMs);
    }
  } finally {
    await browser.close();
  }

  const outputPath = path.resolve("FINAL/data/processed/twitter_deputes.jsonl");
  const payload = results.map((item) => JSON.stringify(item)).join("\n");
  await fs.promises.writeFile(outputPath, payload, "utf-8");
  console.log(`[DONE] R?sultats sauvegard?s dans ${outputPath}`);
}

scrapeDeputes().catch((err) => {
  console.error("[ERROR]", err);
  process.exit(1);
});
