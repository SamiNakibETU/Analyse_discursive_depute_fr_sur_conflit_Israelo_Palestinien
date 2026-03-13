#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test gpt-5-nano sur 30-50 textes et analyse."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from src.annotation.annotation_v4 import BATCHES, run_annotation_batch_sync

BLOCS = {"Gauche radicale": ["LFI-NFP","LFI","GDR"], "Gauche moderee": ["SOC","PS-NFP","ECO","ECO-NFP"],
         "Centre / Majorite": ["REN","MODEM","HOR","EPR","DEM"], "Droite": ["LR","RN","UDR","NI"]}
GROUP_TO_BLOC = {g: b for b, gs in BLOCS.items() for g in gs}


def main(n=40):
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY non défini")
        sys.exit(1)

    DATA_DIR = Path("data/annotated/predictions")
    tw = pd.read_parquet(DATA_DIR / "tweets_v3_full_clean.parquet")
    iv = pd.read_parquet(DATA_DIR / "interventions_v3_full_clean.parquet")

    tw["author"] = tw["depute_name"].fillna(tw["username"])
    tw["group"] = tw["groupe_politique"].fillna("UNKNOWN")
    tw["bloc"] = tw["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
    tw["date"] = pd.to_datetime(tw["date_parsed"], errors="coerce")
    tw["text_clean"] = tw["text"]
    tw["arena"] = "Twitter"

    iv["author"] = iv.get("speaker_name", iv.get("matched_name", iv.get("AUTEUR","")))
    iv["group"] = iv["GROUPE"].fillna(iv.get("matched_group","UNKNOWN"))
    iv["bloc"] = iv["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
    iv["date"] = pd.to_datetime(iv["sitting_date"], errors="coerce")
    iv["text_clean"] = iv["cleaned_text"].fillna(iv.get("TEXTE",""))
    iv["arena"] = "AN"

    shared = ["author","group","bloc","date","text_clean","stance_v3","confidence_v3","primary_frame_v3","primary_target_v3","is_off_topic_v3","arena","retweets","likes"]
    for c in shared:
        if c not in tw.columns: tw[c] = 0 if c in ["retweets","likes"] else None
        if c not in iv.columns: iv[c] = 0 if c in ["retweets","likes"] else None

    tw_f = tw[(~tw["is_off_topic_v3"].fillna(False)) & (tw["confidence_v3"]>=0.70) & (tw["bloc"]!="UNKNOWN") & (tw["date"].notna())]
    iv_f = iv[(~iv["is_off_topic_v3"].fillna(False)) & (iv["confidence_v3"]>=0.70) & (iv["bloc"]!="UNKNOWN") & (iv["date"].notna())]
    df = pd.concat([tw_f[shared], iv_f[shared]], ignore_index=True)
    df_post = df[df["date"] >= pd.Timestamp("2023-10-07")].copy()

    config = BATCHES["CHOC"]
    start, end = pd.Timestamp(config["start"]), pd.Timestamp(config["end"])
    mask = (df_post["date"]>=start) & (df_post["date"]<=end)
    batch_df = df_post[mask].head(n).copy().reset_index(drop=True)

    print(f"Test gpt-5-nano sur {len(batch_df)} textes (batch CHOC)")
    print("Lancement...")
    result = run_annotation_batch_sync(batch_df, "CHOC", output_dir="outputs", model="gpt-5-nano")
    out_path = Path("outputs") / "test_gpt5nano.parquet"
    result.to_parquet(out_path, index=False)

    failed = result.get("annotation_failed", pd.Series([False]*len(result))).fillna(False)
    n_ok = (~failed).sum()
    print(f"\n=== RÉSULTAT ===")
    print(f"Succès : {n_ok}/{len(result)} ({100*n_ok/len(result):.1f}%)")

    if n_ok > 0:
        ok = result[~failed]
        print(f"\n--- Distribution stance_v4 ---")
        print(ok["stance_v4"].value_counts().sort_index())
        print(f"\n--- ceasefire_call ---")
        print(ok["ceasefire_call"].value_counts())
        print(f"\n--- frame_primary ---")
        print(ok["frame_primary"].value_counts())
        print(f"\n--- Par bloc ---")
        for bloc in ["Gauche radicale", "Centre / Majorite", "Droite"]:
            sub = ok[ok["bloc"]==bloc]
            if len(sub) > 0:
                print(f"  {bloc}: stance moyen={sub['stance_v4'].mean():.2f}, n={len(sub)}")
    else:
        print("\n--- Erreurs (échantillon) ---")
        errs = result["flags"].dropna().head(5)
        for e in errs:
            print(f"  {e}")

    print(f"\nSauvegardé : {out_path}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    main(n)
