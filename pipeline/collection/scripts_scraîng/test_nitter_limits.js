#!/usr/bin/env node
/**
 * TEST APPROFONDI DES LIMITES DE NITTER
 * - Tester différentes stratégies de pagination
 * - Voir exactement pourquoi le bouton disparaît
 * - Essayer plusieurs méthodes de contournement
 */

const puppeteer = require("puppeteer");
const fs = require("fs");

const CONFIG = {
  username: "mathildepanot",
  nitterUrl: "https://nitter.net",
  headless: false,  // Visible pour voir ce qui se passe
  slowMo: 100,      // Ralenti pour observer
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function extractTweets(page) {
  return await page.evaluate(() => {
    const allTweets = document.querySelectorAll(".timeline-item");
    const data = [];

    allTweets.forEach((tweet) => {
      try {
        const dateElement = tweet.querySelector(".tweet-date a");
        const date = dateElement?.getAttribute("title") || "";
        const content = tweet.querySelector(".tweet-content")?.innerText || "";
        const link = dateElement?.getAttribute("href") || "";

        data.push({
          date,
          content: content.substring(0, 50),
          link: link ? `https://nitter.net${link}` : "",
        });
      } catch (error) {
        // Skip
      }
    });

    return data;
  });
}

async function debugLoadMoreButton(page, iteration) {
  console.log(`\n🔍 DEBUG Itération ${iteration} - Analyse du bouton "Load more"`);

  const debugInfo = await page.evaluate(() => {
    const showMoreDivs = document.querySelectorAll(".show-more");
    const allLinks = document.querySelectorAll(".show-more a");

    const info = {
      showMoreDivCount: showMoreDivs.length,
      totalLinks: allLinks.length,
      links: []
    };

    allLinks.forEach((link, index) => {
      const text = link.innerText;
      const href = link.getAttribute("href");
      const isVisible = link.offsetParent !== null;

      info.links.push({
        index,
        text,
        href: href ? href.substring(0, 80) + "..." : null,
        isVisible,
        hasCursor: href && href.includes("cursor=")
      });
    });

    return info;
  });

  console.log(`   📊 Divs .show-more: ${debugInfo.showMoreDivCount}`);
  console.log(`   📊 Liens trouvés: ${debugInfo.totalLinks}`);

  debugInfo.links.forEach(link => {
    console.log(`   ${link.index}. "${link.text}" | Visible: ${link.isVisible} | Cursor: ${link.hasCursor}`);
  });

  return debugInfo;
}

// MÉTHODE 1: Navigation directe via URL cursor
async function testMethod1_DirectNavigation(page, url) {
  console.log("\n" + "=".repeat(70));
  console.log("MÉTHODE 1: Navigation directe via URL cursor");
  console.log("=".repeat(70));

  await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
  await page.waitForSelector(".timeline-item", { timeout: 10000 });

  let allTweets = [];
  let iteration = 0;

  while (iteration < 30) {
    iteration++;
    console.log(`\n--- Itération ${iteration}/30 ---`);

    const tweets = await extractTweets(page);
    console.log(`   📊 ${tweets.length} tweets sur la page`);

    const unique = tweets.filter(
      (t) => !allTweets.some((existing) => existing.link === t.link)
    );
    allTweets.push(...unique);
    console.log(`   📈 Total unique: ${allTweets.length}`);

    if (tweets.length > 0) {
      console.log(`   📅 Plus ancien: ${tweets[tweets.length - 1].date}`);
    }

    // Debug le bouton
    const debugInfo = await debugLoadMoreButton(page, iteration);

    // Chercher le lien avec cursor
    const cursorLink = debugInfo.links.find(l => l.hasCursor && l.text.toLowerCase().includes("load more"));

    if (!cursorLink) {
      console.log("   ❌ Aucun lien Load More avec cursor trouvé");
      break;
    }

    // Extraire le cursor de l'URL actuelle
    const currentUrl = page.url();
    console.log(`   🔗 URL actuelle: ${currentUrl.substring(0, 80)}...`);

    // Cliquer sur le bouton
    const clicked = await page.evaluate(() => {
      const links = document.querySelectorAll(".show-more a");
      for (const link of links) {
        if (link.innerText.toLowerCase().includes("load more") &&
            link.getAttribute("href")?.includes("cursor=")) {
          link.click();
          return true;
        }
      }
      return false;
    });

    if (!clicked) {
      console.log("   ❌ Échec du clic");
      break;
    }

    console.log("   ✅ Clic effectué, attente navigation...");

    // Attendre la navigation
    try {
      await page.waitForNavigation({ waitUntil: "networkidle2", timeout: 10000 });
      console.log("   ✅ Navigation complétée");
    } catch (e) {
      console.log("   ⚠️  Timeout navigation, attente simple...");
      await sleep(3000);
    }

    await page.waitForSelector(".timeline-item", { timeout: 5000 });
  }

  console.log(`\n✅ Méthode 1 terminée: ${allTweets.length} tweets uniques`);
  return allTweets;
}

// MÉTHODE 2: Scroll infini au lieu de Load More
async function testMethod2_InfiniteScroll(page, url) {
  console.log("\n" + "=".repeat(70));
  console.log("MÉTHODE 2: Scroll infini (au lieu de cliquer Load More)");
  console.log("=".repeat(70));

  await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
  await page.waitForSelector(".timeline-item", { timeout: 10000 });

  let allTweets = [];
  let iteration = 0;
  let lastHeight = 0;

  while (iteration < 30) {
    iteration++;
    console.log(`\n--- Itération ${iteration}/30 ---`);

    // Scroll jusqu'en bas
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await sleep(2000);

    const tweets = await extractTweets(page);
    console.log(`   📊 ${tweets.length} tweets sur la page`);

    const unique = tweets.filter(
      (t) => !allTweets.some((existing) => existing.link === t.link)
    );
    allTweets.push(...unique);
    console.log(`   📈 Total unique: ${allTweets.length}`);

    if (tweets.length > 0) {
      console.log(`   📅 Plus ancien: ${tweets[tweets.length - 1].date}`);
    }

    // Vérifier hauteur
    const newHeight = await page.evaluate(() => document.body.scrollHeight);
    console.log(`   📏 Hauteur: ${lastHeight} → ${newHeight}`);

    if (newHeight === lastHeight) {
      console.log("   ⚠️  Hauteur inchangée, peut-être fini");

      // Essayer de cliquer Load More
      const hasButton = await page.evaluate(() => {
        const links = document.querySelectorAll(".show-more a");
        for (const link of links) {
          if (link.innerText.toLowerCase().includes("load more")) {
            link.click();
            return true;
          }
        }
        return false;
      });

      if (hasButton) {
        console.log("   🔄 Bouton Load More cliqué, continue...");
        await sleep(3000);
        lastHeight = 0; // Reset
      } else {
        console.log("   ❌ Plus de bouton, arrêt");
        break;
      }
    } else {
      lastHeight = newHeight;
    }
  }

  console.log(`\n✅ Méthode 2 terminée: ${allTweets.length} tweets uniques`);
  return allTweets;
}

// MÉTHODE 3: Attente plus longue entre clics
async function testMethod3_SlowerClicks(page, url) {
  console.log("\n" + "=".repeat(70));
  console.log("MÉTHODE 3: Clics plus lents avec attentes longues");
  console.log("=".repeat(70));

  await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
  await page.waitForSelector(".timeline-item", { timeout: 10000 });

  let allTweets = [];
  let iteration = 0;

  while (iteration < 50) {
    iteration++;
    console.log(`\n--- Itération ${iteration}/50 ---`);

    const tweets = await extractTweets(page);
    console.log(`   📊 ${tweets.length} tweets sur la page`);

    const unique = tweets.filter(
      (t) => !allTweets.some((existing) => existing.link === t.link)
    );
    allTweets.push(...unique);
    console.log(`   📈 Total unique: ${allTweets.length}`);

    if (tweets.length > 0) {
      console.log(`   📅 Plus ancien: ${tweets[tweets.length - 1].date}`);
    }

    if (unique.length === 0) {
      console.log("   ⚠️  Aucun nouveau tweet");
    }

    // Attendre BEAUCOUP plus longtemps
    console.log("   ⏳ Attente 5 secondes...");
    await sleep(5000);

    // Chercher et cliquer le bouton
    const clicked = await page.evaluate(() => {
      const links = document.querySelectorAll(".show-more a");
      for (const link of links) {
        const text = link.innerText.toLowerCase();
        const href = link.getAttribute("href");
        if (text.includes("load more") && href && href.includes("cursor=")) {
          // Scroll jusqu'au bouton
          link.scrollIntoView({ behavior: "smooth", block: "center" });
          setTimeout(() => link.click(), 500);
          return true;
        }
      }
      return false;
    });

    if (!clicked) {
      console.log("   ❌ Aucun bouton Load More trouvé");
      break;
    }

    console.log("   🔄 Bouton cliqué, attente navigation...");
    await sleep(2000);

    try {
      await page.waitForNavigation({ waitUntil: "networkidle2", timeout: 15000 });
    } catch (e) {
      await sleep(3000);
    }

    await page.waitForSelector(".timeline-item", { timeout: 10000 });
    await sleep(2000);
  }

  console.log(`\n✅ Méthode 3 terminée: ${allTweets.length} tweets uniques`);
  return allTweets;
}

async function main() {
  const url = `${CONFIG.nitterUrl}/${CONFIG.username}`;

  console.log("=".repeat(70));
  console.log("🧪 TEST DES LIMITES DE NITTER");
  console.log("=".repeat(70));
  console.log(`URL: ${url}`);
  console.log(`Mode: ${CONFIG.headless ? "Headless" : "Visible (debug)"}`);
  console.log("=".repeat(70));

  const browser = await puppeteer.launch({
    headless: CONFIG.headless,
    slowMo: CONFIG.slowMo,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  );

  // TEST MÉTHODE 1
  const method1Results = await testMethod1_DirectNavigation(page, url);

  // Attendre un peu entre les tests
  console.log("\n⏳ Pause 10 secondes entre méthodes...");
  await sleep(10000);

  // TEST MÉTHODE 3 (la plus prometteuse)
  const method3Results = await testMethod3_SlowerClicks(page, url);

  await browser.close();

  // Résumé
  console.log("\n" + "=".repeat(70));
  console.log("📊 RÉSUMÉ DES TESTS");
  console.log("=".repeat(70));
  console.log(`Méthode 1 (Navigation directe): ${method1Results.length} tweets`);
  console.log(`Méthode 3 (Clics lents): ${method3Results.length} tweets`);
  console.log("=".repeat(70));

  // Sauvegarder résultats
  const results = {
    test_date: new Date().toISOString(),
    username: CONFIG.username,
    methods: {
      method1_direct_navigation: {
        total_tweets: method1Results.length,
        oldest_date: method1Results[method1Results.length - 1]?.date,
        newest_date: method1Results[0]?.date
      },
      method3_slower_clicks: {
        total_tweets: method3Results.length,
        oldest_date: method3Results[method3Results.length - 1]?.date,
        newest_date: method3Results[0]?.date
      }
    }
  };

  fs.writeFileSync(
    "data/processed/nitter_limits_test.json",
    JSON.stringify(results, null, 2),
    "utf-8"
  );

  console.log("\n💾 Résultats sauvegardés: data/processed/nitter_limits_test.json");
}

main().catch((err) => {
  console.error("❌ ERREUR:", err);
  process.exit(1);
});
