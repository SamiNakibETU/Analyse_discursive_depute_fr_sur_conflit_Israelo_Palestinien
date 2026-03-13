#!/usr/bin/env node
/**
 * SCRAPER OPTIMISÉ - Mathilde Panot
 * Tous les tweets depuis 1er janvier 2023
 * SANS filtrage - on prend tout
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  username: "mathildepanot",
  nitterUrl: "https://nitter.net",
  targetDate: new Date("2023-01-01"),
  maxIterations: 500,       // Large pour être sûr d'atteindre 2023
  scrollDelay: 6000,        // 6 secondes entre requêtes (éviter 429)
  headless: true,           // Headless
  slowMo: 0,
  retryDelay: 60000,        // 60 secondes si erreur 429
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
          stats: { replies, retweets, quotes, likes },
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
    // Vérifier si erreur 429
    const has429Error = await page.evaluate(() => {
      return document.body.innerText.includes("HTTP ERROR 429") ||
             document.body.innerText.includes("Cette page ne fonctionne pas");
    });

    if (has429Error) {
      console.log(`   ⚠️  Erreur 429 détectée - attente ${CONFIG.retryDelay / 1000}s...`);
      await sleep(CONFIG.retryDelay);
      return "retry";
    }

    // Chercher le bouton avec cursor
    const clicked = await page.evaluate(() => {
      const links = document.querySelectorAll(".show-more a");
      for (const link of links) {
        const text = link.innerText.toLowerCase();
        const href = link.getAttribute("href");
        if (text.includes("load more") && href && href.includes("cursor=")) {
          link.scrollIntoView({ behavior: "smooth", block: "center" });
          link.click();
          return true;
        }
      }
      return false;
    });

    if (!clicked) return false;

    await sleep(1000);

    // Attendre navigation
    try {
      await page.waitForNavigation({ waitUntil: "networkidle2", timeout: 15000 });
    } catch {
      await sleep(CONFIG.scrollDelay);
    }

    // Attendre que les tweets se chargent
    await page.waitForSelector(".timeline-item", { timeout: 10000 });

    // Délai supplémentaire pour éviter rate limit
    await sleep(CONFIG.scrollDelay);

    return true;
  } catch (err) {
    console.log(`   ⚠️  Erreur dans clickLoadMore: ${err.message}`);
    return false;
  }
}

async function main() {
  const url = `${CONFIG.nitterUrl}/${CONFIG.username}`;

  console.log("=".repeat(70));
  console.log(`🔍 SCRAPING OPTIMISÉ: ${CONFIG.username}`);
  console.log("=".repeat(70));
  console.log(`📅 Objectif: Tous les tweets depuis ${CONFIG.targetDate.toISOString().split('T')[0]}`);
  console.log(`🎯 Max itérations: ${CONFIG.maxIterations}`);
  console.log(`📝 Mode: AUCUN FILTRAGE`);
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
  let reachedTargetDate = false;

  // BOUCLE DE PAGINATION
  while (iteration < CONFIG.maxIterations && !reachedTargetDate) {
    iteration++;

    // Affichage tous les 10 itérations
    if (iteration % 10 === 1 || iteration < 5) {
      console.log(`--- Itération ${iteration}/${CONFIG.maxIterations} ---`);
    }

    const currentTweets = await extractTweets(page);
    const unique = currentTweets.filter(
      (t) => !allTweets.some((existing) => existing.link === t.link)
    );
    allTweets.push(...unique);

    if (iteration % 10 === 0 || iteration < 5) {
      console.log(`   📈 Total: ${allTweets.length} tweets`);
      if (currentTweets.length > 0) {
        const oldest = currentTweets[currentTweets.length - 1];
        console.log(`   📅 Plus ancien: ${oldest.date}`);

        // Vérifier date
        const oldestDate = new Date(oldest.date);
        if (!isNaN(oldestDate.getTime()) && oldestDate < CONFIG.targetDate) {
          console.log(`   ✅ ATTEINT LA DATE CIBLE!`);
          reachedTargetDate = true;
        }
      }
    }

    // Sauvegarder tous les 50 itérations
    if (iteration % 50 === 0) {
      const tempOutput = {
        scraping_in_progress: true,
        iteration,
        total_tweets: allTweets.length,
        tweets: allTweets
      };
      fs.writeFileSync(
        "data/processed/mathilde_temp.json",
        JSON.stringify(tempOutput, null, 2),
        "utf-8"
      );
      console.log(`   💾 Sauvegarde intermédiaire (${allTweets.length} tweets)`);
    }

    if (reachedTargetDate) {
      console.log(`\n✅ Date cible atteinte à l'itération ${iteration}`);
      break;
    }

    // Cliquer Load More
    const hasMore = await clickLoadMore(page);
    if (!hasMore) {
      console.log(`\n⚠️  Plus de bouton Load More à l'itération ${iteration}`);
      break;
    }
  }

  await browser.close();

  // Filtrer par date
  const filteredByDate = allTweets.filter((tweet) => {
    const tweetDate = new Date(tweet.date);
    return !isNaN(tweetDate.getTime()) && tweetDate >= CONFIG.targetDate;
  });

  // Compter mots-clés
  const tweetsWithKeywords = filteredByDate.filter(tweet => containsKeyword(tweet.content));

  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS FINAUX");
  console.log("=".repeat(70));
  console.log(`✅ Total iterations: ${iteration}`);
  console.log(`✅ Total tweets scrapés: ${allTweets.length}`);
  console.log(`📅 Tweets depuis ${CONFIG.targetDate.toISOString().split('T')[0]}: ${filteredByDate.length}`);
  console.log(`🔑 Tweets avec mots-clés Gaza/Palestine: ${tweetsWithKeywords.length}`);
  console.log(`📊 Pourcentage: ${((tweetsWithKeywords.length / filteredByDate.length) * 100).toFixed(1)}%`);

  if (filteredByDate.length > 0) {
    console.log(`\n📅 Premier tweet: ${filteredByDate[0].date}`);
    console.log(`📅 Dernier tweet: ${filteredByDate[filteredByDate.length - 1].date}`);
  }

  // Sauvegarder TOUS les tweets
  const output = {
    speaker: "Mathilde Panot",
    handle: CONFIG.username,
    group: "LFI-NFP",
    scraped_at: new Date().toISOString(),
    start_date: CONFIG.targetDate.toISOString().split('T')[0],
    total_iterations: iteration,
    total_tweets_scraped: allTweets.length,
    tweets_in_date_range: filteredByDate.length,
    tweets_with_keywords: tweetsWithKeywords.length,
    percentage_with_keywords: ((tweetsWithKeywords.length / filteredByDate.length) * 100).toFixed(1),
    keywords_searched: CONFIG.keywords,
    tweets: filteredByDate,  // TOUS les tweets depuis 2023
  };

  const outputPath = "data/processed/mathilde_panot_since_2023.json";
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf-8");
  console.log(`\n💾 Sauvegardé: ${outputPath}`);

  const jsonlPath = "data/processed/mathilde_panot_since_2023.jsonl";
  const jsonlContent = filteredByDate.map(tweet => JSON.stringify(tweet)).join("\n");
  fs.writeFileSync(jsonlPath, jsonlContent, "utf-8");
  console.log(`💾 Sauvegardé: ${jsonlPath}`);
  console.log("=".repeat(70));
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
