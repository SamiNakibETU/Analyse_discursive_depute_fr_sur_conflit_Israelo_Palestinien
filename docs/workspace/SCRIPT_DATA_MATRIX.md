# Matrice script → données → résultats

| Script | Entrées | Sorties |
|--------|---------|---------|
| `pipeline/collection/scripts_scraîng/merge_twitter_sources.py` | config/twitter_sources/*.txt, pipeline/collection/data/processed/interventions_*.jsonl, pipeline/collection/config/twitter_corrections.json | pipeline/collection/data/interim/deputes_twitter_merged.json |
| `pipeline/annotation/src/preprocessing/consolidate_tweets.py` | pipeline/collection/data/interim/twitter_monthly/*.json | pipeline/annotation/data/consolidated/*.parquet |
| `pipeline/annotation/src/preprocessing/filter_gaza_corpus.py` | pipeline/collection/data/processed/interventions_enriched.jsonl, pipeline/annotation/data/consolidated/*.parquet | pipeline/annotation/data/filtered/*.parquet |
| `publication/src/prepare_data.py` | pipeline/annotation/data/annotated/predictions/*.parquet | publication/data/processed/corpus_v3.parquet, corpus_v4.parquet |
| `analysis/scripts/run_analysis.py` | publication/data/processed/corpus_v3.parquet, corpus_v4.parquet | analysis/data/results/*.csv, analysis/figures/*.png |
| `publication/src/build_analyses_extended.py` | publication/data/* | publication/data/results/*.csv |
| `publication/src/analyses_supplementaires.py` | publication/data/processed/* | publication/reports/figures/*, publication/data/results/twitter_vs_an.csv |
| Export manuel / script | analysis/data/results/*.csv, publication/data/results/*.csv | site/data/*.csv (5 fichiers) |
| `site/index.html` | site/data/*.csv (chargement client) | Dataviz (lecture seule) |
