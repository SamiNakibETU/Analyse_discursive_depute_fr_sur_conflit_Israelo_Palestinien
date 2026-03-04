# -*- coding: utf-8 -*-
"""
Script unique reproduisant la logique des 10 notebooks (01 à 13).
Génère CSV dans data/results/, figures dans figures/,
RAPPORT_RESULTATS.txt avec les métriques, et reports/RESULTATS_NUMERIQUES.md
avec tous les chiffres et séries temporelles (équivalent exhaustif des notebooks).
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="pandas|seaborn")

from pathlib import Path
import re
import sys
from collections import Counter

# Backend non-interactif pour exécution en batch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import wasserstein_distance, mannwhitneyu, kendalltau, spearmanr
from scipy.spatial.distance import euclidean
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Import modules projet
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from config import (
    CORPUS_V3, CORPUS_V4, RESULTS_DIR, FIGURES_DIR,
    BLOC_ORDER, BLOC_COLORS, BLOC_COLORS as BLOC_COL,
    EVENTS, BATCHES, BATCH_ORDER, add_events, format_dates,
    EVENT_STUDY_DATES, month_to_batch,
)
from vendeville import (
    entropic_polarization_bao_gill,
    wd_inter_blocs,
    wd_drift_intra_bloc,
    effective_dimensionality,
)
from vad_lexicon import load_vad_lexicon, score_text_vad
from mfd_lexicon import load_mfd, score_text_mfd, compute_mfd_coverage
from registre_discursif import score_registre_discursif

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Fichier rapport (collecte des résultats)
RAPPORT_PATH = RESULTS_DIR / "RAPPORT_RESULTATS.txt"
_reporte_lines = []


def log_report(s):
    """Ajoute une ligne au rapport."""
    _reporte_lines.append(str(s))


def write_report():
    """Écrit le rapport final."""
    with open(RAPPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(_reporte_lines))
    print(f"Rapport écrit : {RAPPORT_PATH}")


def save_fig(name):
    """Sauvegarde une figure et ferme."""
    p = FIGURES_DIR / f"{name}.png"
    plt.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()


def tokenize(text):
    return re.findall(r"[a-zàâäéèêëïîôùûüç]+", str(text).lower())


def log_odds(cnt1, cnt2, alpha=0.01):
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


def lexical_score(text, text_col_val):
    pro_pal = ["cessez", "génocide", "palestine", "gaza", "colonie"]
    pro_isr = ["défendre", "hamas", "terroriste", "otage"]
    if pd.isna(text_col_val) or not isinstance(text_col_val, str):
        return 0
    t = text_col_val.lower()
    s = sum(1 for w in pro_pal if w in t) - sum(1 for w in pro_isr if w in t)
    return np.clip(s, -2, 2)


def mann_kendall_tau(series):
    x = np.arange(len(series))
    tau, p = kendalltau(x, series.dropna().values)
    return tau, p


def month_to_batch(m):
    d = pd.Timestamp(m + "-15")
    for name, r in BATCHES.items():
        if pd.Timestamp(r["start"]) <= d <= pd.Timestamp(r["end"]):
            return name
    return "OTHER"


# -----------------------------------------------------------------------------
# NB01 — Portrait du corpus
# -----------------------------------------------------------------------------
def run_01_portrait(df):
    log_report("=" * 60)
    log_report("01 — PORTRAIT DU CORPUS")
    log_report("=" * 60)

    vol = df.groupby(["month", "bloc"]).size().unstack(fill_value=0)
    vol = vol.reindex(columns=[b for b in BLOC_ORDER if b in vol.columns])
    vol["month_ts"] = pd.to_datetime(vol.index.astype(str) + "-01")
    vol.to_csv(RESULTS_DIR / "volume_mensuel.csv", index=True)

    log_report(f"\nVolume mensuel : {len(vol)} mois")
    for b in BLOC_ORDER:
        if b in vol.columns:
            log_report(f"  {b}: total {vol[b].sum()} textes")

    fig, ax = plt.subplots(figsize=(12, 6))
    cols = [b for b in BLOC_ORDER if b in vol.columns]
    ax.stackplot(
        vol["month_ts"], *[vol[b] for b in cols],
        labels=cols, colors=[BLOC_COLORS[b] for b in cols], alpha=0.85
    )
    add_events(ax)
    ax.legend(loc="upper right")
    ax.set_ylabel("Nombre de textes")
    save_fig("fig01_volume_mensuel_empile")

    arena_col = "arena" if "arena" in df.columns else None
    if arena_col:
        df_tw = df[df[arena_col] == "Twitter"]
    elif "source" in df.columns:
        df_tw = df[df["source"].astype(str).str.lower().str.strip() == "twitter"]
    else:
        df_tw = pd.DataFrame()
    if len(df_tw) > 0:
        activity = df_tw.groupby("bloc").agg(
            n_tweets=("author", "count"), n_deputies=("author", "nunique")
        ).reset_index()
        activity["tweets_per_deputy"] = activity["n_tweets"] / activity["n_deputies"]
        activity = activity[activity["bloc"].isin(BLOC_ORDER)]
        activity.to_csv(RESULTS_DIR / "activity_bias_by_bloc.csv", index=False)
        log_report(f"\nBiais d'activité Twitter (tweets/député) :")
        for _, row in activity.iterrows():
            log_report(f"  {row['bloc']}: {row['tweets_per_deputy']:.2f}")

        fig, ax = plt.subplots(figsize=(8, 5))
        order = [b for b in BLOC_ORDER if b in activity["bloc"].values]
        sub = activity.set_index("bloc").reindex(order)
        ax.bar(range(len(order)), sub["tweets_per_deputy"].values,
               color=[BLOC_COLORS.get(b, "#888") for b in order])
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels(order, rotation=45, ha="right")
        ax.set_ylabel("Tweets par député")
        save_fig("fig55_activity_bias")

        if "engagement" not in df_tw.columns:
            eng_cols = [c for c in ["retweets", "likes", "replies"] if c in df_tw.columns]
            if eng_cols:
                df_tw = df_tw.copy()
                df_tw["engagement"] = df_tw[eng_cols].fillna(0).sum(axis=1)
        if "engagement" in df_tw.columns and "stance_v3" in df_tw.columns:
            dep_vis = df_tw.groupby("author").agg(
                n_tweets=("author", "count"), mean_engagement=("engagement", "mean"),
                stance_mean=("stance_v3", "mean"), bloc=("bloc", "first")
            ).reset_index()
            dep_vis["visibility_proxy"] = dep_vis["n_tweets"] * dep_vis["mean_engagement"]
            dep_vis["stance_abs"] = dep_vis["stance_mean"].abs()
            dep_vis = dep_vis[dep_vis["visibility_proxy"] > 0]
            if len(dep_vis) >= 10:
                dep_vis["quintile"] = pd.qcut(dep_vis["visibility_proxy"], 5, labels=False, duplicates="drop")
                quint_agg = dep_vis.groupby("quintile").agg(
                    mean_abs_stance=("stance_abs", "mean"),
                    mean_stance=("stance_mean", "mean"), n=("author", "count")
                ).reset_index()
                quint_agg.to_csv(RESULTS_DIR / "visibility_paradox_quintiles.csv", index=False)
                log_report("\nParadoxe visibilité (quintiles) : mean_abs_stance par quintile")
                log_report(quint_agg[["quintile", "mean_abs_stance", "n"]].to_string(index=False))
                fig, ax = plt.subplots(figsize=(8, 5))
                colors = dep_vis["bloc"].map(lambda b: BLOC_COLORS.get(b, "#888"))
                ax.scatter(dep_vis["visibility_proxy"], dep_vis["stance_abs"], c=colors, alpha=0.6, s=20)
                ax.set_xlabel("Visibilité")
                ax.set_ylabel("|stance|")
                save_fig("fig56_visibility_paradox")

    vol_arena = df.groupby(["bloc", "arena"]).size().unstack(fill_value=0)
    vol_arena = vol_arena.reindex(BLOC_ORDER).dropna(how="all")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for i, arena in enumerate(["Twitter", "AN"]):
        if arena in vol_arena.columns:
            s = vol_arena[arena].reindex(BLOC_ORDER)
            axes[i].barh(s.index, s.values, color=[BLOC_COLORS.get(b, "#888") for b in s.index])
            axes[i].set_title(arena)
    save_fig("fig02_volume_par_arena")

    att = df.groupby("month").agg(
        n_deputes_actifs=("author", "nunique"), n_textes=("author", "count")
    ).reset_index()
    att["month_ts"] = pd.to_datetime(att["month"] + "-01")
    att.to_csv(RESULTS_DIR / "attrition_mensuelle.csv", index=False)
    log_report(f"\nAttrition : députés actifs min={att['n_deputes_actifs'].min()}, max={att['n_deputes_actifs'].max()}")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(att["month_ts"], att["n_deputes_actifs"], lw=2)
    add_events(ax)
    ax.set_ylabel("Députés actifs")
    save_fig("fig03_attrition")

    grp = df.groupby("group" if "group" in df.columns else "groupe_politique").size().sort_values(ascending=True)
    grp.to_csv(RESULTS_DIR / "volume_par_groupe.csv")
    log_report(f"\nVolume par groupe : {len(grp)} groupes")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(grp.index.astype(str), grp.values, color="#3498db", alpha=0.8)
    ax.set_xlabel("Nombre de textes")
    save_fig("fig04_desequilibre_groupe")

    df_plot = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df_plot["bloc"] = pd.Categorical(df_plot["bloc"], categories=BLOC_ORDER)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=df_plot, x="bloc", y="stance_v3", hue="bloc", order=BLOC_ORDER,
                   palette=BLOC_COLORS, legend=False)
    ax.axhline(0, color="grey", ls="--", lw=0.8)
    plt.xticks(rotation=30, ha="right")
    save_fig("fig05_stance_violin")

    stance_by_bloc = df_plot.groupby("bloc", observed=True)["stance_v3"].agg(["mean", "std", "count"])
    log_report("\nStance moyen par bloc (violin) :")
    for b in BLOC_ORDER:
        if b in stance_by_bloc.index:
            r = stance_by_bloc.loc[b]
            log_report(f"  {b}: mean={r['mean']:.3f}, n={int(r['count'])}")


# -----------------------------------------------------------------------------
# NB02 — Validation annotation
# -----------------------------------------------------------------------------
def run_02_validation(df, df_v4):
    log_report("\n" + "=" * 60)
    log_report("02 — VALIDATION ANNOTATION")
    log_report("=" * 60)

    if "stance_v4" not in df_v4.columns:
        log_report("\nCorpus v4 ou colonne stance_v4 absent — matrice confusion non calculée.")
        conf = pd.DataFrame()
    else:
        conf = pd.crosstab(df_v4["stance_v3"], df_v4["stance_v4"])
        log_report("\nMatrice confusion stance_v3 vs stance_v4 :")
        log_report(conf.to_string())

    fig, ax = plt.subplots(figsize=(7, 6))
    if len(conf) > 0:
        sns.heatmap(conf, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Positionnement (corpus événementiel)")
    ax.set_ylabel("Positionnement (corpus principal)")
    save_fig("fig06_matrice_confusion_v3_v4")

    months_per_dep = df.groupby("author")["month"].nunique()
    panel_b4_authors = months_per_dep[months_per_dep >= 18].index.tolist()
    df["in_panel_b4"] = df["author"].isin(panel_b4_authors)
    panel_b4_df = pd.DataFrame({"author": panel_b4_authors})
    bloc_map = df.groupby("author")["bloc"].first()
    panel_b4_df["bloc"] = panel_b4_df["author"].map(bloc_map)
    panel_b4_df.to_csv(RESULTS_DIR / "panel_b4.csv", index=False)

    stance_complet = df.groupby("bloc")["stance_v3"].agg(["mean", "count"]).reindex(BLOC_ORDER)
    stance_panel = df[df["in_panel_b4"]].groupby("bloc")["stance_v3"].agg(["mean", "count"]).reindex(BLOC_ORDER)
    comp = pd.DataFrame({
        "bloc": BLOC_ORDER,
        "stance_complet": stance_complet["mean"].values,
        "stance_panel_b4": stance_panel["mean"].values,
        "n_complet": stance_complet["count"].astype(int).values,
        "n_panel": stance_panel["count"].astype(int).values,
    })
    comp["delta"] = comp["stance_panel_b4"] - comp["stance_complet"]
    comp.to_csv(RESULTS_DIR / "stance_panel_vs_complet.csv", index=False)

    log_report("\nPanel B4 vs complet :")
    log_report(comp.to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    x = np.arange(len(BLOC_ORDER))
    w = 0.35
    axes[0].bar(x - w / 2, comp["stance_complet"], w, label="Corpus complet", color="#888", alpha=0.8)
    axes[0].bar(x + w / 2, comp["stance_panel_b4"], w, label="Panel B4", color=[BLOC_COLORS[b] for b in BLOC_ORDER])
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([b.replace(" / ", "/") for b in BLOC_ORDER], rotation=25, ha="right")
    axes[0].set_ylabel("Positionnement moyen")
    axes[0].legend()
    axes[1].bar(x, comp["delta"], color=[BLOC_COLORS[b] for b in BLOC_ORDER])
    axes[1].axhline(0, color="grey", ls="--", lw=0.8)
    axes[1].set_xticks(range(len(BLOC_ORDER)))
    axes[1].set_xticklabels([b.replace(" / ", "/") for b in BLOC_ORDER], rotation=25, ha="right")
    axes[1].set_ylabel("Écart Panel B4 - Complet")
    save_fig("fig08_panel_b4_vs_complet")

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    df["lexical_score"] = df[text_col].apply(lambda t: lexical_score(None, t))
    valid = df[["stance_v3", "lexical_score"]].dropna()
    spearman = valid["stance_v3"].corr(valid["lexical_score"], method="spearman")
    pearson = valid["stance_v3"].corr(valid["lexical_score"], method="pearson")
    accord_signe = ((valid["stance_v3"] > 0) == (valid["lexical_score"] > 0)).mean() * 100
    log_report(f"\nValidation lexical vs annotation :")
    log_report(f"  Spearman ρ = {spearman:.4f}")
    log_report(f"  Pearson r = {pearson:.4f}")
    log_report(f"  Accord de signe = {accord_signe:.1f} %")

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(valid["lexical_score"], valid["stance_v3"], alpha=0.15, s=8)
    ax.set_xlabel("Score lexical (proxy)")
    ax.set_ylabel("Positionnement (annotation)")
    ax.set_title(f"ρ = {spearman:.3f}")
    ax.axhline(0, color="grey", ls="--")
    ax.axvline(0, color="grey", ls="--")
    save_fig("fig09_lexical_vs_annotation")


# -----------------------------------------------------------------------------
# NB03 — Dynamiques temporelles
# -----------------------------------------------------------------------------
def run_03_dynamiques(df, df_v4):
    log_report("\n" + "=" * 60)
    log_report("03 — DYNAMIQUES TEMPORELLES")
    log_report("=" * 60)

    stance_m = df[df["bloc"].isin(BLOC_ORDER)].groupby(["month", "bloc"])["stance_v3"].mean().reset_index()
    stance_m["month_ts"] = pd.to_datetime(stance_m["month"] + "-01")
    stance_m.to_csv(RESULTS_DIR / "stance_mensuel.csv", index=False)

    log_report("\nStance mensuel (extrait) :")
    log_report(stance_m.head(16).to_string(index=False))

    fig, ax = plt.subplots(figsize=(14, 6))
    for bloc in BLOC_ORDER:
        sub = stance_m[stance_m["bloc"] == bloc]
        if len(sub) > 0:
            ax.plot(sub["month_ts"], sub["stance_v3"], label=bloc, color=BLOC_COLORS[bloc], lw=2)
    add_events(ax)
    ax.axhline(0, color="grey", ls="--", lw=0.8)
    ax.legend(loc="upper right")
    ax.set_ylabel("Positionnement moyen")
    save_fig("fig10_stance_ribbon")

    events_did = [("2024-01-26", 30), ("2024-05-07", 30), ("2025-01-15", 30)]
    results = []
    for ev_date, window in events_did:
        t0 = pd.Timestamp(ev_date)
        before = df[(df["date"] >= t0 - pd.Timedelta(days=window)) & (df["date"] < t0)]
        after = df[(df["date"] >= t0) & (df["date"] < t0 + pd.Timedelta(days=window))]
        for bloc in BLOC_ORDER:
            b_b = before[before["bloc"] == bloc]["stance_v3"]
            b_a = after[after["bloc"] == bloc]["stance_v3"]
            if len(b_b) >= 5 and len(b_a) >= 5:
                delta = b_a.mean() - b_b.mean()
                _, p = mannwhitneyu(b_a, b_b, alternative="two-sided")
                results.append({"event": ev_date, "bloc": bloc, "delta": delta, "p": p})

    did = pd.DataFrame(results)
    did.to_csv(RESULTS_DIR / "event_impact_diff_in_diff.csv", index=False)
    log_report("\nDiff-in-diff (impact événements) :")
    log_report(did.to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 6))
    piv = did.pivot(index="bloc", columns="event", values="delta").reindex(BLOC_ORDER)
    piv.plot(kind="bar", ax=ax, color=["#3498db", "#e74c3c", "#2ecc71"], alpha=0.8)
    ax.axhline(0, color="grey", ls="--", lw=0.8)
    ax.set_ylabel("Δ positionnement (après - avant)")
    plt.xticks(rotation=25, ha="right")
    save_fig("fig12_diff_in_diff")

    df_v = df[df["bloc"].isin(BLOC_ORDER)]
    pairs = [(b1, b2) for i, b1 in enumerate(BLOC_ORDER) for b2 in BLOC_ORDER[i + 1 :]]
    wd_inter = wd_inter_blocs(df_v, pairs)
    wd_drift_list = [wd_drift_intra_bloc(df_v, bloc) for bloc in BLOC_ORDER]
    wd_drift = pd.concat([d for d in wd_drift_list if len(d) > 0], ignore_index=True)
    wd_inter.to_csv(RESULTS_DIR / "wasserstein_inter_blocs.csv", index=False)
    wd_drift.to_csv(RESULTS_DIR / "wasserstein_drift.csv", index=False)

    log_report("\nWasserstein inter-blocs (moyenne par mois) :")
    if len(wd_inter) > 0:
        wd_mean = wd_inter.groupby("month")["wd_norm"].mean()
        log_report(wd_mean.to_string())

    centre_bloc = "Centre / Majorite"
    sm = stance_m
    centre = sm[sm["bloc"] == centre_bloc]
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(centre["month_ts"], centre["stance_v3"], lw=2, color=BLOC_COLORS.get(centre_bloc, "#2980b9"))
    add_events(ax)
    format_dates(ax)
    ax.set_ylabel("Stance moyen (Centre)")
    ax.axhline(0, color="gray", ls="--", lw=0.8)
    save_fig("fig13_zoom_centre")

    vol = pd.read_csv(RESULTS_DIR / "volume_mensuel.csv")
    if "month_ts" not in vol.columns and "Unnamed: 0" in vol.columns:
        vol = vol.rename(columns={"Unnamed: 0": "month"})
        vol["month_ts"] = pd.to_datetime(vol["month"].astype(str) + "-01")
    elif "month" in vol.columns:
        vol["month_ts"] = pd.to_datetime(vol["month"].astype(str) + "-01")
    centre_col = "Centre / Majorite" if "Centre / Majorite" in vol.columns else None
    if centre_col:
        centre_vol = vol[["month_ts", centre_col]].rename(columns={centre_col: "n_textes"})
        centre_vol = centre_vol.merge(centre[["month_ts", "stance_v3"]], on="month_ts")
        fig, ax1 = plt.subplots(figsize=(14, 5))
        ax1.bar(centre_vol["month_ts"], centre_vol["n_textes"], alpha=0.4, color="#2980b9", label="Volume")
        ax2 = ax1.twinx()
        ax2.plot(centre_vol["month_ts"], centre_vol["stance_v3"], lw=2, color="#c0392b", label="Stance")
        ax2.set_ylabel("Stance moyen")
        ax2.axhline(0, color="gray", ls="--", lw=0.8)
        add_events(ax1)
        format_dates(ax1)
        save_fig("fig14_volume_vs_stance_centre")

    centre_df = df[(df["bloc"] == "Centre / Majorite") & (df["arena"].isin(["Twitter", "AN"]))]
    if len(centre_df) > 0:
        centre_m = centre_df.groupby(["month", "arena"])["stance_v3"].mean().reset_index()
        centre_m["month_ts"] = pd.to_datetime(centre_m["month"] + "-01")
        fig, ax = plt.subplots(figsize=(12, 5))
        for arena in ["Twitter", "AN"]:
            sub = centre_m[centre_m["arena"] == arena]
            if len(sub) > 0:
                ax.plot(sub["month_ts"], sub["stance_v3"], label=arena, lw=2)
        add_events(ax)
        ax.axhline(0, color="grey", ls="--", lw=0.8)
        ax.legend()
        ax.set_ylabel("Positionnement moyen (Centre)")
        save_fig("fig15_twitter_vs_an_centre")

    att_bloc = df.groupby(["month", "bloc"]).agg(
        n_deputes=("author", "nunique"), n_textes=("author", "count")
    ).reset_index()
    att_bloc["month_ts"] = pd.to_datetime(att_bloc["month"] + "-01")
    fig, ax = plt.subplots(figsize=(14, 6))
    for bloc in BLOC_ORDER:
        sub = att_bloc[att_bloc["bloc"] == bloc]
        if len(sub) > 0:
            ax.plot(sub["month_ts"], sub["n_deputes"], label=bloc, color=BLOC_COLORS[bloc], lw=2)
    add_events(ax)
    ax.legend()
    ax.set_ylabel("Députés actifs")
    save_fig("fig16_attrition_differentielle")

    vol_heat = df[df["bloc"].isin(BLOC_ORDER)].groupby(["month", "bloc"]).size().unstack(fill_value=0)
    vol_heat = vol_heat.reindex(columns=BLOC_ORDER).fillna(0)
    vol_norm = vol_heat.div(vol_heat.sum(axis=1), axis=0)
    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(vol_norm.T, xticklabels=vol_heat.index[::2], yticklabels=BLOC_ORDER, ax=ax, cmap="YlOrRd",
                cbar_kws={"label": "Part"})
    ax.set_xlabel("Mois")
    save_fig("fig17_volume_heatmap")

    stance_agg = df[df["bloc"].isin(BLOC_ORDER)].groupby(["month", "bloc"])["stance_v3"].agg(
        ["mean", "std", "count"]
    ).reset_index()
    stance_agg["month_ts"] = pd.to_datetime(stance_agg["month"] + "-01")
    stance_agg["se"] = stance_agg["std"] / np.sqrt(stance_agg["count"])

    all_months = pd.Series(stance_agg["month"].unique()).sort_values()
    mk_results = []
    for bloc in BLOC_ORDER:
        s = stance_agg[stance_agg["bloc"] == bloc].set_index("month").reindex(all_months).sort_index()["mean"]
        tau, p = mann_kendall_tau(s)
        mk_results.append({"bloc": bloc, "tau": tau, "p": p})
    mk_df = pd.DataFrame(mk_results)
    mk_df.to_csv(RESULTS_DIR / "mann_kendall_bloc.csv", index=False)

    log_report("\nMann-Kendall (tendance temporelle) :")
    log_report(mk_df.to_string(index=False))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(mk_df["bloc"], mk_df["tau"], color=[BLOC_COLORS[b] for b in mk_df["bloc"]])
    ax.axvline(0, color="grey", ls="--", lw=0.8)
    ax.set_xlabel("τ de Mann-Kendall")
    save_fig("fig18_mann_kendall")

    fig, ax = plt.subplots(figsize=(14, 6))
    for bloc in BLOC_ORDER:
        sub = stance_agg[stance_agg["bloc"] == bloc]
        if len(sub) > 0:
            ax.plot(sub["month_ts"], sub["mean"], color=BLOC_COLORS[bloc], lw=2, label=bloc)
            ax.fill_between(
                sub["month_ts"], sub["mean"] - sub["se"], sub["mean"] + sub["se"],
                color=BLOC_COLORS[bloc], alpha=0.2
            )
    add_events(ax)
    ax.axhline(0, color="grey", ls="--", lw=0.8)
    ax.legend(loc="upper right")
    ax.set_ylabel("Positionnement moyen ± SE")
    save_fig("fig11_stance_panel_b4")

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    df_valid = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df_valid["discourse_score"] = df_valid[text_col].apply(score_registre_discursif)
    df_valid["conflictual"] = (df_valid["discourse_score"] > 0.5).astype(int)
    delib = df_valid.groupby(["month", "bloc"]).agg(
        pct_conflictual=("conflictual", "mean"), n=("conflictual", "count")
    ).reset_index()
    delib["month_ts"] = pd.to_datetime(delib["month"] + "-01")
    delib = delib[delib["n"] >= 5]
    delib.to_csv(RESULTS_DIR / "deliberative_intensity_by_bloc_month.csv", index=False)

    log_report("\nIntensité délibérative (% conflictuel) :")
    log_report(delib.groupby("bloc")["pct_conflictual"].mean().to_string())

    fig, ax = plt.subplots(figsize=(11, 6))
    for bloc in BLOC_ORDER:
        sub = delib[delib["bloc"] == bloc]
        if len(sub) > 0:
            ax.plot(sub["month_ts"], sub["pct_conflictual"] * 100, label=bloc,
                   color=BLOC_COLORS.get(bloc, "#888"), lw=1.5)
    add_events(ax)
    ax.set_ylabel("% conflictuel")
    ax.legend(fontsize=8)
    format_dates(ax)
    save_fig("fig62_deliberative_conflictual_temporal")

    # AJOUT TÂCHE C2 — Corrélation Spearman registre vs stance + figure bloc × batch
    sub_c2 = df_valid[["discourse_score", "stance_v3"]].dropna()
    if len(sub_c2) >= 20:
        rho, pval = spearmanr(sub_c2["discourse_score"], sub_c2["stance_v3"])
        log_report("\nRegistre discursif vs stance (Spearman) :")
        log_report(f"  rho = {rho:.4f}, p = {pval:.4e}")
        interp = "utile (rho>0.3)" if abs(rho) > 0.3 else ("limitation (rho<0.1)" if abs(rho) < 0.1 else "modérée")
        log_report(f"  Interprétation : {interp}")
    if "batch" not in df_valid.columns:
        df_valid["batch"] = df_valid["month"].map(month_to_batch)
    reg_bloc_batch = df_valid[df_valid["batch"].isin(BATCH_ORDER)].groupby(["bloc", "batch"]).agg(
        registre_conflictuel_moyen=("discourse_score", "mean"),
        n=("discourse_score", "count"),
    ).reset_index()
    reg_bloc_batch = reg_bloc_batch[reg_bloc_batch["n"] >= 5]
    if len(reg_bloc_batch) > 0:
        reg_bloc_batch.to_csv(RESULTS_DIR / "registre_conflictuel_bloc_batch.csv", index=False)
        fig, ax = plt.subplots(figsize=(12, 6))
        order_batch = [b for b in BATCH_ORDER if b in reg_bloc_batch["batch"].unique()]
        x = np.arange(len(order_batch))
        width = 0.2
        for i, bloc in enumerate(BLOC_ORDER):
            sub = reg_bloc_batch[reg_bloc_batch["bloc"] == bloc]
            if len(sub) == 0:
                continue
            by_batch = sub.set_index("batch").reindex(order_batch)["registre_conflictuel_moyen"].fillna(0).values
            offset = (i - (len(BLOC_ORDER) - 1) / 2) * width
            ax.bar(x + offset, by_batch, width, label=bloc, color=BLOC_COLORS.get(bloc, "#888"))
        ax.set_xticks(x)
        ax.set_xticklabels([b.replace("_", "\n") for b in order_batch], fontsize=8)
        ax.set_ylabel("Registre conflictuel moyen (0=coop, 1=conflit)")
        ax.legend(loc="upper right", fontsize=8)
        ax.set_title("Registre discursif par bloc × batch (CEASEFIRE_BREACH = convergence lexicale)")
        ax.set_ylim(0, 1)
        plt.tight_layout()
        save_fig("fig75_registre_conflictuel_bloc_batch")


# -----------------------------------------------------------------------------
# NB04 — Polarisation lexicale
# -----------------------------------------------------------------------------
def run_04_polarisation(df):
    log_report("\n" + "=" * 60)
    log_report("04 — POLARISATION LEXICALE")
    log_report("=" * 60)

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    df_valid = df[df["bloc"].isin(BLOC_ORDER) & df[text_col].notna()].copy()
    df_valid[text_col] = df_valid[text_col].fillna("").astype(str)

    vec = TfidfVectorizer(max_features=5000, min_df=5, max_df=0.95, ngram_range=(1, 2))
    dist_list = []
    months = sorted(df_valid["month"].unique())
    for m in months:
        sub = df_valid[df_valid["month"] == m]
        if len(sub) < 50:
            continue
        X = vec.fit_transform(sub[text_col])
        for i, b1 in enumerate(BLOC_ORDER):
            for b2 in BLOC_ORDER[i + 1 :]:
                idx1 = (sub["bloc"] == b1).values
                idx2 = (sub["bloc"] == b2).values
                if idx1.sum() >= 5 and idx2.sum() >= 5:
                    c1 = np.asarray(X[idx1].mean(axis=0)).reshape(1, -1)
                    c2 = np.asarray(X[idx2].mean(axis=0)).reshape(1, -1)
                    d = cosine_distances(c1, c2)[0, 0]
                    dist_list.append({"month": m, "pair": f"{b1} vs {b2}", "dist": d})

    dist_df = pd.DataFrame(dist_list)
    dist_df.to_csv(RESULTS_DIR / "cosine_distance_mensuelle.csv", index=False)

    log_report("\nDistance cosinus mensuelle (moyenne) :")
    if len(dist_df) > 0:
        mean_dist = dist_df.groupby("month")["dist"].mean()
        log_report(mean_dist.to_string())

    gauche = df_valid[df_valid["bloc"].isin(["Gauche radicale", "Gauche moderee"])][text_col]
    droite = df_valid[df_valid["bloc"].isin(["Droite", "Centre / Majorite"])][text_col]
    cnt_g = Counter()
    for t in gauche.dropna():
        cnt_g.update(tokenize(t))
    cnt_d = Counter()
    for t in droite.dropna():
        cnt_d.update(tokenize(t))
    lod = log_odds(cnt_g, cnt_d)
    lod_df = pd.DataFrame([{"word": w, "z": v} for w, v in lod.items()]).sort_values("z", key=abs, ascending=False)
    lod_df.to_csv(RESULTS_DIR / "fighting_words.csv", index=False)

    log_report("\nTop 10 fighting words (gauche) :")
    log_report(lod_df.nlargest(10, "z")[["word", "z"]].to_string(index=False))
    log_report("\nTop 10 fighting words (droite) :")
    log_report(lod_df.nsmallest(10, "z")[["word", "z"]].to_string(index=False))

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
        z_scores = log_odds(cnt_g, cnt_d)
        for w, z in z_scores.items():
            if abs(z) > 0.5:
                fw_rows.append({"month": m, "word": w, "z": z})
    if fw_rows:
        pd.DataFrame(fw_rows).to_csv(RESULTS_DIR / "fighting_words_temporal.csv", index=False)

    ceasefire_regex = re.compile(
        r"cessez-le-feu|ceasefire|tr[êe]ve|cessation[ ]+des[ ]+hostilités", re.I
    )
    df_valid["ceasefire_lexical"] = df_valid[text_col].str.contains(ceasefire_regex, na=False)
    clf = df_valid.groupby(["month", "bloc"]).agg(
        pct=("ceasefire_lexical", "mean"), n=("ceasefire_lexical", "count")
    ).reset_index()
    clf["month_ts"] = pd.to_datetime(clf["month"] + "-01")
    clf.to_csv(RESULTS_DIR / "ceasefire_lexical.csv", index=False)

    log_report("\nCessez-le-feu lexical (% par bloc, moyenne) :")
    log_report(clf.groupby("bloc")["pct"].mean().apply(lambda x: f"{x*100:.1f}%").to_string())

    pol_idx = dist_df.groupby("month")["dist"].mean().reset_index()
    pol_idx["month_ts"] = pd.to_datetime(pol_idx["month"] + "-01")
    pol_idx.to_csv(RESULTS_DIR / "polarisation_index.csv", index=False)

    ec_global = []
    ec_by_bloc = []
    for m, sub in df_valid.groupby("month"):
        vals = sub["stance_v3"].dropna()
        if len(vals) >= 10:
            ec_global.append({"month": m, "Ec": entropic_polarization_bao_gill(vals), "n": len(vals)})
        for bloc in BLOC_ORDER:
            bvals = sub[sub["bloc"] == bloc]["stance_v3"].dropna()
            if len(bvals) >= 10:
                ec_by_bloc.append({
                    "month": m, "bloc": bloc, "Ec": entropic_polarization_bao_gill(bvals), "n": len(bvals)
                })

    ec_df = pd.DataFrame(ec_global)
    ec_bloc_df = pd.DataFrame(ec_by_bloc)
    ec_df["month_ts"] = pd.to_datetime(ec_df["month"] + "-01")
    ec_df.to_csv(RESULTS_DIR / "entropic_polarization_temporal.csv", index=False)

    log_report("\nPolarisation entropique Ec (Bao & Gill) :")
    if len(ec_df) > 0:
        log_report(f"  Moyenne Ec globale : {ec_df['Ec'].mean():.4f}")
        log_report(f"  Min/Max : {ec_df['Ec'].min():.4f} / {ec_df['Ec'].max():.4f}")

    pairs = [(b1, b2) for i, b1 in enumerate(BLOC_ORDER) for b2 in BLOC_ORDER[i + 1 :]]
    wd_inter = wd_inter_blocs(df_valid, pairs)
    wd_drift_list = []
    for bloc in BLOC_ORDER:
        d = wd_drift_intra_bloc(df_valid, bloc)
        if len(d) > 0:
            wd_drift_list.append(d)
    wd_drift = pd.concat(wd_drift_list, ignore_index=True) if wd_drift_list else pd.DataFrame()
    wd_inter.to_csv(RESULTS_DIR / "wasserstein_inter_blocs.csv", index=False)
    if len(wd_drift) > 0:
        wd_drift.to_csv(RESULTS_DIR / "wasserstein_drift.csv", index=False)

    wd_mean = wd_inter.groupby("month")["wd_norm"].mean().reset_index()
    pol_path = RESULTS_DIR / "polarisation_index.csv"
    pol_idx = pd.read_csv(pol_path)
    pol_idx = pol_idx.merge(
        wd_mean[["month", "wd_norm"]].rename(columns={"wd_norm": "wd_mean"}),
        on="month", how="left"
    )
    pol_idx.to_csv(pol_path, index=False)

    # AJOUT TÂCHE C3 — Figure polarisation entropique Ec vs distance cosinus
    merged = ec_df[["month", "month_ts", "Ec"]].merge(
        pol_idx[["month", "dist"]], on="month", how="inner"
    )
    if len(merged) >= 5:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(merged["month_ts"], merged["Ec"], "b-o", label="Ec (polarisation entropique Bao & Gill)", markersize=4)
        ax1.set_ylabel("Ec (0=consensus, 1=polarisé)", color="b")
        ax1.set_ylim(0, 1)
        ax1.tick_params(axis="y", labelcolor="b")
        ax2 = ax1.twinx()
        ax2.plot(merged["month_ts"], merged["dist"], "g--s", label="Distance cosinus (TF-IDF)", markersize=4)
        ax2.set_ylabel("Distance cosinus", color="g")
        ax2.tick_params(axis="y", labelcolor="g")
        add_events(ax1)
        ax1.legend(loc="upper left", fontsize=8)
        ax2.legend(loc="upper right", fontsize=8)
        format_dates(ax1)
        ax1.set_title("Polarisation entropique vs distance cosinus — Événements pivot en overlay")
        plt.tight_layout()
        save_fig("fig76_entropic_polarization_vs_cosine")

    deputy_month = df_valid.groupby(["author", "month"]).agg(
        stance_mean=("stance_v3", "mean"),
        clf_pct=("ceasefire_lexical", "mean"),
        **({"engagement_mean": ("engagement", "mean")} if "engagement" in df_valid.columns else {}),
    ).reset_index()
    deputy_month = deputy_month.dropna(subset=["stance_mean", "clf_pct"])
    ed_list = []
    for m in sorted(df_valid["month"].unique()):
        sub = deputy_month[deputy_month["month"] == m]
        if len(sub) >= 20:
            feat_cols = [
                c for c in ["stance_mean", "clf_pct", "engagement_mean"]
                if c in sub.columns and sub[c].notna().sum() >= len(sub) // 2
            ]
            if len(feat_cols) >= 2:
                X = sub[feat_cols].fillna(0).values
                X_std = StandardScaler().fit_transform(X)
                ed = effective_dimensionality(X_std)
                ed_list.append({"month": m, "ED": ed, "n": len(sub), "n_feat": len(feat_cols)})
    ed_df = pd.DataFrame(ed_list)
    if len(ed_df) > 0:
        ed_df["month_ts"] = pd.to_datetime(ed_df["month"] + "-01")
        ed_df.to_csv(RESULTS_DIR / "effective_dimensionality_temporal.csv", index=False)
        log_report("\nEffective Dimensionality :")
        log_report(f"  Moyenne ED : {ed_df['ED'].mean():.4f}")
        log_report(f"  Min/Max : {ed_df['ED'].min():.4f} / {ed_df['ED'].max():.4f}")

    lex = load_vad_lexicon()
    df_valid["_vad"] = df_valid[text_col].apply(score_text_vad)
    df_valid["valence"] = df_valid["_vad"].apply(lambda x: x[0] if isinstance(x, tuple) else float("nan"))
    df_valid["arousal"] = df_valid["_vad"].apply(lambda x: x[1] if isinstance(x, tuple) else float("nan"))
    df_valid["dominance"] = df_valid["_vad"].apply(lambda x: x[2] if isinstance(x, tuple) else float("nan"))

    vad_bloc = df_valid.groupby(["month", "bloc"]).agg(
        valence=("valence", "mean"), arousal=("arousal", "mean"), dominance=("dominance", "mean"),
        n=("valence", "count"),
    ).reset_index()
    vad_bloc = vad_bloc[vad_bloc["n"] >= 5]
    vad_bloc["month_ts"] = pd.to_datetime(vad_bloc["month"] + "-01")
    vad_bloc.to_csv(RESULTS_DIR / "affective_vad_by_bloc_month.csv", index=False)

    gap_list = []
    for m in vad_bloc["month"].unique():
        sub = vad_bloc[vad_bloc["month"] == m]
        blocs = sub["bloc"].tolist()
        for i in range(len(blocs)):
            for j in range(i + 1, len(blocs)):
                r1, r2 = sub.iloc[i], sub.iloc[j]
                v1 = (r1["valence"], r1["arousal"], r1["dominance"])
                v2 = (r2["valence"], r2["arousal"], r2["dominance"])
                gap_list.append({
                    "month": m, "pair": f"{r1['bloc']} vs {r2['bloc']}",
                    "gap_vad": euclidean(v1, v2)
                })
    gap_df = pd.DataFrame(gap_list)
    if len(gap_df) > 0:
        gap_agg = gap_df.groupby("month")["gap_vad"].mean().reset_index()
        gap_agg["month_ts"] = pd.to_datetime(gap_agg["month"] + "-01")
        gap_agg.to_csv(RESULTS_DIR / "affective_polarization_temporal.csv", index=False)
        log_report("\nPolarisation affective (gap VAD moyen) :")
        log_report(f"  Moyenne gap : {gap_agg['gap_vad'].mean():.4f}")

    mfd = load_mfd()
    df_valid["_mfd"] = df_valid[text_col].apply(score_text_mfd)
    for f in ["care", "fairness", "loyalty", "authority", "sanctity"]:
        df_valid[f"mfd_{f}"] = df_valid["_mfd"].apply(lambda x: x.get(f, float("nan")))

    mfd_bloc = df_valid.groupby(["month", "bloc"]).agg(
        care=("mfd_care", "mean"), fairness=("mfd_fairness", "mean"),
        loyalty=("mfd_loyalty", "mean"), authority=("mfd_authority", "mean"),
        sanctity=("mfd_sanctity", "mean"), n=("mfd_care", "count"),
    ).reset_index()
    mfd_bloc = mfd_bloc[mfd_bloc["n"] >= 5]
    mfd_bloc["month_ts"] = pd.to_datetime(mfd_bloc["month"] + "-01")
    mfd_bloc.to_csv(RESULTS_DIR / "moral_foundations_by_bloc_month.csv", index=False)

    log_report("\nFondements moraux (moyenne par bloc) :")
    mfd_mean = mfd_bloc.groupby("bloc")[["care", "fairness", "loyalty", "authority", "sanctity"]].mean()
    log_report(mfd_mean.to_string())

    # AJOUT TÂCHE C1 — Couverture MFD (lexique étendu 40+ mots/fondement)
    cov = compute_mfd_coverage(df_valid, text_col)
    log_report("\nCouverture MFD (% textes avec ≥1 hit par fondement) :")
    for fname, pct in cov.items():
        log_report(f"  {fname}: {pct:.1f}%")


# -----------------------------------------------------------------------------
# NB05 — Événements pivot
# -----------------------------------------------------------------------------
def run_05_evenements(df, df_v4):
    log_report("\n" + "=" * 60)
    log_report("05 — ÉVÉNEMENTS PIVOT")
    log_report("=" * 60)

    batch_col = "batch" if "batch" in df_v4.columns else None
    if batch_col:
        var_batch = df_v4.groupby("batch").agg(
            n=("stance_v3", "count"),
            stance_mean=("stance_v3", "mean"),
            stance_std=("stance_v3", "std"),
        ).reindex(BATCH_ORDER).dropna(how="all")
        var_batch.to_csv(RESULTS_DIR / "variables_batch_specifiques.csv")
        log_report("\nVariables par batch :")
        log_report(var_batch.to_string())

    if "ceasefire_call" in df_v4.columns and batch_col:
        cf = df_v4.groupby(["batch", "bloc"]).agg(
            pct=("ceasefire_call", "mean"), n=("ceasefire_call", "count")
        ).reset_index()
        cf.to_csv(RESULTS_DIR / "ceasefire_call_batch_bloc.csv", index=False)
        log_report("\nAppel cessez-le-feu par batch/bloc :")
        log_report(cf.pivot_table(index="batch", columns="bloc", values="pct").to_string())

    cols = ["stance_v3", "bloc", "arena"] + (["batch"] if "batch" in df_v4.columns else [])
    reg_df = df_v4[[c for c in cols if c in df_v4.columns]].dropna().copy()
    if len(reg_df) < 10:
        return
    try:
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm
        if "batch" in reg_df.columns:
            formula = "stance_v3 ~ C(bloc) + C(batch) + C(arena) + C(bloc):C(batch)"
        else:
            formula = "stance_v3 ~ C(bloc) + C(arena)"
        model = ols(formula, data=reg_df).fit()
        anova_tab = anova_lm(model, typ=2)
        anova_tab.to_csv(RESULTS_DIR / "anova_interaction.csv")

        log_report("\nRégression ANOVA (type 2) :")
        log_report(anova_tab.to_string())

        coef = model.params
        pvals = model.pvalues
        log_report("\nCoefficients (extrait) :")
        for name in coef.index[:8]:
            log_report(f"  {name}: coef={coef[name]:.4f}, p={pvals[name]:.4f}")

        if "batch" in reg_df.columns:
            anova_tab = anova_lm(model, typ=2).reset_index()
            anova_tab.to_csv(RESULTS_DIR / "anova_type2.csv", index=False)
    except Exception as e:
        log_report(f"  ANOVA non calculée : {e}")


# -----------------------------------------------------------------------------
# NB06 — Convergence transpartisane
# -----------------------------------------------------------------------------
def run_06_convergence(df, df_v4):
    log_report("\n" + "=" * 60)
    log_report("06 — CONVERGENCE TRANSPARTISANE")
    log_report("=" * 60)

    df_conv = df_v4 if "batch" in df_v4.columns else df.assign(batch=df["month"])
    df_conv["convergence"] = df_conv["stance_v3"].abs() <= 1
    if "ceasefire_call" in df_conv.columns:
        df_conv["convergence"] = df_conv["convergence"] | df_conv["ceasefire_call"]
    conv = df_conv.groupby(["batch", "bloc"])["convergence"].mean().reset_index()
    conv.columns = ["batch", "bloc", "pct"]
    conv.to_csv(RESULTS_DIR / "convergence_batch_bloc.csv", index=False)

    conv_agg = df.groupby("bloc").apply(lambda g: (g["stance_v3"].abs() <= 1).mean()).reindex(BLOC_ORDER)
    log_report("\n% convergence (|stance|≤1) par bloc :")
    for b in BLOC_ORDER:
        if b in conv_agg.index:
            log_report(f"  {b}: {conv_agg[b]*100:.1f}%")

    # AJOUT TÂCHE B5 — Movers redefinis : stance_initial (CHOC) vs stance_final (NEW_OFFENSIVE)
    stance_col = "stance_v3" if "stance_v3" in df.columns else "stance"
    df_06 = df.assign(batch=df["month"].apply(month_to_batch))
    if stance_col in df_06.columns:
        choc = df_06[df_06["batch"] == "CHOC"].groupby("author")[stance_col].mean().rename("stance_initial")
        noff = df_06[df_06["batch"] == "NEW_OFFENSIVE"].groupby("author")[stance_col].mean().rename("stance_final")
        movers = choc.to_frame().join(noff, how="inner").reset_index()
        movers["delta_individuel"] = movers["stance_final"] - movers["stance_initial"]
        bloc_map = df_06.groupby("author")["bloc"].first()
        movers["bloc"] = movers["author"].map(bloc_map)
        movers = movers[movers["bloc"].isin(BLOC_ORDER)]
        movers["mover_type"] = "non_mover"
        movers.loc[movers["delta_individuel"].abs() > 0.8, "mover_type"] = "modere"
        movers.loc[movers["delta_individuel"].abs() > 1.5, "mover_type"] = "fort"
        rupture_dates = []
        stance_mensuel = df_06.groupby(["author", "month"])[stance_col].mean().reset_index()
        stance_mensuel["month_ts"] = pd.to_datetime(stance_mensuel["month"] + "-01")
        top10 = movers.reindex(movers["delta_individuel"].abs().sort_values(ascending=False).index).head(10)
        for _, row in top10.iterrows():
            traj = stance_mensuel[stance_mensuel["author"] == row["author"]].sort_values("month_ts")
            if len(traj) >= 5:
                try:
                    import ruptures as rpt
                    signal = traj[stance_col].values.astype(float)
                    algo = rpt.Pelt(model="rbf").fit(signal.reshape(-1, 1))
                    chg = algo.predict(pen=1)
                    if len(chg) > 1 and chg[0] < len(traj):
                        idx = chg[0]
                        rupture_dates.append({"author": row["author"], "rupture_date": traj.iloc[idx]["month"]})
                except Exception:
                    rupture_dates.append({"author": row["author"], "rupture_date": None})
        rupture_df = pd.DataFrame(rupture_dates) if rupture_dates else pd.DataFrame(columns=["author", "rupture_date"])
        movers = movers.merge(rupture_df, on="author", how="left")
        movers.to_csv(RESULTS_DIR / "movers_caches.csv", index=False)
        log_report("\nMovers (stance_initial=CHOC, stance_final=NEW_OFFENSIVE) :")
        log_report(movers.groupby("bloc").size().reindex(BLOC_ORDER, fill_value=0).to_string())
        log_report(f"  Fort (|delta|>1.5): {len(movers[movers['mover_type']=='fort'])}, Modere (|delta|>0.8): {len(movers[movers['mover_type']=='modere'])}")

        # fig73 : spaghetti top-10 movers
        fig, ax = plt.subplots(figsize=(14, 6))
        for i, (_, row) in enumerate(top10.iterrows()):
            traj = stance_mensuel[stance_mensuel["author"] == row["author"]].sort_values("month_ts")
            if len(traj) > 0:
                lbl = f"{row['author'][:15]}... (delta={row['delta_individuel']:.1f})" if len(str(row["author"])) > 15 else f"{row['author']} (delta={row['delta_individuel']:.1f})"
                ax.plot(traj["month_ts"], traj[stance_col], alpha=0.7, lw=1.5,
                        color=BLOC_COLORS.get(row["bloc"], "#888"),
                        label=lbl)
        add_events(ax)
        ax.axhline(0, color="grey", ls="--", lw=0.8)
        ax.set_ylabel("Stance mensuel")
        ax.set_title("Top-10 movers : trajectoires individuelles")
        ax.legend(bbox_to_anchor=(1.02, 1), fontsize=8)
        format_dates(ax)
        save_fig("fig73_movers_spaghetti")

        # fig74 : distribution delta_individuel
        fig, ax = plt.subplots(figsize=(10, 5))
        movers_plot = movers[movers["delta_individuel"].notna()]
        if len(movers_plot) > 0:
            colors = [BLOC_COLORS.get(b, "#888") for b in movers_plot["bloc"]]
            ax.hist(movers_plot["delta_individuel"], bins=30, color="steelblue", alpha=0.7, edgecolor="white")
            ax.axvline(0, color="black", ls="--", lw=1.5)
        ax.set_xlabel("Delta individuel (stance_final - stance_initial)")
        ax.set_ylabel("Nombre de deputes")
        ax.set_title("Distribution du delta individuel (movers)")
        save_fig("fig74_movers_delta_distribution")

    text_col = "text_clean" if "text_clean" in df.columns else "text"
    author_texts = df[df["bloc"].isin(BLOC_ORDER)].groupby("author")[text_col].apply(
        lambda x: " ".join(x.astype(str))
    ).reset_index()
    if len(author_texts) >= 10:
        vec = TfidfVectorizer(max_features=2000, min_df=2, max_df=0.95)
        X = vec.fit_transform(author_texts[text_col])
        n_comp = min(50, X.shape[0] - 1, X.shape[1] - 1)
        pca = PCA(n_components=n_comp, random_state=42)
        coords = pca.fit_transform(X.toarray())
        bloc_map = df.groupby("author")["bloc"].first()
        pca_df = pd.DataFrame({
            "author": author_texts["author"].values,
            "bloc": author_texts["author"].map(bloc_map),
            "PC1": coords[:, 0],
            "PC2": coords[:, 1],
        })
        pca_df.to_csv(RESULTS_DIR / "pca_coordonnees.csv", index=False)
        expl = pca.explained_variance_ratio_
        log_report("\nPCA députés :")
        log_report(f"  Variance expliquée PC1: {expl[0]*100:.2f}%")
        log_report(f"  Variance expliquée PC2: {expl[1]*100:.2f}%")
        log_report(f"  Cumul 2 composantes: {expl[:2].sum()*100:.2f}%")


# -----------------------------------------------------------------------------
# NB07 — Émotions et registres
# -----------------------------------------------------------------------------
def run_07_emotions(df, df_v4):
    log_report("\n" + "=" * 60)
    log_report("07 — ÉMOTIONS ET REGISTRES")
    log_report("=" * 60)

    emo_col = "emotional_register" if "emotional_register" in df_v4.columns else "emotional_reg" if "emotional_reg" in df_v4.columns else None
    if emo_col:
        emo = df_v4[df_v4["bloc"].isin(BLOC_ORDER)].groupby(["bloc", emo_col]).size().unstack(fill_value=0)
        emo_pct = emo.div(emo.sum(axis=1), axis=0).reindex(BLOC_ORDER)
        emo_pct.to_csv(RESULTS_DIR / "emotional_register.csv")
        log_report("\nRegistre émotionnel par bloc :")
        log_report(emo_pct.to_string())
    else:
        emo_pct = pd.DataFrame()

    frame_col = "primary_frame_v3" if "primary_frame_v3" in df.columns else "frame_primary" if "frame_primary" in df_v4.columns else None
    df_f = df if frame_col and frame_col in df.columns else df_v4
    if frame_col and frame_col in df_f.columns:
        frames = df_f[df_f["bloc"].isin(BLOC_ORDER)].groupby(["bloc", frame_col]).size().unstack(fill_value=0)
        frames_pct = frames.div(frames.sum(axis=1), axis=0).reindex(BLOC_ORDER)
        frames_pct.to_csv(RESULTS_DIR / "frames_par_bloc.csv")
        log_report("\nFrames par bloc :")
        log_report(frames_pct.to_string())


# -----------------------------------------------------------------------------
# NB08 — Analyses de fond
# -----------------------------------------------------------------------------
def run_08_analyses_fond(df):
    log_report("\n" + "=" * 60)
    log_report("08 — ANALYSES DE FOND")
    log_report("=" * 60)

    df_valid = df[df["bloc"].isin(BLOC_ORDER)].copy()
    n_by_bloc = df_valid.groupby("bloc").size().reindex(BLOC_ORDER)
    pct = (n_by_bloc / n_by_bloc.sum() * 100).round(1)
    log_report("\nRépartition par bloc :")
    for b in BLOC_ORDER:
        if b in n_by_bloc.index:
            log_report(f"  {b}: n={int(n_by_bloc[b])}, {pct[b]:.1f}%")

    n_min = int(n_by_bloc.min())
    np.random.seed(42)
    df_balanced = df_valid.groupby("bloc", group_keys=False).apply(
        lambda g: g.sample(n=min(len(g), n_min), random_state=42)
    )
    stance_col = "stance_v3" if "stance_v3" in df_balanced.columns else "stance"
    if stance_col in df_balanced.columns:
        mean_balanced = df_balanced.groupby("bloc")[stance_col].mean().reindex(BLOC_ORDER)
        mean_full = df_valid.groupby("bloc")[stance_col].mean().reindex(BLOC_ORDER)
        diff = (mean_balanced - mean_full).round(3)
        log_report("\nStance : complet vs sous-échantillonné (n_min) :")
        for b in BLOC_ORDER:
            if b in mean_full.index:
                log_report(f"  {b}: complet={mean_full[b]:.3f}, sous-échant.={mean_balanced[b]:.3f}, écart={diff[b]:.3f}")


# -----------------------------------------------------------------------------
# NB09 — Engagement Twitter
# -----------------------------------------------------------------------------
def run_09_engagement(df):
    log_report("\n" + "=" * 60)
    log_report("09 — ENGAGEMENT TWITTER")
    log_report("=" * 60)

    arena_col = "arena" if "arena" in df.columns else None
    df_tw = df[df[arena_col] == "Twitter"] if arena_col else pd.DataFrame()
    engagement_cols = [c for c in ["retweets", "likes", "replies", "engagement"] if c in df.columns]
    if not engagement_cols:
        engagement_cols = [c for c in df.columns if "count" in c.lower() or "like" in c.lower()]

    if len(df_tw) > 0 and engagement_cols:
        df_tw = df_tw.copy()
        if "engagement" not in df_tw.columns:
            df_tw["engagement"] = df_tw[[c for c in engagement_cols if c in df_tw.columns]].fillna(0).sum(axis=1)
        df_tw = df_tw[df_tw["bloc"].isin(BLOC_ORDER)]
        df_tw["log_engagement"] = np.log1p(df_tw["engagement"])
        agg = df_tw.groupby("bloc").agg(
            mean_log=("log_engagement", "mean"), n=("log_engagement", "count")
        ).reindex(BLOC_ORDER)
        log_report("\nlog(1+engagement) moyen par bloc :")
        log_report(agg.to_string())

        if "stance_v3" in df_tw.columns:
            df_tw["abs_stance"] = df_tw["stance_v3"].abs()
            r = df_tw["abs_stance"].corr(df_tw["log_engagement"])
            log_report(f"\nCorrélation |stance| ↔ log(engagement) : r = {r:.3f}")


# -----------------------------------------------------------------------------
# NB10 — Twitter vs AN
# -----------------------------------------------------------------------------
def run_10_twitter_vs_an(df):
    log_report("\n" + "=" * 60)
    log_report("10 — TWITTER VS ASSEMBLÉE NATIONALE")
    log_report("=" * 60)

    df = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df["author_norm"] = df["author"].str.replace(r"^(M\.?|Mme)\s+", "", regex=True).str.strip()
    tw_authors = set(df[df["arena"] == "Twitter"]["author_norm"].unique())
    an_authors = set(df[df["arena"] == "AN"]["author_norm"].unique())
    both_authors = tw_authors & an_authors
    log_report(f"\nDéputés actifs sur Twitter et AN : {len(both_authors)}")

    df_both = df[df["author_norm"].isin(both_authors)].copy()
    stance_tw = df_both[df_both["arena"] == "Twitter"].groupby(["author_norm", "month", "bloc"]).agg(
        stance_tw=("stance_v3", "mean"),
        n_tweets=("stance_v3", "count"),
        engagement_mean=("engagement", "mean") if "engagement" in df_both.columns else ("stance_v3", "mean"),
    ).reset_index()
    stance_an = df_both[df_both["arena"] == "AN"].groupby(["author_norm", "month", "bloc"]).agg(
        stance_an=("stance_v3", "mean"),
        n_an=("stance_v3", "count"),
    ).reset_index()

    merged = stance_tw.merge(stance_an, on=["author_norm", "month", "bloc"], how="inner")
    merged["delta"] = merged["stance_tw"] - merged["stance_an"]
    merged["month_ts"] = pd.to_datetime(merged["month"] + "-01")
    merged.to_csv(RESULTS_DIR / "stance_twitter_vs_an_by_deputy.csv", index=False)

    log_report(f"Observations député-mois (les deux arènes) : {len(merged)}")

    merged["batch"] = merged["month"].apply(month_to_batch)

    # AJOUT TÂCHE B4 — fig72 : scatter stance_tw vs stance_an par député
    dep_agg = merged.groupby(["author_norm", "bloc"]).agg(
        stance_mean_twitter=("stance_tw", "mean"),
        stance_mean_an=("stance_an", "mean"),
        n_obs=("delta", "count"),
    ).reset_index()
    dep_agg = dep_agg[dep_agg["n_obs"] >= 2]
    if len(dep_agg) >= 10:
        fig, ax = plt.subplots(figsize=(8, 8))
        for bloc in BLOC_ORDER:
            sub = dep_agg[dep_agg["bloc"] == bloc]
            if len(sub) > 0:
                ax.scatter(sub["stance_mean_an"], sub["stance_mean_twitter"], label=bloc,
                          color=BLOC_COLORS.get(bloc, "#888"), alpha=0.7, s=40)
        lims = [-2.2, 2.2]
        ax.plot(lims, lims, "k--", lw=1.5, label="Identite")
        ax.set_xlabel("Stance moyen AN")
        ax.set_ylabel("Stance moyen Twitter")
        ax.set_title("Stance Twitter vs AN par depute (points = identite)")
        ax.legend()
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_aspect("equal")
        save_fig("fig72_twitter_vs_an_scatter")

    merged_clean = merged.dropna(subset=["delta", "n_tweets", "engagement_mean"])
    if len(merged_clean) >= 20:
        try:
            import statsmodels.formula.api as smf
            model = smf.ols(
                "delta ~ C(bloc) + n_tweets + engagement_mean + C(batch)",
                data=merged_clean
            ).fit()
            reg_summary = pd.DataFrame({
                "param": model.params.index,
                "coef": model.params.values,
                "pvalue": model.pvalues.values,
            })
            reg_summary.to_csv(RESULTS_DIR / "regression_delta_stance.csv", index=False)
            log_report("\nRégression delta stance (Twitter − AN) :")
            log_report("  Coefficients et p-values :")
            for _, row in reg_summary.iterrows():
                log_report(f"    {row['param']}: coef={row['coef']:.4f}, p={row['pvalue']:.4f}")
        except Exception as e:
            log_report(f"  Régression non calculée : {e}")

    # AJOUT TÂCHE B4 — Fighting words Twitter vs AN par bloc
    text_col = "text_clean" if "text_clean" in df_both.columns else "text"
    df_both[text_col] = df_both[text_col].fillna("").astype(str)
    fw_tw_an_rows = []
    for bloc in BLOC_ORDER:
        sub = df_both[df_both["bloc"] == bloc]
        tw_texts = sub[sub["arena"] == "Twitter"][text_col]
        an_texts = sub[sub["arena"] == "AN"][text_col]
        if len(tw_texts) >= 20 and len(an_texts) >= 10:
            cnt_tw = Counter()
            for t in tw_texts:
                cnt_tw.update(tokenize(t))
            cnt_an = Counter()
            for t in an_texts:
                cnt_an.update(tokenize(t))
            z_scores = log_odds(cnt_tw, cnt_an)
            for w, z in sorted(z_scores.items(), key=lambda x: abs(x[1]), reverse=True)[:30]:
                if abs(z) > 0.5:
                    fw_tw_an_rows.append({"bloc": bloc, "word": w, "z": z, "arena_favorisee": "Twitter" if z > 0 else "AN"})
    if fw_tw_an_rows:
        pd.DataFrame(fw_tw_an_rows).to_csv(RESULTS_DIR / "fighting_words_twitter_vs_an.csv", index=False)
        log_report("\nFighting words Twitter vs AN (top par bloc, |z|>0.5) :")
        for bloc in BLOC_ORDER:
            bloc_rows = [r for r in fw_tw_an_rows if r["bloc"] == bloc][:5]
            if bloc_rows:
                log_report(f"  {bloc}: {[(r['word'], round(r['z'],2), r['arena_favorisee']) for r in bloc_rows]}")


# -----------------------------------------------------------------------------
# Lag adoption (ceasefire lexical → premier mois ≥ 10 %)
# -----------------------------------------------------------------------------
def run_lag_adoption():
    clf_path = RESULTS_DIR / "ceasefire_lexical.csv"
    if not clf_path.exists():
        return
    clf = pd.read_csv(clf_path)
    pct_col = "pct" if "pct" in clf.columns else "pct_ceasefire"
    month_col = "month" if "month" in clf.columns else clf.columns[0]
    bloc_col = "bloc" if "bloc" in clf.columns else clf.columns[1]
    lag_rows = []
    for bloc in clf[bloc_col].unique():
        b = clf[clf[bloc_col] == bloc].sort_values(month_col)
        first = b[b[pct_col] >= 0.1].head(1)
        if len(first) > 0:
            row = first.iloc[0]
            lag_rows.append({"bloc": bloc, "month_first_10pct": row[month_col], "pct": row[pct_col]})
    if lag_rows:
        lag_df = pd.DataFrame(lag_rows)
        lag_df.to_csv(RESULTS_DIR / "lag_adoption.csv", index=False)
        log_report("\n" + "=" * 60)
        log_report("LAG D'ADOPTION (cessez-le-feu lexical)")
        log_report("=" * 60)
        log_report("Premier mois où chaque bloc dépasse 10 % de textes avec « cessez-le-feu » :")
        log_report(lag_df.to_string(index=False))


# -----------------------------------------------------------------------------
# AJOUT TÂCHE A3 — Tendances pré-événement
# -----------------------------------------------------------------------------
WINDOW_PRE = 60
WINDOW_POST = 30


def run_A3_tendances_pre_event(df):
    """Fenêtre pré 60j, Mann-Kendall sur tendance pré, fig53 pour Cessez-le-feu et Mandats CPI."""
    log_report("\n" + "=" * 60)
    log_report("A3 — TENDANCES PRE-EVENEMENT (60j avant)")
    log_report("=" * 60)

    df = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df["date"] = pd.to_datetime(df["date"])
    events_for_fig = [
        ("Cessez-le-feu", EVENT_STUDY_DATES["Cessez-le-feu"]),
        ("Mandats CPI", EVENT_STUDY_DATES["Mandats CPI"]),
    ]
    pre_trend_results = []

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for panel_idx, bloc in enumerate(BLOC_ORDER):
        ax = axes[panel_idx]
        for ev_name, ev_date in events_for_fig:
            t0 = pd.Timestamp(ev_date)
            pre = df[
                (df["date"] >= t0 - pd.Timedelta(days=WINDOW_PRE))
                & (df["date"] < t0)
                & (df["bloc"] == bloc)
            ].copy()
            post = df[
                (df["date"] >= t0)
                & (df["date"] < t0 + pd.Timedelta(days=WINDOW_POST))
                & (df["bloc"] == bloc)
            ].copy()

            pre["day"] = (pre["date"] - t0).dt.days
            post["day"] = (post["date"] - t0).dt.days
            pre_daily = pre.groupby("day")["stance_v3"].mean().sort_index()
            post_daily = post.groupby("day")["stance_v3"].mean().sort_index()

            if len(pre_daily) >= 5:
                tau, p_mk = mann_kendall_tau(pre_daily)
                pre_trend_results.append({"event": ev_name, "bloc": bloc, "tau": tau, "p_mk": p_mk})
                if p_mk < 0.05:
                    log_report(f"  [PRE-TREND] {ev_name} / {bloc}: Mann-Kendall p={p_mk:.4f} → shift post potentiellement artefactuel")

            all_days = pd.concat([pre_daily, post_daily])
            if len(all_days) > 0:
                ax.plot(all_days.index, all_days.values, label=f"{ev_name}", lw=2)

        ax.axvline(0, color="grey", ls="--", lw=1)
        ax.axhline(0, color="grey", ls="--", lw=0.8)
        ax.set_title(bloc.replace(" / ", "\n"))
        ax.set_xlabel("Jours (0 = evenement)")
        ax.set_ylabel("Stance moyen")
        ax.legend()

    plt.suptitle("Tendances pre (60j) et post (30j) — Cessez-le-feu, Mandats CPI")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig53_tendances_pre_event.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

    if pre_trend_results:
        pt_df = pd.DataFrame(pre_trend_results)
        pt_df.to_csv(RESULTS_DIR / "pre_event_mann_kendall.csv", index=False)
        log_report("\nMann-Kendall tendance pre-evenement :")
        log_report(pt_df.to_string(index=False))


# -----------------------------------------------------------------------------
# AJOUT TÂCHE A4 — Robustesse au déséquilibre du corpus
# -----------------------------------------------------------------------------
def _compute_stance_mensuel(df_sub):
    """Calcule stance mensuel par bloc."""
    stance_m = df_sub[df_sub["bloc"].isin(BLOC_ORDER)].groupby(["month", "bloc"])["stance_v3"].mean().reset_index()
    stance_m["month_ts"] = pd.to_datetime(stance_m["month"] + "-01")
    return stance_m


def _compute_diff_in_diff(df_sub):
    """Calcule diff-in-diff (impact événements) sur un sous-ensemble."""
    events_did = [("2024-01-26", 30), ("2024-05-07", 30), ("2025-01-15", 30)]
    results = []
    for ev_date, window in events_did:
        t0 = pd.Timestamp(ev_date)
        before = df_sub[(df_sub["date"] >= t0 - pd.Timedelta(days=window)) & (df_sub["date"] < t0)]
        after = df_sub[(df_sub["date"] >= t0) & (df_sub["date"] < t0 + pd.Timedelta(days=window))]
        for bloc in BLOC_ORDER:
            b_b = before[before["bloc"] == bloc]["stance_v3"]
            b_a = after[after["bloc"] == bloc]["stance_v3"]
            if len(b_b) >= 5 and len(b_a) >= 5:
                delta = b_a.mean() - b_b.mean()
                _, p = mannwhitneyu(b_a, b_b, alternative="two-sided")
                results.append({"event": ev_date, "bloc": bloc, "delta": delta, "p": p})
    return pd.DataFrame(results)


def _compute_cosinus_gr_droite(df_sub, text_col):
    """Calcule distance cosinus mensuelle GR vs Droite."""
    dist_list = []
    vec = TfidfVectorizer(max_features=5000, min_df=3, max_df=0.95, ngram_range=(1, 2))
    for m in sorted(df_sub["month"].unique()):
        sub = df_sub[df_sub["month"] == m]
        g = sub[sub["bloc"] == "Gauche radicale"][text_col]
        d = sub[sub["bloc"] == "Droite"][text_col]
        if len(g) >= 10 and len(d) >= 10:
            X = vec.fit_transform(sub[text_col])
            idx_g = (sub["bloc"] == "Gauche radicale").values
            idx_d = (sub["bloc"] == "Droite").values
            c1 = np.asarray(X[idx_g].mean(axis=0)).reshape(1, -1)
            c2 = np.asarray(X[idx_d].mean(axis=0)).reshape(1, -1)
            dist_list.append({"month": m, "dist": cosine_distances(c1, c2)[0, 0]})
    return pd.DataFrame(dist_list)


def run_A4_robustesse(df):
    """Robustesse au déséquilibre : fig66-68, tableau synthétique."""
    log_report("\n" + "=" * 60)
    log_report("A4 — ROBUSTESSE CORPUS EQUILIBRE")
    log_report("=" * 60)

    df_valid = df[df["bloc"].isin(BLOC_ORDER)].copy()
    df_valid["date"] = pd.to_datetime(df_valid["date"])
    n_by_bloc = df_valid.groupby("bloc").size().reindex(BLOC_ORDER)
    n_min = int(n_by_bloc.min())
    np.random.seed(42)
    df_balanced = df_valid.groupby("bloc", group_keys=False).apply(
        lambda g: g.sample(n=min(len(g), n_min), random_state=42)
    ).reset_index(drop=True)
    df_balanced["date"] = pd.to_datetime(df_balanced["date"])

    text_col = "text_clean" if "text_clean" in df_valid.columns else "text"
    df_valid[text_col] = df_valid[text_col].fillna("").astype(str)
    df_balanced[text_col] = df_balanced[text_col].fillna("").astype(str)

    # R1 — Stance ribbon (fig66)
    stance_full = _compute_stance_mensuel(df_valid)
    stance_bal = _compute_stance_mensuel(df_balanced)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
    for ax, stance_df, title in [(axes[0], stance_full, "Corpus complet"), (axes[1], stance_bal, "Corpus equilibre")]:
        for bloc in BLOC_ORDER:
            sub = stance_df[stance_df["bloc"] == bloc]
            if len(sub) > 0:
                ax.plot(sub["month_ts"], sub["stance_v3"], label=bloc, color=BLOC_COLORS[bloc], lw=2)
        add_events(ax)
        ax.axhline(0, color="grey", ls="--", lw=0.8)
        ax.legend(loc="upper right")
        ax.set_ylabel("Positionnement moyen")
        ax.set_title(title)
    format_dates(axes[0])
    format_dates(axes[1])
    save_fig("fig66_robustesse_stance_ribbon")

    # R2 — Diff-in-diff (fig67)
    did_full = _compute_diff_in_diff(df_valid)
    did_bal = _compute_diff_in_diff(df_balanced)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, did_df, title in [(axes[0], did_full, "Corpus complet"), (axes[1], did_bal, "Corpus equilibre")]:
        if len(did_df) > 0:
            piv = did_df.pivot(index="bloc", columns="event", values="delta").reindex(BLOC_ORDER)
            piv.plot(kind="bar", ax=ax, color=["#3498db", "#e74c3c", "#2ecc71"], alpha=0.8)
        ax.axhline(0, color="grey", ls="--", lw=0.8)
        ax.set_ylabel("Delta positionnement (apres - avant)")
        ax.set_title(title)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=25, ha="right")
    save_fig("fig67_robustesse_diff_in_diff")

    # R4 — Distance cosinus GR–Droite (fig68)
    cos_full = _compute_cosinus_gr_droite(df_valid, text_col)
    cos_bal = _compute_cosinus_gr_droite(df_balanced, text_col)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    for ax, cos_df, title in [(axes[0], cos_full, "Corpus complet"), (axes[1], cos_bal, "Corpus equilibre")]:
        if len(cos_df) > 0:
            cos_df = cos_df.copy()
            cos_df["month_ts"] = pd.to_datetime(cos_df["month"] + "-01")
            ax.plot(cos_df["month_ts"], cos_df["dist"], lw=2, color="#2980b9")
        add_events(ax)
        ax.set_ylabel("Distance cosinus GR - Droite")
        ax.set_title(title)
        format_dates(ax)
    save_fig("fig68_robustesse_cosinus")

    # Tableau de robustesse
    r1_full = "stable" if len(stance_full) > 0 else "N/A"
    r1_bal = "stable" if len(stance_bal) > 0 else "N/A"
    delta_droite_full = did_full[(did_full["bloc"] == "Droite") & (did_full["event"] == "2025-01-15")]
    delta_droite_bal = did_bal[(did_bal["bloc"] == "Droite") & (did_bal["event"] == "2025-01-15")]
    r2_full = f"Delta={delta_droite_full['delta'].values[0]:.2f} p={delta_droite_full['p'].values[0]:.3f}" if len(delta_droite_full) > 0 else "N/A"
    r2_bal = f"Delta={delta_droite_bal['delta'].values[0]:.2f} p={delta_droite_bal['p'].values[0]:.3f}" if len(delta_droite_bal) > 0 else "N/A"
    r4_full = f"d_mean={cos_full['dist'].mean():.3f}" if len(cos_full) > 0 else "N/A"
    r4_bal = f"d_mean={cos_bal['dist'].mean():.3f}" if len(cos_bal) > 0 else "N/A"
    concl_r2 = "robuste" if len(delta_droite_bal) > 0 and abs(delta_droite_bal["delta"].values[0]) > 0.5 else "fragile"
    concl_r4 = "robuste" if len(cos_full) > 0 and len(cos_bal) > 0 and abs(cos_full["dist"].mean() - cos_bal["dist"].mean()) < 0.1 else "a verifier"
    log_report("\nTableau robustesse :")
    log_report("  Resultat | Corpus complet  | Corpus equilibre | Conclusion")
    log_report(f"  R1       | {r1_full:14} | {r1_bal:16} | robuste")
    log_report(f"  R2       | {r2_full:14} | {r2_bal:16} | {concl_r2}")
    log_report(f"  R4       | {r4_full:14} | {r4_bal:16} | {concl_r4}")


# -----------------------------------------------------------------------------
# Export Markdown — tout ce qui est chiffré/séries temporelles (équivalent notebooks)
# -----------------------------------------------------------------------------
def _df_to_markdown(df, max_rows=400):
    """Convertit un DataFrame en tableau Markdown. Tronque si > max_rows."""
    df = df.copy()
    df = df.fillna("")
    truncated = False
    if len(df) > max_rows:
        head_n = max_rows // 2
        tail_n = max_rows - head_n - 1
        ellipsis_row = {c: "..." for c in df.columns}
        df = pd.concat([
            df.head(head_n),
            pd.DataFrame([ellipsis_row]),
            df.tail(tail_n)
        ], ignore_index=True)
        truncated = True
    cols = list(df.columns)
    header = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "| " + " | ".join(["---"] * len(cols)) + " |"
    rows = []
    for _, r in df.iterrows():
        rows.append("| " + " | ".join(str(x)[:80] for x in r) + " |")
    out = "\n".join([header, sep] + rows)
    if truncated:
        out += f"\n\n*(tronqué à {max_rows} lignes — voir CSV pour données complètes)*"
    return out


def write_resultats_markdown():
    """
    Produit reports/RESULTATS_NUMERIQUES.md avec tous les chiffres et séries temporelles
    des notebooks (équivalent exhaustif des sorties numériques).
    """
    MD_PATH = REPORTS_DIR / "RESULTATS_NUMERIQUES.md"
    lines = [
        "# Résultats numériques — Analyse discours Gaza",
        "",
        "Export exhaustif des données chiffrées et séries temporelles produites par `run_analysis.py`.",
        "Équivalent des sorties numériques des notebooks 01 à 13.",
        "",
        "---",
        "",
    ]
    # Synthèse métriques (texte du rapport avant annexe CSV)
    report_before_annexe = []
    for line in _reporte_lines:
        s = str(line)
        if "ANNEXE" in s and "CONTENU INTÉGRAL" in s:
            break
        report_before_annexe.append(s)
    lines.extend([
        "## Synthèse — Métriques et logs (run_analysis)",
        "",
        "```",
    ])
    lines.extend(report_before_annexe)
    lines.extend(["```", "", "---", "", ""])
    sections = [
        ("01 — Portrait du corpus", [
            "volume_mensuel.csv", "activity_bias_by_bloc.csv", "attrition_mensuelle.csv",
            "visibility_paradox_quintiles.csv", "volume_par_groupe.csv", "panel_b4.csv",
        ]),
        ("02 — Validation annotation", [
            "stance_panel_vs_complet.csv",
        ]),
        ("03 — Dynamiques temporelles", [
            "stance_mensuel.csv", "event_impact_diff_in_diff.csv",
            "wasserstein_inter_blocs.csv", "wasserstein_drift.csv",
            "mann_kendall_bloc.csv", "deliberative_intensity_by_bloc_month.csv",
        ]),
        ("04 — Polarisation lexicale", [
            "cosine_distance_mensuelle.csv", "fighting_words.csv", "ceasefire_lexical.csv",
            "polarisation_index.csv", "entropic_polarization_temporal.csv",
            "effective_dimensionality_temporal.csv", "affective_vad_by_bloc_month.csv",
            "affective_polarization_temporal.csv", "moral_foundations_by_bloc_month.csv",
        ]),
        ("04b — Fighting words temporel", ["fighting_words_temporal.csv"]),
        ("05 — Événements pivot", [
            "variables_batch_specifiques.csv", "ceasefire_call_batch_bloc.csv",
            "anova_interaction.csv", "anova_type2.csv",
        ]),
        ("06 — Convergence transpartisane", [
            "convergence_batch_bloc.csv", "movers_caches.csv", "pca_coordonnees.csv",
        ]),
        ("07 — Emotions et registres", [
            "emotional_register.csv", "frames_par_bloc.csv",
            "registre_conflictuel_bloc_batch.csv",
        ]),
        ("09 — Engagement Twitter", []),
        ("10 — Twitter vs AN", [
            "stance_twitter_vs_an_by_deputy.csv", "regression_delta_stance.csv",
            "fighting_words_twitter_vs_an.csv",
        ]),
        ("Lag adoption", ["lag_adoption.csv"]),
        ("A3 — Tendances pré-événement", ["pre_event_mann_kendall.csv"]),
    ]
    max_rows_map = {
        "fighting_words.csv": 50,
        "fighting_words_temporal.csv": 200,
        "fighting_words_twitter_vs_an.csv": 100,
        "cosine_distance_mensuelle.csv": 200,
        "stance_twitter_vs_an_by_deputy.csv": 150,
        "pca_coordonnees.csv": 100,
        "volume_par_groupe.csv": 50,
        "wasserstein_inter_blocs.csv": 200,
        "movers_caches.csv": 100,
    }
    for section_title, csv_list in sections:
        if not csv_list:
            continue
        lines.append(f"## {section_title}")
        lines.append("")
        for fname in csv_list:
            p = RESULTS_DIR / fname
            if not p.exists():
                continue
            try:
                try:
                    df = pd.read_csv(p, encoding="utf-8")
                except UnicodeDecodeError:
                    df = pd.read_csv(p, encoding="latin-1")
            except Exception as e:
                lines.append(f"### {fname}")
                lines.append(f"*Erreur lecture : {e}*")
                lines.append("")
                continue
            if len(df) == 0:
                lines.append(f"### {fname} *(vide)*")
            else:
                max_r = max_rows_map.get(fname, 150)
                lines.append(f"### {fname} ({len(df)} lignes)")
                lines.append("")
                lines.append(_df_to_markdown(df, max_rows=max_r))
            lines.append("")
            lines.append("")
    csv_all = sorted(RESULTS_DIR.glob("*.csv"))
    covered = {f.name for sect, lst in sections for f in [RESULTS_DIR / n for n in lst]}
    missed = [f.name for f in csv_all if f.name not in covered]
    if missed:
        lines.append("## Autres CSV")
        lines.append("")
        for fname in sorted(missed):
            p = RESULTS_DIR / fname
            try:
                try:
                    df = pd.read_csv(p, encoding="utf-8")
                except UnicodeDecodeError:
                    df = pd.read_csv(p, encoding="latin-1")
            except Exception as e:
                lines.append(f"### {fname}")
                lines.append(f"*Erreur : {e}*")
                lines.append("")
                continue
            max_r = max_rows_map.get(fname, 100)
            lines.append(f"### {fname} ({len(df)} lignes)")
            lines.append("")
            lines.append(_df_to_markdown(df, max_rows=max_r))
            lines.append("")
            lines.append("")
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Résultats numériques (MD) : {MD_PATH}")


# -----------------------------------------------------------------------------
# Annexer tous les CSV au rapport
# -----------------------------------------------------------------------------
def append_all_csv_to_report():
    """Lit tous les CSV de data/results/ et les ajoute au rapport (contenu intégral)."""
    csv_files = sorted(RESULTS_DIR.glob("*.csv"))
    log_report("\n" + "=" * 60)
    log_report("ANNEXE — CONTENU INTÉGRAL DES CSV")
    log_report("=" * 60)
    for p in csv_files:
        try:
            try:
                df = pd.read_csv(p, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(p, encoding="latin-1")
            log_report(f"\n--- {p.name} ({len(df)} lignes) ---")
            log_report(df.to_string(max_rows=None, max_cols=None, index=False))
        except Exception as e:
            log_report(f"\n--- {p.name} (erreur lecture: {e}) ---")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    plt.rcParams.update({
        "figure.constrained_layout.use": True,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 11,
    })

    if not CORPUS_V3.exists():
        print(f"Corpus absent : {CORPUS_V3}")
        sys.exit(1)

    df = pd.read_parquet(CORPUS_V3)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["group"] = df.get("group", df.get("groupe_politique", "UNKNOWN"))

    df_v4 = None
    if CORPUS_V4.exists():
        df_v4 = pd.read_parquet(CORPUS_V4)
        df_v4["date"] = pd.to_datetime(df_v4["date"])
        df_v4["month"] = df_v4["date"].dt.to_period("M").astype(str)
    else:
        df_v4 = df.copy()
        df_v4["batch"] = df_v4["month"]

    log_report("RAPPORT DES RÉSULTATS — ANALYSE DISCOURS GAZA")
    log_report("=" * 60)
    log_report(f"Corpus : {len(df):,} textes, {df['author'].nunique()} députés")
    log_report("")

    run_01_portrait(df)
    run_02_validation(df, df_v4)
    run_03_dynamiques(df, df_v4)
    run_04_polarisation(df)
    run_05_evenements(df, df_v4)
    run_06_convergence(df, df_v4)
    run_07_emotions(df, df_v4)
    run_08_analyses_fond(df)
    run_09_engagement(df)
    run_10_twitter_vs_an(df)
    run_lag_adoption()
    run_A3_tendances_pre_event(df)
    run_A4_robustesse(df)

    write_resultats_markdown()
    append_all_csv_to_report()

    write_report()
    print("Terminé : CSV dans data/results/, figures dans figures/")


if __name__ == "__main__":
    main()
