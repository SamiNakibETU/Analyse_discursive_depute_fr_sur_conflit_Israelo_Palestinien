# Manifeste des artefacts canoniques

Post-cleanup — structure finale appliquée.

---

## 1. Scripts canoniques

| Script | Emplacement | Entrées | Sorties |
|--------|-------------|---------|---------|
| `prepare_data.py` | `publication/src/` | pipeline/annotation outputs (parquet) | corpus_v3.parquet, corpus_v4.parquet |
| `run_analysis.py` | `analysis/scripts/` | corpus_v3/v4, lexiques | CSV results/, figures/, RAPPORT_RESULTATS.txt, RESULTATS_NUMERIQUES.md |
| `build_analyses_extended.py` | `publication/src/` | corpus, results | trajectoires, movers, coherence, targets |
| `analyses_supplementaires.py` | `publication/src/` | corpus | fig21–25, twitter_vs_an.csv |

---

## 2. Tables CSV canoniques (analysis)

- `analysis/data/results/` — CSV produits par run_analysis
- `publication/data/results/` — exports publication

## 3. Tables CSV couche web (site/data)

Les CSV dans `site/data/` alimentent la dataviz éditoriale :
- frames_par_bloc.csv
- vue_ensemble.csv
- stance_mensuel.csv
- event_impact_diff_in_diff.csv
- emotional_register.csv

## 4. Figures canoniques

- `analysis/figures/` — figures générées par run_analysis (fig01–fig76)
- `publication/reports/figures/` — figures publication

---

## 5. Chaîne canonique

```
pipeline/collection/     → pipeline/annotation/
    → publication/src/prepare_data.py
        → analysis/scripts/run_analysis.py
            → site/data/*.csv (export/copie)
                → site/index.html (dataviz)
```

## 6. Points d'entrée

1. **Dataviz** : ouvrir `site/index.html` (ou `index.html` racine, redirection)
2. **Lancer l'analyse** : `analysis/scripts/run_analysis.py` (prérequis : corpus_v3/v4)
3. **Consulter les résultats** : `analysis/data/results/`, `publication/docs/COMPTE_RENDU_RESULTATS.md`
