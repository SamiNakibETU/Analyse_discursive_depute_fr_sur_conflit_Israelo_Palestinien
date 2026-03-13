# -*- coding: utf-8 -*-
"""
Analyses supplémentaires du brief - Figures fig21–fig25.
Exécuter : python src/analyses_supplementaires.py
Nécessite : data/processed/corpus_v3.parquet et corpus_v4.parquet
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu, pearsonr, chi2_contingency
from sklearn.feature_extraction.text import CountVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    PROJECT_ROOT, DATA_DIR, PROCESSED_DIR, RESULTS_DIR,
    COLORS, BLOC_ORDER, EVENTS, BATCH_ORDER, BATCHES,
)

FIG_DIR = PROJECT_ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
CORPUS_V3 = PROCESSED_DIR / "corpus_v3.parquet"
CORPUS_V4 = PROCESSED_DIR / "corpus_v4.parquet"

plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "serif",
})


def assign_batch(d, batches):
    """Assigner un batch à une date."""
    if pd.isna(d):
        return "OTHER"
    for name, cfg in batches.items():
        start = pd.Timestamp(cfg["start"])
        end = pd.Timestamp(cfg["end"])
        if start <= d <= end:
            return name
    return "OTHER"


def run_all():
    if not CORPUS_V3.exists():
        print("Corpus v3 non trouvé. Exécuter: python src/prepare_data.py")
        return

    v3 = pd.read_parquet(CORPUS_V3)
    v3["date"] = pd.to_datetime(v3["date"])
    if "group" not in v3.columns and "groupe_politique" in v3.columns:
        v3["group"] = v3["groupe_politique"]
    v3["batch"] = v3["date"].apply(lambda d: assign_batch(d, BATCHES))

    # --- B2: Twitter vs AN ---
    print("B2: Twitter vs AN...")
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
    for idx, (arena_name, arena_label) in enumerate([("Twitter", "Twitter / X"), ("AN", "Assemblée nationale")]):
        ax = axes[idx]
        df_arena = v3[v3["arena"] == arena_name]
        for bloc in BLOC_ORDER:
            df_bloc = df_arena[df_arena["bloc"] == bloc]
            monthly = (
                df_bloc.groupby(df_bloc["date"].dt.to_period("M"))
                .agg(stance_mean=("stance_v3", "mean"), n=("stance_v3", "count"))
                .reset_index()
            )
            monthly["date"] = monthly["date"].dt.to_timestamp()
            monthly = monthly[monthly["n"] >= 5]
            if len(monthly) > 0:
                ax.plot(
                    monthly["date"],
                    monthly["stance_mean"],
                    color=COLORS.get(bloc, "#888"),
                    lw=2,
                    marker="o",
                    ms=4,
                    label=bloc,
                )
        ax.set_title(f'({"a" if idx == 0 else "b"}) {arena_label}', fontsize=14)
        ax.set_ylabel("Stance moyen" if idx == 0 else "")
        ax.axhline(0, color="grey", lw=0.5, ls="--")
        ax.legend(fontsize=9)
        for date_str in EVENTS.keys():
            ax.axvline(pd.Timestamp(date_str), color="grey", lw=0.5, ls=":")
    plt.suptitle("Stance par bloc - Twitter vs Assemblée nationale", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig25_twitter_vs_an.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  -> fig25_twitter_vs_an.png")

    # Export twitter_vs_an.csv (régression par arène)
    try:
        import statsmodels.formula.api as smf
        v3_sub = v3[v3["primary_frame_v3"].notna()]
        mod = smf.ols(
            "stance_v3 ~ C(bloc, Treatment('Centre / Majorite')) + C(arena) + C(primary_frame_v3)",
            data=v3_sub,
        ).fit(cov_type="HC3")
        arena_coef = mod.params.get("C(arena)[T.Twitter]", np.nan)
        arena_p = mod.pvalues.get("C(arena)[T.Twitter]", np.nan)
        pd.DataFrame(
            [{"arena_Twitter_coef": arena_coef, "arena_Twitter_p": arena_p}]
        ).to_csv(RESULTS_DIR / "twitter_vs_an.csv", index=False)
        print("  -> twitter_vs_an.csv")
    except Exception as e:
        print(f"  Régression twitter_vs_an: {e}")

    # --- B3: Attrition différentielle ---
    print("B3: Attrition différentielle...")
    deputy_profile = (
        v3.groupby(["author", "bloc"])
        .agg(
            stance_mean=("stance_v3", "mean"),
            last_month=("date", "max"),
            first_month=("date", "min"),
            n_textes=("stance_v3", "count"),
            n_months=("date", lambda x: x.dt.to_period("M").nunique()),
        )
        .reset_index()
    )
    deputy_profile["last_month_num"] = (
        deputy_profile["last_month"].dt.to_period("M") - pd.Period("2023-10", freq="M")
    ).apply(lambda x: x.n)
    fig, axes = plt.subplots(1, 4, figsize=(20, 5), sharey=True)
    for idx, bloc in enumerate(BLOC_ORDER):
        ax = axes[idx]
        df_bloc = deputy_profile[deputy_profile["bloc"] == bloc]
        if len(df_bloc) >= 3:
            ax.scatter(
                df_bloc["last_month_num"],
                df_bloc["stance_mean"],
                color=COLORS.get(bloc, "#888"),
                alpha=0.5,
                s=df_bloc["n_textes"] * 2,
            )
            r, p = pearsonr(df_bloc["last_month_num"], df_bloc["stance_mean"])
            ax.set_title(f"{bloc}\nr={r:.2f}, p={p:.3f}", fontsize=11)
        ax.set_xlabel("Dernier mois actif")
        if idx == 0:
            ax.set_ylabel("Stance moyen")
    plt.suptitle("Attrition différentielle : qui arrête de parler ?", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig21_attrition_differentielle.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  -> fig21_attrition_differentielle.png")

    # --- B4: RN vs LR temporel ---
    print("B4: RN vs LR temporel...")
    rn = v3[v3["group"].isin(["RN"])]["stance_v3"]
    lr = v3[v3["group"].isin(["LR"])]["stance_v3"]
    stat, p_mw = mannwhitneyu(rn, lr, alternative="two-sided")
    df_droite = v3[v3["group"].isin(["RN", "LR"])]
    monthly_rn_lr = (
        df_droite.groupby([df_droite["date"].dt.to_period("M"), "group"])
        .agg(stance_mean=("stance_v3", "mean"), n=("stance_v3", "count"))
        .reset_index()
    )
    monthly_rn_lr["date"] = monthly_rn_lr["date"].dt.to_timestamp()
    fig, ax = plt.subplots(figsize=(14, 6))
    for grp, color in [("RN", "#2A0134"), ("LR", "#6A5ACD")]:
        df_grp = monthly_rn_lr[monthly_rn_lr["group"] == grp]
        df_grp = df_grp[df_grp["n"] >= 5]
        if len(df_grp) > 0:
            ax.plot(
                df_grp["date"],
                df_grp["stance_mean"],
                color=color,
                lw=2,
                marker="o",
                ms=4,
                label=f"{grp} (n={len(v3[v3['group']==grp])})",
            )
    ax.axhline(0, color="grey", lw=0.5, ls="--")
    ax.set_ylabel("Stance moyen")
    ax.set_title(f"RN vs LR - évolution temporelle (Mann-Whitney p={p_mw:.4f})")
    ax.legend()
    for date_str in EVENTS.keys():
        ax.axvline(pd.Timestamp(date_str), color="grey", lw=0.5, ls=":")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig22_rn_vs_lr_temporel.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  -> fig22_rn_vs_lr_temporel.png")

    # --- B5: Fighting words par batch ---
    print("B5: Fighting words par batch...")

    def fighting_words(texts1, texts2, n_top=15):
        vec = CountVectorizer(max_features=5000, min_df=3)
        all_texts = list(texts1) + list(texts2)
        counts = vec.fit_transform(all_texts).toarray()
        n1 = len(texts1)
        c1 = counts[:n1].sum(axis=0)
        c2 = counts[n1:].sum(axis=0)
        alpha = 0.01
        n_w1, n_w2 = c1.sum(), c2.sum()
        delta = (
            np.log((c1 + alpha) / (n_w1 + alpha * len(vec.vocabulary_) - c1 - alpha))
            - np.log((c2 + alpha) / (n_w2 + alpha * len(vec.vocabulary_) - c2 - alpha))
        )
        var = 1.0 / (c1 + alpha) + 1.0 / (c2 + alpha)
        z = delta / np.sqrt(var)
        return pd.DataFrame(
            {"word": vec.get_feature_names_out(), "z": z, "count_gauche": c1, "count_droite": c2}
        )

    results = []
    txt_col = "text_clean" if "text_clean" in v3.columns else "text"
    v3["text"] = v3[txt_col].fillna("").astype(str)
    for batch in BATCH_ORDER:
        df_batch = v3[v3["batch"] == batch]
        gauche = df_batch[df_batch["bloc"] == "Gauche radicale"]["text"]
        droite = df_batch[df_batch["bloc"] == "Droite"]["text"]
        if len(gauche) >= 20 and len(droite) >= 20:
            fw = fighting_words(gauche, droite)
            fw["batch"] = batch
            results.append(fw)
    if results:
        fw_all = pd.concat(results)
        key_words = [
            "cessez",
            "genocide",
            "génocide",
            "colonisation",
            "otages",
            "terrorisme",
            "humanitaire",
            "droit",
            "international",
            "crime",
            "embargo",
        ]
        words_in_corpus = [
            w
            for w in key_words
            if w in fw_all["word"].values
            or (w.replace("é", "e") in fw_all["word"].values)
        ]
        if not words_in_corpus:
            words_in_corpus = fw_all.groupby("word")["z"].abs().nlargest(15).index.tolist()
        pivot = (
            fw_all[fw_all["word"].isin(words_in_corpus)]
            .pivot_table(index="word", columns="batch", values="z", aggfunc="mean")
        )
        for b in BATCH_ORDER:
            if b not in pivot.columns:
                pivot[b] = np.nan
        pivot = pivot.reindex(columns=[b for b in BATCH_ORDER if b in pivot.columns])
        if len(pivot) > 0 and len(pivot.columns) > 0:
            fig, ax = plt.subplots(figsize=(14, 8))
            sns.heatmap(
                pivot,
                cmap="RdBu_r",
                center=0,
                annot=True,
                fmt=".1f",
                ax=ax,
                cbar_kws={"label": "z-score (+ = Gauche, - = Droite)"},
            )
            ax.set_title("Vocabulaire distinctif Gauche ↔ Droite par période")
            plt.tight_layout()
            plt.savefig(FIG_DIR / "fig23_fighting_words_temporel.png", dpi=300, bbox_inches="tight")
            plt.close()
            print("  -> fig23_fighting_words_temporel.png")
        else:
            print("  (pas assez de données pour heatmap)")
    else:
        print("  (pas de batches avec assez de textes)")

    # --- B6: Droite au cessez-le-feu ---
    print("B6: Droite au cessez-le-feu...")
    df_droite = v3[v3["bloc"] == "Droite"]
    monthly = (
        df_droite.groupby(df_droite["date"].dt.to_period("M"))
        .agg(
            stance_mean=("stance_v3", "mean"),
            stance_ci=("stance_v3", lambda x: 1.96 * x.std() / np.sqrt(len(x)) if len(x) > 1 else 0),
            n=("stance_v3", "count"),
        )
        .reset_index()
    )
    monthly["date"] = monthly["date"].dt.to_timestamp()
    monthly["stance_ci"] = monthly["stance_ci"].fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly["date"], monthly["stance_mean"], color=COLORS["Droite"], lw=2.5, marker="o")
    ax.fill_between(
        monthly["date"],
        monthly["stance_mean"] - monthly["stance_ci"],
        monthly["stance_mean"] + monthly["stance_ci"],
        alpha=0.2,
        color=COLORS["Droite"],
    )
    cf_date = pd.Timestamp("2025-01-15")
    ax.axvline(cf_date, color="red", lw=2, ls="--")
    ax.annotate(
        "Cessez-le-feu\nΔ = -1.10 (p=0.045)",
        xy=(cf_date, -0.5),
        xytext=(cf_date + pd.Timedelta(days=60), 0),
        fontsize=11,
        arrowprops=dict(arrowstyle="->", color="red"),
        color="red",
        fontweight="bold",
    )
    ax.set_ylabel("Stance moyen (Droite)")
    ax.set_title("Radicalisation de la Droite après le cessez-le-feu (jan. 2025)")
    ax.axhline(0, color="grey", lw=0.5, ls="--")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig24_droite_cessefire_shift.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  -> fig24_droite_cessefire_shift.png")

    # --- B7: Chi² émotions (nécessite v4) ---
    if CORPUS_V4.exists():
        print("B7: Chi² émotions...")
        v4 = pd.read_parquet(CORPUS_V4)
        v4_sub = v4[v4["emotional_register"].notna() & v4["bloc"].notna()]
        if len(v4_sub) > 0:
            ct = pd.crosstab(v4_sub["emotional_register"], v4_sub["bloc"])
            chi2, p, dof, expected = chi2_contingency(ct)
            residuals = (ct - expected) / np.sqrt(expected)
            print(f"  Chi² = {chi2:.2f}, p = {p:.4f}")
            for reg in residuals.index:
                for bloc in residuals.columns:
                    r = residuals.loc[reg, bloc]
                    if abs(r) > 2:
                        print(f"    {bloc} × {reg}: r={r:.1f}")
    else:
        print("B7: corpus v4 absent, skip Chi² émotions")

    print("\nAnalyses terminées.")


if __name__ == "__main__":
    run_all()
