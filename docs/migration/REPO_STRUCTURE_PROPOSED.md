# Structure GitHub Proposee (Dependance-First)

## Principe

Cette structure est proposee apres audit des dependances observees dans `final/`, `projet_gaza/`, `analyse_discursive_depute/`, `fr_assemblee_discourse_analysis/` et la couche web racine (`index.html`, `scripts/`, `data/`).

Le coeur analytique recommande est `analyse_discursive_depute/` (voir comparaison dans `MIGRATION_PLAN.md`), avec une couche publication (`fr_assemblee_discourse_analysis/`) et une couche web (`site/`) conservees.

## Arborescence cible

```text
revirement-politique-fr-gaza/
├── README.md
├── ROOT_README.md
├── requirements.txt
├── pyproject.toml                     # a normaliser dans lot suivant
├── .gitignore
├── docs/
│   ├── METHODOLOGIE.md
│   ├── COMPTE_RENDU_RESULTATS.md
│   ├── PIPELINE_TRACEABILITY.md
│   ├── FIGURE_TRACEABILITY_MATRIX.md
│   └── migration/
│       ├── MIGRATION_PLAN.md
│       ├── REPO_STRUCTURE_PROPOSED.md
│       ├── FILES_TO_ARCHIVE.md
│       └── PATHS_TO_UPDATE.md
├── pipeline/
│   ├── collect/                       # derive de final/src/final_pipeline + scripts_scraing
│   ├── annotation/                    # derive de projet_gaza/src/annotation + scripts
│   ├── preprocessing/                 # derive de projet_gaza/src/preprocessing
│   └── analysis/                      # derive de analyse_discursive_depute/src + scripts
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── results/
├── notebooks/
│   ├── analysis/                      # notebooks canoniques
│   └── publication/
├── figures/
├── reports/
├── site/                              # actuel index.html + scripts/ + styles/ + data_viz/
│   ├── index.html
│   ├── scripts/
│   ├── styles/
│   └── data/
├── publication/                       # derive de fr_assemblee_discourse_analysis
│   ├── docs/
│   ├── reports/
│   └── notebooks/
├── tests/
└── archive/
    ├── legacy_workspaces/
    ├── pocs/
    ├── debug_logs/
    └── foreign_projects/
```

## Ce qui reste dans le repo principal

- `final/` (collecte), `projet_gaza/` (annotation), `analyse_discursive_depute/` (analyse), `fr_assemblee_discourse_analysis/` (publication) tant que les deplacements ne sont pas executes par lots verifies.
- `index.html`, `scripts/`, `styles/`, `data/` (site editorial actuel).

## Ce qui devrait aller en archive

- `archive/legacy_workspaces/_archive/` (archive historique).
- `archive/pocs/nitter-scraper-basics/` (POC).
- `analyse_discursive_depute/DATA_VIZ_Article/archive/` (anciens essais).
- `final/logs/*.html` et artefacts de debug anciens (apres verification qu'ils ne sont pas requis pour reproduction).

## Ce qui devrait etre ignore par git

- caches et outputs regenerables: `.cache/`, `__pycache__/`, `*.pyc`, notebooks checkpoints.
- gros artefacts de donnees: `data/raw/`, `data/interim/`, `data/processed/*.parquet`, logs JSONL/HTML massifs.
- environnements et secrets: `.venv/`, `.env`, fichiers de credentials.

## Sous-module / repo separe (recommandation)

- Option 1 (preferee): garder monorepo avec separation claire `pipeline/`, `publication/`, `site/`.
- Option 2: extraire `site/` en repo separe si publication web devient independante du pipeline.
- Option 3: extraire `final/` scraping en package reutilisable uniquement si API stable et tests dedies.

## Risques de rupture identifies

- chemins `ROOT.parent / "projet_gaza"` et `ROOT.parent / "fr_assemblee_discourse_analysis"` dans configs Python;
- notebooks relies a `../data/results` et a des conventions de cwd;
- scripts web qui chargent `data/*.csv` en relatif;
- scripts `final/` dependant de `PYTHONPATH=src`;
- references documentaires hardcodees vers l'arborescence actuelle.
