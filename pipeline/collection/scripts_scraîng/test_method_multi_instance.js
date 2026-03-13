#!/usr/bin/env node
/**
 * MÉTHODE 3: Utiliser plusieurs instances Nitter
 * Basculer si une instance rate-limit
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  username: "mathildepanot",
  nitterInstances: [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.cz",
  ],
  targetDate: new Date("2023-01-01"),
  maxIterations: 300,
  delayBetweenRequests: 4000,
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function testInstance(instance) {
  try {
    const response = await fetch(`${instance}/elonmusk`);
    return response.ok;
  } catch {
    return false;
  }
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
          content: content.substring(0, 100),
          link: link ? link : "",
          stats: {
            replies: statsElements[0]?.innerText.trim() || "0",
            retweets: statsElements[1]?.innerText.trim() || "0",
          }
        });
      } catch (e) {}
    });

    let nextCursor = null;
    const links = document.querySelectorAll(".show-more a");
    for (const link of links) {
      const href = link.getAttribute("href");
      if (link.innerText.toLowerCase().includes("load more") && href?.includes("cursor=")) {
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
  console.log("🧪 MÉTHODE 3: Multi-instances Nitter");
  console.log("=".repeat(70));

  // Tester instances
  console.log("\n🔍 Test des instances Nitter...");
  const workingInstances = [];
  for (const instance of CONFIG.nitterInstances) {
    const works = await testInstance(instance);
    console.log(`   ${works ? "✅" : "❌"} ${instance}`);
    if (works) workingInstances.push(instance);
  }

  if (workingInstances.length === 0) {
    console.log("❌ Aucune instance Nitter disponible!");
    return;
  }

  console.log(`\n✅ ${workingInstances.length} instance(s) disponible(s)`);

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
  let currentInstanceIndex = 0;
  let currentInstance = workingInstances[currentInstanceIndex];
  let currentUrl = `${currentInstance}/${CONFIG.username}`;
  let reachedTarget = false;
  let consecutiveErrors = 0;

  while (iteration < CONFIG.maxIterations && !reachedTarget) {
    iteration++;

    if (iteration % 10 === 1 || iteration <= 5) {
      console.log(`\n--- Itération ${iteration}/${CONFIG.maxIterations} ---`);
      console.log(`   🌐 Instance: ${currentInstance}`);
    }

    try {
      await page.goto(currentUrl, {
        waitUntil: "networkidle2",
        timeout: 30000
      });
      await page.waitForSelector(".timeline-item", { timeout: 10000 });

      const { tweets, nextCursor } = await extractTweetsAndCursor(page);

      const unique = tweets.filter(
        (t) => !allTweets.some((existing) => existing.link === t.link)
      );
      allTweets.push(...unique);

      consecutiveErrors = 0; // Reset errors

      if (iteration % 10 === 0 || iteration <= 5) {
        console.log(`   📈 Total: ${allTweets.length} tweets`);
        if (tweets.length > 0) {
          console.log(`   📅 Plus ancien: ${tweets[tweets.length - 1].date}`);

          const oldestDate = new Date(tweets[tweets.length - 1].date);
          if (!isNaN(oldestDate.getTime()) && oldestDate < CONFIG.targetDate) {
            console.log(`   ✅ DATE CIBLE!`);
            reachedTarget = true;
          }
        }
      }

      if (!nextCursor) {
        console.log(`\n⚠️ Pas de cursor - changement d'instance`);
        currentInstanceIndex = (currentInstanceIndex + 1) % workingInstances.length;
        currentInstance = workingInstances[currentInstanceIndex];
        console.log(`   🔄 Nouvelle instance: ${currentInstance}`);
        continue;
      }

      if (reachedTarget) break;

      currentUrl = `${currentInstance}/${CONFIG.username}?cursor=${nextCursor}`;

    } catch (err) {
      console.log(`   ❌ Erreur: ${err.message.substring(0, 50)}`);
      consecutiveErrors++;

      if (consecutiveErrors >= 3) {
        console.log(`   🔄 3 erreurs - changement d'instance`);
        currentInstanceIndex = (currentInstanceIndex + 1) % workingInstances.length;
        currentInstance = workingInstances[currentInstanceIndex];
        currentUrl = `${currentInstance}/${CONFIG.username}`;
        consecutiveErrors = 0;
      }
    }

    await sleep(CONFIG.delayBetweenRequests);
  }

  await browser.close();

  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSULTATS MÉTHODE 3");
  console.log("=".repeat(70));
  console.log(`✅ Iterations: ${iteration}`);
  console.log(`✅ Total tweets: ${allTweets.length}`);
  if (allTweets.length > 0) {
    console.log(`📅 Plus récent: ${allTweets[0].date}`);
    console.log(`📅 Plus ancien: ${allTweets[allTweets.length - 1].date}`);
  }

  fs.writeFileSync(
    "data/processed/test_method3_results.json",
    JSON.stringify({
      method: "multi_instance",
      iterations: iteration,
      total_tweets: allTweets.length,
      instances_used: workingInstances,
      tweets: allTweets
    }, null, 2),
    "utf-8"
  );
  console.log("\n💾 Sauvegardé: data/processed/test_method3_results.json");
  console.log("=".repeat(70));
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
