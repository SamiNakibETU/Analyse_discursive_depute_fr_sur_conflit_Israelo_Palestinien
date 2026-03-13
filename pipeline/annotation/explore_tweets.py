# -*- coding: utf-8 -*-
"""Explore tweets structure for RT context."""
import pandas as pd
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_parquet("data/filtered/tweets_gaza.parquet")

# Detecter RT par le texte (commence par RT @)
df["detected_rt"] = df["text"].str.startswith("RT @")
# Detecter replies par @ en debut
df["detected_reply"] = df["text"].str.match(r"^@\w+")

# Stats
print("=== STATISTIQUES ===")
print(f"Total tweets: {len(df)}")
print(f"Retweets (detectes): {df['detected_rt'].sum()} ({100*df['detected_rt'].sum()/len(df):.1f}%)")
print(f"Replies (detectes): {df['detected_reply'].sum()} ({100*df['detected_reply'].sum()/len(df):.1f}%)")
print()

# Exemples de RT
print("=== EXEMPLES DE RETWEETS ===")
rts = df[df["detected_rt"] == True].head(5)
for i, (idx, row) in enumerate(rts.iterrows()):
    print(f"\n--- RT #{i+1} ---")
    print(f"Depute: {row['username']} ({row['groupe_politique']})")
    print(f"Date: {row['date_raw']}")
    print(f"Texte: {row['text']}")
    print(f"URL: {row['url']}")

# Exemples de replies
print("\n\n=== EXEMPLES DE REPLIES ===")
replies = df[df["detected_reply"] == True].head(5)
for i, (idx, row) in enumerate(replies.iterrows()):
    print(f"\n--- Reply #{i+1} ---")
    print(f"Depute: {row['username']} ({row['groupe_politique']})")
    print(f"Date: {row['date_raw']}")
    print(f"Texte: {row['text']}")
    print(f"URL: {row['url']}")

# Exemples de tweets originaux
print("\n\n=== EXEMPLES DE TWEETS ORIGINAUX ===")
originals = df[(df["detected_rt"] == False) & (df["detected_reply"] == False)].head(5)
for i, (idx, row) in enumerate(originals.iterrows()):
    print(f"\n--- Tweet #{i+1} ---")
    print(f"Depute: {row['username']} ({row['groupe_politique']})")
    print(f"Date: {row['date_raw']}")
    print(f"Texte: {row['text']}")
    print(f"URL: {row['url']}")
