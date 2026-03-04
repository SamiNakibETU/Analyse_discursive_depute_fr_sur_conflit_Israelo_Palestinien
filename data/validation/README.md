# Validation humaine

1. **Échantillon** : `python src/validation_humaine.py` → génère `sample_150.csv`
2. **Annotation** : Annoter chaque texte sur l'échelle -2 (favorable à Israël) à +2 (favorable à la Palestine). Ajouter la colonne `stance_humain`.
3. **Métriques** : `python src/validation_metrics.py` → κ (Cohen), ρ (Spearman)
