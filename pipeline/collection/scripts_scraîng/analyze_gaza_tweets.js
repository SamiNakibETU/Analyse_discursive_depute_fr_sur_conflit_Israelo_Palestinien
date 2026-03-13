#!/usr/bin/env node
/**
 * Analyse des tweets mentionnant Gaza/Palestine
 */

const fs = require("fs");

const lines = fs
  .readFileSync("data/processed/twitter_deputes_complete.jsonl", "utf-8")
  .split("\n")
  .filter((l) => l.trim());

console.log("======================================================================");
console.log("📊 ANALYSE TWEETS GAZA/PALESTINE");
console.log("======================================================================\n");

console.log(`Total tweets collectés: ${lines.length}`);

const keywords =
  /gaza|palestine|palestin|israël|israel|hamas|otage|cisjordanie|proche-orient|netanyahu|tsahal/i;
const filtered = lines.filter((l) => keywords.test(JSON.parse(l).text));

console.log(
  `Tweets Gaza/Palestine: ${filtered.length} (${Math.round(
    (filtered.length / lines.length) * 100
  )}%)\n`
);

// Par année
console.log("Répartition par année:");
const byYear = { 2023: 0, 2024: 0, 2025: 0 };
filtered.forEach((l) => {
  const t = JSON.parse(l);
  const year = t.collection_period.split("-")[0];
  byYear[year] = (byYear[year] || 0) + 1;
});

console.log(`  2023: ${byYear[2023]} tweets`);
console.log(`  2024: ${byYear[2024]} tweets`);
console.log(`  2025: ${byYear[2025]} tweets\n`);

// Exemples
console.log("Exemples de tweets (10 premiers):");
console.log("=".repeat(70) + "\n");

filtered.slice(0, 10).forEach((l, i) => {
  const t = JSON.parse(l);
  console.log(`${i + 1}. [${t.collection_period}] ${t.date}`);
  console.log(`   ${t.text.substring(0, 200).replace(/\n/g, " ")}...`);
  console.log(
    `   💙 ${t.likes} | 🔁 ${t.retweets} | 🔗 https://twitter.com${t.url}\n`
  );
});

console.log("=".repeat(70));
console.log("\n✅ Analyse terminée");
console.log(
  `📁 Fichier complet: data/processed/twitter_deputes_complete.jsonl`
);
