# -*- coding: utf-8 -*-
"""
Registre discursif : coopération vs conflit (marqueurs lexicaux).
Méthode inspirée des travaux sur l'intensité délibérative en parlements.
AJOUT TÂCHE C2 : CONTEXTES_AMBIGU pour mots dépendant du contexte.
"""

import re

# Mots dépendant du contexte : conflictuel dans certains cas, coopératif dans d'autres.
# Format : (mot_regex, [(contexte_conflictuel, +1), (contexte_cooperatif, -1)])
CONTEXTES_AMBIGU = [
    # "responsable" : conflictuel si "responsable de la mort/de la mort de/des victimes",
    # coopératif si "responsable politique" ou "être responsable" (ordre = priorité)
    (
        r"\bresponsable\b",
        [
            (r"responsable\s+(de\s+la\s+mort|des\s+morts|de\s+la\s+mort\s+de|des\s+victimes|du\s+massacre)", 1),
            (r"politique\s+responsable|responsable\s+politique|être\s+responsable\b", -1),
        ],
    ),
]

MARQUEURS_CONFLICTUELS = [
    r"\binacceptable\b",  # "responsable" retiré -> géré par CONTEXTES_AMBIGU
    r"\bhonte\b", r"\bscandale\b",
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
    Les mots de CONTEXTES_AMBIGU sont comptés selon le contexte (AJOUT TÂCHE C2).
    """
    if text is None or (isinstance(text, str) and not text.strip()):
        return float("nan")
    t = str(text).lower()
    n_conf = 0
    n_coop = 0

    # Gestion des contextes ambigus : priorité au premier pattern qui matche
    for mot_regex, contextes in CONTEXTES_AMBIGU:
        if re.search(mot_regex, t, re.I):
            for ctx_regex, sens in contextes:
                if re.search(ctx_regex, t, re.I):
                    if sens > 0:
                        n_conf += 1
                    else:
                        n_coop += 1
                    break

    # Marqueurs directs (hors ambigus)
    n_conf += sum(1 for p in MARQUEURS_CONFLICTUELS if re.search(p, t, re.I))
    n_coop += sum(1 for p in MARQUEURS_COOPERATIFS if re.search(p, t, re.I))
    total = n_conf + n_coop
    if total == 0:
        return 0.5
    return n_conf / total
