# -*- coding: utf-8 -*-
"""
Moral Foundations Theory — lexique minimal français.
Voir eMFD (Hopp et al. 2021), Husson & Palma (2024) pour version complète.
"""

import re
from pathlib import Path

# MFD minimal FR : fondement -> liste de mots (stem)
MFD_FR_FALLBACK = {
    "care": ["soin", "protéger", "enfant", "souffrance", "victime", "bless", "secours",
             "humanitaire", "dignité", "compassion", "secourir", "innocent"],
    "fairness": ["juste", "droit", "équité", "tricher", "injustice", "égalité",
                "illégal", "illégalité", "arbitraire"],
    "loyalty": ["fidèle", "patrie", "trahir", "trahison", "nation", "solidarité",
                "alliance", "allié", "loyauté"],
    "authority": ["obéir", "respecter", "ordre", "loi", "gouvernement", "état",
                  "institution", "légitime", "rébellion", "défier"],
    "sanctity": ["pur", "sacré", "souiller", "dégradation", "respect", "dignité"],
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
