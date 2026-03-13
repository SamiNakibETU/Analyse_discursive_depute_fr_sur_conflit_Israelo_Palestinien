# -*- coding: utf-8 -*-
"""
Configuration centrale du projet.
"""

from pathlib import Path
import os

# Chemins
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"


def _env_path(var_name: str) -> Path | None:
    raw = os.environ.get(var_name, "").strip()
    return Path(raw).expanduser().resolve() if raw else None


def _resolve_workspace_root() -> Path:
    # Optional workspace anchor for portable sibling resolution.
    return _env_path("PROJECT_ROOT") or ROOT.parent


def _resolve_source_project() -> Path:
    # Explicit override wins.
    explicit = _env_path("GAZA_SOURCE_PROJECT")
    if explicit:
        return explicit

    # Portable sibling fallback from workspace root.
    candidate = _resolve_workspace_root() / "pipeline" / "annotation"
    if candidate.exists():
        return candidate

    # Fallback: legacy name for back-compat
    legacy = _resolve_workspace_root() / "projet_gaza"
    if legacy.exists():
        return legacy
    return ROOT.parent / "pipeline" / "annotation"

# Corpus
CORPUS_V3 = PROCESSED_DIR / "corpus_v3.parquet"
CORPUS_V4 = PROCESSED_DIR / "corpus_v4.parquet"

# Palette (obligatoire, identique partout)
COLORS = {
    "Gauche radicale": "#E63946",
    "Gauche moderee": "#F4A261",
    "Centre / Majorite": "#457B9D",
    "Droite": "#1D3557",
    "Extreme droite": "#2A0134",
}

BLOC_ORDER = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"]

# Événements clés
EVENTS = {
    "2023-10-07": "7 oct.",
    "2024-01-26": "CIJ",
    "2024-05-06": "Rafah",
    "2024-10-17": "Sinwar",
    "2024-11-21": "CPI",
    "2025-01-15": "CF",
    "2025-03-15": "Rupture",
}

BATCH_ORDER = [
    "CHOC",
    "POST_CIJ",
    "RAFAH",
    "POST_SINWAR",
    "MANDATS_CPI",
    "CEASEFIRE_BREACH",
    "NEW_OFFENSIVE",
]

# Compatibilité prepare_data
PROJECT_ROOT = ROOT
DATA_RAW = DATA_DIR / "raw"
DATA_PROC = PROCESSED_DIR
FIGURES = FIGURES_DIR  # Alias

# Source des données brutes (projet original)
# Optional granular overrides:
# - GAZA_SOURCE_DATA_DIR     (defaults to <GAZA_SOURCE_PROJECT>/data)
# - GAZA_SOURCE_OUTPUTS_DIR  (defaults to <GAZA_SOURCE_PROJECT>/outputs)
SOURCE_DIR = _resolve_source_project()
_SOURCE_DATA_DIR = _env_path("GAZA_SOURCE_DATA_DIR") or (SOURCE_DIR / "data")
SOURCE_V4_DIR = _env_path("GAZA_SOURCE_OUTPUTS_DIR") or (SOURCE_DIR / "outputs")
SOURCE_TWEETS = _SOURCE_DATA_DIR / "annotated" / "predictions" / "tweets_v3_full_clean.parquet"
SOURCE_INTERV = _SOURCE_DATA_DIR / "annotated" / "predictions" / "interventions_v3_full_clean.parquet"

# Classification politique - 4 blocs (Droite et ED regroupés, voir justification NB01 §1.A.3)
BLOCS = {
    "Gauche radicale": ["LFI-NFP", "LFI", "GDR"],
    "Gauche moderee": ["SOC", "PS-NFP", "ECO", "ECO-NFP"],
    "Centre / Majorite": ["REN", "MODEM", "HOR", "EPR", "DEM"],
    "Droite": ["LR", "RN", "UDR", "NI"],  # RN + UDR (Reconquête) = ED regroupés avec LR
}

# Alternative 5 blocs (pour analyses sensibles RN vs LR) - désactiver GROUP_TO_BLOC ci-dessous et utiliser BLOCS_5
# BLOCS_5 = {**BLOCS, "Extreme droite": ["RN"], "Droite": ["LR", "UDR", "NI"]}

GROUP_TO_BLOC = {g: b for b, gs in BLOCS.items() for g in gs}
BLOCS_ORDER = BLOC_ORDER

# Fenêtres des 7 batches v4
BATCHES = {
    "CHOC": {"start": "2023-10-07", "end": "2023-11-15", "label": "Choc initial"},
    "POST_CIJ": {"start": "2024-01-26", "end": "2024-02-15", "label": "Post-CIJ"},
    "RAFAH": {"start": "2024-05-01", "end": "2024-06-15", "label": "Offensive Rafah"},
    "POST_SINWAR": {"start": "2024-10-15", "end": "2024-10-31", "label": "Post-Sinwar"},
    "MANDATS_CPI": {"start": "2024-11-21", "end": "2024-12-31", "label": "Mandats CPI"},
    "CEASEFIRE_BREACH": {"start": "2025-01-01", "end": "2025-03-31", "label": "Cessez-le-feu & rupture"},
    "NEW_OFFENSIVE": {"start": "2025-04-01", "end": "2025-06-30", "label": "Nouvelle offensive"},
}

# Filtres qualité
MIN_CONFIDENCE = 0.70
CORPUS_START_DATE = "2023-10-07"
MIN_TEXTS_PER_DEPUTE = 5
