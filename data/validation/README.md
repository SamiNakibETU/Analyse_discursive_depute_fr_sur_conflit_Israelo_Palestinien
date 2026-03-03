# Validation humaine

1. **Échantillon** : `python src/validation_humaine.py` → génère `sample_150.csv`
2. **Annotation** : Annoter chaque texte sur l'échelle -2 (pro-Israël) à +2 (pro-Palestine). Ajouter la colonne `stance_humain`.
3. **Métriques** : `python src/validation_metrics.py` → κ (Cohen), ρ (Spearman)
