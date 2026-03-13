# -*- coding: utf-8 -*-
"""
Script de lancement V3 - Corpus complet
=======================================
Lance l'annotation V3 sur les tweets ET interventions separement,
avec des prompts adaptes a chaque type de source.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
from unidecode import unidecode
from annotation.llm_annotation_v3 import annotate_text_v3

# Configuration
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "annotated" / "predictions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_filtered_data():
    """Load filtered corpus."""
    tweets_path = DATA_DIR / "filtered" / "tweets_gaza.parquet"
    interv_wide = DATA_DIR / "filtered" / "interventions_gaza_wide.parquet"
    interv_strict = DATA_DIR / "filtered" / "interventions_gaza.parquet"

    tweets_df = pd.read_parquet(tweets_path) if tweets_path.exists() else None
    if interv_wide.exists():
        interv_df = pd.read_parquet(interv_wide)
    elif interv_strict.exists():
        interv_df = pd.read_parquet(interv_strict)
    else:
        interv_df = None

    return tweets_df, interv_df


def prepare_tweets_for_annotation(df: pd.DataFrame, sample_size: int = None) -> pd.DataFrame:
    """Prepare tweets dataframe for annotation."""
    # Standardize column names
    col_mapping = {
        'text': 'TEXTE',
        'normalized_text': 'TEXTE',
        'username': 'AUTEUR',
        'depute_name': 'AUTEUR',
        'groupe_politique': 'GROUPE',
        'date_parsed': 'DATE',
        'is_retweet': 'CONTEXTE'
    }
    
    df = df.copy()
    
    # Apply mapping
    for old, new in col_mapping.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]
    
    # Create context column
    if 'is_retweet' in df.columns:
        df['CONTEXTE'] = df['is_retweet'].apply(lambda x: 'RETWEET' if x else 'ORIGINAL')
    else:
        df['CONTEXTE'] = 'UNKNOWN'
    
    # Add period
    if 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        df['PERIODE'] = df['DATE'].apply(categorize_period)
    else:
        df['PERIODE'] = 'UNKNOWN'
    
    # Ensure required columns exist
    for col in ['TEXTE', 'AUTEUR', 'GROUPE', 'DATE', 'PERIODE']:
        if col not in df.columns:
            df[col] = 'UNKNOWN'
    
    # Sample if requested
    if sample_size and sample_size < len(df):
        # Stratified sample by group and period
        df = df.groupby(['GROUPE', 'PERIODE'], group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(1, sample_size // 20)), random_state=42)
        )
        if len(df) > sample_size:
            df = df.sample(sample_size, random_state=42)
    
    return df


def _normalize_for_search(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = unidecode(text)
    return text


def _clean_person_name(name: str) -> str:
    """Normalize person names for consistency."""
    if not isinstance(name, str):
        return "UNKNOWN"
    cleaned = " ".join(name.replace("\u00a0", " ").split())
    if cleaned == "":
        return "UNKNOWN"
    # If all caps, convert to title case with particles preserved
    if cleaned.upper() == cleaned:
        particles = {"de", "du", "des", "la", "le", "les", "d'", "l'"}
        parts = []
        for part in cleaned.lower().split():
            if part in particles:
                parts.append(part)
            else:
                parts.append(part.capitalize())
        return " ".join(parts)
    return cleaned


def _find_keyword_word_index(text: str, keywords: list[str]) -> int | None:
    """Return word index for first keyword hit in text."""
    if not text or not keywords:
        return None

    normalized = _normalize_for_search(text)
    for kw in keywords:
        if not kw:
            continue
        kw_norm = _normalize_for_search(str(kw))
        pos = normalized.find(kw_norm)
        if pos >= 0:
            # approximate word index from char position
            prefix = normalized[:pos]
            return len(prefix.split())
    return None


def _excerpt_around_keywords(
    text: str,
    keywords: list[str],
    window_words: int = 500,
    max_words: int = 1200,
    min_words: int = 200,
) -> tuple[str, dict]:
    """
    Extract a window around the first keyword hit.
    If the intervention is short, keep full text.
    """
    if not isinstance(text, str) or not text.strip():
        return "", {"excerpt_used": False, "start_complete": True, "end_complete": True}

    words = text.split()
    total_words = len(words)
    if total_words <= max_words:
        return text, {"excerpt_used": False, "start_complete": True, "end_complete": True}

    hit_idx = _find_keyword_word_index(text, keywords) or 0
    start = max(0, hit_idx - window_words)
    end = min(total_words, hit_idx + window_words + 1)

    excerpt = " ".join(words[start:end])
    if len(excerpt.split()) < min_words:
        return text, {"excerpt_used": False, "start_complete": True, "end_complete": True}

    return excerpt, {
        "excerpt_used": True,
        "start_complete": start == 0,
        "end_complete": end == total_words,
    }


def prepare_interventions_for_annotation(df: pd.DataFrame, sample_size: int = None) -> pd.DataFrame:
    """Prepare interventions dataframe for annotation."""
    col_mapping = {
        'cleaned_text': 'TEXTE',
        'raw_text': 'TEXTE',
        'normalized_text': 'TEXTE',
        'intervention_text': 'TEXTE',
        'speaker_name': 'AUTEUR',
        'groupe_politique': 'GROUPE',
        'sitting_date': 'DATE',
        'intervention_date': 'DATE'
    }
    
    df = df.copy()
    
    # Apply mapping
    for old, new in col_mapping.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]
    
    # Context from intervention type
    if 'intervention_type' in df.columns:
        df['CONTEXTE'] = df['intervention_type']
    else:
        df['CONTEXTE'] = 'PARLEMENTAIRE'
    
    # Add period
    if 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
        df['PERIODE'] = df['DATE'].apply(categorize_period)
    else:
        df['PERIODE'] = 'UNKNOWN'
    
    # Ensure required columns
    for col in ['TEXTE', 'AUTEUR', 'GROUPE', 'DATE', 'PERIODE']:
        if col not in df.columns:
            df[col] = 'UNKNOWN'

    # Fill GROUPE from matched_group if missing/unknown
    if "matched_group" in df.columns:
        mask_unknown = df["GROUPE"].astype(str).str.strip().str.upper() == "UNKNOWN"
        df.loc[mask_unknown, "GROUPE"] = df.loc[mask_unknown, "matched_group"]
    if "matched_group_long" in df.columns:
        mask_unknown = df["GROUPE"].astype(str).str.strip().str.upper() == "UNKNOWN"
        df.loc[mask_unknown, "GROUPE"] = df.loc[mask_unknown, "matched_group_long"]

    # Normalize author names
    df["AUTEUR"] = df["AUTEUR"].apply(_clean_person_name)

    # Build excerpts around keyword hits for long interventions
    keyword_col = "keyword_matches_new" if "keyword_matches_new" in df.columns else "keyword_matches"
    if keyword_col in df.columns:
        excerpts = []
        excerpt_meta = []
        for _, row in df.iterrows():
            text = row.get("TEXTE", "")
            keywords = row.get(keyword_col, []) if isinstance(row.get(keyword_col, []), list) else []
            excerpt, meta = _excerpt_around_keywords(text, keywords)
            excerpts.append(excerpt)
            excerpt_meta.append(meta)

        df["TEXTE"] = excerpts
        df["EXCERPT_INFO"] = excerpt_meta
        df["CONTEXTE"] = df["CONTEXTE"].astype(str) + " | excerpt=" + df["EXCERPT_INFO"].astype(str)
    
    # Sample if requested
    if sample_size and sample_size < len(df):
        df = df.groupby(['GROUPE', 'PERIODE'], group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(1, sample_size // 20)), random_state=42)
        )
        if len(df) > sample_size:
            df = df.sample(sample_size, random_state=42)
    
    return df


def annotate_with_checkpoints(
    df: pd.DataFrame,
    source_type: str,
    output_path: Path,
    text_col: str = "TEXTE",
    author_col: str = "AUTEUR",
    group_col: str = "GROUPE",
    date_col: str = "DATE",
    period_col: str = "PERIODE",
    context_col: str = "CONTEXTE",
    model: str = "gpt-4o-mini",
    save_interval: int = 100,
):
    """
    Annotation avec checkpoints et reprise automatique.
    Sauve un .checkpoint.parquet tous les N items.
    """
    checkpoint_path = output_path.with_suffix(".checkpoint.parquet")

    if checkpoint_path.exists():
        done_df = pd.read_parquet(checkpoint_path)
        start_idx = len(done_df)
    else:
        done_df = None
        start_idx = 0

    if start_idx >= len(df):
        final_df = done_df if done_df is not None else df
        final_df.to_parquet(output_path, index=False)
        return final_df

    new_results = []

    for idx in range(start_idx, len(df)):
        row = df.iloc[idx]
        context = ""
        if context_col and context_col in df.columns:
            context = str(row.get(context_col, ""))

        result = annotate_text_v3(
            text=str(row.get(text_col, "")),
            source_type=source_type,
            author=str(row.get(author_col, "Unknown")),
            group=str(row.get(group_col, "Unknown")),
            date=str(row.get(date_col, "Unknown")),
            period=str(row.get(period_col, "Unknown")),
            context=context,
            model=model,
        )

        new_results.append(
            {
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
                "rhetorical_strategy_v3": result.rhetorical_strategy,
            }
        )

        if (idx + 1) % save_interval == 0:
            new_slice = df.iloc[start_idx : idx + 1].reset_index(drop=True)
            new_block = pd.concat(
                [new_slice, pd.DataFrame(new_results)], axis=1
            )
            if done_df is not None:
                partial = pd.concat([done_df, new_block], axis=0, ignore_index=True)
            else:
                partial = new_block
            partial.to_parquet(checkpoint_path, index=False)

    # Final save
    tail_df = pd.concat(
        [
            df.iloc[start_idx:].reset_index(drop=True),
            pd.DataFrame(new_results),
        ],
        axis=1,
    )
    if done_df is not None:
        final_df = pd.concat([done_df, tail_df], axis=0, ignore_index=True)
    else:
        final_df = tail_df

    final_df.to_parquet(output_path, index=False)
    return final_df


def categorize_period(date) -> str:
    """Categorize date into conflict period."""
    if pd.isna(date):
        return "UNKNOWN"
    
    if date < pd.Timestamp('2023-10-07'):
        return "PRE_CONFLICT"
    elif date < pd.Timestamp('2023-11-24'):
        return "INITIAL_OFFENSIVE"
    elif date < pd.Timestamp('2024-01-01'):
        return "TRUCE_PERIOD"
    elif date < pd.Timestamp('2024-05-01'):
        return "CIJ_PERIOD"
    elif date < pd.Timestamp('2024-11-01'):
        return "RAFAH_OFFENSIVE"
    elif date < pd.Timestamp('2025-01-19'):
        return "ICC_PERIOD"
    else:
        return "CEASEFIRE"


def main():
    print("=" * 70)
    print("ANNOTATION V3 - CORPUS COMPLET")
    print("=" * 70)
    
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["tweets", "interventions", "both"], default="both")
    parser.add_argument("--sample", type=int, default=None, help="Sample size per source")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()
    
    # Load data
    tweets_df, interv_df = load_filtered_data()
    
    # Process tweets
    if args.source in ["tweets", "both"] and tweets_df is not None:
        print(f"\n{'=' * 50}")
        print("TWEETS")
        print(f"{'=' * 50}")
        print(f"Total: {len(tweets_df)}")
        
        tweets_prep = prepare_tweets_for_annotation(tweets_df, args.sample)
        print(f"Pour annotation: {len(tweets_prep)}")
        
        output_tweets = OUTPUT_DIR / "tweets_v3_full.parquet"

        result_tweets = annotate_with_checkpoints(
            tweets_prep,
            source_type="tweet",
            text_col="TEXTE",
            author_col="AUTEUR",
            group_col="GROUPE",
            context_col="CONTEXTE",
            model=args.model,
            output_path=output_tweets,
            save_interval=100,
        )
        
        result_tweets.to_parquet(output_tweets, index=False)
        print(f"\nSauvegarde: {output_tweets}")
        
        # Stats
        valid = result_tweets[~result_tweets['is_off_topic_v3']]
        print(f"\nDistribution (3 classes):")
        print(valid['stance_3class_v3'].value_counts().sort_index())
    
    # Process interventions
    if args.source in ["interventions", "both"] and interv_df is not None:
        print(f"\n{'=' * 50}")
        print("INTERVENTIONS PARLEMENTAIRES")
        print(f"{'=' * 50}")
        print(f"Total: {len(interv_df)}")
        
        interv_prep = prepare_interventions_for_annotation(interv_df, args.sample)
        print(f"Pour annotation: {len(interv_prep)}")
        
        output_interv = OUTPUT_DIR / "interventions_v3_full.parquet"

        result_interv = annotate_with_checkpoints(
            interv_prep,
            source_type="intervention",
            text_col="TEXTE",
            author_col="AUTEUR",
            group_col="GROUPE",
            context_col="CONTEXTE",
            model=args.model,
            output_path=output_interv,
            save_interval=100,
        )
        
        result_interv.to_parquet(output_interv, index=False)
        print(f"\nSauvegarde: {output_interv}")
        
        # Stats
        valid = result_interv[~result_interv['is_off_topic_v3']]
        print(f"\nDistribution (3 classes):")
        print(valid['stance_3class_v3'].value_counts().sort_index())
    
    print(f"\n{'=' * 70}")
    print("TERMINE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
