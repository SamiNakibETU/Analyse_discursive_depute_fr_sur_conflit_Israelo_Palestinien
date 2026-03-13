# Audit final avant cleanup (post-migration)

**Date** : 2025-03-13  
**État** : Audit post-migration — structure finale appliquée

---

## 1. État d'entrée (avant cleanup)

| # | Couche | Dossier | Rôle |
|---|--------|---------|------|
| 1 | Collecte | `final/` | Collecte AN + scraping Twitter (Nitter) |
| 2 | Annotation | `projet_gaza/` | Consolidation, filtrage, annotation LLM v3/v4 |
| 3 | Publication | `fr_assemblee_discourse_analysis/` | prepare_data, analyses complémentaires, exports |
| 4 | Analyse | `analyse_discursive_depute/` | Moteur analytique canonique, run_analysis.py |
| 5 | Web | `index.html`, `scripts/`, `styles/`, `data/` | Dataviz éditoriale |
| 6 | Hors flux | `archive/`, `logs/`, `.claude/`, `.cache` | Archive, debug, cache |

---

## 2. Dépendances critiques identifiées

| Script / config | Référence | Cible |
|----------------|-----------|-------|
| `projet_gaza/consolidate_tweets.py` | `PROJECT_ROOT.parent / "final"` | `pipeline/collection` |
| `projet_gaza/filter_gaza_corpus.py` | `PROJECT_ROOT.parent / "final"` | `pipeline/collection` |
| `projet_gaza/00_data_consolidation.py` | `PROJECT_ROOT.parent / "final"` | `pipeline/collection` |
| `final/merge_twitter_sources.py` | `base_path / "final"` | `pipeline/collection` |
| `fr_assemblee_discourse_analysis/config.py` | `projet_gaza` (sibling) | `pipeline/annotation` |
| `analyse_discursive_depute/config.py` | `fr_assemblee_discourse_analysis` (sibling) | `publication` |
| `index.html` / `scripts/main.js` | `data/*.csv` (relatifs) | Conservés via `site/` |

---

## 3. Chaîne canonique

```
pipeline/collection/     → pipeline/annotation/     → publication/src/prepare_data.py
                              → analysis/scripts/run_analysis.py
                              → site/data/*.csv (dataviz)
```

---

## 4. Imports Python centraux

- **publication/src/config.py** : `SOURCE_DIR` = `pipeline/annotation` (ou `GAZA_SOURCE_PROJECT`)
- **analysis/src/config.py** : `SOURCE_PROJECT` = `publication` (ou `GAZA_SOURCE_PROJECT`)

Variable d'environnement `PROJECT_ROOT` : racine du workspace pour résolution portable.
