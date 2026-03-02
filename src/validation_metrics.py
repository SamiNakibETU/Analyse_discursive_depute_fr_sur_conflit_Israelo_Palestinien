# -*- coding: utf-8 -*-
"""
Métriques de validation humaine vs annotation LLM.

Fichiers attendus :
  - data/validation/sample.csv (généré par validation_humaine.py)
  - data/validation/annotations.csv (colonnes : id, human_stance)

Usage :
  python src/validation_metrics.py

Affiche Cohen's kappa (accord catégoriel) et Spearman (corrélation ordinale).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

VALIDATION_DIR = Path(__file__).resolve().parent.parent / "data" / "validation"


def main():
    import pandas as pd
    from sklearn.metrics import cohen_kappa_score
    from scipy.stats import spearmanr

    sample_path = VALIDATION_DIR / "sample.csv"
    annot_path = VALIDATION_DIR / "annotations.csv"

    if not sample_path.exists():
        print("Exécuter d'abord : python src/validation_humaine.py")
        return
    if not annot_path.exists():
        print(
            f"Créer {annot_path} avec colonnes : id, human_stance (-2 à +2)\n"
            "Après avoir annoté manuellement les textes de sample.csv"
        )
        return

    sample = pd.read_csv(sample_path)
    annot = pd.read_csv(annot_path)
    merged = sample.merge(annot, on="id", how="inner")

    # Charger les scores LLM depuis le corpus
    from config import CORPUS_V3, BLOC_ORDER

    df = pd.read_parquet(CORPUS_V3)
    df = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df["_idx"] = range(len(df))
    llm_map = df.set_index("_idx")["stance_v3"].to_dict()

    merged["llm_stance"] = merged["id"].map(llm_map)
    merged = merged.dropna(subset=["human_stance", "llm_stance"])

    if len(merged) < 10:
        print(f"Trop peu de paires valides : {len(merged)}")
        return

    human = merged["human_stance"].astype(int)
    llm = merged["llm_stance"].round().astype(int).clip(-2, 2)

    kappa = cohen_kappa_score(human, llm)
    rho, pval = spearmanr(merged["human_stance"], merged["llm_stance"])

    print(f"Cohen's κ = {kappa:.3f}")
    print(f"Spearman ρ = {rho:.3f} (p = {pval:.4f})")
    print(f"N = {len(merged)} paires annotées")


if __name__ == "__main__":
    main()
