# Validation humaine

1. **Générer l'échantillon** : `python src/validation_humaine_sample.py`
   → Crée `validation_humaine_sample.csv` (150 textes, colonnes : id, text, bloc)

2. **Annoter** : Ajouter une colonne `stance_human` (-2 à +2) à la main.
   Sauvegarder sous `validation_humaine_annotated.csv`.

3. **Calculer les métriques** : `python src/validation_metrics.py`
   → Affiche κ (Cohen), ρ (Spearman), matrice de confusion humain vs LLM.
