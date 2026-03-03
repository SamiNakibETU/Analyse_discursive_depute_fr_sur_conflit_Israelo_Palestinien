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

# Projet source optionnel (pour prepare_data) — variable d'environnement ou chemin par défaut
_SOURCE_ENV = os.environ.get("GAZA_SOURCE_PROJECT")
SOURCE_PROJECT = Path(_SOURCE_ENV) if _SOURCE_ENV else ROOT.parent / "fr_assemblee_discourse_analysis"
SOURCE_PROC = SOURCE_PROJECT / "data" / "processed"
SOURCE_RESULTS = SOURCE_PROJECT / "data" / "results"

# Blocs politiques et couleurs — granularité 4 blocs (analyses principales)
BLOC_COLORS = {
    "Gauche radicale": "#c0392b",
    "Gauche moderee": "#e67e22",
    "Centre / Majorite": "#2980b9",
    "Droite": "#2c3e50",
}
BLOC_ORDER = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"]

# Granularité fine — 5 blocs (LR et RN séparés pour les analyses de robustesse)
# Voir docs/AMELIORATIONS.md § B1
BLOC_COLORS_FINE = {
    "Gauche radicale": "#c0392b",
    "Gauche moderee": "#e67e22",
    "Centre / Majorite": "#2980b9",
    "LR": "#7f8c8d",
    "RN / extreme droite": "#1a1a2e",
}
BLOC_ORDER_FINE = [
    "Gauche radicale", "Gauche moderee", "Centre / Majorite", "LR", "RN / extreme droite"
]

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
