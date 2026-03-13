# -*- coding: utf-8 -*-
"""
00 - Préparation des données propres.

Produit deux fichiers dans data/processed/ :
  - corpus_v3.parquet  : corpus complet post-7 oct, annoté en v3 (baseline)
  - corpus_v4.parquet  : 5 905 textes sur les 7 fenêtres pivot, annotés en v4

Usage :
    python src/prepare_data.py
"""

import hashlib
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    SOURCE_TWEETS, SOURCE_INTERV, SOURCE_V4_DIR,
    DATA_RAW, DATA_PROC,
    GROUP_TO_BLOC, BLOCS_ORDER, BATCHES,
    MIN_CONFIDENCE, CORPUS_START_DATE,
)


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def text_hash(text: str) -> str:
    return hashlib.md5(str(text)[:500].encode("utf-8", errors="replace")).hexdigest()


def assign_bloc(group: str) -> str:
    return GROUP_TO_BLOC.get(str(group).strip(), "Autre")


# ──────────────────────────────────────────────────────────────────────────────
# ÉTAPE 1 : Charger et nettoyer les tweets
# ──────────────────────────────────────────────────────────────────────────────

def load_tweets() -> pd.DataFrame:
    print("  Chargement des tweets...")
    tw = pd.read_parquet(SOURCE_TWEETS)

    # Colonnes utiles uniquement
    keep = [
        "depute_name", "username", "groupe_politique",
        "text", "date_parsed",
        "retweets", "likes", "replies", "quotes",
        "is_retweet", "is_reply",
        "stance_v3", "confidence_v3", "intensity_v3",
        "primary_frame_v3", "primary_target_v3",
        "is_off_topic_v3", "is_ambiguous_v3", "has_both_sides_v3",
        "reasoning_v3",
    ]
    tw = tw[[c for c in keep if c in tw.columns]].copy()

    # Normalisation
    tw["author"]     = tw["depute_name"].fillna(tw.get("username", ""))
    tw["group"]      = tw["groupe_politique"].fillna("UNKNOWN")
    tw["bloc"]       = tw["group"].apply(assign_bloc)
    tw["date"]       = pd.to_datetime(tw["date_parsed"], errors="coerce")
    tw["text_clean"] = tw["text"].fillna("").str.strip()
    tw["arena"]      = "Twitter"
    tw["retweets"]   = pd.to_numeric(tw.get("retweets", 0), errors="coerce").fillna(0).astype(int)
    tw["likes"]      = pd.to_numeric(tw.get("likes", 0), errors="coerce").fillna(0).astype(int)
    tw["replies"]    = pd.to_numeric(tw.get("replies", 0), errors="coerce").fillna(0).astype(int)
    tw["quotes"]     = pd.to_numeric(tw.get("quotes", 0), errors="coerce").fillna(0).astype(int)
    tw["engagement"] = tw["retweets"] + tw["likes"] + tw["replies"] + tw["quotes"]
    tw["is_retweet"] = tw.get("is_retweet", False).fillna(False).astype(bool)

    print(f"    {len(tw):,} tweets chargés")
    return tw


# ──────────────────────────────────────────────────────────────────────────────
# ÉTAPE 2 : Charger et nettoyer les interventions AN
# ──────────────────────────────────────────────────────────────────────────────

def load_interventions() -> pd.DataFrame:
    print("  Chargement des interventions AN...")
    iv = pd.read_parquet(SOURCE_INTERV)

    # Colonnes utiles
    keep = [
        "speaker_name", "matched_name", "AUTEUR",
        "GROUPE", "matched_group",
        "cleaned_text", "TEXTE",
        "sitting_date",
        "stance_v3", "confidence_v3", "intensity_v3",
        "primary_frame_v3", "primary_target_v3",
        "is_off_topic_v3", "is_ambiguous_v3", "has_both_sides_v3",
        "reasoning_v3",
    ]
    iv = iv[[c for c in keep if c in iv.columns]].copy()

    # Normalisation
    for col in ["speaker_name", "matched_name", "AUTEUR"]:
        if col not in iv.columns:
            iv[col] = None
    iv["author"] = (
        iv["speaker_name"].fillna(iv["matched_name"]).fillna(iv["AUTEUR"]).fillna("Inconnu")
    )

    for col in ["GROUPE", "matched_group"]:
        if col not in iv.columns:
            iv[col] = None
    iv["group"] = iv["GROUPE"].fillna(iv["matched_group"]).fillna("UNKNOWN")
    iv["bloc"]  = iv["group"].apply(assign_bloc)

    iv["date"] = pd.to_datetime(iv["sitting_date"], errors="coerce")

    if "cleaned_text" in iv.columns and "TEXTE" in iv.columns:
        iv["text_clean"] = iv["cleaned_text"].fillna(iv["TEXTE"]).fillna("").str.strip()
    elif "cleaned_text" in iv.columns:
        iv["text_clean"] = iv["cleaned_text"].fillna("").str.strip()
    else:
        iv["text_clean"] = iv["TEXTE"].fillna("").str.strip()

    iv["arena"]      = "AN"
    iv["retweets"]   = 0
    iv["likes"]      = 0
    iv["replies"]    = 0
    iv["quotes"]     = 0
    iv["engagement"] = 0
    iv["is_retweet"] = False

    print(f"    {len(iv):,} interventions chargées")
    return iv


# ──────────────────────────────────────────────────────────────────────────────
# ÉTAPE 3 : Construire corpus_v3 (baseline)
# ──────────────────────────────────────────────────────────────────────────────

SHARED_COLS = [
    "author", "group", "bloc", "arena", "date", "text_clean",
    "retweets", "likes", "replies", "quotes", "engagement", "is_retweet",
    "stance_v3", "confidence_v3", "intensity_v3",
    "primary_frame_v3", "primary_target_v3",
    "is_off_topic_v3", "is_ambiguous_v3", "has_both_sides_v3",
    "reasoning_v3",
]

def build_corpus_v3(tw: pd.DataFrame, iv: pd.DataFrame) -> pd.DataFrame:
    print("  Construction du corpus v3...")

    for c in SHARED_COLS:
        if c not in tw.columns:
            tw[c] = None
        if c not in iv.columns:
            iv[c] = None

    df = pd.concat([tw[SHARED_COLS], iv[SHARED_COLS]], ignore_index=True)

    # Filtres qualité
    mask_post   = df["date"] >= pd.Timestamp(CORPUS_START_DATE)
    mask_conf   = df["confidence_v3"].fillna(0) >= MIN_CONFIDENCE
    mask_topic  = ~df["is_off_topic_v3"].fillna(False)
    mask_bloc   = df["bloc"].isin(["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"])
    mask_date   = df["date"].notna()
    mask_text   = df["text_clean"].str.len() > 10

    df_full = df.copy()
    df_full["text_hash"] = df_full["text_clean"].apply(text_hash)
    df_full["month"]     = df_full["date"].dt.to_period("M").astype(str)
    df_full["year"]      = df_full["date"].dt.year

    # Corpus filtré (post-7 oct, qualité)
    df_filt = df_full[mask_post & mask_conf & mask_topic & mask_bloc & mask_date & mask_text].copy()
    df_filt = df_filt.reset_index(drop=True)

    print(f"    Corpus brut total : {len(df_full):,} textes")
    print(f"    Corpus post-7 oct filtré : {len(df_filt):,} textes")
    print(f"    Répartition:")
    for bloc in BLOCS_ORDER:
        n = (df_filt["bloc"] == bloc).sum()
        pct = 100 * n / len(df_filt)
        print(f"      {bloc}: {n:,} ({pct:.1f}%)")
    print(f"    Twitter: {(df_filt['arena']=='Twitter').sum():,} | AN: {(df_filt['arena']=='AN').sum():,}")

    return df_filt


# ──────────────────────────────────────────────────────────────────────────────
# ÉTAPE 4 : Construire corpus_v4 (annotations LLM par période)
# ──────────────────────────────────────────────────────────────────────────────

V4_GLOBAL_COLS = [
    "stance_v4", "ceasefire_call", "ceasefire_type",
    "target_primary", "target_secondary", "frame_primary",
    "conditionality", "emotional_register", "key_demands",
    "reasoning_v4", "flags",
]

V4_PERIOD_COLS = {
    "CHOC":             ["condemns_hamas_attack", "self_defense_mention",
                         "proportionality_issue", "displacement_mention"],
    "POST_CIJ":         ["icj_reference", "genocide_framing", "icc_mention"],
    "RAFAH":            ["rafah_reaction", "icc_mention", "genocide_framing"],
    "POST_SINWAR":      ["sinwar_reaction", "famine_mention", "ethnic_cleansing_frame"],
    "MANDATS_CPI":      ["icc_warrants_position", "genocide_framing"],
    "CEASEFIRE_BREACH": ["ceasefire_breach_blame", "reconstruction_mention", "two_state_mention"],
    "NEW_OFFENSIVE":    ["conquest_framing", "state_recognition_mention", "transpartisan_convergence"],
}

BASE_COLS_FROM_V4 = [
    "author", "group", "bloc", "arena", "date", "text_clean",
    "retweets", "likes", "stance_v3", "confidence_v3",
    "primary_frame_v3", "primary_target_v3",
]

def _normalize_v4_row(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les types pour cohérence inter-batches."""
    # target_secondary : peut être liste ou string
    if "target_secondary" in df.columns:
        df["target_secondary"] = df["target_secondary"].apply(
            lambda x: x[0] if isinstance(x, list) and x
            else (None if isinstance(x, list) else x)
        )
    # key_demands et flags : doivent être des listes
    for col in ["key_demands", "flags"]:
        if col in df.columns:
            def _to_list(x):
                if isinstance(x, (list, np.ndarray)):
                    return list(x)
                if x is None:
                    return []
                if isinstance(x, float) and np.isnan(x):
                    return []
                if isinstance(x, str) and x == "":
                    return []
                return [str(x)]
            df[col] = df[col].apply(_to_list)
    # Normaliser "none" string -> None
    for col in ["ceasefire_type", "target_secondary"]:
        if col in df.columns:
            df[col] = df[col].replace({"none": None, "": None})
    # stance_v4 : entier
    if "stance_v4" in df.columns:
        df["stance_v4"] = pd.to_numeric(df["stance_v4"], errors="coerce").round().astype("Int64")
    # ceasefire_call : booléen
    if "ceasefire_call" in df.columns:
        df["ceasefire_call"] = df["ceasefire_call"].fillna(False).astype(bool)
    return df


def build_corpus_v4() -> pd.DataFrame:
    print("  Construction du corpus v4...")
    frames = []

    for batch_name, batch_cfg in BATCHES.items():
        p = SOURCE_V4_DIR / f"annotations_v4_{batch_name}.parquet"
        if not p.exists():
            print(f"    AVERTISSEMENT: {p.name} introuvable, batch ignoré.")
            continue

        df = pd.read_parquet(p)
        df = _normalize_v4_row(df)
        df["batch"]       = batch_name
        df["batch_label"] = batch_cfg["label"]

        # Ne garder que les annotations réussies
        if "annotation_failed" in df.columns:
            df = df[~df["annotation_failed"].fillna(False)].copy()
        if "stance_v4" in df.columns:
            df = df[df["stance_v4"].notna()].copy()

        frames.append(df)
        print(f"    {batch_name}: {len(df):,} textes annotés avec succès")

    if not frames:
        raise RuntimeError("Aucun fichier v4 trouvé dans " + str(SOURCE_V4_DIR))

    v4 = pd.concat(frames, ignore_index=True)
    v4["text_hash"] = v4["text_clean"].apply(text_hash)
    v4["month"]     = pd.to_datetime(v4["date"]).dt.to_period("M").astype(str)
    v4["year"]      = pd.to_datetime(v4["date"]).dt.year

    # Nettoyage colonnes dupliquées issues du pipeline (condems_hamas_attack, etc.)
    dup_cols = [c for c in v4.columns if c.strip() != c or c.startswith(" ")]
    if dup_cols:
        v4 = v4.drop(columns=dup_cols)

    # Consolider condemns_hamas_attack (deux variantes présentes dans le batch)
    if "condems_hamas_attack" in v4.columns and "condemns_hamas_attack" in v4.columns:
        v4["condemns_hamas_attack"] = v4["condemns_hamas_attack"].combine_first(v4["condems_hamas_attack"])
        v4 = v4.drop(columns=["condems_hamas_attack"])
    elif "condems_hamas_attack" in v4.columns:
        v4 = v4.rename(columns={"condems_hamas_attack": "condemns_hamas_attack"})

    print(f"\n  Total corpus v4 : {len(v4):,} textes")
    print(f"  Répartition par bloc:")
    for bloc in BLOCS_ORDER:
        n = (v4["bloc"] == bloc).sum()
        pct = 100 * n / len(v4)
        print(f"    {bloc}: {n:,} ({pct:.1f}%)")
    print(f"  stance_v4 distribution:")
    print(f"    {v4['stance_v4'].value_counts().sort_index().to_dict()}")
    print(f"  ceasefire_call = True: {v4['ceasefire_call'].sum():,} ({100*v4['ceasefire_call'].mean():.1f}%)")

    return v4


# ──────────────────────────────────────────────────────────────────────────────
# ÉTAPE 5 : Comparaison v3 / v4 (sur les textes communs)
# ──────────────────────────────────────────────────────────────────────────────

def compare_v3_v4(corpus_v3: pd.DataFrame, corpus_v4: pd.DataFrame) -> dict:
    from scipy import stats

    print("  Comparaison v3 / v4 sur les textes communs...")
    merged = corpus_v4.merge(
        corpus_v3[["text_hash", "stance_v3"]].rename(columns={"stance_v3": "stance_v3_ref"}),
        on="text_hash", how="inner"
    )
    if len(merged) == 0:
        print("    Aucun texte commun trouvé.")
        return {}

    v3 = merged["stance_v3"].dropna()
    v4 = merged["stance_v4"].dropna()
    common = merged.dropna(subset=["stance_v3", "stance_v4"])

    rho, p = stats.spearmanr(common["stance_v3"], common["stance_v4"])
    print(f"    Textes communs : {len(common):,}")
    print(f"    Spearman rho(stance_v3, stance_v4) = {rho:.3f} (p={p:.2e})")

    # Movers cachés : stance_v3=0 mais ceasefire_call=True
    movers = corpus_v4[
        (corpus_v4["stance_v3"].fillna(99) == 0) & (corpus_v4["ceasefire_call"] == True)
    ]
    print(f"    'Movers cachés' (stance_v3=0 & ceasefire_call=True) : {len(movers):,}")

    return {"spearman_rho": rho, "p_value": p, "n_common": len(common), "n_movers": len(movers)}


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("PREPARATION DES DONNEES - Gaza Discourse Analysis")
    print("=" * 60)

    # Créer les dossiers si besoin
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    DATA_PROC.mkdir(parents=True, exist_ok=True)

    # Vérifier les sources
    for src in [SOURCE_TWEETS, SOURCE_INTERV]:
        if not src.exists():
            print(f"ERREUR : Source introuvable : {src}")
            sys.exit(1)

    # --- Corpus v3 ---
    print("\n[1/4] Chargement des données brutes...")
    tw = load_tweets()
    iv = load_interventions()

    print("\n[2/4] Construction du corpus v3 (baseline)...")
    corpus_v3 = build_corpus_v3(tw, iv)
    out_v3 = DATA_PROC / "corpus_v3.parquet"
    corpus_v3.to_parquet(out_v3, index=False)
    print(f"  -> Sauvegardé : {out_v3} ({len(corpus_v3):,} lignes)")

    # --- Corpus v4 ---
    print("\n[3/4] Construction du corpus v4 (annotations LLM par période)...")
    corpus_v4 = build_corpus_v4()
    out_v4 = DATA_PROC / "corpus_v4.parquet"
    corpus_v4.to_parquet(out_v4, index=False)
    print(f"  -> Sauvegardé : {out_v4} ({len(corpus_v4):,} lignes)")

    # --- Comparaison v3/v4 ---
    print("\n[4/4] Validation croisée v3 / v4...")
    stats_out = compare_v3_v4(corpus_v3, corpus_v4)

    # --- Rapport de qualité ---
    print("\n" + "=" * 60)
    print("RAPPORT DE QUALITE DES DONNEES")
    print("=" * 60)
    print(f"corpus_v3.parquet  : {len(corpus_v3):,} textes | {corpus_v3['author'].nunique()} députés")
    print(f"corpus_v4.parquet  : {len(corpus_v4):,} textes | {corpus_v4['author'].nunique()} députés")
    print(f"Couverture v4/v3   : {100*len(corpus_v4)/len(corpus_v3):.1f}%")
    if stats_out:
        print(f"Accord v3/v4       : Spearman rho = {stats_out['spearman_rho']:.3f}")
    print("\nDONNEES PRETES.")


if __name__ == "__main__":
    main()
