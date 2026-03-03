# -*- coding: utf-8 -*-
"""
Métriques de validation humaine vs LLM.
Cohen's kappa (accord nominal), Spearman (corrélation continue).
Exige : data/validation/sample_150.csv annoté avec colonne 'stance_humain' (-2 à +2).

Usage: python src/validation_metrics.py
"""

from pathlib import Path
import pandas as pd
import numpy as np

try:
    from sklearn.metrics import cohen_kappa_score
    from scipy.stats import spearmanr
except ImportError:
    cohen_kappa_score = None
    spearmanr = None


def main():
    val_dir = Path(__file__).resolve().parent.parent / "data" / "validation"
    sample_path = val_dir / "sample_150.csv"

    if not sample_path.exists():
        print("Fichier absent. Exécuter validation_humaine.py puis annoter les textes.")
        return

    df = pd.read_csv(sample_path)
    if "stance_humain" not in df.columns:
        print("Ajouter la colonne 'stance_humain' (-2 à +2) après annotation.")
        return

    llm_col = "stance_v3" if "stance_v3" in df.columns else "stance"
    if llm_col not in df.columns:
        print("Recharger le sample avec les colonnes LLM (merge avec corpus).")
        return

    human = df["stance_humain"].dropna().astype(int)
    llm = df.loc[human.index, llm_col]

    if cohen_kappa_score and spearmanr:
        kappa = cohen_kappa_score(human, llm)
        rho, p = spearmanr(human, llm)
        print(f"Cohen κ = {kappa:.3f}")
        print(f"Spearman ρ = {rho:.3f} (p = {p:.4f})")
        print("→ κ ≥ 0,4 : accord modéré ; κ ≥ 0,6 : bon accord")
    else:
        print("Installer scikit-learn et scipy : pip install scikit-learn scipy")


if __name__ == "__main__":
    main()
