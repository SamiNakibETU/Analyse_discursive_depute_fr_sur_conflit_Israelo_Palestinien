# -*- coding: utf-8 -*-
"""
Génère les CSV d'analyses supplémentaires : fighting_words_temporal, lag_adoption,
movers_caches, pca_coordonnees. À exécuter après les notebooks 01–04 (ou prepare_data).
Utilise uniquement data/results/ et data/processed/ — aucune dépendance externe.
"""

import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import PROCESSED_DIR, RESULTS_DIR, CORPUS_V3, BLOC_ORDER

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def tokenize(text):
    return re.findall(r"[a-zàâäéèêëïîôùûüç]+", str(text).lower())


def log_odds_z(cnt1, cnt2, alpha=0.01):
    """Log-odds ratio avec prior (Monroe et al. 2008)."""
    n1 = sum(cnt1.values()) + alpha * 2
    n2 = sum(cnt2.values()) + alpha * 2
    out = {}
    for w in set(cnt1) | set(cnt2):
        c1 = cnt1.get(w, 0) + alpha
        c2 = cnt2.get(w, 0) + alpha
        delta = np.log(c1 / n1) - np.log(c2 / n2)
        var = 1 / c1 + 1 / c2
        out[w] = delta / np.sqrt(var) if var > 0 else 0
    return out


def main():
    if not CORPUS_V3.exists():
        print(f"Corpus v3 absent : {CORPUS_V3}. Exécuter d'abord les notebooks ou prepare_data.")
        return

    df = pd.read_parquet(CORPUS_V3)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    text_col = "text_clean" if "text_clean" in df.columns else "text"
    df_valid = df[df["bloc"].isin(BLOC_ORDER) & df[text_col].notna()].copy()
    df_valid[text_col] = df_valid[text_col].fillna("").astype(str)

    # 1. Fighting words temporel : Gauche radicale vs Droite, par mois
    fw_rows = []
    for m in sorted(df_valid["month"].unique()):
        sub = df_valid[df_valid["month"] == m]
        g = sub[sub["bloc"] == "Gauche radicale"][text_col]
        d = sub[sub["bloc"] == "Droite"][text_col]
        if len(g) < 10 or len(d) < 10:
            continue
        cnt_g = Counter()
        for t in g.dropna():
            cnt_g.update(tokenize(t))
        cnt_d = Counter()
        for t in d.dropna():
            cnt_d.update(tokenize(t))
        z_scores = log_odds_z(cnt_g, cnt_d)
        for w, z in z_scores.items():
            if abs(z) > 0.5:
                fw_rows.append({"month": m, "word": w, "z": z})
    if fw_rows:
        pd.DataFrame(fw_rows).to_csv(RESULTS_DIR / "fighting_words_temporal.csv", index=False)
        print(f"Écrit : fighting_words_temporal.csv ({len(fw_rows)} lignes)")

    # 2. Lag d'adoption : mois où chaque bloc dépasse 10 % cessez-le-feu
    clf_path = RESULTS_DIR / "ceasefire_lexical.csv"
    if clf_path.exists():
        clf = pd.read_csv(clf_path)
        if "pct" in clf.columns or "pct_ceasefire" in clf.columns:
            pct_col = "pct" if "pct" in clf.columns else "pct_ceasefire"
            month_col = "month" if "month" in clf.columns else clf.columns[0]
            bloc_col = "bloc" if "bloc" in clf.columns else clf.columns[1]
            lag_rows = []
            for bloc in clf[bloc_col].unique():
                b = clf[clf[bloc_col] == bloc].sort_values(month_col)
                first = b[b[pct_col] >= 10].head(1)
                if len(first) > 0:
                    row = first.iloc[0]
                    lag_rows.append({"bloc": bloc, "month_first_10pct": row[month_col], "pct": row[pct_col]})
            if lag_rows:
                pd.DataFrame(lag_rows).to_csv(RESULTS_DIR / "lag_adoption.csv", index=False)
                print("Écrit : lag_adoption.csv")
        else:
            print("ceasefire_lexical.csv : format non reconnu (attendu pct ou pct_ceasefire).")
    else:
        print("ceasefire_lexical.csv absent — exécuter le notebook 04 avant lag_adoption.")

    # 3. Movers : députés avec variation de stance (depuis corpus)
    stance_col = "stance_v3" if "stance_v3" in df_valid.columns else "stance"
    if stance_col in df_valid.columns:
        rng = df_valid.groupby("author")[stance_col].agg(["mean", "min", "max"])
        rng["stance_range"] = rng["max"] - rng["min"]
        movers = rng[rng["stance_range"] > 0].reset_index()
        bloc_map = df_valid.groupby("author")["bloc"].first()
        movers["bloc"] = movers["author"].map(bloc_map)
        movers = movers.rename(columns={"mean": "stance_mean"})[["author", "bloc", "stance_mean", "stance_range"]]
        movers.to_csv(RESULTS_DIR / "movers_caches.csv", index=False)
        print(f"Écrit : movers_caches.csv ({len(movers)} movers)")

    # 4. PCA des députés : TF-IDF agrégé par auteur
    author_texts = df_valid.groupby("author")[text_col].apply(lambda x: " ".join(x.astype(str))).reset_index()
    if len(author_texts) >= 10:
        vec = TfidfVectorizer(max_features=2000, min_df=2, max_df=0.95)
        X = vec.fit_transform(author_texts[text_col])
        n_comp = min(50, X.shape[0] - 1, X.shape[1] - 1)
        pca = PCA(n_components=n_comp, random_state=42)
        coords = pca.fit_transform(X.toarray())
        bloc_map = df_valid.groupby("author")["bloc"].first()
        pca_df = pd.DataFrame({
            "author": author_texts["author"].values,
            "bloc": author_texts["author"].map(bloc_map),
            "PC1": coords[:, 0],
            "PC2": coords[:, 1],
        })
        pca_df.to_csv(RESULTS_DIR / "pca_coordonnees.csv", index=False)
        print(f"Écrit : pca_coordonnees.csv ({len(pca_df)} députés)")


if __name__ == "__main__":
    main()
