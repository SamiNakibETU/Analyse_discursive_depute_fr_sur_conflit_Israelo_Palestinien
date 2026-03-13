#!/usr/bin/env node
/**
 * Test scraping for ONE député with pagination (Load More)
 * Based on working archive/pocs/nitter-scraper-basics
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

// ========================================
// CONFIGURATION
// ========================================
const CONFIG = {
  username: "mathildepanot",      // Test avec Mathilde Panot (LFI-NFP)
  nitterUrl: "https://nitter.net",
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
  startDate: "2023-10-07",        // Gaza war started Oct 7, 2023
  maxTweets: 50,                   // Reduce to 50 for faster testing
  maxIterations: 200,              // Stop after 200 iterations max
  scrollDelay: 1500,               // Faster scrolling
  headless: true,                  // Headless for speed
  slowMo: 0,                       // No slowMo for speed
};

// ========================================
// UTILITIES
// ========================================
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function containsKeyword(text) {
  const lower = (text || "").toLowerCase();
  return CONFIG.keywords.some((kw) => lower.includes(kw.toLowerCase()));
}

function parseDate(dateStr) {
  // Parse Nitter date format: "Dec 25, 2024 · 10:30 AM UTC"
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

    allTweets.forEach((tweet, index) => {
      try {
        const fullname = tweet.querySelector(".fullname")?.innerText || "";
        const username = tweet.querySelector(".username")?.innerText || "";
        const dateElement = tweet.querySelector(".tweet-date a");
        const date = dateElement?.getAttribute("title") || "";
        const content = tweet.querySelector(".tweet-content")?.innerText || "";
        const link = dateElement?.getAttribute("href") || "";

        // Stats extraction (using .tweet-stat like working scraper)
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
        console.error(`⚠️ Erreur extraction tweet #${index + 1}`);
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
    // Find all buttons in .show-more
    const allButtons = await page.$$(".show-more a");

    if (allButtons.length === 0) {
      console.log("   📭 Aucun bouton trouvé");
      return false;
    }

    console.log(`   🔍 ${allButtons.length} bouton(s) trouvé(s)`);

    // Find "Load more" button with cursor
    let loadMoreButton = null;

    for (const button of allButtons) {
      const buttonText = await page.evaluate((el) => el.innerText, button);
      const buttonHref = await page.evaluate(
        (el) => el.getAttribute("href"),
        button
      );

      // Look for "Load more" with cursor parameter
      if (
        buttonText.toLowerCase().includes("load more") &&
        buttonHref &&
        buttonHref.includes("cursor=")
      ) {
        loadMoreButton = button;
        console.log(`   ✅ Bouton "Load more" identifié !`);
        break;
      }
    }

    if (!loadMoreButton) {
      console.log('   ⚠️ Aucun bouton "Load more" valide trouvé');
      return false;
    }

    console.log('   🔄 Clic sur "Load more"...');

    // Scroll to button
    await page.evaluate((button) => {
      button.scrollIntoView({ behavior: "smooth", block: "center" });
    }, loadMoreButton);

    await sleep(500);

    // CRITICAL: Wait for navigation after click
    try {
      await Promise.all([
        page.waitForNavigation({ waitUntil: "networkidle2", timeout: 10000 }),
        loadMoreButton.click(),
      ]);
      console.log("   ✅ Navigation complétée");
    } catch (navError) {
      // Sometimes no navigation, just AJAX loading
      console.log("   ⚠️ Pas de navigation détectée, attente simple...");
      await loadMoreButton.click();
      await sleep(CONFIG.scrollDelay);
    }

    // Wait for tweets to load
    await page.waitForSelector(".timeline-item", { timeout: 5000 });
    console.log(`   ✅ Tweets rechargés`);

    return true;
  } catch (error) {
    console.log("   ⚠️ Erreur lors du clic :", error.message);
    return false;
  }
}

// ========================================
// MAIN SCRAPING FUNCTION
// ========================================
async function scrapeOneDepute() {
  const url = `${CONFIG.nitterUrl}/${CONFIG.username}`;

  console.log("=".repeat(70));
  console.log(`🧪 TEST SCRAPING - UN DÉPUTÉ`);
  console.log("=".repeat(70));
  console.log(`👤 Député: @${CONFIG.username}`);
  console.log(`🎯 Objectif: ${CONFIG.maxTweets} tweets max`);
  console.log(`📅 Depuis: ${CONFIG.startDate}`);
  console.log(`🔑 Mots-clés: ${CONFIG.keywords.join(", ")}`);
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
  let filteredTweets = [];
  let iteration = 0;
  let consecutiveFailures = 0;
  const targetDate = new Date(CONFIG.startDate);

  // PAGINATION LOOP
  while (filteredTweets.length < CONFIG.maxTweets && iteration < CONFIG.maxIterations) {
    iteration++;
    console.log(`\n--- Itération ${iteration}/${CONFIG.maxIterations} ---`);

    // Extract current tweets
    const currentTweets = await extractTweets(page);
    console.log(`   📊 ${currentTweets.length} tweets sur la page`);

    // Remove duplicates
    const uniqueTweets = currentTweets.filter(
      (tweet) => !allTweets.some((existing) => existing.link === tweet.link)
    );

    console.log(`   ➕ ${uniqueTweets.length} nouveaux tweets uniques`);

    // Add to collection
    allTweets.push(...uniqueTweets);

    // Filter by keywords and date
    const newFiltered = uniqueTweets.filter((tweet) => {
      const matchesKeyword = containsKeyword(tweet.content);
      const tweetDate = parseDate(tweet.date);
      const afterTargetDate = tweetDate && tweetDate >= targetDate;
      return matchesKeyword && afterTargetDate;
    });

    filteredTweets.push(...newFiltered);

    console.log(`   🔑 ${newFiltered.length} tweets avec mots-clés Gaza/Palestine`);
    console.log(`   📈 Total filtré: ${filteredTweets.length}/${CONFIG.maxTweets}`);

    // Check if we reached our goal
    if (filteredTweets.length >= CONFIG.maxTweets) {
      console.log(`\n✅ Objectif atteint: ${filteredTweets.length} tweets`);
      break;
    }

    // Check oldest tweet date
    if (currentTweets.length > 0) {
      const oldestTweet = currentTweets[currentTweets.length - 1];
      const oldestDate = parseDate(oldestTweet.date);
      console.log(`   📅 Tweet le plus ancien: ${oldestTweet.date}`);

      // If we've gone past our target date, stop
      if (oldestDate && oldestDate < targetDate) {
        console.log(`\n⏹️  Atteint la date cible ${CONFIG.startDate}`);
        break;
      }
    }

    // Check if no progress
    const previousTotal = allTweets.length - uniqueTweets.length;
    if (uniqueTweets.length === 0) {
      consecutiveFailures++;
      console.log(
        `   ⚠️ Aucun nouveau tweet (tentative ${consecutiveFailures}/3)`
      );

      if (consecutiveFailures >= 3) {
        console.log("\n⚠️ Aucun nouveau tweet après 3 tentatives, arrêt");
        break;
      }
    } else {
      consecutiveFailures = 0;
    }

    // Try to click "Load more"
    const hasMore = await clickLoadMore(page);

    if (!hasMore) {
      console.log('\n📭 Plus de bouton "Load more" disponible');
      break;
    }
  }

  await browser.close();

  // Limit to max requested
  filteredTweets = filteredTweets.slice(0, CONFIG.maxTweets);

  // Final results
  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS FINAUX");
  console.log("=".repeat(70));
  console.log(`✅ Total tweets scrapés: ${allTweets.length}`);
  console.log(`🔑 Tweets avec mots-clés Gaza/Palestine: ${filteredTweets.length}`);

  if (filteredTweets.length > 0) {
    console.log(`📅 Premier tweet: ${filteredTweets[0].date}`);
    console.log(`📅 Dernier tweet: ${filteredTweets[filteredTweets.length - 1].date}`);

    console.log("\n📖 Aperçu des 3 premiers tweets:");
    filteredTweets.slice(0, 3).forEach((tweet, i) => {
      console.log(`  ${i + 1}. ${tweet.date}`);
      console.log(`     ${tweet.content.substring(0, 100)}...`);
    });
  }

  // Save results
  const output = {
    speaker: "Mathilde Panot",
    handle: CONFIG.username,
    group: "LFI-NFP",
    scraped_at: new Date().toISOString(),
    total_tweets_seen: allTweets.length,
    filtered_tweets_count: filteredTweets.length,
    tweets: filteredTweets,
  };

  const outputPath = "data/processed/test_one_depute.json";
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf-8");
  console.log(`\n💾 Sauvegardé dans ${outputPath}`);
  console.log("=".repeat(70));

  return output;
}

// RUN
scrapeOneDepute().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
