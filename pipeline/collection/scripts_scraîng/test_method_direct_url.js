#!/usr/bin/env node
/**
 * MÉTHODE 1: Navigation directe via URL cursor
 * Au lieu de cliquer, extraire le cursor et naviguer directement
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  username: "mathildepanot",
  nitterUrl: "https://nitter.net",
  targetDate: new Date("2023-01-01"),
  maxIterations: 300,
  delayBetweenRequests: 4000,
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function extractTweetsAndCursor(page) {
  return await page.evaluate(() => {
    const tweets = [];
    const items = document.querySelectorAll(".timeline-item");

    items.forEach((tweet) => {
      try {
        const dateElement = tweet.querySelector(".tweet-date a");
        const date = dateElement?.getAttribute("title") || "";
        const content = tweet.querySelector(".tweet-content")?.innerText || "";
        const link = dateElement?.getAttribute("href") || "";

        const statsElements = tweet.querySelectorAll(".tweet-stat");
        tweets.push({
          date,
          content,
          link: link ? `https://nitter.net${link}` : "",
          stats: {
            replies: statsElements[0]?.innerText.trim() || "0",
            retweets: statsElements[1]?.innerText.trim() || "0",
            quotes: statsElements[2]?.innerText.trim() || "0",
            likes: statsElements[3]?.innerText.trim() || "0",
          }
        });
      } catch (e) {}
    });

    // Extraire le cursor du bouton "Load more"
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

async function main() {
  console.log("=".repeat(70));
  console.log("🧪 MÉTHODE 1: Navigation directe via URL cursor");
  console.log("=".repeat(70));

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  );

  let allTweets = [];
  let iteration = 0;
  let currentUrl = `${CONFIG.nitterUrl}/${CONFIG.username}`;
  let reachedTarget = false;

  while (iteration < CONFIG.maxIterations && !reachedTarget) {
    iteration++;

    if (iteration % 10 === 1 || iteration <= 5) {
      console.log(`\n--- Itération ${iteration}/${CONFIG.maxIterations} ---`);
      console.log(`   🔗 ${currentUrl.substring(0, 80)}...`);
    }

    // Naviguer vers l'URL
    await page.goto(currentUrl, {
      waitUntil: "networkidle2",
      timeout: 30000
    });
    await page.waitForSelector(".timeline-item", { timeout: 10000 });

    // Extraire tweets et cursor
    const { tweets, nextCursor } = await extractTweetsAndCursor(page);

    const unique = tweets.filter(
      (t) => !allTweets.some((existing) => existing.link === t.link)
    );
    allTweets.push(...unique);

    if (iteration % 10 === 0 || iteration <= 5) {
      console.log(`   📊 ${tweets.length} tweets page, ${unique.length} nouveaux`);
      console.log(`   📈 Total: ${allTweets.length}`);

      if (tweets.length > 0) {
        const oldest = tweets[tweets.length - 1];
        console.log(`   📅 Plus ancien: ${oldest.date}`);

        const oldestDate = new Date(oldest.date);
        if (!isNaN(oldestDate.getTime()) && oldestDate < CONFIG.targetDate) {
          console.log(`   ✅ DATE CIBLE ATTEINTE!`);
          reachedTarget = true;
        }
      }

      console.log(`   🔑 Next cursor: ${nextCursor ? "✓" : "✗"}`);
    }

    // Sauvegardes périodiques
    if (iteration % 50 === 0) {
      const temp = {
        iteration,
        total: allTweets.length,
        oldest: allTweets[allTweets.length - 1]?.date,
        tweets: allTweets
      };
      fs.writeFileSync(
        "data/processed/test_method1_temp.json",
        JSON.stringify(temp, null, 2),
        "utf-8"
      );
      console.log(`   💾 Sauvegarde: ${allTweets.length} tweets`);
    }

    if (!nextCursor) {
      console.log(`\n❌ Aucun cursor trouvé - arrêt`);
      break;
    }

    if (reachedTarget) break;

    // Construire prochaine URL
    currentUrl = `${CONFIG.nitterUrl}/${CONFIG.username}?cursor=${nextCursor}`;

    // Délai entre requêtes
    await sleep(CONFIG.delayBetweenRequests);
  }

  await browser.close();

  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS MÉTHODE 1");
  console.log("=".repeat(70));
  console.log(`✅ Iterations: ${iteration}`);
  console.log(`✅ Total tweets: ${allTweets.length}`);
  if (allTweets.length > 0) {
    console.log(`📅 Plus récent: ${allTweets[0].date}`);
    console.log(`📅 Plus ancien: ${allTweets[allTweets.length - 1].date}`);
  }

  const output = {
    method: "direct_url_navigation",
    iterations: iteration,
    total_tweets: allTweets.length,
    tweets: allTweets
  };

  fs.writeFileSync(
    "data/processed/test_method1_results.json",
    JSON.stringify(output, null, 2),
    "utf-8"
  );
  console.log("\n💾 Sauvegardé: data/processed/test_method1_results.json");
  console.log("=".repeat(70));
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
