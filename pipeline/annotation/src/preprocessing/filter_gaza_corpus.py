"""
Filtrage du corpus pour extraire les tweets/interventions sur Gaza/Palestine.

Applique le dictionnaire de mots-clés et génère le corpus filtré.
"""

import json
import re
import logging
from pathlib import Path
from typing import Set, List, Dict, Any
from collections import Counter

import pandas as pd
from unidecode import unidecode
from tqdm import tqdm

# Configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent


def normalize_text(text: str) -> str:
    """Normalise le texte pour la recherche."""
    if not text:
        return ""
    # Minuscules, suppression accents, normalisation espaces
    text = text.lower()
    text = unidecode(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


STAGE_DIRECTION_KEYWORDS = [
    "applaud", "applaudissements",
    "rires", "rire", "sourires",
    "murmures", "murmure",
    "exclamations", "exclamation",
    "protestations", "protestation",
    "brouhaha", "sifflets", "huee", "huees", "huée", "huées",
    "interruption", "interruptions",
    "silence",
    "s'exprime", "s'expriment", "s'exprimant",
    "s'assey", "se rassoit", "se rassoient",
]


def clean_intervention_text(text: str) -> str:
    """
    Nettoie les interventions AN en supprimant les indications scéniques
    (applaudissements, rires, interruptions, etc.) qui coupent le flux.
    """
    if not text:
        return ""

    # Supprimer les indications entre parenthèses contenant des mots-clés scéniques
    stage_pattern = re.compile(
        r"\(([^)]*(?:"
        + "|".join(re.escape(k) for k in STAGE_DIRECTION_KEYWORDS)
        + r")[^)]*)\)",
        flags=re.IGNORECASE,
    )
    cleaned = stage_pattern.sub(" ", text)

    # Supprimer les lignes/segments purement scéniques restants
    cleaned = re.sub(
        r"\b(?:applaudissements?|rires?|murmures?|exclamations?|protestations?|brouhaha|sifflets?|hu[ée]es?|silence)\b\.?",
        " ",
        cleaned,
        flags=re.IGNORECASE,
    )

    # Normaliser les espaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


class GazaFilter:
    """Filtre les textes pertinents sur Gaza/Palestine."""

    def __init__(self, keywords_path: Path):
        with open(keywords_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self._build_patterns()

    def _build_patterns(self):
        """Construit les patterns de recherche."""
        # Termes core (haute précision)
        self.core_terms = set(
            normalize_text(t)
            for t in self.config.get("core_terms", {}).get("terms", [])
        )

        # Tous les autres termes (contextuels)
        self.context_terms = set()
        for category in ["locations", "actors", "events", "concepts", "qualifiers"]:
            cat_data = self.config.get(category, {})
            if isinstance(cat_data, dict):
                for key, value in cat_data.items():
                    if isinstance(value, list):
                        self.context_terms.update(normalize_text(t) for t in value)
            elif isinstance(cat_data, list):
                self.context_terms.update(normalize_text(t) for t in cat_data)

        # Exclusions
        self.exclusions = set(
            normalize_text(t)
            for t in self.config.get("exclusions", {}).get("terms", [])
        )

        logger.info(
            f"Loaded {len(self.core_terms)} core terms, {len(self.context_terms)} context terms"
        )

    def _find_matches(self, text: str) -> Dict[str, List[str]]:
        """Trouve les correspondances dans le texte."""
        normalized = normalize_text(text)

        core_matches = [t for t in self.core_terms if t in normalized]
        context_matches = [t for t in self.context_terms if t in normalized]
        exclusion_matches = [t for t in self.exclusions if t in normalized]

        return {
            "core": core_matches,
            "context": context_matches,
            "exclusions": exclusion_matches,
        }

    def is_relevant(self, text: str) -> tuple[bool, Dict[str, Any]]:
        """
        Détermine si un texte est pertinent.

        Returns:
            (is_relevant, metadata)
        """
        matches = self._find_matches(text)

        # Règle 1: Au moins 1 terme core → pertinent
        if matches["core"]:
            return True, {
                "match_type": "core",
                "matches": matches["core"] + matches["context"],
                "confidence": "high",
            }

        # Règle 2: Au moins 2 termes contextuels (hors exclusions) → pertinent
        non_excluded_context = [
            t for t in matches["context"] if t not in matches["exclusions"]
        ]
        if len(non_excluded_context) >= 2:
            return True, {
                "match_type": "context",
                "matches": non_excluded_context,
                "confidence": "medium",
            }

        # Règle 3: Seulement des exclusions → non pertinent
        return False, {"match_type": "none", "matches": [], "confidence": "na"}

    def is_relevant_loose(self, text: str) -> tuple[bool, Dict[str, Any]]:
        """
        Version large: garder TOUT ce qui mentionne Gaza/Palestine
        avec au moins 1 terme (core ou contextuel), sans appliquer les exclusions.
        """
        matches = self._find_matches(text)
        all_matches = matches["core"] + matches["context"]

        if matches["core"]:
            return True, {
                "match_type": "core",
                "matches": all_matches,
                "confidence": "high",
            }

        if matches["context"]:
            return True, {
                "match_type": "context_any",
                "matches": all_matches,
                "confidence": "low",
            }

        return False, {"match_type": "none", "matches": [], "confidence": "na"}


def filter_tweets(
    input_file: Path, output_file: Path, keywords_file: Path
) -> pd.DataFrame:
    """Filtre les tweets."""
    logger.info(f"Loading tweets from {input_file}")
    df = pd.read_parquet(input_file)
    logger.info(f"Loaded {len(df):,} tweets")

    # Initialiser le filtre
    gaza_filter = GazaFilter(keywords_file)

    # Appliquer le filtre
    results = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Filtering"):
        text = row.get("text", "")
        is_relevant, metadata = gaza_filter.is_relevant(text)

        if is_relevant:
            results.append(
                {
                    **row.to_dict(),
                    "match_type": metadata["match_type"],
                    "keyword_matches": metadata["matches"],
                    "match_confidence": metadata["confidence"],
                }
            )

    filtered_df = pd.DataFrame(results)

    # Statistiques
    logger.info("\n" + "=" * 40)
    logger.info("RÉSULTATS DU FILTRAGE")
    logger.info("=" * 40)
    logger.info(f"Tweets initiaux: {len(df):,}")
    logger.info(f"Tweets filtrés: {len(filtered_df):,}")
    logger.info(f"Taux de pertinence: {len(filtered_df)/len(df)*100:.1f}%")

    if "match_type" in filtered_df.columns:
        logger.info(f"\nPar type de match:")
        for mt, count in filtered_df["match_type"].value_counts().items():
            logger.info(f"  {mt}: {count:,}")

    # Top mots-clés
    all_keywords = []
    for matches in filtered_df.get("keyword_matches", []):
        if isinstance(matches, list):
            all_keywords.extend(matches)

    logger.info(f"\nTop 15 mots-clés:")
    for kw, count in Counter(all_keywords).most_common(15):
        logger.info(f"  {kw}: {count:,}")

    # Sauvegarder
    output_file.parent.mkdir(parents=True, exist_ok=True)
    filtered_df.to_parquet(output_file, index=False)
    logger.info(f"\nSauvegardé: {output_file}")

    return filtered_df


def filter_interventions(
    input_file: Path,
    output_file: Path,
    keywords_file: Path,
    mode: str = "strict",
) -> pd.DataFrame:
    """Filtre les interventions AN."""
    logger.info(f"Loading interventions from {input_file}")

    # Charger JSONL
    interventions = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            interventions.append(json.loads(line))

    df = pd.DataFrame(interventions)
    logger.info(f"Loaded {len(df):,} interventions")

    gaza_filter = GazaFilter(keywords_file)

    results = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Filtering"):
        raw_text = row.get("raw_text", "") or row.get("text", "")
        cleaned_text = clean_intervention_text(raw_text)
        text_for_filter = cleaned_text or row.get("normalized_text", "")

        if mode == "loose":
            is_relevant, metadata = gaza_filter.is_relevant_loose(text_for_filter)
        else:
            is_relevant, metadata = gaza_filter.is_relevant(text_for_filter)

        if is_relevant:
            results.append(
                {
                    **row.to_dict(),
                    "cleaned_text": cleaned_text,
                    "match_type": metadata["match_type"],
                    "keyword_matches_new": metadata["matches"],
                    "match_confidence": metadata["confidence"],
                }
            )

    filtered_df = pd.DataFrame(results)

    logger.info(f"\nInterventions filtrées ({mode}): {len(filtered_df):,}/{len(df):,}")

    # Sauvegarder
    output_file.parent.mkdir(parents=True, exist_ok=True)
    filtered_df.to_parquet(output_file, index=False)
    logger.info(f"Sauvegardé: {output_file}")

    return filtered_df


def main():
    """Point d'entrée principal."""
    keywords_file = PROJECT_ROOT / "lexicons" / "filtering_keywords.json"

    # Filtrer tweets
    tweets_input = PROJECT_ROOT / "data" / "consolidated" / "tweets_all.parquet"
    tweets_output = PROJECT_ROOT / "data" / "filtered" / "tweets_gaza.parquet"

    if tweets_input.exists():
        filter_tweets(tweets_input, tweets_output, keywords_file)
    else:
        logger.warning(f"Fichier tweets non trouvé: {tweets_input}")
        logger.info("Exécutez d'abord consolidate_tweets.py")

    # Filtrer interventions
    # Version large: repartir du corpus general enrichi
    interv_input = (
        PROJECT_ROOT.parent
        / "collection"
        / "data"
        / "processed"
        / "interventions_enriched.jsonl"
    )
    interv_output_loose = (
        PROJECT_ROOT / "data" / "filtered" / "interventions_gaza_wide.parquet"
    )
    interv_output_strict = (
        PROJECT_ROOT / "data" / "filtered" / "interventions_gaza.parquet"
    )

    if interv_input.exists():
        filter_interventions(interv_input, interv_output_loose, keywords_file, mode="loose")
        # Garde aussi une version stricte en sortie pour compatibilité
        filter_interventions(interv_input, interv_output_strict, keywords_file, mode="strict")
    else:
        logger.warning(f"Fichier interventions non trouvé: {interv_input}")


if __name__ == "__main__":
    main()

