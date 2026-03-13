# -*- coding: utf-8 -*-
"""
Topic Modeling ameliore avec BERTopic sur le corpus Gaza.
Avec preprocessing correct et stopwords francais.
"""

import sys
import re
import warnings
from pathlib import Path

import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
warnings.filterwarnings('ignore')

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Stopwords francais etendus
FRENCH_STOPWORDS = set([
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "a", "au", "aux",
    "ce", "cette", "ces", "que", "qui", "quoi", "dont", "ou", "pour", "par", "sur",
    "avec", "sans", "sous", "dans", "entre", "vers", "chez", "plus", "moins", "tres",
    "est", "sont", "etre", "avoir", "fait", "faire", "dit", "dire", "peut", "doit",
    "il", "elle", "ils", "elles", "on", "nous", "vous", "je", "tu", "son", "sa", "ses",
    "leur", "leurs", "notre", "nos", "votre", "vos", "mon", "ma", "mes", "ton", "ta", "tes",
    "ne", "pas", "ni", "mais", "si", "car", "donc", "or", "soit", "comme", "aussi",
    "tout", "tous", "toute", "toutes", "autre", "autres", "meme", "memes",
    "quand", "comment", "pourquoi", "combien", "encore", "toujours", "jamais", "deja",
    "ici", "y", "se", "lui", "eux", "soi", "cela", "ceci", "celle", "ceux",
    "ca", "c", "d", "l", "n", "s", "j", "m", "t", "qu", "jusqu", "lorsqu",
    "quelque", "quelques", "aucun", "aucune", "chaque", "plusieurs", "certains",
    "peu", "beaucoup", "trop", "assez", "bien", "mal", "mieux", "pire",
    "alors", "ainsi", "apres", "avant", "depuis", "pendant", "depuis",
    "fois", "temps", "jour", "jours", "annee", "annees", "an", "ans",
    "faut", "falloir", "vouloir", "pouvoir", "devoir", "savoir", "voir",
    "aller", "venir", "partir", "rester", "mettre", "prendre", "donner",
    "http", "https", "www", "com", "fr", "twitter", "rt", "via"
])


def clean_text(text: str) -> str:
    """Nettoie un texte pour le topic modeling."""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    
    # Supprimer URLs
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    
    # Supprimer mentions Twitter
    text = re.sub(r'@\w+', '', text)
    
    # Supprimer hashtags (garder le mot)
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Supprimer emojis et caracteres speciaux
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Supprimer chiffres seuls
    text = re.sub(r'\b\d+\b', '', text)
    
    # Normaliser espaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Supprimer stopwords
    words = text.split()
    words = [w for w in words if w not in FRENCH_STOPWORDS and len(w) > 2]
    
    return ' '.join(words)


def load_corpus():
    """Charge et prepare le corpus."""
    tweets_file = DATA_DIR / "filtered" / "tweets_gaza.parquet"
    interv_file = DATA_DIR / "filtered" / "interventions_gaza.parquet"
    
    dfs = []
    
    if tweets_file.exists():
        tweets = pd.read_parquet(tweets_file)
        tweets["source"] = "Twitter"
        tweets["text_clean"] = tweets["text"].apply(clean_text)
        
        if "groupe_politique" in tweets.columns:
            tweets["groupe_norm"] = tweets["groupe_politique"]
        else:
            tweets["groupe_norm"] = "Inconnu"
        
        print(f"Tweets charges: {len(tweets)}")
        dfs.append(tweets[["text_clean", "source", "groupe_norm", "username"]].rename(
            columns={"text_clean": "text", "username": "author"}
        ))
    
    if interv_file.exists():
        interv = pd.read_parquet(interv_file)
        interv["source"] = "Assemblee"
        
        text_col = "raw_text" if "raw_text" in interv.columns else "text"
        interv["text_clean"] = interv[text_col].apply(clean_text)
        
        if "matched_group" in interv.columns:
            interv["groupe_norm"] = interv["matched_group"]
        else:
            interv["groupe_norm"] = "Inconnu"
        
        author_col = "speaker_name" if "speaker_name" in interv.columns else "orateur"
        author_data = interv[author_col] if author_col in interv.columns else "Inconnu"
        
        print(f"Interventions chargees: {len(interv)}")
        dfs.append(interv[["text_clean", "source", "groupe_norm"]].rename(
            columns={"text_clean": "text"}
        ).assign(author=author_data))
    
    if not dfs:
        print("ERREUR: Aucun fichier trouve")
        return None
    
    corpus = pd.concat(dfs, ignore_index=True)
    
    # Filtrer textes trop courts apres nettoyage
    corpus = corpus[corpus["text"].str.len() > 30]
    corpus = corpus.dropna(subset=["text"])
    
    print(f"\nCorpus total apres nettoyage: {len(corpus)} documents")
    return corpus


def run_bertopic(corpus: pd.DataFrame, sample_size: int = None):
    """Execute BERTopic avec configuration optimisee."""
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    from umap import UMAP
    from hdbscan import HDBSCAN
    
    texts = corpus["text"].tolist()
    
    if sample_size and len(texts) > sample_size:
        print(f"Echantillonnage stratifie a {sample_size} documents...")
        # Echantillonnage stratifie par groupe
        corpus_sample = corpus.groupby("groupe_norm", group_keys=False).apply(
            lambda x: x.sample(min(len(x), max(10, int(sample_size * len(x) / len(corpus)))), random_state=42)
        )
        if len(corpus_sample) < sample_size:
            remaining = sample_size - len(corpus_sample)
            extra = corpus[~corpus.index.isin(corpus_sample.index)].sample(min(remaining, len(corpus) - len(corpus_sample)), random_state=42)
            corpus_sample = pd.concat([corpus_sample, extra])
        
        corpus = corpus_sample.reset_index(drop=True)
        texts = corpus["text"].tolist()
        print(f"Echantillon final: {len(texts)} documents")
    
    print(f"\nChargement du modele d'embedding...")
    # Modele multilingue plus leger
    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    
    # Vectorizer avec stopwords
    vectorizer = CountVectorizer(
        stop_words=list(FRENCH_STOPWORDS),
        min_df=5,
        max_df=0.95,
        ngram_range=(1, 2)
    )
    
    # UMAP optimise pour la memoire
    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        random_state=42,
        low_memory=True
    )
    
    # HDBSCAN
    hdbscan_model = HDBSCAN(
        min_cluster_size=20,
        min_samples=5,
        metric='euclidean',
        prediction_data=True
    )
    
    print("Extraction des topics...")
    topic_model = BERTopic(
        embedding_model=embedding_model,
        vectorizer_model=vectorizer,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        language="french",
        calculate_probabilities=False,  # Economie memoire
        verbose=True,
        nr_topics="auto",
        top_n_words=10
    )
    
    topics, _ = topic_model.fit_transform(texts)
    
    corpus["topic"] = topics
    
    return topic_model, corpus


def analyze_topics(topic_model, corpus: pd.DataFrame):
    """Analyse et visualise les topics."""
    
    print("\n" + "="*60)
    print("TOPICS IDENTIFIES")
    print("="*60)
    
    topic_info = topic_model.get_topic_info()
    n_topics = len(topic_info[topic_info["Topic"] != -1])
    print(f"\nNombre de topics: {n_topics}")
    print(f"Documents non-assignes (outliers): {topic_info[topic_info['Topic'] == -1]['Count'].sum()}")
    
    print("\n--- TOP TOPICS ---")
    for _, row in topic_info[topic_info["Topic"] != -1].head(15).iterrows():
        words = topic_model.get_topic(row["Topic"])[:7]
        word_str = ", ".join([w[0] for w in words])
        print(f"\nTopic {row['Topic']} ({row['Count']} docs):")
        print(f"  Mots-cles: {word_str}")
    
    # Distribution par groupe politique
    print("\n" + "="*60)
    print("TOPICS PAR GROUPE POLITIQUE")
    print("="*60)
    
    topic_by_group = corpus.groupby(["groupe_norm", "topic"]).size().unstack(fill_value=0)
    
    # Normaliser par groupe
    topic_pct = topic_by_group.div(topic_by_group.sum(axis=1), axis=0) * 100
    
    for group in ["LFI-NFP", "RN", "LR", "EPR", "PS-NFP", "ECO-NFP", "GDR"]:
        if group in topic_pct.index:
            print(f"\n{group}:")
            top_topics = topic_pct.loc[group].sort_values(ascending=False).head(3)
            for topic_id, pct in top_topics.items():
                if topic_id != -1 and pct > 5:
                    words = topic_model.get_topic(topic_id)[:4]
                    if words:
                        word_str = ", ".join([w[0] for w in words])
                        print(f"  Topic {topic_id} ({pct:.1f}%): {word_str}")
    
    # Visualisations
    print("\n" + "="*60)
    print("GENERATION DES VISUALISATIONS")
    print("="*60)
    
    try:
        fig = topic_model.visualize_barchart(top_n_topics=min(15, n_topics), n_words=8)
        fig.write_html(str(OUTPUT_DIR / "topics_barchart_v2.html"))
        print(f"  Sauvegarde: topics_barchart_v2.html")
    except Exception as e:
        print(f"  Barchart: {e}")
    
    try:
        fig = topic_model.visualize_topics()
        fig.write_html(str(OUTPUT_DIR / "topics_intertopic_v2.html"))
        print(f"  Sauvegarde: topics_intertopic_v2.html")
    except Exception as e:
        print(f"  Intertopic: {e}")
    
    try:
        if n_topics > 2:
            fig = topic_model.visualize_hierarchy()
            fig.write_html(str(OUTPUT_DIR / "topics_hierarchy_v2.html"))
            print(f"  Sauvegarde: topics_hierarchy_v2.html")
    except Exception as e:
        print(f"  Hierarchy: {e}")
    
    try:
        # Heatmap topics par groupe
        fig = topic_model.visualize_heatmap()
        fig.write_html(str(OUTPUT_DIR / "topics_heatmap_v2.html"))
        print(f"  Sauvegarde: topics_heatmap_v2.html")
    except Exception as e:
        print(f"  Heatmap: {e}")
    
    # Documents representatifs par topic
    print("\n" + "="*60)
    print("EXEMPLES PAR TOPIC")
    print("="*60)
    
    for topic_id in topic_info[topic_info["Topic"] != -1]["Topic"].head(5):
        docs = corpus[corpus["topic"] == topic_id].head(2)
        words = topic_model.get_topic(topic_id)[:5]
        word_str = ", ".join([w[0] for w in words]) if words else "N/A"
        
        print(f"\n--- Topic {topic_id}: {word_str} ---")
        for _, doc in docs.iterrows():
            text_preview = doc["text"][:150].replace("\n", " ")
            print(f"  [{doc['source']}] {doc.get('author', '?')[:20]}: {text_preview}...")
    
    # Sauvegarder
    corpus.to_parquet(OUTPUT_DIR / "corpus_with_topics_v2.parquet", index=False)
    topic_info.to_csv(OUTPUT_DIR / "topic_info_v2.csv", index=False)
    
    print(f"\nResultats sauvegardes dans {OUTPUT_DIR}/")
    
    return topic_info


def main():
    print("="*60)
    print("TOPIC MODELING V2 - CORPUS GAZA")
    print("="*60)
    
    corpus = load_corpus()
    if corpus is None:
        return
    
    # Echantillon de 3000 docs (bon compromis memoire/qualite)
    SAMPLE_SIZE = 3000
    
    topic_model, corpus_with_topics = run_bertopic(corpus, sample_size=SAMPLE_SIZE)
    
    topic_info = analyze_topics(topic_model, corpus_with_topics)
    
    # Sauvegarder modele
    try:
        topic_model.save(str(OUTPUT_DIR / "bertopic_model_v2"), serialization="safetensors", save_ctfidf=True)
        print(f"\nModele sauvegarde: bertopic_model_v2/")
    except:
        try:
            topic_model.save(str(OUTPUT_DIR / "bertopic_model_v2"))
            print(f"\nModele sauvegarde: bertopic_model_v2")
        except Exception as e:
            print(f"\nErreur sauvegarde modele: {e}")
    
    print("\n" + "="*60)
    print("TOPIC MODELING V2 TERMINE")
    print("="*60)


if __name__ == "__main__":
    main()
