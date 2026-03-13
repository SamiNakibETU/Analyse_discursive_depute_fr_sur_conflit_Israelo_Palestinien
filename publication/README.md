# Analyse discursive - Assemblée nationale française

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Analyse computationnelle du discours des députés français sur le conflit israélo-palestinien (oct. 2023 - jan. 2026)**

*Auteur : Sami Nakib*

---

## Résumé

Ce projet documente l'évolution des positions de 459 députés français sur le conflit israélo-palestinien à travers **10 774 textes** (tweets et interventions à l'Assemblée nationale) sur 28 mois. Il combine annotation LLM, analyse de cadrage et méthodes de science politique computationnelle.

**Lecture prudente du matériau :** les extrêmes apparaissent plus stables que le Centre dans les séries visibles, plusieurs fenêtres événementielles montrent des shifts avant/après par bloc, et certaines sorties suggèrent une convergence tardive. Ces résultats restent descriptifs et ne justifient pas d'inférence causale stricte.

---

## Structure du projet

```
fr_assemblee_discourse_analysis/
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── Makefile
├── docs/
│   ├── COMPTE_RENDU_RESULTATS.md   # Compte rendu exhaustif
│   ├── CODEBOOK.md                 # Prompts LLM, variables, batches
│   ├── METHODOLOGIE.md             # Méthodologie détaillée
│   ├── EXPLORATION_GROUPES.md      # Lien vers rapport mapping groupes → blocs
│   ├── PUBLICATION_CHECKLIST.md    # Checklist avant push GitHub
│   ├── PUSH_GIT.md                 # Instructions push sans Cursor Agent
│   └── RAPPORT_VALIDATION_AGENT.md # Rapport complet pour validation agent
│
├── data/
│   ├── raw/              # Données brutes (sources externes)
│   ├── processed/        # Corpus annotés (corpus_v3.parquet, corpus_v4.parquet)
│   ├── results/          # Résultats d'analyse (CSV)
│   └── README.md         # Documentation des données
│
├── src/
│   ├── config.py                   # Configuration (palette, événements, chemins)
│   ├── prepare_data.py             # Pipeline de préparation des données
│   ├── export_stance_par_groupe.py  # Export stance par groupe + panel vs complet
│   ├── build_analyses_extended.py   # CSV étendus (trajectoires, movers, cohérence, target, key_demands, etc.)
│   ├── ml_pipeline.py              # Validation ML : embeddings, fine-tuning CamemBERT
│   └── analyses_supplementaires.py  # Figures fig21–fig25 (Twitter vs AN, attrition, etc.)
│
├── notebooks/
│   ├── 01_corpus_validation.ipynb      # Données et validation méthodologique
│   ├── 02_framing_lexique_emotions.ipynb # Framing, stance, polarisation, émotions
│   ├── 03_evenements_convergence.ipynb  # Événements pivot et convergence
│   └── 04_ml_validation.ipynb           # Validation ML (embeddings, corrélation LLM vs ML)
│
└── reports/
    └── figures/          # Figures générées (PNG 300 DPI)
```

---

## Résultats clés

> **Compte rendu exhaustif** : [docs/COMPTE_RENDU_RESULTATS.md](docs/COMPTE_RENDU_RESULTATS.md)  
> **Rapport validation agent** : [docs/RAPPORT_VALIDATION_AGENT.md](docs/RAPPORT_VALIDATION_AGENT.md) - tous les résultats chiffrés pour vérification.

| Résultat | Détail |
|----------|--------|
| **Polarisation lexicale** | Distance cosinus Gauche↔Droite : 0,75–0,92 sur la période |
| **Variabilité du Centre** | Bloc le plus réactif dans les fenêtres visibles (Rafah +0,40, p=0,008 ; CIJ −0,44, p=0,018), sans être le seul à montrer des shifts ponctuels |
| **Diffusion temporelle** | Décalage d'environ 14 mois dans l'adoption du lexique « cessez-le-feu » entre blocs |
| **Convergence transpartisane** | 35,5 % G.mod, 30,3 % Centre au batch NEW_OFFENSIVE (mi-2025) |
| **Validation LLM** | Accord inter-version v3/v4 ρ=0,86 (Spearman) |

---

## Résultats visuels

### Évolution du stance par bloc (oct. 2023 – jan. 2026)

![Stance temporel](reports/figures/fig04_stance_evolution.png)

*Les positions des Gauche radicale et Droite restent stables ; le Centre / Majorité oscille au rythme des événements.*

### Impact des événements sur le stance (Δ avant → après)

![Event impact](reports/figures/fig11_event_impact_heatmap.png)

*Le Centre / Majorité est le bloc le plus souvent réactif dans les fenêtres visibles, mais certains autres blocs présentent aussi des shifts ponctuels.*

### Convergence transpartisane (batch NEW_OFFENSIVE)

![Convergence](reports/figures/fig12_convergence_transpartisane.png)

*En fin de période, 35,5 % de la Gauche modérée et 30,3 % du Centre montrent des signaux de convergence.*

### Discours Twitter vs Assemblée nationale

![Twitter vs AN](reports/figures/fig25_twitter_vs_an.png)

*Dans l'export visible `data/results/twitter_vs_an.csv`, l'effet moyen de l'arène Twitter n'est pas significatif une fois contrôlés le bloc et le frame (coef = -0,023 ; p = 0,336).*

---

## Installation et reproduction

```bash
# Cloner le repo
git clone https://github.com/SamiNakibETU/Analyse-discursive-sur-le-conflit-Israelo-Palestinien.git
cd Analyse-discursive-sur-le-conflit-Israelo-Palestinien

# Installer les dépendances
pip install -r requirements.txt
# ou: make install

# Option A : Les CSV dans data/results/ sont déjà fournis → lancer directement les notebooks
jupyter notebook notebooks/

# Option B : Régénérer les corpus (nécessite le projet source sibling avec les données annotées)
make data
# ou: python src/prepare_data.py

# Option C : Générer les figures complémentaires visibles dans ce repo (fig21 à fig25)
make figures
# ou: make analyses

# Option D : Générer les CSV étendus (trajectoires, movers, cohérence Twitter/AN, target, key_demands, conditionality, Droite)
make analyses_extended
# ou: python src/build_analyses_extended.py

# Option E : Pipeline ML (validation embeddings + corrélation LLM vs ML)
make ml
# ou: python src/ml_pipeline.py --mode embeddings && python src/ml_pipeline.py --mode validate

# Option F : Fine-tuning CamemBERT (GPU recommandé)
make ml-finetune
```

---

## Données

| Source | Volume | Période |
|--------|--------|---------|
| Tweets députés | 9 135 | oct. 2023 – jan. 2026 |
| Interventions AN | 1 639 | oct. 2023 – déc. 2025 |
| **Total (post-filtrage)** | **10 774** | **28 mois** |

Les données brutes ne sont pas incluses. Les corpus sont générés via `src/prepare_data.py` à partir d'un projet source sibling pointé par `src/config.py`. Ce repo versionne de nombreux CSV finaux, mais ne démontre pas seul toute la chaîne raw -> outputs.

---

## Notebooks

| Notebook | Contenu |
|----------|---------|
| `01_corpus_validation` | Validation du corpus, accord LLM (ρ=0.86), biais d'attrition, Panel B4 |
| `02_framing_lexique_emotions` | Cadres discursifs, stance, polarisation lexicale, registres émotionnels, diffusion cessez-le-feu, niveau individu (trajectoires, movers, variance) |
| `03_evenements_convergence` | Impact des événements (diff-in-diff), régression multivariée, convergence transpartisane, cohérence Twitter/AN, cibles, demandes, conditionnalité, cas négatif Droite |
| `04_ml_validation` | Validation ML : embeddings + LR, corrélation LLM vs ML par bloc/arène, fine-tuning CamemBERT |

---

## Méthodologie

- **Annotation** : GPT-4o-mini (v3 baseline, v4 longitudinale sur 7 fenêtres)
- **Validation** : Spearman ρ=0.86 (v3/v4), Wordscores ρ=0.92, Wordfish ρ=0.88
- **Modélisation** : OLS HC3, interaction bloc×batch
- **Ruptures** : algorithme Pelt (`ruptures`)
- **Analyses événementielles** : comparaisons avant/après par bloc sur 6 événements visibles ; pas de diff-in-diff canonique sans groupe contrôle

---

## Limites

- Pas de validation humaine systématique démontrée dans ce repo
- Corpus déséquilibré (63,5 % Gauche radicale)
- Panel B4 non représentatif (75 % G.rad)
- Pas de causalité stricte : « associé à », pas « causé par »
- Reproductibilité partielle : certains fichiers de sortie sont versionnés sans chaîne complète de régénération visible ici

## Pistes de recherche

- Validation humaine sur un échantillon de 100–200 textes
- Analyse au niveau individuel (député) plutôt que par bloc
- Séparation Twitter / AN pour tester l'hypothèse de « signaling digital »
- Extension du corpus aux débats du Sénat
- Comparaison avec d'autres parlements européens

---

## Cadre méthodologique

Ce travail adopte une posture académique et descriptive. Les résultats sont présentés de manière mesurée ; aucune prise de position normative n'est défendue. Les termes « stance », « polarisation » et « convergence » renvoient à des mesures quantitatives du discours, sans préjuger des positions des acteurs.

---

## Citation

Si vous utilisez ce travail, merci de citer :

```bibtex
@misc{nakib2026assemblee,
  author = {Nakib, Sami},
  title = {Analyse discursive du conflit israélo-palestinien à l'Assemblée nationale française},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/SamiNakibETU/Analyse-discursive-sur-le-conflit-Israelo-Palestinien},
  note = {10 774 textes, 459 députés, oct. 2023 - jan. 2026}
}
```

---

## Licence

MIT - voir [LICENSE](LICENSE).
