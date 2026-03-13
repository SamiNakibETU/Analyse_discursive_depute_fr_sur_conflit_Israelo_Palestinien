/**
 * Test rapide de détection Nitter
 * Teste Benjamin Haddad (@benjaminhaddad)
 */

const puppeteer = require('puppeteer');

async function testAccount(username, instance) {
  console.log(`\n🔍 Test: ${username} sur ${instance}`);

  const browser = await puppeteer.launch({
    headless: false,  // Visible pour debug
    slowMo: 50
  });

  const page = await browser.newPage();

  try {
    const url = `${instance}/${username}`;
    console.log(`📡 Chargement: ${url}`);

    await page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: 15000
    });

    // Attendre chargement
    await new Promise(r => setTimeout(r, 3000));

    // Analyser page
    const info = await page.evaluate(() => {
      return {
        // Sélecteurs
        hasGovBadge: !!document.querySelector('.verified-icon.government'),
        hasProfileCard: !!document.querySelector('.profile-card'),
        hasTimeline: !!document.querySelector('.timeline'),
        tweetCount: document.querySelectorAll('.timeline-item').length,

        // Erreur
        hasError: !!document.querySelector('.error-panel'),
        errorText: document.querySelector('.error-panel')?.innerText || '',

        // Info
        pageTitle: document.title,
        profileName: document.querySelector('.profile-card-fullname')?.innerText || '',
        username: document.querySelector('.profile-card-username')?.innerText || ''
      };
    });

    console.log('\n📊 Résultat:');
    console.log(`   Title: ${info.pageTitle}`);
    console.log(`   Profile: ${info.profileName} (${info.username})`);
    console.log(`   Badge Gov: ${info.hasGovBadge ? '✅' : '❌'}`);
    console.log(`   Profile Card: ${info.hasProfileCard ? '✅' : '❌'}`);
    console.log(`   Timeline: ${info.hasTimeline ? '✅' : '❌'}`);
    console.log(`   Tweets: ${info.tweetCount}`);
    console.log(`   Erreur: ${info.hasError ? '⚠️ ' + info.errorText : '✅ Aucune'}`);

    const accountExists = info.hasProfileCard || info.hasTimeline || info.hasGovBadge;
    console.log(`\n${accountExists ? '✅ COMPTE VALIDÉ' : '❌ COMPTE NON TROUVÉ'}`);

    // Pause pour inspecter visuellement
    console.log('\n⏸️  Pause 5 secondes pour inspection visuelle...');
    await new Promise(r => setTimeout(r, 5000));

  } catch (error) {
    console.error(`❌ Erreur: ${error.message}`);
  } finally {
    await browser.close();
  }
}

async function main() {
  console.log('='.repeat(70));
  console.log('TEST DÉTECTION NITTER - Comptes Réels');
  console.log('='.repeat(70));

  // Test comptes réels connus
  await testAccount('benjaminhaddad', 'https://nitter.net');      // Benjamin Haddad
  await testAccount('jnbarrot', 'https://nitter.net');            // Jean-Noël Barrot
  await testAccount('SabrinaSebaihi', 'https://nitter.net');      // Sabrina Sebaihi
  await testAccount('elisa_martin_gre', 'https://nitter.net');    // Élisa Martin

  // Test compte inexistant
  await testAccount('qsdlfkjqsdlfkjqsdf123456', 'https://nitter.net');

  console.log('\n='.repeat(70));
  console.log('✅ Tests terminés');
  console.log('='.repeat(70));
}

main().catch(console.error);
