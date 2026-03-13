#!/usr/bin/env node
/**
 * Extrait les comptes Twitter depuis le fichier HTML
 */

const fs = require("fs").promises;
const path = require("path");

async function main() {
  const htmlPath = path.resolve("../twitter_account_deputé.html");
  const html = await fs.readFile(htmlPath, "utf-8");

  // Extraire tous les comptes Twitter
  // Format : <td><a href="/deputes/fiche/...">Nom</a></td> ... <td><a class="twitter" href="https://twitter.com/@username/">
  const deputeRegex = /<td><a href="\/deputes\/fiche\/[^"]+">([^<]+)<\/a><\/td>/g;
  const twitterRegex = /<a class="twitter" href="https:\/\/twitter\.com\/@([^\/]+)\//g;

  const deputes = [];
  const twitters = [];
  let match;

  while ((match = deputeRegex.exec(html)) !== null) {
    deputes.push(match[1].trim());
  }

  while ((match = twitterRegex.exec(html)) !== null) {
    twitters.push(match[1].toLowerCase());
  }

  console.log(`Députés trouvés: ${deputes.length}`);
  console.log(`Comptes Twitter trouvés: ${twitters.length}\n`);

  // Associer députés et comptes Twitter (même ordre dans le HTML)
  const accounts = [];
  const minLength = Math.min(deputes.length, twitters.length);

  for (let i = 0; i < minLength; i++) {
    if (deputes[i] && twitters[i]) {
      accounts.push({
        depute_name: deputes[i],
        validated_username: twitters[i],
        group: "Unknown",
        priority_score: 5,
      });
    }
  }

  console.log(`✅ ${accounts.length} comptes extraits\n`);

  // Afficher les 10 premiers
  console.log("Premiers comptes:");
  accounts.slice(0, 10).forEach((acc, i) => {
    console.log(`${i + 1}. ${acc.depute_name} (@${acc.validated_username})`);
  });

  // Sauvegarder
  const output = {
    extracted_at: new Date().toISOString(),
    source: "twitter_account_deputé.html",
    validated_accounts: accounts,
  };

  const outputPath = path.resolve("data/interim/extracted_accounts.json");
  await fs.writeFile(outputPath, JSON.stringify(output, null, 2), "utf-8");

  console.log(`\n💾 Sauvegardé: ${outputPath}`);
}

main().catch(console.error);
