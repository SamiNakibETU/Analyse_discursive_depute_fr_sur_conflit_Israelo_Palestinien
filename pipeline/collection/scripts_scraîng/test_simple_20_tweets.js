#!/usr/bin/env node
/**
 * Simple test: scrape last 20 tweets from Mathilde Panot
 * No filtering, just raw extraction
 * Based on archive/pocs/nitter-scraper-basics/scraper-debug.js
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  url: "https://nitter.net/mathildepanot",
  headless: false,
  slowMo: 50,
};

async function extractTweets(page) {
  return await page.evaluate(() => {
    const allTweets = document.querySelectorAll(".timeline-item");
    const data = [];

    allTweets.forEach((tweet, index) => {
      try {
        const nom = tweet.querySelector(".fullname")?.innerText || "";
        const username = tweet.querySelector(".username")?.innerText || "";
        const date =
          tweet.querySelector(".tweet-date a")?.getAttribute("title") || "";
        const contenu = tweet.querySelector(".tweet-content")?.innerText || "";
        const lien =
          tweet.querySelector(".tweet-link")?.getAttribute("href") || "";

        const statsElements = tweet.querySelectorAll(".tweet-stat");
        const commentaires = statsElements[0]?.innerText.trim() || "0";
        const retweets = statsElements[1]?.innerText.trim() || "0";
        const citations = statsElements[2]?.innerText.trim() || "0";
        const likes = statsElements[3]?.innerText.trim() || "0";

        data.push({
          nom,
          username,
          date,
          contenu,
          lien: lien ? `https://nitter.net${lien}` : "",
          commentaires,
          retweets,
          citations,
          likes,
        });
      } catch (error) {
        console.error(`⚠️  Erreur extraction tweet #${index + 1}`);
      }
    });

    return data;
  });
}

async function main() {
  console.log("=".repeat(70));
  console.log("🧪 TEST SIMPLE: 20 DERNIERS TWEETS");
  console.log("=".repeat(70));
  console.log(`👤 Député: Mathilde Panot (@mathildepanot)`);
  console.log(`📡 URL: ${CONFIG.url}`);
  console.log("=".repeat(70) + "\n");

  const browser = await puppeteer.launch({
    headless: CONFIG.headless,
    slowMo: CONFIG.slowMo,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  );

  console.log(`📡 Chargement de ${CONFIG.url}...`);
  await page.goto(CONFIG.url, {
    waitUntil: "networkidle2",
    timeout: 30000,
  });

  await page.waitForSelector(".timeline-item", { timeout: 10000 });
  console.log("✅ Page chargée\n");

  // Extract tweets
  const tweets = await extractTweets(page);

  await browser.close();

  console.log(`📊 ${tweets.length} tweets extraits\n`);

  // Show all tweets
  console.log("=" + "=".repeat(70));
  console.log("📖 TOUS LES TWEETS:");
  console.log("=".repeat(70));

  tweets.forEach((tweet, index) => {
    console.log(`\n[${index + 1}/${tweets.length}] ${tweet.date}`);
    console.log(`👤 ${tweet.nom} ${tweet.username}`);
    console.log(`💬 ${tweet.contenu.substring(0, 150)}${tweet.contenu.length > 150 ? '...' : ''}`);
    console.log(`🔗 ${tweet.lien}`);
    console.log(`📊 💬 ${tweet.commentaires} | 🔄 ${tweet.retweets} | 💬 ${tweet.citations} | ❤️  ${tweet.likes}`);

    // Check for Gaza/Palestine keywords
    const keywords = ["gaza", "palestine", "israël", "israel", "hamas", "otage"];
    const hasKeyword = keywords.some(kw =>
      tweet.contenu.toLowerCase().includes(kw)
    );
    if (hasKeyword) {
      console.log(`🔑 ✅ CONTIENT MOT-CLÉ GAZA/PALESTINE!`);
    }
  });

  console.log("\n" + "=".repeat(70));

  // Count keywords
  const keywordTweets = tweets.filter(tweet => {
    const keywords = ["gaza", "palestine", "israël", "israel", "hamas", "otage"];
    return keywords.some(kw => tweet.contenu.toLowerCase().includes(kw));
  });

  console.log(`\n📊 RÉSUMÉ:`);
  console.log(`   Total tweets: ${tweets.length}`);
  console.log(`   Avec mots-clés Gaza/Palestine: ${keywordTweets.length}`);
  console.log("=".repeat(70));

  // Save
  const output = {
    scraper: "test_simple_20_tweets",
    url: CONFIG.url,
    scraped_at: new Date().toISOString(),
    total_tweets: tweets.length,
    tweets_with_keywords: keywordTweets.length,
    tweets: tweets,
  };

  const outputPath = "data/processed/test_simple_20.json";
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf-8");
  console.log(`\n💾 Sauvegardé dans ${outputPath}`);
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
