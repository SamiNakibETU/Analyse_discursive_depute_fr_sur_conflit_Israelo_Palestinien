# 🇫🇷 Discours parlementaire français sur Gaza (2023–2026)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](requirements.txt)
[![Textes: 10 774](https://img.shields.io/badge/corpus-10%20774%20textes-green)]()
[![Députés: 459](https://img.shields.io/badge/députés-459-orange)]()
[![Méthodes: 7](https://img.shields.io/badge/méthodes%20de%20polarisation-7-purple)]()

Analyse computationnelle du discours de **459 députés** sur **10 774 textes** (tweets et interventions à l'Assemblée nationale) entre octobre 2023 et janvier 2026. Annotation de stance, analyse de cadrage, méthodes de science politique computationnelle.

> **Profil** : Sciences Po × Ingénieur × Data Science — un projet qui connecte
> l'analyse quantitative du discours politique aux méthodes de NLP et aux théories
> de la communication politique (Mayhew 1974, Monroe et al. 2008, Barberá et al. 2015).

---

## Résultat phare

![Stance mensuel par bloc](figures/fig10_stance_ribbon.png)

*Stance mensuel par bloc politique (oct. 2023 – janv. 2026). IC 95 %. Le Centre varie fortement après les événements pivot ; Gauche radicale et Droite restent stables.*

---

## Résultats principaux

| Résultat | Figure |
|----------|--------|
| Le Centre réagit, les extrêmes restent stables | [fig10](figures/fig10_stance_ribbon.png) |
| Paradoxe de la Droite au cessez-le-feu (Δ stance -1,03, p≈0,008) | [fig12](figures/fig12_diff_in_diff.png) |
| Convergence transpartisane tardive (G.mod 35,5 %, Centre 30,3 %) | [fig33](figures/fig33_convergence_batch.png) |
| Polarisation lexicale Gauche radicale / Droite | [fig18](figures/fig18_distance_cosinus_gr_droite.png) |
| Variables batch-spécifiques (condemns_hamas, genocide_framing...) | [fig28](figures/fig28_variables_batch.png) |

> **Résultat contre-intuitif** : quand le Centre appelle au cessez-le-feu (jan. 2025),
> la Droite *durcit* son discours au lieu de converger — compatible avec une stratégie
> de différenciation partisane (Meguid 2005, *Party Competition between Unequals*).

Voir [Catalogue des figures](docs/CATALOGUE_FIGURES.md) pour la liste complète (fig01–fig65).

---

## Positionnement académique

Ce projet s'inscrit dans le programme de recherche de la **science politique computationnelle** :

| Dimension | Contribution |
|-----------|-------------|
| Arènes | Twitter/X **ET** Assemblée nationale (dual-arena, rare en littérature) |
| Durée | 28 mois continus (oct. 2023 – jan. 2026) |
| Polarisation | 7 métriques : stance, cosinus, Wasserstein, entropie, VAD, MFT, registre |
| Événements | 7 batches × 6 event studies (design quasi-expérimental descriptif) |
| Langue | Corpus francophone (LFI → RN, lacune dans la littérature anglophone) |

Références clés : Monroe et al. (2008) fighting words ; Barberá et al. (2015) Twitter ideology ;
Rheault & Cochrane (2020) word embeddings parlementaires ; Çetinkaya et al. (2025) cross-platform.
Voir [État de l'art complet](docs/ETAT_DE_L_ART.md).

---

## Reproduction

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python src/prepare_data.py
python scripts/run_analysis.py
```

Le corpus (`corpus_v3.parquet`, `corpus_v4.parquet`) doit être placé dans `data/processed/` — ou copié via `prepare_data.py` si le projet source est voisin. Variable d'environnement : `GAZA_SOURCE_PROJECT`.

Le script produit CSV dans `data/results/`, figures dans `figures/`, rapport dans `data/results/RAPPORT_RESULTATS.txt`.

---

## Méthodologie

| Étape | Méthode |
|-------|---------|
| Annotation stance | Échelle -2 à +2, accord v3↔v4 : Spearman 0,86 |
| Segmentation | 7 batches (CHOC → NEW_OFFENSIVE), cf. [METHODOLOGIE.md](docs/METHODOLOGIE.md) |
| Event studies | Shift temporel avant/après, Mann-Whitney |
| Polarisation | Distance cosinus, log-odds (Monroe et al. 2008) |
| Polarisation affective | NRC-VAD (valence, arousal, dominance) |
| Fondements moraux | Moral Foundations Theory (eMFD, Hopp et al. 2021) |
| Réseau | Similarité cosinus inter-députés (NetworkX) — `src/network_analysis.py` |
| Topic modeling | BERTopic / LDA inductif — `src/topic_modeling.py` |

**Limites :** pas de validation humaine systématique ; corpus déséquilibré par bloc ; aucune inférence causale stricte ; LR et RN regroupés en « Droite » (test de robustesse en cours).

**Documentation :** [METHODOLOGIE.md](docs/METHODOLOGIE.md), [CODEBOOK.md](docs/CODEBOOK.md), [DONNEES.md](docs/DONNEES.md), [METHODES_COMPLEMENTAIRES.md](docs/METHODES_COMPLEMENTAIRES.md), [ETAT_DE_L_ART.md](docs/ETAT_DE_L_ART.md), [AMELIORATIONS.md](docs/AMELIORATIONS.md), [REFLEXION_CRITIQUE.md](docs/REFLEXION_CRITIQUE.md).

---

## Structure

```
├── scripts/    # run_analysis.py (script unique)
├── notebooks/  # 01–10 : reproductibles
├── src/        # config, prepare_data, vad_lexicon, mfd_lexicon, registre_discursif,
│               # network_analysis, topic_modeling, validation_humaine, validation_metrics
├── data/results/
├── figures/
└── docs/       # METHODOLOGIE.md, CODEBOOK.md, DONNEES.md, METHODES_COMPLEMENTAIRES.md,
                # ETAT_DE_L_ART.md, AMELIORATIONS.md, REFLEXION_CRITIQUE.md, STRATEGIE_CONTENU.md
```

---

## Livrables

- **Brief analytique** : [reports/brief_analytique.md](reports/brief_analytique.md) (8 pages, figures clés)
- **État de l'art** : [docs/ETAT_DE_L_ART.md](docs/ETAT_DE_L_ART.md) (10 références clés, positionnement)
- **Roadmap amélioration** : [docs/AMELIORATIONS.md](docs/AMELIORATIONS.md) (14 actions priorisées)
- **Réflexion critique** : [docs/REFLEXION_CRITIQUE.md](docs/REFLEXION_CRITIQUE.md) (forces, failles, questions socratiques)
- **Stratégie contenu** : [docs/STRATEGIE_CONTENU.md](docs/STRATEGIE_CONTENU.md) (8 épisodes Substack, 5 threads X)
- **Validation humaine** : `python src/validation_humaine.py` → annotation → `python src/validation_metrics.py`

---

## Licence

MIT © 2026
