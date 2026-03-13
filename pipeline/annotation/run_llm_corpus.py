# -*- coding: utf-8 -*-
"""
Applique les predictions LLM sur le corpus complet par chunks.
Sauvegarde au fur et a mesure pour ne pas perdre de travail.
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# Charger .env
load_dotenv(Path(__file__).parent.parent / ".env")

sys.stdout.reconfigure(encoding='utf-8')

# Configuration
CHUNK_SIZE = 500  # Nombre de textes par chunk
DELAY_BETWEEN_CALLS = 0.25  # Secondes entre appels API
OUTPUT_DIR = Path("data/annotated/predictions")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STANCE_PROMPT = """Tu es un expert en analyse du discours politique francais sur le conflit Israel-Palestine.

Classifie le positionnement (stance) de ce texte.

Source: {source}
Auteur: {author} ({group})

Texte:
"{text}"

Echelle de stance:
- PRO_ISRAEL (-1): Soutien explicite a Israel, critique du Hamas, defense du droit a se defendre, focus sur le 7 octobre/otages
- NEUTRE (0): Position equilibree, appel a la paix sans blame clair, position institutionnelle, ou sujet hors conflit
- PRO_PALESTINE (1): Critique explicite d'Israel/Netanyahu, soutien aux Palestiniens, termes comme genocide/apartheid/colonisation

Reponds UNIQUEMENT avec un JSON:
{{"stance": -1|0|1, "confidence": "high"|"medium"|"low", "hors_sujet": true|false}}
"""


def classify_batch(client, texts_data: list, source: str) -> list:
    """Classifie un batch de textes."""
    results = []
    
    for item in tqdm(texts_data, desc=f"Chunk {source}", leave=False):
        text = item.get("text", "")
        
        if pd.isna(text) or str(text).strip() == "" or len(str(text)) < 20:
            results.append({
                "stance_llm": None,
                "confidence_llm": "skip",
                "hors_sujet_llm": None
            })
            continue
        
        prompt = STANCE_PROMPT.format(
            text=str(text)[:2000],
            author=item.get("author", "Inconnu"),
            group=item.get("group", "Inconnu"),
            source=source
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un assistant specialise. Reponds uniquement en JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=100
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parser JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            result = json.loads(content)
            results.append({
                "stance_llm": result.get("stance", 0),
                "confidence_llm": result.get("confidence", "low"),
                "hors_sujet_llm": result.get("hors_sujet", False)
            })
            
        except Exception as e:
            results.append({
                "stance_llm": None,
                "confidence_llm": "error",
                "hors_sujet_llm": None
            })
        
        time.sleep(DELAY_BETWEEN_CALLS)
    
    return results


def process_tweets_chunk(chunk_id: int = 0):
    """Traite un chunk de tweets."""
    from openai import OpenAI
    
    tweets_file = Path("data/filtered/tweets_gaza.parquet")
    if not tweets_file.exists():
        print(f"ERREUR: {tweets_file} non trouve")
        return
    
    print(f"Chargement des tweets...")
    df = pd.read_parquet(tweets_file)
    print(f"Total tweets: {len(df)}")
    
    # Calculer les limites du chunk
    start_idx = chunk_id * CHUNK_SIZE
    end_idx = min((chunk_id + 1) * CHUNK_SIZE, len(df))
    
    if start_idx >= len(df):
        print(f"Chunk {chunk_id} depasse la taille du corpus")
        return
    
    print(f"Traitement du chunk {chunk_id}: lignes {start_idx} a {end_idx}")
    
    chunk_df = df.iloc[start_idx:end_idx].copy()
    
    # Preparer les donnees
    texts_data = []
    for _, row in chunk_df.iterrows():
        texts_data.append({
            "text": row.get("text", ""),
            "author": row.get("username", "Inconnu"),
            "group": row.get("groupe_politique", "Inconnu")
        })
    
    # Classifier
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results = classify_batch(client, texts_data, "Twitter")
    
    # Ajouter les resultats
    results_df = pd.DataFrame(results)
    chunk_df = chunk_df.reset_index(drop=True)
    chunk_df = pd.concat([chunk_df, results_df], axis=1)
    
    # Sauvegarder
    output_file = OUTPUT_DIR / f"tweets_chunk_{chunk_id:03d}.parquet"
    chunk_df.to_parquet(output_file, index=False)
    
    # Stats
    print(f"\n=== CHUNK {chunk_id} TERMINE ===")
    print(f"Sauvegarde: {output_file}")
    stance_counts = results_df["stance_llm"].value_counts()
    print(f"Pro-Israel (-1): {stance_counts.get(-1, 0)}")
    print(f"Neutre (0): {stance_counts.get(0, 0)}")
    print(f"Pro-Palestine (1): {stance_counts.get(1, 0)}")
    
    return chunk_df


def process_interventions_chunk(chunk_id: int = 0):
    """Traite un chunk d'interventions AN."""
    from openai import OpenAI
    
    interv_file = Path("data/filtered/interventions_gaza.parquet")
    if not interv_file.exists():
        print(f"ERREUR: {interv_file} non trouve")
        return
    
    print(f"Chargement des interventions...")
    df = pd.read_parquet(interv_file)
    print(f"Total interventions: {len(df)}")
    
    # Calculer les limites du chunk
    start_idx = chunk_id * CHUNK_SIZE
    end_idx = min((chunk_id + 1) * CHUNK_SIZE, len(df))
    
    if start_idx >= len(df):
        print(f"Chunk {chunk_id} depasse la taille du corpus")
        return
    
    print(f"Traitement du chunk {chunk_id}: lignes {start_idx} a {end_idx}")
    
    chunk_df = df.iloc[start_idx:end_idx].copy()
    
    # Trouver la colonne texte
    text_col = "raw_text" if "raw_text" in df.columns else "text"
    
    # Preparer les donnees
    texts_data = []
    for _, row in chunk_df.iterrows():
        texts_data.append({
            "text": row.get(text_col, ""),
            "author": row.get("speaker_name", "Inconnu"),
            "group": row.get("matched_group", "Inconnu")
        })
    
    # Classifier
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results = classify_batch(client, texts_data, "Assemblee")
    
    # Ajouter les resultats
    results_df = pd.DataFrame(results)
    chunk_df = chunk_df.reset_index(drop=True)
    chunk_df = pd.concat([chunk_df, results_df], axis=1)
    
    # Sauvegarder
    output_file = OUTPUT_DIR / f"interventions_chunk_{chunk_id:03d}.parquet"
    chunk_df.to_parquet(output_file, index=False)
    
    # Stats
    print(f"\n=== CHUNK {chunk_id} TERMINE ===")
    print(f"Sauvegarde: {output_file}")
    stance_counts = results_df["stance_llm"].value_counts()
    print(f"Pro-Israel (-1): {stance_counts.get(-1, 0)}")
    print(f"Neutre (0): {stance_counts.get(0, 0)}")
    print(f"Pro-Palestine (1): {stance_counts.get(1, 0)}")
    
    return chunk_df


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM predictions sur corpus")
    parser.add_argument("--source", choices=["tweets", "interventions", "both"], default="tweets")
    parser.add_argument("--chunk", type=int, default=0, help="Numero du chunk a traiter")
    
    args = parser.parse_args()
    
    print("="*60)
    print(f"PREDICTIONS LLM - {args.source.upper()} - CHUNK {args.chunk}")
    print(f"Debut: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    if args.source in ["tweets", "both"]:
        process_tweets_chunk(args.chunk)
    
    if args.source in ["interventions", "both"]:
        process_interventions_chunk(args.chunk)
    
    print(f"\nFin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
