"""
Prepare un CSV stratifie pour annotation manuelle.

Stratification:
- Par periode temporelle (pre/post 7 octobre, etc.)
- Par groupe politique (proportionnel)
- Par source (tweets vs interventions)
"""

import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent


# Periodes d'analyse
PERIODS = {
    "P0_pre_7oct": ("2023-01-01", "2023-10-06"),
    "P1_choc": ("2023-10-07", "2023-10-31"),
    "P2_offensive": ("2023-11-01", "2024-01-25"),
    "P3_post_cij": ("2024-01-26", "2024-05-05"),
    "P4_rafah": ("2024-05-06", "2024-09-30"),
    "P5_escalade": ("2024-10-01", "2024-11-20"),
    "P6_mandats_cpi": ("2024-11-21", "2025-01-14"),
    "P7_cessez_feu": ("2025-01-15", "2026-12-31"),
}


def assign_period(date) -> str:
    """Assigne une periode a une date."""
    if pd.isna(date):
        return "unknown"
    
    date = pd.to_datetime(date)
    for period_name, (start, end) in PERIODS.items():
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        if start_dt <= date <= end_dt:
            return period_name
    return "unknown"


def stratified_sample(
    df: pd.DataFrame,
    n_samples: int,
    stratify_cols: list,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Echantillonnage stratifie.
    
    Essaie de respecter les proportions originales,
    avec un minimum de 1 par strate si possible.
    """
    np.random.seed(random_state)
    
    # Creer une colonne de stratification combinee
    df = df.copy()
    df["_strata"] = df[stratify_cols].astype(str).agg("_".join, axis=1)
    
    strata_counts = df["_strata"].value_counts()
    total = len(df)
    
    samples = []
    remaining = n_samples
    
    # Premiere passe: allocation proportionnelle
    for strata, count in strata_counts.items():
        prop = count / total
        n_for_strata = max(1, int(prop * n_samples))
        n_for_strata = min(n_for_strata, count, remaining)
        
        strata_df = df[df["_strata"] == strata]
        sample = strata_df.sample(n=n_for_strata, random_state=random_state)
        samples.append(sample)
        remaining -= n_for_strata
        
        if remaining <= 0:
            break
    
    result = pd.concat(samples, ignore_index=True)
    result = result.drop(columns=["_strata"])
    
    return result


def prepare_tweets_for_annotation(
    input_file: Path,
    n_samples: int = 500
) -> pd.DataFrame:
    """Prepare les tweets pour annotation."""
    logger.info(f"Loading tweets from {input_file}")
    df = pd.read_parquet(input_file)
    
    # Preparer les colonnes
    df["date"] = pd.to_datetime(df["date_parsed"])
    df["period"] = df["date"].apply(assign_period)
    
    # Groupe politique (si disponible)
    if "groupe_politique" not in df.columns:
        df["groupe_politique"] = "unknown"
    df["groupe_politique"] = df["groupe_politique"].fillna("unknown")
    
    # Echantillonnage stratifie
    stratify_cols = ["period", "groupe_politique"]
    sample_df = stratified_sample(df, n_samples, stratify_cols)
    
    # Colonnes pour annotation
    annotation_df = pd.DataFrame({
        "id": range(1, len(sample_df) + 1),
        "source": "twitter",
        "username": sample_df["username"].values,
        "date": sample_df["date"].dt.strftime("%Y-%m-%d").values,
        "period": sample_df["period"].values,
        "groupe_politique": sample_df["groupe_politique"].values,
        "text": sample_df["text"].values,
        "keyword_matches": sample_df["keyword_matches"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else str(x)
        ).values,
        # Colonnes a remplir
        "stance": "",  # -1, 0, 1
        "intensity": "",  # 1, 2, 3
        "target": "",  # Israel, Palestine, Hamas, Civils, France, Autre
        "frame": "",  # HUM, SEC, LEG, HIS, DIP, MOR
        "confidence": "",  # high, medium, low
        "notes": ""
    })
    
    return annotation_df


def prepare_interventions_for_annotation(
    input_file: Path,
    n_samples: int = 200
) -> pd.DataFrame:
    """Prepare les interventions AN pour annotation."""
    logger.info(f"Loading interventions from {input_file}")
    df = pd.read_parquet(input_file)
    
    # Preparer les colonnes
    if "sitting_date" in df.columns:
        df["date"] = pd.to_datetime(df["sitting_date"])
    elif "intervention_date" in df.columns:
        df["date"] = pd.to_datetime(df["intervention_date"])
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    else:
        df["date"] = pd.NaT
    
    df["period"] = df["date"].apply(assign_period)
    
    # Groupe politique
    if "groupe_politique" not in df.columns:
        if "matched_group" in df.columns:
            df["groupe_politique"] = df["matched_group"]
        elif "group" in df.columns:
            df["groupe_politique"] = df["group"]
        else:
            df["groupe_politique"] = "unknown"
    df["groupe_politique"] = df["groupe_politique"].fillna("unknown")
    
    # Nom du depute
    if "depute_name" not in df.columns:
        if "speaker_name" in df.columns:
            df["depute_name"] = df["speaker_name"]
        elif "matched_name" in df.columns:
            df["depute_name"] = df["matched_name"]
        else:
            df["depute_name"] = "unknown"
    
    # Echantillonnage stratifie
    stratify_cols = ["period", "groupe_politique"]
    sample_df = stratified_sample(df, n_samples, stratify_cols)
    
    # Texte
    text_col = "normalized_text" if "normalized_text" in sample_df.columns else "text"
    
    # Colonnes pour annotation
    annotation_df = pd.DataFrame({
        "id": range(1, len(sample_df) + 1),
        "source": "assemblee_nationale",
        "depute_name": sample_df["depute_name"].values,
        "date": sample_df["date"].dt.strftime("%Y-%m-%d").values,
        "period": sample_df["period"].values,
        "groupe_politique": sample_df["groupe_politique"].values,
        "text": sample_df[text_col].values,
        "keyword_matches": sample_df.get("keyword_matches_new", sample_df.get("keyword_matches", "")).apply(
            lambda x: ", ".join(x) if isinstance(x, list) else str(x)
        ).values,
        # Colonnes a remplir
        "stance": "",
        "intensity": "",
        "target": "",
        "frame": "",
        "confidence": "",
        "notes": ""
    })
    
    return annotation_df


def main():
    """Genere les fichiers CSV pour annotation."""
    output_dir = PROJECT_ROOT / "data" / "annotated" / "to_annotate"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Tweets
    tweets_file = PROJECT_ROOT / "data" / "filtered" / "tweets_gaza.parquet"
    if tweets_file.exists():
        tweets_df = prepare_tweets_for_annotation(tweets_file, n_samples=500)
        output_tweets = output_dir / "tweets_to_annotate.csv"
        tweets_df.to_csv(output_tweets, index=False, encoding="utf-8-sig")
        logger.info(f"Saved {len(tweets_df)} tweets to {output_tweets}")
        
        # Stats
        logger.info(f"\nDistribution tweets:")
        logger.info(f"  Par periode:")
        for period, count in tweets_df["period"].value_counts().items():
            logger.info(f"    {period}: {count}")
        logger.info(f"  Par groupe:")
        for group, count in tweets_df["groupe_politique"].value_counts().head(8).items():
            logger.info(f"    {group}: {count}")
    
    # Interventions
    interv_file = PROJECT_ROOT / "data" / "filtered" / "interventions_gaza.parquet"
    if interv_file.exists():
        interv_df = prepare_interventions_for_annotation(interv_file, n_samples=200)
        output_interv = output_dir / "interventions_to_annotate.csv"
        interv_df.to_csv(output_interv, index=False, encoding="utf-8-sig")
        logger.info(f"\nSaved {len(interv_df)} interventions to {output_interv}")
        
        # Stats
        logger.info(f"\nDistribution interventions:")
        logger.info(f"  Par periode:")
        for period, count in interv_df["period"].value_counts().items():
            logger.info(f"    {period}: {count}")
    
    # Fichier combine
    if tweets_file.exists() and interv_file.exists():
        combined = pd.concat([tweets_df, interv_df], ignore_index=True)
        combined["id"] = range(1, len(combined) + 1)
        output_combined = output_dir / "corpus_to_annotate.csv"
        combined.to_csv(output_combined, index=False, encoding="utf-8-sig")
        logger.info(f"\nSaved combined corpus ({len(combined)} texts) to {output_combined}")
    
    # Instructions
    print("\n" + "=" * 60)
    print("FICHIERS GENERES")
    print("=" * 60)
    print(f"\n1. {output_tweets}")
    print(f"2. {output_interv}")
    print(f"3. {output_combined}")
    print("\n" + "=" * 60)
    print("INSTRUCTIONS D'ANNOTATION")
    print("=" * 60)
    print("""
Colonnes a remplir:

- stance: -1 (Pro-Israel), 0 (Neutre), 1 (Pro-Palestine)
- intensity: 1 (modere), 2 (marque), 3 (fort)
- target: Israel, Palestine, Hamas, Civils, France, Autre
- frame: HUM (humanitaire), SEC (securitaire), LEG (juridique), 
         HIS (historique), DIP (diplomatique), MOR (moral)
- confidence: high, medium, low
- notes: commentaires libres

Voir le codebook complet: docs/codebook_annotation.md
""")


if __name__ == "__main__":
    main()
