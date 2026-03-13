#!/usr/bin/env node
/**
 * TEST DES RATE LIMITS NITTER
 * 
 * Ce script teste les instances Nitter pour:
 * 1. Verifier qu'elles fonctionnent
 * 2. Mesurer les temps de reponse
 * 3. Detecter le rate limiting
 */

const puppeteer = require("puppeteer");
const fs = require("fs").promises;

// Instances a tester (janvier 2026)
const NITTER_INSTANCES = [
  "https://nitter.privacyredirect.com",
  "https://nitter.tiekoetter.com",
  "https://nuku.trabun.org",
  "https://lightbrd.com",
  "https://nitter.net"
];

// Comptes de test
const TEST_ACCOUNTS = [
  "mathildepanot",
  "gabrielattal",
  "ericcoquerel"
];

// Configuration
const CONFIG = {
  requestDelay: 3000,      // 3s entre requetes
  pageTimeout: 45000,      // 45s timeout
  selectorTimeout: 10000,  // 10s pour selectors
  maxRetries: 2
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function testInstance(browser, instanceUrl) {
  console.log(`\n[TEST] ${instanceUrl}`);
  console.log("-".repeat(50));
  
  const results = {
    instance: instanceUrl,
    working: false,
    avg_response_ms: 0,
    tests: [],
    rate_limited: false
  };
  
  let totalTime = 0;
  let successCount = 0;
  
  for (const username of TEST_ACCOUNTS) {
    const testResult = {
      username,
      success: false,
      response_ms: 0,
      tweet_count: 0,
      error: null
    };
    
    let page = null;
    const startTime = Date.now();
    
    try {
      page = await browser.newPage();
      await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");
      
      const url = `${instanceUrl}/${username}`;
      console.log(`  -> Test @${username}...`);
      
      await page.goto(url, { 
        waitUntil: "networkidle2", 
        timeout: CONFIG.pageTimeout 
      });
      
      // Verifier si page d'erreur ou rate limit
      const pageContent = await page.content();
      
      if (pageContent.includes("rate limit") || pageContent.includes("Rate limit")) {
        testResult.error = "RATE_LIMITED";
        results.rate_limited = true;
        console.log(`     [!] RATE LIMITED`);
      } else if (pageContent.includes("Instance has been rate limited")) {
        testResult.error = "INSTANCE_RATE_LIMITED";
        results.rate_limited = true;
        console.log(`     [!] INSTANCE RATE LIMITED`);
      } else {
        // Chercher les tweets
        try {
          await page.waitForSelector(".timeline-item", { timeout: CONFIG.selectorTimeout });
          
          const tweetCount = await page.evaluate(() => {
            return document.querySelectorAll(".timeline-item").length;
          });
          
          testResult.success = true;
          testResult.tweet_count = tweetCount;
          successCount++;
          console.log(`     [OK] ${tweetCount} tweets trouves`);
          
        } catch (e) {
          testResult.error = "NO_TWEETS";
          console.log(`     [!] Pas de tweets visibles`);
        }
      }
      
    } catch (error) {
      testResult.error = error.message.substring(0, 50);
      console.log(`     [X] Erreur: ${testResult.error}`);
    } finally {
      if (page) await page.close();
    }
    
    testResult.response_ms = Date.now() - startTime;
    totalTime += testResult.response_ms;
    results.tests.push(testResult);
    
    // Delai entre requetes
    await sleep(CONFIG.requestDelay);
  }
  
  results.working = successCount > 0;
  results.avg_response_ms = Math.round(totalTime / TEST_ACCOUNTS.length);
  results.success_rate = `${successCount}/${TEST_ACCOUNTS.length}`;
  
  console.log(`\n  RESULTAT: ${results.working ? "OK" : "ECHEC"}`);
  console.log(`  Temps moyen: ${results.avg_response_ms}ms`);
  console.log(`  Succes: ${results.success_rate}`);
  
  return results;
}

async function testSearchFunction(browser, instanceUrl) {
  console.log(`\n[TEST RECHERCHE] ${instanceUrl}`);
  
  let page = null;
  const result = {
    search_working: false,
    response_ms: 0,
    error: null
  };
  
  try {
    page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");
    
    // Test recherche mensuelle (format utilise par le scraper)
    const searchUrl = `${instanceUrl}/search?f=tweets&q=from:mathildepanot+since:2025-12-01+until:2025-12-31`;
    console.log(`  -> Test recherche mensuelle...`);
    
    const startTime = Date.now();
    await page.goto(searchUrl, { waitUntil: "networkidle2", timeout: CONFIG.pageTimeout });
    
    try {
      await page.waitForSelector(".timeline-item", { timeout: CONFIG.selectorTimeout });
      
      const tweetCount = await page.evaluate(() => {
        return document.querySelectorAll(".timeline-item").length;
      });
      
      result.search_working = true;
      result.tweet_count = tweetCount;
      result.response_ms = Date.now() - startTime;
      console.log(`     [OK] ${tweetCount} tweets trouves en ${result.response_ms}ms`);
      
    } catch (e) {
      result.error = "Pas de resultats de recherche";
      console.log(`     [!] ${result.error}`);
    }
    
  } catch (error) {
    result.error = error.message.substring(0, 50);
    console.log(`     [X] Erreur: ${result.error}`);
  } finally {
    if (page) await page.close();
  }
  
  return result;
}

async function main() {
  console.log("=".repeat(60));
  console.log("TEST DES RATE LIMITS NITTER");
  console.log("Date:", new Date().toISOString());
  console.log("=".repeat(60));
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  
  const allResults = [];
  
  for (const instance of NITTER_INSTANCES) {
    const result = await testInstance(browser, instance);
    
    // Si l'instance fonctionne, tester aussi la recherche
    if (result.working) {
      const searchResult = await testSearchFunction(browser, instance);
      result.search_test = searchResult;
    }
    
    allResults.push(result);
    
    // Pause entre instances
    console.log("\n--- Pause 5s avant instance suivante ---\n");
    await sleep(5000);
  }
  
  await browser.close();
  
  // Resume
  console.log("\n" + "=".repeat(60));
  console.log("RESUME DES TESTS");
  console.log("=".repeat(60));
  
  const workingInstances = allResults.filter(r => r.working && !r.rate_limited);
  
  console.log(`\nInstances fonctionnelles: ${workingInstances.length}/${allResults.length}`);
  
  for (const result of allResults) {
    const status = result.working ? (result.rate_limited ? "[RATE LIMITED]" : "[OK]") : "[ECHEC]";
    const search = result.search_test?.search_working ? "recherche OK" : "recherche NON";
    console.log(`  ${status} ${result.instance}`);
    console.log(`      Temps: ${result.avg_response_ms}ms | ${search}`);
  }
  
  // Recommandation
  console.log("\n" + "=".repeat(60));
  console.log("RECOMMANDATION");
  console.log("=".repeat(60));
  
  if (workingInstances.length > 0) {
    // Trier par temps de reponse
    workingInstances.sort((a, b) => a.avg_response_ms - b.avg_response_ms);
    const best = workingInstances[0];
    
    console.log(`\nMeilleure instance: ${best.instance}`);
    console.log(`Temps moyen: ${best.avg_response_ms}ms`);
    
    // Calculer delai recommande
    const recommendedDelay = Math.max(3000, best.avg_response_ms + 2000);
    console.log(`\nDelai recommande entre requetes: ${recommendedDelay}ms`);
    console.log(`Estimation pour 200 deputes x 36 mois:`);
    console.log(`  ${200 * 36} requetes x ${recommendedDelay}ms = ~${Math.round(200 * 36 * recommendedDelay / 1000 / 60 / 60)}h`);
  } else {
    console.log("\n[!] Aucune instance fonctionnelle trouvee!");
    console.log("    Verifier: https://github.com/zedeus/nitter/wiki/Instances");
  }
  
  // Sauvegarder resultats
  const outputPath = "data/interim/nitter_rate_limit_test.json";
  await fs.writeFile(outputPath, JSON.stringify({
    tested_at: new Date().toISOString(),
    results: allResults,
    recommendation: workingInstances.length > 0 ? {
      best_instance: workingInstances[0].instance,
      avg_response_ms: workingInstances[0].avg_response_ms,
      recommended_delay_ms: Math.max(3000, workingInstances[0].avg_response_ms + 2000)
    } : null
  }, null, 2));
  
  console.log(`\nResultats sauvegardes: ${outputPath}`);
}

main().catch(err => {
  console.error("\n[ERREUR FATALE]", err);
  process.exit(1);
});








