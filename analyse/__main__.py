"""Exécute l'analyse secondaire : python -m analyse"""
import warnings

import pandas as pd

from . import chargement as ch
from . import figures, mesures
from .chemins import SORTIES, TABLES


def formater(v):
    if isinstance(v, (bool,)) or not isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, int) or float(v).is_integer():
        return f"{int(v):,}".replace(",", " ")
    if abs(v) < 0.001:
        return f"{v:.1e}"
    return f"{v:.3f}".replace(".", ",")


def main():
    warnings.simplefilter("ignore", category=FutureWarning)
    r = mesures.Registre()
    for section in mesures.SECTIONS:
        section(r)

    TABLES.mkdir(parents=True, exist_ok=True)
    for nom, df in r.tables.items():
        df.to_csv(TABLES / f"{nom}.csv")

    lignes = ["# Chiffres clés", "", "Fichier généré par `python -m analyse`. Ne pas modifier à la main.", "",
              "Nature : `texte` = mesure sur le texte seul ; `extraction` = information factuelle extraite par le modèle ;",
              "`jugement` = appréciation du modèle, exposée au biais partisan du prompt (docs/methodologie.md, §4).", "",
              "| Clé | Valeur | Libellé | Nature | Source |", "|---|---:|---|---|---|"]
    for c in r.chiffres:
        lignes.append(f"| `{c['cle']}` | {formater(c['valeur'])} | {c['libelle']} | {c['nature']} | {c['source']} |")
    (SORTIES / "chiffres_cles.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")

    figures.style()
    tables = dict(r.tables, _position_mensuelle=ch.position_mensuelle())
    for f in figures.TOUTES:
        f(tables)
    print(f"{len(r.tables)} tables, {len(r.chiffres)} chiffres, {len(figures.TOUTES)} figures -> {SORTIES}")


if __name__ == "__main__":
    main()
