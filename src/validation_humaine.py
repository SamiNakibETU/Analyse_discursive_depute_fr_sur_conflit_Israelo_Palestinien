# -*- coding: utf-8 -*-
"""
Échantillonnage stratifié pour validation humaine de l'annotation LLM.

Génère data/validation/sample.csv avec 150 textes (≈40 par bloc si possible).
Colonnes : id, text, bloc — PAS le stance LLM, pour éviter le biais.

Usage :
  python src/validation_humaine.py

Puis annoter manuellement chaque texte sur l'échelle -2 à +2.
Sauvegarder les annotations dans data/validation/annotations.csv (colonnes : id, human_stance).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CORPUS_V3, BLOC_ORDER

VALIDATION_DIR = Path(__file__).resolve().parent.parent / "data" / "validation"
N_PER_BLOC = 40
N_TOTAL = 150


def main():
    import pandas as pd

    df = pd.read_parquet(CORPUS_V3)
    df = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df["_idx"] = range(len(df))

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    if text_col not in df.columns:
        print(f"Colonne de texte absente. Disponibles : {list(df.columns)}")
        return

    df["_idx"] = range(len(df))
    sample_list = []
    for bloc in BLOC_ORDER:
        sub = df[df["bloc"] == bloc]
        n = min(N_PER_BLOC, len(sub))
        if n == 0:
            continue
        drawn = sub.sample(n=n, random_state=42)
        sample_list.append(drawn)

    sample = pd.concat(sample_list, ignore_index=True).sample(frac=1, random_state=42)
    sample = sample.head(N_TOTAL)

    out = sample[["_idx", text_col, "bloc"]].rename(
        columns={"_idx": "id", text_col: "text"}
    )
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    out_path = VALIDATION_DIR / "sample.csv"
    out.to_csv(out_path, index=False)
    print(f"Échantillon de {len(out)} textes exporté vers {out_path}")
    print(out["bloc"].value_counts().to_string())


if __name__ == "__main__":
    main()
