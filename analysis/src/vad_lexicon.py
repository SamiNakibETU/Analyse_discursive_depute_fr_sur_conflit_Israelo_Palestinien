# -*- coding: utf-8 -*-
"""
Lexique Valence–Arousal–Dominance pour l’analyse affective.
Charge NRC-VAD (Mohammad, NRC Canada) si disponible.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VAD_PATH = ROOT / "data" / "lexicons" / "nrc-vad" / "NRC-VAD-Lexicon" / "OneFilePerLanguage" / "French-NRC-VAD-Lexicon.txt"

VAD_FALLBACK = {
    "colère": (0.2, 0.9, 0.7), "indignation": (0.2, 0.85, 0.65),
    "honte": (0.15, 0.7, 0.2), "mépris": (0.1, 0.6, 0.8),
    "souffrance": (0.15, 0.7, 0.2), "massacre": (0.05, 0.9, 0.4),
    "génocide": (0.02, 0.95, 0.5), "dignité": (0.75, 0.6, 0.6),
    "justice": (0.7, 0.6, 0.65), "paix": (0.9, 0.4, 0.5),
    "inacceptable": (0.15, 0.8, 0.65), "responsable": (0.3, 0.65, 0.7),
}


def load_vad_lexicon(path=None):
    """Charge NRC-VAD français. Format : mot_fr -> (valence, arousal, dominance)."""
    p = path or DEFAULT_VAD_PATH
    if Path(p).exists():
        lex = {}
        with open(p, encoding="utf-8") as f:
            next(f)  # header
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 5:
                    try:
                        v, a, d = float(parts[1]), float(parts[2]), float(parts[3])
                        fr = parts[4].strip().lower()
                        for token in re.findall(r"[a-zàâäéèêëïîôùûüç]+", fr):
                            if len(token) > 2:
                                lex[token] = (v, a, d)
                    except (ValueError, IndexError):
                        pass
        return lex if lex else VAD_FALLBACK
    return VAD_FALLBACK


def score_text_vad(text, lexicon=None):
    """Retourne (valence, arousal, dominance) moyens. Scores 0–1."""
    if lexicon is None:
        lexicon = load_vad_lexicon()
    words = re.findall(r"[a-zàâäéèêëïîôùûüç]+", str(text).lower())
    if not words:
        return (float("nan"), float("nan"), float("nan"))
    v_sum = a_sum = d_sum = n = 0
    for w in words:
        if w in lexicon:
            v, a, d = lexicon[w]
            v_sum += v
            a_sum += a
            d_sum += d
            n += 1
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    return (v_sum / n, a_sum / n, d_sum / n)
