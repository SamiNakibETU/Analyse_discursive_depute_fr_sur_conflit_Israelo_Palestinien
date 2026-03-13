#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'exécution du pipeline d'annotation v4.
Usage: python run_annotation_v4.py [--batch CHOC] [--dry-run]
"""

import argparse
import os
import sys
from pathlib import Path

# S'assurer que projet_gaza est dans le path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from src.annotation.annotation_v4 import BATCHES, run_annotation_batch_sync

OCT7 = pd.Timestamp("2023-10-07")
BLOCS = {
    "Gauche radicale": ["LFI-NFP", "LFI", "GDR"],
    "Gauche moderee": ["SOC", "PS-NFP", "ECO", "ECO-NFP"],
    "Centre / Majorite": ["REN", "MODEM", "HOR", "EPR", "DEM"],
    "Droite": ["LR", "RN", "UDR", "NI"],
}
GROUP_TO_BLOC = {g: b for b, gs in BLOCS.items() for g in gs}


def load_and_filter_data(data_dir: Path):
    """Charge et filtre les données."""
    tw = pd.read_parquet(data_dir / "tweets_v3_full_clean.parquet")
    iv = pd.read_parquet(data_dir / "interventions_v3_full_clean.parquet")

    tw["author"] = tw["depute_name"].fillna(tw["username"])
    tw["group"] = tw["groupe_politique"].fillna("UNKNOWN")
    tw["bloc"] = tw["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
    tw["date"] = pd.to_datetime(tw["date_parsed"], errors="coerce")
    tw["text_clean"] = tw["text"]
    tw["arena"] = "Twitter"

    iv["author"] = iv.get("speaker_name", iv.get("matched_name", iv.get("AUTEUR", "")))
    iv["group"] = iv["GROUPE"].fillna(iv.get("matched_group", "UNKNOWN"))
    iv["bloc"] = iv["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
    iv["date"] = pd.to_datetime(iv["sitting_date"], errors="coerce")
    iv["text_clean"] = iv["cleaned_text"].fillna(iv.get("TEXTE", ""))
    iv["arena"] = "AN"

    shared = ["author", "group", "bloc", "date", "text_clean", "stance_v3", "confidence_v3",
              "primary_frame_v3", "primary_target_v3", "is_off_topic_v3", "arena", "retweets", "likes"]
    for c in shared:
        if c not in tw.columns:
            tw[c] = 0 if c in ["retweets", "likes"] else None
        if c not in iv.columns:
            iv[c] = 0 if c in ["retweets", "likes"] else None

    tw_f = tw[(~tw["is_off_topic_v3"].fillna(False)) & (tw["confidence_v3"] >= 0.70) & (tw["bloc"] != "UNKNOWN") & (tw["date"].notna())]
    iv_f = iv[(~iv["is_off_topic_v3"].fillna(False)) & (iv["confidence_v3"] >= 0.70) & (iv["bloc"] != "UNKNOWN") & (iv["date"].notna())]

    df = pd.concat([tw_f[shared], iv_f[shared]], ignore_index=True)
    df_post = df[df["date"] >= OCT7].copy()
    return df_post


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", choices=list(BATCHES.keys()) + ["all"], default="all")
    parser.add_argument("--dry-run", action="store_true", help="Affiche les effectifs sans annoter")
    parser.add_argument("--retry-failed", action="store_true", help="Ré-annote uniquement les textes en échec (annotation_failed)")
    parser.add_argument("--model", default="gpt-4o-mini", help="gpt-4o-mini (fiable) ou gpt-5-nano (économique, peut avoir content vide)")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--data-dir", default="data/annotated/predictions")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not (data_dir / "tweets_v3_full_clean.parquet").exists():
        print(f"ERREUR: {data_dir / 'tweets_v3_full_clean.parquet'} introuvable.")
        sys.exit(1)

    df_post = load_and_filter_data(data_dir)
    print(f"Corpus post-7 oct: {len(df_post):,} textes")

    batches_to_run = [args.batch] if args.batch != "all" else list(BATCHES.keys())

    output_dir = Path(args.output_dir)
    for batch_name in batches_to_run:
        config = BATCHES[batch_name]
        start = pd.Timestamp(config["start"])
        end = pd.Timestamp(config["end"])
        mask = (df_post["date"] >= start) & (df_post["date"] <= end)
        batch_df = df_post[mask].copy()
        batch_df = batch_df.reset_index(drop=True)

        existing_path = output_dir / f"annotations_v4_{batch_name}.parquet"
        if args.retry_failed and existing_path.exists():
            existing = pd.read_parquet(existing_path)
            failed_mask = existing.get("annotation_failed", pd.Series([False] * len(existing))).fillna(False)
            n_failed = int(failed_mask.sum())
            if n_failed == 0:
                print(f"Batch {batch_name}: 0 échec, rien à ré-annoter.")
                continue
            # Colonnes à garder pour ré-annotation (données brutes)
            keep_cols = ["author", "group", "bloc", "date", "text_clean", "stance_v3", "confidence_v3",
                         "primary_frame_v3", "primary_target_v3", "is_off_topic_v3", "arena", "retweets", "likes"]
            batch_df = existing.loc[failed_mask, [c for c in keep_cols if c in existing.columns]].copy()
            batch_df = batch_df.reset_index(drop=True)
            print(f"Batch {batch_name}: {n_failed:,} échecs à ré-annoter (sur {len(existing):,})")
        elif args.retry_failed:
            print(f"Batch {batch_name}: pas de fichier existant, annotation complète.")

        if len(batch_df) == 0:
            continue

        if args.dry_run:
            print(f"  → {len(batch_df):,} textes à annoter")
            continue

        if not os.environ.get("OPENAI_API_KEY"):
            print("OPENAI_API_KEY non défini. Exportez-la ou définissez-la.")
            sys.exit(1)

        result_df = run_annotation_batch_sync(batch_df, batch_name, output_dir=str(args.output_dir), model=args.model, concurrency=args.concurrency)

        if args.retry_failed and existing_path.exists():
            # Fusionner : garder les succès existants + remplacer par les nouveaux résultats
            success_existing = existing[~failed_mask].copy()
            merged = pd.concat([success_existing, result_df], ignore_index=True)
            merged.to_parquet(existing_path, index=False)
            n_ok = (~result_df["annotation_failed"].fillna(False)).sum() if "annotation_failed" in result_df.columns else len(result_df)
            print(f"  → {n_ok:,} ré-annotés avec succès, fusionné dans annotations_v4_{batch_name}.parquet")
        else:
            print(f"  → annotations_v4_{batch_name}.parquet sauvegardé.")


if __name__ == "__main__":
    main()
