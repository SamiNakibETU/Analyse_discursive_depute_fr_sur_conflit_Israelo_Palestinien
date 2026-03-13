# Pipeline Incrémental de Découverte Twitter

## Vue d'ensemble

Pipeline en 4 phases pour découvrir automatiquement les comptes Twitter des députés ayant parlé de Gaza/Palestine à l'Assemblée Nationale.

**Stratégie** : Validation légère (1 tweet) avant scraping complet pour éviter les recherches inutiles.

---

## Architecture

```
📊 interventions_enriched.jsonl (736 lignes)
    ↓
🔍 Phase 1: Extract Députés
    ↓
📋 deputes_unique.json (~200 députés)
    ↓
🎯 Phase 2: Generate Candidates
    ↓
📝 twitter_candidates.json (patterns usernames)
    ↓
✅ Phase 3: Validate Accounts (1 tweet test)
    ↓
💾 validated_accounts.json (comptes confirmés)
    ↓
🐦 Phase 4: Scrape Complet (100 tweets/compte)
    ↓
📦 twitter_deputes_final.jsonl
```

---

## Prérequis

### Python
```bash
# Vérifier version Python
python --version  # >= 3.8
```

### Node.js & Puppeteer
```bash
# Vérifier version Node
node --version  # >= 14

# Installer Puppeteer si nécessaire
npm install puppeteer
```

---

## Phase 1: Extraction Députés (~30 secondes)

**Objectif** : Extraire tous les orateurs uniques depuis les interventions enrichies.

### Exécution
```bash
cd D:\Users\Proprietaire\Desktop\Projets\Revirement_politique_fr_gaza\final
python scripts/phase1_extract_deputes.py
```

### Output
- `data/interim/deputes_unique.json`

### Contenu
```json
{
  "extracted_at": "2025-10-19T...",
  "total_interventions": 736,
  "unique_speakers": 203,
  "deputes": [
    {
      "name": "Aymeric Caron",
      "normalized_name": "aymeric caron",
      "group": "LFI",
      "interventions_count": 15,
      "priority_score": 100.0,
      "top_keywords": {"gaza": 12, "palestine": 8},
      "first_intervention": "2023-10-15",
      "last_intervention": "2024-06-04"
    }
  ]
}
```

### Vérification
```bash
# Afficher top 10
python -c "import json; d=json.load(open('data/interim/deputes_unique.json')); [print(f\"{i}. {dep['name']} ({dep['interventions_count']} inter.)\") for i, dep in enumerate(d['deputes'][:10], 1)]"
```

---

## Phase 2: Génération Candidats (~1 minute)

**Objectif** : Générer patterns usernames Twitter possibles pour chaque député.

### Exécution
```bash
python scripts/phase2_generate_candidates.py
```

### Output
- `data/interim/twitter_candidates.json`

### Patterns Générés
Pour "Gabriel Attal":
- `GabrielAttal` (PrenomNom)
- `AttalGabriel` (NomPrenom)
- `gabriel_attal` (prenom_nom)
- `GAttal` (InitialeNom)
- `gabrielattal` (minuscule)
- `Attal` (nom seul)

### Vérification
```bash
# Compter candidats
python -c "import json; d=json.load(open('data/interim/twitter_candidates.json')); print(f'À valider: {d[\"to_find\"]} députés')"
```

---

## Phase 3: Validation Comptes (1-2 heures)

**CRITIQUE** : Teste chaque candidat sur Nitter (1 tweet de validation).

### Exécution
```bash
node scripts/phase3_validate_accounts.js
```

### Fonctionnement
- Teste max 5 candidats par député
- Essaye 4 instances Nitter (fallback)
- Sauvegarde progrès tous les 10 comptes
- Logs détaillés dans `logs/validation_log.txt`

### Suivi en temps réel
```bash
# Terminal 1 : Lancer validation
node scripts/phase3_validate_accounts.js

# Terminal 2 : Suivre logs
tail -f logs/validation_log.txt

# Terminal 3 : Compter validés
python -c "import json; d=json.load(open('data/interim/validated_accounts.json')); print(f'Validés: {d.get(\"validated_count\", 0)}')"
```

### Output
- `data/interim/validated_accounts.json`
- `logs/validation_log.txt`

### Format Résultat
```json
{
  "validated_at": "2025-10-19T...",
  "total_tested": 192,
  "validated_count": 87,
  "failed_count": 105,
  "success_rate": "45.3",
  "validated_accounts": [
    {
      "depute_name": "Aymeric Caron",
      "group": "LFI",
      "validated_username": "AymericCaron",
      "test_instance": "https://nitter.poast.org",
      "tweet_count": 156,
      "validated_at": "2025-10-19T14:23:45Z"
    }
  ],
  "failed_searches": [...]
}
```

### En cas d'interruption
Le script sauvegarde tous les 10 comptes. Vous pouvez :
1. Relancer le script (il reprendra depuis le début)
2. Ou modifier le script pour skip les déjà validés

---

## Phase 4: Scraping Complet (2-3 heures)

**Objectif** : Scraper 100 tweets par compte validé (keywords Gaza/Palestine uniquement).

### Exécution
```bash
node scripts/phase4_scrape_validated.js
```

### Fonctionnement
- Charge `validated_accounts.json` depuis Phase 3
- Scrappe max 100 tweets/compte
- Filtre keywords : gaza, palestine, israël, hamas, otage, rafah, etc.
- Essaye instances Nitter dans l'ordre

### Output
- `data/processed/twitter_deputes_final.jsonl`

### Format JSONL
Chaque ligne = 1 député scraped
```json
{
  "speaker": "Aymeric Caron",
  "handle": "AymericCaron",
  "group": "LFI",
  "scraped_at": "2025-10-19T16:45:00Z",
  "tweets": [
    {
      "url": "/AymericCaron/status/...",
      "content": "Le massacre à Gaza doit cesser...",
      "date": "2024-05-15 14:32:00 UTC",
      "fullUrl": "https://nitter.poast.org/AymericCaron/status/...",
      "stats": {
        "replies": 45,
        "retweets": 234,
        "quotes": 12,
        "likes": 1567
      }
    }
  ]
}
```

### Vérification
```bash
# Compter tweets totaux
python -c "import json; tweets=0; [tweets:=tweets+len(json.loads(line)['tweets']) for line in open('data/processed/twitter_deputes_final.jsonl')]; print(f'Total tweets: {tweets}')"
```

---

## Monitoring & Logs

### Logs Phase 3 (Validation)
```bash
# Temps réel
tail -f logs/validation_log.txt

# Rechercher échecs
grep "❌" logs/validation_log.txt

# Rechercher succès
grep "✅ TROUVÉ" logs/validation_log.txt
```

### Compteurs Rapides
```bash
# Phase 1
python -c "import json; print(json.load(open('data/interim/deputes_unique.json'))['unique_speakers'], 'députés')"

# Phase 2
python -c "import json; print(json.load(open('data/interim/twitter_candidates.json'))['to_find'], 'à valider')"

# Phase 3
python -c "import json; d=json.load(open('data/interim/validated_accounts.json')); print(f\"{d['validated_count']}/{d['total_tested']} validés ({d['success_rate']}%)\")"

# Phase 4
wc -l data/processed/twitter_deputes_final.jsonl
```

---

## Gestion des Erreurs

### Instance Nitter Down
Le script essaye automatiquement 4 instances dans l'ordre.

**Test manuel** :
```bash
# Tester instance
curl -I https://nitter.poast.org/faureolivier
```

Si toutes sont down, mettre à jour `CONFIG.nitterInstances` dans les scripts.

### Timeout Phase 3
Si un compte bloque (timeout), le script continue automatiquement au suivant après 15 secondes.

### Mémoire insuffisante
Phase 4 peut être lourde. Réduire `maxTweetsPerUser` dans le script.

---

## Optimisations

### Tester Instance Nitter
Avant Phase 3, vérifier instances actives :
```bash
curl -I https://nitter.poast.org
curl -I https://nitter.cz
curl -I https://nitter.privacydev.net
```

### Parallélisation Phase 3
Pour accélérer, modifier `phase3_validate_accounts.js` pour lancer plusieurs browsers en parallèle (avancé).

### Reprendre Phase 3
Si interrompu à 50%, modifier le script pour filter députés déjà validés :
```javascript
const alreadyValidated = new Set(validated.map(v => v.depute_name));
const toTest = candidates.filter(c => !alreadyValidated.has(c.depute_name));
```

---

## Résultats Attendus

### Phase 1
- ~200 députés uniques identifiés

### Phase 2
- ~190 députés à valider (11 déjà mappés)
- ~6 candidats/député en moyenne

### Phase 3
- Taux succès estimé : **40-60%**
- ~80-110 comptes Twitter validés

### Phase 4
- ~80-110 comptes scrapés
- ~50-80 tweets/compte (filtrés keywords)
- **Total : 4000-8000 tweets**

---

## Commandes Complètes

```bash
# Setup
cd D:\Users\Proprietaire\Desktop\Projets\Revirement_politique_fr_gaza\final

# Phase 1 (30 sec)
python scripts/phase1_extract_deputes.py

# Phase 2 (1 min)
python scripts/phase2_generate_candidates.py

# Phase 3 (1-2h)
node scripts/phase3_validate_accounts.js

# Phase 4 (2-3h)
node scripts/phase4_scrape_validated.js
```

---

## Troubleshooting

### Erreur "Module not found: puppeteer"
```bash
npm install puppeteer
```

### Erreur "File not found: interventions_enriched.jsonl"
Vérifier path dans scripts (doit être relatif au dossier `final/`)

### Phase 3 bloque
Ctrl+C et vérifier logs. Comptes validés sont sauvegardés tous les 10.

### Pas assez de comptes validés
- Vérifier instances Nitter actives
- Augmenter `maxCandidatesPerDepute` (actuellement 5)
- Ajouter patterns usernames dans Phase 2

---

## Fichiers Générés

```
final/
├── data/
│   ├── interim/
│   │   ├── deputes_unique.json          # Phase 1
│   │   ├── twitter_candidates.json      # Phase 2
│   │   └── validated_accounts.json      # Phase 3
│   └── processed/
│       └── twitter_deputes_final.jsonl  # Phase 4
└── logs/
    └── validation_log.txt               # Phase 3
```

---

## Support

**Instances Nitter testées** :
- https://nitter.poast.org ✅
- https://nitter.cz ✅
- https://nitter.privacydev.net ⚠️ (instable)
- https://nitter.net ⚠️ (instable)

**Working scraper reference** :
- `D:\Users\Proprietaire\Desktop\Projet_perso\Projets\Revirement_politique_fr_gaza\archive\pocs\nitter-scraper-basics\scraper.js`

---

## Notes Importantes

⚠️ **Rate Limiting** : Respecter délais entre requêtes (2s entre comptes)

⚠️ **Instances Nitter** : Peuvent tomber sans préavis. Tester manuellement avant lancement.

⚠️ **Headless Mode** : Phase 3 en headless par défaut. Mettre `headless: false` pour debug visuel.

⚠️ **Sauvegarde Progressive** : Phase 3 sauvegarde tous les 10 comptes. Ne pas interrompre brutalement.

✅ **Incrémental** : Chaque phase indépendante. Peut arrêter/reprendre.

✅ **Logs détaillés** : Tout est tracé dans `logs/validation_log.txt`
