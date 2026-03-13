# -*- coding: utf-8 -*-
"""
Topic Modeling avec BERTopic sur le corpus Gaza.
Analyse non-supervisee pour identifier les themes et frames.
"""

import sys
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('ignore')

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_corpus():
    """Charge les tweets et interventions filtres."""
    tweets_file = DATA_DIR / "filtered" / "tweets_gaza.parquet"
    interv_file = DATA_DIR / "filtered" / "interventions_gaza.parquet"
    
    dfs = []
    
    if tweets_file.exists():
        tweets = pd.read_parquet(tweets_file)
        tweets["source"] = "Twitter"
        tweets["text_col"] = tweets["text"]
        # Normaliser le nom de colonne groupe
        if "groupe_politique" in tweets.columns:
            tweets["groupe_norm"] = tweets["groupe_politique"]
        elif "groupe_norm" not in tweets.columns:
            tweets["groupe_norm"] = "Inconnu"
        print(f"Tweets charges: {len(tweets)}")
        dfs.append(tweets[["text_col", "source", "groupe_norm", "username"]].rename(columns={"text_col": "text", "username": "author"}))
    
    if interv_file.exists():
        interv = pd.read_parquet(interv_file)
        interv["source"] = "Assemblee"
        # Trouver la colonne texte (differents formats possibles)
        text_candidates = ["text", "intervention_text", "raw_text", "normalized_text"]
        text_col = None
        for col in text_candidates:
            if col in interv.columns:
                text_col = col
                break
        if text_col is None:
            print(f"ERREUR: Pas de colonne texte trouvee. Colonnes: {interv.columns.tolist()}")
            return None
        
        interv["text_col"] = interv[text_col]
        print(f"Interventions chargees: {len(interv)} (colonne texte: {text_col})")
        
        # Normaliser groupe
        if "matched_group" in interv.columns:
            interv["groupe_norm"] = interv["matched_group"]
        elif "groupe_norm" not in interv.columns:
            interv["groupe_norm"] = "Inconnu"
        
        author_col = "speaker_name" if "speaker_name" in interv.columns else "orateur"
        author_data = interv[author_col] if author_col in interv.columns else "Inconnu"
        dfs.append(interv[["text_col", "source", "groupe_norm"]].rename(columns={"text_col": "text"}).assign(author=author_data))
    
    if not dfs:
        print("ERREUR: Aucun fichier trouve")
        return None
    
    corpus = pd.concat(dfs, ignore_index=True)
    corpus = corpus.dropna(subset=["text"])
    corpus = corpus[corpus["text"].str.len() > 50]  # Filtrer textes trop courts
    
    print(f"\nCorpus total: {len(corpus)} documents")
    return corpus


def run_bertopic(corpus: pd.DataFrame, sample_size: int = None):
    """Execute BERTopic sur le corpus."""
    try:
        from bertopic import BERTopic
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Installation des dependances...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "bertopic", "sentence-transformers", "-q"])
        from bertopic import BERTopic
        from sentence_transformers import SentenceTransformer
    
    texts = corpus["text"].tolist()
    
    if sample_size and len(texts) > sample_size:
        print(f"Echantillonnage a {sample_size} documents...")
        indices = np.random.choice(len(texts), sample_size, replace=False)
        texts = [texts[i] for i in indices]
        corpus = corpus.iloc[indices].reset_index(drop=True)
    
    print(f"\nChargement du modele d'embedding...")
    # Utiliser un modele francais ou multilingue
    try:
        embedding_model = SentenceTransformer("dangvantuan/sentence-camembert-base")
    except:
        embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    
    print("Extraction des topics (peut prendre quelques minutes)...")
    topic_model = BERTopic(
        embedding_model=embedding_model,
        language="french",
        calculate_probabilities=True,
        verbose=True,
        nr_topics="auto",  # Reduire automatiquement
        min_topic_size=15
    )
    
    topics, probs = topic_model.fit_transform(texts)
    
    # Ajouter les topics au corpus
    corpus["topic"] = topics
    corpus["topic_prob"] = probs.max(axis=1) if probs.ndim > 1 else probs
    
    return topic_model, corpus


def analyze_topics(topic_model, corpus: pd.DataFrame):
    """Analyse et visualise les topics."""
    
    # 1. Info sur les topics
    print("\n" + "="*60)
    print("TOPICS IDENTIFIES")
    print("="*60)
    
    topic_info = topic_model.get_topic_info()
    print(f"\nNombre de topics: {len(topic_info) - 1}")  # -1 pour exclure le topic -1 (outliers)
    
    print("\nTop 10 topics:")
    for _, row in topic_info.head(11).iterrows():
        if row["Topic"] != -1:
            words = topic_model.get_topic(row["Topic"])[:5]
            word_str = ", ".join([w[0] for w in words])
            print(f"  Topic {row['Topic']} ({row['Count']} docs): {word_str}")
    
    # 2. Distribution par groupe politique
    print("\n" + "="*60)
    print("DISTRIBUTION PAR GROUPE POLITIQUE")
    print("="*60)
    
    topic_by_group = corpus.groupby(["groupe_norm", "topic"]).size().unstack(fill_value=0)
    
    # Top 5 topics par groupe
    for group in corpus["groupe_norm"].unique():
        if group in topic_by_group.index:
            group_topics = topic_by_group.loc[group].sort_values(ascending=False).head(3)
            print(f"\n{group}:")
            for topic_id, count in group_topics.items():
                if topic_id != -1 and count > 5:
                    words = topic_model.get_topic(topic_id)[:3]
                    word_str = ", ".join([w[0] for w in words]) if words else "N/A"
                    print(f"  Topic {topic_id} ({count}): {word_str}")
    
    # 3. Visualisations
    print("\nGeneration des visualisations...")
    
    # Barchart des topics
    fig = topic_model.visualize_barchart(top_n_topics=10)
    fig.write_html(str(OUTPUT_DIR / "topics_barchart.html"))
    print(f"  Sauvegarde: {OUTPUT_DIR / 'topics_barchart.html'}")
    
    # Hierarchie des topics
    try:
        fig = topic_model.visualize_hierarchy()
        fig.write_html(str(OUTPUT_DIR / "topics_hierarchy.html"))
        print(f"  Sauvegarde: {OUTPUT_DIR / 'topics_hierarchy.html'}")
    except Exception as e:
        print(f"  Hierarchie non generee: {e}")
    
    # Heatmap topics x groupes
    try:
        fig = topic_model.visualize_heatmap()
        fig.write_html(str(OUTPUT_DIR / "topics_heatmap.html"))
        print(f"  Sauvegarde: {OUTPUT_DIR / 'topics_heatmap.html'}")
    except Exception as e:
        print(f"  Heatmap non generee: {e}")
    
    # 4. Sauvegarder les resultats
    corpus.to_parquet(OUTPUT_DIR / "corpus_with_topics.parquet", index=False)
    topic_info.to_csv(OUTPUT_DIR / "topic_info.csv", index=False)
    
    print(f"\nResultats sauvegardes dans {OUTPUT_DIR}/")
    
    return topic_info


def main():
    print("="*60)
    print("TOPIC MODELING - CORPUS GAZA")
    print("="*60)
    
    # Charger le corpus
    corpus = load_corpus()
    if corpus is None:
        return
    
    # Limiter pour le premier run (eviter les timeouts et problemes de RAM)
    SAMPLE_SIZE = 1000  # Encore reduit pour eviter les erreurs de memoire Windows
    
    # BERTopic
    topic_model, corpus_with_topics = run_bertopic(corpus, sample_size=SAMPLE_SIZE)
    
    # Analyse
    topic_info = analyze_topics(topic_model, corpus_with_topics)
    
    # Sauvegarder le modele
    topic_model.save(str(OUTPUT_DIR / "bertopic_model"))
    print(f"\nModele sauvegarde: {OUTPUT_DIR / 'bertopic_model'}")
    
    print("\n" + "="*60)
    print("TOPIC MODELING TERMINE")
    print("="*60)


if __name__ == "__main__":
    main()
