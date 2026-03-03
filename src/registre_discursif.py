# -*- coding: utf-8 -*-
"""
Registre discursif : coopération vs conflit (marqueurs lexicaux).
Méthode inspirée des travaux sur l'intensité délibérative en parlements.
"""

import re

MARQUEURS_CONFLICTUELS = [
    r"\binacceptable\b", r"\bresponsable\b", r"\bhonte\b", r"\bscandale\b",
    r"\bdoit\s+(être|payer|répondre)\b", r"\bdevrait\s+(être|avoir)\b",
    r"\baccusation\b", r"\baccuser\b", r"\bcondamner\b", r"\bcondamnation\b",
    r"\bexiger\b", r"\bexige\b", r"\bcomptes?\s+à\s+rendre\b",
    r"\bmentir\b", r"\bmensonge\b", r"\bmanipulation\b",
    r"\bignorer\b", r"\brefuser\b", r"\bdénier\b",
]

MARQUEURS_COOPERATIFS = [
    r"\bproposons?\b", r"\bproposition\b", r"\bsuggérer\b", r"\bsouhaiter\b",
    r"\binformer\b", r"\binformation\b", r"\bclarifier\b",
    r"\bcollaborer\b", r"\bdialogue\b", r"\bdiscussion\b",
    r"\bdéclarer\b", r"\bannoncer\b", r"\bprésenter\b",
]


def score_registre_discursif(text):
    """
    Score 0 (coopératif) à 1 (conflictuel) selon les marqueurs présents.
    """
    if text is None or (isinstance(text, str) and not text.strip()):
        return float("nan")
    t = str(text).lower()
    n_conf = sum(1 for p in MARQUEURS_CONFLICTUELS if re.search(p, t, re.I))
    n_coop = sum(1 for p in MARQUEURS_COOPERATIFS if re.search(p, t, re.I))
    total = n_conf + n_coop
    if total == 0:
        return 0.5
    return n_conf / total
