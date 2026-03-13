#!/usr/bin/env node
/**
 * Moniteur de progression du scraping
 */

const fs = require("fs");
const path = require("path");

async function countScrapedFiles() {
  const monthlyDir = path.resolve("data/interim/twitter_monthly");
  let totalFiles = 0;
  let totalTweets = 0;
  const deputeStats = [];

  try {
    const deputes = await fs.promises.readdir(monthlyDir);

    for (const depute of deputes) {
      const deputePath = path.join(monthlyDir, depute);
      const stat = await fs.promises.stat(deputePath);

      if (stat.isDirectory()) {
        const files = await fs.promises.readdir(deputePath);
        const jsonFiles = files.filter((f) => f.endsWith(".json"));
        totalFiles += jsonFiles.length;

        let deputeTweets = 0;
        for (const file of jsonFiles) {
          const data = JSON.parse(
            await fs.promises.readFile(
              path.join(deputePath, file),
              "utf-8"
            )
          );
          deputeTweets += data.tweets?.length || 0;
        }

        totalTweets += deputeTweets;
        deputeStats.push({
          username: depute,
          months: jsonFiles.length,
          tweets: deputeTweets,
        });
      }
    }
  } catch (error) {
    // Dossier n'existe pas encore
  }

  return { totalFiles, totalTweets, deputeCount: deputeStats.length, deputeStats };
}

async function readProgressFile() {
  try {
    const progressPath = path.resolve("data/interim/scraping_progress.json");
    const data = await fs.promises.readFile(progressPath, "utf-8");
    return JSON.parse(data);
  } catch (e) {
    return null;
  }
}

async function main() {
  console.clear();
  console.log("╔═══════════════════════════════════════════════════════════════════╗");
  console.log("║          MONITORING SCRAPING TWITTER - DÉPUTÉS                    ║");
  console.log("╚═══════════════════════════════════════════════════════════════════╝\n");

  const stats = await countScrapedFiles();
  const progress = await readProgressFile();

  if (progress) {
    console.log("📊 PROGRESSION GLOBALE");
    console.log("─".repeat(70));
    console.log(`Démarré le     : ${new Date(progress.started_at).toLocaleString("fr-FR")}`);
    console.log(`Dernière mise à jour : ${new Date(progress.last_update).toLocaleString("fr-FR")}`);
    console.log();
    console.log(`Députés complétés : ${progress.deputes_completed}/${progress.deputes_total} (${Math.round((progress.deputes_completed / progress.deputes_total) * 100)}%)`);
    console.log(`Mois scrapés   : ${progress.months_completed}/${progress.months_total} (${Math.round((progress.months_completed / progress.months_total) * 100)}%)`);
    console.log(`Tweets collectés : ${progress.tweets_collected.toLocaleString("fr-FR")}`);
    console.log();

    // Estimation temps restant
    const elapsed = Date.now() - new Date(progress.started_at).getTime();
    const monthsPerMs = progress.months_completed / elapsed;
    const monthsRemaining = progress.months_total - progress.months_completed;
    const msRemaining = monthsRemaining / monthsPerMs;
    const hoursRemaining = msRemaining / 1000 / 60 / 60;

    console.log(`⏱️  Temps écoulé   : ${(elapsed / 1000 / 60).toFixed(1)} minutes`);
    console.log(`⏱️  Temps estimé restant : ${hoursRemaining.toFixed(1)} heures`);
  }

  console.log("\n📁 FICHIERS GÉNÉRÉS");
  console.log("─".repeat(70));
  console.log(`Fichiers mensuels : ${stats.totalFiles}`);
  console.log(`Députés scrapés  : ${stats.deputeCount}/378`);
  console.log(`Total tweets     : ${stats.totalTweets.toLocaleString("fr-FR")}`);
  console.log(`Moyenne/député   : ${Math.round(stats.totalTweets / stats.deputeCount)} tweets`);

  console.log("\n👥 DERNIERS DÉPUTÉS SCRAPÉS");
  console.log("─".repeat(70));
  stats.deputeStats
    .slice(-10)
    .reverse()
    .forEach((d, i) => {
      console.log(
        `  ${i + 1}. @${d.username.padEnd(20)} - ${d.months} mois - ${d.tweets.toLocaleString("fr-FR")} tweets`
      );
    });

  console.log("\n💡 Commandes utiles:");
  console.log("  - Rafraîchir : node scripts/monitor_progress.js");
  console.log("  - Voir log : tail -f logs/scraping_full_run.log");
  console.log("  - Consolidation : node scripts/consolidate_monthly_data.js");

  console.log("\n" + "═".repeat(70));
}

main();
