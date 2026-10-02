"""Constantes partagées : blocs, fenêtres d'annotation v4, événements, familles de cibles."""
import pandas as pd

BLOCS = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"]
LIBELLES = {
    "Gauche radicale": "Gauche radicale",
    "Gauche moderee": "Gauche modérée",
    "Centre / Majorite": "Centre / Majorité",
    "Droite": "Droite",
}

# Bornes utilisées au moment de l'annotation v4 (annotation/v4/annotation_v4.py).
# Toutes les tables « par fenêtre » de la chaîne variables reposent sur elles.
FENETRES = {
    "CHOC": ("2023-10-07", "2023-11-15"),
    "POST_CIJ": ("2024-01-26", "2024-02-15"),
    "RAFAH": ("2024-05-01", "2024-06-15"),
    "POST_SINWAR": ("2024-10-15", "2024-10-31"),
    "MANDATS_CPI": ("2024-11-21", "2024-12-31"),
    "CEASEFIRE_BREACH": ("2025-01-01", "2025-03-31"),
    "NEW_OFFENSIVE": ("2025-04-01", "2025-06-30"),
}
ORDRE_FENETRES = list(FENETRES)
LIBELLES_FENETRES = {
    "CHOC": "7 oct. – 15 nov. 2023",
    "POST_CIJ": "Ordonnance CIJ",
    "RAFAH": "Rafah, européennes",
    "POST_SINWAR": "Mort de Sinwar",
    "MANDATS_CPI": "Mandats CPI",
    "CEASEFIRE_BREACH": "Cessez-le-feu et rupture",
    "NEW_OFFENSIVE": "Nouvelle offensive",
}

EVENEMENTS = {
    "2023-05-04": "Résolution « apartheid » (AN)",
    "2023-10-07": "7 octobre",
    "2024-01-26": "Ordonnance CIJ",
    "2024-06-09": "Européennes, dissolution",
    "2024-11-21": "Mandats CPI",
    "2025-01-19": "Cessez-le-feu",
    "2025-03-18": "Reprise de l'offensive",
    "2025-09-22": "Reconnaissance de la Palestine",
}

# Regroupement des cibles principales (libellés libres produits par l'annotation v4).
# L'ordre compte : la première famille dont le motif correspond l'emporte.
FAMILLES_CIBLES = [
    ("populations", r"PALESTIN|PEUPLE_|GAZA|CIVIL|OTAGE|HOSTAGE|VICTIM|ENFANT|CHILDREN"),
    ("hamas_axe", r"HAMAS|HEZBOLLAH|IRAN|HOUTHI|SINWAR|JIHAD|ISLAMIS|TERROR"),
    ("israel", r"ISRA|NETANYA|TSAHAL|^IDF$|SMOTRICH|BEN_GVIR|GALLANT"),
    ("adversaires_fr", r"^LFI$|INSOUMIS|M[EÉ]LEN?CHON|EXTR[EÊ]ME_|^GAUCHE$|^DROITE$|^RN$|RASSEMBLEMENT|LE_PEN|BARDELLA"
                       r"|^PS$|PARTI_SOCIALISTE|NUPES|NFP|EELV|ECOLO|GLUCKSMANN|RIMA_HAS|BOYARD|DELOGU|OBONO|CARON"
                       r"|MACRONIE|MACRONISTE|OPPOSITION|OPPOSANT|AURORE_BERG|MEYER_HABIB"),
    ("executif_fr", r"MACRON|FRANCE_GOV|FRENCH_GOV|GOUVERNEMENT|GOVERNMENT|BARROT|RETAILLEAU|ATTAL|BAYROU|BORNE|BARNIER"
                    r"|LECORNU|S[EÉ]JOURN[EÉ]|COLONNA|DARMANIN|^FRANCE$"),
]


def famille_cible(libelle: str) -> str:
    import re
    lib = str(libelle).upper().strip()
    for nom, motif in FAMILLES_CIBLES:
        if re.search(motif, lib):
            return nom
    return "autre"


def fenetre_de_date(date) -> str | None:
    d = pd.Timestamp(date)
    for nom, (debut, fin) in FENETRES.items():
        if pd.Timestamp(debut) <= d <= pd.Timestamp(fin):
            return nom
    return None
