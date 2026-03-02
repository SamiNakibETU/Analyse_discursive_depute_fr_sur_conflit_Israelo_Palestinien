# Discours parlementaire français sur Gaza (2023-2026)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](requirements.txt)

Analyse computationnelle du discours de **459 députés** sur **10 774 textes** (tweets et interventions à l'Assemblée nationale) entre octobre 2023 et janvier 2026. Annotation par LLM, analyse de cadrage, méthodes de science politique computationnelle.

---

## Résultats clés

- **Le Centre réagit, les extrêmes restent stables** — Seul le Centre varie significativement après la CIJ, les mandats CPI, le cessez-le-feu et sa rupture. Gauche radicale et Droite gardent des positions fixes sur 28 mois.
- **Convergence transpartisane tardive** — 35,5 % des textes G.mod et 30,3 % des textes Centre convergent vers le vocabulaire du cessez-le-feu en fin de période. La diffusion lexicale suit les positions implicites.
- **Réaction paradoxale de la Droite au cessez-le-feu** — Delta stance -1,03 (p≈0,008) : la Droite durcit son discours quand le Centre appelle au cessez-le-feu, signe de stratégie de différenciation.
- **Polarisation lexicale Gauche radicale / Droite** — Distance cosinus maximale en décembre 2024. Les « fighting words » (log-odds) distinguent nettement les vocabulaires par bloc.
- **Panel B4** — Sous-ensemble de députés actifs sur 18 mois consécutifs pour l’analyse des trajectoires individuelles et des movers.

---

## Structure

```
repo_propre/
├── notebooks/       # 8 notebooks : corpus → validation → dynamiques → polarisation → événements → convergence → émotions → analyses_fond
├── src/             # config, prepare_data, build_extra_analyses, export_figures_social
├── data/
│   ├── processed/   # corpus_v3.parquet, corpus_v4.parquet (non versionnés)
│   └── results/     # CSV générés par les notebooks et build_extra_analyses
├── figures/         # Figures PNG (générées par les notebooks)
└── docs/            # Méthodologie, catalogue figures, catalogue données
```

---

## Reproduction

```bash
# 1. Environnement
python -m venv .venv && .venv\Scripts\activate   # ou source .venv/bin/activate
pip install -r requirements.txt

# 2. Données
python src/prepare_data.py   # Copie depuis fr_assemblee_discourse_analysis si voisin
# Si absent : placer manuellement corpus_v3.parquet et corpus_v4.parquet dans data/processed/

# 3. Analyses supplémentaires
python src/build_extra_analyses.py

# 4. Notebooks dans l'ordre (01 → 08)
jupyter notebook notebooks/

# 5. Export figures (optionnel)
python src/export_figures_social.py   # → figures/social/
```

Variable d'environnement : `GAZA_SOURCE_PROJECT` pour indiquer le chemin du projet source (si différent du défaut).

---

## Méthodologie

| Étape | Outil / méthode |
|-------|-----------------|
| Annotation stance | LLM (corpus v3/v4), accord v3-v4 : Spearman 0,86, accord exact 61,6 % |
| Segmentation temporelle | 7 batches (CHOC → NEW_OFFENSIVE), cf. docs/METHODOLOGIE.md |
| Event studies | Shift temporel avant/après, Mann-Whitney |
| Régression | OLS avec HC3, interaction bloc × batch |
| Polarisation | Distance cosinus, log-odds (Monroe et al. 2008) |

---

## Figures principales

| Figure | Contenu |
|-------|---------|
| fig10 | Stance mensuel par bloc (ribbon + IC 95 %) |
| fig12 | Heatmap impact événements × blocs |
| fig33 | Convergence lexicale vers cessez-le-feu par batch |
| fig28 | Variables batch-spécifiques (condemns_hamas, etc.) |

Voir `docs/CATALOGUE_FIGURES.md` pour la liste complète.

---

## Licence

MIT © 2026
