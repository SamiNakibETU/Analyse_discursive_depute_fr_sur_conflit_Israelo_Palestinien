"""Lecture des tables de résultats et des interventions, avec les corrections documentées dans docs/donnees.md."""
import re
import unicodedata

import pandas as pd

from .chemins import INTERVENTIONS_AN, RES_LEX, RES_VAR, VALIDATION
from .referentiel import BLOCS, ORDRE_FENETRES, famille_cible

MOIS = {"janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
        "août": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12}

# Mention explicite du conflit (bornes de mots : « Bahamas » ne doit pas compter pour « Hamas »).
MOTIF_CONFLIT = r"\bgaza\b|\bisra[eë]l|\bpalestin|\bhamas\b|cisjordanie"


def cle_personne(nom: str) -> str:
    """Clé d'identité : sans civilité, sans fonction ministérielle, sans accents, en minuscules.

    Les noms issus des comptes rendus portent « M. » ou « Mme » ; ceux issus de X n'en portent pas.
    Sans cette normalisation, une même personne compte pour deux auteurs.
    """
    s = re.sub(r"^(M\.|Mme|Mlle)\s+", "", str(nom)).split(",")[0].strip()
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def lire(nom: str, chaine: str = "variables") -> pd.DataFrame:
    dossier = RES_VAR if chaine == "variables" else RES_LEX
    return pd.read_csv(dossier / nom, encoding="utf-8-sig")


def position_mensuelle() -> pd.DataFrame:
    return lire("stance_mensuel.csv")


def volume_mensuel() -> pd.DataFrame:
    return lire("volume_mensuel.csv").pivot(index="month", columns="bloc", values="n_textes").fillna(0)[BLOCS]


def personnes() -> pd.DataFrame:
    """Une ligne par personne réelle (fusion des doublons « M. X » / « X »)."""
    t = lire("trajectoires_individuelles.csv")
    t["cle"] = t["author"].map(cle_personne)
    agg = t.groupby("cle").agg(
        nom=("author", lambda s: min(s, key=len)),
        bloc=("bloc", lambda s: s.mode().iloc[0]),
        n_textes=("n_textes", "sum"),
        n_variantes=("author", "size"),
    )
    return agg.sort_values("n_textes", ascending=False)


def auteurs_bruts() -> pd.DataFrame:
    return lire("trajectoires_individuelles.csv")


def cibles_par_fenetre() -> pd.DataFrame:
    t = lire("target_primary_par_batch_bloc.csv")
    t["famille"] = t["target_primary"].map(famille_cible)
    return t


def cibles_par_bloc() -> pd.DataFrame:
    t = lire("target_primary_par_bloc.csv")
    t["famille"] = t["target_primary"].map(famille_cible)
    return t


def cessez_le_feu_par_fenetre() -> pd.DataFrame:
    return lire("ceasefire_call_batch_bloc.csv")


def emotions_par_fenetre() -> pd.DataFrame:
    return lire("emotional_register_v4.csv")


def demandes_par_fenetre() -> pd.DataFrame:
    d = lire("key_demands_par_batch_bloc.csv")
    # Les listes vides ou sérialisées (« [] », « ['ceasefire'] ») sont ramenées à une étiquette simple.
    d["demande"] = d["demand"].astype(str).str.strip("[]'\" ").replace({"": "none", "nan": "none"})
    return d


def cadres_v3() -> pd.DataFrame:
    f = lire("frames_par_bloc.csv")
    return f[f["version"] == "v3"]


def registres() -> pd.DataFrame:
    return lire("emotional_register.csv")


def conditionnalite() -> pd.DataFrame:
    return lire("conditionality.csv")


def variables_fenetres() -> pd.DataFrame:
    return lire("variables_batch_specifiques.csv")


def anova() -> pd.DataFrame:
    return lire("anova_type2.csv", "lexicale").set_index("index")


def mots_discriminants_mensuels() -> pd.DataFrame:
    return lire("fighting_words_temporal.csv", "lexicale")


def engagement() -> pd.DataFrame:
    return lire("engagement_bloc_stance.csv")


def activite_x() -> pd.DataFrame:
    return lire("activity_bias_by_bloc.csv", "lexicale")


def movers() -> pd.DataFrame:
    return lire("movers_caches.csv", "lexicale")


def interventions_an() -> pd.DataFrame:
    """Interventions en séance (16e législature, juillet 2022 – juin 2024), texte intégral."""
    df = pd.read_csv(INTERVENTIONS_AN, encoding="utf-8-sig")
    parties = df["date_seance"].str.extract(r"(\d{1,2})\s+(\S+)\s+(\d{4})")
    df["date"] = pd.to_datetime(
        parties[2] + "-" + parties[1].str.lower().map(MOIS).astype(str) + "-" + parties[0], format="%Y-%m-%d"
    )
    df["mois"] = df["date"].dt.to_period("M")
    df["texte"] = df["texte_discours"].fillna("")
    df["conflit"] = df["texte"].str.lower().str.contains(MOTIF_CONFLIT)
    df["cle"] = df["locuteur"].map(cle_personne)
    df["membre_gouvernement"] = df["locuteur"].str.contains(",", na=False)
    df["apres_7_octobre"] = df["date"] >= "2023-10-07"
    return df


def echantillon_validation() -> pd.DataFrame:
    e = pd.read_csv(VALIDATION / "echantillon.csv")
    llm = pd.read_csv(VALIDATION / "etiquettes_llm_v3.csv").rename(columns={"position_llm_v3": "position_llm"})
    return e.merge(llm, on="id", how="left")


__all__ = [n for n in dir() if not n.startswith("_")] + ["ORDRE_FENETRES"]
