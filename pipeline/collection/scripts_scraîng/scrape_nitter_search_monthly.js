#!/usr/bin/env node
/**
 * SCRAPER NITTER PAR RECHERCHE MENSUELLE
 *
 * Contourne la limite de pagination timeline (40 pages) en utilisant
 * des recherches temporelles indépendantes par mois.
 *
 * Au lieu de : Timeline infiniment → Bloque à page 40
 * On fait :    33 recherches mensuelles → Jamais plus de 5 pages/mois
 */

const puppeteer = require("puppeteer");
const fs = require("fs").promises;
const path = require("path");

const CONFIG = {
  // Instances Nitter fonctionnelles (testées 5 janvier 2026)
  // Source: https://github.com/zedeus/nitter/wiki/Instances
  nitterInstances: [
    "https://nitter.net",                  // ✅ Meilleure - 2095ms
    "https://nitter.privacyredirect.com",  // ✅ Backup - 2492ms
    "https://nitter.tiekoetter.com",       // ✅ Backup - 3550ms
  ],
  nitterUrl: "https://nitter.net", // Instance principale (testée la plus rapide)
  startDate: "2023-01-01",
  endDate: "2026-01-31", // Jusqu'à janvier 2026
  maxPagesPerMonth: 5, // Sécurité : jamais proche de limite 40
  delayBetweenMonths: 4000, // 4s entre requêtes (recommandé après tests)
  delayBetweenDeputes: 6000, // 6s entre députés
  retryAttempts: 3,
  retryBackoff: [5000, 10000, 20000], // Backoff: 5s, 10s, 20s
  pageTimeout: 45000, // 45s timeout pour goto
  selectorTimeout: 10000, // 10s timeout pour sélecteurs
};

// Modes d'exécution
const MODE = {
  test: false, // Test 1 député × 3 mois
  testDepute: null, // Si test, quel député ?
  testMonths: 3, // Si test, combien de mois ?
  maxDeputes: null, // Limite nombre députés (null = tous)
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Génère les périodes mensuelles entre deux dates
 */
function generateMonthlyPeriods(startDate, endDate) {
  const periods = [];
  let current = new Date(startDate);
  const end = new Date(endDate);

  while (current <= end) {
    const year = current.getFullYear();
    const month = String(current.getMonth() + 1).padStart(2, "0");

    // Dernier jour du mois
    const lastDay = new Date(year, current.getMonth() + 1, 0).getDate();

    periods.push({
      label: `${year}-${month}`,
      start: `${year}-${month}-01`,
      end: `${year}-${month}-${String(lastDay).padStart(2, "0")}`,
    });

    // Mois suivant
    current.setMonth(current.getMonth() + 1);
  }

  return periods;
}

/**
 * Extrait les tweets d'une page Nitter
 */
async function extractTweetsFromPage(page) {
  return await page.evaluate(() => {
    const items = document.querySelectorAll(".timeline-item");
    const tweets = [];

    items.forEach((item) => {
      const contentEl = item.querySelector(".tweet-content");
      const dateEl = item.querySelector(".tweet-date a");

      if (!contentEl || !dateEl) return;

      // Stats
      const stats = {};
      const statsContainer = item.querySelector(".tweet-stats");
      if (statsContainer) {
        const iconHeart = statsContainer.querySelector(".icon-heart");
        const iconRetweet = statsContainer.querySelector(".icon-retweet");
        const iconQuote = statsContainer.querySelector(".icon-quote");
        const iconComment = statsContainer.querySelector(".icon-comment");

        if (iconHeart) {
          const parent = iconHeart.closest(".tweet-stat");
          stats.likes = parseInt(parent?.innerText.trim()) || 0;
        }
        if (iconRetweet) {
          const parent = iconRetweet.closest(".tweet-stat");
          stats.retweets = parseInt(parent?.innerText.trim()) || 0;
        }
        if (iconQuote) {
          const parent = iconQuote.closest(".tweet-stat");
          stats.quotes = parseInt(parent?.innerText.trim()) || 0;
        }
        if (iconComment) {
          const parent = iconComment.closest(".tweet-stat");
          stats.replies = parseInt(parent?.innerText.trim()) || 0;
        }
      }

      tweets.push({
        text: contentEl.innerText.trim(),
        date: dateEl.getAttribute("title") || "",
        url: dateEl.getAttribute("href") || "",
        likes: stats.likes || 0,
        retweets: stats.retweets || 0,
        quotes: stats.quotes || 0,
        replies: stats.replies || 0,
      });
    });

    return tweets;
  });
}

/**
 * Vérifie si bouton "Load more" existe
 */
async function hasLoadMoreButton(page) {
  return await page.evaluate(() => {
    const loadMoreLinks = document.querySelectorAll(".show-more a");
    for (const link of loadMoreLinks) {
      const href = link.getAttribute("href") || "";
      const text = link.innerText.toLowerCase();
      if (href.includes("cursor=") && text.includes("load more")) {
        return true;
      }
    }
    return false;
  });
}

/**
 * Clique sur "Load more"
 */
async function clickLoadMore(page) {
  try {
    await page.evaluate(() => {
      const loadMoreLinks = document.querySelectorAll(".show-more a");
      for (const link of loadMoreLinks) {
        const href = link.getAttribute("href") || "";
        const text = link.innerText.toLowerCase();
        if (href.includes("cursor=") && text.includes("load more")) {
          link.click();
          return;
        }
      }
    });

    await sleep(2000);
    await page.waitForSelector(".timeline-item", { timeout: 10000 });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Scrape un mois pour un député (avec pagination)
 */
async function scrapeMonthForDepute(browser, username, period, attempt = 1) {
  const query = `from:${username} since:${period.start} until:${period.end}`;
  const url = `${CONFIG.nitterUrl}/search?f=tweets&q=${encodeURIComponent(
    query
  )}`;

  let page = null;

  try {
    page = await browser.newPage();
    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    );

    await page.goto(url, { waitUntil: "networkidle2", timeout: CONFIG.pageTimeout });

    // Attendre les tweets (ou erreur si aucun)
    try {
      await page.waitForSelector(".timeline-item", { timeout: CONFIG.selectorTimeout });
    } catch (e) {
      // Pas de tweets ce mois → OK, retourner tableau vide
      await page.close();
      return [];
    }

    const allTweets = [];
    let pageCount = 0;

    // Extraire première page
    const tweets1 = await extractTweetsFromPage(page);
    allTweets.push(...tweets1);

    // Paginer si nécessaire (max 5 pages)
    while (pageCount < CONFIG.maxPagesPerMonth) {
      const hasMore = await hasLoadMoreButton(page);
      if (!hasMore) break;

      const clicked = await clickLoadMore(page);
      if (!clicked) break;

      const moreTweets = await extractTweetsFromPage(page);
      const newTweets = moreTweets.filter(
        (t) => !allTweets.some((existing) => existing.url === t.url)
      );

      if (newTweets.length === 0) break; // Plus de nouveaux tweets

      allTweets.push(...newTweets);
      pageCount++;

      // Sécurité : si déjà beaucoup de tweets, arrêter
      if (allTweets.length >= 200) break;
    }

    await page.close();
    return allTweets;
  } catch (error) {
    if (page) await page.close();

    // Retry logic
    if (attempt < CONFIG.retryAttempts) {
      const backoff = CONFIG.retryBackoff[attempt - 1];
      console.log(
        `      ⚠️  Erreur (tentative ${attempt}/${CONFIG.retryAttempts}): ${error.message}`
      );
      console.log(`      ⏳ Attente ${backoff / 1000}s avant retry...`);
      await sleep(backoff);
      return scrapeMonthForDepute(browser, username, period, attempt + 1);
    }

    console.log(`      ❌ Échec après ${CONFIG.retryAttempts} tentatives`);
    return [];
  }
}

/**
 * Pipeline principal
 */
async function main() {
  // Parse arguments CLI
  const args = process.argv.slice(2);
  if (args.includes("--test")) {
    MODE.test = true;
    const deputeIndex = args.indexOf("--depute");
    if (deputeIndex !== -1 && args[deputeIndex + 1]) {
      MODE.testDepute = args[deputeIndex + 1];
    }
    const monthsIndex = args.indexOf("--months");
    if (monthsIndex !== -1 && args[monthsIndex + 1]) {
      MODE.testMonths = parseInt(args[monthsIndex + 1]);
    }
  }

  const maxDeputesIndex = args.indexOf("--max-deputes");
  if (maxDeputesIndex !== -1 && args[maxDeputesIndex + 1]) {
    MODE.maxDeputes = parseInt(args[maxDeputesIndex + 1]);
  }

  console.log("======================================================================");
  console.log("🔍 SCRAPING NITTER PAR RECHERCHE MENSUELLE");
  console.log("======================================================================");
  console.log(`Mode: ${MODE.test ? "TEST" : "PRODUCTION"}`);
  if (MODE.test) {
    console.log(
      `Député: ${MODE.testDepute || "Premier de la liste"} | Mois: ${MODE.testMonths}`
    );
  }
  if (MODE.maxDeputes) {
    console.log(`Limite: ${MODE.maxDeputes} députés`);
  }
  console.log("======================================================================\n");

  // Charger députés validés
  const inputFileIndex = args.indexOf("--input");
  const inputFile =
    inputFileIndex !== -1 && args[inputFileIndex + 1]
      ? args[inputFileIndex + 1]
      : "data/interim/validated_accounts.json";

  const validatedPath = path.resolve(inputFile);
  const validatedData = JSON.parse(await fs.readFile(validatedPath, "utf-8"));
  let deputes = validatedData.validated_accounts || [];

  // Filtrer pour test
  if (MODE.test && MODE.testDepute) {
    deputes = deputes.filter((d) => d.validated_username === MODE.testDepute);
    if (deputes.length === 0) {
      console.error(
        `❌ Député "${MODE.testDepute}" introuvable dans validated_accounts.json`
      );
      process.exit(1);
    }
  } else if (MODE.test) {
    deputes = [deputes[0]]; // Premier député
  }

  if (MODE.maxDeputes) {
    deputes = deputes.slice(0, MODE.maxDeputes);
  }

  console.log(`📊 ${deputes.length} député(s) à scraper\n`);

  // Générer périodes mensuelles
  let periods = generateMonthlyPeriods(CONFIG.startDate, CONFIG.endDate);

  if (MODE.test) {
    periods = periods.slice(0, MODE.testMonths);
  }

  console.log(
    `📅 ${periods.length} mois à couvrir (${periods[0].start} → ${periods[periods.length - 1].end})\n`
  );

  // Lancer browser
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  let totalTweets = 0;
  const startTime = Date.now();

  // Progression
  const progress = {
    started_at: new Date().toISOString(),
    deputes_completed: 0,
    deputes_total: deputes.length,
    months_completed: 0,
    months_total: deputes.length * periods.length,
    tweets_collected: 0,
  };

  for (let i = 0; i < deputes.length; i++) {
    const depute = deputes[i];
    const username = depute.validated_username;

    console.log(
      `\n[${"=".repeat(68)}]`
    );
    console.log(
      `[${i + 1}/${deputes.length}] ${depute.depute_name} (@${username})`
    );
    console.log(
      `[${"=".repeat(68)}]\n`
    );

    let deputeTweets = 0;

    for (let j = 0; j < periods.length; j++) {
      const period = periods[j];

      // Vérifier si déjà scrapé
      const outputDir = path.resolve(
        `data/interim/twitter_monthly/${username}`
      );
      const outputFile = path.join(outputDir, `${period.label}.json`);

      try {
        await fs.access(outputFile);
        // Fichier existe, charger pour compter tweets
        const existing = JSON.parse(await fs.readFile(outputFile, "utf-8"));
        const existingCount = existing.tweets?.length || 0;
        console.log(
          `   [${j + 1}/${periods.length}] ${period.label} : ⏭️  Déjà scrapé (${existingCount} tweets)`
        );
        deputeTweets += existingCount;
        totalTweets += existingCount;
        progress.months_completed++;
        continue;
      } catch (e) {
        // Fichier n'existe pas, scraper
      }

      // Scraper ce mois
      const tweets = await scrapeMonthForDepute(browser, username, period);

      const icon = tweets.length > 0 ? "✅" : "⚪";
      console.log(
        `   [${j + 1}/${periods.length}] ${period.label} : ${icon} ${tweets.length} tweets`
      );

      deputeTweets += tweets.length;
      totalTweets += tweets.length;
      progress.months_completed++;
      progress.tweets_collected = totalTweets;

      // Sauvegarder
      if (tweets.length > 0) {
        await fs.mkdir(outputDir, { recursive: true });
        await fs.writeFile(
          outputFile,
          JSON.stringify(
            {
              depute: depute.depute_name,
              username: username,
              group: depute.group || "N/A",
              period: period,
              tweets: tweets,
              scraped_at: new Date().toISOString(),
            },
            null,
            2
          ),
          "utf-8"
        );
      }

      // Sauvegarder progression tous les 10 mois
      if (progress.months_completed % 10 === 0) {
        progress.last_update = new Date().toISOString();
        await fs.writeFile(
          path.resolve("data/interim/scraping_progress.json"),
          JSON.stringify(progress, null, 2),
          "utf-8"
        );
      }

      // Rate limiting
      await sleep(CONFIG.delayBetweenMonths);
    }

    console.log(`\n   📊 Total ${depute.depute_name}: ${deputeTweets} tweets`);
    progress.deputes_completed++;

    // Délai entre députés
    if (i < deputes.length - 1) {
      await sleep(CONFIG.delayBetweenDeputes);
    }
  }

  await browser.close();

  const duration = ((Date.now() - startTime) / 1000 / 60).toFixed(1);

  console.log("\n" + "=".repeat(70));
  console.log("✅ SCRAPING TERMINÉ");
  console.log("=".repeat(70));
  console.log(`📊 Total tweets collectés: ${totalTweets}`);
  console.log(`⏱️  Durée: ${duration} minutes`);
  console.log(`📁 Données: data/interim/twitter_monthly/`);
  console.log("=".repeat(70));

  // Sauvegarder progression finale
  progress.last_update = new Date().toISOString();
  progress.completed_at = new Date().toISOString();
  await fs.writeFile(
    path.resolve("data/interim/scraping_progress.json"),
    JSON.stringify(progress, null, 2),
    "utf-8"
  );
}

main().catch((err) => {
  console.error("\n❌ ERREUR FATALE:", err);
  process.exit(1);
});
