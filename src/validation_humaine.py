# -*- coding: utf-8 -*-
"""
Échantillonnage pour validation humaine de l'annotation LLM.
150 textes stratifiés par bloc (max 40 par bloc), mélangés v3/v4.
Exporter sans colonne stance LLM — l'annotateur juge en aveugle.

Usage: python src/validation_humaine.py
Sortie: data/validation/sample_150.csv
"""

from pathlib import Path
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CORPUS_V3, CORPUS_V4, BLOC_ORDER


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

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    n_per_bloc = min(40, df.groupby("bloc").size().min())

    sample = (
        df.groupby("bloc", group_keys=False)
        .apply(lambda g: g.sample(n=min(n_per_bloc, len(g)), random_state=42))
        .reset_index(drop=True)
    )

    sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)

    if "id" not in sample.columns:
        sample["id"] = range(len(sample))
    export_cols = ["id", text_col, "bloc", "source", "author", "date"]
    export_cols = [c for c in export_cols if c in sample.columns]

    out = sample[export_cols].copy()
    out.columns = [c if c != text_col else "text" for c in out.columns]
    out.to_csv(out_path, index=False)
    print(f"Échantillon {len(out)} textes → {out_path}")
    print(out["bloc"].value_counts().to_string())


if __name__ == "__main__":
    main()
