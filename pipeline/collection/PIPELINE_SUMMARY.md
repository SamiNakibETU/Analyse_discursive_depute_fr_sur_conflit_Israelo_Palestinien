# Pipeline Twitter - Résumé Exécutif

## 🎯 Objectif

Découvrir automatiquement les comptes Twitter de ~200 députés ayant parlé de Gaza/Palestine à l'Assemblée Nationale.

## 📊 État Actuel

- ✅ **736 interventions** enrichies (avec noms députés)
- ✅ **11 comptes Twitter** déjà mappés manuellement
- ⏳ **~190 députés** à découvrir automatiquement

## 🚀 Solution : Pipeline 4 Phases

### Architecture

```
📄 interventions_enriched.jsonl (736)
    ↓ Phase 1: Extract (30s)
📋 deputes_unique.json (~200)
    ↓ Phase 2: Generate (1min)
🎯 twitter_candidates.json (~1140 candidats)
    ↓ Phase 3: Validate (1-2h)
✅ validated_accounts.json (~80-110)
    ↓ Phase 4: Scrape (2-3h)
🐦 twitter_deputes_final.jsonl (4K-8K tweets)
```

## 📝 Scripts Créés

| Script | Langage | Durée | Description |
|--------|---------|-------|-------------|
| `phase1_extract_deputes.py` | Python | 30s | Extrait orateurs uniques + stats |
| `phase2_generate_candidates.py` | Python | 1min | Génère patterns usernames (6/député) |
| `phase3_validate_accounts.js` | Node.js | 1-2h | Teste 1 tweet via Nitter |
| `phase4_scrape_validated.js` | Node.js | 2-3h | Scrappe 100 tweets/compte |

## ⚡ Exécution Rapide

### Option 1: Script automatisé
```bash
cd final
scripts\run_full_pipeline.bat
```

### Option 2: Manuel (recommandé pour monitoring)
```bash
cd final

# Phase 1 (30s)
python scripts/phase1_extract_deputes.py

# Phase 2 (1min)
python scripts/phase2_generate_candidates.py

# Phase 3 (1-2h) ⚠️ CRITIQUE
node scripts/phase3_validate_accounts.js

# Phase 4 (2-3h)
node scripts/phase4_scrape_validated.js
```

## 🔍 Monitoring

### Logs Phase 3 (temps réel)
```bash
# Terminal 1: Exécution
node scripts/phase3_validate_accounts.js

# Terminal 2: Logs live
tail -f logs/validation_log.txt

# Terminal 3: Compteur
python -c "import json; print(json.load(open('data/interim/validated_accounts.json')).get('validated_count', 0), 'validés')"
```

## 📊 Résultats Attendus

| Phase | Input | Output | Taux Succès |
|-------|-------|--------|-------------|
| 1 | 736 interventions | ~200 députés | 100% |
| 2 | 200 députés | ~190 à valider (11 mappés) | 100% |
| 3 | ~1140 candidats | ~80-110 validés | **40-60%** |
| 4 | 100 comptes | ~5K tweets | 90% |

## 🎨 Stratégie Validation (Phase 3)

### Patterns Username Testés
Pour "Gabriel Attal":
1. `GabrielAttal` ← PrenomNom
2. `AttalGabriel` ← NomPrenom
3. `gabriel_attal` ← snake_case
4. `GAttal` ← InitialeNom
5. `gabrielattal` ← minuscule
6. `Attal` ← nom seul

### Instances Nitter (fallback)
1. `nitter.poast.org` ✅ Stable
2. `nitter.cz` ✅ Stable
3. `nitter.privacydev.net` ⚠️ Instable
4. `nitter.net` ⚠️ Instable

### Algorithme Validation
```
Pour chaque député:
  Pour les 5 premiers candidats:
    Pour chaque instance Nitter:
      Si 1 tweet trouvé → VALIDÉ ✅
      Sinon essayer instance suivante
    Delay 2s
  Si aucun candidat → ÉCHEC ❌
```

## 💾 Fichiers Générés

```
final/
├── data/
│   ├── interim/
│   │   ├── deputes_unique.json          ← Phase 1
│   │   ├── twitter_candidates.json      ← Phase 2
│   │   └── validated_accounts.json      ← Phase 3 ⭐
│   └── processed/
│       └── twitter_deputes_final.jsonl  ← Phase 4 🎯
├── logs/
│   └── validation_log.txt               ← Phase 3 logs
└── scripts/
    ├── phase1_extract_deputes.py
    ├── phase2_generate_candidates.py
    ├── phase3_validate_accounts.js
    └── phase4_scrape_validated.js
```

## 🛡️ Robustesse

### ✅ Sauvegarde Progressive
- Phase 3 sauvegarde tous les **10 comptes**
- Peut reprendre après interruption

### ✅ Fallback Multi-Instances
- Teste 4 instances Nitter
- Continue si une instance tombe

### ✅ Error Handling
- Skip compte si timeout (15s)
- Continue si un député échoue
- Logs détaillés pour debug

### ✅ Rate Limiting
- 2s entre comptes
- 1s entre instances Nitter
- Respecte ToS Nitter

## 📈 Timeline Estimée

| Phase | Durée | Cumul |
|-------|-------|-------|
| Phase 1 | 30s | 0h00 |
| Phase 2 | 1min | 0h01 |
| Phase 3 | **1-2h** | 1h-2h |
| Phase 4 | 2-3h | 3h-5h |

**Total : 3-5 heures** (dont 70% automatisé, surveillance légère)

## 🎯 Prochaines Étapes

### 1. Vérifier Prérequis
```bash
python --version  # >= 3.8
node --version    # >= 14
npm list puppeteer  # Installé
```

### 2. Tester Instance Nitter
```bash
curl -I https://nitter.poast.org/faureolivier
# Doit retourner 200 OK
```

### 3. Lancer Phase 1-2 (rapide)
```bash
python scripts/phase1_extract_deputes.py
python scripts/phase2_generate_candidates.py
```

### 4. Analyser Candidats
```bash
python -c "import json; d=json.load(open('data/interim/twitter_candidates.json')); print(f'{d[\"to_find\"]} députés, ~{sum(len(c[\"username_candidates\"]) for c in d[\"candidates\"])} candidats')"
```

### 5. Lancer Phase 3 (monitoring)
```bash
# Terminal 1
node scripts/phase3_validate_accounts.js

# Terminal 2 (optionnel)
tail -f logs/validation_log.txt
```

### 6. Vérifier Résultats
```bash
python -c "import json; d=json.load(open('data/interim/validated_accounts.json')); print(f'{d[\"validated_count\"]} validés ({d[\"success_rate\"]}%)')"
```

### 7. Lancer Phase 4 (si >50 validés)
```bash
node scripts/phase4_scrape_validated.js
```

## 🔧 Troubleshooting

### ❌ "Module puppeteer not found"
```bash
npm install puppeteer
```

### ❌ Phase 3 bloque
- Vérifier instances Nitter (curl)
- Mettre `headless: false` pour debug visuel
- Vérifier logs: `logs/validation_log.txt`

### ❌ Taux validation <30%
- Ajouter patterns usernames dans Phase 2
- Augmenter `maxCandidatesPerDepute` (5 → 10)
- Tester autres instances Nitter

### ❌ Timeout Phase 4
- Réduire `maxTweetsPerUser` (100 → 50)
- Augmenter `scrollDelayMs` (2500 → 3500)

## 📚 Documentation

- **Guide complet** : `PIPELINE_TWITTER_README.md`
- **Code source** : `scripts/phase*.{py,js}`
- **Logs** : `logs/validation_log.txt`

## 📞 Contact

- Script basé sur scraper Nitter working : `archive/pocs/nitter-scraper-basics/scraper.js`
- Instances Nitter testées manuellement avant exécution

---

**Prêt à lancer ?** Commencez par Phase 1-2 (2 minutes) pour valider le setup.
