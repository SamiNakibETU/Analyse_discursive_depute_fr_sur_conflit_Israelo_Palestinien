# -*- coding: utf-8 -*-
"""
Échantillonnage pour validation humaine.
150 textes triplement stratifiés : bloc (proportionnel), arène (proportionnel), batch (min 2 par bloc×batch).
Export sans stance_v3/stance_v4 — l'annotateur juge en aveugle.

Usage: python src/validation_humaine.py
Sortie: data/validation/sample_150.csv

# AJOUT TÂCHE A1
"""

from pathlib import Path
import hashlib
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CORPUS_V3, CORPUS_V4, BLOC_ORDER, BATCHES, month_to_batch


def _compute_text_hash(text):
    """Hash du texte pour merge ultérieur avec corpus (sans exposer le contenu)."""
    return hashlib.sha256(str(text).encode("utf-8", errors="replace")).hexdigest()[:16]


def main():
    out_dir = Path(__file__).resolve().parent.parent / "data" / "validation"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "sample_150.csv"

    dfs = []
    if CORPUS_V3.exists():
        df3 = pd.read_parquet(CORPUS_V3)
        df3["source"] = "v3"
        dfs.append(df3)
    if CORPUS_V4.exists():
        df4 = pd.read_parquet(CORPUS_V4)
        df4["source"] = "v4"
        dfs.append(df4)

    if not dfs:
        print("Corpus absent. Exécuter prepare_data.py d'abord.")
        return

    df = pd.concat(dfs, ignore_index=True)
    df = df[df["bloc"].isin(BLOC_ORDER)].copy()

    if "month" not in df.columns:
        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    df["batch"] = df["month"].apply(month_to_batch)

    arena_col = "arena" if "arena" in df.columns else None
    if arena_col is None:
        df["arena"] = "Twitter"
    else:
        df["arena"] = df[arena_col].fillna("Twitter")

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    df["text_hash"] = df[text_col].apply(_compute_text_hash)

    n_total = len(df)
    target = 150
    sampled_indices = []

    grp = df.groupby(["bloc", "batch"])
    for (bloc, batch), sub in grp:
        n_available = len(sub)
        if n_available == 0:
            continue
        n_take = min(2, n_available)
        taken = sub.sample(n=n_take, random_state=42).index.tolist()
        sampled_indices.extend(taken)

    sampled_set = set(sampled_indices)
    df_remaining = df[~df.index.isin(sampled_set)]

    if len(sampled_indices) < target and len(df_remaining) > 0:
        need = target - len(sampled_indices)
        bloc_props = df.groupby("bloc").size() / n_total
        for bloc in BLOC_ORDER:
            if need <= 0:
                break
            sub = df_remaining[(df_remaining["bloc"] == bloc) & (~df_remaining.index.isin(sampled_set))]
            if len(sub) == 0:
                continue
            n_for_bloc = max(1, round(need * bloc_props.get(bloc, 0.25)))
            n_for_bloc = min(n_for_bloc, need, len(sub))
            if n_for_bloc > 0:
                arena_props = sub.groupby("arena").size() / len(sub)
                for arena_val in ["Twitter", "AN"]:
                    if arena_val not in arena_props.index:
                        continue
                    sub_arena = sub[sub["arena"] == arena_val]
                    n_arena = min(max(1, round(n_for_bloc * arena_props[arena_val])), len(sub_arena), need)
                    if n_arena > 0:
                        extra = sub_arena.sample(n=n_arena, random_state=42).index.tolist()
                        sampled_indices.extend(extra)
                        sampled_set.update(extra)
                        need -= n_arena

    if len(sampled_indices) < target and len(df_remaining) > 0:
        still_need = target - len(sampled_indices)
        pool = df_remaining[~df_remaining.index.isin(sampled_indices)]
        if len(pool) > 0:
            add = pool.sample(n=min(still_need, len(pool)), random_state=42).index.tolist()
            sampled_indices.extend(add)

    sample = df.loc[sampled_indices].drop_duplicates(subset=["text_hash"], keep="first")
    if len(sample) > target:
        sample = sample.sample(n=target, random_state=42)
    sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)

    sample["id"] = range(len(sample))
    export_cols = ["id", "text_hash", text_col, "bloc", "arena", "batch", "author", "date", "source"]
    export_cols = [c for c in export_cols if c in sample.columns]
    out = sample[export_cols].copy()
    out = out.rename(columns={text_col: "text"}) if text_col != "text" else out

    for col in ["stance_v3", "stance_v4", "stance"]:
        if col in out.columns:
            out = out.drop(columns=[col])

    out.to_csv(out_path, index=False)
    print(f"Echantillon {len(out)} textes -> {out_path}")
    print("\nRépartition par bloc:")
    print(out["bloc"].value_counts().to_string())
    print("\nRépartition par arène:")
    print(out["arena"].value_counts().to_string())
    print("\nRépartition par batch:")
    print(out["batch"].value_counts().to_string())


if __name__ == "__main__":
    main()
