# Traçabilité de pipeline

Ce document synthétise la chaîne analytique observable dans le workspace entier. Il distingue explicitement :

- `observable` : démontrable dans les fichiers présents ;
- `probable` : cohérent avec les fichiers présents, mais avec un saut de traçabilité ;
- `non démontrable` : non reconstructible avec les éléments disponibles.

## 1. Collecte amont

| Étape | Fichiers principaux | Sorties | Statut |
| --- | --- | --- | --- |
| Collecte AN | `final/src/final_pipeline/pipeline.py`, `final/config/project_settings.json` | `final/data/raw/sessions.jsonl`, `final/data/processed/interventions_relevant.jsonl`, `final/data/processed/interventions_enriched.jsonl` | `observable` |
| Découverte comptes Twitter | `final/scripts_scraîng/build_twitter_deputes_clean.py` | `final/data/interim/deputes_twitter_clean.json` | `observable` |
| Scraping Twitter mensuel | `final/scripts_scraîng/scrape_nitter_search_monthly.js` | `final/data/interim/twitter_monthly/<username>/<YYYY-MM>.json` | `observable` |
| Usage de l'API Twitter v2 | docs historiques dans `fr_assemblee_discourse_analysis/docs/METHODOLOGIE.md` | non visible dans le code du workspace | `non démontrable` |

## 2. Consolidation et filtrage

| Étape | Fichiers principaux | Variables / sorties | Statut |
| --- | --- | --- | --- |
| Consolidation tweets | `projet_gaza/src/preprocessing/consolidate_tweets.py` | `tweets_all.parquet`, normalisation des champs `text`, `date_parsed`, métriques d'engagement | `observable` |
| Filtrage Gaza/Palestine | `projet_gaza/src/preprocessing/filter_gaza_corpus.py`, `projet_gaza/lexicons/filtering_keywords.json` | `tweets_gaza.parquet`, `interventions_gaza.parquet`, `match_type`, `keyword_matches`, `match_confidence` | `observable` |
| Règle de filtrage | 1 terme core ou 2 termes contextuels non exclus | filtrage thématique | `observable` |
| Déduplication fine des tweets proches, quotes, threads | documentation partielle seulement | non visible comme protocole complet et unique | `non démontrable` |

## 3. Annotation

| Étape | Fichiers principaux | Variables / sorties | Statut |
| --- | --- | --- | --- |
| Annotation v3 corpus complet | `projet_gaza/src/annotation/llm_annotation_v3.py` | `stance_v3`, `confidence_v3`, `primary_frame_v3`, `primary_target_v3`, etc. | `observable` |
| Annotation v4 par fenêtres | `projet_gaza/src/annotation/annotation_v4.py` | `stance_v4`, `ceasefire_call`, `conditionality`, `emotional_register`, variables batch-spécifiques | `observable` |
| Température / structured outputs v3 | `temperature=0.05`, `response_format={"type": "json_object"}` | configuration d'annotation | `observable` |
| Validation humaine systématique terminée | scripts présents dans `analyse_discursive_depute/src/validation_humaine.py` et `validation_metrics.py` | protocole présent, mais exécution crédible à confirmer | `probable` |

## 4. Construction des corpus d'analyse

| Étape | Fichiers principaux | Sorties | Statut |
| --- | --- | --- | --- |
| Construction `corpus_v3.parquet` | `fr_assemblee_discourse_analysis/src/prepare_data.py` | fusion tweets + AN, filtres qualité, `text_hash`, `month`, `year` | `observable` |
| Construction `corpus_v4.parquet` | `fr_assemblee_discourse_analysis/src/prepare_data.py` | concaténation des batches v4, harmonisation des colonnes | `observable` |
| Chemin source | `fr_assemblee_discourse_analysis/src/config.py` | `SOURCE_DIR = ROOT.parent / "projet_gaza"` | `observable` |
| Corpus final entièrement régénérable depuis ce repo nettoyé seul | dépend d'un projet source sibling et de fichiers non versionnés | `non démontrable` |

## 5. Analyses et exports

| Étape | Fichiers principaux | Sorties | Statut |
| --- | --- | --- | --- |
| Analyses principales | `analyse_discursive_depute/scripts/run_analysis.py` | la majorité des CSV de `analyse_discursive_depute/data/results/` | `observable` |
| Exports publication complémentaires | `fr_assemblee_discourse_analysis/src/build_analyses_extended.py`, `src/analyses_supplementaires.py` | `twitter_vs_an.csv`, trajectoires, movers, targets, conditionnalité, etc. | `observable` |
| Dataviz racine modulaire | `scripts/main.js`, `data/*.csv` | 5 planches éditoriales alimentées par CSV simplifiés | `observable` |
| Dataviz racine servie par `index.html` | `index.html` | données inline, pas branchées automatiquement aux CSV racine | `observable` |

## 6. Points de rupture de traçabilité

1. Plusieurs CSV présents dans `fr_assemblee_discourse_analysis/data/results/` ne sont pas tous régénérés par un script unique visible dans ce repo.
2. Des noms identiques (`convergence_batch_bloc.csv`, `event_impact_diff_in_diff.csv`, `frames_par_bloc.csv`) existent dans plusieurs sous-projets avec des définitions ou schémas différents.
3. Le dossier racine contient une surface éditoriale qui simplifie ou réencode certains résultats.
4. Des figures sont documentées dans plusieurs README, mais les PNG ne sont pas systématiquement présents dans le workspace.

## 7. Interprétation prudente de la chaîne

- On peut défendre que le workspace contient une chaîne `collecte -> filtrage -> annotation -> corpus -> analyses -> dataviz`.
- On ne peut pas défendre qu'un seul dépôt propre et autoportant permet aujourd'hui de tout régénérer sans dépendances externes ni états intermédiaires manquants.
- Les analyses événementielles visibles sont des comparaisons avant/après par bloc. Elles ne doivent pas être présentées comme des diff-in-diff canoniques sans groupe contrôle.
