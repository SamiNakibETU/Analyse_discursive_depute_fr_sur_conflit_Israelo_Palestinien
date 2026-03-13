# -*- coding: utf-8 -*-
"""
Moral Foundations Theory — lexique minimal français.
Voir eMFD (Hopp et al. 2021), Husson & Palma (2024) pour version complète.
"""

import re
from pathlib import Path

# AJOUT TÂCHE C1 — MFD étendu : 40+ mots par fondement
# Sources : Haidt (2012), eMFD Hopp et al. (2021), termes fréquents dans corpus frame MOR/HUM
MFD_FR_FALLBACK = {
    "care": [
        "soin", "soins", "protéger", "enfant", "enfants", "souffrance", "victime", "victimes",
        "bless", "blessé", "blessés", "secours", "humanitaire", "dignité", "compassion",
        "secourir", "innocent", "innocents", "civil", "civils", "population", "réfugié",
        "réfugiés", "famille", "familles", "orphelin", "orphelins", "humanité", "protéction",
        "aide", "aider", "santé", "mourir", "mort", "morts", "tué", "tués", "femme", "femmes",
        "vulnérable", "vulnérables", "désastre", "catastrophe", "urgence", "secourisme",
    ],
    "fairness": [
        "juste", "justice", "droit", "droits", "équité", "tricher", "injustice", "égalité",
        "illégal", "illégalité", "arbitraire", "procès", "tribunal", "condamner", "accusation",
        "crime", "criminelle", "violation", "violations", "convention", "résolution", "juger",
        "équitable", "discrimination", "discriminer", "préjudice", "réparation", "responsable",
        "responsabilité", "illégalité", "illégalement", "conforme", "conformité", "légal",
        "légalité", "légalement", "procédure", "audience", "verdict", "acquitt", "culpabilité",
    ],
    "loyalty": [
        "fidèle", "fidélité", "patrie", "trahir", "trahison", "nation", "national",
        "solidarité", "alliance", "allié", "alliés", "loyauté", "groupe", "communauté",
        "identité", "appartenance", "cohesion", "unité", "ralliement", "désertion",
        "traître", "traîtres", "collaboration", "résistance", "compatriote", "fraternité",
        "frère", "soeur", "tradition", "traditions", "coutume", "héritage", "mémoire",
        "commémoration", "ancêtre", "patrimoine", "nationalisme", "souveraineté",
        "cohesion", "rassembler", "rassemblement", "union", "fédérer", "coalition",
        "drapeau", "symbole", "collectif", "collective",
    ],
    "authority": [
        "obéir", "respecter", "ordre", "loi", "lois", "gouvernement", "état", "états",
        "institution", "institutions", "légitime", "rébellion", "défier", "hiérarchie",
        "commandement", "diriger", "dirigeant", "pouvoir", "autorité", "souverain",
        "leadership", "gouverner", "réglement", "règle", "règles", "décret", "décision",
        "officiel", "officielle", "responsable", "responsabilité", "compte", "rendre",
        "contrôle", "contrôler", "superviser", "déléguer", "mandat", "élu", "élection",
    ],
    "sanctity": [
        "pur", "pureté", "sacré", "sacre", "souiller", "souillé", "dégradation", "respect",
        "dignité", "saint", "sainte", "tabou", "profanation", "sacrilège", "déshonneur",
        "honneur", "honorable", "réputation", "débauche", "corruption", "corrompu",
        "intégrité", "vertu", "vertueux", "moral", "morale", "éthique", "condamnable",
        "condamnation", "indigne", "indignité", "honnêteté", "probité", "décence",
        "pudeur", "chasteté", "péché", "pécheur", "impur", "dégrader", "souillure",
        "honorablement", "déshonorant", "sacraliser", "respectabilité",
    ],
}


def load_mfd(path=None):
    """Charge le MFD. path: chemin vers eMFD si dispo."""
    if path and Path(path).exists():
        # Format eMFD: word, foundation, weight...
        mfd = {f: [] for f in MFD_FR_FALLBACK}
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    word = parts[0].lower()
                    fname = parts[1].lower()
                    if fname in mfd:
                        mfd[fname].append(word)
        return mfd if any(mfd[f] for f in mfd) else MFD_FR_FALLBACK
    return MFD_FR_FALLBACK


def score_text_mfd(text, mfd=None):
    """
    Retourne un dict {care, fairness, loyalty, authority, sanctity} avec la proportion
    de mots de chaque fondement dans le texte (0-1).
    """
    if mfd is None:
        mfd = load_mfd()
    words = set(re.findall(r"[a-zàâäéèêëïîôùûüç]+", str(text).lower()))
    if not words:
        return {f: float("nan") for f in mfd}
    scores = {}
    for fname, lex_words in mfd.items():
        n = sum(1 for w in words if any(lex_w in w or w in lex_w for lex_w in lex_words))
        scores[fname] = n / len(words) if len(words) > 0 else 0
    return scores


def compute_mfd_coverage(df, text_col="text", mfd=None):
    """
    Calcule le % de textes ayant au moins 1 hit par fondement (AJOUT TÂCHE C1).
    Retourne un dict {fondement: pct_couverture}.
    """
    if mfd is None:
        mfd = load_mfd()
    coverages = {}
    for fname, lex_words in mfd.items():
        n_hit = sum(
            1 for t in df[text_col].dropna()
            if _text_has_foundation(str(t), lex_words)
        )
        coverages[fname] = n_hit / len(df) * 100 if len(df) > 0 else 0
    return coverages


def _text_has_foundation(text, lex_words):
    """Vérifie si le texte contient au moins un mot du fondement."""
    words = set(re.findall(r"[a-zàâäéèêëïîôùûüç]+", str(text).lower()))
    return any(lex_w in w or w in lex_w for w in words for lex_w in lex_words)
