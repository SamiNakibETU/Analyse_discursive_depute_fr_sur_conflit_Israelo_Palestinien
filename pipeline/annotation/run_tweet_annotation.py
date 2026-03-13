# -*- coding: utf-8 -*-
"""
Script d'annotation LLM V3 pour les tweets avec contexte enrichi.
Ajoute le contexte complet pour chaque tweet (RT, replies, metadata).
"""
import sys
import os
import json
import time
import re
from pathlib import Path
from datetime import datetime

import pandas as pd
from tqdm import tqdm

sys.stdout.reconfigure(encoding='utf-8')

# Ajouter src au path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from annotation.llm_annotation_v3 import annotate_text_v3, AnnotationResultV3

# Configuration
INPUT_FILE = PROJECT_ROOT / "data" / "filtered" / "tweets_gaza.parquet"
OUTPUT_DIR = PROJECT_ROOT / "data" / "annotated" / "predictions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 500
MODEL = "gpt-4o-mini"

# Periodes pour le contexte
PERIODS = {
    "pre_october_2023": ("2023-01-01", "2023-10-06"),
    "october_attack": ("2023-10-07", "2023-10-31"),
    "ground_offensive": ("2023-11-01", "2023-12-31"),
    "genocide_debate": ("2024-01-01", "2024-03-31"),
    "rafah_offensive": ("2024-04-01", "2024-08-31"),
    "icc_mandate": ("2024-09-01", "2024-12-31"),
    "ceasefire": ("2025-01-01", "2026-12-31"),
}


def get_period(date_str):
    """Determine la periode pour une date."""
    if pd.isna(date_str):
        return "Unknown"
    try:
        if isinstance(date_str, str):
            date = pd.to_datetime(date_str)
        else:
            date = date_str
        for name, (start, end) in PERIODS.items():
            if pd.to_datetime(start) <= date <= pd.to_datetime(end):
                return name
        return "Other"
    except:
        return "Unknown"


def build_tweet_context(row):
    """Construit le contexte enrichi pour un tweet."""
    context_parts = []
    
    text = str(row.get("text", ""))
    
    # Detecter si c'est un RT
    if text.startswith("RT @"):
        match = re.match(r"RT @(\w+):", text)
        if match:
            original_author = match.group(1)
            context_parts.append(f"Ce tweet est un RETWEET de @{original_author}. Le depute approuve/partage ce contenu.")
    
    # Detecter si c'est une reply
    if text.startswith("@"):
        match = re.match(r"^@(\w+)", text)
        if match:
            replied_to = match.group(1)
            context_parts.append(f"Ce tweet est une REPONSE a @{replied_to}.")
    
    # Mentions dans le texte
    mentions = re.findall(r"@(\w+)", text)
    if mentions and not text.startswith("RT "):
        context_parts.append(f"Mentions: {', '.join(['@' + m for m in mentions[:5]])}")
    
    # Hashtags
    hashtags = re.findall(r"#(\w+)", text)
    if hashtags:
        context_parts.append(f"Hashtags: {', '.join(['#' + h for h in hashtags[:10]])}")
    
    # Engagement
    retweets = row.get("retweets", 0)
    likes = row.get("likes", 0)
    if pd.notna(retweets) and pd.notna(likes):
        context_parts.append(f"Engagement: {int(retweets)} RT, {int(likes)} likes")
    
    # URL pour tracabilite
    url = row.get("url", "")
    if url and pd.notna(url):
        if not url.startswith("http"):
            url = f"https://twitter.com{url.replace('#m', '')}"
        context_parts.append(f"URL: {url}")
    
    return " | ".join(context_parts) if context_parts else "Aucun contexte additionnel"


def prepare_tweet_for_annotation(row):
    """Prepare un tweet pour l'annotation."""
    return {
        "text": str(row.get("text", "")),
        "author": str(row.get("username", "Unknown")),
        "group": str(row.get("groupe_politique", "Unknown")),
        "date": str(row.get("date_raw", "Unknown")),
        "period": get_period(row.get("date_parsed")),
        "context": build_tweet_context(row),
    }


def main():
    print("=" * 70)
    print("ANNOTATION LLM V3 - TWEETS AVEC CONTEXTE ENRICHI")
    print("=" * 70)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modele: {MODEL}")
    
    # Charger les donnees
    print(f"\nChargement: {INPUT_FILE}")
    df = pd.read_parquet(INPUT_FILE)
    print(f"Total tweets: {len(df)}")
    
    # Verifier les chunks deja traites
    existing_chunks = list(OUTPUT_DIR.glob("tweets_v3_chunk_*.parquet"))
    processed_indices = set()
    for chunk_file in existing_chunks:
        chunk_num = int(chunk_file.stem.split("_")[-1])
        start_idx = chunk_num * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(df))
        processed_indices.update(range(start_idx, end_idx))
    
    print(f"Deja traites: {len(processed_indices)} tweets")
    remaining = len(df) - len(processed_indices)
    print(f"Restants: {remaining} tweets")
    
    if remaining == 0:
        print("\nTous les tweets ont ete annotes!")
        return
    
    # Traiter par chunks
    n_chunks = (len(df) + CHUNK_SIZE - 1) // CHUNK_SIZE
    
    for chunk_idx in range(n_chunks):
        start_idx = chunk_idx * CHUNK_SIZE
        end_idx = min(start_idx + CHUNK_SIZE, len(df))
        
        output_file = OUTPUT_DIR / f"tweets_v3_chunk_{chunk_idx:03d}.parquet"
        
        if output_file.exists():
            print(f"\nChunk {chunk_idx}: deja traite, skip")
            continue
        
        chunk_df = df.iloc[start_idx:end_idx].copy()
        print(f"\n{'=' * 50}")
        print(f"CHUNK {chunk_idx}/{n_chunks-1} ({start_idx}-{end_idx})")
        print(f"{'=' * 50}")
        
        results = []
        
        for idx, (_, row) in enumerate(tqdm(chunk_df.iterrows(), total=len(chunk_df), desc=f"Chunk {chunk_idx}")):
            prepared = prepare_tweet_for_annotation(row)
            
            result = annotate_text_v3(
                text=prepared["text"],
                source_type="tweet",
                author=prepared["author"],
                group=prepared["group"],
                date=prepared["date"],
                period=prepared["period"],
                context=prepared["context"],
                model=MODEL
            )
            
            result_dict = {
                "stance_v3": result.stance,
                "stance_3class_v3": result.stance_3class,
                "intensity_v3": result.intensity,
                "confidence_v3": result.confidence,
                "primary_target_v3": result.primary_target,
                "secondary_target_v3": result.secondary_target,
                "primary_frame_v3": result.primary_frame,
                "secondary_frame_v3": result.secondary_frame,
                "is_off_topic_v3": result.is_off_topic,
                "is_ambiguous_v3": result.is_ambiguous,
                "has_both_sides_v3": result.has_both_sides,
                "reasoning_v3": result.reasoning,
                "indicators_v3": json.dumps(result.key_indicators, ensure_ascii=False),
                "rhetorical_strategy_v3": result.rhetorical_strategy
            }
            results.append(result_dict)
            
            # Rate limiting
            time.sleep(0.3)
        
        # Combiner et sauvegarder
        results_df = pd.DataFrame(results)
        chunk_result = pd.concat([chunk_df.reset_index(drop=True), results_df], axis=1)
        chunk_result.to_parquet(output_file, index=False)
        
        # Stats du chunk
        valid = chunk_result[~chunk_result['is_off_topic_v3']]
        print(f"\nStats chunk {chunk_idx}:")
        print(f"  Hors sujet: {chunk_result['is_off_topic_v3'].sum()}")
        print(f"  Distribution stance:")
        for stance in [-2, -1, 0, 1, 2]:
            count = (valid['stance_v3'] == stance).sum()
            pct = 100 * count / len(valid) if len(valid) > 0 else 0
            print(f"    {stance}: {count} ({pct:.1f}%)")
        
        print(f"\nSauvegarde: {output_file}")
    
    print("\n" + "=" * 70)
    print("ANNOTATION TERMINEE")
    print("=" * 70)


if __name__ == "__main__":
    main()
