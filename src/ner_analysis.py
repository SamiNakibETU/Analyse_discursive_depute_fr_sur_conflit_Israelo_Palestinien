# -*- coding: utf-8 -*-
"""
AJOUT TÂCHE B1 — Module NER : analyse des cibles discursives.

Extraction d'entités nommées (PER, ORG, GPE, LOC) et score d'humanisation
lexical (termes humanisants vs institutionnels-militaires).
"""

import json
import re
from typing import Optional

import pandas as pd

# Lexiques pour compute_humanization_score
LEXIQUE_HUMANISANT = [
    "civil", "civils", "civile", "enfant", "enfants", "famille", "familles",
    "victime", "victimes", "population", "populations", "humanitaire",
    "blessé", "tué", "mort", "femme", "femmes", "réfugié", "réfugiés",
]
LEXIQUE_INSTITUTIONNEL_MILITAIRE = [
    "Hamas", "terroriste", "terroristes", "opération", "militaire",
    "frappe", "roquette", "bombe", "armée", "IDF", "Tsahal",
    "otage", "otages",
]

# Entités pour fallback regex si spacy non disponible
FALLBACK_ENTITIES = ["Netanyahu", "Hamas", "Israël", "Palestine", "Gaza", "civils"]


def run_ner(
    df: pd.DataFrame,
    text_col: str = "text",
    model: str = "fr_core_news_lg",
) -> pd.DataFrame:
    """
    Ajoute les colonnes entities_PER, entities_ORG, entities_GPE, entities_LOC
    (listes sérialisées en string JSON).

    Si spacy ou le modèle n'est pas disponible, utilise un fallback regex.
    """
    out = df.copy()
    entity_types = ["PER", "ORG", "GPE", "LOC"]
    nlp = None
    try:
        import spacy
        nlp = spacy.load(model)
    except Exception:
        nlp = None

    for et in entity_types:
        out[f"entities_{et}"] = "[]"

    def extract_entities(row):
        text = row.get(text_col, "")
        if pd.isna(text) or not isinstance(text, str):
            return {f"entities_{et}": "[]" for et in entity_types}
        text = str(text).strip()
        if not text:
            return {f"entities_{et}": "[]" for et in entity_types}
        if nlp is not None:
            doc = nlp(text[:1000000])
            ents_by_type = {et: [] for et in entity_types}
            for ent in doc.ents:
                if ent.label_ in entity_types:
                    ents_by_type[ent.label_].append(ent.text)
            return {f"entities_{et}": json.dumps(ents_by_type[et]) for et in entity_types}
        else:
            found = []
            for pattern in FALLBACK_ENTITIES:
                if re.search(rf"\b{re.escape(pattern)}\b", text, re.I):
                    found.append(pattern)
            if found:
                per_org = [p for p in found if p in ["Netanyahu"]]
                gpe_loc = [p for p in found if p in ["Israël", "Palestine", "Gaza"]]
                return {
                    "entities_PER": json.dumps(per_org) if per_org else "[]",
                    "entities_ORG": json.dumps([p for p in found if p == "Hamas"]) if "Hamas" in found else "[]",
                    "entities_GPE": json.dumps(gpe_loc) if gpe_loc else "[]",
                    "entities_LOC": json.dumps([p for p in found if p in ["Gaza"]]) if "Gaza" in found else "[]",
                }
            return {f"entities_{et}": "[]" for et in entity_types}

    results = df.apply(extract_entities, axis=1)
    for et in entity_types:
        out[f"entities_{et}"] = [r.get(f"entities_{et}", "[]") for r in results]
    return out


def extract_entity_counts(
    df: pd.DataFrame,
    entity_type: str,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    Extrait les fréquences des entités pour un type donné.
    entity_type : PER, ORG, GPE ou LOC.
    """
    col = f"entities_{entity_type}"
    if col not in df.columns:
        return pd.DataFrame(columns=["entity", "count"])
    from collections import Counter
    cnt = Counter()
    for val in df[col].dropna():
        try:
            lst = json.loads(val) if isinstance(val, str) else val
            if isinstance(lst, list):
                cnt.update(lst)
            elif isinstance(lst, str):
                cnt[lst] += 1
        except (json.JSONDecodeError, TypeError):
            pass
    if not cnt:
        return pd.DataFrame(columns=["entity", "count"])
    top = cnt.most_common(top_n)
    return pd.DataFrame(top, columns=["entity", "count"])


def compute_humanization_score(df: pd.DataFrame, text_col: str = "text") -> pd.Series:
    """
    Ratio (termes humanisants) / (termes humanisants + termes militaro-institutionnels).
    Valeur entre 0 et 1. Proche de 1 = discours plus humanisant.
    """
    def score_one(text):
        if pd.isna(text) or not isinstance(text, str):
            return float("nan")
        t = str(text).lower()
        hum = sum(1 for w in LEXIQUE_HUMANISANT if re.search(rf"\b{re.escape(w)}\b", t))
        inst = sum(1 for w in LEXIQUE_INSTITUTIONNEL_MILITAIRE if re.search(rf"\b{re.escape(w)}\b", t))
        total = hum + inst
        if total == 0:
            return float("nan")
        return hum / total
    return df[text_col].apply(score_one)
