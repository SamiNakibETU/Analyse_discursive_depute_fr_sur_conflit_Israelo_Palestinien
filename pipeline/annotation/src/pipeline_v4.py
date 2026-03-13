# -*- coding: utf-8 -*-
"""
Pipeline v4 — Corrections méthodologiques (A1, B4), analyses NLP, visualisations
"""

import re
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats
from scipy.spatial.distance import cosine as cosine_dist
from scipy.stats import kendalltau, spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer

# =============================================================================
# CONFIG
# =============================================================================

BLOCS = {
    "Gauche radicale": ["LFI-NFP", "LFI", "GDR"],
    "Gauche moderee": ["SOC", "PS-NFP", "ECO", "ECO-NFP"],
    "Centre / Majorite": ["REN", "MODEM", "HOR", "EPR", "DEM"],
    "Droite": ["LR", "RN", "UDR", "NI"],
}
GROUP_TO_BLOC = {g: b for b, gs in BLOCS.items() for g in gs}
BLOC_ORDER = list(BLOCS.keys())

COLORS = {
    "Gauche radicale": "#c0392b",
    "Gauche moderee": "#e74c3c",
    "Centre / Majorite": "#f39c12",
    "Droite": "#2c3e50",
}

EVENTS = {
    "2023-10-07": "7 octobre",
    "2024-01-26": "Ordonnance CIJ",
    "2024-05-20": "Mandat CPI requis",
    "2024-05-28": "Massacre Rafah",
    "2024-06-09": "Dissolution AN",
    "2024-10-16": "Mort Sinwar",
    "2024-11-21": "Mandats CPI émis",
    "2025-01-19": "Cessez-le-feu",
    "2025-03-15": "Rupture cessez-le-feu",
    "2025-05-06": "Discours Barrot AN",
}
EVENTS_DT = {pd.Timestamp(k): v for k, v in EVENTS.items()}

STOPWORDS_FR = set([
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "a", "au",
    "aux", "ce", "ces", "cette", "il", "elle", "ils", "elles", "on", "nous",
    "vous", "je", "tu", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa",
    "ses", "notre", "nos", "votre", "vos", "leur", "leurs", "qui", "que",
    "quoi", "dont", "ou", "mais", "donc", "car", "ni", "ne", "pas",
    "plus", "tres", "bien", "tout", "tous", "toute", "toutes", "meme",
    "aussi", "comme", "avec", "pour", "sur", "dans", "par", "sans", "sous",
])


def clean_text(text):
    if pd.isna(text):
        return ""
    t = str(text).lower()
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"@\w+", "", t)
    t = re.sub(r"#(\w+)", r"\1", t)
    t = re.sub(r"[^\w\s\u00e0\u00e2\u00e4\u00e9\u00e8\u00ea\u00eb\u00ef\u00ee\u00f4\u00f9\u00fb\u00fc\u00ff\u00e7\u0153\u00e6-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def tokenize(text):
    words = clean_text(text).split()
    return [w for w in words if w not in STOPWORDS_FR and len(w) >= 3]


# =============================================================================
# FIX A1 — Score lexical SANS circularité (ancre = bloc uniquement)
# =============================================================================

def compute_lexical_score_fixed(df_post: pd.DataFrame) -> pd.DataFrame:
    """
    Recalcule le score lexical en utilisant UNIQUEMENT le bloc comme ancre.
    AVANT (circulaire): anchors_pro_pal = df[(bloc=="Gauche radicale") & (stance_v3>=1)]
    APRÈS (corrigé): anchors_pro_pal = df[bloc=="Gauche radicale"]
    """
    df = df_post.copy()
    if "text_tokens" not in df.columns:
        df["text_tokens"] = df["text_clean"].apply(tokenize)

    # Ancres par bloc uniquement (PAS de filtre stance_v3)
    anchor_pal = df[df["bloc"] == "Gauche radicale"]["text_tokens"].tolist()
    anchor_isr = df[df["bloc"] == "Droite"]["text_tokens"].tolist()

    counts_pal = Counter(w for doc in anchor_pal for w in doc)
    counts_isr = Counter(w for doc in anchor_isr for w in doc)
    total_pal = sum(counts_pal.values())
    total_isr = sum(counts_isr.values())

    all_words = set(counts_pal.keys()) | set(counts_isr.keys())
    word_scores = {}
    for w in all_words:
        total_w = counts_pal.get(w, 0) + counts_isr.get(w, 0)
        if total_w < 10:
            continue
        freq_pal = counts_pal.get(w, 0) / total_pal
        freq_isr = counts_isr.get(w, 0) / total_isr
        denom = freq_pal + freq_isr
        if denom > 0:
            word_scores[w] = (freq_pal - freq_isr) / denom

    def lexical_score(tokens):
        scores = [word_scores[w] for w in tokens if w in word_scores]
        if not scores:
            return np.nan
        return np.mean(scores)

    df["score_lexical_fixed_raw"] = df["text_tokens"].apply(lexical_score)
    valid = df["score_lexical_fixed_raw"].notna()
    if valid.sum() > 0:
        raw = df.loc[valid, "score_lexical_fixed_raw"]
        rng = raw.max() - raw.min()
        if rng > 0:
            df.loc[valid, "score_lexical_fixed"] = (raw - raw.min()) / rng * 4 - 2
        else:
            df.loc[valid, "score_lexical_fixed"] = 0
    else:
        df["score_lexical_fixed"] = np.nan

    return df, word_scores


# =============================================================================
# FIX B4 — Panel fixe (députés actifs ≥1 tweet/mois pendant toute la période POST)
# =============================================================================

def get_panel_fixe(df_post: pd.DataFrame) -> pd.DataFrame:
    """Identifie les députés actifs en continu (≥1 texte/mois sur toute la période POST)."""
    months = df_post["month"].dropna().unique()
    n_months = len(months)
    if n_months == 0:
        return pd.DataFrame()

    dep_month_counts = df_post.groupby(["author", "month"]).size().reset_index(name="n")
    dep_tot_months = dep_month_counts.groupby("author")["month"].nunique()
    panel_fixe = dep_tot_months[dep_tot_months >= n_months * 0.9].index.tolist()
    return df_post[df_post["author"].isin(panel_fixe)].copy()


def compute_polarization_panel_fixe(df_panel: pd.DataFrame) -> tuple:
    """Recalcule la distance cosinus mensuelle entre blocs sur le panel fixe."""
    months = sorted(df_panel["month"].dropna().unique())
    pair_distances = {}
    for i in range(len(BLOC_ORDER)):
        for j in range(i + 1, len(BLOC_ORDER)):
            key = f"{BLOC_ORDER[i][:3]}-{BLOC_ORDER[j][:3]}"
            pair_distances[key] = []

    month_list = []
    for month in months:
        sub = df_panel[df_panel["month"] == month]
        if len(sub) < 20:
            continue
        bloc_texts = {}
        for bloc in BLOC_ORDER:
            texts = sub[sub["bloc"] == bloc]["text_clean"].apply(clean_text).tolist()
            bloc_texts[bloc] = " ".join(texts) if texts else ""
        if any(len(t.split()) < 10 for t in bloc_texts.values()):
            continue
        month_list.append(month)
        tfidf = TfidfVectorizer(max_features=2000, stop_words=list(STOPWORDS_FR))
        try:
            vecs = tfidf.fit_transform([bloc_texts[b] for b in BLOC_ORDER]).toarray()
        except ValueError:
            continue
        for i in range(len(BLOC_ORDER)):
            for j in range(i + 1, len(BLOC_ORDER)):
                key = f"{BLOC_ORDER[i][:3]}-{BLOC_ORDER[j][:3]}"
                d = cosine_dist(vecs[i], vecs[j]) if np.linalg.norm(vecs[i]) > 0 and np.linalg.norm(vecs[j]) > 0 else np.nan
                pair_distances[key].append(d)

    min_len = min(len(v) for v in pair_distances.values()) if pair_distances else 0
    month_list = month_list[:min_len]
    for k in pair_distances:
        pair_distances[k] = pair_distances[k][:min_len]
    global_pol = np.nanmean([pair_distances[k] for k in pair_distances], axis=0) if pair_distances else np.array([])
    return month_list, pair_distances, global_pol


# =============================================================================
# FIGHTIN' WORDS TEMPOREL (CHOC vs RESOL)
# =============================================================================

def fightin_words(corpus_a, corpus_b, alpha_prior=0.01, min_count=5):
    """Fightin' Words (Monroe et al. 2008) avec prior Dirichlet."""
    counts_a = Counter(w for doc in corpus_a for w in doc)
    counts_b = Counter(w for doc in corpus_b for w in doc)
    vocab = set(k for k, v in (counts_a + counts_b).items() if v >= min_count)
    n_a = sum(counts_a[w] for w in vocab)
    n_b = sum(counts_b[w] for w in vocab)
    V = len(vocab)
    alpha_w = alpha_prior
    alpha_0 = V * alpha_w
    results = []
    for w in vocab:
        y_a = counts_a[w]
        y_b = counts_b[w]
        log_odds = (
            np.log((y_a + alpha_w) / (n_a + alpha_0 - y_a - alpha_w))
            - np.log((y_b + alpha_w) / (n_b + alpha_0 - y_b - alpha_w))
        )
        var = (1 / (y_a + alpha_w)) + (1 / (y_b + alpha_w))
        z_score = log_odds / np.sqrt(var)
        results.append({"word": w, "z_score": z_score, "log_odds": log_odds})
    return pd.DataFrame(results).sort_values("z_score", ascending=False)


# =============================================================================
# FEEL EMOTION LEXICON (simplifié français)
# =============================================================================

FEEL_SIMPLIFIED = {
    "anger": ["colère", "fureur", "honte", "scandale", "indigne", "indignation", "révolte", "révoltant", "outrage", "outrageant"],
    "fear": ["menace", "danger", "terrorisme", "terroriste", "sécurité", "peur", "crainte", "inquiétude", "inquiétant"],
    "sadness": ["tristesse", "deuil", "douleur", "souffrance", "compassion", "victimes", "mort", "morts", "mourir"],
    "trust": ["paix", "dialogue", "négociation", "accord", "confiance"],
    "disgust": ["horreur", "atrocité", "barbarie", "monstrueux"],
}


def compute_feel_proportions(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule la proportion de mots par émotion par bloc × mois."""
    rows = []
    for _, row in df.iterrows():
        text_low = clean_text(row["text_clean"])
        words = text_low.split()
        total = max(len(words), 1)
        bloc = row["bloc"]
        month = row["month"]
        for emotion, terms in FEEL_SIMPLIFIED.items():
            count = sum(1 for w in words if any(t in w for t in terms))
            rows.append({"bloc": bloc, "month": month, "emotion": emotion, "pct": count / total * 100})
    return pd.DataFrame(rows).groupby(["bloc", "month", "emotion"])["pct"].mean().reset_index()


# =============================================================================
# CONTAGION LEXICALE CESSEZ-LE-FEU
# =============================================================================

CEASEFIRE_TERMS = ["cessez-le-feu", "cessez le feu", "ceasefire", "trêve", "trêve humanitaire"]


def has_ceasefire_term(text: str) -> bool:
    t = clean_text(str(text))
    return any(term in t for term in CEASEFIRE_TERMS)


# =============================================================================
# VISUALISATIONS
# =============================================================================

def add_events_to_ax(ax, fontsize=7, rotation=90):
    ymin, ymax = ax.get_ylim()
    y_pos = ymax - 0.05 * (ymax - ymin)
    for dt, label in EVENTS_DT.items():
        ax.axvline(dt, color="#888", ls="--", lw=0.7, alpha=0.5, zorder=1)
        ax.text(dt, y_pos, f"  {label}", rotation=rotation, fontsize=fontsize, va="top", ha="left", color="#666", style="italic")


def setup_plot_style():
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 150,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def plot_ceasefire_adoption(df_v4: pd.DataFrame, output_path: Path):
    """Courbe d'adoption du cessez-le-feu par bloc × mois."""
    setup_plot_style()
    df = df_v4[df_v4["ceasefire_call"].notna()].copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.start_time
    monthly = df.groupby(["bloc", "month"]).agg(
        n_ceasefire=("ceasefire_call", "sum"),
        n_total=("ceasefire_call", "count"),
    ).reset_index()
    monthly["pct"] = monthly["n_ceasefire"] / monthly["n_total"] * 100

    fig, ax = plt.subplots(figsize=(14, 7))
    for bloc in BLOC_ORDER:
        sub = monthly[monthly["bloc"] == bloc].sort_values("month")
        if not sub.empty:
            ax.plot(sub["month"], sub["pct"], color=COLORS[bloc], lw=2, label=bloc, marker="o", markersize=4)
    add_events_to_ax(ax)
    ax.set_xlabel("Mois")
    ax.set_ylabel("% de textes avec appel au cessez-le-feu")
    ax.set_title("Courbe d'adoption du cessez-le-feu par bloc (v4)")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_conditionality_heatmap(df_v4: pd.DataFrame, output_path: Path):
    """Heatmap conditionality × bloc × phase."""
    setup_plot_style()
    df = df_v4.copy()
    df["date_dt"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date_dt"].notna()]
    df["month_num"] = df["date_dt"].dt.year * 12 + df["date_dt"].dt.month
    if df.empty or df["month_num"].nunique() < 2:
        return
    q = pd.qcut(df["month_num"], q=6, labels=["P1", "P2", "P3", "P4", "P5", "P6"], duplicates="drop")
    df["phase"] = q
    cond = df[df["conditionality"].notna()].groupby(["bloc", "phase"]).apply(
        lambda x: (x["conditionality"] == "conditional").mean() * 100
    ).reset_index(name="pct_conditional")
    piv = cond.pivot_table(index="bloc", columns="phase", values="pct_conditional")
    piv = piv.reindex(index=BLOC_ORDER)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(piv, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, cbar_kws={"label": "% conditional"})
    ax.set_title("Carte de la conditionnalité (% conditional par bloc × phase)")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_emotional_register(df_v4: pd.DataFrame, output_path: Path):
    """Stacked bar: distribution emotional_register par bloc × phase."""
    setup_plot_style()
    df = df_v4[df_v4["emotional_register"].notna()].copy()
    df["date_dt"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date_dt"].notna()]
    df["phase"] = df["date_dt"].dt.to_period("Q").astype(str)
    if df.empty:
        return
    cross = pd.crosstab(
        [df["bloc"], df["phase"]],
        df["emotional_register"],
        normalize="index",
    ).mul(100)
    fig, ax = plt.subplots(figsize=(14, 7))
    cross.plot(kind="bar", stacked=True, ax=ax, colormap="tab10", width=0.8)
    ax.set_xlabel("Bloc × Phase")
    ax.set_ylabel("%")
    ax.set_title("Registre émotionnel par bloc et phase")
    ax.legend(title="Registre", bbox_to_anchor=(1.02, 1))
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_ceasefire_lexical_contagion(df: pd.DataFrame, output_path: Path):
    """Line chart: % de textes contenant 'cessez-le-feu' par bloc × mois."""
    setup_plot_style()
    df = df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.start_time
    df["has_ceasefire"] = df["text_clean"].apply(has_ceasefire_term)
    monthly = df.groupby(["bloc", "month"]).agg(
        pct=("has_ceasefire", "mean"),
        n=("has_ceasefire", "count"),
    ).reset_index()
    monthly["pct"] *= 100

    fig, ax = plt.subplots(figsize=(14, 7))
    for bloc in BLOC_ORDER:
        sub = monthly[monthly["bloc"] == bloc].sort_values("month")
        if not sub.empty and sub["n"].sum() >= 5:
            ax.plot(sub["month"], sub["pct"], color=COLORS[bloc], lw=2, label=bloc, marker="o", markersize=4)
    add_events_to_ax(ax)
    ax.set_xlabel("Mois")
    ax.set_ylabel("% de textes contenant 'cessez-le-feu' / 'trêve'")
    ax.set_title("Contagion lexicale du cessez-le-feu par bloc")
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_event_study(df_v4: pd.DataFrame, output_path: Path, window_days: int = 14):
    """Event study : stance/ceasefire avant vs après chaque événement pivot."""
    setup_plot_style()
    events = [
        ("2024-01-26", "CIJ"),
        ("2024-05-28", "Rafah"),
        ("2024-10-16", "Sinwar"),
        ("2024-11-21", "CPI"),
        ("2025-01-19", "Cessez-le-feu"),
    ]
    df = df_v4.copy()
    df["date_dt"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date_dt"].notna() & df["stance_v4"].notna()]
    if df.empty:
        return
    rows = []
    for ev_date, ev_name in events:
        ev = pd.Timestamp(ev_date)
        before = df[(df["date_dt"] >= ev - pd.Timedelta(days=window_days)) & (df["date_dt"] < ev)]
        after = df[(df["date_dt"] >= ev) & (df["date_dt"] < ev + pd.Timedelta(days=window_days))]
        for bloc in BLOC_ORDER:
            b_before = before[before["bloc"] == bloc]
            b_after = after[after["bloc"] == bloc]
            stance_before = b_before["stance_v4"].mean() if len(b_before) > 0 else np.nan
            stance_after = b_after["stance_v4"].mean() if len(b_after) > 0 else np.nan
            cf_before = b_before["ceasefire_call"].mean() * 100 if len(b_before) > 0 and "ceasefire_call" in b_before else np.nan
            cf_after = b_after["ceasefire_call"].mean() * 100 if len(b_after) > 0 and "ceasefire_call" in b_after else np.nan
            rows.append({
                "event": ev_name, "bloc": bloc,
                "stance_before": stance_before, "stance_after": stance_after,
                "cf_before": cf_before, "cf_after": cf_after,
                "delta_stance": stance_after - stance_before if not (np.isnan(stance_before) or np.isnan(stance_after)) else np.nan,
            })
    ev_df = pd.DataFrame(rows)
    piv = ev_df.pivot_table(index="bloc", columns="event", values="delta_stance")
    piv = piv.reindex(index=BLOC_ORDER)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(piv, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, cbar_kws={"label": "Δ stance (après - avant)"})
    ax.set_title("Event study : changement de stance (2 sem. avant → 2 sem. après)")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_fightin_words_temporal(fw_choc: pd.DataFrame, fw_resol: pd.DataFrame, bloc: str, output_path: Path):
    """Z-score plot Fightin' Words pour un bloc en CHOC vs RESOL."""
    setup_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    for ax, fw, title in zip(axes, [fw_choc, fw_resol], ["CHOC (oct 2023 - jan 2024)", "RESOL (nov 2024 - jan 2026)"]):
        top = fw.head(25)
        y_pos = range(len(top))
        colors = [COLORS.get(bloc, "#333")] * len(top)
        ax.barh(list(y_pos), top["z_score"].values, color=colors, alpha=0.8)
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(top["word"].tolist(), fontsize=9)
        ax.set_xlabel("Z-score")
        ax.set_title(f"{bloc} — {title}")
        ax.axvline(0, color="grey", lw=0.8)
    fig.suptitle(f"Fightin' Words temporel — {bloc}", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
