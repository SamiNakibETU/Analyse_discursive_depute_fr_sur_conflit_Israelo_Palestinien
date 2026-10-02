"""
Consolidation des tweets bruts en format Parquet.

Ce script consolide les ~8500 fichiers JSON mensuels en un fichier Parquet unique.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Generator, Dict, Any

import pandas as pd
from tqdm import tqdm

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent.parent
COLLECTION_ROOT = PROJECT_ROOT.parent / "collection"
RAW_TWEETS_DIR = COLLECTION_ROOT / "data" / "interim" / "twitter_monthly"
OUTPUT_DIR = PROJECT_ROOT / "data" / "consolidated"


def iter_tweet_files(base_dir: Path) -> Generator[Path, None, None]:
    """Itère sur tous les fichiers JSON de tweets."""
    for user_dir in base_dir.iterdir():
        if user_dir.is_dir() and user_dir.name != "x.com":
            for json_file in user_dir.glob("*.json"):
                yield json_file


def parse_tweet_date(date_str: str) -> datetime | None:
    """Parse la date d'un tweet Nitter."""
    if not date_str:
        return None
    
    # Format Nitter: "Jan 30, 2023 · 7:09 PM UTC"
    try:
        # Nettoyer la chaîne
        clean = date_str.replace(" · ", " ").replace(" UTC", "")
        return datetime.strptime(clean, "%b %d, %Y %I:%M %p")
    except ValueError:
        try:
            # Format alternatif
            return datetime.strptime(date_str[:10], "%Y-%m-%d")
        except ValueError:
            return None


def extract_tweets_from_file(file_path: Path) -> list[Dict[str, Any]]:
    """Extrait les tweets d'un fichier JSON mensuel."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.warning(f"Erreur lecture {file_path}: {e}")
        return []
    
    tweets = data.get("tweets", [])
    username = file_path.parent.name
    month = file_path.stem  # ex: "2023-01"
    
    extracted = []
    for tweet in tweets:
        parsed_date = parse_tweet_date(tweet.get("date", ""))
        
        extracted.append({
            "username": username,
            "month_file": month,
            "tweet_id": tweet.get("id"),
            "text": tweet.get("text", ""),
            "date_raw": tweet.get("date"),
            "date_parsed": parsed_date,
            "retweets": tweet.get("retweets", 0),
            "likes": tweet.get("likes", 0),
            "replies": tweet.get("replies", 0),
            "quotes": tweet.get("quotes", 0),
            "is_retweet": tweet.get("is_retweet", False),
            "is_reply": tweet.get("is_reply", False),
            "has_media": bool(tweet.get("media")),
            "url": tweet.get("url", "")
        })
    
    return extracted


def consolidate_all_tweets() -> pd.DataFrame:
    """Consolide tous les tweets en un DataFrame."""
    logger.info(f"Scanning {RAW_TWEETS_DIR}")
    
    all_files = list(iter_tweet_files(RAW_TWEETS_DIR))
    logger.info(f"Found {len(all_files)} JSON files")
    
    all_tweets = []
    users_seen = set()
    
    for file_path in tqdm(all_files, desc="Processing files"):
        tweets = extract_tweets_from_file(file_path)
        all_tweets.extend(tweets)
        users_seen.add(file_path.parent.name)
    
    df = pd.DataFrame(all_tweets)
    
    # Convertir les types
    if 'date_parsed' in df.columns:
        df['date_parsed'] = pd.to_datetime(df['date_parsed'])
    
    # Créer une clé de déduplication composite (le champ id est souvent vide)
    # Utilise: username + date_raw + premiers 100 chars du texte
    df['_dedup_key'] = (
        df['username'].fillna('') + '|' + 
        df['date_raw'].fillna('') + '|' + 
        df['text'].fillna('').str[:100]
    )
    
    # Filtrer les faux tweets (requêtes de recherche)
    # Pattern: "from:xxx until:xxx" sont des artefacts du scraping
    initial_count = len(df)
    df = df[~df['text'].str.contains(r'^from:\w+ until:', regex=True, na=False)]
    search_artifacts = initial_count - len(df)
    if search_artifacts > 0:
        logger.info(f"Removed {search_artifacts} search query artifacts")
    
    # Dédupliquer par clé composite
    initial_count = len(df)
    df = df.drop_duplicates(subset=['_dedup_key'], keep='first')
    df = df.drop(columns=['_dedup_key'])
    duplicates_removed = initial_count - len(df)
    
    logger.info(f"Consolidated {len(df)} unique tweets from {len(users_seen)} users")
    logger.info(f"Removed {duplicates_removed} duplicates")
    
    return df


def add_metadata(df: pd.DataFrame, deputes_file: Path) -> pd.DataFrame:
    """Ajoute les métadonnées des députés (groupe politique, etc.)."""
    if not deputes_file.exists():
        logger.warning(f"Fichier députés non trouvé: {deputes_file}")
        return df
    
    with open(deputes_file, 'r', encoding='utf-8') as f:
        deputes_data = json.load(f)
    
    # Créer mapping username -> metadata
    username_to_meta = {}
    for dep in deputes_data.get('validated_accounts', []):
        username = dep.get('validated_username', '').lower()
        username_to_meta[username] = {
            'depute_name': dep.get('depute_name'),
            'groupe_politique': dep.get('group'),
            'intervention_count': dep.get('intervention_count', 0)
        }
    
    # Merger
    df['username_lower'] = df['username'].str.lower()
    meta_df = pd.DataFrame.from_dict(username_to_meta, orient='index')
    meta_df.index.name = 'username_lower'
    meta_df = meta_df.reset_index()
    
    df = df.merge(meta_df, on='username_lower', how='left')
    df = df.drop(columns=['username_lower'])
    
    matched = df['depute_name'].notna().sum()
    logger.info(f"Matched {matched}/{len(df)} tweets to deputies metadata")
    
    return df


def main():
    """Point d'entrée principal."""
    logger.info("=" * 60)
    logger.info("CONSOLIDATION DES TWEETS")
    logger.info("=" * 60)
    
    # Créer le dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Consolider
    df = consolidate_all_tweets()
    
    # Ajouter métadonnées
    deputes_file = COLLECTION_ROOT / "data" / "interim" / "deputes_to_scrape.json"
    df = add_metadata(df, deputes_file)
    
    # Statistiques
    logger.info("\n" + "=" * 40)
    logger.info("STATISTIQUES")
    logger.info("=" * 40)
    logger.info(f"Total tweets: {len(df):,}")
    logger.info(f"Utilisateurs uniques: {df['username'].nunique()}")
    if 'date_parsed' in df.columns:
        logger.info(f"Période: {df['date_parsed'].min()} → {df['date_parsed'].max()}")
    if 'groupe_politique' in df.columns:
        logger.info(f"\nPar groupe politique:")
        for group, count in df['groupe_politique'].value_counts().head(10).items():
            logger.info(f"  {group}: {count:,}")
    
    # Sauvegarder en Parquet
    output_file = OUTPUT_DIR / "tweets_all.parquet"
    df.to_parquet(output_file, index=False, compression='snappy')
    logger.info(f"\nSauvegardé: {output_file}")
    logger.info(f"Taille: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Sauvegarder aussi en CSV pour inspection
    csv_sample = OUTPUT_DIR / "tweets_sample.csv"
    df.head(1000).to_csv(csv_sample, index=False)
    logger.info(f"Échantillon CSV: {csv_sample}")
    
    return df


if __name__ == "__main__":
    main()


