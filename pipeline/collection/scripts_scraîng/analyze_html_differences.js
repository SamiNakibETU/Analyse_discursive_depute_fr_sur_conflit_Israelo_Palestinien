#!/usr/bin/env node
/**
 * Analyze HTML differences between working and failing iterations
 */

const fs = require("fs");
const path = require("path");

async function analyzeHtml(filepath) {
  const html = await fs.promises.readFile(filepath, "utf-8");

  // Count timeline items
  const timelineMatches = html.match(/<div class="timeline-item[^>]*>/g) || [];
  const timelineCount = timelineMatches.length;

  // Find all .show-more elements
  const showMoreMatches = html.match(/<div class="[^"]*show-more[^"]*">/g) || [];
  const showMoreCount = showMoreMatches.length;

  // Find Load more links
  const loadMoreMatches = html.match(/<a href="[^"]*cursor=[^"]+">Load more<\/a>/gi) || [];
  const loadMoreCount = loadMoreMatches.length;

  // Extract cursor if present
  let cursor = null;
  const cursorMatch = html.match(/<a href="[^"]*cursor=([^"&]+)[^"]*">Load more<\/a>/i);
  if (cursorMatch) {
    cursor = cursorMatch[1];
  }

  // Check for "Load newest" link
  const loadNewestMatches = html.match(/>Load newest<\/a>/gi) || [];
  const hasLoadNewest = loadNewestMatches.length > 0;

  // Extract oldest tweet date
  const dateMatches = html.match(/title="([^"]+\d{4}[^"]+)"/g) || [];
  const dates = dateMatches.map(m => m.match(/title="([^"]+)"/)[1]);
  const oldestDate = dates[dates.length - 1] || "N/A";

  return {
    timelineCount,
    showMoreCount,
    loadMoreCount,
    hasLoadNewest,
    hasCursor: !!cursor,
    cursor: cursor ? cursor.substring(0, 30) + "..." : null,
    oldestDate,
    fileSize: html.length,
  };
}

async function main() {
  console.log("======================================================================");
  console.log("🔬 ANALYSE COMPARATIVE DES HTML");
  console.log("======================================================================\n");

  const logsDir = path.resolve("logs");
  const files = await fs.promises.readdir(logsDir);
  const htmlFiles = files
    .filter(f => f.startsWith("html_iteration_") && f.endsWith(".html"))
    .sort((a, b) => {
      const numA = parseInt(a.match(/\d+/)[0]);
      const numB = parseInt(b.match(/\d+/)[0]);
      return numA - numB;
    });

  console.log(`Fichiers trouvés: ${htmlFiles.length}\n`);

  const results = [];

  for (const file of htmlFiles) {
    const iteration = parseInt(file.match(/\d+/)[0]);
    const filepath = path.join(logsDir, file);
    const analysis = await analyzeHtml(filepath);

    results.push({
      iteration,
      ...analysis,
    });
  }

  // Display table
  console.log("Iter | Tweets | .show-more | Load more | Cursor | Load newest | Oldest date");
  console.log("-----|--------|------------|-----------|--------|-------------|------------------");

  for (const r of results) {
    const iter = r.iteration.toString().padStart(4);
    const tweets = r.timelineCount.toString().padStart(6);
    const showMore = r.showMoreCount.toString().padStart(10);
    const loadMore = r.loadMoreCount.toString().padStart(9);
    const cursor = r.hasCursor ? "YES" : "NO ";
    const loadNewest = r.hasLoadNewest ? "YES" : "NO ";
    const oldestDate = r.oldestDate.substring(0, 17);

    console.log(`${iter} | ${tweets} | ${showMore} | ${loadMore} | ${cursor}    | ${loadNewest}         | ${oldestDate}`);
  }

  console.log("\n======================================================================");
  console.log("🔍 OBSERVATIONS CLÉS");
  console.log("======================================================================\n");

  // Find pattern changes
  const firstNoCursor = results.find(r => !r.hasCursor);
  if (firstNoCursor) {
    console.log(`❌ Première itération SANS cursor: ${firstNoCursor.iteration}`);
    console.log(`   Date la plus ancienne: ${firstNoCursor.oldestDate}`);
  }

  const cursorCounts = results.map(r => r.hasCursor ? 1 : 0);
  const cursorsFound = cursorCounts.reduce((a, b) => a + b, 0);
  console.log(`\n📊 Statistiques:`);
  console.log(`   Itérations avec cursor: ${cursorsFound}/${results.length}`);
  console.log(`   Itérations sans cursor: ${results.length - cursorsFound}/${results.length}`);

  // Check for "Load newest" pattern
  const allHaveLoadNewest = results.slice(1).every(r => r.hasLoadNewest);
  console.log(`\n   Toutes les itérations (sauf 1) ont "Load newest": ${allHaveLoadNewest ? "OUI" : "NON"}`);

  console.log("\n======================================================================");
}

main().catch((err) => {
  console.error("❌ Erreur:", err);
  process.exit(1);
});
