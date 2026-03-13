# Paths To Update Before Structural Moves

## Chemins Python critiques

| Fichier | Chemin actuel | Risque | Reecriture cible (proposee) |
| --- | --- | --- | --- |
| `analyse_discursive_depute/src/config.py` | `ROOT.parent / "fr_assemblee_discourse_analysis"` | rupture si fusion/relocalisation | utiliser variable env `GAZA_SOURCE_PROJECT` obligatoire + fallback configurable |
| `fr_assemblee_discourse_analysis/src/config.py` | `ROOT.parent / "projet_gaza"` | couplage fort entre dossiers siblings | introduire `GAZA_SOURCE_PROJECT`/`SOURCE_DIR` dans `.env.example` |
| `projet_gaza/src/preprocessing/consolidate_tweets.py` | `PROJECT_ROOT.parent / "final" / "data" / "interim"` | casse si `final/` deplace | passer par config centralisee `PIPELINE_SOURCE_FINAL_DATA` |
| scripts `final/scripts_scraîng/*.py` | imports `final_pipeline` via `PYTHONPATH=src` | fragile en CI | packager `final_pipeline` et appels `python -m` |

## Notebooks

| Pattern | Chemin actuel | Action |
| --- | --- | --- |
| `analyse_discursive_depute/notebooks/*.ipynb` | `Path("../data/results")` | migrer vers helper `PROJECT_ROOT` ou `%cd` documente |
| notebooks publication | references cwd implicites | ajouter cellule unique `ROOT = Path(...).resolve()` |

## Couche web

| Fichier | Chemins actuels | Action |
| --- | --- | --- |
| `scripts/main.js` | `data/frames_par_bloc.csv`, etc. | conserver structure `site/data/` ou injecter chemin base configurable |
| `index.html` inline dataset | donnees en dur dans script | documenter la source de verite et automatiser export CSV->JS si necessaire |

## Documentation / commandes

| Fichier | Chemin hardcode | Action |
| --- | --- | --- |
| `fr_assemblee_discourse_analysis/docs/PUSH_GIT.md` | chemin absolu Windows | remplacer par chemins relatifs portables |
| `fr_assemblee_discourse_analysis/docs/PUBLICATION_CHECKLIST.md` | chemin absolu Windows | idem |
| `final/GUIDE_EXECUTION.md` | commandes avec `cd D:\...` | ajouter variantes relatives et bash |

## Configurations de dependances

| Fichier | Situation | Action |
| --- | --- | --- |
| racine `requirements.txt` vs sous-projets `requirements.txt` | duplication non harmonisee | definir un mode: mono-env ou env par sous-projet |
| deux `pyproject.toml` (`analyse_discursive_depute`, `fr_assemblee_discourse_analysis`) | metadata concurrentes | choisir package canonique et retrocompatibilite |
