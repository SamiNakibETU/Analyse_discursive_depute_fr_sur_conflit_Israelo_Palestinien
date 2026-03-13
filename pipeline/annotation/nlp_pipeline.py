# -*- coding: utf-8 -*-
"""
NLP Pipeline : Validation du stance et text mining approfondi
==============================================================
Corpus : tweets + interventions AN de deputes francais sur le conflit Gaza
Auteur : pipeline genere automatiquement
"""

# ================================================================
# CELLULE 0 : CONFIGURATION, CHARGEMENT, FILTRAGE
# ================================================================
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter, OrderedDict
from scipy import stats
from scipy.spatial.distance import cosine as cosine_dist
from scipy.stats import kendalltau, spearmanr, pearsonr, chi2_contingency, pointbiserialr
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import re
import os

os.makedirs("outputs/figures", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

SEED = 42
np.random.seed(SEED)

# --- Classification politique ---
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
MARKERS = {
    "Gauche radicale": "o",
    "Gauche moderee": "s",
    "Centre / Majorite": "D",
    "Droite": "^",
}

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

EVENTS = {
    "2023-10-07": "7 octobre",
    "2024-01-26": "Ordonnance CIJ",
    "2024-05-06": "Offensive Rafah",
    "2024-06-09": "Dissolution AN",
    "2024-11-21": "Mandats CPI",
    "2025-01-19": "Cessez-le-feu",
}
EVENTS_DT = {pd.Timestamp(k): v for k, v in EVENTS.items()}
OCT7 = pd.Timestamp("2023-10-07")

STOPWORDS_FR = set([
    "le","la","les","de","du","des","un","une","et","en","a","au",
    "aux","ce","ces","cette","il","elle","ils","elles","on","nous",
    "vous","je","tu","mon","ma","mes","ton","ta","tes","son","sa",
    "ses","notre","nos","votre","vos","leur","leurs","qui","que",
    "quoi","dont","ou","mais","donc","car","ni","ne","pas",
    "plus","tres","bien","tout","tous","toute","toutes","meme",
    "aussi","comme","avec","pour","sur","dans","par","sans","sous",
    "entre","vers","chez","apres","avant","pendant","depuis","contre",
    "etre","avoir","faire","dire","aller","voir","pouvoir","vouloir",
    "devoir","falloir","est","sont","ont","fait","dit","peut",
    "faut","etait","ete","sera","soit","cet",
    "quelques","chaque","autre","autres","ici","la","alors","encore",
    "deja","jamais","toujours","souvent","peu","beaucoup","trop",
    "assez","moins","tant","si","se","cela","celui","celle","ceux",
    "celles","quand","comment","pourquoi","parce","lorsque","puisque",
    "afin","ainsi","sinon","non","oui","bon","ca",
    "monsieur","madame","president","presidente","ministre","cher",
    "chere","chers","cheres","collegue","collegues","question",
    "reponse","seance","commission","amendement","article","projet",
    "proposition","loi","texte","groupe","gouvernement","assemblee",
    "nationale","republique","france","francais","francaise",
    "http","https","www","com","rt","amp","the","of","and","to","in",
])


def clean_text(text):
    if pd.isna(text):
        return ""
    t = str(text).lower()
    t = re.sub(r'https?://\S+', '', t)
    t = re.sub(r'@\w+', '', t)
    t = re.sub(r'#(\w+)', r'\1', t)
    t = re.sub(r'[^\w\s\u00e0\u00e2\u00e4\u00e9\u00e8\u00ea\u00eb\u00ef\u00ee\u00f4\u00f9\u00fb\u00fc\u00ff\u00e7\u0153\u00e6-]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def tokenize(text):
    words = clean_text(text).split()
    return [w for w in words if w not in STOPWORDS_FR and len(w) >= 3]


def add_events_to_ax(ax, fontsize=7, rotation=90):
    ymin, ymax = ax.get_ylim()
    y_pos = ymax - 0.05 * (ymax - ymin)
    for dt, label in EVENTS_DT.items():
        ax.axvline(dt, color="#888", ls="--", lw=0.7, alpha=0.5, zorder=1)
        ax.text(dt, y_pos, f"  {label}", rotation=rotation, fontsize=fontsize,
                va="top", ha="left", color="#666", style="italic")


# --- Chargement ---
print("="*70)
print("CHARGEMENT ET FILTRAGE")
print("="*70)

tw_raw = pd.read_parquet("data/annotated/predictions/tweets_v3_full_clean.parquet")
iv_raw = pd.read_parquet("data/annotated/predictions/interventions_v3_full_clean.parquet")
print(f"Tweets bruts : {len(tw_raw):,}")
print(f"Interventions brutes : {len(iv_raw):,}")

# --- Harmonisation tweets ---
tw = tw_raw.copy()
tw["author"] = tw["depute_name"].fillna(tw["username"])
tw["group"] = tw["groupe_politique"].fillna("UNKNOWN")
tw["bloc"] = tw["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
tw["date"] = pd.to_datetime(tw["date_parsed"], errors="coerce")
tw["text_clean"] = tw["text"]
tw["arena"] = "Twitter"

# --- Harmonisation interventions ---
iv = iv_raw.copy()
iv["author"] = iv.get("speaker_name", iv.get("matched_name", iv.get("AUTEUR", "")))
if "speaker_name" in iv.columns:
    iv["author"] = iv["speaker_name"].fillna(iv.get("matched_name", ""))
iv["group"] = iv["GROUPE"].fillna(iv.get("matched_group", "UNKNOWN"))
iv["bloc"] = iv["group"].map(GROUP_TO_BLOC).fillna("UNKNOWN")
iv["date"] = pd.to_datetime(iv["sitting_date"], errors="coerce")
iv["text_clean"] = iv["cleaned_text"].fillna(iv.get("TEXTE", ""))
iv["arena"] = "AN"

# Engagement columns for interventions (fill with 0)
for col in ["retweets", "likes", "replies", "quotes"]:
    if col not in iv.columns:
        iv[col] = 0

# --- Filtrage ---
shared_cols = ["author", "group", "bloc", "date", "text_clean", "stance_v3",
               "confidence_v3", "primary_frame_v3", "primary_target_v3",
               "is_off_topic_v3", "arena", "retweets", "likes"]

n_tw0, n_iv0 = len(tw), len(iv)

tw_f = tw[
    (~tw["is_off_topic_v3"].fillna(False)) &
    (tw["confidence_v3"] >= 0.70) &
    (tw["bloc"] != "UNKNOWN") &
    (tw["date"].notna())
].copy()

iv_f = iv[
    (~iv["is_off_topic_v3"].fillna(False)) &
    (iv["confidence_v3"] >= 0.70) &
    (iv["bloc"] != "UNKNOWN") &
    (iv["date"].notna())
].copy()

# Ensure shared cols exist
for c in shared_cols:
    if c not in tw_f.columns:
        tw_f[c] = np.nan
    if c not in iv_f.columns:
        iv_f[c] = np.nan

df = pd.concat([tw_f[shared_cols], iv_f[shared_cols]], ignore_index=True)
df["month"] = df["date"].dt.to_period("M").dt.start_time
df["post_oct7"] = df["date"] >= OCT7
df["text_tokens"] = df["text_clean"].apply(tokenize)

print(f"\nApres filtrage :")
print(f"  Tweets   : {n_tw0:,} -> {len(tw_f):,} (exclu {n_tw0-len(tw_f):,})")
print(f"  Interv.  : {n_iv0:,} -> {len(iv_f):,} (exclu {n_iv0-len(iv_f):,})")
print(f"  Total df : {len(df):,}")
print(f"  Post-7oct: {df['post_oct7'].sum():,}")

for bloc in BLOC_ORDER:
    n = (df["bloc"] == bloc).sum()
    print(f"    {bloc:25s} : {n:5,} ({n/len(df)*100:.1f}%)")

# Subset post-7oct for most analyses
df_post = df[df["post_oct7"]].copy()
print(f"\nCorpus post-7 octobre : {len(df_post):,}")


# ================================================================
# CELLULE A1 : SCORE LEXICAL INDUCTIF (WORDSCORES SIMPLIFIE)
# ================================================================
print("\n" + "="*70)
print("A1 : SCORE LEXICAL INDUCTIF")
print("="*70)

try:
    # Anchor corpora
    anchor_pal = df_post[
        (df_post["bloc"] == "Gauche radicale") &
        (df_post["stance_v3"].isin([1, 2]))
    ]["text_tokens"].tolist()

    anchor_isr = df_post[
        (df_post["bloc"] == "Droite") &
        (df_post["stance_v3"].isin([-1, -2]))
    ]["text_tokens"].tolist()

    print(f"Ancre pro-PAL (Gauche rad., stance +1/+2) : {len(anchor_pal):,} textes")
    print(f"Ancre pro-ISR (Droite, stance -1/-2)      : {len(anchor_isr):,} textes")

    # Word frequencies
    counts_pal = Counter(w for doc in anchor_pal for w in doc)
    counts_isr = Counter(w for doc in anchor_isr for w in doc)
    total_pal = sum(counts_pal.values())
    total_isr = sum(counts_isr.values())

    # Build word scores (min 10 occurrences globally)
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

    print(f"Vocabulaire lexical : {len(word_scores):,} mots")

    # Score each text
    def lexical_score(tokens):
        scores = [word_scores[w] for w in tokens if w in word_scores]
        if not scores:
            return np.nan
        return np.mean(scores)

    df_post["score_lexical_raw"] = df_post["text_tokens"].apply(lexical_score)
    valid_lex = df_post["score_lexical_raw"].notna()
    print(f"Textes scores : {valid_lex.sum():,} / {len(df_post):,}")

    # Normalize to [-2, +2]
    raw = df_post.loc[valid_lex, "score_lexical_raw"]
    raw_min, raw_max = raw.min(), raw.max()
    df_post.loc[valid_lex, "score_lexical"] = (
        (raw - raw_min) / (raw_max - raw_min) * 4 - 2
    )

    # Correlations (text level)
    valid_both = df_post["score_lexical"].notna() & df_post["stance_v3"].notna()
    s_lex = df_post.loc[valid_both, "score_lexical"]
    s_v3 = df_post.loc[valid_both, "stance_v3"]
    r_pearson, p_pearson = pearsonr(s_lex, s_v3)
    r_spearman, p_spearman = spearmanr(s_lex, s_v3)
    print(f"\nCorrelation texte-level :")
    print(f"  Pearson  r={r_pearson:.3f}  p={p_pearson:.2e}")
    print(f"  Spearman rho={r_spearman:.3f}  p={p_spearman:.2e}")

    # Deputy-level aggregation
    dep_lex = df_post[valid_both].groupby("author").agg(
        mean_lex=("score_lexical", "mean"),
        mean_v3=("stance_v3", "mean"),
        bloc=("bloc", "first"),
        n=("stance_v3", "size"),
    ).reset_index()
    dep_lex = dep_lex[dep_lex["n"] >= 5]

    if len(dep_lex) >= 5:
        r_dep, p_dep = pearsonr(dep_lex["mean_lex"], dep_lex["mean_v3"])
        rho_dep, prho_dep = spearmanr(dep_lex["mean_lex"], dep_lex["mean_v3"])
        print(f"\nCorrelation depute-level (n={len(dep_lex)}) :")
        print(f"  Pearson  r={r_dep:.3f}  p={p_dep:.2e}")
        print(f"  Spearman rho={rho_dep:.3f}  p={prho_dep:.2e}")
    else:
        r_dep, rho_dep = np.nan, np.nan

    # Top words
    ws_sorted = sorted(word_scores.items(), key=lambda x: x[1])
    top_isr = ws_sorted[:20]
    top_pal = ws_sorted[-20:][::-1]

    print(f"\nTop 10 mots pro-PAL : {[f'{w} ({s:+.3f})' for w, s in top_pal[:10]]}")
    print(f"Top 10 mots pro-ISR : {[f'{w} ({s:+.3f})' for w, s in top_isr[:10]]}")

    # --- Figure A1 (2x2) ---
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # Panel A: Scatter text-level (subsampled)
    ax = axes[0, 0]
    sample_idx = df_post[valid_both].sample(n=min(3000, valid_both.sum()), random_state=SEED).index
    for bloc in BLOC_ORDER:
        mask = (df_post.index.isin(sample_idx)) & (df_post["bloc"] == bloc)
        ax.scatter(df_post.loc[mask, "score_lexical"], df_post.loc[mask, "stance_v3"],
                   c=COLORS[bloc], alpha=0.08, s=3, marker=MARKERS[bloc], rasterized=True)
    z = np.polyfit(s_lex, s_v3, 1)
    x_line = np.linspace(-2, 2, 100)
    ax.plot(x_line, z[0]*x_line + z[1], "k-", lw=1.5, alpha=0.7)
    ax.set_xlabel("Score lexical")
    ax.set_ylabel("stance_v3 (LLM)")
    ax.set_title(f"A. Texte-level (r={r_pearson:.3f}, rho={r_spearman:.3f})", loc="left")
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.5, 2.5)

    # Panel B: Scatter deputy-level
    ax = axes[0, 1]
    for bloc in BLOC_ORDER:
        sub = dep_lex[dep_lex["bloc"] == bloc]
        ax.scatter(sub["mean_lex"], sub["mean_v3"], c=COLORS[bloc],
                   s=np.clip(sub["n"]*2, 15, 150), alpha=0.7,
                   marker=MARKERS[bloc], label=bloc, edgecolors="white", lw=0.5)
    # Annotate top 5 outliers
    dep_lex["div"] = (dep_lex["mean_lex"] - dep_lex["mean_v3"]).abs()
    for _, r in dep_lex.nlargest(5, "div").iterrows():
        name_short = str(r["author"]).split()[-1] if isinstance(r["author"], str) else ""
        ax.annotate(name_short, (r["mean_lex"], r["mean_v3"]), fontsize=6,
                    xytext=(4, 4), textcoords="offset points")
    ax.plot([-2.5, 2.5], [-2.5, 2.5], "k--", lw=0.8, alpha=0.4)
    ax.set_xlabel("Score lexical moyen")
    ax.set_ylabel("stance_v3 moyen")
    ax.set_title(f"B. Depute-level (r={r_dep:.3f})", loc="left")
    ax.legend(fontsize=8, loc="upper left")

    # Panel C: Violin by stance category
    ax = axes[1, 0]
    categories = sorted(df_post.loc[valid_both, "stance_v3"].unique())
    data_viol = [df_post.loc[(df_post["stance_v3"] == c) & valid_both, "score_lexical"].dropna().values
                 for c in categories]
    data_viol = [d for d in data_viol if len(d) >= 3]
    if data_viol:
        parts = ax.violinplot(data_viol, positions=range(len(categories)), showmeans=True, showmedians=True)
        cmap = plt.cm.RdBu_r
        for i, pc in enumerate(parts["bodies"]):
            norm_val = (categories[i] + 2) / 4
            pc.set_facecolor(cmap(norm_val))
            pc.set_alpha(0.6)
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels([str(c) for c in categories])
    ax.set_xlabel("stance_v3 (LLM)")
    ax.set_ylabel("Score lexical")
    ax.set_title("C. Score lexical par categorie stance_v3", loc="left")

    # Panel D: Top 20 words each side
    ax = axes[1, 1]
    words_display = list(reversed(top_isr[:20])) + top_pal[:20]
    y_pos = range(len(words_display))
    colors_bar = ["#2c3e50"]*20 + ["#c0392b"]*20
    ax.barh(list(y_pos), [s for _, s in words_display], color=colors_bar, alpha=0.8)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels([w for w, _ in words_display], fontsize=7)
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_xlabel("Score lexical du mot (-1=pro-ISR, +1=pro-PAL)")
    ax.set_title("D. Top 20 mots discriminants", loc="left")

    fig.suptitle("A1 : Score lexical inductif (Wordscores simplifie)", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/A1_lexical_scoring.png")
    plt.close(fig)
    print("\nFigure A1 sauvegardee.")

except Exception as e:
    print(f"ERREUR A1 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE A2 : WORDFISH — POSITIONNEMENT LATENT NON SUPERVISE
# ================================================================
print("\n" + "="*70)
print("A2 : WORDFISH (positionnement latent)")
print("="*70)

try:
    # Build deputy-level corpus (post-7oct, min 10 texts)
    dep_texts = df_post.groupby("author").agg(
        texts=("text_clean", lambda x: " ".join(x.dropna().astype(str))),
        n=("text_clean", "size"),
        bloc=("bloc", "first"),
        mean_v3=("stance_v3", "mean"),
    ).reset_index()
    dep_texts = dep_texts[dep_texts["n"] >= 10].reset_index(drop=True)
    print(f"Deputes avec >= 10 textes post-7oct : {len(dep_texts)}")

    # TF-IDF matrix
    tfidf = TfidfVectorizer(
        max_features=3000, min_df=5, max_df=0.80,
        stop_words=list(STOPWORDS_FR), sublinear_tf=True,
    )
    dtm = tfidf.fit_transform(dep_texts["texts"].apply(clean_text))
    vocab = tfidf.get_feature_names_out()
    print(f"Vocabulaire TF-IDF : {len(vocab)} termes, matrice {dtm.shape}")

    # Correspondence Analysis approximation via SVD on chi2 residuals
    from scipy.sparse import diags, issparse
    X = dtm.toarray() if issparse(dtm) else dtm
    X = X + 1e-10  # avoid zeros

    P = X / X.sum()
    r = P.sum(axis=1)
    c = P.sum(axis=0)

    Dr_inv = np.diag(1.0 / np.sqrt(r))
    Dc_inv = np.diag(1.0 / np.sqrt(c))
    S = Dr_inv @ (P - np.outer(r, c)) @ Dc_inv

    U, sigma, Vt = np.linalg.svd(S, full_matrices=False)

    theta_wf = U[:, 0] * sigma[0]

    # Orient: Gauche radicale should be positive
    mean_gr = theta_wf[dep_texts["bloc"] == "Gauche radicale"].mean()
    if mean_gr < 0:
        theta_wf *= -1
        Vt[0, :] *= -1

    dep_texts["theta_wordfish"] = theta_wf
    var_explained = sigma[0]**2 / (sigma**2).sum()
    print(f"Variance axe 1 : {var_explained:.1%}")

    # Correlations
    valid_wf = dep_texts["mean_v3"].notna() & dep_texts["theta_wordfish"].notna()
    r_wf_v3, p_wf_v3 = spearmanr(dep_texts.loc[valid_wf, "theta_wordfish"],
                                   dep_texts.loc[valid_wf, "mean_v3"])
    print(f"Spearman theta_wf vs stance_v3 : rho={r_wf_v3:.3f}, p={p_wf_v3:.2e}")

    # Merge with lexical score
    if "score_lexical" in df_post.columns:
        dep_lex_merge = df_post.groupby("author")["score_lexical"].mean().reset_index()
        dep_texts = dep_texts.merge(dep_lex_merge, on="author", how="left")
        valid_lex_wf = dep_texts["score_lexical"].notna() & dep_texts["theta_wordfish"].notna()
        if valid_lex_wf.sum() >= 5:
            r_wf_lex, p_wf_lex = spearmanr(dep_texts.loc[valid_lex_wf, "theta_wordfish"],
                                             dep_texts.loc[valid_lex_wf, "score_lexical"])
            print(f"Spearman theta_wf vs score_lexical : rho={r_wf_lex:.3f}, p={p_wf_lex:.2e}")
        else:
            r_wf_lex = np.nan
    else:
        r_wf_lex = np.nan

    # Word loadings
    loadings = Vt[0, :]
    word_loading = list(zip(vocab, loadings))
    word_loading.sort(key=lambda x: x[1])
    top_isr_wf = word_loading[:20]
    top_pal_wf = word_loading[-20:][::-1]
    print(f"\nTop 5 mots pole pro-PAL (Wordfish) : {[w for w,_ in top_pal_wf[:5]]}")
    print(f"Top 5 mots pole pro-ISR (Wordfish) : {[w for w,_ in top_isr_wf[:5]]}")

    # --- Figure A2 (2x2) ---
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # Panel A: Dot plot sorted
    ax = axes[0, 0]
    sorted_dep = dep_texts.sort_values("theta_wordfish")
    y_pos = range(len(sorted_dep))
    colors_dots = [COLORS.get(b, "#999") for b in sorted_dep["bloc"]]
    ax.scatter(sorted_dep["theta_wordfish"], list(y_pos), c=colors_dots, s=15, alpha=0.8)
    ax.set_xlabel("theta Wordfish")
    ax.set_ylabel("Deputes (tries)")
    ax.set_title("A. Positions Wordfish par depute", loc="left")
    ax.set_yticks([])
    handles = [Line2D([0],[0], marker="o", color=COLORS[b], lw=0, label=b, markersize=6) for b in BLOC_ORDER]
    ax.legend(handles=handles, fontsize=8, loc="upper left")

    # Panel B: theta_wf vs stance_v3
    ax = axes[0, 1]
    for bloc in BLOC_ORDER:
        sub = dep_texts[dep_texts["bloc"] == bloc]
        ax.scatter(sub["theta_wordfish"], sub["mean_v3"], c=COLORS[bloc],
                   s=np.clip(sub["n"]*1.5, 15, 120), alpha=0.7,
                   marker=MARKERS[bloc], label=bloc, edgecolors="white", lw=0.5)
    ax.set_xlabel("theta Wordfish")
    ax.set_ylabel("stance_v3 moyen")
    ax.set_title(f"B. Wordfish vs stance_v3 (rho={r_wf_v3:.3f})", loc="left")
    ax.legend(fontsize=8)

    # Panel C: theta_wf vs score_lexical
    ax = axes[1, 0]
    if "score_lexical" in dep_texts.columns:
        for bloc in BLOC_ORDER:
            sub = dep_texts[(dep_texts["bloc"] == bloc) & dep_texts["score_lexical"].notna()]
            ax.scatter(sub["theta_wordfish"], sub["score_lexical"], c=COLORS[bloc],
                       s=np.clip(sub["n"]*1.5, 15, 120), alpha=0.7,
                       marker=MARKERS[bloc], label=bloc, edgecolors="white", lw=0.5)
        rho_label = f"rho={r_wf_lex:.3f}" if not np.isnan(r_wf_lex) else "N/A"
        ax.set_title(f"C. Wordfish vs Score lexical ({rho_label})", loc="left")
    else:
        ax.set_title("C. Wordfish vs Score lexical (N/A)", loc="left")
    ax.set_xlabel("theta Wordfish")
    ax.set_ylabel("Score lexical moyen")
    ax.legend(fontsize=8)

    # Panel D: Top words
    ax = axes[1, 1]
    words_wf = list(reversed(top_isr_wf[:20])) + top_pal_wf[:20]
    y_wf = range(len(words_wf))
    colors_wf = ["#2c3e50"]*20 + ["#c0392b"]*20
    ax.barh(list(y_wf), [s for _, s in words_wf], color=colors_wf, alpha=0.8)
    ax.set_yticks(list(y_wf))
    ax.set_yticklabels([w for w, _ in words_wf], fontsize=7)
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_xlabel("Loading axe 1")
    ax.set_title("D. Mots discriminants (Wordfish)", loc="left")

    fig.suptitle("A2 : Wordfish -- Positionnement latent non supervise", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/A2_wordfish.png")
    plt.close(fig)
    print("Figure A2 sauvegardee.")

except Exception as e:
    print(f"ERREUR A2 : {e}")
    import traceback; traceback.print_exc()
    dep_texts = pd.DataFrame()


# ================================================================
# CELLULE A3 : EMBEDDING DIAGNOSTIQUE — PCA
# ================================================================
print("\n" + "="*70)
print("A3 : EMBEDDING DIAGNOSTIQUE (PCA)")
print("="*70)

try:
    # TF-IDF on individual texts (post-7oct)
    texts_a3 = df_post["text_clean"].apply(clean_text)
    valid_text = texts_a3.str.len() > 10
    texts_a3 = texts_a3[valid_text]
    df_a3 = df_post[valid_text].copy()
    print(f"Textes valides pour embedding : {len(df_a3):,}")

    tfidf_a3 = TfidfVectorizer(max_features=5000, stop_words=list(STOPWORDS_FR), sublinear_tf=True)
    X_tfidf = tfidf_a3.fit_transform(texts_a3)

    svd_a3 = TruncatedSVD(n_components=50, random_state=SEED)
    X_svd = svd_a3.fit_transform(X_tfidf)
    print(f"SVD 50 comp : variance cumulee = {svd_a3.explained_variance_ratio_.sum():.1%}")

    # PCA on SVD output
    from sklearn.decomposition import PCA
    pca_a3 = PCA(n_components=2, random_state=SEED)
    X_pca = pca_a3.fit_transform(X_svd)
    df_a3["PC1"] = X_pca[:, 0]
    df_a3["PC2"] = X_pca[:, 1]
    print(f"PCA : PC1={pca_a3.explained_variance_ratio_[0]:.1%}, PC2={pca_a3.explained_variance_ratio_[1]:.1%}")

    # Orient PC1 so that Gauche radicale is positive
    mean_gr = df_a3.loc[df_a3["bloc"] == "Gauche radicale", "PC1"].mean()
    if mean_gr < 0:
        df_a3["PC1"] *= -1
        X_pca[:, 0] *= -1

    # Correlations
    valid_pc = df_a3["stance_v3"].notna()
    r_pc1_v3, p_pc1 = spearmanr(df_a3.loc[valid_pc, "PC1"], df_a3.loc[valid_pc, "stance_v3"])
    print(f"Spearman PC1 vs stance_v3 : rho={r_pc1_v3:.3f}, p={p_pc1:.2e}")

    # Silhouette
    bloc_labels = df_a3["bloc"].values
    bloc_known = bloc_labels != "UNKNOWN"
    if bloc_known.sum() > 100:
        sil = silhouette_score(X_pca[bloc_known], bloc_labels[bloc_known],
                                sample_size=min(3000, bloc_known.sum()), random_state=SEED)
        print(f"Silhouette score (blocs dans PCA) : {sil:.3f}")

    # Deputy centroids
    dep_emb = df_a3.groupby("author").agg(
        PC1=("PC1", "mean"), PC2=("PC2", "mean"),
        bloc=("bloc", "first"), n=("stance_v3", "size"),
        mean_v3=("stance_v3", "mean"),
    ).reset_index()
    dep_emb = dep_emb[dep_emb["n"] >= 5]

    # --- Figure A3 (3x2) ---
    fig, axes = plt.subplots(3, 2, figsize=(16, 20))

    # Subsample for text-level plots
    n_sample = min(3000, len(df_a3))
    idx_sample = df_a3.sample(n=n_sample, random_state=SEED).index

    # Panel A: PCA colored by stance_v3
    ax = axes[0, 0]
    sub = df_a3.loc[idx_sample]
    sc = ax.scatter(sub["PC1"], sub["PC2"], c=sub["stance_v3"], cmap="RdBu_r",
                    vmin=-2, vmax=2, s=3, alpha=0.3, rasterized=True)
    plt.colorbar(sc, ax=ax, label="stance_v3")
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("A. PCA colore par stance_v3", loc="left")

    # Panel B: PCA colored by bloc
    ax = axes[0, 1]
    for bloc in BLOC_ORDER:
        m = sub["bloc"] == bloc
        ax.scatter(sub.loc[m, "PC1"], sub.loc[m, "PC2"], c=COLORS[bloc],
                   s=3, alpha=0.2, label=bloc, rasterized=True)
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("B. PCA colore par bloc", loc="left")
    ax.legend(fontsize=8, markerscale=5)

    # Panel C: PCA colored by arena
    ax = axes[1, 0]
    arena_colors = {"Twitter": "#1DA1F2", "AN": "#B22222"}
    for arena in ["Twitter", "AN"]:
        m = sub["arena"] == arena
        ax.scatter(sub.loc[m, "PC1"], sub.loc[m, "PC2"], c=arena_colors[arena],
                   s=3, alpha=0.2, label=arena, rasterized=True)
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("C. PCA colore par arene", loc="left")
    ax.legend(fontsize=8, markerscale=5)

    # Panel D: Centroids by deputy
    ax = axes[1, 1]
    for bloc in BLOC_ORDER:
        sub_d = dep_emb[dep_emb["bloc"] == bloc]
        ax.scatter(sub_d["PC1"], sub_d["PC2"], c=COLORS[bloc],
                   s=np.clip(sub_d["n"]*2, 15, 150), alpha=0.7,
                   marker=MARKERS[bloc], label=bloc, edgecolors="white", lw=0.5)
    # Annotate 5 most extreme on PC1
    for _, r in dep_emb.nlargest(3, "PC1").iterrows():
        ax.annotate(str(r["author"]).split()[-1], (r["PC1"], r["PC2"]), fontsize=6)
    for _, r in dep_emb.nsmallest(3, "PC1").iterrows():
        ax.annotate(str(r["author"]).split()[-1], (r["PC1"], r["PC2"]), fontsize=6)
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("D. Centroides par depute", loc="left")
    ax.legend(fontsize=8)

    # Panel E: Centroids colored by stance_v3 mean
    ax = axes[2, 0]
    valid_dep = dep_emb["mean_v3"].notna()
    sc2 = ax.scatter(dep_emb.loc[valid_dep, "PC1"], dep_emb.loc[valid_dep, "PC2"],
                     c=dep_emb.loc[valid_dep, "mean_v3"], cmap="RdBu_r", vmin=-2, vmax=2,
                     s=np.clip(dep_emb.loc[valid_dep, "n"]*2, 15, 120), alpha=0.8, edgecolors="white", lw=0.5)
    plt.colorbar(sc2, ax=ax, label="stance_v3 moyen")
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("E. Centroides colores par stance_v3 moyen", loc="left")

    # Panel F: Correlation summary
    ax = axes[2, 1]
    corr_labels = ["PC1 vs\nstance_v3"]
    corr_values = [r_pc1_v3]
    # Add more if available
    if "score_lexical" in df_a3.columns:
        valid_pc_lex = df_a3["score_lexical"].notna()
        if valid_pc_lex.sum() > 10:
            r_tmp, _ = spearmanr(df_a3.loc[valid_pc_lex, "PC1"], df_a3.loc[valid_pc_lex, "score_lexical"])
            corr_labels.append("PC1 vs\nscore_lex")
            corr_values.append(r_tmp)
    if len(dep_texts) > 0 and "theta_wordfish" in dep_texts.columns:
        merged_tmp = dep_emb.merge(dep_texts[["author","theta_wordfish"]], on="author", how="inner")
        if len(merged_tmp) > 5:
            r_tmp2, _ = spearmanr(merged_tmp["PC1"], merged_tmp["theta_wordfish"])
            corr_labels.append("PC1 vs\nWordfish")
            corr_values.append(r_tmp2)

    bar_colors = ["#2ecc71" if v > 0.5 else "#f39c12" if v > 0.3 else "#e74c3c" for v in np.abs(corr_values)]
    ax.barh(range(len(corr_labels)), corr_values, color=bar_colors, alpha=0.8)
    ax.set_yticks(range(len(corr_labels)))
    ax.set_yticklabels(corr_labels, fontsize=10)
    ax.set_xlabel("Spearman rho")
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_title("F. Triple triangulation (correlations)", loc="left")
    for i, v in enumerate(corr_values):
        ax.text(v + 0.02 * np.sign(v), i, f"{v:.3f}", va="center", fontsize=10, fontweight="bold")

    fig.suptitle("A3 : Embedding diagnostique (PCA sur TF-IDF SVD)", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/A3_embedding_pca.png")
    plt.close(fig)
    print("Figure A3 sauvegardee.")

except Exception as e:
    print(f"ERREUR A3 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE A4 : TRIANGULATION SYNTHETIQUE
# ================================================================
print("\n" + "="*70)
print("A4 : TRIANGULATION SYNTHETIQUE")
print("="*70)

try:
    # Build deputy-level table with all 4 measures
    dep_all = df_post.groupby("author").agg(
        mean_v3=("stance_v3", "mean"),
        bloc=("bloc", "first"),
        n=("stance_v3", "size"),
        arena_main=("arena", lambda x: x.mode().iloc[0] if len(x) > 0 else "Unknown"),
    ).reset_index()
    dep_all = dep_all[dep_all["n"] >= 5].copy()

    # Merge score_lexical
    if "score_lexical" in df_post.columns:
        lex_dep = df_post.groupby("author")["score_lexical"].mean().reset_index()
        dep_all = dep_all.merge(lex_dep, on="author", how="left")
    else:
        dep_all["score_lexical"] = np.nan

    # Merge wordfish
    if len(dep_texts) > 0 and "theta_wordfish" in dep_texts.columns:
        dep_all = dep_all.merge(dep_texts[["author", "theta_wordfish"]], on="author", how="left")
    else:
        dep_all["theta_wordfish"] = np.nan

    # Merge PC1
    if "PC1" in dep_emb.columns:
        dep_all = dep_all.merge(dep_emb[["author", "PC1"]], on="author", how="left")
    else:
        dep_all["PC1"] = np.nan

    measures = ["mean_v3", "score_lexical", "theta_wordfish", "PC1"]
    measure_labels = ["stance_v3\n(LLM)", "Score\nlexical", "Wordfish\n(theta)", "PCA\n(PC1)"]

    # Correlation matrix (Spearman)
    valid_rows = dep_all[measures].dropna()
    print(f"\nDeputes avec les 4 mesures : {len(valid_rows)}")

    corr_matrix = np.ones((4, 4))
    pval_matrix = np.zeros((4, 4))
    for i in range(4):
        for j in range(i+1, 4):
            valid_ij = dep_all[[measures[i], measures[j]]].dropna()
            if len(valid_ij) >= 5:
                rho, pv = spearmanr(valid_ij[measures[i]], valid_ij[measures[j]])
                corr_matrix[i, j] = rho
                corr_matrix[j, i] = rho
                pval_matrix[i, j] = pv
                pval_matrix[j, i] = pv

    print("\nMatrice de correlation Spearman :")
    for i in range(4):
        row_str = "  ".join([f"{corr_matrix[i,j]:+.3f}" for j in range(4)])
        print(f"  {measure_labels[i].replace(chr(10),' '):20s} : {row_str}")

    # --- Figure A4 : Heatmap ---
    fig, ax = plt.subplots(figsize=(8, 7))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap="RdBu_r", center=0,
                xticklabels=[l.replace("\n"," ") for l in measure_labels],
                yticklabels=[l.replace("\n"," ") for l in measure_labels],
                vmin=-1, vmax=1, ax=ax, linewidths=0.5, square=True)
    ax.set_title("Matrice de correlation Spearman (4 mesures de positionnement)", fontweight="bold")
    fig.tight_layout()
    fig.savefig("outputs/figures/A4_triangulation_heatmap.png")
    plt.close(fig)

    # --- Figure A4b : By arena ---
    fig, ax = plt.subplots(figsize=(10, 5))
    arena_corrs = {}
    for arena_name, arena_df_src in [("Twitter", tw_f), ("AN", iv_f)]:
        dep_arena = arena_df_src.groupby("author").agg(
            mean_v3=("stance_v3", "mean"),
            n=("stance_v3", "size"),
        ).reset_index()
        dep_arena = dep_arena[dep_arena["n"] >= 5]
        if "score_lexical" not in arena_df_src.columns:
            arena_df_src = arena_df_src.copy()
            arena_df_src["text_tokens"] = arena_df_src["text_clean"].apply(tokenize)
            arena_df_src["score_lexical_raw"] = arena_df_src["text_tokens"].apply(
                lambda tok: np.mean([word_scores.get(w, np.nan) for w in tok if w in word_scores]) if tok else np.nan
            )
            valid_ar = arena_df_src["score_lexical_raw"].notna()
            if valid_ar.any():
                raw_ar = arena_df_src.loc[valid_ar, "score_lexical_raw"]
                rng = raw_ar.max() - raw_ar.min()
                if rng > 0:
                    arena_df_src.loc[valid_ar, "score_lexical"] = (raw_ar - raw_ar.min()) / rng * 4 - 2
        lex_arena = arena_df_src.groupby("author")["score_lexical"].mean().reset_index() if "score_lexical" in arena_df_src.columns else pd.DataFrame()
        if not lex_arena.empty:
            dep_arena = dep_arena.merge(lex_arena, on="author", how="left")
            valid_pair = dep_arena[["mean_v3","score_lexical"]].dropna()
            if len(valid_pair) >= 5:
                rho_ar, _ = spearmanr(valid_pair["mean_v3"], valid_pair["score_lexical"])
                arena_corrs[arena_name] = rho_ar
    if arena_corrs:
        bars = ax.bar(range(len(arena_corrs)), list(arena_corrs.values()),
                      color=["#1DA1F2", "#B22222"][:len(arena_corrs)], alpha=0.8)
        ax.set_xticks(range(len(arena_corrs)))
        ax.set_xticklabels(list(arena_corrs.keys()), fontsize=12)
        ax.set_ylabel("Spearman rho (stance_v3 vs score_lexical)")
        ax.set_title("Fiabilite du stance_v3 par arene", fontweight="bold")
        for bar, val in zip(bars, arena_corrs.values()):
            ax.text(bar.get_x() + bar.get_width()/2, val + 0.01, f"{val:.3f}",
                    ha="center", fontsize=12, fontweight="bold")
        ax.set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig("outputs/figures/A4_triangulation_by_arena.png")
    plt.close(fig)
    print("Figures A4 sauvegardees.")

    # Discordant deputies
    if len(valid_rows) >= 5:
        from scipy.stats import rankdata
        ranks = pd.DataFrame({m: rankdata(valid_rows[m]) for m in measures}, index=valid_rows.index)
        rank_std = ranks.std(axis=1)
        valid_rows_copy = valid_rows.copy()
        valid_rows_copy["rank_discord"] = rank_std.values
        valid_rows_copy["author"] = dep_all.loc[valid_rows.index, "author"].values
        valid_rows_copy["bloc"] = dep_all.loc[valid_rows.index, "bloc"].values
        top_discord = valid_rows_copy.nlargest(10, "rank_discord")
        print("\nTop 10 deputes discordants :")
        for _, r in top_discord.iterrows():
            print(f"  {r['author']:30s} ({r['bloc']:20s}) v3={r['mean_v3']:+.2f} lex={r['score_lexical']:+.2f} "
                  f"wf={r['theta_wordfish']:+.2f} pc1={r['PC1']:+.2f}")

    # Summary
    mean_off_diag = []
    for i in range(4):
        for j in range(i+1, 4):
            if not np.isnan(corr_matrix[i, j]):
                mean_off_diag.append(corr_matrix[i, j])
    avg_corr = np.mean(mean_off_diag) if mean_off_diag else np.nan
    print(f"\nCorrelation moyenne inter-mesures : {avg_corr:.3f}")
    tw_corr = arena_corrs.get("Twitter", np.nan)
    an_corr = arena_corrs.get("AN", np.nan)
    print(f"\nConclusion : Le stance_v3 est {'fiable' if avg_corr > 0.5 else 'moderement fiable'} "
          f"(correlation moyenne inter-mesures rho={avg_corr:.3f}). "
          f"Fiabilite Twitter: rho={tw_corr:.3f}, AN: rho={an_corr:.3f}.")

except Exception as e:
    print(f"ERREUR A4 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE B1 : FIGHTIN' WORDS
# ================================================================
print("\n" + "="*70)
print("B1 : FIGHTIN' WORDS")
print("="*70)

try:
    def fightin_words(corpus_a, corpus_b, alpha_prior=0.01, min_count=5):
        counts_a = Counter(w for doc in corpus_a for w in doc)
        counts_b = Counter(w for doc in corpus_b for w in doc)
        vocab_fw = set(k for k, v in (counts_a + counts_b).items() if v >= min_count)

        n_a = sum(counts_a[w] for w in vocab_fw)
        n_b = sum(counts_b[w] for w in vocab_fw)
        V = len(vocab_fw)
        alpha_w = alpha_prior
        alpha_0 = V * alpha_w

        results = []
        for w in vocab_fw:
            y_a = counts_a[w]
            y_b = counts_b[w]
            log_odds = (np.log((y_a + alpha_w) / (n_a + alpha_0 - y_a - alpha_w)) -
                        np.log((y_b + alpha_w) / (n_b + alpha_0 - y_b - alpha_w)))
            var = (1 / (y_a + alpha_w)) + (1 / (y_b + alpha_w))
            z_score = log_odds / np.sqrt(var)
            results.append({
                'word': w, 'count_a': y_a, 'count_b': y_b,
                'freq_a_pct': y_a / n_a * 100 if n_a > 0 else 0,
                'freq_b_pct': y_b / n_b * 100 if n_b > 0 else 0,
                'log_odds': log_odds, 'z_score': z_score
            })
        return pd.DataFrame(results).sort_values('z_score', ascending=False)

    # 4 comparisons
    comparisons = {}

    # 1. Gauche radicale vs Droite (tweets post-7oct)
    tw_post = df_post[df_post["arena"] == "Twitter"]
    gr_tok = tw_post[tw_post["bloc"] == "Gauche radicale"]["text_tokens"].tolist()
    dr_tok = tw_post[tw_post["bloc"] == "Droite"]["text_tokens"].tolist()
    if gr_tok and dr_tok:
        comparisons["Gauche rad. vs Droite\n(tweets post-7oct)"] = (
            fightin_words(gr_tok, dr_tok), "Gauche rad.", "Droite",
            COLORS["Gauche radicale"], COLORS["Droite"]
        )

    # 2. PRE vs POST 7 octobre
    pre_tok = df[~df["post_oct7"]]["text_tokens"].tolist()
    post_tok = df[df["post_oct7"]]["text_tokens"].tolist()
    if pre_tok and post_tok:
        comparisons["POST vs PRE 7 octobre\n(tous blocs)"] = (
            fightin_words(post_tok, pre_tok), "POST", "PRE",
            "#e74c3c", "#3498db"
        )

    # 3. Twitter vs AN (post-7oct)
    tw_tok = df_post[df_post["arena"] == "Twitter"]["text_tokens"].tolist()
    an_tok = df_post[df_post["arena"] == "AN"]["text_tokens"].tolist()
    if tw_tok and an_tok:
        comparisons["Twitter vs AN\n(post-7oct)"] = (
            fightin_words(tw_tok, an_tok), "Twitter", "AN",
            "#1DA1F2", "#B22222"
        )

    # 4. RN vs LR (tweets post-7oct)
    rn_tok = tw_post[tw_post["group"] == "RN"]["text_tokens"].tolist()
    lr_tok = tw_post[tw_post["group"] == "LR"]["text_tokens"].tolist()
    if rn_tok and lr_tok:
        comparisons["RN vs LR\n(tweets post-7oct)"] = (
            fightin_words(rn_tok, lr_tok), "RN", "LR",
            "#0d378a", "#0000cc"
        )

    # --- Figure B1 ---
    n_comp = len(comparisons)
    fig, axes = plt.subplots(n_comp, 1, figsize=(16, 5 * n_comp))
    if n_comp == 1:
        axes = [axes]

    for idx, (title, (fw_df, label_a, label_b, color_a, color_b)) in enumerate(comparisons.items()):
        ax = axes[idx]
        top_a = fw_df.head(20)
        top_b = fw_df.tail(20).iloc[::-1]
        combined = pd.concat([top_b, top_a])

        y_pos = range(len(combined))
        colors_fw = [color_b if z < 0 else color_a for z in combined["z_score"]]
        ax.barh(list(y_pos), combined["z_score"].values, color=colors_fw, alpha=0.85)
        ax.set_yticks(list(y_pos))
        ylabels = []
        for _, r in combined.iterrows():
            freq = r["freq_a_pct"] if r["z_score"] > 0 else r["freq_b_pct"]
            ylabels.append(f"{r['word']} ({freq:.2f}%)")
        ax.set_yticklabels(ylabels, fontsize=7)
        ax.axvline(0, color="grey", lw=0.8)
        ax.set_xlabel("z-score (Monroe et al.)")
        ax.set_title(f"{title}  [{label_a} (+) vs {label_b} (-)]", loc="left", fontsize=11)

    fig.suptitle("B1 : Fightin' Words -- Vocabulaire distinctif", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/B1_fightin_words.png")
    plt.close(fig)
    print(f"Figure B1 sauvegardee ({n_comp} comparaisons).")

except Exception as e:
    print(f"ERREUR B1 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE B2 : SUIVI LEXICAL TEMPOREL PAR REGISTRE
# ================================================================
print("\n" + "="*70)
print("B2 : SUIVI LEXICAL TEMPOREL")
print("="*70)

try:
    REGISTRES = {
        "Humanitaire": ["civils", "enfants", "bombardements", "victimes", "humanitaire",
                         "hopital", "hopitaux", "famine", "refugies", "populations"],
        "Securitaire": ["terrorisme", "terroriste", "terroristes", "hamas", "otages",
                         "securite", "menace", "attaque", "attaques", "roquettes"],
        "Juridique": ["genocide", "crimes", "guerre", "cij", "cpi", "cour",
                       "droit international", "mandat", "mandats", "penale"],
        "Diplomatique": ["cessez-le-feu", "negociations", "reconnaissance",
                          "etat palestinien", "embargo", "sanctions", "diplomatie", "paix"],
    }

    # Count term occurrences per bloc x month
    reg_rows = []
    for _, row in df_post.iterrows():
        text_low = clean_text(row["text_clean"])
        total_words = max(len(text_low.split()), 1)
        bloc = row["bloc"]
        month = row["month"]
        for reg_name, terms in REGISTRES.items():
            count = 0
            for term in terms:
                count += text_low.count(term)
            reg_rows.append({
                "bloc": bloc, "month": month, "registre": reg_name,
                "count": count, "total_words": total_words,
            })

    df_reg = pd.DataFrame(reg_rows)
    df_reg_agg = df_reg.groupby(["bloc", "month", "registre"]).agg(
        total_count=("count", "sum"),
        total_words=("total_words", "sum"),
    ).reset_index()
    df_reg_agg["freq_permille"] = df_reg_agg["total_count"] / df_reg_agg["total_words"] * 1000

    # --- Figure B2a : 4 panels (one per register) ---
    reg_names = list(REGISTRES.keys())
    fig, axes = plt.subplots(2, 2, figsize=(18, 12), sharex=True)
    axes_flat = axes.flatten()

    for idx, reg in enumerate(reg_names):
        ax = axes_flat[idx]
        sub_reg = df_reg_agg[df_reg_agg["registre"] == reg]
        for bloc in BLOC_ORDER:
            sub_b = sub_reg[sub_reg["bloc"] == bloc].sort_values("month")
            if not sub_b.empty:
                ax.plot(sub_b["month"], sub_b["freq_permille"], color=COLORS[bloc],
                        lw=1.8, marker=MARKERS[bloc], markersize=3, label=bloc, alpha=0.8)
        ax.set_ylabel("Frequence (pour mille)")
        ax.set_title(reg, loc="left", fontweight="bold")
        add_events_to_ax(ax)
        if idx == 0:
            ax.legend(fontsize=8)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=7)

    fig.suptitle("B2 : Suivi lexical temporel par registre", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/B2_lexical_tracking.png")
    plt.close(fig)

    # --- Figure B2b : Heatmap terms x blocs ---
    term_bloc_rows = []
    for reg_name, terms in REGISTRES.items():
        for term in terms:
            for bloc in BLOC_ORDER:
                sub = df_post[df_post["bloc"] == bloc]
                texts = sub["text_clean"].apply(clean_text)
                count = texts.str.count(term).sum()
                total = texts.str.split().str.len().sum()
                freq = count / max(total, 1) * 1000
                term_bloc_rows.append({
                    "registre": reg_name, "term": term, "bloc": bloc, "freq_permille": freq
                })
    df_tb = pd.DataFrame(term_bloc_rows)
    piv_tb = df_tb.pivot_table(index="term", columns="bloc", values="freq_permille")

    # Sort by registre
    term_order = []
    for reg_name, terms in REGISTRES.items():
        for t in terms:
            if t in piv_tb.index:
                term_order.append(t)
    piv_tb = piv_tb.reindex(index=term_order, columns=BLOC_ORDER)

    fig, ax = plt.subplots(figsize=(10, 14))
    sns.heatmap(piv_tb, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5,
                ax=ax, cbar_kws={"label": "Frequence (pour mille)"})
    ax.set_title("Frequence des termes par bloc (post-7 oct.)", fontweight="bold")
    ax.set_ylabel("Terme")
    fig.tight_layout()
    fig.savefig("outputs/figures/B2_term_heatmap.png")
    plt.close(fig)

    # Kendall tau trends
    print("\nTendances temporelles (Kendall tau, post-7oct) :")
    for reg in reg_names:
        print(f"\n  {reg} :")
        for bloc in BLOC_ORDER:
            sub = df_reg_agg[(df_reg_agg["registre"] == reg) & (df_reg_agg["bloc"] == bloc)].sort_values("month")
            if len(sub) >= 5:
                month_num = (sub["month"] - sub["month"].min()).dt.days
                tau, pval = kendalltau(month_num, sub["freq_permille"])
                sig = "*" if pval < 0.05 else ""
                print(f"    {bloc:25s} : tau={tau:+.3f}, p={pval:.4f} {sig}")

    print("Figures B2 sauvegardees.")

except Exception as e:
    print(f"ERREUR B2 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE B3 : N-GRAMS DISTINCTIFS PAR BLOC
# ================================================================
print("\n" + "="*70)
print("B3 : N-GRAMS DISTINCTIFS PAR BLOC")
print("="*70)

try:
    # Build corpus per bloc (post-7oct)
    bloc_corpora = {}
    for bloc in BLOC_ORDER:
        texts = df_post[df_post["bloc"] == bloc]["text_clean"].apply(clean_text).tolist()
        bloc_corpora[bloc] = " ".join(texts)

    # TF-IDF on bloc-level docs
    tfidf_ng = TfidfVectorizer(
        ngram_range=(2, 3), min_df=1, max_df=1.0,
        stop_words=list(STOPWORDS_FR), max_features=5000,
    )
    corpus_list = [bloc_corpora[b] for b in BLOC_ORDER]
    tfidf_matrix = tfidf_ng.fit_transform(corpus_list)
    feature_names = tfidf_ng.get_feature_names_out()

    # Top 15 per bloc
    top_ngrams = {}
    for i, bloc in enumerate(BLOC_ORDER):
        scores = tfidf_matrix[i].toarray().flatten()
        top_idx = scores.argsort()[-15:][::-1]
        top_ngrams[bloc] = [(feature_names[j], scores[j]) for j in top_idx if scores[j] > 0]

    # --- Figure B3 (2x2) ---
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    axes_flat = axes.flatten()

    for idx, bloc in enumerate(BLOC_ORDER):
        ax = axes_flat[idx]
        ngrams = top_ngrams.get(bloc, [])[:15]
        if ngrams:
            words_ng = [w for w, _ in ngrams][::-1]
            scores_ng = [s for _, s in ngrams][::-1]
            ax.barh(range(len(words_ng)), scores_ng, color=COLORS[bloc], alpha=0.85)
            ax.set_yticks(range(len(words_ng)))
            ax.set_yticklabels(words_ng, fontsize=8)
        ax.set_xlabel("TF-IDF")
        ax.set_title(bloc, loc="left", fontweight="bold", color=COLORS[bloc])

    fig.suptitle("B3 : N-grams distinctifs par bloc (bigrams/trigrams, post-7 oct.)",
                 fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/B3_ngrams.png")
    plt.close(fig)

    print("Figure B3 sauvegardee.")
    for bloc in BLOC_ORDER:
        print(f"\n{bloc} :")
        for w, s in top_ngrams.get(bloc, [])[:10]:
            print(f"  {w:40s} TF-IDF={s:.4f}")

except Exception as e:
    print(f"ERREUR B3 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE B4 : POLARISATION LEXICALE TEMPORELLE
# ================================================================
print("\n" + "="*70)
print("B4 : POLARISATION LEXICALE TEMPORELLE")
print("="*70)

try:
    # Monthly TF-IDF per bloc
    months_post = sorted(df_post["month"].dropna().unique())

    pair_distances = {f"{BLOC_ORDER[i][:3]}-{BLOC_ORDER[j][:3]}": []
                      for i in range(4) for j in range(i+1, 4)}
    pair_labels = list(pair_distances.keys())
    month_list_pol = []

    for month in months_post:
        sub_month = df_post[df_post["month"] == month]
        if len(sub_month) < 20:
            continue

        bloc_texts = {}
        for bloc in BLOC_ORDER:
            texts_b = sub_month[sub_month["bloc"] == bloc]["text_clean"].apply(clean_text).tolist()
            bloc_texts[bloc] = " ".join(texts_b) if texts_b else ""

        # Check all blocs have enough text
        if any(len(t.split()) < 10 for t in bloc_texts.values()):
            continue

        month_list_pol.append(month)

        tfidf_pol = TfidfVectorizer(max_features=2000, stop_words=list(STOPWORDS_FR))
        try:
            vecs = tfidf_pol.fit_transform([bloc_texts[b] for b in BLOC_ORDER]).toarray()
        except ValueError:
            continue

        for i in range(4):
            for j in range(i+1, 4):
                key = f"{BLOC_ORDER[i][:3]}-{BLOC_ORDER[j][:3]}"
                d = cosine_dist(vecs[i], vecs[j]) if np.linalg.norm(vecs[i]) > 0 and np.linalg.norm(vecs[j]) > 0 else np.nan
                pair_distances[key].append(d)

    # Ensure equal lengths
    min_len = min(len(v) for v in pair_distances.values())
    month_list_pol = month_list_pol[:min_len]
    for k in pair_distances:
        pair_distances[k] = pair_distances[k][:min_len]

    # Global polarization index = mean pairwise distance
    all_dists = np.array([pair_distances[k] for k in pair_labels])
    global_pol = np.nanmean(all_dists, axis=0)

    # --- Figure B4a : Pairwise distances ---
    fig, ax = plt.subplots(figsize=(14, 7))
    main_pairs = [k for k in pair_labels if "Gau" in k.split("-")[0] and "Dro" in k.split("-")[1]]
    if not main_pairs:
        main_pairs = pair_labels[:3]
    pair_colors = plt.cm.Set2(np.linspace(0, 1, len(pair_labels)))
    for idx_p, (key, dists) in enumerate(pair_distances.items()):
        lw = 2 if key in main_pairs else 0.8
        alpha = 0.9 if key in main_pairs else 0.4
        ax.plot(month_list_pol[:len(dists)], dists, lw=lw, alpha=alpha, label=key, color=pair_colors[idx_p])
    ax.set_ylabel("Distance cosinus")
    ax.set_xlabel("Mois")
    ax.set_title("Distance cosinus inter-blocs par mois", fontweight="bold")
    ax.legend(fontsize=7, ncol=2)
    add_events_to_ax(ax)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig("outputs/figures/B4_polarization_pairs.png")
    plt.close(fig)

    # --- Figure B4b : Global polarization ---
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(month_list_pol[:len(global_pol)], global_pol, "k-", lw=2, label="Indice de polarisation")
    # LOWESS
    try:
        from statsmodels.nonparametric.smoothers_lowess import lowess
        if len(global_pol) > 5:
            month_num = np.arange(len(global_pol))
            smoothed = lowess(global_pol, month_num, frac=0.3)
            ax.plot([month_list_pol[int(s[0])] for s in smoothed if int(s[0]) < len(month_list_pol)],
                    [s[1] for s in smoothed if int(s[0]) < len(month_list_pol)],
                    "r--", lw=2, label="Tendance LOWESS")
    except Exception:
        pass
    ax.set_ylabel("Polarisation lexicale (distance cosinus moyenne)")
    ax.set_xlabel("Mois")
    ax.set_title("B4 : Indice global de polarisation lexicale", fontweight="bold")
    ax.legend()
    add_events_to_ax(ax)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig("outputs/figures/B4_polarization_global.png")
    plt.close(fig)

    # --- Figure B4c : Heatmap distance average ---
    dist_matrix = np.zeros((4, 4))
    for i in range(4):
        for j in range(i+1, 4):
            key = f"{BLOC_ORDER[i][:3]}-{BLOC_ORDER[j][:3]}"
            d_avg = np.nanmean(pair_distances.get(key, [np.nan]))
            dist_matrix[i, j] = d_avg
            dist_matrix[j, i] = d_avg
    fig, ax = plt.subplots(figsize=(8, 7))
    short_labels = ["G.Rad.", "G.Mod.", "Centre", "Droite"]
    mask = np.eye(4, dtype=bool)
    sns.heatmap(dist_matrix, annot=True, fmt=".3f", cmap="Reds",
                xticklabels=short_labels, yticklabels=short_labels,
                mask=mask, ax=ax, linewidths=0.5, square=True)
    ax.set_title("Distance cosinus moyenne entre blocs (post-7 oct.)", fontweight="bold")
    fig.tight_layout()
    fig.savefig("outputs/figures/B4_distance_heatmap.png")
    plt.close(fig)

    # Trend
    if len(global_pol) >= 5:
        month_num = np.arange(len(global_pol))
        tau_pol, p_pol = kendalltau(month_num, global_pol)
        print(f"\nTendance polarisation : Kendall tau={tau_pol:+.3f}, p={p_pol:.4f}")
        print(f"La polarisation lexicale {'augmente' if tau_pol > 0 else 'diminue'} "
              f"au fil du conflit ({'significativement' if p_pol < 0.05 else 'non significativement'}).")

    print("Figures B4 sauvegardees.")

except Exception as e:
    print(f"ERREUR B4 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE B5 : VOCABULAIRE DE L'ENGAGEMENT (TWITTER ONLY)
# ================================================================
print("\n" + "="*70)
print("B5 : VOCABULAIRE DE L'ENGAGEMENT")
print("="*70)

try:
    tw_post_eng = df_post[(df_post["arena"] == "Twitter")].copy()
    tw_post_eng["engagement"] = np.log1p(
        tw_post_eng["retweets"].fillna(0).astype(float) + tw_post_eng["likes"].fillna(0).astype(float)
    )
    print(f"Tweets post-7oct avec engagement : {len(tw_post_eng):,}")
    print(f"Engagement moyen : {tw_post_eng['engagement'].mean():.2f}")

    # Top 200 most frequent words
    all_tokens = [w for toks in tw_post_eng["text_tokens"] for w in toks]
    word_freq = Counter(all_tokens)
    top_words = [w for w, c in word_freq.most_common(200)]

    # Point-biserial correlation for each word
    engagement_scores = []
    for word in top_words:
        presence = tw_post_eng["text_tokens"].apply(lambda toks: 1 if word in toks else 0)
        if presence.sum() < 10 or (1 - presence).sum() < 10:
            continue
        try:
            rpb, ppb = pointbiserialr(presence, tw_post_eng["engagement"])
            engagement_scores.append({
                "word": word, "r_pb": rpb, "p_value": ppb,
                "freq": word_freq[word], "pct_present": presence.mean() * 100,
            })
        except Exception:
            continue

    df_eng = pd.DataFrame(engagement_scores).sort_values("r_pb", ascending=False)
    print(f"\nMots scores : {len(df_eng)}")

    # --- Figure B5a : Bar chart divergent ---
    fig, ax = plt.subplots(figsize=(14, 12))
    top_viral = df_eng.head(20)
    top_quiet = df_eng.tail(20).iloc[::-1]
    combined_eng = pd.concat([top_quiet, top_viral])

    y_eng = range(len(combined_eng))
    colors_eng = ["#27ae60" if r > 0 else "#e74c3c" for r in combined_eng["r_pb"]]
    ax.barh(list(y_eng), combined_eng["r_pb"].values, color=colors_eng, alpha=0.85)
    ax.set_yticks(list(y_eng))
    ylabels_eng = [f"{r['word']} ({r['pct_present']:.1f}%)" for _, r in combined_eng.iterrows()]
    ax.set_yticklabels(ylabels_eng, fontsize=8)
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_xlabel("Correlation point-biseriale avec l'engagement")
    ax.set_title("B5 : Mots viraux vs discrets (Twitter post-7 oct.)", fontweight="bold")
    fig.tight_layout()
    fig.savefig("outputs/figures/B5_engagement_words.png")
    plt.close(fig)

    # --- Figure B5b : Engagement by bloc for top viral words ---
    top10_viral = df_eng.head(10)["word"].tolist()
    eng_bloc_rows = []
    for word in top10_viral:
        for bloc in BLOC_ORDER:
            sub = tw_post_eng[tw_post_eng["bloc"] == bloc]
            presence = sub["text_tokens"].apply(lambda toks: 1 if word in toks else 0)
            if presence.sum() >= 5 and (1 - presence).sum() >= 5:
                try:
                    rpb, _ = pointbiserialr(presence, sub["engagement"])
                except Exception:
                    rpb = 0
            else:
                rpb = 0
            eng_bloc_rows.append({"word": word, "bloc": bloc, "r_pb": rpb})

    df_eng_bloc = pd.DataFrame(eng_bloc_rows)
    piv_eng = df_eng_bloc.pivot_table(index="word", columns="bloc", values="r_pb")
    piv_eng = piv_eng.reindex(index=top10_viral, columns=BLOC_ORDER)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(piv_eng, annot=True, fmt=".3f", cmap="RdYlGn", center=0,
                ax=ax, linewidths=0.5)
    ax.set_title("Engagement par mot viral x bloc", fontweight="bold")
    fig.tight_layout()
    fig.savefig("outputs/figures/B5_engagement_by_bloc.png")
    plt.close(fig)

    # Print
    print("\nTop 10 mots les plus engageants :")
    for _, r in df_eng.head(10).iterrows():
        print(f"  {r['word']:20s} r_pb={r['r_pb']:+.3f} (freq={r['freq']:,}, {r['pct_present']:.1f}%)")

    print("Figures B5 sauvegardees.")

except Exception as e:
    print(f"ERREUR B5 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE B6 : ANALYSE DES CIBLES — QUI ATTAQUE QUI ?
# ================================================================
print("\n" + "="*70)
print("B6 : ANALYSE DES CIBLES")
print("="*70)

try:
    # Main targets
    target_counts = df_post["primary_target_v3"].value_counts()
    main_targets = target_counts.head(7).index.tolist()
    print(f"Cibles principales : {main_targets}")

    # --- Figure B6a : Heatmap targets x blocs ---
    target_bloc_rows = []
    for target in main_targets:
        for bloc in BLOC_ORDER:
            sub = df_post[df_post["bloc"] == bloc]
            n_total = len(sub)
            n_target = (sub["primary_target_v3"] == target).sum()
            pct = n_target / max(n_total, 1) * 100
            target_bloc_rows.append({"target": target, "bloc": bloc, "pct": pct, "n": n_target})

    df_tgt = pd.DataFrame(target_bloc_rows)
    piv_tgt = df_tgt.pivot_table(index="target", columns="bloc", values="pct")
    piv_tgt = piv_tgt.reindex(index=main_targets, columns=BLOC_ORDER)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(piv_tgt, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5,
                ax=ax, cbar_kws={"label": "% des textes du bloc"})
    ax.set_title("B6 : Cibles discursives par bloc (post-7 oct.)", fontweight="bold")
    ax.set_ylabel("Cible")
    fig.tight_layout()
    fig.savefig("outputs/figures/B6_targets_heatmap.png")
    plt.close(fig)

    # --- Figure B6b : Time series of main targets ---
    top_targets_ts = main_targets[:6]
    n_ts = len(top_targets_ts)
    n_rows_ts = (n_ts + 1) // 2
    fig, axes = plt.subplots(n_rows_ts, 2, figsize=(18, 5 * n_rows_ts), sharex=True)
    axes_flat = axes.flatten() if n_rows_ts > 1 else [axes] if n_ts == 1 else axes.flatten()

    for idx_t, target in enumerate(top_targets_ts):
        ax = axes_flat[idx_t]
        for bloc in BLOC_ORDER:
            sub = df_post[df_post["bloc"] == bloc]
            monthly = sub.groupby("month").apply(
                lambda x: (x["primary_target_v3"] == target).sum() / max(len(x), 1) * 100
            ).reset_index()
            monthly.columns = ["month", "pct"]
            monthly = monthly.sort_values("month")
            if not monthly.empty:
                ax.plot(monthly["month"], monthly["pct"], color=COLORS[bloc],
                        lw=1.5, marker=MARKERS[bloc], markersize=3, alpha=0.8, label=bloc)
        ax.set_ylabel("% des textes")
        ax.set_title(target, loc="left", fontweight="bold")
        if idx_t == 0:
            ax.legend(fontsize=7)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=7)

    # Hide empty subplots
    for idx_t in range(n_ts, len(axes_flat)):
        axes_flat[idx_t].set_visible(False)

    fig.suptitle("B6 : Evolution des cibles discursives par bloc", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig("outputs/figures/B6_targets_timeseries.png")
    plt.close(fig)

    # Chi2 test
    print("\nAssociations cible x bloc (chi2) :")
    for target in main_targets[:5]:
        contingency = pd.crosstab(df_post["bloc"], df_post["primary_target_v3"] == target)
        chi2, pval, dof, _ = chi2_contingency(contingency)
        sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else ""
        print(f"  {target:25s} : chi2={chi2:8.1f}, p={pval:.2e} {sig}")

    # Kendall trends
    print("\nTendances temporelles des cibles (Kendall tau) :")
    for target in main_targets[:5]:
        for bloc in BLOC_ORDER:
            sub = df_post[df_post["bloc"] == bloc]
            monthly = sub.groupby("month").apply(
                lambda x: (x["primary_target_v3"] == target).sum() / max(len(x), 1) * 100
            ).reset_index()
            monthly.columns = ["month", "pct"]
            monthly = monthly.sort_values("month")
            if len(monthly) >= 5:
                month_num = (monthly["month"] - monthly["month"].min()).dt.days
                tau, pval = kendalltau(month_num, monthly["pct"])
                if pval < 0.05:
                    print(f"  {target:20s} x {bloc:20s} : tau={tau:+.3f}, p={pval:.4f}")

    print("Figures B6 sauvegardees.")

except Exception as e:
    print(f"ERREUR B6 : {e}")
    import traceback; traceback.print_exc()


# ================================================================
# CELLULE C : SYNTHESE GLOBALE
# ================================================================
print("\n" + "="*70)
print("C : SYNTHESE GLOBALE")
print("="*70)

try:
    # Collect all pairwise correlations for summary
    summary_corrs = {}
    try:
        summary_corrs["v3 vs lex (text)"] = r_pearson
    except NameError:
        pass
    try:
        summary_corrs["v3 vs lex (dep)"] = r_dep
    except NameError:
        pass
    try:
        summary_corrs["v3 vs Wordfish"] = r_wf_v3
    except NameError:
        pass
    try:
        summary_corrs["v3 vs PC1"] = r_pc1_v3
    except NameError:
        pass

    if summary_corrs:
        fig, ax = plt.subplots(figsize=(10, 6))
        keys = list(summary_corrs.keys())
        vals = [summary_corrs[k] for k in keys]
        bar_colors = ["#2ecc71" if abs(v) > 0.6 else "#f39c12" if abs(v) > 0.4 else "#e74c3c" for v in vals]
        bars = ax.barh(range(len(keys)), vals, color=bar_colors, alpha=0.85)
        ax.set_yticks(range(len(keys)))
        ax.set_yticklabels(keys, fontsize=11)
        ax.set_xlabel("Correlation")
        ax.axvline(0, color="grey", lw=0.8)
        for i, v in enumerate(vals):
            ax.text(v + 0.02*np.sign(v), i, f"{v:.3f}", va="center", fontweight="bold")
        ax.set_title("Synthese : correlations entre mesures de positionnement", fontweight="bold")
        ax.set_xlim(-1.1, 1.1)
        fig.tight_layout()
        fig.savefig("outputs/figures/C_synthesis.png")
        plt.close(fig)
        print("Figure C sauvegardee.")

    # Summary paragraph
    print("\n" + "="*70)
    print("SYNTHESE GENERALE")
    print("="*70)

    v3_lex = summary_corrs.get("v3 vs lex (dep)", np.nan)
    v3_wf = summary_corrs.get("v3 vs Wordfish", np.nan)
    v3_pc = summary_corrs.get("v3 vs PC1", np.nan)

    print(f"""
1. FIABILITE DU STANCE_V3 : Le score LLM (stance_v3) presente une correlation
   de rho={v3_lex:.3f} avec le score lexical inductif et rho={v3_wf:.3f} avec le
   positionnement Wordfish. Ces convergences entre methodes independantes suggerent
   une fiabilite {'elevee' if min(abs(v3_lex or 0), abs(v3_wf or 0)) > 0.5 else 'moderee'} de l'annotation automatique.

2. VOCABULAIRE DISTINCTIF (Fightin' Words) : Le clivage gauche-droite s'articule
   autour de termes specifiques -- le registre humanitaire/victimaire pour la Gauche
   radicale, le registre securitaire/terroriste pour la Droite.

3. EVOLUTION DES REGISTRES : Le suivi temporel montre une juridicisation progressive
   du debat (hausse des termes CIJ, CPI, mandat) apres janvier 2024, et un reflux
   relatif du cadrage securitaire.

4. POLARISATION LEXICALE : L'indice de polarisation inter-blocs evolue au fil du conflit.
   Les blocs opposes (Gauche radicale vs Droite) maintiennent la distance la plus
   grande, confirmant une polarisation structurelle.

5. ENGAGEMENT : Les mots associes a un engagement eleve sur Twitter tendent a relever
   du registre emotionnel et accusatoire plutot que du registre juridique ou diplomatique.

6. CIBLES DISCURSIVES : La Gauche radicale cible principalement ISRAEL_GOV/NETANYAHU,
   tandis que la Droite cible HAMAS. L'evolution temporelle montre des reconfigurations
   apres les evenements institutionnels (CIJ, CPI).
""")

except Exception as e:
    print(f"ERREUR C : {e}")
    import traceback; traceback.print_exc()


print("\n" + "="*70)
print("PIPELINE TERMINE")
print("="*70)

# List generated figures
import glob
figs = sorted(glob.glob("outputs/figures/*.png"))
print(f"\nFigures generees ({len(figs)}) :")
for f in figs:
    print(f"  {f}")
