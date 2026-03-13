# FINAL data pipeline

Ce dossier contient une re-implementation complete des etapes 1 et 2 :

- **etape 1 - Scraping** : collecte de l'ensemble des comptes rendus pertinents (mots-cles Gaza/Israel/Palestine) depuis le 1er janvier 2022, parsing XML officiel et extraction des interventions filtrees.
- **etape 2 - Attribution** : normalisation des noms d'orateurs, rapprochement avec les bases deputes (legislatures 16 et 17) et dictionnaire d'orateurs externes.

## Structure

- config/ : configuration JSON (projet, mots-cles, sources orateurs).
- src/final_pipeline/ : code Python organise en modules (scraping, enrichment, stockage).
- scripts/run_pipeline.py : point d'entree pour executer les deux etapes.
- data/ : dossiers de sortie (raw, interim, processed).

## Dependances

`
python -m venv .venv
.venv\Scripts\activate
pip install -r FINAL/requirements.txt
`

## Execution

`
set PYTHONPATH=FINAL/src
python FINAL/scripts/run_pipeline.py
`

Les fichiers produits :

- data/raw/sessions.jsonl : sessions retenues avec metadonnees de listing.
- data/processed/interventions_relevant.jsonl : interventions filtrees (etape 1).
- data/processed/interventions_enriched.jsonl : interventions enrichies (etape 2).
- data/processed/run_metadata.json : resume de l'execution.

## Notes techniques

- Gestion des erreurs reseau avec retries exponentiels (tenacity + urllib3 Retry).
- Parser XML robuste (lxml) utilisant les namespaces officiels.
- Normalisation/accents geree en ASCII pour une comparaison fiable, fuzzy matching via RapidFuzz.
- Sources orateurs : config/deputes_groupes_17e.json, API nosdeputes.fr, dictionnaire orateurs_exterieurs.json.

