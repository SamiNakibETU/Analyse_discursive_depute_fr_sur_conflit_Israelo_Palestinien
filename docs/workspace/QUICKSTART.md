# Guide de démarrage

**Temps de lecture : 30 secondes**

## Structure du workspace

| Dossier | Rôle |
|---------|------|
| `site/` | **Dataviz éditoriale** — ouvrir `site/index.html` |
| `analysis/` | **Moteur analytique canonique** — run_analysis.py, notebooks |
| `publication/` | **Couche publication** — prepare_data, exports, COMPTE_RENDU |
| `pipeline/collection/` | **Collecte** — AN + scraping Twitter |
| `pipeline/annotation/` | **Consolidation et annotation** — corpus v3/v4 |
| `archive/` | Hors flux principal |
| `docs/` | Documentation, traçabilité, design |

## Chaîne canonique

```
pipeline/collection/ → pipeline/annotation/ → publication/prepare_data
    → analysis/run_analysis → site/data/*.csv (dataviz)
```

## Démarrage rapide

1. **Voir la dataviz** : ouvrir `site/index.html` (ou `index.html` racine qui redirige)
2. **Consulter les résultats** : `analysis/data/results/`, `publication/docs/COMPTE_RENDU_RESULTATS.md`
3. **Relancer l’analyse** : `python analysis/scripts/run_analysis.py` (prérequis : corpus v3/v4 dans `publication/data/processed/`)

## Variable d’environnement optionnelle

- `PROJECT_ROOT` : racine du workspace (pour résolution portable des chemins)
- `GAZA_SOURCE_PROJECT` : override du projet source (par défaut `pipeline/annotation`)
