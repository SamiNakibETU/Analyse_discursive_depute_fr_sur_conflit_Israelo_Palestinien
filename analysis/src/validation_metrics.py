# -*- coding: utf-8 -*-
"""
Métriques de validation humaine vs annotation LLM (stance_v3).
Cohen's kappa, Spearman, accord exact/±1, biais par bloc, matrice confusion 5x5.
Produit fig51_validation_matrice_confusion.png et fig52_validation_biais_bloc.png.

Usage: python src/validation_metrics.py
Exige : data/validation/sample_150.csv avec colonne 'stance_humain' (-2 à +2).
Merge avec corpus pour récupérer stance_v3 via text_hash.

# AJOUT TÂCHE A1
"""

from pathlib import Path
import hashlib
import pandas as pd
import numpy as np

import sys
_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir))
ROOT = _script_dir.parent
VAL_DIR = ROOT / "data" / "validation"
PROCESSED_DIR = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "data" / "results"

try:
    from sklearn.metrics import cohen_kappa_score
    from scipy.stats import spearmanr
except ImportError:
    cohen_kappa_score = None
    spearmanr = None


def _build_stance_ref(corpus_v3_path, corpus_v4_path):
    """Construit le DataFrame de reference (text_hash, stance_v3) depuis les corpus."""
    ref = pd.DataFrame()
    for p in [corpus_v3_path, corpus_v4_path]:
        if p is not None and Path(p).exists():
            corp = pd.read_parquet(str(p))
            tc = "text_clean" if "text_clean" in corp.columns else "text"
            corp = corp.copy()
            corp["text_hash"] = corp[tc].apply(
                lambda t: hashlib.sha256(str(t).encode("utf-8", errors="replace")).hexdigest()[:16]
            )
            ref = pd.concat([ref, corp[["text_hash", "stance_v3"]]], ignore_index=True)
    return ref.drop_duplicates(subset=["text_hash"], keep="first") if len(ref) > 0 else ref


def load_annotated_sample(
    sample_path=None,
    annotations_path=None,
    corpus_v3_path=None,
    corpus_v4_path=None,
):
    """
    Charge le sample annoté et merge avec le corpus pour récupérer stance_v3.
    Si stance_humain absent du sample, tente de charger annotations.csv (id, stance_humain).

    Returns:
        (DataFrame, error_message). DataFrame avec stance_humain et stance_v3, ou (None, err).
    """
    sample_path = sample_path or VAL_DIR / "sample_150.csv"
    annotations_path = annotations_path or VAL_DIR / "annotations.csv"
    corpus_v3_path = corpus_v3_path or PROCESSED_DIR / "corpus_v3.parquet"
    corpus_v4_path = corpus_v4_path or PROCESSED_DIR / "corpus_v4.parquet"

    if not sample_path.exists():
        return None, "Fichier absent. Exécuter validation_humaine.py puis annoter les textes."

    df = pd.read_csv(sample_path)
    if "stance_humain" not in df.columns and annotations_path.exists():
        ann = pd.read_csv(annotations_path)
        if "id" in ann.columns and "stance_humain" in ann.columns:
            df = df.merge(ann[["id", "stance_humain"]], on="id", how="left")
    if "stance_humain" not in df.columns:
        return None, (
            "Ajouter la colonne 'stance_humain' (-2 a +2) dans sample_150.csv ou creer "
            "data/validation/annotations.csv avec colonnes id et stance_humain."
        )

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    if "text" not in df.columns and text_col in df.columns:
        df = df.rename(columns={text_col: "text"})

    if "text_hash" not in df.columns:
        df["text_hash"] = df["text"].apply(
            lambda t: hashlib.sha256(str(t).encode("utf-8", errors="replace")).hexdigest()[:16]
        )

    ref = _build_stance_ref(corpus_v3_path, corpus_v4_path)

    merge_cols = ["text_hash", "stance_v3"]
    if len(ref) == 0:
        return None, "Corpus vide ou inaccessible."
    ref_sub = ref[merge_cols].drop_duplicates(subset=["text_hash"])
    df_merged = df.merge(ref_sub, on="text_hash", how="left")

    valid = df_merged[df_merged["stance_humain"].notna()].copy()
    valid["stance_humain"] = valid["stance_humain"].astype(int)
    valid = valid[valid["stance_humain"].between(-2, 2)]

    if len(valid) == 0:
        return None, "Aucune annotation valide (stance_humain -2 a +2)."

    if valid["stance_v3"].isna().all():
        sample_hashes = set(df["text_hash"].astype(str))
        ref_hashes = set(ref["text_hash"].astype(str))
        overlap_set = sample_hashes & ref_hashes
        return None, (
            f"stance_v3 absent apres merge. Overlap text_hash: {len(overlap_set)}/{len(sample_hashes)}. "
            "Verifier coherence text_hash sample/corpus."
        )

    return valid, None


def compute_metrics(df):
    """
    Calcule Cohen kappa, Spearman, accord exact, accord ±1, biais par bloc.
    df doit avoir stance_humain et stance_v3.
    """
    valid = df[df["stance_humain"].notna() & df["stance_v3"].notna()].copy()
    valid["stance_humain"] = valid["stance_humain"].astype(int)
    valid["stance_v3"] = valid["stance_v3"].astype(int)
    human = valid["stance_humain"]
    llm = valid["stance_v3"]

    results = {}
    if cohen_kappa_score is not None:
        results["kappa"] = cohen_kappa_score(human, llm)
    if spearmanr is not None:
        rho, p = spearmanr(human, llm)
        results["spearman_rho"] = rho
        results["spearman_p"] = p

    results["accord_exact"] = (human == llm).mean() * 100
    results["accord_pm1"] = ((human - llm).abs() <= 1).mean() * 100

    bias_by_bloc = {}
    if "bloc" in valid.columns:
        for bloc in valid["bloc"].dropna().unique():
            sub = valid[valid["bloc"] == bloc]
            if len(sub) >= 2:
                bias_by_bloc[bloc] = (sub["stance_v3"].astype(float) - sub["stance_humain"].astype(float)).mean()
    results["bias_by_bloc"] = bias_by_bloc

    results["confusion"] = pd.crosstab(
        valid["stance_humain"],
        valid["stance_v3"],
        rownames=["humain"],
        colnames=["LLM"],
    )
    return results


def plot_figures(results, figures_dir=None):
    """Produit fig51 (matrice confusion) et fig52 (biais par bloc)."""
    import matplotlib.pyplot as plt
    import seaborn as sns

    figures_dir = figures_dir or ROOT / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    from config import BLOC_ORDER, BLOC_COLORS

    if "confusion" in results and results["confusion"].size > 0:
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(
            results["confusion"],
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax,
        )
        ax.set_xlabel("Positionnement LLM (stance_v3)")
        ax.set_ylabel("Positionnement humain")
        ax.set_title("Matrice de confusion : humain vs LLM")
        p = figures_dir / "fig51_validation_matrice_confusion.png"
        plt.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close()
        print(f"Figure sauvegardee : {p}")

    if results.get("bias_by_bloc"):
        fig, ax = plt.subplots(figsize=(8, 5))
        blocs = [b for b in BLOC_ORDER if b in results["bias_by_bloc"]]
        biases = [results["bias_by_bloc"][b] for b in blocs]
        colors = [BLOC_COLORS.get(b, "#888") for b in blocs]
        x = range(len(blocs))
        ax.bar(x, biases, color=colors)
        ax.axhline(0, color="grey", ls="--", lw=1)
        ax.set_xticks(x)
        ax.set_xticklabels([b.replace(" / ", "\n") for b in blocs], rotation=0, ha="center")
        ax.set_ylabel("Biais (mean(LLM - humain))")
        ax.set_title("Biais systematique LLM par bloc")
        p = figures_dir / "fig52_validation_biais_bloc.png"
        plt.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close()
        print(f"Figure sauvegardee : {p}")


def write_report(results, report_path=None):
    """Ecrit un rapport texte des métriques."""
    report_path = report_path or ROOT / "data" / "results" / "RAPPORT_VALIDATION_HUMAINE.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "=" * 60,
        "RAPPORT VALIDATION HUMAINE vs LLM",
        "=" * 60,
    ]
    if "kappa" in results:
        lines.append(f"Cohen's Kappa : {results['kappa']:.3f}")
        lines.append("  (>= 0.4 : accord modere ; >= 0.6 : bon accord)")
    if "spearman_rho" in results:
        lines.append(f"Spearman rho : {results['spearman_rho']:.3f} (p = {results.get('spearman_p', 'N/A')})")
    lines.append(f"Accord exact : {results.get('accord_exact', 0):.1f} %")
    lines.append(f"Accord a +/-1 point : {results.get('accord_pm1', 0):.1f} %")
    if results.get("bias_by_bloc"):
        lines.append("\nBiais par bloc (mean(LLM - humain)) :")
        for bloc, b in results["bias_by_bloc"].items():
            lines.append(f"  {bloc} : {b:.3f}")
    if "confusion" in results and results["confusion"].size > 0:
        lines.append("\nMatrice de confusion (lignes=humain, colonnes=LLM) :")
        lines.append(results["confusion"].to_string())
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Rapport ecrit : {report_path}")


def main():
    df, err = load_annotated_sample()
    if err:
        print(err)
        print(
            "\nPour annoter : ajouter la colonne 'stance_humain' (-2 a +2) dans sample_150.csv, "
            "ou creer annotations.csv avec colonnes id et stance_humain puis merger."
        )
        return

    results = compute_metrics(df)

    print("\n--- Metriques de validation ---")
    if "kappa" in results:
        print(f"Cohen kappa = {results['kappa']:.3f}")
    if "spearman_rho" in results:
        print(f"Spearman rho = {results['spearman_rho']:.3f} (p = {results.get('spearman_p'):.4f})")
    print(f"Accord exact = {results.get('accord_exact', 0):.1f} %")
    print(f"Accord a +/-1 = {results.get('accord_pm1', 0):.1f} %")
    if results.get("bias_by_bloc"):
        print("Biais par bloc:")
        for bloc, b in results["bias_by_bloc"].items():
            print(f"  {bloc}: {b:.3f}")

    plot_figures(results)
    write_report(results)


if __name__ == "__main__":
    main()
