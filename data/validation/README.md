# Validation humaine

1. Générer l'échantillon : `python src/validation_humaine.py` → `sample.csv`
2. Annoter chaque texte sur l'échelle -2 (pro-Israël) à +2 (pro-Palestine)
3. Créer `annotations.csv` avec colonnes : `id`, `human_stance`
4. Calculer les métriques : `python src/validation_metrics.py`
