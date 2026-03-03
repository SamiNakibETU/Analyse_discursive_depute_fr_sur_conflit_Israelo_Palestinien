# -*- coding: utf-8 -*-
"""
Analyse de réseau des co-mentions et co-occurrences lexicales entre blocs.

Deux graphes produits :
  1. Graphe biparti député–terme (co-occurrence) → clusters discursifs.
  2. Graphe de co-citation : deux députés sont liés s'ils partagent un vocabulaire
     significatif (distance cosinus > seuil).

Usage :
    from src.network_analysis import build_cooccurrence_graph, build_deputy_similarity_graph
    G = build_deputy_similarity_graph(df, stance_col="stance_v3", threshold=0.3)
"""

import numpy as np
import pandas as pd

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


def _require_networkx():
    if not HAS_NETWORKX:
        raise ImportError("networkx est requis : pip install networkx")


def _require_sklearn():
    if not HAS_SKLEARN:
        raise ImportError("scikit-learn est requis : pip install scikit-learn")


# ---------------------------------------------------------------------------
# Graphe de similarité cosinus entre députés
# ---------------------------------------------------------------------------

def build_deputy_similarity_graph(
    df: pd.DataFrame,
    text_col: str = "text",
    author_col: str = "author",
    bloc_col: str = "bloc",
    threshold: float = 0.25,
    max_features: int = 5000,
    min_texts_per_deputy: int = 3,
) -> "nx.Graph":
    """
    Construit un graphe non dirigé où les nœuds sont les députés et les arêtes
    représentent une similarité cosinus TF-IDF > threshold.

    Parameters
    ----------
    df : DataFrame avec colonnes text, author, bloc.
    threshold : seuil de similarité cosinus (0-1). Défaut 0.25.
    max_features : nombre de features TF-IDF.
    min_texts_per_deputy : nombre minimal de textes pour inclure un député.

    Returns
    -------
    networkx.Graph avec attributs de nœud : bloc, n_texts, mean_stance (si disponible).
    """
    _require_networkx()
    _require_sklearn()

    # Agréger les textes par député
    grouped = df.groupby(author_col)[text_col].apply(lambda x: " ".join(x.dropna())).reset_index()
    counts = df.groupby(author_col)[text_col].count().reset_index(name="n_texts")
    grouped = grouped.merge(counts, on=author_col)
    grouped = grouped[grouped["n_texts"] >= min_texts_per_deputy].reset_index(drop=True)

    if grouped.empty:
        return nx.Graph()

    # TF-IDF
    vec = TfidfVectorizer(
        max_features=max_features,
        sublinear_tf=True,
        min_df=2,
        ngram_range=(1, 2),
    )
    tfidf_matrix = vec.fit_transform(grouped[text_col])
    sim_matrix = cosine_similarity(tfidf_matrix)

    # Attributs de nœud
    bloc_map = df.groupby(author_col)[bloc_col].first().to_dict()
    stance_map: dict = {}
    for col in ["stance_v3", "stance_v4"]:  # stance_v3 preferred; v4 used as fallback
        if col in df.columns:
            stance_map = df.groupby(author_col)[col].mean().to_dict()
            break

    G = nx.Graph()
    deputies = grouped[author_col].tolist()

    for i, dep in enumerate(deputies):
        G.add_node(
            dep,
            bloc=bloc_map.get(dep, ""),
            n_texts=int(grouped.loc[i, "n_texts"]),
            mean_stance=float(stance_map.get(dep, float("nan"))),
        )

    # Arêtes
    n = len(deputies)
    for i in range(n):
        for j in range(i + 1, n):
            sim = float(sim_matrix[i, j])
            if sim >= threshold:
                G.add_edge(deputies[i], deputies[j], weight=sim)

    return G


# ---------------------------------------------------------------------------
# Centralité et brokers transpartisans
# ---------------------------------------------------------------------------

def find_transpartisan_brokers(
    G: "nx.Graph",
    bloc_col: str = "bloc",
    top_n: int = 20,
) -> pd.DataFrame:
    """
    Identifie les députés avec la betweenness centrality la plus haute,
    en filtrant ceux qui ont des arêtes vers au moins deux blocs différents
    (brokers transpartisans potentiels).

    Returns
    -------
    DataFrame : author, bloc, betweenness, n_blocs_voisins, voisins_blocs.
    """
    _require_networkx()

    betweenness = nx.betweenness_centrality(G, weight="weight", normalized=True)

    rows = []
    for node, bw in betweenness.items():
        neighbors = list(G.neighbors(node))
        neighbor_blocs = {G.nodes[n].get(bloc_col, "") for n in neighbors if G.nodes[n].get(bloc_col)}
        rows.append({
            "author": node,
            "bloc": G.nodes[node].get(bloc_col, ""),
            "betweenness": bw,
            "n_blocs_voisins": len(neighbor_blocs),
            "voisins_blocs": ", ".join(sorted(neighbor_blocs)),
        })

    result = pd.DataFrame(rows).sort_values("betweenness", ascending=False)
    brokers = result[result["n_blocs_voisins"] >= 2]
    return brokers.head(top_n).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Graphe de co-occurrence terme–terme par bloc
# ---------------------------------------------------------------------------

def build_term_cooccurrence(
    df: pd.DataFrame,
    text_col: str = "text",
    bloc_col: str = "bloc",
    bloc: str = "",
    top_n_terms: int = 50,
    window: int = 5,
) -> "nx.Graph":
    """
    Construit un graphe de co-occurrence de termes pour un bloc donné.
    Deux termes sont liés s'ils apparaissent dans la même fenêtre de `window` mots.

    Returns
    -------
    networkx.Graph pondéré (poids = fréquence de co-occurrence).
    """
    _require_networkx()
    _require_sklearn()

    subset = df[df[bloc_col] == bloc] if bloc else df
    texts = subset[text_col].dropna().tolist()

    # Sélection des top_n_terms par TF-IDF global
    vec = TfidfVectorizer(max_features=top_n_terms, min_df=2)
    vec.fit(texts)
    vocab = set(vec.get_feature_names_out())

    cooc: dict = {}
    for text in texts:
        tokens = [w.lower() for w in str(text).split() if w.lower() in vocab]
        for i, t1 in enumerate(tokens):
            for t2 in tokens[i + 1: i + window]:
                if t1 != t2:
                    pair = tuple(sorted([t1, t2]))
                    cooc[pair] = cooc.get(pair, 0) + 1

    G = nx.Graph()
    for (t1, t2), weight in cooc.items():
        G.add_edge(t1, t2, weight=weight)
    return G


# ---------------------------------------------------------------------------
# Métriques de réseau
# ---------------------------------------------------------------------------

def network_summary(G: "nx.Graph") -> dict:
    """Retourne un dict de métriques de base sur le graphe."""
    _require_networkx()
    if G.number_of_nodes() == 0:
        return {}
    return {
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "density": nx.density(G),
        "avg_clustering": nx.average_clustering(G, weight="weight"),
        "n_components": nx.number_connected_components(G),
    }


def modularity_by_bloc(G: "nx.Graph", bloc_attr: str = "bloc") -> float:
    """
    Calcule la modularité du graphe selon la partition par blocs politiques.
    Retourne NaN si le graphe est vide ou non partitionnable.
    """
    _require_networkx()
    if G.number_of_nodes() == 0:
        return float("nan")
    communities: dict = {}
    for node, data in G.nodes(data=True):
        b = data.get(bloc_attr, "unknown")
        communities.setdefault(b, set()).add(node)
    partition = list(communities.values())
    try:
        return nx.algorithms.community.quality.modularity(G, partition)
    except Exception:
        return float("nan")
