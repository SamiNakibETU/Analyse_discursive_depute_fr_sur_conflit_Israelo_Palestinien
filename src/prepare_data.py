# -*- coding: utf-8 -*-
"""
Préparation des données. Copie les corpus (et optionnellement des CSV pré-générés)
depuis le projet source si disponible. Définir GAZA_SOURCE_PROJECT pour pointer
vers un autre chemin.
"""

import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    PROCESSED_DIR,
    RESULTS_DIR,
    CORPUS_V3,
    CORPUS_V4,
    SOURCE_PROC,
    SOURCE_RESULTS,
)

# CSV optionnels à copier si le projet source les produit (évite de régénérer)
RESULTS_TO_COPY = [
    "variables_batch_specifiques",
    "cosine_distance_mensuelle",
    "fighting_words",
    "stance_mensuel",
    "volume_mensuel",
    "event_impact_diff_in_diff",
    "panel_b4",
    "emotional_register_v4",
    "ceasefire_lexical",
    "convergence_batch_bloc",
    "attrition_mensuelle",
    "volume_par_groupe",
    "stance_panel_vs_complet",
    "mann_kendall_bloc",
    "polarisation_index",
    "entropic_polarization_temporal",
    "wasserstein_inter_blocs",
    "wasserstein_drift",
    "effective_dimensionality_temporal",
    "activity_bias_by_bloc",
    "visibility_paradox_quintiles",
    "stance_twitter_vs_an_by_deputy",
    "regression_delta_stance",
    "deliberative_intensity_by_bloc_month",
    "affective_vad_by_bloc_month",
    "affective_polarization_temporal",
    "moral_foundations_by_bloc_month",
    "frames_par_bloc",
    "anova_type2",
    "anova_interaction",
    "ceasefire_call_batch_bloc",
]


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Corpus
    if CORPUS_V3.exists() and CORPUS_V4.exists():
        print("Corpus déjà présents dans data/processed/")
    elif SOURCE_PROC.exists():
        for name in ["corpus_v3", "corpus_v4"]:
            for suffix in ["_clean", ""]:
                src = SOURCE_PROC / f"{name}{suffix}.parquet"
                dst = PROCESSED_DIR / f"{name}.parquet"
                if src.exists() and not dst.exists():
                    shutil.copy2(src, dst)
                    print(f"Copié : {src.name} -> {dst}")
    else:
        print(
            f"Corpus absents. Placer manuellement corpus_v3.parquet et corpus_v4.parquet "
            f"dans {PROCESSED_DIR}\n"
            f"Ou définir GAZA_SOURCE_PROJECT vers le projet source."
        )

    # CSV optionnels
    if SOURCE_RESULTS.exists():
        copied = 0
        for name in RESULTS_TO_COPY:
            src = SOURCE_RESULTS / f"{name}.csv"
            dst = RESULTS_DIR / f"{name}.csv"
            if src.exists():
                shutil.copy2(src, dst)
                copied += 1
        if copied:
            print(f"Copié {copied} CSV depuis le projet source.")
    else:
        print("Projet source absent — les CSV seront générés par run_analysis.py.")


if __name__ == "__main__":
    main()
