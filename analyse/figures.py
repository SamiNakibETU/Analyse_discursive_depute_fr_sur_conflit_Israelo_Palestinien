"""Figures de l'analyse secondaire (charte : docs/charte_graphique.md)."""
import urllib.request
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

from .chemins import FIGURES, POLICES
from .referentiel import BLOCS, LIBELLES, LIBELLES_FENETRES, ORDRE_FENETRES

ENCRE = "#111111"
FILET = "#D4D0CA"
GRIS = "#888888"
ACCENT = "#E8413C"
COULEURS = {"Gauche radicale": ACCENT, "Gauche moderee": "#F2A29F", "Centre / Majorite": "#8C8C8C", "Droite": ENCRE}
TRAITS = {"Gauche radicale": "-", "Gauche moderee": "-", "Centre / Majorite": "-", "Droite": "-"}

POLICES_GOOGLE = (
    "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;700"
    "&family=Barlow:ital,wght@0,400;0,500;1,400&family=Courier+Prime:wght@400;700"
)
TITRE = "Barlow Condensed"
TEXTE = "Barlow"
CHIFFRE = "Courier Prime"


def installer_polices():
    """Télécharge les polices de la charte (licence OFL) dans un cache local ; repli sur DejaVu sinon."""
    import re
    POLICES.mkdir(parents=True, exist_ok=True)
    if not any(POLICES.glob("*.ttf")):
        try:
            css = urllib.request.urlopen(POLICES_GOOGLE, timeout=20).read().decode()
            for fam, style, poids, url in re.findall(
                r"font-family: '([^']+)';\s*font-style: (\w+);\s*font-weight: (\d+);[^}]*?url\((https[^)]+\.ttf)\)", css, flags=re.S
            ):
                nom = f"{fam.replace(' ', '')}-{poids}{'-italic' if style == 'italic' else ''}.ttf"
                urllib.request.urlretrieve(url, POLICES / nom)
        except Exception as exc:  # réseau indisponible : figures en police de repli
            warnings.warn(f"Polices de la charte indisponibles ({exc}) ; repli sur DejaVu Sans.")
    for f in POLICES.glob("*.ttf"):
        font_manager.fontManager.addfont(str(f))


def style():
    installer_polices()
    familles = {f.name for f in font_manager.fontManager.ttflist}
    corps = TEXTE if TEXTE in familles else "DejaVu Sans"
    plt.rcParams.update({
        "font.family": [corps, "DejaVu Sans"], "font.size": 11, "text.color": ENCRE,
        "axes.edgecolor": ENCRE, "axes.labelcolor": ENCRE, "axes.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y",
        "grid.color": FILET, "grid.linewidth": 0.6, "xtick.color": ENCRE, "ytick.color": ENCRE,
        "xtick.labelsize": 10, "ytick.labelsize": 10, "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "legend.frameon": False,
    })


def _police(nom):
    familles = {f.name for f in font_manager.fontManager.ttflist}
    return nom if nom in familles else "DejaVu Sans"


def cadre(fig, titre, sous_titre, source, numero):
    fig.text(0.04, 0.965, numero, fontfamily=_police(TITRE), fontweight="bold", fontsize=11, color=ACCENT, va="top")
    fig.text(0.04, 0.93, titre, fontfamily=_police(TITRE), fontweight="bold", fontsize=21, va="top", color=ENCRE)
    fig.text(0.04, 0.862, sous_titre, fontsize=10.5, va="top", color=GRIS, linespacing=1.35)
    fig.text(0.04, 0.025, source, fontsize=8.5, color=GRIS, style="italic", va="bottom")
    fig.text(0.96, 0.025, "Sami Nakib", fontsize=8.5, color=GRIS, ha="right", va="bottom")


def nouvelle(numero, titre, sous_titre, source, haut=0.78, bas=0.12, gauche=0.08, droite=0.96, taille=(10, 6.2), **kw):
    fig = plt.figure(figsize=taille)
    cadre(fig, titre, sous_titre, source, numero)
    ax = fig.add_axes([gauche, bas, droite - gauche, haut - bas], **kw)
    return fig, ax


def enregistrer(fig, nom):
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{nom}.png", dpi=150)
    plt.close(fig)


def _axe_mois(ax, index):
    pos = np.arange(len(index))
    reperes = [i for i, m in enumerate(index) if str(m).endswith(("-01", "-07"))]
    ax.set_xticks(reperes)
    noms = {"01": "janv.", "07": "juil."}
    ax.set_xticklabels([f"{noms[str(index[i])[5:7]]} {str(index[i])[:4]}" for i in reperes])
    ax.set_xlim(-0.5, len(index) - 0.5)
    return pos


def _etiquette_fin(ax, x, y, texte, couleur, dy=0):
    ax.annotate(texte, (x, y), xytext=(6, dy), textcoords="offset points", va="center", fontsize=10,
                fontfamily=_police(TITRE), fontweight="bold", color=couleur, annotation_clip=False)


# ---------------------------------------------------------------------------

def f01_positions(tables):
    sm = tables["_position_mensuelle"]
    p = sm.pivot(index="month", columns="bloc", values="stance_mean")[BLOCS]
    lo = sm.pivot(index="month", columns="bloc", values="ci95_lo")[BLOCS]
    hi = sm.pivot(index="month", columns="bloc", values="ci95_hi")[BLOCS]
    n = sm.pivot(index="month", columns="bloc", values="n")[BLOCS]
    p, lo, hi = p.where(n >= 10), lo.where(n >= 10), hi.where(n >= 10)
    fig, ax = nouvelle("01", "Vingt-huit mois, quatre lignes plates",
                       "Position moyenne des textes de chaque bloc, de −2 (défense d'Israël) à +2 (soutien à la cause palestinienne),\n"
                       "avec intervalle de confiance à 95 %. L'écart entre gauche radicale et droite vaut 2,9 points en moyenne et ne se réduit pas.",
                       "Source : 10 774 tweets et interventions, annotation gpt-4o-mini (v3), modèle informé du groupe de l'auteur. Table stance_mensuel.csv. Mois à moins de 10 textes masqués.",
                       droite=0.84)
    x = _axe_mois(ax, list(p.index))
    for b in BLOCS:
        ax.fill_between(x, lo[b], hi[b], color=COULEURS[b], alpha=0.12, lw=0)
        ax.plot(x, p[b], color=COULEURS[b], lw=2.2)
        _etiquette_fin(ax, x[-1], p[b].dropna().iloc[-3:].mean(), LIBELLES[b], COULEURS[b])
    ax.axhline(0, color=ENCRE, lw=0.8)
    ax.set_ylim(-2, 2)
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_yticklabels(["−2", "−1", "0", "+1", "+2"], fontfamily=_police(CHIFFRE))
    enregistrer(fig, "f01_positions_mensuelles")


def f02_variance(tables):
    eta = tables["h1_anova"].iloc[::-1]
    fig, ax = nouvelle("02", "Le parti dit presque tout, le calendrier presque rien",
                       "Part de la variance des positions expliquée par chaque facteur (η² partiel), sur les 5 905 textes\n"
                       "des sept fenêtres événementielles. Le bloc de l'auteur pèse vingt fois plus que le moment où il s'exprime.",
                       "Source : table anova_type2.csv. Mesure exposée au biais du prompt (le modèle connaissait le groupe de l'auteur) : la part du bloc est un plafond.",
                       gauche=0.2, haut=0.74)
    couleurs = [ACCENT if f == "bloc" else ENCRE for f in eta["facteur"]]
    ax.barh(eta["facteur"], eta["eta2_partiel"], color=couleurs, height=0.55)
    for i, v in enumerate(eta["eta2_partiel"]):
        ax.text(v + 0.01, i, f"{v * 100:.1f} %".replace(".", ","), va="center", fontfamily=_police(CHIFFRE),
                fontweight="bold" if eta["facteur"].iloc[i] == "bloc" else "normal",
                color=ACCENT if eta["facteur"].iloc[i] == "bloc" else ENCRE)
    ax.set_xlim(0, 0.75)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.set_xticks([0, 0.25, 0.5, 0.75])
    ax.set_xticklabels(["0 %", "25 %", "50 %", "75 %"], fontfamily=_police(CHIFFRE))
    ax.tick_params(axis="y", labelsize=12)
    for lab in ax.get_yticklabels():
        lab.set_fontfamily(_police(TITRE))
        lab.set_fontweight("bold")
    enregistrer(fig, "f02_decomposition_variance")


def _fenetres(ax):
    x = np.arange(len(ORDRE_FENETRES))
    ax.set_xticks(x)
    ax.set_xticklabels([LIBELLES_FENETRES[f].replace(", ", ",\n").replace(" et ", "\net ") for f in ORDRE_FENETRES], fontsize=9)
    ax.set_xlim(-0.4, len(x) - 0.6)
    return x


def f03_cessez_le_feu(tables):
    cf = tables["h2_cessez_le_feu"][ORDRE_FENETRES]
    fig, ax = nouvelle("03", "Le cessez-le-feu a changé de camp",
                       "Part des textes appelant explicitement à un cessez-le-feu, par fenêtre et par bloc. La demande s'effondre à gauche\n"
                       "(de 37 % à 8 % pour la gauche radicale) pendant qu'elle s'installe au Centre, qui la formule davantage dès l'automne 2024.",
                       "Source : annotation v4, 5 905 textes, table ceasefire_call_batch_bloc.csv. Même tendance sur le texte seul (ceasefire_lexical.csv). Tests de Cochran-Armitage.",
                       droite=0.82)
    x = _fenetres(ax)
    for b in BLOCS:
        ax.plot(x, cf.loc[b], color=COULEURS[b], lw=2.4 if b in ("Gauche radicale", "Centre / Majorite") else 1.4,
                marker="o", ms=4)
        z = tables["h2_cessez_le_feu"].loc[b, "z"]
        _etiquette_fin(ax, x[-1], cf.loc[b].iloc[-1] + {"Gauche moderee": 2.2, "Gauche radicale": -2.2, "Droite": 2.6}.get(b, 0),
                       f"{LIBELLES[b]}  z = {z:+.1f}".replace(".", ",").replace("-", "−"), COULEURS[b])
    ax.set_ylim(0, 55)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_yticklabels([f"{v} %" for v in [0, 10, 20, 30, 40, 50]], fontfamily=_police(CHIFFRE))
    enregistrer(fig, "f03_cessez_le_feu")


def f04_attribution(tables):
    a = tables["h2_indice_attribution"]
    fig, ax = nouvelle("04", "Qui est responsable ? La réponse ne bouge qu'au Centre",
                       "Indice d'attribution : (cibles israéliennes − cibles Hamas et alliés) / (somme des deux). +1 : seul Israël est visé ;\n"
                       "−1 : seuls le Hamas et ses alliés. Les gauches ne visent plus qu'Israël dès janvier 2024 ; le Centre quitte le pôle Hamas.",
                       "Source : cible principale de chaque texte, annotation v4. Table target_primary_par_batch_bloc.csv, regroupement documenté.",
                       droite=0.82)
    x = _fenetres(ax)
    ax.axhline(0, color=ENCRE, lw=0.8)
    for b in BLOCS:
        ax.plot(x, a[b], color=COULEURS[b], lw=2.4 if b == "Centre / Majorite" else 1.6, marker="o", ms=4)
        _etiquette_fin(ax, x[-1], a[b].iloc[-1] + {"Gauche moderee": -0.09, "Gauche radicale": 0.07}.get(b, 0), LIBELLES[b], COULEURS[b])
    ax.set_ylim(-1.05, 1.1)
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticklabels(["−1\nHamas", "−0,5", "0", "+0,5", "+1\nIsraël"], fontfamily=_police(CHIFFRE))
    enregistrer(fig, "f04_attribution")


def f05_fonctions(tables):
    js = tables["h2_divergences"]
    paires = [("Gauche radicale / Droite", "Gauche radicale / droite", ENCRE, "s"),
              ("Centre / Majorité / Droite", "Centre / droite", GRIS, "o"),
              ("Gauche modérée / Centre / Majorité", "Centre / gauche modérée", ACCENT, "o")]
    fig, ax = nouvelle("05", "Le Centre pense comme la droite et ressent comme la gauche",
                       "Divergence de Jensen-Shannon entre les distributions de deux blocs, pour chacune des quatre fonctions du cadrage\n"
                       "(Entman, 1993). 0 : discours identiques ; 1 : sans rien en commun. Plus le point est à gauche, plus les blocs se ressemblent.",
                       "Sources : cadres (frames_par_bloc.csv, v3), cibles et demandes (v4), registres émotionnels (emotional_register.csv).",
                       gauche=0.25, haut=0.74, droite=0.95)
    y = np.arange(len(js.index))[::-1]
    for col, lib, coul, mk in paires:
        ax.scatter(js[col], y, s=90 if mk == "s" else 75, color=coul, marker=mk, zorder=3, label=lib)
    for i, f in enumerate(js.index):
        ax.plot([js.loc[f].min(), js.loc[f].max()], [y[i], y[i]], color=FILET, lw=1, zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels(js.index, fontfamily=_police(TITRE), fontweight="bold", fontsize=12)
    ax.set_xlim(0, 0.5)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_xticklabels(["0", "0,1", "0,2", "0,3", "0,4", "0,5"], fontfamily=_police(CHIFFRE))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.legend(loc="lower right", fontsize=9.5, handletextpad=0.3)
    enregistrer(fig, "f05_fonctions_du_cadrage")


def f06_registres(tables):
    r = tables["h2_registres_fenetres"].set_index(["registre", "bloc"])
    fig = plt.figure(figsize=(10, 6.2))
    cadre(fig, "Le deuil s'éteint, l'indignation s'installe",
          "Part des textes par registre émotionnel dominant, par fenêtre. À gauche radicale, le deuil passe de 14 % à 3 % pendant que\n"
          "l'indignation monte de 51 % à 68 %. À droite, la défiance domine dès le premier jour et ne cède qu'en partie.",
          "Source : annotation v4. Table emotional_register_v4.csv. Tendances : Cochran-Armitage.", "06")
    panneaux = [("Gauche radicale", [("indignation", ACCENT), ("grief", ENCRE)]),
                ("Droite", [("defiance", ENCRE), ("indignation", ACCENT)])]
    noms = {"indignation": "indignation", "grief": "deuil", "defiance": "défiance"}
    for k, (b, regs) in enumerate(panneaux):
        ax = fig.add_axes([0.07 + k * 0.47, 0.19, 0.31, 0.53])
        x = _fenetres(ax)
        ax.set_xticklabels(["7 oct.", "CIJ", "Rafah", "Sinwar", "CPI", "Cessez-le-feu", "Offensive"], rotation=35, ha="right", fontsize=8.5)
        for reg, coul in regs:
            ligne = r.loc[(reg, b)]
            ax.plot(x, [ligne[f] for f in ORDRE_FENETRES], color=coul, lw=2.2, marker="o", ms=3.5)
            _etiquette_fin(ax, x[-1], ligne[ORDRE_FENETRES[-1]], f"{noms[reg]}  z = {ligne['z']:+.1f}".replace(".", ",").replace("-", "−"), coul)
        ax.set_title(LIBELLES[b], loc="left", fontfamily=_police(TITRE), fontweight="bold", fontsize=13)
        ax.set_ylim(0, 85)
        ax.set_yticks([0, 20, 40, 60, 80])
        ax.set_yticklabels([f"{v} %" for v in [0, 20, 40, 60, 80]], fontfamily=_police(CHIFFRE), fontsize=9)
    enregistrer(fig, "f06_registres_emotionnels")


def f07_volume(tables):
    v = tables["h3_volume"]
    fig = plt.figure(figsize=(10, 6.2))
    cadre(fig, "L'attention retombe, et la parole se resserre sur un camp",
          "En haut : textes par mois et par bloc. En bas : part de la gauche radicale dans le volume mensuel. Après le pic d'octobre 2023\n"
          "(1 353 textes), le volume se stabilise autour de 320 par mois, et la gauche radicale en fournit une part croissante (48 % puis 85 %).",
          "Source : table volume_mensuel.csv. Tendance de la part : τ de Kendall = 0,29, p = 0,03.", "07")
    ax = fig.add_axes([0.08, 0.42, 0.76, 0.36])
    idx = list(v.index)
    x = np.arange(len(idx))
    bas = np.zeros(len(x))
    for b in BLOCS[::-1]:
        ax.bar(x, v[b], bottom=bas, color=COULEURS[b], width=0.8, lw=0)
        bas += v[b].to_numpy()
    for b, yy in zip(BLOCS, [1150, 820, 560, 260]):
        ax.text(len(x) - 0.2, yy, LIBELLES[b], color=COULEURS[b], fontfamily=_police(TITRE), fontweight="bold", fontsize=10)
    ax.set_xlim(-0.6, len(x) - 0.4)
    ax.set_xticks([])
    ax.set_yticks([0, 500, 1000])
    ax.set_yticklabels(["0", "500", "1 000"], fontfamily=_police(CHIFFRE))
    ax2 = fig.add_axes([0.08, 0.12, 0.76, 0.24])
    _axe_mois(ax2, idx)
    ax2.plot(x, v["part_gauche_radicale"] * 100, color=ACCENT, lw=2.2)
    ax2.fill_between(x, 0, v["part_gauche_radicale"] * 100, color=ACCENT, alpha=0.1, lw=0)
    ax2.set_ylim(0, 100)
    ax2.set_yticks([0, 50, 100])
    ax2.set_yticklabels(["0 %", "50 %", "100 %"], fontfamily=_police(CHIFFRE))
    enregistrer(fig, "f07_volume_et_appropriation")


def f08_concentration(tables):
    c = tables["h3_concentration"]
    fig, ax = nouvelle("08", "Vingt députés font la moitié du débat",
                       "Part cumulée des 10 774 textes produite par les N personnes les plus prolifiques, sur 332 personnes au total\n"
                       "(après fusion des doublons de nom). La personne médiane a produit 6 textes en 28 mois.",
                       "Source : table trajectoires_individuelles.csv, noms normalisés. Indice de Gini : 0,77.",
                       gauche=0.2, haut=0.74)
    lib = [f"{k} personne{'s' if k > 1 else ''}" for k in c["premiers"]]
    lib[-1] = "les 332"
    y = np.arange(len(c))[::-1]
    for i, (yy, v) in enumerate(zip(y, c["part_corpus"])):
        coul = ACCENT if c["premiers"].iloc[i] == 20 else (FILET if i == len(c) - 1 else ENCRE)
        ax.barh(yy, v, color=coul, height=0.6)
        ax.text(v + 0.01, yy, f"{v * 100:.0f} %", va="center", fontfamily=_police(CHIFFRE), color=ACCENT if coul == ACCENT else ENCRE,
                fontweight="bold" if coul == ACCENT else "normal")
    ax.set_yticks(y)
    ax.set_yticklabels(lib, fontfamily=_police(TITRE), fontweight="bold", fontsize=11.5)
    ax.set_xlim(0, 1.08)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(["0 %", "25 %", "50 %", "75 %", "100 %"], fontfamily=_police(CHIFFRE))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    enregistrer(fig, "f08_concentration")


def f09_domestication(tables):
    piv = tables["h4_cibles_interieures_pivot"] * 100
    tend = tables["h4_tendances"]
    fig, ax = nouvelle("09", "Pour la droite, Gaza devient une affaire française",
                       "Part des textes dont la cible principale est un acteur politique français (adversaire partisan ou exécutif), par fenêtre.\n"
                       "À droite, elle passe de 17 % à 45 % pendant la campagne européenne, puis se maintient au-dessus du niveau initial.",
                       "Source : annotation v4, table target_primary_par_batch_bloc.csv. Fenêtre « Rafah, européennes » : 1er mai – 15 juin 2024 (67 textes de droite).",
                       droite=0.8)
    x = _fenetres(ax)
    ax.axvspan(1.6, 2.4, color=FILET, alpha=0.45, lw=0)
    for b in BLOCS:
        ax.plot(x, piv[b], color=COULEURS[b], lw=2.6 if b == "Droite" else 1.4, marker="o", ms=4 if b == "Droite" else 3)
        z = tend.loc[b, "z"]
        _etiquette_fin(ax, x[-1], piv[b].iloc[-1] + {"Gauche radicale": -1.4, "Gauche moderee": -1.8, "Centre / Majorite": 1.6}.get(b, 0),
                       f"{LIBELLES[b]}  z = {z:+.1f}".replace(".", ",").replace("-", "−"), COULEURS[b])
    ax.set_ylim(0, 50)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_yticklabels([f"{v} %" for v in [0, 10, 20, 30, 40, 50]], fontfamily=_police(CHIFFRE))
    enregistrer(fig, "f09_domestication")


def f10_an_mensuel(tables):
    m = tables["h5_mensuel_an"]
    idx = pd.period_range(m.index.min(), m.index.max(), freq="M")
    s = m["sur_le_conflit"].reindex(idx, fill_value=0)
    fig, ax = nouvelle("10", "Avant le 7 octobre, un seul débat",
                       "Interventions en séance mentionnant explicitement Gaza, Israël, la Palestine, le Hamas ou la Cisjordanie, par mois.\n"
                       "Avant le 7 octobre : trois par mois en moyenne, sauf le 4 mai 2023 (résolution sur « l'apartheid », 79 interventions).",
                       "Source : comptes rendus intégraux de l'Assemblée nationale (open data), 16e législature, juillet 2022 – juin 2024.")
    x = np.arange(len(idx))
    coul = [ACCENT if p >= pd.Period("2023-10", "M") else ENCRE for p in idx]
    ax.bar(x, s.values, color=coul, width=0.75, lw=0)
    reperes = [i for i, p in enumerate(idx) if p.month in (1, 7)]
    ax.set_xticks(reperes)
    ax.set_xticklabels([f"{'janv.' if idx[i].month == 1 else 'juil.'} {idx[i].year}" for i in reperes])
    i_mai = list(idx).index(pd.Period("2023-05", "M"))
    i_oct = list(idx).index(pd.Period("2023-10", "M"))
    ax.annotate("4 mai 2023\nrésolution n° 1082", (i_mai, s.iloc[i_mai]), xytext=(i_mai - 4.5, 200), fontsize=9.5,
                arrowprops=dict(arrowstyle="-", color=GRIS, lw=0.8), color=ENCRE)
    ax.annotate("7 octobre 2023 : 301", (i_oct, s.iloc[i_oct]), xytext=(i_oct + 1.0, 290), fontsize=9.5, color=ACCENT,
                fontfamily=_police(TITRE), fontweight="bold")
    ax.set_ylim(0, 330)
    ax.set_yticks([0, 100, 200, 300])
    ax.set_yticklabels(["0", "100", "200", "300"], fontfamily=_police(CHIFFRE))
    ax.set_xlim(-0.6, len(x) - 0.4)
    enregistrer(fig, "f10_assemblee_avant_apres")


def f11_lexique(tables):
    lx = tables["h5_lexique_avant_apres"]
    ordre = ["apartheid", "colonisation, colonies, colons", "deux États", "antisémitisme, antisémite", "droit international",
             "génocide", "cessez-le-feu", "otage(s)", "humanitaire", "terrorisme, terroriste"]
    lx = lx.loc[ordre]
    fig, ax = nouvelle("11", "De l'occupation à la guerre",
                       "Fréquence de quelques termes pour 10 000 mots, dans les interventions en séance sur le conflit, avant le 7 octobre\n"
                       "(14 mois, 22 508 mots) et après (9 mois, 106 762 mots). Traits fins : intervalle de confiance à 95 % (Poisson).",
                       "Source : comptes rendus intégraux de l'Assemblée nationale, juillet 2022 – juin 2024. Comptage par expressions régulières.",
                       gauche=0.27, haut=0.76, droite=0.95)
    y = np.arange(len(lx))[::-1]
    for i, t in enumerate(lx.index):
        r = lx.loc[t]
        ax.plot([r["avant"], r["apres"]], [y[i], y[i]], color=FILET, lw=2.2, zorder=1)
        ax.plot([r["avant_bas"], r["avant_haut"]], [y[i] + 0.12] * 2, color=ENCRE, lw=0.8)
        ax.plot([r["apres_bas"], r["apres_haut"]], [y[i] - 0.12] * 2, color=ACCENT, lw=0.8)
        ax.scatter(r["avant"], y[i], color=ENCRE, s=55, zorder=3)
        ax.scatter(r["apres"], y[i], color=ACCENT, s=55, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(lx.index, fontfamily=_police(TITRE), fontweight="bold", fontsize=11.5)
    ax.set_xlim(0, 42)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xticklabels(["0", "10", "20", "30", "40"], fontfamily=_police(CHIFFRE))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.scatter([], [], color=ENCRE, s=55, label="avant le 7 octobre")
    ax.scatter([], [], color=ACCENT, s=55, label="après")
    ax.legend(loc="center right", fontsize=10)
    enregistrer(fig, "f11_lexique_avant_apres")


TOUTES = [f01_positions, f02_variance, f03_cessez_le_feu, f04_attribution, f05_fonctions, f06_registres,
          f07_volume, f08_concentration, f09_domestication, f10_an_mensuel, f11_lexique]
