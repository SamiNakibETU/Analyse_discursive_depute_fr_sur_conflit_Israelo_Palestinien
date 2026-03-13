#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test du nouveau script sur 10 textes du batch POST_CIJ."""
import os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from openai import OpenAI
from run_annotation_v4_gpt4mini import load_source_data, annotate_one, text_hash
from src.annotation.annotation_v4 import BATCHES

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("ERREUR: OPENAI_API_KEY non défini")
    sys.exit(1)

data_dir = Path("data/annotated/predictions")
print("Chargement données...")
source_df = load_source_data(data_dir)

# POST_CIJ
config = BATCHES["POST_CIJ"]
start, end = pd.Timestamp(config["start"]), pd.Timestamp(config["end"])
batch_df = source_df[(source_df["date"] >= start) & (source_df["date"] <= end)].head(10).copy()
print(f"Test sur {len(batch_df)} textes POST_CIJ")

client = OpenAI(api_key=api_key)
n_ok, n_fail = 0, 0

for i, (_, row) in enumerate(batch_df.iterrows()):
    text_preview = str(row.get("text_clean", ""))[:80].replace("\n", " ")
    print(f"\n[{i+1}/10] {text_preview}...")
    res = annotate_one(client, row, "POST_CIJ")
    if res["success"]:
        ann = res["annotation"]
        print(f"  ✓ stance={ann['stance_v4']} | ceasefire={ann['ceasefire_call']} | frame={ann['frame_primary']}")
        print(f"  reasoning: {ann.get('reasoning','')[:100]}...")
        n_ok += 1
    else:
        print(f"  ✗ ECHEC: {res['error']}")
        n_fail += 1
    time.sleep(0.35)

print(f"\n=== RÉSULTAT: {n_ok}/10 OK, {n_fail} echecs ===")
