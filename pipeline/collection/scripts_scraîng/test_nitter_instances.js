#!/usr/bin/env node
/**
 * TEST INSTANCES NITTER
 *
 * Teste automatiquement 15+ instances Nitter pour identifier
 * celles qui sont opérationnelles et fonctionnelles
 */

const puppeteer = require('puppeteer');
const https = require('https');
const http = require('http');
const { URL } = require('url');
const fs = require('fs').promises;

const INSTANCES = [
  'https://nitter.net',
  'https://nitter.it',
  'https://nitter.pussthecat.org',
  'https://nitter.fdn.fr',
  'https://nitter.kavin.rocks',
  'https://nitter.unixfox.eu',
  'https://nitter.moomoo.me',
  'https://nitter.fly.dev',
  'https://nitter.woodland.cafe',
  'https://nitter.projectsegfau.lt',
  'https://nitter.eu.projectsegfau.lt',
  'https://nitter.esmailelbob.xyz',
  'https://nitter.mint.lgbt',
  'https://nitter.bus-hit.me',
  'https://nitter.tiekoetter.com',
  'https://nitter.d420.de',
  'https://nitter.nixnet.services'
];

function httpRequest(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === 'https:' ? https : http;

    const timer = setTimeout(() => {
      req.destroy();
      reject(new Error('Timeout'));
    }, timeout);

    const req = client.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' },
      timeout: timeout
    }, (res) => {
      clearTimeout(timer);

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          body: data,
          headers: res.headers
        });
      });
    });

    req.on('error', (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

async function testInstanceBasic(instance) {
  try {
    const start = Date.now();
    const response = await httpRequest(instance, 10000);
    const latency = Date.now() - start;

    // Accept 200, 301, 302
    if (response.statusCode >= 200 && response.statusCode < 400) {
      let score = 10;
      score -= Math.max(0, Math.floor((latency - 2000) / 1000) * 5);

      return {
        instance,
        basicTest: 'OK',
        statusCode: response.statusCode,
        latency,
        score: Math.max(0, score)
      };
    } else {
      return {
        instance,
        basicTest: 'FAIL',
        error: `HTTP ${response.statusCode}`,
        score: 0
      };
    }
  } catch (error) {
    return {
      instance,
      basicTest: 'FAIL',
      error: error.message,
      score: 0
    };
  }
}

async function testInstanceFunctional(browser, instance) {
  let page;

  try {
    page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

    const testUrl = `${instance}/search?f=tweets&q=from:mathildepanot+since:2023-01-01+until:2023-01-31`;

    const start = Date.now();
    await page.goto(testUrl, {
      waitUntil: 'networkidle2',
      timeout: 20000
    });
    const latency = Date.now() - start;

    // Vérifier présence tweets
    await new Promise(r => setTimeout(r, 2000)); // Laisser JS charger

    const tweetCount = await page.evaluate(() => {
      return document.querySelectorAll('.timeline-item').length;
    });

    await page.close();

    if (tweetCount === 0) {
      return {
        functionalTest: 'FAIL',
        error: 'Aucun tweet détecté',
        tweetCount: 0,
        latency,
        score: 0
      };
    }

    let score = 20; // Base score for functional
    if (tweetCount >= 10) score += 10;
    else if (tweetCount >= 5) score += 5;
    score -= Math.max(0, Math.floor((latency - 3000) / 1000) * 2);

    return {
      functionalTest: 'OK',
      tweetCount,
      latency,
      score: Math.max(0, score)
    };

  } catch (error) {
    if (page) await page.close();
    return {
      functionalTest: 'FAIL',
      error: error.message,
      score: 0
    };
  }
}

async function main() {
  console.log('======================================================================');
  console.log('🔍 TEST INSTANCES NITTER - Recherche instances fonctionnelles');
  console.log('======================================================================');
  console.log(`\n📊 ${INSTANCES.length} instances à tester\n`);

  const results = [];

  // Phase 1: Tests basiques (rapides)
  console.log('Phase 1/2 : Tests basiques (HTTP)...\n');

  for (let i = 0; i < INSTANCES.length; i++) {
    const instance = INSTANCES[i];
    process.stdout.write(`[${i+1}/${INSTANCES.length}] ${instance.padEnd(45)} `);

    const result = await testInstanceBasic(instance);

    if (result.basicTest === 'OK') {
      console.log(`✅ HTTP ${result.statusCode} (${result.latency}ms)`);
      results.push(result);
    } else {
      console.log(`❌ ${result.error}`);
    }

    await new Promise(r => setTimeout(r, 500)); // Rate limiting
  }

  const passedBasic = results.filter(r => r.basicTest === 'OK');
  console.log(`\n✅ ${passedBasic.length}/${INSTANCES.length} instances répondent\n`);

  if (passedBasic.length === 0) {
    console.log('❌ AUCUNE instance ne répond. Toutes sont DOWN.');
    console.log('\n💡 Solutions :');
    console.log('   1. Attendre quelques heures et réessayer');
    console.log('   2. Demander Twitter API Academic Research');
    console.log('   3. Analyser données déjà collectées (3,600 tweets)');

    // Sauvegarder résultat vide
    await fs.writeFile(
      'data/interim/nitter_instances_working.json',
      JSON.stringify({
        tested_at: new Date().toISOString(),
        total_tested: INSTANCES.length,
        functional_count: 0,
        functional_instances: []
      }, null, 2)
    );

    return;
  }

  // Phase 2: Tests fonctionnels (lents mais précis)
  console.log('Phase 2/2 : Tests fonctionnels (scraping test)...\n');

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  for (let i = 0; i < passedBasic.length; i++) {
    const result = passedBasic[i];
    process.stdout.write(`[${i+1}/${passedBasic.length}] ${result.instance.padEnd(45)} `);

    const funcResult = await testInstanceFunctional(browser, result.instance);
    Object.assign(result, funcResult);
    result.totalScore = result.score + funcResult.score;

    if (funcResult.functionalTest === 'OK') {
      console.log(`✅ ${funcResult.tweetCount} tweets (${funcResult.latency}ms, score: ${result.totalScore})`);
    } else {
      console.log(`❌ ${funcResult.error}`);
    }

    await new Promise(r => setTimeout(r, 3000));
  }

  await browser.close();

  // Résultats finaux
  const functional = results
    .filter(r => r.functionalTest === 'OK' && r.totalScore >= 15)
    .sort((a, b) => b.totalScore - a.totalScore);

  console.log('\n' + '='.repeat(70));
  console.log('📊 RÉSULTATS FINAUX');
  console.log('='.repeat(70));

  if (functional.length === 0) {
    console.log('\n❌ AUCUNE instance fonctionnelle trouvée');
    console.log('\n💡 Toutes les instances Nitter testées sont DOWN ou bloquées.');
    console.log('   Recommandation : Passer à Twitter API Academic Research');

    await fs.writeFile(
      'data/interim/nitter_instances_working.json',
      JSON.stringify({
        tested_at: new Date().toISOString(),
        total_tested: INSTANCES.length,
        functional_count: 0,
        functional_instances: []
      }, null, 2)
    );

    return;
  }

  console.log(`\n✅ ${functional.length} instance(s) FONCTIONNELLE(S) :\n`);

  functional.forEach((r, i) => {
    console.log(`${i+1}. ${r.instance}`);
    console.log(`   Score: ${r.totalScore}/40`);
    console.log(`   Latency: ${r.latency}ms`);
    console.log(`   Tweets trouvés: ${r.tweetCount}`);
    console.log();
  });

  // Sauvegarder résultats
  const output = {
    tested_at: new Date().toISOString(),
    total_tested: INSTANCES.length,
    functional_count: functional.length,
    functional_instances: functional.map(r => ({
      url: r.instance,
      score: r.totalScore,
      latency: r.latency,
      tweet_count: r.tweetCount
    }))
  };

  await fs.writeFile(
    'data/interim/nitter_instances_working.json',
    JSON.stringify(output, null, 2),
    'utf-8'
  );

  console.log('💾 Résultats sauvegardés : data/interim/nitter_instances_working.json');
  console.log('\n✅ TESTS TERMINÉS');
  console.log('\n🚀 Prochaine étape :');
  console.log('   node scripts/scrape_nitter_search_monthly.js --input data/interim/extracted_accounts.json');
}

main().catch(console.error);
