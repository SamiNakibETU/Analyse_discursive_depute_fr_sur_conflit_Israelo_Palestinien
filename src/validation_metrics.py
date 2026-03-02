# -*- coding: utf-8 -*-
"""
Métriques de validation humaine vs LLM.
Cohen's kappa (accord catégoriel), Spearman (corrélation ordinale).

Usage : python src/validation_metrics.py
Input : data/validation/validation_humaine_annotated.csv (id, text, bloc, stance_human)
        data/validation/validation_humaine_llm_ref.csv (id, stance_v3) — généré par validation_humaine_sample.py
"""

from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score, confusion_matrix

VALIDATION_DIR = Path(__file__).resolve().parent.parent / "data" / "validation"


def main():
    annotated_path = VALIDATION_DIR / "validation_humaine_annotated.csv"
    ref_path = VALIDATION_DIR / "validation_humaine_llm_ref.csv"

    if not annotated_path.exists():
        print(f"Fichier manquant : {annotated_path}")
        print("Copier validation_humaine_sample.csv vers validation_humaine_annotated.csv, ajouter colonne stance_human (-2 à +2)")
        return

    if not ref_path.exists():
        print(f"Fichier manquant : {ref_path}")
        print("Exécuter d'abord : python src/validation_humaine_sample.py")
        return

    df = pd.read_csv(annotated_path)
    ref = pd.read_csv(ref_path)

    if "stance_human" not in df.columns:
        print("Colonne 'stance_human' manquante (score -2 à +2 annoté à la main)")
        return

    df = df.merge(ref[["id", "stance_v3"]], on="id", how="left")
    valid = df[["stance_human", "stance_v3"]].dropna()
    if len(valid) < 5:
        print("Trop peu de paires annotées pour calculer les métriques.")
        return

    human = valid["stance_human"].astype(int)
    llm = valid["stance_v3"].round().astype(int)

    kappa = cohen_kappa_score(human, llm)
    rho, p_spear = spearmanr(valid["stance_human"], valid["stance_v3"])
    cm = confusion_matrix(human, llm)

    print("=== Validation humaine vs LLM ===\n")
    print(f"Cohen's κ = {kappa:.3f} (accord modéré si κ > 0.4)")
    print(f"Spearman ρ = {rho:.3f} (p = {p_spear:.4f})")
    print("\nMatrice de confusion (humain × LLM) :")
    print(pd.DataFrame(cm, index=[f"H{i}" for i in range(-2, 3)], columns=[f"L{i}" for i in range(-2, 3)]).to_string())


if __name__ == "__main__":
    main()
