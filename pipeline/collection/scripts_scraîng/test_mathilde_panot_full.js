#!/usr/bin/env node
/**
 * Test: Scraper TOUS les tweets de Mathilde Panot depuis 1er janvier 2023
 * Utilise pagination (Load More) comme archive/pocs/nitter-scraper-basics
 * SANS filtrage par mots-clés - on prend tout
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

// ========================================
// CONFIGURATION
// ========================================
const CONFIG = {
  username: "mathildepanot",
  nitterUrl: "https://nitter.net",
  startDate: "2023-01-01",        // Tous les tweets depuis 1er janvier 2023
  maxTweets: 5000,                 // Large limit to get all tweets
  scrollDelay: 1500,
  headless: true,
  slowMo: 0,
  maxConsecutiveFailures: 3,
};

// ========================================
// UTILITIES
// ========================================
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseDate(dateStr) {
  try {
    return new Date(dateStr);
  } catch {
    return null;
  }
}

// ========================================
// EXTRACT TWEETS FROM CURRENT PAGE
// ========================================
async function extractTweets(page) {
  return await page.evaluate(() => {
    const allTweets = document.querySelectorAll(".timeline-item");
    const data = [];

    allTweets.forEach((tweet) => {
      try {
        const fullname = tweet.querySelector(".fullname")?.innerText || "";
        const username = tweet.querySelector(".username")?.innerText || "";
        const dateElement = tweet.querySelector(".tweet-date a");
        const date = dateElement?.getAttribute("title") || "";
        const content = tweet.querySelector(".tweet-content")?.innerText || "";
        const link = dateElement?.getAttribute("href") || "";

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
          link: link ? `https://nitter.net${link}` : "",
          stats: {
            replies,
            retweets,
            quotes,
            likes,
          },
        });
      } catch (error) {
        // Skip problematic tweets
      }
    });

    return data;
  });
}

// ========================================
// CLICK "LOAD MORE" BUTTON
// ========================================
async function clickLoadMore(page) {
  try {
    const allButtons = await page.$$(".show-more a");

    if (allButtons.length === 0) {
      return false;
    }

    let loadMoreButton = null;

    for (const button of allButtons) {
      const buttonText = await page.evaluate((el) => el.innerText, button);
      const buttonHref = await page.evaluate(
        (el) => el.getAttribute("href"),
        button
      );

      if (
        buttonText.toLowerCase().includes("load more") &&
        buttonHref &&
        buttonHref.includes("cursor=")
      ) {
        loadMoreButton = button;
        break;
      }
    }

    if (!loadMoreButton) {
      return false;
    }

    // Scroll to button
    await page.evaluate((button) => {
      button.scrollIntoView({ behavior: "smooth", block: "center" });
    }, loadMoreButton);

    await sleep(500);

    // Wait for navigation after click
    try {
      await Promise.all([
        page.waitForNavigation({ waitUntil: "networkidle2", timeout: 10000 }),
        loadMoreButton.click(),
      ]);
    } catch (navError) {
      await loadMoreButton.click();
      await sleep(CONFIG.scrollDelay);
    }

    // Wait for tweets to reload
    await page.waitForSelector(".timeline-item", { timeout: 5000 });

    return true;
  } catch (error) {
    return false;
  }
}

// ========================================
// MAIN SCRAPING FUNCTION
// ========================================
async function scrapeMathildePanot() {
  const url = `${CONFIG.nitterUrl}/${CONFIG.username}`;
  const targetDate = new Date(CONFIG.startDate);

  console.log("=".repeat(70));
  console.log(`🧪 TEST COMPLET: Mathilde Panot`);
  console.log("=".repeat(70));
  console.log(`👤 Député: @${CONFIG.username}`);
  console.log(`📅 Depuis: ${CONFIG.startDate}`);
  console.log(`🎯 Objectif: TOUS les tweets (max ${CONFIG.maxTweets})`);
  console.log(`📝 Mode: SANS filtrage - on garde tout`);
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

  console.log(`📡 Chargement de ${url}...`);
  await page.goto(url, {
    waitUntil: "networkidle2",
    timeout: 30000,
  });

  await page.waitForSelector(".timeline-item", { timeout: 10000 });
  console.log("✅ Page chargée\n");

  let allTweets = [];
  let iteration = 0;
  let consecutiveFailures = 0;
  let reachedTargetDate = false;

  // PAGINATION LOOP
  while (allTweets.length < CONFIG.maxTweets && !reachedTargetDate) {
    iteration++;
    console.log(`\n--- Itération ${iteration} ---`);

    // Extract current tweets
    const currentTweets = await extractTweets(page);
    console.log(`   📊 ${currentTweets.length} tweets sur la page`);

    // Remove duplicates
    const uniqueTweets = currentTweets.filter(
      (tweet) => !allTweets.some((existing) => existing.link === tweet.link)
    );

    console.log(`   ➕ ${uniqueTweets.length} nouveaux tweets uniques`);

    // Add ALL tweets (no filtering by keywords)
    allTweets.push(...uniqueTweets);

    console.log(`   📈 Total accumulé: ${allTweets.length}`);

    // Check oldest tweet date
    if (currentTweets.length > 0) {
      const oldestTweet = currentTweets[currentTweets.length - 1];
      const oldestDate = parseDate(oldestTweet.date);
      console.log(`   📅 Tweet le plus ancien: ${oldestTweet.date}`);

      // If we've gone past target date, mark and continue one more iteration
      if (oldestDate && oldestDate < targetDate) {
        console.log(`   ⏹️  Atteint la date cible ${CONFIG.startDate}`);
        reachedTargetDate = true;
      }
    }

    // Check if we reached our goal
    if (allTweets.length >= CONFIG.maxTweets) {
      console.log(`\n✅ Limite atteinte: ${allTweets.length} tweets`);
      break;
    }

    // Check if no progress
    if (uniqueTweets.length === 0) {
      consecutiveFailures++;
      console.log(
        `   ⚠️  Aucun nouveau tweet (tentative ${consecutiveFailures}/${CONFIG.maxConsecutiveFailures})`
      );

      if (consecutiveFailures >= CONFIG.maxConsecutiveFailures) {
        console.log("\n⚠️  Aucun nouveau tweet après 3 tentatives, arrêt");
        break;
      }
    } else {
      consecutiveFailures = 0;
    }

    // Try to click "Load more"
    console.log(`   🔄 Clic sur "Load more"...`);
    const hasMore = await clickLoadMore(page);

    if (!hasMore) {
      console.log('\n📭 Plus de bouton "Load more" disponible');
      break;
    }
  }

  await browser.close();

  // Filter tweets to only those after target date
  const filteredByDate = allTweets.filter((tweet) => {
    const tweetDate = parseDate(tweet.date);
    return tweetDate && tweetDate >= targetDate;
  });

  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS FINAUX");
  console.log("=".repeat(70));
  console.log(`✅ Total tweets scrapés: ${allTweets.length}`);
  console.log(`📅 Tweets depuis ${CONFIG.startDate}: ${filteredByDate.length}`);

  if (filteredByDate.length > 0) {
    console.log(`📅 Premier tweet: ${filteredByDate[0].date}`);
    console.log(`📅 Dernier tweet: ${filteredByDate[filteredByDate.length - 1].date}`);

    console.log("\n📖 Aperçu des 5 premiers tweets:");
    filteredByDate.slice(0, 5).forEach((tweet, i) => {
      console.log(`  ${i + 1}. ${tweet.date}`);
      console.log(`     ${tweet.content.substring(0, 80)}...`);
    });

    console.log("\n📖 Aperçu des 5 derniers tweets:");
    filteredByDate.slice(-5).forEach((tweet, i) => {
      console.log(`  ${filteredByDate.length - 4 + i}. ${tweet.date}`);
      console.log(`     ${tweet.content.substring(0, 80)}...`);
    });
  }

  // Save results
  const output = {
    speaker: "Mathilde Panot",
    handle: CONFIG.username,
    group: "LFI-NFP",
    scraped_at: new Date().toISOString(),
    start_date: CONFIG.startDate,
    total_iterations: iteration,
    total_tweets_scraped: allTweets.length,
    tweets_since_start_date: filteredByDate.length,
    tweets: filteredByDate,
  };

  const outputPath = "data/processed/mathilde_panot_full.json";
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf-8");
  console.log(`\n💾 Sauvegardé dans ${outputPath}`);

  // Also save as JSONL
  const jsonlPath = "data/processed/mathilde_panot_full.jsonl";
  const jsonlContent = filteredByDate.map(tweet => JSON.stringify(tweet)).join("\n");
  fs.writeFileSync(jsonlPath, jsonlContent, "utf-8");
  console.log(`💾 Sauvegardé dans ${jsonlPath} (format JSONL)`);

  console.log("=".repeat(70));

  return output;
}

// RUN
scrapeMathildePanot().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
