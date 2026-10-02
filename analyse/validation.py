"""Validation humaine de l'annotation automatique.

    python -m analyse.validation grille   # crée data/validation/grille_annotation.csv (à remplir)
    python -m analyse.validation scores   # compare la grille remplie aux étiquettes du modèle

La grille ne montre ni l'auteur ni le bloc : l'annotateur juge le texte seul.
Les étiquettes du modèle (annotation v3) sont dans etiquettes_llm_v3.csv et ne doivent pas être consultées avant.
"""
import sys

import numpy as np
import pandas as pd
from scipy import stats

from .chargement import echantillon_validation
from .chemins import TABLES, VALIDATION
from .stats import kappa_pondere

GRILLE = VALIDATION / "grille_annotation.csv"


def creer_grille(graine: int = 7):
    e = echantillon_validation()
    g = e[["id", "date", "arena", "text"]].rename(columns={"arena": "arene", "text": "texte"})
    g = g.sample(frac=1, random_state=graine).reset_index(drop=True)
    g["position_humaine"] = ""
    g["certitude"] = ""
    g["commentaire"] = ""
    g.to_csv(GRILLE, index=False, encoding="utf-8-sig")
    print(f"{len(g)} textes -> {GRILLE}")


def scores():
    g = pd.read_csv(GRILLE, encoding="utf-8-sig")
    g = g[pd.to_numeric(g["position_humaine"], errors="coerce").notna()]
    if g.empty:
        sys.exit("La colonne position_humaine est vide : remplir la grille d'abord (valeurs -2 à 2).")
    e = echantillon_validation().merge(g[["id", "position_humaine"]], on="id")
    h, m = e["position_humaine"].astype(int), e["position_llm"].astype(int)
    k = kappa_pondere(h, m)
    rho, p = stats.spearmanr(h, m)
    res = pd.Series({
        "textes": len(e), "kappa": k["kappa"], "kappa_quadratique": k["kappa_quadratique"],
        "spearman": rho, "spearman_p": p, "accord_exact": (h == m).mean(), "accord_a_1_point": ((h - m).abs() <= 1).mean(),
    })
    biais = e.assign(ecart=m - h).groupby("bloc")["ecart"].agg(["mean", "count"])
    confusion = pd.crosstab(h.rename("humain"), m.rename("modele"))
    TABLES.mkdir(parents=True, exist_ok=True)
    res.to_csv(TABLES / "validation_scores.csv", header=["valeur"])
    biais.to_csv(TABLES / "validation_biais_par_bloc.csv")
    confusion.to_csv(TABLES / "validation_confusion.csv")
    print(res.round(3).to_string(), "\n\nÉcart moyen modèle − humain par bloc :\n", biais.round(2).to_string(), "\n\n", confusion)


if __name__ == "__main__":
    {"grille": creer_grille, "scores": scores}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
