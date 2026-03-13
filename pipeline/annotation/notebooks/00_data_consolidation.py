# %% [markdown]
# # 00 - Consolidation des données
# 
# Ce notebook consolide les données brutes (tweets et interventions AN) 
# en format Parquet pour analyse.

# %%
import sys
from pathlib import Path

# Ajouter src au path
PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pandas as pd
import json
from datetime import datetime
from collections import Counter

# %%
# Configuration
COLLECTION_DATA = PROJECT_ROOT.parent / "collection" / "data"
FINAL_DATA = COLLECTION_DATA  # alias
TWEETS_DIR = FINAL_DATA / "interim" / "twitter_monthly"
INTERVENTIONS_FILE = FINAL_DATA / "processed" / "interventions_gaza_filtered.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "data" / "consolidated"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Project root: {PROJECT_ROOT}")
print(f"Tweets dir exists: {TWEETS_DIR.exists()}")
print(f"Interventions file exists: {INTERVENTIONS_FILE.exists()}")

# %% [markdown]
# ## 1. Consolidation des tweets

# %%
def iter_tweet_files(base_dir):
    """Itère sur tous les fichiers JSON de tweets."""
    for user_dir in base_dir.iterdir():
        if user_dir.is_dir() and user_dir.name != "x.com":
            for json_file in user_dir.glob("*.json"):
                yield json_file

# Compter les fichiers
all_files = list(iter_tweet_files(TWEETS_DIR))
print(f"Nombre de fichiers JSON: {len(all_files)}")

# %%
from tqdm.auto import tqdm

def parse_tweet_date(date_str):
    """Parse la date d'un tweet Nitter."""
    if not date_str:
        return None
    try:
        clean = date_str.replace(" · ", " ").replace(" UTC", "")
        return datetime.strptime(clean, "%b %d, %Y %I:%M %p")
    except ValueError:
        return None

def extract_tweets_from_file(file_path):
    """Extrait les tweets d'un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return []
    
    tweets = data.get("tweets", [])
    username = file_path.parent.name
    month = file_path.stem
    
    extracted = []
    for tweet in tweets:
        extracted.append({
            "username": username,
            "month_file": month,
            "tweet_id": tweet.get("id"),
            "text": tweet.get("text", ""),
            "date_raw": tweet.get("date"),
            "date_parsed": parse_tweet_date(tweet.get("date")),
            "retweets": tweet.get("retweets", 0),
            "likes": tweet.get("likes", 0),
            "replies": tweet.get("replies", 0),
            "is_retweet": tweet.get("is_retweet", False),
            "is_reply": tweet.get("is_reply", False),
            "url": tweet.get("url", "")
        })
    return extracted

# %%
# Consolider tous les tweets
all_tweets = []
for file_path in tqdm(all_files, desc="Processing files"):
    tweets = extract_tweets_from_file(file_path)
    all_tweets.extend(tweets)

tweets_df = pd.DataFrame(all_tweets)
print(f"\nTweets bruts: {len(tweets_df):,}")

# %%
# Dédupliquer
initial = len(tweets_df)
tweets_df = tweets_df.drop_duplicates(subset=['tweet_id'], keep='first')
print(f"Tweets après déduplication: {len(tweets_df):,}")
print(f"Doublons supprimés: {initial - len(tweets_df):,}")

# %%
# Convertir les dates
tweets_df['date_parsed'] = pd.to_datetime(tweets_df['date_parsed'])

# Statistiques
print(f"\n=== STATISTIQUES TWEETS ===")
print(f"Total: {len(tweets_df):,}")
print(f"Utilisateurs: {tweets_df['username'].nunique()}")
print(f"Période: {tweets_df['date_parsed'].min()} → {tweets_df['date_parsed'].max()}")

# %%
# Sauvegarder
output_file = OUTPUT_DIR / "tweets_all.parquet"
tweets_df.to_parquet(output_file, index=False)
print(f"\nSauvegardé: {output_file}")
print(f"Taille: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

# %% [markdown]
# ## 2. Consolidation des interventions AN

# %%
# Charger les interventions
interventions = []
with open(INTERVENTIONS_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        interventions.append(json.loads(line))

interv_df = pd.DataFrame(interventions)
print(f"\n=== STATISTIQUES INTERVENTIONS ===")
print(f"Total: {len(interv_df):,}")
print(f"Colonnes: {list(interv_df.columns)}")

# %%
# Sauvegarder
interv_output = OUTPUT_DIR / "interventions_all.parquet"
interv_df.to_parquet(interv_output, index=False)
print(f"\nSauvegardé: {interv_output}")

# %% [markdown]
# ## 3. Résumé

# %%
print("\n" + "=" * 50)
print("CONSOLIDATION TERMINÉE")
print("=" * 50)
print(f"\nTweets: {len(tweets_df):,}")
print(f"Interventions: {len(interv_df):,}")
print(f"\nFichiers créés:")
print(f"  - {output_file}")
print(f"  - {interv_output}")


