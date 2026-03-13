/**
 * Phase 3 : Validation comptes Twitter
 * Teste 1 tweet par candidat via Nitter
 */

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
  nitterInstances: [
    'https://nitter.net',           // ✅ Working (200 OK) - Instance unique
  ],
  timeout: 15000,
  delayBetweenTests: 2000,
  maxCandidatesPerDepute: 5,  // Tester max 5 candidats par député
  headless: true
};

const INPUT_PATH = 'data/interim/twitter_candidates.json';
const OUTPUT_PATH = 'data/interim/validated_accounts.json';
const LOG_PATH = 'logs/validation_log.txt';

// ============================================================================
// LOGGING
// ============================================================================

async function log(message) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}\n`;

  console.log(message);

  // Append to log file
  await fs.mkdir(path.dirname(LOG_PATH), { recursive: true });
  await fs.appendFile(LOG_PATH, logMessage, 'utf-8');
}

// ============================================================================
// VALIDATION
// ============================================================================

async function testUsername(browser, username, nitterUrl) {
  /**
   * Teste si un username existe et est actif
   * Retourne : { exists: true/false, tweetFound: true/false }
   */

  const page = await browser.newPage();

  try {
    const url = `${nitterUrl}/${username}`;

    await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: CONFIG.timeout
    });

    // Attendre un peu pour que la page charge
    await new Promise(r => setTimeout(r, 2000));

    // Vérifier si le compte existe (plusieurs méthodes)
    const accountInfo = await page.evaluate(() => {
      // Méthode 1: Chercher badge vérifié gouvernement
      const govBadge = document.querySelector('.verified-icon.government');

      // Méthode 2: Chercher profile-card (header du compte)
      const profileCard = document.querySelector('.profile-card');

      // Méthode 3: Chercher timeline
      const timeline = document.querySelector('.timeline');
      const timelineItems = document.querySelectorAll('.timeline-item');

      // Méthode 4: Chercher message d'erreur "User not found"
      const errorMsg = document.querySelector('.error-panel');
      const notFound = errorMsg && errorMsg.innerText.includes('not found');

      return {
        hasGovBadge: !!govBadge,
        hasProfile: !!profileCard,
        hasTimeline: !!timeline,
        tweetCount: timelineItems.length,
        notFound: notFound,
        pageTitle: document.title
      };
    });

    await page.close();

    // Si "not found" → compte n'existe pas
    if (accountInfo.notFound) {
      return {
        exists: false,
        tweetFound: false,
        error: 'User not found'
      };
    }

    // Si profile card ou timeline existe → compte valide
    const accountExists = accountInfo.hasProfile || accountInfo.hasTimeline || accountInfo.hasGovBadge;

    return {
      exists: accountExists,
      tweetFound: accountInfo.tweetCount > 0,
      tweetCount: accountInfo.tweetCount,
      hasGovBadge: accountInfo.hasGovBadge,
      instance: nitterUrl
    };

  } catch (error) {
    await page.close();

    return {
      exists: false,
      tweetFound: false,
      error: error.message
    };
  }
}

async function validateDepute(browser, deputeData) {
  /**
   * Valide candidats pour un député
   * Retourne premier candidat fonctionnel ou null
   */

  const name = deputeData.depute_name;
  const candidates = deputeData.username_candidates.slice(0, CONFIG.maxCandidatesPerDepute);

  await log(`\n🔍 Test : ${name} (${candidates.length} candidats)`);

  for (const candidate of candidates) {
    await log(`   Candidat: @${candidate}`);

    // Tester sur chaque instance Nitter
    for (const instance of CONFIG.nitterInstances) {
      const result = await testUsername(browser, candidate, instance);

      // Accepter si le compte existe (même sans tweets visibles)
      if (result.exists) {
        const badge = result.hasGovBadge ? '🏛️ ' : '';
        const tweetInfo = result.tweetFound ? `${result.tweetCount} tweets` : 'profil actif';
        await log(`   ✅ TROUVÉ : ${badge}@${candidate} via ${instance} (${tweetInfo})`);

        return {
          depute_name: name,
          group: deputeData.group,
          priority_score: deputeData.priority_score,
          validated_username: candidate,
          test_instance: instance,
          tweet_count: result.tweetCount,
          has_gov_badge: result.hasGovBadge || false,
          validated_at: new Date().toISOString()
        };
      }

      // Delay entre instances
      await new Promise(r => setTimeout(r, 1000));
    }

    await log(`   ❌ Non trouvé : @${candidate}`);

    // Delay entre candidats
    await new Promise(r => setTimeout(r, CONFIG.delayBetweenTests));
  }

  await log(`   ⚠️  Aucun candidat valide pour ${name}`);
  return null;
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  console.log('='.repeat(70));
  console.log('PHASE 3 : VALIDATION COMPTES TWITTER');
  console.log('='.repeat(70));

  // Charger candidats
  const data = JSON.parse(await fs.readFile(INPUT_PATH, 'utf-8'));
  const candidates = data.candidates;

  await log(`\n📊 ${candidates.length} députés à valider`);
  await log(`📊 Instances Nitter : ${CONFIG.nitterInstances.join(', ')}`);

  // Lancer browser
  const browser = await puppeteer.launch({
    headless: CONFIG.headless,
    args: ['--no-sandbox']
  });

  await log('\n✅ Browser lancé');

  // Valider candidats
  const validated = [];
  const failed = [];

  for (let i = 0; i < candidates.length; i++) {
    const dep = candidates[i];

    await log(`\n[${i+1}/${candidates.length}] ${dep.depute_name}`);

    const result = await validateDepute(browser, dep);

    if (result) {
      validated.push(result);
    } else {
      failed.push({
        depute_name: dep.depute_name,
        group: dep.group,
        reason: 'Aucun candidat trouvé'
      });
    }

    // Sauvegarder progrès tous les 10
    if ((i + 1) % 10 === 0) {
      const progress = {
        validated_at: new Date().toISOString(),
        progress: `${i+1}/${candidates.length}`,
        validated_count: validated.length,
        failed_count: failed.length,
        validated_accounts: validated,
        failed_searches: failed
      };

      await fs.writeFile(OUTPUT_PATH, JSON.stringify(progress, null, 2), 'utf-8');
      await log(`\n💾 Progrès sauvegardé : ${validated.length} validés, ${failed.length} échecs`);
    }
  }

  await browser.close();

  // Résultat final
  const finalResult = {
    validated_at: new Date().toISOString(),
    total_tested: candidates.length,
    validated_count: validated.length,
    failed_count: failed.length,
    success_rate: (validated.length / candidates.length * 100).toFixed(1),
    validated_accounts: validated,
    failed_searches: failed
  };

  await fs.writeFile(OUTPUT_PATH, JSON.stringify(finalResult, null, 2), 'utf-8');

  console.log('\n' + '='.repeat(70));
  console.log('✅ PHASE 3 TERMINÉE');
  console.log('='.repeat(70));
  console.log(`\n📊 RÉSULTATS :`);
  console.log(`   Testés : ${candidates.length}`);
  console.log(`   Validés : ${validated.length} (${finalResult.success_rate}%)`);
  console.log(`   Échecs : ${failed.length}`);
  console.log(`\n💾 Résultats : ${OUTPUT_PATH}`);
  console.log(`📋 Logs : ${LOG_PATH}`);
}

main().catch(console.error);
