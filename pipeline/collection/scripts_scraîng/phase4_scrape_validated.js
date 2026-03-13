#!/usr/bin/env node
/**
 * Phase 4 : Scraping Complet des Comptes Validés
 * Scraper Twitter (via Nitter) pour les députés validés : Gaza/Palestine
 */

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const CONFIG = {
  nitterInstances: [
    "https://nitter.net",           // ✅ Working (200 OK) - Instance unique
  ],
  keywords: [
    "gaza",
    "palestine",
    "israel",
    "israël",
    "hamas",
    "otage",
    "otages",
    "cessez-le-feu",
    "rafah",
    "cisjordanie",
    "apartheid",
  ],
  maxTweetsPerUser: 100,
  scrollDelayMs: 2500,
  timeoutMs: 40000,
  delayBetweenUsersMs: 2000,
  testMode: false,             // ✅ MODE PRODUCTION: Scraper tous les députés
  testModeLimit: 5,            // Nombre de députés à tester (si testMode=true)
};

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function loadJson(pathname) {
  const abs = path.resolve(pathname);
  return JSON.parse(await fs.promises.readFile(abs, "utf-8"));
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
    console.warn(`[WARN] Navigation échouée ${url}: ${err.message}`);
    return false;
  }
}

async function scrapeTimeline(browser, instance, username) {
  const page = await browser.newPage();
  const collected = [];

  try {
    const profileUrl = `${instance.replace(/\/$/, "")}/${username}`;

    // Set user agent (like working scraper)
    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    );

    // Navigate to profile
    await page.goto(profileUrl, {
      waitUntil: "networkidle2",
      timeout: CONFIG.timeoutMs
    });

    // Wait for timeline to load (with try-catch)
    try {
      await page.waitForSelector(".timeline-item", { timeout: 10000 });
    } catch (waitError) {
      console.log(`      ⚠️  Timeout waiting for .timeline-item`);
      return [];
    }

    await delay(CONFIG.scrollDelayMs);

    // Extract tweets using working selector pattern
    const tweets = await page.evaluate(() => {
      const allTweets = document.querySelectorAll(".timeline-item");
      const data = [];

      allTweets.forEach((tweet) => {
        try {
          const fullname = tweet.querySelector(".fullname")?.innerText || "";
          const username = tweet.querySelector(".username")?.innerText || "";
          const dateElement = tweet.querySelector(".tweet-date a");
          const date = dateElement?.getAttribute("title") || "";
          const content = tweet.querySelector(".tweet-content")?.innerText || "";
          const url = dateElement?.getAttribute("href") || "";

          // Stats extraction using .tweet-stat (working approach)
          const statsElements = tweet.querySelectorAll(".tweet-stat");
          const replies = statsElements[0]?.innerText.trim() || "0";
          const retweets = statsElements[1]?.innerText.trim() || "0";
          const quotes = statsElements[2]?.innerText.trim() || "0";
          const likes = statsElements[3]?.innerText.trim() || "0";

          data.push({
            fullname,
            username,
            date,
            content,
            url: url ? `https://nitter.net${url}` : "",
            stats: {
              replies,
              retweets,
              quotes,
              likes,
            },
          });
        } catch (error) {
          console.error("Error extracting tweet");
        }
      });

      return data;
    });

    // Filter by keywords
    for (const tweet of tweets) {
      if (containsKeyword(tweet.content)) {
        collected.push(tweet);
      }
    }

  } finally {
    await page.close();
  }

  return collected;
}

async function scrapeValidatedDeputes() {
  // Charger députés uniques et mapping Twitter
  const deputesData = await loadJson("data/interim/deputes_unique.json");
  const deputes = deputesData.deputes || [];

  const twitterMapping = await loadJson("config/twitter_handles.json");

  // Créer liste des députés avec Twitter
  const validatedAccounts = deputes
    .filter(dep => twitterMapping[dep.name])
    .map(dep => ({
      depute_name: dep.name,
      validated_username: twitterMapping[dep.name],
      group: dep.group,
      priority_score: dep.priority_score
    }));

  // Appliquer limite si en mode test
  const accountsToScrape = CONFIG.testMode
    ? validatedAccounts.slice(0, CONFIG.testModeLimit)
    : validatedAccounts;

  console.log("\n" + "=".repeat(70));
  if (CONFIG.testMode) {
    console.log(`🧪 MODE TEST ACTIVÉ - Scraping de ${accountsToScrape.length} députés`);
  } else {
    console.log(`📊 MODE PRODUCTION - Scraping de ${accountsToScrape.length} députés`);
  }
  console.log(`[INFO] ${validatedAccounts.length} comptes validés au total (depuis twitter_handles.json)`);
  console.log("=".repeat(70) + "\n");

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });

  console.log("✅ Browser Puppeteer lancé\n");

  const results = [];
  let processed = 0;
  let totalTweetsFound = 0;

  try {
    for (const entry of accountsToScrape) {
      processed += 1;
      const username = entry.validated_username;
      const name = entry.depute_name;

      console.log("\n" + "-".repeat(70));
      console.log(`[${processed}/${accountsToScrape.length}] 🔍 ${name} (@${username})`);
      console.log(`   Groupe: ${entry.group || "N/A"}`);

      let tweets = [];

      // Essayer instances Nitter dans l'ordre
      for (const instance of CONFIG.nitterInstances) {
        console.log(`   ⏳ Scraping depuis ${instance}...`);
        tweets = await scrapeTimeline(browser, instance, username);
        if (tweets.length > 0) {
          console.log(`   ✅ ${tweets.length} tweets trouvés (filtrés par mots-clés Gaza/Palestine)`);
          totalTweetsFound += tweets.length;
          break;
        } else {
          console.log(`   ⚠️  Aucun tweet trouvé avec les mots-clés`);
        }
        await delay(1200);
      }

      results.push({
        speaker: name,
        handle: username,
        group: entry.group,
        scraped_at: new Date().toISOString(),
        tweets,
      });

      console.log(`   📊 Progression: ${totalTweetsFound} tweets au total`);
      console.log("-".repeat(70));

      await delay(CONFIG.delayBetweenUsersMs);
    }
  } finally {
    await browser.close();
  }

  const outputPath = path.resolve("data/processed/twitter_deputes_final.jsonl");
  const payload = results.map((item) => JSON.stringify(item)).join("\n");
  await fs.promises.writeFile(outputPath, payload, "utf-8");

  console.log(`\n💾 Résultats sauvegardés dans ${outputPath}`);

  // Stats finales
  const totalTweets = results.reduce((sum, r) => sum + r.tweets.length, 0);
  const accountsWithTweets = results.filter(r => r.tweets.length > 0).length;

  console.log("\n" + "=".repeat(70));
  console.log("📊 STATISTIQUES FINALES");
  console.log("=".repeat(70));
  console.log(`   Comptes scrapés : ${results.length}`);
  console.log(`   Comptes avec tweets Gaza/Palestine : ${accountsWithTweets}`);
  console.log(`   Total tweets trouvés : ${totalTweets}`);
  console.log(`   Moyenne : ${(totalTweets / results.length).toFixed(1)} tweets/compte`);
  if (CONFIG.testMode) {
    console.log(`\n   ⚠️  MODE TEST - Seuls ${CONFIG.testModeLimit} députés ont été scrapés`);
    console.log(`   Pour scraper tous les ${validatedAccounts.length} comptes, mettez testMode: false`);
  }
  console.log("=".repeat(70));
}

scrapeValidatedDeputes().catch((err) => {
  console.error("[ERROR]", err);
  process.exit(1);
});
