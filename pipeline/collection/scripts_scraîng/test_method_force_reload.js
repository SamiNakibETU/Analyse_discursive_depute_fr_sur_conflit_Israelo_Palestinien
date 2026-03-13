#!/usr/bin/env node
/**
 * MÉTHODE 2: Forcer le rechargement et attente plus longue
 * Parfois le bouton n'apparaît pas car DOM pas prêt
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  username: "mathildepanot",
  nitterUrl: "https://nitter.net",
  targetDate: new Date("2023-01-01"),
  maxIterations: 300,
  delayBetweenRequests: 5000,
  reloadIfNoButton: true,
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function extractTweets(page) {
  return await page.evaluate(() => {
    const items = document.querySelectorAll(".timeline-item");
    const data = [];

    items.forEach((tweet) => {
      try {
        const dateElement = tweet.querySelector(".tweet-date a");
        const date = dateElement?.getAttribute("title") || "";
        const content = tweet.querySelector(".tweet-content")?.innerText || "";
        const link = dateElement?.getAttribute("href") || "";
        const statsElements = tweet.querySelectorAll(".tweet-stat");

        data.push({
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

    return data;
  });
}

async function findAndClickLoadMore(page, retries = 3) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    // Attendre que le DOM soit stable
    await sleep(2000);

    const buttonInfo = await page.evaluate(() => {
      const links = document.querySelectorAll(".show-more a");
      let loadMoreFound = null;

      links.forEach((link, i) => {
        const text = link.innerText.toLowerCase();
        const href = link.getAttribute("href");

        if (text.includes("load more") && href && href.includes("cursor=")) {
          loadMoreFound = {
            index: i,
            text: link.innerText,
            href: href.substring(0, 50),
            hasCursor: true
          };
        }
      });

      return {
        totalLinks: links.length,
        loadMoreButton: loadMoreFound
      };
    });

    console.log(`     Tentative ${attempt}/${retries}:`);
    console.log(`       Liens .show-more: ${buttonInfo.totalLinks}`);
    console.log(`       Load More trouvé: ${buttonInfo.loadMoreButton ? "✓" : "✗"}`);

    if (buttonInfo.loadMoreButton) {
      // Cliquer
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

      if (clicked) {
        console.log(`       ✅ Clic effectué`);

        await sleep(1000);

        // Attendre navigation
        try {
          await page.waitForNavigation({ waitUntil: "networkidle2", timeout: 15000 });
        } catch {
          await sleep(CONFIG.delayBetweenRequests);
        }

        await page.waitForSelector(".timeline-item", { timeout: 10000 });
        return true;
      }
    }

    if (attempt < retries) {
      console.log(`       ⚠️  Rechargement de la page...`);
      await page.reload({ waitUntil: "networkidle2" });
      await page.waitForSelector(".timeline-item", { timeout: 10000 });
    }
  }

  return false;
}

async function main() {
  console.log("=".repeat(70));
  console.log("🧪 MÉTHODE 2: Force reload avec retry");
  console.log("=".repeat(70));

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  );

  console.log(`📡 Chargement initial...`);
  await page.goto(`${CONFIG.nitterUrl}/${CONFIG.username}`, {
    waitUntil: "networkidle2",
    timeout: 30000
  });
  await page.waitForSelector(".timeline-item", { timeout: 10000 });

  let allTweets = [];
  let iteration = 0;
  let reachedTarget = false;

  while (iteration < CONFIG.maxIterations && !reachedTarget) {
    iteration++;

    if (iteration % 10 === 1 || iteration <= 5) {
      console.log(`\n--- Itération ${iteration}/${CONFIG.maxIterations} ---`);
    }

    const tweets = await extractTweets(page);
    const unique = tweets.filter(
      (t) => !allTweets.some((existing) => existing.link === t.link)
    );
    allTweets.push(...unique);

    if (iteration % 10 === 0 || iteration <= 5) {
      console.log(`   📊 ${tweets.length} tweets, ${unique.length} nouveaux`);
      console.log(`   📈 Total: ${allTweets.length}`);

      if (tweets.length > 0) {
        const oldest = tweets[tweets.length - 1];
        console.log(`   📅 Plus ancien: ${oldest.date}`);

        const oldestDate = new Date(oldest.date);
        if (!isNaN(oldestDate.getTime()) && oldestDate < CONFIG.targetDate) {
          console.log(`   ✅ DATE CIBLE!`);
          reachedTarget = true;
        }
      }
    }

    if (iteration % 50 === 0) {
      fs.writeFileSync(
        "data/processed/test_method2_temp.json",
        JSON.stringify({ iteration, total: allTweets.length, tweets: allTweets }, null, 2),
        "utf-8"
      );
      console.log(`   💾 Sauvegarde: ${allTweets.length} tweets`);
    }

    if (reachedTarget) break;

    // Chercher et cliquer Load More avec retry
    const success = await findAndClickLoadMore(page, 3);

    if (!success) {
      console.log(`\n❌ Impossible de trouver Load More après 3 tentatives`);
      break;
    }

    await sleep(CONFIG.delayBetweenRequests);
  }

  await browser.close();

  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS MÉTHODE 2");
  console.log("=".repeat(70));
  console.log(`✅ Iterations: ${iteration}`);
  console.log(`✅ Total tweets: ${allTweets.length}`);
  if (allTweets.length > 0) {
    console.log(`📅 Plus récent: ${allTweets[0].date}`);
    console.log(`📅 Plus ancien: ${allTweets[allTweets.length - 1].date}`);
  }

  fs.writeFileSync(
    "data/processed/test_method2_results.json",
    JSON.stringify({
      method: "force_reload_retry",
      iterations: iteration,
      total_tweets: allTweets.length,
      tweets: allTweets
    }, null, 2),
    "utf-8"
  );
  console.log("\n💾 Sauvegardé: data/processed/test_method2_results.json");
  console.log("=".repeat(70));
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
