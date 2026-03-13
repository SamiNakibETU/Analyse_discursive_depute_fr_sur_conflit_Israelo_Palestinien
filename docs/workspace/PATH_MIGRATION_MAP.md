# Table de migration des chemins

**Post-cleanup** — ancien chemin → nouveau chemin

---

## Dossiers

| Ancien chemin | Nouveau chemin |
|---------------|----------------|
| `final/` | `pipeline/collection/` |
| `projet_gaza/` | `pipeline/annotation/` |
| `analyse_discursive_depute/` | `analysis/` |
| `fr_assemblee_discourse_analysis/` | `publication/` |
| `index.html` (racine) | `site/index.html` |
| `scripts/` (racine) | `site/scripts/` |
| `styles/` (racine) | `site/styles/` |
| `data/` (racine, dataviz) | `site/data/` |

---

## Entrée dataviz

| Ancien | Nouveau |
|--------|---------|
| Ouvrir `index.html` à la racine | Ouvrir `site/index.html` ou `index.html` (redirection) |

---

## Références patchées

| Fichier | Modification |
|---------|--------------|
| `pipeline/annotation/src/preprocessing/consolidate_tweets.py` | `"final"` → `"pipeline" / "collection"` |
| `pipeline/annotation/src/preprocessing/filter_gaza_corpus.py` | `"final"` → `"pipeline" / "collection"` |
| `pipeline/annotation/notebooks/00_data_consolidation.py` | `"final"` → `"pipeline" / "collection"` |
| `pipeline/collection/scripts_scraîng/merge_twitter_sources.py` | `base_path` 4 niveaux + `"final"` → `"pipeline" / "collection"` |
| `publication/src/config.py` | `"projet_gaza"` → `"pipeline" / "annotation"` |
| `analysis/src/config.py` | `"fr_assemblee_discourse_analysis"` → `"publication"` |
