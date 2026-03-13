/**
 * Génère fighting_words.json depuis le CSV source.
 * Usage: node scripts/prepare_fighting_words.js
 */
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const csvPath = join(__dirname, '../../data/results/fighting_words.csv');
const outPath = join(__dirname, '../src/data/fighting_words.json');

const csv = readFileSync(csvPath, 'utf-8');
const lines = csv.trim().split('\n').slice(1);

const rows = lines.map((line) => {
  const [word, zStr] = line.split(',');
  const z = parseFloat(zStr);
  return { word, z };
});

const gauche = rows
  .filter((r) => r.z > 0)
  .sort((a, b) => b.z - a.z)
  .slice(0, 10)
  .map((r) => ({ word: r.word, z: Math.round(r.z * 100) / 100 }));

const droite = rows
  .filter((r) => r.z < 0)
  .sort((a, b) => a.z - b.z)
  .slice(0, 10)
  .map((r) => ({ word: r.word, z: Math.round(Math.abs(r.z) * 100) / 100 }));

const output = { gauche, droite };
writeFileSync(outPath, JSON.stringify(output, null, 2), 'utf-8');
console.log(`Written ${outPath}`);
