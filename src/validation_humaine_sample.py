# -*- coding: utf-8 -*-
"""
Échantillonnage pour validation humaine de l'annotation LLM.
150 textes stratifiés : ~40 par bloc (si possible), mélangés v3/v4.
Exporte un CSV sans le stance LLM pour annotation à l'aveugle.

Usage : python src/validation_humaine_sample.py
Output : data/validation/validation_humaine_sample.csv
"""

from pathlib import Path

import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CORPUS_V3, BLOC_ORDER

VALIDATION_DIR = Path(__file__).resolve().parent.parent / "data" / "validation"
N_TARGET = 150
N_PER_BLOC = 40


def main():
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CORPUS_V3)
    df_valid = df[df["bloc"].isin(BLOC_ORDER)].copy()

    # Stratifié par bloc : min(40, len(bloc)) par bloc
    samples = []
    for bloc in BLOC_ORDER:
        sub = df_valid[df_valid["bloc"] == bloc]
        n_take = min(N_PER_BLOC, len(sub))
        if n_take > 0:
            s = sub.sample(n=n_take, random_state=42)
            samples.append(s)

    if not samples:
        print("Aucune donnée avec bloc valide.")
        return

    sample = pd.concat(samples, ignore_index=True)
    # Sous-échantillonner à 150 si trop
    if len(sample) > N_TARGET:
        sample = sample.sample(n=N_TARGET, random_state=42)
    sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)

    text_col = "text_clean" if "text_clean" in sample.columns else "text"
    sample["id"] = range(len(sample))
    sample["text"] = sample[text_col]

    out_path = VALIDATION_DIR / "validation_humaine_sample.csv"
    sample[["id", "text", "bloc"]].to_csv(out_path, index=False, encoding="utf-8")

    ref_path = VALIDATION_DIR / "validation_humaine_llm_ref.csv"
    sample[["id", "stance_v3"]].to_csv(ref_path, index=False)
    print(f"Échantillon exporté : {out_path} ({len(sample)} textes)")
    print(f"Référence LLM (pour métriques) : {ref_path}")
    print(sample["bloc"].value_counts().to_string())


if __name__ == "__main__":
    main()
