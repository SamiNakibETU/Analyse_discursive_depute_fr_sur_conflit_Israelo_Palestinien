# -*- coding: utf-8 -*-
"""
Topic modeling inductif avec BERTopic (CamemBERT embeddings pour le français).

Produit des topics *émergents* non définis a priori, complémentaires aux cadres
HUM/SEC/LEG… annotés par LLM.

Usage :
    from src.topic_modeling import fit_topics, topics_by_bloc, topics_over_time

Dépendances optionnelles (non incluses dans requirements.txt de base) :
    pip install bertopic>=0.16 umap-learn>=0.5 hdbscan>=0.8

Si BERTopic n'est pas disponible, le module propose un fallback LDA léger via
sklearn.decomposition.LatentDirichletAllocation.
"""

import numpy as np
import pandas as pd

try:
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    HAS_BERTOPIC = True
except ImportError:
    HAS_BERTOPIC = False

try:
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.feature_extraction.text import CountVectorizer
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# ---------------------------------------------------------------------------
# BERTopic (modèle préféré)
# ---------------------------------------------------------------------------

# Modèle multilingue par défaut : compatible French sans téléchargement supplémentaire.
# Alternative French-only : "camembert-base" (meilleure qualité, téléchargement >400 MB).
DEFAULT_EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def fit_topics(
    texts: list,
    n_topics: int = 20,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    language: str = "french",
    seed: int = 42,
) -> tuple:
    """
    Ajuste un modèle BERTopic sur la liste de textes.

    Parameters
    ----------
    texts : liste de chaînes de caractères.
    n_topics : nombre cible de topics (BERTopic utilise nr_topics pour fusionner).
    embedding_model : identifiant HuggingFace pour les embeddings.
    language : langue pour le vectorizer de représentation.
    seed : graine pour la reproductibilité (umap).

    Returns
    -------
    (topic_model, topics, probs) :
        - topic_model : instance BERTopic ajustée.
        - topics : liste d'entiers (topic assigné à chaque texte).
        - probs : matrice de probabilités (n_textes, n_topics).

    Raises
    ------
    ImportError si BERTopic n'est pas installé.
    """
    if not HAS_BERTOPIC:
        raise ImportError(
            "BERTopic est requis : pip install bertopic>=0.16 umap-learn>=0.5 hdbscan>=0.8"
        )

    try:
        from umap import UMAP
        from hdbscan import HDBSCAN
        umap_model = UMAP(
            n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric="cosine",
            random_state=seed,
        )
        hdbscan_model = HDBSCAN(
            min_cluster_size=10,
            metric="euclidean",
            cluster_selection_method="eom",
            prediction_data=True,
        )
    except ImportError:
        umap_model = None
        hdbscan_model = None

    embedding_model_obj = SentenceTransformer(embedding_model)

    topic_model = BERTopic(
        embedding_model=embedding_model_obj,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        language=language,
        nr_topics=n_topics,
        verbose=False,
        calculate_probabilities=True,
    )

    topics, probs = topic_model.fit_transform(texts)
    return topic_model, topics, probs


def topics_by_bloc(
    df: pd.DataFrame,
    topic_model,
    topics: list,
    bloc_col: str = "bloc",
) -> pd.DataFrame:
    """
    Calcule la distribution des topics par bloc politique.

    Returns
    -------
    DataFrame pivot : blocs en lignes, topics en colonnes, valeurs = proportions.
    """
    df = df.copy()
    df["topic"] = topics

    pivot = (
        df.groupby([bloc_col, "topic"])
        .size()
        .reset_index(name="count")
    )
    pivot_wide = pivot.pivot(index=bloc_col, columns="topic", values="count").fillna(0)
    # Normaliser par ligne
    pivot_wide = pivot_wide.div(pivot_wide.sum(axis=1), axis=0)
    return pivot_wide


def topics_over_time(
    df: pd.DataFrame,
    topic_model,
    topics: list,
    timestamps_col: str = "date",
    nr_bins: int = 20,
) -> pd.DataFrame:
    """
    Calcule l'évolution temporelle des topics (fréquence par période).

    Returns
    -------
    DataFrame : timestamp, topic, frequency (compatible BERTopic.visualize_topics_over_time).
    """
    if not HAS_BERTOPIC:
        raise ImportError("BERTopic est requis.")

    texts = df["text"].fillna("").tolist()
    timestamps = df[timestamps_col].tolist()
    tot = topic_model.topics_over_time(texts, timestamps=timestamps, nr_bins=nr_bins)
    return tot


def top_words_per_topic(topic_model, n_words: int = 10) -> dict:
    """
    Retourne un dict {topic_id: [(mot, score), ...]} pour les n_words principaux.
    """
    if not HAS_BERTOPIC:
        raise ImportError("BERTopic est requis.")
    info = topic_model.get_topics()
    return {
        topic_id: [(w, round(s, 4)) for w, s in words[:n_words]]
        for topic_id, words in info.items()
        if topic_id != -1
    }


# ---------------------------------------------------------------------------
# Fallback LDA (si BERTopic non disponible)
# ---------------------------------------------------------------------------

def fit_lda(
    texts: list,
    n_topics: int = 15,
    max_features: int = 3000,
    max_iter: int = 20,
    seed: int = 42,
) -> tuple:
    """
    Ajuste un modèle LDA (sklearn) comme alternative légère à BERTopic.

    Returns
    -------
    (lda_model, vectorizer, doc_topic_matrix) :
        - lda_model : LatentDirichletAllocation ajusté.
        - vectorizer : CountVectorizer ajusté.
        - doc_topic_matrix : ndarray (n_docs, n_topics).

    Raises
    ------
    ImportError si scikit-learn n'est pas installé.
    """
    if not HAS_SKLEARN:
        raise ImportError("scikit-learn est requis : pip install scikit-learn")

    vectorizer = CountVectorizer(
        max_features=max_features,
        min_df=3,
        max_df=0.95,
        ngram_range=(1, 2),
        stop_words=_french_stopwords(),
    )
    dtm = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        max_iter=max_iter,
        learning_method="online",
        random_state=seed,
        n_jobs=-1,
    )
    doc_topic = lda.fit_transform(dtm)
    return lda, vectorizer, doc_topic


def lda_top_words(lda_model, vectorizer, n_words: int = 10) -> dict:
    """
    Retourne {topic_id: [mot1, mot2, ...]} pour les n_words principaux de chaque topic LDA.
    """
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    for idx, component in enumerate(lda_model.components_):
        top_indices = component.argsort()[-n_words:][::-1]  # top n_words in descending order
        topics[idx] = [feature_names[i] for i in top_indices]
    return topics


def assign_dominant_topic(doc_topic_matrix: np.ndarray) -> np.ndarray:
    """Retourne le topic dominant (argmax) pour chaque document."""
    return np.argmax(doc_topic_matrix, axis=1)


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def _french_stopwords() -> list:
    """Liste minimale de stop-words français pour LDA."""
    return [
        "le", "la", "les", "de", "du", "des", "un", "une", "et", "en",
        "à", "au", "aux", "est", "sont", "ont", "nous", "vous", "ils",
        "elles", "ce", "se", "sa", "son", "ses", "cette", "ces", "par",
        "pour", "sur", "dans", "avec", "que", "qui", "quoi", "dont",
        "ou", "si", "mais", "donc", "or", "ni", "car", "pas", "plus",
        "très", "bien", "aussi", "même", "encore", "tout", "tous",
        "toute", "toutes", "leur", "leurs", "comme", "je", "il", "elle",
        "on", "mon", "ton", "http", "https", "co", "rt",
    ]
