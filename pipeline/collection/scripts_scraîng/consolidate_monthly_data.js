#!/usr/bin/env node
/**
 * CONSOLIDATION DES DONNÉES MENSUELLES
 *
 * Fusionne tous les fichiers mensuels en un seul fichier final
 * avec déduplication et statistiques par député
 */

const fs = require("fs").promises;
const path = require("path");

async function getAllMonthlyFiles() {
  const monthlyDir = path.resolve("data/interim/twitter_monthly");
  const files = [];

  try {
    const deputes = await fs.readdir(monthlyDir);

    for (const depute of deputes) {
      const deputePath = path.join(monthlyDir, depute);
      const stat = await fs.stat(deputePath);

      if (stat.isDirectory()) {
        const monthFiles = await fs.readdir(deputePath);

        for (const file of monthFiles) {
          if (file.endsWith(".json")) {
            files.push(path.join(deputePath, file));
          }
        }
      }
    }
  } catch (error) {
    console.error(`Erreur lecture dossier: ${error.message}`);
    return [];
  }

  return files;
}

async function main() {
  console.log("======================================================================");
  console.log("📦 CONSOLIDATION DONNÉES MENSUELLES");
  console.log("======================================================================\n");

  // Récupérer tous les fichiers mensuels
  const files = await getAllMonthlyFiles();
  console.log(`📂 ${files.length} fichiers mensuels trouvés\n`);

  if (files.length === 0) {
    console.log("❌ Aucun fichier mensuel à consolider");
    process.exit(1);
  }

  // Charger et fusionner
  const allTweetsByDepute = {};
  const tweetUrls = new Set(); // Pour déduplication
  let totalTweets = 0;
  let duplicates = 0;

  for (const file of files) {
    try {
      const data = JSON.parse(await fs.readFile(file, "utf-8"));
      const deputeName = data.depute || "Unknown";
      const username = data.username || "unknown";

      if (!allTweetsByDepute[username]) {
        allTweetsByDepute[username] = {
          depute_name: deputeName,
          username: username,
          group: data.group || "Unknown",
          tweets: [],
          periods: [],
        };
      }

      allTweetsByDepute[username].periods.push(data.period?.label || "Unknown");

      // Ajouter tweets avec déduplication
      for (const tweet of data.tweets || []) {
        if (!tweetUrls.has(tweet.url)) {
          tweetUrls.add(tweet.url);
          allTweetsByDepute[username].tweets.push({
            ...tweet,
            collection_method: "search",
            collection_period: data.period?.label || "Unknown",
          });
          totalTweets++;
        } else {
          duplicates++;
        }
      }
    } catch (error) {
      console.error(`⚠️  Erreur fichier ${path.basename(file)}: ${error.message}`);
    }
  }

  console.log(`\n📊 STATISTIQUES`);
  console.log(`${"=".repeat(70)}\n`);

  // Statistiques par député
  const deputes = Object.keys(allTweetsByDepute);
  console.log(`Députés avec tweets: ${deputes.length}`);
  console.log(`Total tweets uniques: ${totalTweets}`);
  console.log(`Doublons éliminés: ${duplicates}\n`);

  console.log(`Tweets par député:\n`);
  for (const username of deputes) {
    const data = allTweetsByDepute[username];
    data.tweets.sort((a, b) => {
      const dateA = new Date(a.date);
      const dateB = new Date(b.date);
      return dateA - dateB; // Tri chronologique (ancien → récent)
    });

    const oldest = data.tweets[0]?.date || "N/A";
    const newest = data.tweets[data.tweets.length - 1]?.date || "N/A";
    const periodsCount = new Set(data.periods).size;

    console.log(`  ${data.depute_name} (@${username})`);
    console.log(`    Tweets: ${data.tweets.length}`);
    console.log(`    Périodes: ${periodsCount} mois`);
    console.log(`    Plus ancien: ${oldest}`);
    console.log(`    Plus récent: ${newest}\n`);
  }

  // Sauvegarder fichier consolidé JSONL
  const outputPath = path.resolve("data/processed/twitter_deputes_complete.jsonl");
  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  let linesWritten = 0;

  for (const username of deputes) {
    const data = allTweetsByDepute[username];

    for (const tweet of data.tweets) {
      const line =
        JSON.stringify({
          depute_name: data.depute_name,
          username: data.username,
          group: data.group,
          text: tweet.text,
          date: tweet.date,
          url: tweet.url,
          likes: tweet.likes || 0,
          retweets: tweet.retweets || 0,
          quotes: tweet.quotes || 0,
          replies: tweet.replies || 0,
          collection_method: tweet.collection_method,
          collection_period: tweet.collection_period,
        }) + "\n";

      await fs.appendFile(outputPath, line, "utf-8");
      linesWritten++;
    }
  }

  console.log(`\n✅ Consolidation terminée`);
  console.log(`📁 Fichier: ${outputPath}`);
  console.log(`📝 Lignes écrites: ${linesWritten}`);

  // Sauvegarder statistiques JSON
  const statsPath = path.resolve("data/processed/twitter_stats.json");
  const stats = {
    consolidation_date: new Date().toISOString(),
    total_deputes: deputes.length,
    total_tweets: totalTweets,
    duplicates_removed: duplicates,
    deputes: deputes.map((username) => {
      const data = allTweetsByDepute[username];
      return {
        depute_name: data.depute_name,
        username: data.username,
        group: data.group,
        tweets_count: data.tweets.length,
        periods_count: new Set(data.periods).size,
        oldest_tweet: data.tweets[0]?.date || null,
        newest_tweet: data.tweets[data.tweets.length - 1]?.date || null,
      };
    }),
  };

  await fs.writeFile(statsPath, JSON.stringify(stats, null, 2), "utf-8");
  console.log(`📊 Statistiques: ${statsPath}`);

  console.log("\n" + "=".repeat(70));
}

main().catch((err) => {
  console.error("❌ Erreur:", err);
  process.exit(1);
});
