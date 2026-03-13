# -*- coding: utf-8 -*-
"""
Configuration centrale. Toutes les constantes, chemins et paramètres sont ici.
"""

from pathlib import Path
import os

# Chemins
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
FIGURES_DIR = ROOT / "figures"
PROJECT_ROOT = ROOT

CORPUS_V3 = PROCESSED_DIR / "corpus_v3.parquet"
CORPUS_V4 = PROCESSED_DIR / "corpus_v4.parquet"

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
    candidate = _resolve_workspace_root() / "publication"
    if candidate.exists():
        return candidate

    # Fallback: legacy name for back-compat
    legacy = _resolve_workspace_root() / "fr_assemblee_discourse_analysis"
    if legacy.exists():
        return legacy
    return ROOT.parent / "publication"


# Projet source optionnel (pour prepare_data)
# Optional granular overrides:
# - GAZA_SOURCE_PROCESSED_DIR (defaults to <GAZA_SOURCE_PROJECT>/data/processed)
# - GAZA_SOURCE_RESULTS_DIR   (defaults to <GAZA_SOURCE_PROJECT>/data/results)
SOURCE_PROJECT = _resolve_source_project()
SOURCE_PROC = _env_path("GAZA_SOURCE_PROCESSED_DIR") or (SOURCE_PROJECT / "data" / "processed")
SOURCE_RESULTS = _env_path("GAZA_SOURCE_RESULTS_DIR") or (SOURCE_PROJECT / "data" / "results")

# Blocs politiques et couleurs (4 blocs — rétro-compatibilité : ne pas modifier)
BLOC_COLORS = {
    "Gauche radicale": "#c0392b",
    "Gauche moderee": "#e67e22",
    "Centre / Majorite": "#2980b9",
    "Droite": "#2c3e50",
}
BLOC_ORDER = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"]

# AJOUT TÂCHE A2 — Séparation LR / RN
GROUP_TO_BLOC_5 = {
    "LR": "Droite LR",
    "RN": "Droite RN",
    "UDR": "Droite RN",
    "NI": None,
}
BLOC_ORDER_5 = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite LR", "Droite RN"]
BLOC_COLORS_5 = {
    "Gauche radicale": "#c0392b",
    "Gauche moderee": "#e67e22",
    "Centre / Majorite": "#2980b9",
    "Droite LR": "#3498db",
    "Droite RN": "#2c3e50",
}


def add_bloc_5(df, group_col="group", bloc_col="bloc"):
    """Ajoute la colonne bloc_5 (LR vs RN séparés). NI exclu. Les autres blocs conservent leur nom."""
    out = df.copy()
    droit_groups = out[out[bloc_col] == "Droite"][group_col].map(GROUP_TO_BLOC_5)
    out["bloc_5"] = out[bloc_col]
    out.loc[droit_groups.index, "bloc_5"] = droit_groups
    out = out[out["bloc_5"].notna()]
    return out


# Dates d'annonce pour les lignes verticales sur les figures
EVENTS = {
    "2023-10-07": "7 oct.",
    "2024-01-26": "CIJ",
    "2024-05-07": "Rafah",
    "2024-10-17": "Sinwar",
    "2024-11-21": "Mandats CPI",
    "2025-01-15": "Cessez-le-feu",
    "2025-03-18": "Reprise offensive",
}

# Fenêtres temporelles (batches) — utilisées pour les analyses par période
# Définition alignée avec le traitement des notebooks
BATCHES = {
    "CHOC": {"start": "2023-10-07", "end": "2023-12-31"},
    "POST_CIJ": {"start": "2024-01-26", "end": "2024-04-30"},
    "RAFAH": {"start": "2024-05-07", "end": "2024-10-15"},
    "POST_SINWAR": {"start": "2024-10-16", "end": "2024-11-20"},
    "MANDATS_CPI": {"start": "2024-11-21", "end": "2025-01-14"},
    "CEASEFIRE_BREACH": {"start": "2025-01-15", "end": "2025-03-17"},
    "NEW_OFFENSIVE": {"start": "2025-03-18", "end": "2026-01-31"},
}
BATCH_ORDER = list(BATCHES.keys())

# Dates utilisées pour les event studies (shift avant/après)
EVENT_STUDY_DATES = {
    "Ordonnance CIJ": "2024-01-26",
    "Offensive Rafah": "2024-05-28",
    "Mort Sinwar": "2024-10-16",
    "Mandats CPI": "2024-11-21",
    "Cessez-le-feu": "2025-01-19",
    "Rupture CLF": "2025-03-15",
}


def month_to_batch(m):
    """Associe un mois (YYYY-MM) à un batch temporel."""
    import pandas as pd
    if pd.isna(m) or m is None:
        return "OTHER"
    d = pd.Timestamp(str(m) + "-15")
    for name, r in BATCHES.items():
        if pd.Timestamp(r["start"]) <= d <= pd.Timestamp(r["end"]):
            return name
    return "OTHER"


def add_events(ax, events=None, ymax_frac=0.97, fontsize=6.5):
    """Trace les lignes verticales pour les événements pivot et ajoute les labels."""
    import pandas as pd
    if events is None:
        events = EVENTS
    ylim = ax.get_ylim()
    for date_str, label in events.items():
        d = pd.Timestamp(date_str)
        ax.axvline(d, color="grey", alpha=0.4, ls="--", lw=0.8)
        ax.text(
            d,
            ylim[1] * ymax_frac,
            f" {label}",
            fontsize=fontsize,
            ha="center",
            va="top",
            color="#777",
            rotation=45,
        )


def format_dates(ax, interval=3):
    """Configure le formatage des dates sur l'axe x."""
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
