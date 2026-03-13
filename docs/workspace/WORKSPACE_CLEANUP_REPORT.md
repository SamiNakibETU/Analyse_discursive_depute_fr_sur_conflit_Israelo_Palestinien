# Rapport de cleanup global du workspace

**Date** : 2025-03-13  
**Objectif** : Structure physique propre, cohérente, maintenable, publiable

---

## I. État initial réel

- `final/`, `projet_gaza/`, `analyse_discursive_depute/`, `fr_assemblee_discourse_analysis/` à la racine
- `index.html`, `scripts/`, `styles/`, `data/` à la racine
- Noms ambigus, chaîne difficile à lire en 30 secondes
- Références codées en dur (final, projet_gaza, fr_assemblee) dans configs et scripts

---

## II. Structure finale réelle

| Couche | Dossier | Rôle |
|--------|---------|------|
| Analyse | `analysis/` | Moteur analytique canonique |
| Publication | `publication/` | prepare_data, exports |
| Pipeline | `pipeline/collection/` | Collecte AN + Twitter |
| Pipeline | `pipeline/annotation/` | Consolidation, annotation |
| Web | `site/` | Dataviz éditoriale |
| Hors flux | `archive/` | Reliquats, debug |
| Racine | `index.html` | Redirection vers site/index.html |

---

## III. Mouvements appliqués

| Action | Détail |
|--------|--------|
| Création | `pipeline/`, `site/` |
| Déplacement | `final/` → `pipeline/collection/` |
| Déplacement | `projet_gaza/` → `pipeline/annotation/` |
| Déplacement | `analyse_discursive_depute/` → `analysis/` |
| Déplacement | `fr_assemblee_discourse_analysis/` → `publication/` |
| Déplacement | `index.html`, `scripts/`, `styles/`, `data/` → `site/` |
| Création | `index.html` racine (redirection) |

---

## IV. Renommages appliqués

- `final` → `pipeline/collection`
- `projet_gaza` → `pipeline/annotation`
- `analyse_discursive_depute` → `analysis`
- `fr_assemblee_discourse_analysis` → `publication`

---

## V. Éléments archivés

- `logs/`, `.claude/`, `.cache/` : déjà dans `.gitignore`, hors flux
- `archive/` : contient les reliquats des migrations précédentes

---

## VI. Documentation finale

- `WORKSPACE_FINAL_AUDIT.md`
- `WORKSPACE_CLEANUP_REPORT.md` (ce fichier)
- `FINAL_STRUCTURE.md`
- `PATH_MIGRATION_MAP.md`
- `CANONICAL_ARTIFACTS.md`
- `PUBLICATION_ALIAS_MAP.md`
- `ARCHIVE_INDEX.md`
- `README.md` (racine mis à jour)

---

## VII. Vérifications

- [x] Imports Python (config.py publication, analysis) patchés
- [x] Chemins consolidate_tweets, filter_gaza_corpus, 00_data_consolidation patchés
- [x] merge_twitter_sources patché (base_path + chemins)
- [x] .gitignore mis à jour (pipeline/collection, pipeline/annotation)
- [x] index.html racine redirige vers site/index.html
- [ ] **À vérifier manuellement** : exécution de prepare_data.py, run_analysis.py, ouverture site/index.html

---

## VIII. Risques restants

1. **fr_assemblee_discourse_analysis** : si sous-module Git, le renommage en `publication/` peut nécessiter une configuration `.gitmodules` ou un lien symbolique.
2. **scripts_scraîng** : typo conservée (î) pour éviter rupture des imports.
3. **Legacy fallback** : analysis/config.py conserve un fallback vers `fr_assemblee_discourse_analysis` si `publication` n'existe pas.

---

## IX. Recommandation d'usage

- **Analyste** : aller dans `analysis/`, lancer `run_analysis.py` (prérequis : corpus dans `publication/data/processed/`).
- **Publication** : aller dans `publication/`, lancer `prepare_data.py` puis scripts d'export.
- **Dataviz** : ouvrir `site/index.html` ou `index.html` (redirection).
- **Pipeline amont** : `pipeline/collection/` pour la collecte, `pipeline/annotation/` pour l'annotation.
