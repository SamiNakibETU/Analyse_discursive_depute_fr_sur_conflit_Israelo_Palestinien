#!/usr/bin/env python3
"""
Génère stance_par_groupe.csv et stance_panel_vs_complet.csv depuis le corpus v3.

Usage : python src/export_stance_par_groupe.py

Nécessite : data/processed/corpus_v3.parquet (généré par prepare_data.py)
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "data" / "results"
CORPUS = PROCESSED / "corpus_v3.parquet"

BLOCS_ORDER = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"]


def main():
    if not CORPUS.exists():
        print(f"Corpus non trouvé : {CORPUS}")
        print("Exécuter d'abord : python src/prepare_data.py")
        return

    v3 = pd.read_parquet(CORPUS)
    v3["date"] = pd.to_datetime(v3["date"], errors="coerce")
    v3["month"] = v3["date"].dt.to_period("M")

    # Colonne group ou groupe_politique
    grp_col = "group" if "group" in v3.columns else "groupe_politique"
    if grp_col not in v3.columns:
        print("Colonne group/groupe_politique absente du corpus.")
        return

    # 1. Stance par groupe
    stance_grp = (
        v3.groupby(grp_col)
        .agg(
            n_textes=("stance_v3", "count"),
            stance_mean=("stance_v3", "mean"),
            stance_std=("stance_v3", "std"),
            n_deputes=("author", "nunique"),
        )
        .reset_index()
    )
    stance_grp = stance_grp.rename(columns={grp_col: "groupe_politique"})
    stance_grp["pct_corpus"] = (stance_grp["n_textes"] / stance_grp["n_textes"].sum() * 100).round(1)
    bloc_map = v3.groupby(grp_col)["bloc"].first().to_dict()
    stance_grp["bloc"] = stance_grp["groupe_politique"].map(bloc_map)
    stance_grp = stance_grp[["groupe_politique", "bloc", "n_textes", "pct_corpus", "stance_mean", "stance_std", "n_deputes"]]
    stance_grp.to_csv(RESULTS / "stance_par_groupe.csv", index=False)
    print(f"Exporté : {RESULTS / 'stance_par_groupe.csv'}")

    # 2. Panel B4 vs complet
    months_per_dep = v3.groupby("author")["month"].nunique().reset_index()
    months_per_dep.columns = ["author", "n_months"]
    panel_list = months_per_dep[months_per_dep["n_months"] >= 18]["author"].tolist()
    v3["in_panel"] = v3["author"].isin(panel_list)

    stance_full = v3.groupby("bloc")["stance_v3"].agg(["mean", "count"]).rename(columns={"mean": "stance_complet", "count": "n_complet"})
    stance_b4 = v3[v3["in_panel"]].groupby("bloc")["stance_v3"].agg(["mean", "count"]).rename(columns={"mean": "stance_panel_b4", "count": "n_panel"})
    comp = stance_full.join(stance_b4).reset_index()
    comp["delta"] = comp["stance_panel_b4"] - comp["stance_complet"]
    comp = comp.set_index("bloc").reindex(BLOCS_ORDER).reset_index()
    comp[["bloc", "stance_complet", "stance_panel_b4", "delta", "n_complet", "n_panel"]].to_csv(
        RESULTS / "stance_panel_vs_complet.csv", index=False
    )
    print(f"Exporté : {RESULTS / 'stance_panel_vs_complet.csv'}")


if __name__ == "__main__":
    main()
