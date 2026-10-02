"""Mesures de l'analyse secondaire, organisées par hypothèse (voir docs/methodologie.md)."""
import itertools

import numpy as np
import pandas as pd
from scipy import stats as sps

from . import chargement as ch
from . import stats as st
from .referentiel import BLOCS, LIBELLES, ORDRE_FENETRES


# Nature de chaque source : le texte seul, une extraction factuelle par le modèle, ou un jugement du modèle.
# Le prompt d'annotation indiquait au modèle l'auteur, son groupe et son bloc (voir docs/methodologie.md, §4).
# Les jugements sont donc exposés à un biais de conformité partisane ; les mesures sur le texte seul ne le sont pas.
NATURE = {
    "stance_mensuel.csv": "jugement", "anova_type2.csv": "jugement", "movers_caches.csv": "jugement",
    "emotional_register.csv": "jugement", "frames_par_bloc.csv": "jugement", "twitter_vs_an.csv": "jugement",
    "regression_delta_stance.csv": "jugement",
    "ceasefire_call_batch_bloc.csv": "extraction", "target_primary_par_batch_bloc.csv": "extraction",
    "key_demands_par_batch_bloc.csv": "extraction", "variables_batch_specifiques.csv": "extraction",
}


def nature(source: str) -> str:
    for cle, val in NATURE.items():
        if cle in source:
            return val
    return "texte"


class Registre:
    """Collecte les tables produites et les chiffres cités dans les documents."""

    def __init__(self):
        self.tables: dict[str, pd.DataFrame] = {}
        self.chiffres: list[dict] = []

    def table(self, nom, df):
        self.tables[nom] = df
        return df

    def chiffre(self, cle, valeur, libelle, source):
        self.chiffres.append({"cle": cle, "valeur": valeur, "libelle": libelle, "source": source, "nature": nature(source)})
        return valeur


# ---------------------------------------------------------------------------
# Fiabilité des données
# ---------------------------------------------------------------------------

def fiabilite(r: Registre):
    bruts = ch.auteurs_bruts()
    pers = ch.personnes()
    r.chiffre("auteurs_bruts", len(bruts), "Auteurs distincts dans les tables d'origine", "trajectoires_individuelles.csv")
    r.chiffre("personnes", len(pers), "Personnes réelles après fusion des doublons de civilité", "trajectoires_individuelles.csv")
    r.chiffre("doublons", int((pers["n_variantes"] > 1).sum()), "Personnes présentes sous plusieurs graphies", "trajectoires_individuelles.csv")
    r.table("fiabilite_personnes_par_bloc", pers.groupby("bloc").agg(personnes=("nom", "size"), textes=("n_textes", "sum"))
            .reindex(BLOCS).assign(auteurs_bruts=bruts.groupby("bloc").size().reindex(BLOCS)))

    v = ch.variables_fenetres()
    deg = v.groupby(["batch", "variable"])["pct"].apply(lambda s: bool((s == 100).all())).reset_index(name="degeneree")
    r.table("fiabilite_variables_v4", deg)
    r.chiffre("variables_degenerees", int(deg["degeneree"].sum()), "Variables v4 à 100 % dans tous les blocs (inutilisables)", "variables_batch_specifiques.csv")

    m = ch.movers()
    m["cle"] = m["author"].map(ch.cle_personne)
    m = m.merge(pers[["n_textes"]], left_on="cle", right_index=True, how="left")
    m["ecart_initial"] = m["stance_initial"] - m.groupby("bloc")["stance_initial"].transform("mean")
    rho, p = sps.spearmanr(m["ecart_initial"], m["delta_individuel"])
    r.chiffre("rtm_rho", rho, "Corrélation écart initial au bloc / changement individuel (régression vers la moyenne)", "movers_caches.csv")
    r.chiffre("rtm_p", p, "p-valeur associée", "movers_caches.csv")
    r.table("fiabilite_movers_forts", m[m["mover_type"] == "fort"][["author", "bloc", "stance_initial", "stance_final", "delta_individuel", "n_textes"]])

    # Concordance des deux chaînes sur les tables homonymes
    lignes = []
    a = ch.lire("stance_mensuel.csv", "lexicale").set_index(["month", "bloc"])["stance_v3"]
    b = ch.position_mensuelle().set_index(["month", "bloc"])["stance_mean"]
    lignes.append(("stance_mensuel", len(a), int((a - b.reindex(a.index)).abs().gt(0.01).sum())))
    a = ch.lire("ceasefire_call_batch_bloc.csv", "lexicale").set_index(["batch", "bloc"])["pct"] * 100
    b = ch.cessez_le_feu_par_fenetre().set_index(["batch", "bloc"])["pct_ceasefire"]
    lignes.append(("ceasefire_call_batch_bloc", len(a), int((a - b.reindex(a.index)).abs().gt(0.01).sum())))
    a = ch.lire("attrition_mensuelle.csv", "lexicale").set_index("month")["n_textes"]
    b = ch.lire("attrition_mensuelle.csv").set_index("month")["n_textes"]
    lignes.append(("attrition_mensuelle", len(a), int((a - b.reindex(a.index)).abs().gt(0).sum())))
    a = ch.lire("cosine_distance_mensuelle.csv", "lexicale")
    b = ch.lire("cosine_distance_mensuelle.csv")
    a["paire"] = a["pair"].str.replace(" vs ", " ↔ ")
    j = a.merge(b, left_on=["month", "paire"], right_on=["month", "pair"])
    lignes.append(("cosine_distance_mensuelle", len(j), int((j["dist"] - j["cosine_dist"]).abs().gt(0.01).sum())))
    r.chiffre("cosinus_correlation_chaines", float(j[["dist", "cosine_dist"]].corr().iloc[0, 1]),
              "Corrélation des deux mesures de distance cosinus (toutes paires, tous mois)", "cosine_distance_mensuelle.csv")
    r.table("fiabilite_concordance", pd.DataFrame(lignes, columns=["table", "valeurs_comparees", "ecarts"]))

    did_a = ch.lire("event_impact_diff_in_diff.csv", "lexicale")
    did_b = ch.lire("event_impact_diff_in_diff.csv")
    cij = pd.DataFrame({
        "chaine": ["lexicale", "variables"],
        "delta": [did_a.query("event == '2024-01-26' and bloc == 'Centre / Majorite'")["delta"].iloc[0],
                  did_b.query("event == 'Ordonnance CIJ' and bloc == 'Centre / Majorite' and variable == 'stance_v3'")["delta"].iloc[0]],
        "p": [did_a.query("event == '2024-01-26' and bloc == 'Centre / Majorite'")["p"].iloc[0],
              did_b.query("event == 'Ordonnance CIJ' and bloc == 'Centre / Majorite' and variable == 'stance_v3'")["p_mannwhitney"].iloc[0]],
    })
    r.table("fiabilite_cij_centre", cij)

    e = ch.echantillon_validation()
    r.table("validation_distribution_llm", e["position_llm"].value_counts().sort_index().rename("n").to_frame())


# ---------------------------------------------------------------------------
# H1. Cristallisation des positions
# ---------------------------------------------------------------------------

def h1_cristallisation(r: Registre):
    a = ch.anova()
    res = a.loc["Residual", "sum_sq"]
    eta = pd.DataFrame({
        "facteur": ["bloc", "fenêtre", "arène", "bloc × fenêtre"],
        "eta2_partiel": [a.loc[k, "sum_sq"] / (a.loc[k, "sum_sq"] + res) for k in ["C(bloc)", "C(batch)", "C(arena)", "C(bloc):C(batch)"]],
        "F": [a.loc[k, "F"] for k in ["C(bloc)", "C(batch)", "C(arena)", "C(bloc):C(batch)"]],
    })
    r.table("h1_anova", eta)
    r.chiffre("eta2_bloc", eta.loc[0, "eta2_partiel"], "η² partiel du bloc (position, 5 905 textes v4)", "anova_type2.csv")
    r.chiffre("eta2_fenetre", eta.loc[1, "eta2_partiel"], "η² partiel de la fenêtre", "anova_type2.csv")
    r.chiffre("eta2_arene", eta.loc[2, "eta2_partiel"], "η² partiel de l'arène", "anova_type2.csv")

    sm = ch.position_mensuelle()
    lignes = []
    for b in BLOCS:
        g = sm[(sm["bloc"] == b) & (sm["n"] >= 5)]
        h = st.heterogeneite(g["stance_mean"], g["se"])
        t = st.tendance_monotone(g["stance_mean"])
        lignes.append({"bloc": b, "mois": len(g), **h, "kendall_tau": t["tau"], "kendall_p": t["p"]})
    het = r.table("h1_heterogeneite", pd.DataFrame(lignes))
    for _, l in het.iterrows():
        r.chiffre(f"tau_{l['bloc']}", l["tau"], f"Écart-type réel mois à mois, {LIBELLES[l['bloc']]}", "stance_mensuel.csv")
        r.chiffre(f"moyenne_{l['bloc']}", l["moyenne"], f"Position moyenne pondérée, {LIBELLES[l['bloc']]}", "stance_mensuel.csv")

    p = sm.pivot(index="month", columns="bloc", values="stance_mean")
    n = sm.pivot(index="month", columns="bloc", values="n")
    ok = n[BLOCS].min(axis=1) >= 15
    ecart = p["Gauche radicale"] - p["Droite"]
    lam = (p["Centre / Majorite"] - p["Droite"]) / ecart
    serie = r.table("h1_ecart_et_centre", pd.DataFrame({"ecart_gr_droite": ecart, "position_relative_centre": lam,
                                                        "n_min": n[BLOCS].min(axis=1), "mois_retenu": ok}))
    te = st.tendance_monotone(ecart[ok])
    tl = st.tendance_monotone(lam[ok])
    r.chiffre("mois_complets", int(ok.sum()), "Mois où chaque bloc a au moins 15 textes", "stance_mensuel.csv")
    r.chiffre("ecart_moyen", ecart[ok].mean(), "Écart moyen gauche radicale – droite (points sur 4)", "stance_mensuel.csv")
    r.chiffre("ecart_min", ecart[ok].min(), "Écart minimal", "stance_mensuel.csv")
    r.chiffre("ecart_max", ecart[ok].max(), "Écart maximal", "stance_mensuel.csv")
    r.chiffre("ecart_tendance_p", te["p"], "Tendance de l'écart (Kendall), p", "stance_mensuel.csv")
    r.chiffre("lambda_moyen", lam[ok].mean(), "Position relative du Centre (0 = droite, 1 = gauche radicale)", "stance_mensuel.csv")
    r.chiffre("lambda_tendance_tau", tl["tau"], "Tendance de la position relative du Centre, τ", "stance_mensuel.csv")
    r.chiffre("lambda_tendance_p", tl["p"], "Tendance de la position relative du Centre, p", "stance_mensuel.csv")
    fw = ch.mots_discriminants_mensuels()
    gaza = fw[fw["word"] == "gaza"].set_index("month")["z"]
    hamas = fw[fw["word"] == "hamas"].set_index("month")["z"]
    r.table("h1_gaza_hamas", pd.DataFrame({"gaza": gaza, "hamas": hamas}))
    r.chiffre("gaza_mois_gauche", int((gaza > 0).sum()), "Mois où « gaza » est un mot distinctif de la gauche", "fighting_words_temporal.csv")
    r.chiffre("hamas_mois_droite", int((hamas < 0).sum()), "Mois où « hamas » est un mot distinctif de la droite", "fighting_words_temporal.csv")
    r.chiffre("mots_mois", int(len(hamas)), "Mois couverts par la table", "fighting_words_temporal.csv")
    r.chiffre("signal_bruit", ecart[ok].mean() / het["tau"].max(), "Écart inter-blocs rapporté à la plus forte variation temporelle intra-bloc", "stance_mensuel.csv")


# ---------------------------------------------------------------------------
# H2. Mobilité du cadrage (fonctions d'Entman)
# ---------------------------------------------------------------------------

def _distribution(df, categorie, valeur):
    p = df.pivot_table(index="bloc", columns=categorie, values=valeur, aggfunc="sum").fillna(0).reindex(BLOCS)
    return p.div(p.sum(axis=1), axis=0)


def h2_cadrage(r: Registre):
    fonctions = {
        "Définition du problème": _distribution(ch.cadres_v3(), "frame", "pct"),
        "Attribution": _distribution(ch.cibles_par_bloc(), "famille", "n"),
        "Évaluation morale": _distribution(ch.registres(), "register", "pct"),
        "Remède": _distribution(ch.demandes_par_fenetre(), "demande", "n"),
    }
    lignes = []
    for f, d in fonctions.items():
        for a, b in itertools.combinations(BLOCS, 2):
            lignes.append({"fonction": f, "paire": f"{LIBELLES[a]} / {LIBELLES[b]}", "divergence_js": st.divergence_js(d.loc[a], d.loc[b])})
    js = r.table("h2_divergences", pd.DataFrame(lignes).pivot(index="fonction", columns="paire", values="divergence_js")
                 .reindex(list(fonctions)))
    r.table("h2_attribution_distribution", fonctions["Attribution"])

    # Attribution : Israël contre Hamas et son axe, par fenêtre
    c = ch.cibles_par_fenetre()
    tot = c.groupby(["bloc", "batch"])["n"].sum()
    isr = c[c["famille"] == "israel"].groupby(["bloc", "batch"])["n"].sum().reindex(tot.index, fill_value=0)
    ham = c[c["famille"] == "hamas_axe"].groupby(["bloc", "batch"])["n"].sum().reindex(tot.index, fill_value=0)
    attr = ((isr - ham) / (isr + ham)).unstack("bloc").reindex(ORDRE_FENETRES)[BLOCS]
    r.table("h2_indice_attribution", attr)
    r.chiffre("attr_centre_choc", attr.loc["CHOC", "Centre / Majorite"], "Indice d'attribution du Centre, fenêtre du 7 octobre", "target_primary_par_batch_bloc.csv")
    r.chiffre("attr_centre_fin", attr.loc["NEW_OFFENSIVE", "Centre / Majorite"], "Indice d'attribution du Centre, avril-juin 2025", "target_primary_par_batch_bloc.csv")
    r.chiffre("attr_gr_choc", attr.loc["CHOC", "Gauche radicale"], "Indice d'attribution de la gauche radicale, fenêtre du 7 octobre", "target_primary_par_batch_bloc.csv")
    r.chiffre("attr_gm_choc", attr.loc["CHOC", "Gauche moderee"], "Indice d'attribution de la gauche modérée, fenêtre du 7 octobre", "target_primary_par_batch_bloc.csv")

    # Remède : appel au cessez-le-feu
    cf = ch.cessez_le_feu_par_fenetre()
    lignes = []
    for b in BLOCS:
        g = cf[cf["bloc"] == b].set_index("batch").reindex(ORDRE_FENETRES)
        t = st.tendance_proportions(g["n_ceasefire"], g["n_textes"])
        lignes.append({"bloc": b, **{f: g.loc[f, "pct_ceasefire"] for f in ORDRE_FENETRES}, "z": t["z"], "p": t["p"]})
        r.chiffre(f"cf_z_{b}", t["z"], f"Tendance de l'appel au cessez-le-feu, {LIBELLES[b]} (z)", "ceasefire_call_batch_bloc.csv")
    r.table("h2_cessez_le_feu", pd.DataFrame(lignes).set_index("bloc"))

    # Même question mesurée sur le texte seul (expression régulière, sans modèle de langage)
    lx = ch.lire("ceasefire_lexical.csv", "lexicale")
    pct, n = lx.pivot(index="month", columns="bloc", values="pct"), lx.pivot(index="month", columns="bloc", values="n")
    k = (pct * n).fillna(0)
    lignes = []
    for b in BLOCS:
        t = st.tendance_proportions(k[b].round(), n[b].fillna(0))
        avant = k[b].loc[:"2024-06"].sum() / n[b].loc[:"2024-06"].sum()
        apres = k[b].loc["2024-07":].sum() / n[b].loc["2024-07":].sum()
        lignes.append({"bloc": b, "oct_2023_juin_2024": avant, "juil_2024_janv_2026": apres, "z": t["z"], "p": t["p"]})
        r.chiffre(f"cflex_avant_{b}", avant, f"« cessez-le-feu » dans le texte, oct. 2023 – juin 2024, {LIBELLES[b]}", "ceasefire_lexical.csv")
        r.chiffre(f"cflex_apres_{b}", apres, f"« cessez-le-feu » dans le texte, juil. 2024 – janv. 2026, {LIBELLES[b]}", "ceasefire_lexical.csv")
        r.chiffre(f"cflex_z_{b}", t["z"], f"Tendance mensuelle, {LIBELLES[b]} (z)", "ceasefire_lexical.csv")
    r.table("h2_cessez_le_feu_lexical", pd.DataFrame(lignes).set_index("bloc"))

    # Évaluation morale : indignation, deuil, défiance par fenêtre
    e = ch.emotions_par_fenetre()
    lignes = []
    for reg in ["indignation", "grief", "defiance"]:
        for b in BLOCS:
            g = e[e["bloc"] == b]
            tot_f = g.groupby("batch")["total"].first().reindex(ORDRE_FENETRES)
            k = g[g["emotional_register"] == reg].groupby("batch")["n"].sum().reindex(ORDRE_FENETRES, fill_value=0)
            t = st.tendance_proportions(k, tot_f)
            lignes.append({"registre": reg, "bloc": b, **(100 * k / tot_f).round(1).to_dict(), "z": t["z"], "p": t["p"]})
    r.table("h2_registres_fenetres", pd.DataFrame(lignes))

    # Remède : textes sans aucune demande
    d = ch.demandes_par_fenetre()
    part = d.groupby("bloc").apply(lambda g: g.loc[g["demande"] == "none", "n"].sum() / g["n"].sum(), include_groups=False).reindex(BLOCS)
    r.table("h2_sans_demande", part.rename("part_sans_demande").to_frame())
    for b in BLOCS:
        r.chiffre(f"sans_demande_{b}", part[b], f"Part des textes sans demande, {LIBELLES[b]}", "key_demands_par_batch_bloc.csv")
    r.chiffre("js_cadre_gr_droite", js.loc["Définition du problème", "Gauche radicale / Droite"], "Divergence gauche radicale / droite sur la définition du problème", "frames_par_bloc.csv")


# ---------------------------------------------------------------------------
# H3. Cycle d'attention et appropriation de l'enjeu
# ---------------------------------------------------------------------------

def h3_attention(r: Registre):
    v = ch.volume_mensuel()
    parts = v.div(v.sum(axis=1), axis=0)
    nb_effectif = 1 / (parts ** 2).sum(axis=1)
    serie = r.table("h3_volume", v.assign(total=v.sum(axis=1), part_gauche_radicale=parts["Gauche radicale"], nombre_effectif_blocs=nb_effectif))
    t1 = st.tendance_monotone(parts["Gauche radicale"])
    t2 = st.tendance_monotone(nb_effectif)
    r.chiffre("part_gr_debut", parts["Gauche radicale"].iloc[0], "Part de la gauche radicale, octobre 2023", "volume_mensuel.csv")
    r.chiffre("part_gr_fin", parts["Gauche radicale"].iloc[-1], "Part de la gauche radicale, janvier 2026", "volume_mensuel.csv")
    r.chiffre("part_gr_p", t1["p"], "Tendance de la part de la gauche radicale, p", "volume_mensuel.csv")
    r.chiffre("neb_debut", nb_effectif.iloc[0], "Nombre effectif de blocs, octobre 2023", "volume_mensuel.csv")
    r.chiffre("neb_fin", nb_effectif.iloc[-1], "Nombre effectif de blocs, janvier 2026", "volume_mensuel.csv")
    r.chiffre("neb_p", t2["p"], "Tendance du nombre effectif de blocs, p", "volume_mensuel.csv")
    r.chiffre("volume_oct23", v.sum(axis=1).iloc[0], "Textes en octobre 2023", "volume_mensuel.csv")
    r.chiffre("volume_mediane", v.sum(axis=1).iloc[1:].median(), "Médiane mensuelle des textes après octobre 2023", "volume_mensuel.csv")

    pers = ch.personnes()
    n = pers["n_textes"]
    total = n.sum()
    conc = pd.DataFrame({"premiers": [1, 2, 5, 10, 20, 50, 100, len(n)],
                         "part_corpus": [n.head(k).sum() / total for k in [1, 2, 5, 10, 20, 50, 100, len(n)]]})
    r.table("h3_concentration", conc)
    r.table("h3_premiers_auteurs", pers.head(20)[["nom", "bloc", "n_textes"]])
    r.chiffre("gini", st.gini(n), "Indice de Gini de la production par personne", "trajectoires_individuelles.csv")
    r.chiffre("mediane_textes", n.median(), "Textes par personne (médiane, 28 mois)", "trajectoires_individuelles.csv")
    r.chiffre("top10", conc.loc[3, "part_corpus"], "Part du corpus produite par les 10 premiers", "trajectoires_individuelles.csv")
    r.chiffre("top20", conc.loc[4, "part_corpus"], "Part du corpus produite par les 20 premiers", "trajectoires_individuelles.csv")
    r.chiffre("au_plus_5", int((n <= 5).sum()), "Personnes ayant produit 5 textes ou moins", "trajectoires_individuelles.csv")
    gr = pers[pers["bloc"] == "Gauche radicale"]
    r.chiffre("part_personnes_gr", len(gr) / len(pers), "Part des personnes appartenant à la gauche radicale", "trajectoires_individuelles.csv")
    r.chiffre("part_textes_gr", gr["n_textes"].sum() / total, "Part des textes produits par la gauche radicale", "trajectoires_individuelles.csv")
    r.table("h3_activite_x", ch.activite_x().set_index("bloc").reindex(BLOCS))


# ---------------------------------------------------------------------------
# H4. Domestication du conflit
# ---------------------------------------------------------------------------

def h4_domestication(r: Registre):
    c = ch.cibles_par_fenetre()
    c["interieur"] = c["famille"].isin(["adversaires_fr", "executif_fr"])
    tot = c.groupby(["bloc", "batch"])["n"].sum()
    dom = c[c["interieur"]].groupby(["bloc", "batch"])["n"].sum().reindex(tot.index, fill_value=0)
    adv = c[c["famille"] == "adversaires_fr"].groupby(["bloc", "batch"])["n"].sum().reindex(tot.index, fill_value=0)
    t = pd.DataFrame({"textes": tot, "cibles_interieures": dom, "adversaires_partisans": adv})
    t["part_interieure"] = t["cibles_interieures"] / t["textes"]
    t["part_adversaires"] = t["adversaires_partisans"] / t["textes"]
    r.table("h4_cibles_interieures", t.reset_index())
    piv = t["part_interieure"].unstack("bloc").reindex(ORDRE_FENETRES)[BLOCS]
    r.table("h4_cibles_interieures_pivot", piv)

    tendances = []
    for b in BLOCS:
        g = t.xs(b, level="bloc").reindex(ORDRE_FENETRES)
        tt = st.tendance_proportions(g["cibles_interieures"], g["textes"])
        tendances.append({"bloc": b, "z": tt["z"], "p": tt["p"]})
    tend = r.table("h4_tendances", pd.DataFrame(tendances).set_index("bloc"))
    r.chiffre("droite_dom_z", tend.loc["Droite", "z"], "Droite : tendance des cibles intérieures sur les sept fenêtres (z)", "target_primary_par_batch_bloc.csv")
    r.chiffre("droite_dom_tendance_p", tend.loc["Droite", "p"], "p-valeur", "target_primary_par_batch_bloc.csv")

    d = t.xs("Droite", level="bloc")
    r.chiffre("droite_choc", d.loc["CHOC", "part_interieure"], "Droite : part des cibles intérieures, 7 oct. – 15 nov. 2023", "target_primary_par_batch_bloc.csv")
    r.chiffre("droite_fin", d.loc["NEW_OFFENSIVE", "part_interieure"], "Droite : part des cibles intérieures, avril-juin 2025", "target_primary_par_batch_bloc.csv")
    raf = d.loc["RAFAH"]
    reste = d.drop("RAFAH").sum()
    test = st.comparer_proportions(raf["cibles_interieures"], raf["textes"], reste["cibles_interieures"], reste["textes"])
    r.chiffre("droite_rafah", test["p_a"], "Droite : part des cibles intérieures, 1er mai – 15 juin 2024", "target_primary_par_batch_bloc.csv")
    r.chiffre("droite_rafah_n", int(raf["textes"]), "Droite : textes de la fenêtre", "target_primary_par_batch_bloc.csv")
    r.chiffre("droite_autres", test["p_b"], "Droite : part des cibles intérieures, autres fenêtres", "target_primary_par_batch_bloc.csv")
    r.chiffre("droite_rafah_p", test["p"], "Test khi², p", "target_primary_par_batch_bloc.csv")
    ensemble = t.groupby("bloc")[["cibles_interieures", "adversaires_partisans", "textes"]].sum()
    for b in BLOCS:
        r.chiffre(f"interieur_{b}", ensemble.loc[b, "cibles_interieures"] / ensemble.loc[b, "textes"], f"Part des cibles intérieures, {LIBELLES[b]}", "target_primary_par_batch_bloc.csv")
        r.chiffre(f"adversaires_{b}", ensemble.loc[b, "adversaires_partisans"] / ensemble.loc[b, "textes"], f"Part des cibles visant un adversaire partisan, {LIBELLES[b]}", "target_primary_par_batch_bloc.csv")

    fw = ch.mots_discriminants_mensuels()
    lfi = fw[fw["word"] == "lfi"].set_index("month")["z"]
    r.table("h4_lfi_mensuel", lfi.rename("z").to_frame())
    r.chiffre("lfi_mois_negatifs", int((lfi < 0).sum()), "Mois où « lfi » est un mot distinctif de la droite", "fighting_words_temporal.csv")
    r.chiffre("lfi_mois_total", int(len(lfi)), "Mois où « lfi » apparaît dans la table", "fighting_words_temporal.csv")
    r.chiffre("lfi_min_mois", str(lfi.idxmin()), "Mois du score le plus marqué", "fighting_words_temporal.csv")


# ---------------------------------------------------------------------------
# H5. Avant et après le 7 octobre à l'Assemblée (texte intégral, sans modèle de langage)
# ---------------------------------------------------------------------------

TERMES = {
    "apartheid": r"apartheid",
    "colonisation, colonies, colons": r"colonisation|colonies|\bcolons\b",
    "deux États": r"deux [ée]tats",
    "terrorisme, terroriste": r"terroris",
    "otage(s)": r"\botages?\b",
    "humanitaire": r"humanitaire",
    "cessez-le-feu": r"cessez-le-feu",
    "génocide": r"g[ée]nocid",
    "antisémitisme, antisémite": r"antis[ée]mit",
    "droit international": r"droit international",
}


def h5_avant_apres(r: Registre):
    df = ch.interventions_an()
    c = df[df["conflit"]]
    mensuel = df.groupby("mois").agg(interventions=("texte", "size"), sur_le_conflit=("conflit", "sum"),
                                     seances=("url_source", "nunique"))
    r.table("h5_mensuel_an", mensuel)
    avant = c[~c["apres_7_octobre"]]
    apres = c[c["apres_7_octobre"]]
    mois_avant = df.loc[~df["apres_7_octobre"], "mois"].nunique()
    mois_apres = df.loc[df["apres_7_octobre"], "mois"].nunique()
    debat = avant[avant["date"] == "2023-05-04"]
    r.chiffre("an_avant", len(avant), "Interventions sur le conflit, juillet 2022 – 6 octobre 2023", "data/an_2022_2024")
    r.chiffre("an_debat_4mai", len(debat), "dont débat du 4 mai 2023 (résolution n° 1082)", "data/an_2022_2024")
    r.chiffre("an_avant_par_mois_hors_debat", (len(avant) - len(debat)) / mois_avant, "Par mois de séance, hors 4 mai 2023", "data/an_2022_2024")
    r.chiffre("an_apres", len(apres), "Interventions sur le conflit, 7 octobre 2023 – juin 2024", "data/an_2022_2024")
    r.chiffre("an_apres_par_mois", len(apres) / mois_apres, "Par mois de séance", "data/an_2022_2024")
    r.chiffre("mois_avant", mois_avant, "Mois de séance avant", "data/an_2022_2024")
    r.chiffre("mois_apres", mois_apres, "Mois de séance après", "data/an_2022_2024")

    dep = c[~c["membre_gouvernement"]]
    o_av = set(dep.loc[~dep["apres_7_octobre"], "cle"])
    o_ap = set(dep.loc[dep["apres_7_octobre"], "cle"])
    pers = ch.personnes()
    part = pers.loc[pers.index.isin(o_av), "n_textes"].sum() / pers["n_textes"].sum()
    top20 = sorted(set(pers.head(20).index) & o_av)
    r.chiffre("orateurs_avant", len(o_av), "Députés intervenant sur le conflit avant le 7 octobre", "data/an_2022_2024")
    r.chiffre("orateurs_apres", len(o_ap), "Députés intervenant sur le conflit après (jusqu'en juin 2024)", "data/an_2022_2024")
    r.chiffre("orateurs_communs", len(o_av & o_ap), "Présents dans les deux périodes", "data/an_2022_2024")
    r.chiffre("part_corpus_orateurs_avant", part, "Part du corpus 2023-2026 produite par des orateurs d'avant le 7 octobre", "data/an_2022_2024 + trajectoires_individuelles.csv")
    r.chiffre("top20_deja_presents", len(top20), "Parmi les 20 premiers producteurs, déjà orateurs avant", "data/an_2022_2024 + trajectoires_individuelles.csv")
    r.table("h5_premiers_deja_presents", pers.loc[top20, ["nom", "bloc", "n_textes"]].sort_values("n_textes", ascending=False))
    r.table("h5_orateurs_4_mai_2023", debat.groupby("locuteur").size().sort_values(ascending=False).rename("interventions").to_frame())

    mots = lambda s: int(s.str.split().str.len().sum())
    ta, tp = avant["texte"].str.lower(), apres["texte"].str.lower()
    wa, wp = mots(ta), mots(tp)
    lignes = []
    for nom, motif in TERMES.items():
        ka, kp = int(ta.str.count(motif).sum()), int(tp.str.count(motif).sum())
        ra = st.taux_poisson(ka, wa)
        rp = st.taux_poisson(kp, wp)
        lignes.append({"terme": nom, "avant": ra[0], "avant_bas": ra[1], "avant_haut": ra[2],
                       "apres": rp[0], "apres_bas": rp[1], "apres_haut": rp[2], "n_avant": ka, "n_apres": kp})
    lex = r.table("h5_lexique_avant_apres", pd.DataFrame(lignes).set_index("terme"))
    r.chiffre("mots_avant", wa, "Mots des interventions sur le conflit, avant", "data/an_2022_2024")
    r.chiffre("mots_apres", wp, "Mots des interventions sur le conflit, après", "data/an_2022_2024")
    for terme in ["apartheid", "terrorisme, terroriste", "otage(s)", "humanitaire", "cessez-le-feu", "antisémitisme, antisémite"]:
        r.chiffre(f"lex_avant_{terme}", lex.loc[terme, "avant"], f"« {terme} » pour 10 000 mots, avant", "data/an_2022_2024")
        r.chiffre(f"lex_apres_{terme}", lex.loc[terme, "apres"], f"« {terme} » pour 10 000 mots, après", "data/an_2022_2024")


# ---------------------------------------------------------------------------
# Compléments et résultats nuls
# ---------------------------------------------------------------------------

def complements(r: Registre):
    reg = ch.lire("regression_delta_stance.csv", "lexicale")
    r.table("comp_twitter_an_regression", reg)
    tw = ch.lire("twitter_vs_an.csv")
    r.chiffre("arene_coef", tw["arena_Twitter_coef"].iloc[0], "Effet de l'arène X sur la position (bloc et mois contrôlés)", "twitter_vs_an.csv")
    r.chiffre("arene_p", tw["arena_Twitter_p"].iloc[0], "p-valeur", "twitter_vs_an.csv")
    gr = reg[reg["param"] == "C(bloc)[T.Gauche radicale]"].iloc[0]
    r.chiffre("gr_ecart_x_an", gr["coef"], "Gauche radicale : écart X – séance (député-mois)", "regression_delta_stance.csv")
    r.chiffre("gr_ecart_x_an_p", gr["pvalue"], "p-valeur", "regression_delta_stance.csv")

    e = ch.engagement()
    lignes = []
    for b, extreme in [("Gauche radicale", 2), ("Centre / Majorite", -2), ("Droite", -2)]:
        g = e[e["bloc"] == b].set_index("stance_v3")
        lignes.append({"bloc": b, "position_extreme": extreme, "mediane_extreme": g.loc[extreme, "engagement_median"],
                       "mediane_neutre": g.loc[0, "engagement_median"], "n_extreme": g.loc[extreme, "n"], "n_neutre": g.loc[0, "n"],
                       "rapport": g.loc[extreme, "engagement_median"] / g.loc[0, "engagement_median"]})
    r.table("comp_engagement", pd.DataFrame(lignes))

    vad = ch.lire("affective_vad_by_bloc_month.csv", "lexicale")
    mfd = ch.lire("moral_foundations_by_bloc_month.csv", "lexicale")
    r.table("comp_lexiques_nuls", pd.DataFrame({
        "mesure": ["valence", "activation", "dominance"] + ["soin", "équité", "loyauté", "autorité", "sainteté"],
        "min": [vad[c].min() for c in ["valence", "arousal", "dominance"]] + [mfd[c].min() for c in ["care", "fairness", "loyalty", "authority", "sanctity"]],
        "max": [vad[c].max() for c in ["valence", "arousal", "dominance"]] + [mfd[c].max() for c in ["care", "fairness", "loyalty", "authority", "sanctity"]],
    }))


SECTIONS = [fiabilite, h1_cristallisation, h2_cadrage, h3_attention, h4_domestication, h5_avant_apres, complements]
