#!/usr/bin/env node
/**
 * Diagnostic: Capture HTML at working vs failing iterations
 */

const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const CONFIG = {
  nitterUrl: "https://nitter.net",
  username: "mathildepanot",
  scrollDelay: 3000,
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function extractTweetsAndCursor(page) {
  return await page.evaluate(() => {
    const items = document.querySelectorAll(".timeline-item");
    const tweets = [];

    items.forEach((item) => {
      const dateElement = item.querySelector(".tweet-date a");
      const contentElement = item.querySelector(".tweet-content");
      if (dateElement && contentElement) {
        tweets.push({
          date: dateElement.getAttribute("title") || "",
          content: contentElement.innerText.substring(0, 50),
          url: dateElement.getAttribute("href") || "",
        });
      }
    });

    // Find Load More button and extract cursor
    let nextCursor = null;
    const loadMoreLinks = document.querySelectorAll(".show-more a");
    for (const link of loadMoreLinks) {
      const text = link.innerText.toLowerCase();
      const href = link.getAttribute("href");
      if (text.includes("load more") && href && href.includes("cursor=")) {
        const match = href.match(/cursor=([^&]+)/);
        if (match) nextCursor = match[1];
        break;
      }
    }

    return { tweets, nextCursor };
  });
}

async function captureHtmlAtIteration(page, iteration, cursor) {
  console.log(`\n📸 Capture à l'itération ${iteration}`);

  const url = cursor
    ? `${CONFIG.nitterUrl}/${CONFIG.username}?cursor=${cursor}`
    : `${CONFIG.nitterUrl}/${CONFIG.username}`;

  console.log(`   URL: ${url}`);

  await page.goto(url, {
    waitUntil: "networkidle2",
    timeout: 30000,
  });

  await page.waitForSelector(".timeline-item", { timeout: 10000 });
  await sleep(CONFIG.scrollDelay);

  const { tweets, nextCursor } = await extractTweetsAndCursor(page);

  console.log(`   Tweets: ${tweets.length}`);
  console.log(`   Plus ancien: ${tweets[tweets.length - 1]?.date || "N/A"}`);
  console.log(`   Cursor trouvé: ${nextCursor ? "OUI" : "NON"}`);

  // Capture HTML
  const html = await page.content();
  const htmlPath = path.resolve(`logs/html_iteration_${iteration}.html`);
  await fs.promises.writeFile(htmlPath, html, "utf-8");
  console.log(`   💾 HTML sauvegardé: ${htmlPath}`);

  // Extract .show-more section
  const showMoreHtml = await page.evaluate(() => {
    const showMore = document.querySelector(".show-more");
    return showMore ? showMore.outerHTML : "❌ Element .show-more NOT FOUND";
  });

  console.log(`\n   .show-more HTML:\n${showMoreHtml}\n`);

  return { tweets, nextCursor };
}

async function main() {
  console.log("======================================================================");
  console.log("🔬 DIAGNOSTIC: Capture HTML aux points critiques");
  console.log("======================================================================\n");

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  );

  let allTweets = [];
  let currentCursor = null;

  // Iterate to iteration 10 (working)
  console.log("=== Phase 1: Itérations 1-10 (zone fonctionnelle) ===");
  for (let i = 1; i <= 10; i++) {
    const result = await captureHtmlAtIteration(page, i, currentCursor);
    allTweets.push(...result.tweets);

    if (!result.nextCursor) {
      console.log(`\n⚠️ ARRÊT PRÉMATURÉ à l'itération ${i} - Pas de cursor\n`);
      break;
    }

    currentCursor = result.nextCursor;

    // Save HTML only at iteration 10
    if (i === 10) {
      console.log(`\n✅ Itération 10 COMPLÉTÉE - HTML sauvegardé comme référence\n`);
    }

    await sleep(CONFIG.scrollDelay);
  }

  // Continue to iteration 41-44 (failing zone)
  console.log("\n=== Phase 2: Itérations 11-44 (zone de blocage) ===");
  for (let i = 11; i <= 45; i++) {
    const result = await captureHtmlAtIteration(page, i, currentCursor);
    allTweets.push(...result.tweets);

    if (!result.nextCursor) {
      console.log(`\n❌ BLOCAGE à l'itération ${i} - Pas de cursor`);
      console.log(`   Total tweets accumulés: ${allTweets.length}`);
      console.log(`   HTML de cette itération sauvegardé pour analyse\n`);
      break;
    }

    currentCursor = result.nextCursor;
    await sleep(CONFIG.scrollDelay);
  }

  await browser.close();

  console.log("\n======================================================================");
  console.log("📊 RÉSUMÉ DIAGNOSTIC");
  console.log("======================================================================");
  console.log(`Total tweets collectés: ${allTweets.length}`);
  console.log(`Plus récent: ${allTweets[0]?.date || "N/A"}`);
  console.log(`Plus ancien: ${allTweets[allTweets.length - 1]?.date || "N/A"}`);
  console.log("\n💡 Fichiers HTML générés dans logs/ pour comparaison");
  console.log("======================================================================");
}

main().catch((err) => {
  console.error("❌ Erreur:", err);
  process.exit(1);
});
