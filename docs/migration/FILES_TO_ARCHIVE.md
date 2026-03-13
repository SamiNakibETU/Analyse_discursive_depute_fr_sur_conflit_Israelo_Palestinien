# Files And Folders To Archive (Proposed)

## Regle appliquee

Rien n'est supprime. Tout element non canonique doit etre deplace vers `archive/` en conservant l'historique et en reecrivant les liens references.

## A archiver en priorite (risque faible)

| Chemin | Motif | Usage verifie | Action |
| --- | --- | --- | --- |
| `archive/legacy_workspaces/_archive/` | ancien contenu historise | references docs seulement | deplacement termine |
| `archive/pocs/nitter-scraper-basics/` | POC scraping isole | aucun import Python detecte | deplacement termine |
| `.cache/` | cache de scraping et HTML intermediaires | scripts `.cache/deputes/*.js` seulement | conserver hors git ou archiver en `archive/debug_logs/cache_snapshot/` |
| `final/logs/` | logs iteratifs HTML | pas de dependance runtime detectee | archiver en `archive/debug_logs/final_logs/` |

## A archiver en seconde vague (verification supplementaire requise)

| Chemin | Motif | Blocage |
| --- | --- | --- |
| `analyse_discursive_depute/DATA_VIZ_Article/archive/` | versions de dataviz legacy | verifier references dans docs dataviz et scripts de build |
| `twitter_account_député.md`, `deputé_2023_tweeter.html`, `twitter_account_deputé.html` | artefacts ponctuels de collecte | verifier s'ils servent encore de source manuelle |
| fichiers de test ad hoc dans `projet_gaza/` (`test_api_direct.py`, `test_new_script.py`, `test_gpt5nano.py`) | scripts exploratoires | garder si encore utilises pour recalibrage API |

## A NE PAS archiver (canoniques)

- `final/src/final_pipeline/*`, `final/scripts_scraîng/*` (collecte amont)
- `projet_gaza/src/*` (filtrage/annotation)
- `analyse_discursive_depute/src/*`, `analyse_discursive_depute/scripts/run_analysis.py`
- `fr_assemblee_discourse_analysis/src/*` (publication et exports etendus)
- `index.html`, `scripts/`, `styles/`, `data/*.csv` (site editorial actif)
