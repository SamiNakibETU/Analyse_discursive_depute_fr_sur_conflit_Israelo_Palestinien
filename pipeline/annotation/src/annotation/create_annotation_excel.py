"""
Cree un fichier Excel bien formate pour l'annotation manuelle.
Plus facile a utiliser qu'un CSV.
"""

import logging
from pathlib import Path
from datetime import datetime

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


def truncate_text(text, max_len=500):
    """Tronque le texte pour la lisibilite."""
    if pd.isna(text):
        return ""
    text = str(text)
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


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
    """Cree le fichier d'annotation."""
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
    
    # Echantillonner
    sample_tweets = stratified_sample(tweets_df, 300, ["period", "groupe_politique"])
    
    # Formater pour annotation
    tweets_annot = pd.DataFrame({
        "ID": [f"T{i:04d}" for i in range(1, len(sample_tweets) + 1)],
        "SOURCE": "Twitter",
        "AUTEUR": sample_tweets["username"].values,
        "GROUPE": sample_tweets["groupe_politique"].values,
        "DATE": sample_tweets["date"].dt.strftime("%Y-%m-%d").values,
        "PERIODE": sample_tweets["period"].values,
        "TEXTE": sample_tweets["text"].apply(truncate_text).values,
        "MOTS_CLES": sample_tweets["keyword_matches"].apply(format_keywords).values,
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
    
    # Echantillonner
    sample_interv = stratified_sample(interv_df, 150, ["period", "groupe_politique"])
    
    # Formater
    interv_annot = pd.DataFrame({
        "ID": [f"I{i:04d}" for i in range(1, len(sample_interv) + 1)],
        "SOURCE": "Assemblee",
        "AUTEUR": sample_interv["auteur"].values,
        "GROUPE": sample_interv["groupe_politique"].values,
        "DATE": sample_interv["date"].dt.strftime("%Y-%m-%d").values,
        "PERIODE": sample_interv["period"].values,
        "TEXTE": sample_interv["normalized_text"].apply(lambda x: truncate_text(x, 800)).values,
        "MOTS_CLES": sample_interv["keyword_matches_new"].apply(format_keywords).values,
        "STANCE": "",
        "INTENSITE": "",
        "CIBLE": "",
        "CADRAGE": "",
        "NOTES": ""
    })
    
    # --- COMBINER ---
    combined = pd.concat([tweets_annot, interv_annot], ignore_index=True)
    combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)  # Melanger
    combined["ID"] = [f"{i:04d}" for i in range(1, len(combined) + 1)]
    
    # --- SAUVEGARDER ---
    
    # CSV avec point-virgule (mieux pour Excel FR)
    csv_file = output_dir / "annotation_corpus.csv"
    combined.to_csv(csv_file, index=False, sep=";", encoding="utf-8-sig")
    logger.info(f"CSV saved: {csv_file}")
    
    # Excel (si openpyxl disponible)
    try:
        excel_file = output_dir / "annotation_corpus.xlsx"
        
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            # Feuille principale
            combined.to_excel(writer, sheet_name="A_ANNOTER", index=False)
            
            # Feuille instructions
            instructions = pd.DataFrame({
                "COLONNE": ["STANCE", "STANCE", "STANCE", "INTENSITE", "INTENSITE", "INTENSITE", 
                           "CIBLE", "CIBLE", "CIBLE", "CIBLE", "CIBLE", "CIBLE",
                           "CADRAGE", "CADRAGE", "CADRAGE", "CADRAGE", "CADRAGE", "CADRAGE"],
                "VALEUR": ["-1", "0", "1", "1", "2", "3",
                          "Israel", "Palestine", "Hamas", "Civils", "France", "Autre",
                          "HUM", "SEC", "LEG", "HIS", "DIP", "MOR"],
                "DESCRIPTION": [
                    "Pro-Israel: soutien Israel, critique Hamas",
                    "Neutre: equilibre, appel a la paix",
                    "Pro-Palestine: critique Israel, soutien Gaza",
                    "Modere: formulation diplomatique",
                    "Marque: position claire",
                    "Fort: termes forts (genocide, terroristes...)",
                    "Cible principale = Israel",
                    "Cible principale = Palestine/Gaza",
                    "Cible principale = Hamas",
                    "Cible principale = civils",
                    "Cible principale = politique francaise",
                    "Autre cible",
                    "Humanitaire (famine, civils, aide...)",
                    "Securitaire (terrorisme, defense, otages...)",
                    "Juridique (CIJ, CPI, droit international...)",
                    "Historique (occupation, colonisation...)",
                    "Diplomatique (negociations, deux Etats...)",
                    "Moral (genocide, barbarie, apartheid...)"
                ]
            })
            instructions.to_excel(writer, sheet_name="INSTRUCTIONS", index=False)
            
            # Feuille stats
            stats = pd.DataFrame({
                "Statistique": ["Total textes", "Tweets", "Interventions AN",
                               "Periodes couvertes", "Groupes politiques"],
                "Valeur": [len(combined), len(tweets_annot), len(interv_annot),
                          combined["PERIODE"].nunique(), combined["GROUPE"].nunique()]
            })
            stats.to_excel(writer, sheet_name="STATS", index=False)
        
        logger.info(f"Excel saved: {excel_file}")
        
    except ImportError:
        logger.warning("openpyxl not installed, Excel file not created")
        logger.info("Install with: pip install openpyxl")
    
    # --- RESUME ---
    print("\n" + "=" * 60)
    print("FICHIERS D'ANNOTATION CREES")
    print("=" * 60)
    print(f"\n1. CSV (separateur ;) : {csv_file}")
    print(f"2. Excel : {excel_file if 'excel_file' in dir() else 'Non cree'}")
    print(f"\nTotal: {len(combined)} textes a annoter")
    print(f"  - Tweets: {len(tweets_annot)}")
    print(f"  - Interventions: {len(interv_annot)}")
    
    print("\n" + "=" * 60)
    print("COMMENT ANNOTER")
    print("=" * 60)
    print("""
1. Ouvrir le fichier Excel (ou CSV avec Excel/LibreOffice)

2. Pour chaque ligne, remplir:

   STANCE (obligatoire):
     -1 = Pro-Israel
      0 = Neutre  
      1 = Pro-Palestine

   INTENSITE (optionnel):
     1 = Modere
     2 = Marque
     3 = Fort

   CIBLE (optionnel):
     Israel, Palestine, Hamas, Civils, France, Autre

   CADRAGE (optionnel):
     HUM = Humanitaire
     SEC = Securitaire
     LEG = Juridique
     HIS = Historique
     DIP = Diplomatique
     MOR = Moral

   NOTES: commentaires libres

3. Sauvegarder et renvoyer le fichier
""")


if __name__ == "__main__":
    create_annotation_file()
