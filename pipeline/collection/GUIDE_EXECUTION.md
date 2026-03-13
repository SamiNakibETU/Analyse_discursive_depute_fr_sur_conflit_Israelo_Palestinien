# Guide d'Execution - Projet Gaza/Palestine

**Date**: 5 janvier 2026  
**Status**: Pret pour execution

---

## Resume des Corrections Effectuees

### 1. Pipeline AN (Assemblee Nationale)
- [x] **BUG CORRIGE**: Regex word boundary `\\b` -> `\b` dans `keywords.py`
- [x] **MOTS-CLES AMELIORES**: 94 termes au lieu de ~50 (ajout: UNRWA, 7 octobre, famine, etc.)
- [x] **PERIODE AJUSTEE**: 2023-01-01 -> 2026-01-31

### 2. Pipeline Twitter
- [x] **INSTANCES TESTEES**: 3 fonctionnelles sur 5
- [x] **RATE LIMITS**: Delai 4s recommande (teste sans probleme)
- [x] **MAPPING DEPUTES**: 115/203 deputes avec Twitter trouve

### 3. Fichiers Archives
- syria-monitor-mvp/ -> `archive/legacy_workspaces/_archive/other_projects/`
- Anciens scripts et HTML -> `archive/legacy_workspaces/_archive/`

---

## Etape 1: Relancer le Pipeline AN

Le pipeline doit etre relance pour beneficier du bug fix et des nouveaux mots-cles.

```powershell
cd "D:\Users\Proprietaire\Desktop\Projet_perso\Projets\Revirement_politique_fr_gaza\final"

# Activer PYTHONPATH
$env:PYTHONPATH = "src"

# Lancer le pipeline
python scripts/run_pipeline.py
```

**Duree estimee**: 30-60 minutes  
**Resultat attendu**: ~1000-2000 interventions (vs 736 avant correction)

---

## Etape 2: Pipeline Twitter

### 2.1 Verifier la liste des deputes

```powershell
# Regenerer la liste propre
python scripts/build_twitter_deputes_clean.py
```

Resultat: `data/interim/deputes_twitter_clean.json`

### 2.2 Test avec 3 deputes

```powershell
# Creer fichier de test
$testDeputes = @{
    validated_accounts = @(
        @{ depute_name = "Mathilde Panot"; validated_username = "mathildepanot"; group = "LFI" }
        @{ depute_name = "Gabriel Attal"; validated_username = "gabrielattal"; group = "EPR" }
        @{ depute_name = "Eric Coquerel"; validated_username = "ericcoquerel"; group = "LFI" }
    )
} | ConvertTo-Json -Depth 3

$testDeputes | Out-File -FilePath "data/interim/test_3_deputes.json" -Encoding utf8

# Lancer le test
node scripts/scrape_nitter_search_monthly.js --input data/interim/test_3_deputes.json --max-deputes 3
```

**Duree estimee**: 15-20 minutes (3 deputes x 36 mois x 4s)

### 2.3 Scraping complet

Si le test fonctionne:

```powershell
# Preparer le fichier d'entree depuis la liste propre
$clean = Get-Content "data/interim/deputes_twitter_clean.json" | ConvertFrom-Json
$withTwitter = $clean.deputes | Where-Object { $_.twitter_handle -ne $null }

$input = @{
    validated_accounts = $withTwitter | ForEach-Object {
        @{
            depute_name = $_.depute_name
            validated_username = $_.twitter_handle
            group = $_.group
        }
    }
} | ConvertTo-Json -Depth 3

$input | Out-File -FilePath "data/interim/deputes_to_scrape.json" -Encoding utf8

# Lancer le scraping complet (en arriere-plan)
Start-Process -NoNewWindow node -ArgumentList "scripts/scrape_nitter_search_monthly.js", "--input", "data/interim/deputes_to_scrape.json"
```

**Duree estimee**: 8-10 heures (115 deputes x 36 mois x 4s)

---

## Verification des Resultats

### Compter les tweets collectes

```powershell
# Compter tous les tweets
$folders = Get-ChildItem "data/interim/twitter_monthly" -Directory
$total = 0
foreach ($folder in $folders) {
    $files = Get-ChildItem $folder.FullName -Filter "*.json"
    foreach ($file in $files) {
        $content = Get-Content $file.FullName | ConvertFrom-Json
        if ($content.tweets) { $total += $content.tweets.Count }
    }
}
Write-Host "Total tweets: $total"
```

### Voir la progression

```powershell
Get-Content "data/interim/scraping_progress.json" | ConvertFrom-Json
```

---

## Instances Nitter (Janvier 2026)

| Instance | Status | Temps |
|----------|--------|-------|
| nitter.net | Principale | 2095ms |
| nitter.privacyredirect.com | Backup 1 | 2492ms |
| nitter.tiekoetter.com | Backup 2 | 3550ms |

Verifier l'etat: https://status.d420.de

---

## Structure des Donnees Finales

```
final/data/
├── processed/
│   ├── interventions_enriched.jsonl   # AN: interventions filtrees
│   └── twitter_deputes_final.jsonl    # Twitter: tweets consolides
└── interim/
    ├── deputes_twitter_clean.json     # Mapping deputes <-> Twitter
    └── twitter_monthly/               # Tweets par depute/mois
        ├── mathildepanot/
        │   ├── 2023-01.json
        │   └── ...
        └── ...
```

---

## Troubleshooting

### "Module not found" (Python)
```powershell
pip install -r requirements.txt
```

### "Cannot find module puppeteer" (Node)
```powershell
npm install puppeteer
```

### Scraping bloque
1. Verifier instance Nitter: `curl -I https://nitter.net`
2. Augmenter delai dans CONFIG
3. Changer d'instance

### Pas de tweets trouves
- Verifier que le compte Twitter existe
- Verifier que l'instance fonctionne sur https://status.d420.de

---

## Prochaines Etapes (Analyse)

1. **Consolider** les tweets mensuels en un seul fichier
2. **Filtrer** les tweets mentionnant Gaza/Palestine
3. **Croiser** avec les interventions AN
4. **Analyser** l'evolution temporelle par groupe politique
5. **Visualiser** les resultats








