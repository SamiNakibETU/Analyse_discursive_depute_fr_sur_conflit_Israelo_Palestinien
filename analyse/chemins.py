from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DONNEES = RACINE / "data"
RES_LEX = DONNEES / "resultats" / "chaine_lexicale"
RES_VAR = DONNEES / "resultats" / "chaine_variables"
INTERVENTIONS_AN = DONNEES / "an_2022_2024" / "interventions.csv"
VALIDATION = DONNEES / "validation"

SORTIES = RACINE / "sorties"
TABLES = SORTIES / "tables"
FIGURES = SORTIES / "figures"
POLICES = SORTIES / ".polices"
