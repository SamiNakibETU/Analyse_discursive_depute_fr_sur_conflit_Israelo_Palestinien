"""
Fichier d'annotation V2 - ameliore avec:
- Textes complets (non tronques)
- Contexte tweets (RT, reply)
- Option HORS_SUJET
- URL originale
- Instructions claires
"""

import logging
from pathlib import Path

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Periodes
PERIODS = {
    "P0_pre_7oct": ("2023-01-01", "2023-10-06"),
    "P1_choc": ("2023-10-07", "2023-10-31"),
    "P2_offensive": ("2023-11-01", "2024-01-25"),
    "P3_post_cij": ("2024-01-26", "2024-05-05"),
    "P4_rafah": ("2024-05-06", "2024-09-30"),
    "P5_escalade": ("2024-10-01", "2024-11-20"),
    "P6_mandats_cpi": ("2024-11-21", "2025-01-14"),
    "P7_cessez_feu": ("2025-01-15", "2026-12-31"),
}


def assign_period(date) -> str:
    if pd.isna(date):
        return "unknown"
    date = pd.to_datetime(date)
    for period_name, (start, end) in PERIODS.items():
        if pd.to_datetime(start) <= date <= pd.to_datetime(end):
            return period_name
    return "unknown"


def stratified_sample(df, n_samples, stratify_cols, random_state=42):
    """Echantillonnage stratifie."""
    np.random.seed(random_state)
    df = df.copy()
    df["_strata"] = df[stratify_cols].astype(str).agg("_".join, axis=1)
    
    strata_counts = df["_strata"].value_counts()
    total = len(df)
    
    samples = []
    remaining = n_samples
    
    for strata, count in strata_counts.items():
        prop = count / total
        n_for_strata = max(1, int(prop * n_samples))
        n_for_strata = min(n_for_strata, count, remaining)
        
        strata_df = df[df["_strata"] == strata]
        sample = strata_df.sample(n=n_for_strata, random_state=random_state)
        samples.append(sample)
        remaining -= n_for_strata
        
        if remaining <= 0:
            break
    
    result = pd.concat(samples, ignore_index=True)
    return result.drop(columns=["_strata"])


def format_keywords(kw):
    """Formate les keywords pour affichage."""
    if kw is None:
        return ""
    if isinstance(kw, np.ndarray):
        return ", ".join(kw.tolist())
    if isinstance(kw, list):
        return ", ".join(kw)
    return str(kw)


def create_annotation_file():
    """Cree le fichier d'annotation V2."""
    output_dir = PROJECT_ROOT / "data" / "annotated" / "to_annotate"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # --- TWEETS ---
    tweets_file = PROJECT_ROOT / "data" / "filtered" / "tweets_gaza.parquet"
    logger.info(f"Loading tweets from {tweets_file}")
    tweets_df = pd.read_parquet(tweets_file)
    
    # Preparer
    tweets_df["date"] = pd.to_datetime(tweets_df["date_parsed"])
    tweets_df["period"] = tweets_df["date"].apply(assign_period)
    tweets_df["groupe_politique"] = tweets_df["groupe_politique"].fillna("inconnu")
    
    # Echantillonner (300 tweets)
    sample_tweets = stratified_sample(tweets_df, 300, ["period", "groupe_politique"])
    
    # Contexte tweet
    def get_tweet_context(row):
        ctx = []
        if row.get("is_retweet"):
            ctx.append("RT")
        if row.get("is_reply"):
            ctx.append("REPLY")
        return " ".join(ctx) if ctx else ""
    
    # Formater pour annotation - TEXTE COMPLET
    tweets_annot = pd.DataFrame({
        "ID": [f"T{i:04d}" for i in range(1, len(sample_tweets) + 1)],
        "SOURCE": "Twitter",
        "AUTEUR": sample_tweets["username"].values,
        "GROUPE": sample_tweets["groupe_politique"].values,
        "DATE": sample_tweets["date"].dt.strftime("%Y-%m-%d").values,
        "PERIODE": sample_tweets["period"].values,
        "CONTEXTE": sample_tweets.apply(get_tweet_context, axis=1).values,
        "URL": sample_tweets["url"].values,  # Lien original
        "TEXTE": sample_tweets["text"].values,  # TEXTE COMPLET
        "MOTS_CLES": sample_tweets["keyword_matches"].apply(format_keywords).values,
        "HORS_SUJET": "",  # 1 si hors sujet
        "STANCE": "",
        "INTENSITE": "",
        "CIBLE": "",
        "CADRAGE": "",
        "NOTES": ""
    })
    
    # --- INTERVENTIONS ---
    interv_file = PROJECT_ROOT / "data" / "filtered" / "interventions_gaza.parquet"
    logger.info(f"Loading interventions from {interv_file}")
    interv_df = pd.read_parquet(interv_file)
    
    # Preparer
    interv_df["date"] = pd.to_datetime(interv_df["sitting_date"])
    interv_df["period"] = interv_df["date"].apply(assign_period)
    interv_df["groupe_politique"] = interv_df["matched_group"].fillna("inconnu")
    interv_df["auteur"] = interv_df["speaker_name"].fillna("inconnu")
    
    # Echantillonner (150 interventions)
    sample_interv = stratified_sample(interv_df, 150, ["period", "groupe_politique"])
    
    # Formater - TEXTE COMPLET
    interv_annot = pd.DataFrame({
        "ID": [f"I{i:04d}" for i in range(1, len(sample_interv) + 1)],
        "SOURCE": "Assemblee",
        "AUTEUR": sample_interv["auteur"].values,
        "GROUPE": sample_interv["groupe_politique"].values,
        "DATE": sample_interv["date"].dt.strftime("%Y-%m-%d").values,
        "PERIODE": sample_interv["period"].values,
        "CONTEXTE": "",  # Pas de contexte particulier pour AN
        "URL": "",
        "TEXTE": sample_interv["normalized_text"].values,  # TEXTE COMPLET
        "MOTS_CLES": sample_interv["keyword_matches_new"].apply(format_keywords).values,
        "HORS_SUJET": "",
        "STANCE": "",
        "INTENSITE": "",
        "CIBLE": "",
        "CADRAGE": "",
        "NOTES": ""
    })
    
    # --- COMBINER ---
    combined = pd.concat([tweets_annot, interv_annot], ignore_index=True)
    combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)
    combined["ID"] = [f"{i:04d}" for i in range(1, len(combined) + 1)]
    
    # --- SAUVEGARDER ---
    
    # CSV avec point-virgule
    csv_file = output_dir / "annotation_v2.csv"
    combined.to_csv(csv_file, index=False, sep=";", encoding="utf-8-sig")
    logger.info(f"CSV saved: {csv_file}")
    
    # Excel
    excel_file = output_dir / "annotation_v2.xlsx"
    
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        # Feuille principale
        combined.to_excel(writer, sheet_name="A_ANNOTER", index=False)
        
        # Feuille instructions detaillees
        instructions = pd.DataFrame({
            "ETAPE": [
                "1. HORS_SUJET",
                "1. HORS_SUJET",
                "",
                "2. STANCE",
                "2. STANCE",
                "2. STANCE",
                "2. STANCE",
                "",
                "3. INTENSITE",
                "3. INTENSITE",
                "3. INTENSITE",
                "3. INTENSITE",
                "",
                "4. CIBLE",
                "4. CIBLE",
                "4. CIBLE",
                "4. CIBLE",
                "4. CIBLE",
                "4. CIBLE",
                "4. CIBLE",
                "",
                "5. CADRAGE",
                "5. CADRAGE",
                "5. CADRAGE",
                "5. CADRAGE",
                "5. CADRAGE",
                "5. CADRAGE",
                "5. CADRAGE",
            ],
            "VALEUR": [
                "1",
                "(vide)",
                "",
                "-1",
                "0",
                "1",
                "(vide)",
                "",
                "1",
                "2",
                "3",
                "(vide)",
                "",
                "Israel",
                "Palestine",
                "Hamas",
                "Civils",
                "France",
                "Autre",
                "(vide)",
                "",
                "HUM",
                "SEC",
                "LEG",
                "HIS",
                "DIP",
                "MOR",
                "(vide)",
            ],
            "DESCRIPTION": [
                "Texte HORS SUJET - ne parle pas de Gaza/Palestine/Israel",
                "Texte pertinent - a annoter",
                "",
                "Pro-Israel: soutien Israel, critique Hamas, droit a la defense",
                "Neutre: equilibre, appel a la paix, les deux cotes",
                "Pro-Palestine: critique Israel, soutien Gaza, denonciation",
                "Pas de positionnement clair (mais sujet pertinent)",
                "",
                "Modere: formulation diplomatique, nuancee",
                "Marque: position claire mais sans exces",
                "Fort: termes forts (genocide, terroristes, barbarie...)",
                "Non applicable",
                "",
                "Cible principale = Israel/gouvernement israelien",
                "Cible principale = Palestine/Palestiniens/Gaza",
                "Cible principale = Hamas",
                "Cible principale = civils (israeliens ou palestiniens)",
                "Cible principale = politique francaise",
                "Autre cible ou multiple",
                "Pas de cible specifique",
                "",
                "Humanitaire (famine, civils, aide, hopitaux...)",
                "Securitaire (terrorisme, defense, otages, menace...)",
                "Juridique (CIJ, CPI, droit international, genocide...)",
                "Historique (occupation, colonisation, Nakba...)",
                "Diplomatique (negociations, deux Etats, ONU...)",
                "Moral (barbarie, apartheid, resistance legitime...)",
                "Pas de cadrage dominant",
            ]
        })
        instructions.to_excel(writer, sheet_name="INSTRUCTIONS", index=False)
        
        # Feuille contexte colonnes
        contexte = pd.DataFrame({
            "COLONNE": ["CONTEXTE", "CONTEXTE", "URL", "MOTS_CLES"],
            "VALEUR": ["RT", "REPLY", "(lien)", "(liste)"],
            "EXPLICATION": [
                "Le tweet est un retweet - regarder le contenu retweete",
                "Le tweet est une reponse - peut manquer de contexte",
                "Cliquer pour voir le tweet original sur Twitter/X",
                "Mots du dictionnaire qui ont declenche la selection"
            ]
        })
        contexte.to_excel(writer, sheet_name="CONTEXTE", index=False)
        
        # Stats
        stats_data = {
            "Statistique": [
                "Total textes",
                "Tweets",
                "Interventions AN",
                "Tweets RT",
                "Tweets Reply",
                "Periodes couvertes",
                "Groupes politiques"
            ],
            "Valeur": [
                len(combined),
                len(tweets_annot),
                len(interv_annot),
                int(sample_tweets["is_retweet"].sum()) if "is_retweet" in sample_tweets else 0,
                int(sample_tweets["is_reply"].sum()) if "is_reply" in sample_tweets else 0,
                combined["PERIODE"].nunique(),
                combined["GROUPE"].nunique()
            ]
        }
        stats = pd.DataFrame(stats_data)
        stats.to_excel(writer, sheet_name="STATS", index=False)
    
    logger.info(f"Excel saved: {excel_file}")
    
    # --- RESUME ---
    print("\n" + "=" * 70)
    print("FICHIER D'ANNOTATION V2 CREE")
    print("=" * 70)
    print(f"\nFichier: {excel_file}")
    print(f"\nTotal: {len(combined)} textes")
    print(f"  - Tweets: {len(tweets_annot)}")
    print(f"  - Interventions: {len(interv_annot)}")
    
    print("\n" + "=" * 70)
    print("PROCEDURE D'ANNOTATION")
    print("=" * 70)
    print("""
1. Ouvrir annotation_v2.xlsx dans Excel

2. Pour CHAQUE ligne:

   a) Lire le TEXTE complet
      - Si tweet: verifier CONTEXTE (RT/REPLY) et cliquer URL si besoin
   
   b) HORS_SUJET = 1 si le texte ne parle PAS de Gaza/Palestine/Israel
      -> Si hors sujet, passer a la ligne suivante
   
   c) STANCE (si pertinent):
      -1 = Pro-Israel
       0 = Neutre/equilibre
       1 = Pro-Palestine
       (vide) = pas de positionnement clair
   
   d) INTENSITE (optionnel):
      1 = Modere | 2 = Marque | 3 = Fort
   
   e) CIBLE (optionnel): Israel, Palestine, Hamas, Civils, France, Autre
      -> Peut etre vide si pas de cible claire
   
   f) CADRAGE (optionnel): HUM, SEC, LEG, HIS, DIP, MOR
      -> Peut etre vide
   
   g) NOTES: commentaires libres (doutes, contexte manquant...)

3. Sauvegarder regulierement
""")


if __name__ == "__main__":
    create_annotation_file()
