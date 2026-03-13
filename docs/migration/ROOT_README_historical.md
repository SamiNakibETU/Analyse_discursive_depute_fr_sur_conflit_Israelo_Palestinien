# Revirement politique francais sur le conflit israelo-palestinien

Workspace de recherche et de publication sur les prises de position de deputes francais (tweets + Assemblee nationale), periode 2023-2026.

## Objectif du repo

Ce workspace contient quatre couches complementaires:

- collecte amont (`final/`);
- consolidation/annotation (`projet_gaza/`);
- analyse discursive principale (`analyse_discursive_depute/`);
- couche publication-ready (`fr_assemblee_discourse_analysis/`);
- dataviz editoriale web (`index.html`, `scripts/`, `styles/`, `data/`).

## Etat actuel

- La chaine est fonctionnelle mais distribuee sur plusieurs sous-projets.
- Les dependances entre dossiers sont reelles (pas seulement documentaires).
- Une migration structurelle est planifiee de facon sure dans:
  - `MIGRATION_PLAN.md`
  - `REPO_STRUCTURE_PROPOSED.md`
  - `FILES_TO_ARCHIVE.md`
  - `PATHS_TO_UPDATE.md`

## Points d'entree techniques

- Collecte: `final/scripts_scraîng/` et `final/src/final_pipeline/`
- Annotation: `projet_gaza/src/annotation/`
- Preparation corpus publication: `fr_assemblee_discourse_analysis/src/prepare_data.py`
- Analyse principale: `analyse_discursive_depute/scripts/run_analysis.py`
- Site editorial: `index.html` + `scripts/main.js`

## Reproduction minimale (etat courant)

1. Executer la collecte et la consolidation (`final/` puis `projet_gaza/`).
2. Generer `corpus_v3.parquet` et `corpus_v4.parquet`.
3. Lancer `analyse_discursive_depute/scripts/run_analysis.py`.
4. Generer les exports publication complets si besoin via `fr_assemblee_discourse_analysis/src/build_analyses_extended.py`.

## Important

- Ne pas deplacer de dossiers sans reecriture des chemins dans `config.py`, notebooks et docs.
- Ne pas supprimer de donnees: archiver d'abord.
