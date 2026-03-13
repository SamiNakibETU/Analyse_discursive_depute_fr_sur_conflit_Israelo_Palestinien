# Discours parlementaire français sur le conflit israélo-palestinien (2023–2026)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](requirements.txt)
[![Corpus: 10 774 textes](https://img.shields.io/badge/corpus-10%20774%20textes-green)]()
[![Députés: 459](https://img.shields.io/badge/députés-459-orange)]()

Analyse computationnelle des prises de position publiques de députés français sur le conflit israélo-palestinien, via Twitter/X et l’Assemblée nationale.

---

## Objet

Entre octobre 2023 et janvier 2026, 459 députés ont produit 10 774 textes (tweets et interventions en séance) faisant référence au conflit israélo-palestinien. Ce corpus permet d’analyser :

- **Évolution temporelle** : positions par bloc politique sur 28 mois ;
- **Réactivité aux événements** : ordonnance CIJ, mandats CPI, cessez-le-feu, rupture du cessez-le-feu ;
- **Distance lexicale** : divergence et convergence des vocabulaires entre groupes.

---

## Données

| Dimension | Données |
|-----------|---------|
| **Corpus** | 10 774 textes, 459 députés |
| **Période** | Octobre 2023 – janvier 2026 |
| **Sources** | Twitter/X, Assemblée nationale |
| **Blocs** | Gauche radicale, Gauche modérée, Centre / Majorité, Droite |
| **Batches** | 7 fenêtres : CHOC, POST_CIJ, RAFAH, MANDATS_CPI, CEASEFIRE_BREACH, NEW_OFFENSIVE |

Détail : [METHODOLOGIE.md](docs/METHODOLOGIE.md), [DONNEES.md](docs/DONNEES.md).

---

## Méthode

### Annotation

**Stance** : échelle -2 à +2 (défense israélienne ↔ soutien palestinien / cessez-le-feu). Annotation par LLM, calibration par bloc. Accord inter-versions (v3↔v4) : Spearman ρ = 0,86 ; accord exact 61,6 %, accord à 1 pt 95,3 %.

**Cadres discursifs** : HUM, SEC, LEG, DIP, MOR, HIS, ECO, POL (références théoriques dans [CODEBOOK.md](docs/CODEBOOK.md)).

### Pipeline analytique

| Étape | Contenu |
|-------|---------|
| Données | Corpus v3 (10 774 textes) et v4 (5 905, fenêtres événementielles) |
| Segmentation | 7 batches alignés sur événements (CHOC → NEW_OFFENSIVE) |
| Analyses | Stance mensuel par bloc ; diff-in-diff avant/après événements ; distance cosinus TF-IDF ; log-odds (fighting words) ; polarisation entropique (Bao & Gill) |
| Compléments | VAD, fondements moraux (MFD), registre discursif, NER cibles |

→ [METHODOLOGIE.md](docs/METHODOLOGIE.md) · [METHODES_COMPLEMENTAIRES.md](docs/METHODES_COMPLEMENTAIRES.md)

---

## Résultats mesurés

### 1. Stance mensuel par bloc

![Stance mensuel par bloc](figures/fig10_stance_ribbon.png)

*Stance moyen par bloc politique (IC 95 %) sur 28 mois. Le Centre varie après les événements pivot ; la Gauche radicale et la Droite restent stables.*

### 2. Shift au cessez-le-feu (janv. 2025)

![Diff-in-diff événements × blocs](figures/fig12_diff_in_diff.png)

*Impact des événements sur le stance par bloc. Quand le Centre appelle au cessez-le-feu, la Droite durcit son discours (Δ stance −1,03, p ≈ 0,008).*

### 3. Convergence lexicale

![Convergence batch](figures/fig33_convergence_batch.png)

*Proportion de textes convergents vers le vocabulaire « cessez-le-feu » par bloc et batch. 35,5 % (G. modérée) et 30,3 % (Centre) en fin de période.*

### 4. Polarisation lexicale

![Distance cosinus G. radicale – Droite](figures/fig18_distance_cosinus_gr_droite.png)

*Distance cosinus TF-IDF entre vocabulaires Gauche radicale et Droite. Maximum en décembre 2024. Fighting words (log-odds) distinguent nettement les blocs.*

| Observation | Mesure |
|-------------|--------|
| Variation du Centre | Stance Centre varie après CIJ, mandats CPI, cessez-le-feu ; G. radicale et Droite stables |
| Shift Droite au cessez-le-feu | Δ stance = −1,03 (*p* ≈ 0,008) |
| Convergence lexicale | 35,5 % (G. modérée) et 30,3 % (Centre) en vocabulaire cessez-le-feu en fin de période |
| Polarisation lexicale | Distance cosinus max G. radicale / Droite en déc. 2024 |
| Robustesse | Résultats reproduits sur corpus équilibré (A4) |

→ [Catalogue des figures](docs/CATALOGUE_FIGURES.md) (fig01–fig76) · [Brief analytique](reports/analytical_brief.md)

---

## Reproduction

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python src/prepare_data.py
python scripts/run_analysis.py
```

Corpus requis dans `data/processed/` : `corpus_v3.parquet`, `corpus_v4.parquet`. Variable d’environnement : `GAZA_SOURCE_PROJECT` (projet source).

**Sorties** : CSV (`data/results/`), figures (`figures/`), rapport (`RAPPORT_RESULTATS.txt`), export MD (`reports/RESULTATS_NUMERIQUES.md`).

---

## Structure

```
analyse_discursive_depute/
├── scripts/          # run_analysis.py
├── notebooks/        # 01–13
├── src/              # config, lexiques, validation, NER
├── data/processed/   # corpus (non versionné)
├── data/results/     # CSV
├── figures/          # fig01–fig76
├── reports/
└── docs/             # METHODOLOGIE, CODEBOOK, DONNEES
```

---

## Documentation

[METHODOLOGIE.md](docs/METHODOLOGIE.md) · [CODEBOOK.md](docs/CODEBOOK.md) · [DONNEES.md](docs/DONNEES.md) · [METHODES_COMPLEMENTAIRES.md](docs/METHODES_COMPLEMENTAIRES.md)

---

## Limites

Validation humaine en cours. Corpus déséquilibré (Gauche radicale majoritaire) ; robustesse testée. Design descriptif avant/après, pas d’inférence causale stricte.

---

MIT © 2026
