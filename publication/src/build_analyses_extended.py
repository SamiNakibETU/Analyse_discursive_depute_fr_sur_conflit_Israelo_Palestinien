# -*- coding: utf-8 -*-
"""
Génère les analyses étendues (niveau individu, cohérence, target, key_demands, etc.)
depuis corpus_v3.parquet et corpus_v4.parquet.

Usage : python src/build_analyses_extended.py
Prérequis : make data
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    PROJECT_ROOT, DATA_DIR, PROCESSED_DIR, RESULTS_DIR,
    COLORS, BLOC_ORDER, BATCH_ORDER, BATCHES,
)

CORPUS_V3 = PROCESSED_DIR / "corpus_v3.parquet"
CORPUS_V4 = PROCESSED_DIR / "corpus_v4.parquet"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def assign_batch(d, batches):
    if pd.isna(d):
        return "OTHER"
    for name, cfg in batches.items():
        start = pd.Timestamp(cfg["start"])
        end = pd.Timestamp(cfg["end"])
        if start <= d <= end:
            return name
    return "OTHER"


def flatten_key_demands(x):
    """key_demands peut être liste, string ou array."""
    if x is None:
        return []
    if isinstance(x, np.ndarray):
        if x.size == 0:
            return []
        return [str(i) for i in x.ravel()]
    try:
        if pd.isna(x):
            return []
    except (ValueError, TypeError):
        pass
    if isinstance(x, list):
        return [str(i) for i in x]
    if isinstance(x, str):
        return [x] if x else []
    return []


def main():
    if not CORPUS_V3.exists():
        print(f"Corpus v3 absent : {CORPUS_V3}")
        return

    v3 = pd.read_parquet(CORPUS_V3)
    v3["date"] = pd.to_datetime(v3["date"])
    v3["month"] = v3["date"].dt.to_period("M")
    v3["group"] = v3.get("group", v3.get("groupe_politique", ""))

    has_v4 = CORPUS_V4.exists()
    if has_v4:
        v4 = pd.read_parquet(CORPUS_V4)
        v4["date"] = pd.to_datetime(v4["date"])
        v4["month"] = v4["date"].dt.to_period("M")
        v4["batch"] = v4["date"].apply(lambda d: assign_batch(d, BATCHES))

    # -------------------------------------------------------------------------
    # 1. TRAJECTOIRES INDIVIDUELLES : stance par député, variance, movers
    # -------------------------------------------------------------------------
    dep_profile = (
        v3.groupby(["author", "bloc", "group"])
        .agg(
            stance_mean=("stance_v3", "mean"),
            stance_std=("stance_v3", "std"),
            stance_min=("stance_v3", "min"),
            stance_max=("stance_v3", "max"),
            n_textes=("stance_v3", "count"),
            n_months=("month", "nunique"),
            first_month=("date", "min"),
            last_month=("date", "max"),
        )
        .reset_index()
    )
    dep_profile["stance_range"] = dep_profile["stance_max"] - dep_profile["stance_min"]
    dep_profile["is_mover"] = dep_profile["stance_range"] >= 2  # au moins 2 points d'écart
    dep_profile.to_csv(RESULTS_DIR / "trajectoires_individuelles.csv", index=False)
    print("  -> trajectoires_individuelles.csv")

    # Variance intra-bloc
    variance_intra = (
        dep_profile.groupby("bloc")
        .agg(
            n_deputes=("author", "count"),
            stance_mean_global=("stance_mean", "mean"),
            stance_std_global=("stance_std", "mean"),
            pct_movers=("is_mover", "mean"),
        )
        .reset_index()
    )
    variance_intra.to_csv(RESULTS_DIR / "variance_intra_bloc.csv", index=False)
    print("  -> variance_intra_bloc.csv")

    # Top movers par bloc (n >= 10 textes)
    movers = dep_profile[dep_profile["n_textes"] >= 10].nlargest(20, "stance_range")[
        ["author", "bloc", "group", "stance_mean", "stance_range", "n_textes", "n_months"]
    ]
    movers.to_csv(RESULTS_DIR / "movers_top20.csv", index=False)
    print("  -> movers_top20.csv")

    # -------------------------------------------------------------------------
    # 2. COHÉRENCE TWITTER vs AN par député (même député, deux arènes)
    # -------------------------------------------------------------------------
    dep_arena = (
        v3.groupby(["author", "bloc", "arena"])
        .agg(stance_mean=("stance_v3", "mean"), n=("stance_v3", "count"))
        .reset_index()
    )
    pivot_arena = dep_arena.pivot_table(
        index=["author", "bloc"], columns="arena", values=["stance_mean", "n"], aggfunc="mean"
    )
    pivot_arena.columns = [f"{c[0]}_{c[1]}" for c in pivot_arena.columns]
    pivot_arena = pivot_arena.reset_index()
    # Garder seulement les députés présents dans les deux arènes
    both = pivot_arena[
        pivot_arena["n_Twitter"].notna()
        & (pivot_arena["n_Twitter"] >= 3)
        & pivot_arena["n_AN"].notna()
        & (pivot_arena["n_AN"] >= 2)
    ].copy()
    both["delta_twitter_an"] = both["stance_mean_Twitter"] - both["stance_mean_AN"]
    both["abs_delta"] = both["delta_twitter_an"].abs()
    both = both.sort_values("abs_delta", ascending=False)
    both.to_csv(RESULTS_DIR / "coherence_twitter_an_par_depute.csv", index=False)
    print("  -> coherence_twitter_an_par_depute.csv")

    # -------------------------------------------------------------------------
    # 3. TARGET_PRIMARY : qui est critiqué, évolution par batch et bloc (v4)
    # -------------------------------------------------------------------------
    if has_v4 and "target_primary" in v4.columns:
        target_counts = (
            v4.groupby(["batch", "bloc", "target_primary"])
            .size()
            .reset_index(name="n")
        )
        target_pct = target_counts.merge(
            v4.groupby(["batch", "bloc"]).size().reset_index(name="total"),
            on=["batch", "bloc"],
        )
        target_pct["pct"] = (target_pct["n"] / target_pct["total"] * 100).round(2)
        target_pct[["batch", "bloc", "target_primary", "n", "pct"]].to_csv(
            RESULTS_DIR / "target_primary_par_batch_bloc.csv", index=False
        )
        print("  -> target_primary_par_batch_bloc.csv")

        target_bloc = (
            v4.groupby(["bloc", "target_primary"])
            .size()
            .reset_index(name="n")
        )
        target_bloc = target_bloc.merge(
            v4.groupby("bloc").size().reset_index(name="total"), on="bloc"
        )
        target_bloc["pct"] = (target_bloc["n"] / target_bloc["total"] * 100).round(2)
        target_bloc[["bloc", "target_primary", "n", "pct"]].to_csv(
            RESULTS_DIR / "target_primary_par_bloc.csv", index=False
        )
        print("  -> target_primary_par_bloc.csv")

    # -------------------------------------------------------------------------
    # 4. KEY_DEMANDS : combinaisons par bloc et batch (v4)
    # -------------------------------------------------------------------------
    if has_v4 and "key_demands" in v4.columns:
        rows = []
        for _, row in v4.iterrows():
            demands = flatten_key_demands(row.get("key_demands"))
            if not demands:
                demands = ["none"]
            for d in demands:
                rows.append({"bloc": row["bloc"], "batch": row.get("batch", "?"), "demand": d})
        df_dem = pd.DataFrame(rows)
        if len(df_dem) > 0:
            combo = df_dem.groupby(["bloc", "batch", "demand"]).size().reset_index(name="n")
            combo = combo.merge(
                df_dem.groupby(["bloc", "batch"]).size().reset_index(name="total"),
                on=["bloc", "batch"],
            )
            combo["pct"] = (combo["n"] / combo["total"] * 100).round(2)
            combo.to_csv(RESULTS_DIR / "key_demands_par_batch_bloc.csv", index=False)
            print("  -> key_demands_par_batch_bloc.csv")

    # -------------------------------------------------------------------------
    # 5. CONDITIONALITY : évolution temporelle (v4 par batch)
    # -------------------------------------------------------------------------
    if has_v4 and "conditionality" in v4.columns:
        cond_batch = (
            v4.groupby(["batch", "bloc", "conditionality"])
            .size()
            .reset_index(name="n")
        )
        cond_batch = cond_batch.merge(
            v4.groupby(["batch", "bloc"]).size().reset_index(name="total"),
            on=["batch", "bloc"],
        )
        cond_batch["pct"] = (cond_batch["n"] / cond_batch["total"] * 100).round(2)
        cond_batch[["batch", "bloc", "conditionality", "n", "pct"]].to_csv(
            RESULTS_DIR / "conditionality_par_batch_bloc.csv", index=False
        )
        print("  -> conditionality_par_batch_bloc.csv")

    # -------------------------------------------------------------------------
    # 6. CAS NÉGATIF DROITE : synthèse descriptive
    # -------------------------------------------------------------------------
    v3["batch"] = v3["date"].apply(lambda d: assign_batch(d, BATCHES))
    droite = v3[v3["bloc"] == "Droite"]
    droite_batch = (
        droite.groupby("batch")
        .agg(
            stance_mean=("stance_v3", "mean"),
            stance_std=("stance_v3", "std"),
            n=("stance_v3", "count"),
        )
        .reset_index()
    )
    droite_batch = droite_batch[droite_batch["batch"].isin(BATCH_ORDER)]
    droite_batch["bloc"] = "Droite"
    droite_batch.to_csv(RESULTS_DIR / "droite_stance_par_batch.csv", index=False)
    print("  -> droite_stance_par_batch.csv")

    # Stance mensuel Droite (pour figure zoom)
    droite_monthly = (
        droite.groupby(droite["date"].dt.to_period("M"))
        .agg(stance_mean=("stance_v3", "mean"), n=("stance_v3", "count"))
        .reset_index()
    )
    droite_monthly["date"] = droite_monthly["date"].dt.to_timestamp()
    droite_monthly.to_csv(RESULTS_DIR / "droite_stance_mensuel.csv", index=False)
    print("  -> droite_stance_mensuel.csv")

    print("\nAnalyses etendues terminees.")


if __name__ == "__main__":
    main()
