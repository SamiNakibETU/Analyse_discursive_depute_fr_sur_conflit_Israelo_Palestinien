#!/usr/bin/env node
/**
 * Scraper TOUS les tweets disponibles sur Nitter pour Mathilde Panot
 * SANS FILTRAGE - on garde tout
 * Puis on compte combien mentionnent Gaza/Palestine
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  username: "mathildepanot",
  nitterUrl: "https://nitter.net",
  maxIterations: 1000,         // Très haut pour atteindre 2023 - limite par date
  scrollDelay: 2500,           // Plus de temps entre chaque scroll
  headless: true,              // Headless pour vitesse
  slowMo: 0,
  keywords: [
    "gaza", "palestine", "israel", "israël", "hamas",
    "otage", "otages", "cessez-le-feu", "rafah",
    "cisjordanie", "apartheid"
  ],
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function containsKeyword(text) {
  const lower = (text || "").toLowerCase();
  return CONFIG.keywords.some((kw) => lower.includes(kw.toLowerCase()));
}

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
        // Skip
      }
    });

    return data;
  });
}

async function clickLoadMore(page) {
  try {
    const allButtons = await page.$$(".show-more a");
    if (allButtons.length === 0) return false;

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

    if (!loadMoreButton) return false;

    await page.evaluate((button) => {
      button.scrollIntoView({ behavior: "smooth", block: "center" });
    }, loadMoreButton);

    await sleep(500);

    try {
      await Promise.all([
        page.waitForNavigation({ waitUntil: "networkidle2", timeout: 10000 }),
        loadMoreButton.click(),
      ]);
    } catch {
      await loadMoreButton.click();
      await sleep(CONFIG.scrollDelay);
    }

    await page.waitForSelector(".timeline-item", { timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

async function main() {
  const url = `${CONFIG.nitterUrl}/${CONFIG.username}`;

  console.log("=".repeat(70));
  console.log(`🔍 SCRAPING COMPLET: Mathilde Panot`);
  console.log("=".repeat(70));
  console.log(`👤 @${CONFIG.username}`);
  console.log(`📝 Mode: AUCUN FILTRAGE - tous les tweets disponibles sur Nitter`);
  console.log(`🎯 Max itérations: ${CONFIG.maxIterations}`);
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
  await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
  await page.waitForSelector(".timeline-item", { timeout: 10000 });
  console.log("✅ Page chargée\n");

  let allTweets = [];
  let iteration = 0;
  let consecutiveFailures = 0;
  const targetDate = new Date("2023-01-01");
  let reachedTargetDate = false;

  // BOUCLE DE PAGINATION - continue jusqu'à la date cible
  while (iteration < CONFIG.maxIterations && !reachedTargetDate) {
    iteration++;
    console.log(`--- Itération ${iteration}/${CONFIG.maxIterations} ---`);

    const currentTweets = await extractTweets(page);
    console.log(`   📊 ${currentTweets.length} tweets sur la page`);

    const uniqueTweets = currentTweets.filter(
      (tweet) => !allTweets.some((existing) => existing.link === tweet.link)
    );

    console.log(`   ➕ ${uniqueTweets.length} nouveaux tweets`);
    allTweets.push(...uniqueTweets);
    console.log(`   📈 Total: ${allTweets.length} tweets`);

    if (currentTweets.length > 0) {
      const oldest = currentTweets[currentTweets.length - 1];
      console.log(`   📅 Plus ancien: ${oldest.date}`);

      // Vérifier si on a atteint la date cible
      const oldestDate = new Date(oldest.date);
      if (!isNaN(oldestDate.getTime()) && oldestDate < targetDate) {
        console.log(`   ✅ Atteint la date cible (1er janvier 2023)`);
        reachedTargetDate = true;
        // Continue encore une itération pour être sûr
      }
    }

    if (uniqueTweets.length === 0) {
      consecutiveFailures++;
      if (consecutiveFailures >= 5) {
        console.log("\n⚠️  Aucun nouveau tweet après 5 tentatives");
        break;
      }
    } else {
      consecutiveFailures = 0;
    }

    if (!reachedTargetDate) {
      console.log(`   🔄 Clic sur "Load more"...`);
      const hasMore = await clickLoadMore(page);

      if (!hasMore) {
        console.log('\n📭 Plus de bouton "Load more"');
        break;
      }
    }
  }

  await browser.close();

  // Analyse des mots-clés
  const tweetsWithKeywords = allTweets.filter(tweet => containsKeyword(tweet.content));

  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS");
  console.log("=".repeat(70));
  console.log(`✅ Total tweets scrapés: ${allTweets.length}`);
  console.log(`🔑 Tweets mentionnant Gaza/Palestine: ${tweetsWithKeywords.length}`);
  console.log(`📊 Pourcentage: ${((tweetsWithKeywords.length / allTweets.length) * 100).toFixed(1)}%`);

  if (allTweets.length > 0) {
    console.log(`\n📅 Premier tweet: ${allTweets[0].date}`);
    console.log(`📅 Dernier tweet: ${allTweets[allTweets.length - 1].date}`);
  }

  console.log("\n🔑 Aperçu tweets avec mots-clés Gaza/Palestine:");
  tweetsWithKeywords.slice(0, 5).forEach((tweet, i) => {
    console.log(`\n  ${i + 1}. ${tweet.date}`);
    console.log(`     ${tweet.content.substring(0, 100)}...`);
  });

  // Sauvegarder TOUS les tweets (sans filtrage)
  const output = {
    speaker: "Mathilde Panot",
    handle: CONFIG.username,
    group: "LFI-NFP",
    scraped_at: new Date().toISOString(),
    total_iterations: iteration,
    total_tweets: allTweets.length,
    tweets_with_keywords: tweetsWithKeywords.length,
    percentage_with_keywords: ((tweetsWithKeywords.length / allTweets.length) * 100).toFixed(1),
    keywords_searched: CONFIG.keywords,
    tweets: allTweets,  // TOUS les tweets
  };

  const outputPath = "data/processed/mathilde_panot_all_tweets.json";
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf-8");
  console.log(`\n💾 Sauvegardé: ${outputPath}`);

  // Aussi en JSONL
  const jsonlPath = "data/processed/mathilde_panot_all_tweets.jsonl";
  const jsonlContent = allTweets.map(tweet => JSON.stringify(tweet)).join("\n");
  fs.writeFileSync(jsonlPath, jsonlContent, "utf-8");
  console.log(`💾 Sauvegardé: ${jsonlPath}`);

  console.log("=".repeat(70));
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
