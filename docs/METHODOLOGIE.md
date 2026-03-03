# Méthodologie — Analyse discursive sur le conflit israélo-palestinien

Documentation pas à pas du pipeline analytique complet (octobre 2023 – janvier 2026).

---

## 1. Vue d'ensemble

| Phase | Contenu | Fichiers / Commandes |
|-------|---------|----------------------|
| **1** | Données brutes | Tweets + interventions AN (projet source) |
| **2** | Annotation | `stance_v3`, `stance_v4`, cadres, batches |
| **3** | Préparation | `prepare_data.py` |
| **4** | Analyses | `scripts/run_analysis.py` ou notebooks 01 → 10 |
| **5** | Validation | `validation_humaine.py`, `validation_metrics.py` |

---

## 2. Données sources

### 2.1 Corpus principal (v3)

- **Tweets** : `tweets_v3_full_clean.parquet` — textes, date, groupe politique, annotation de stance
- **Interventions AN** : `interventions_v3_full_clean.parquet` — idem
- **Unification** : fusion en un seul `corpus_v3.parquet` avec colonnes harmonisées (`author`, `bloc`, `date`, `text`, `stance_v3`, etc.)
- **Effectif** : 10 774 textes, 459 députés

### 2.2 Corpus événementiel (v4)

- **Fenêtres** : textes centrés sur 6–7 événements pivot (CIJ, Rafah, mandats CPI, cessez-le-feu, rupture CLF, etc.)
- **Fichier** : `corpus_v4.parquet`
- **Effectif** : 5 905 textes (sous-ensemble du v3)
- **Usage** : analyses par batch, variables batch-spécifiques, régression avec interaction

---

## 3. Annotation de stance

### 3.1 Échelle

| Score | Interprétation |
|-------|----------------|
| -2 | Très favorable à Israël / défense israélienne |
| -1 | Plutôt favorable à Israël |
| 0 | Neutre / ambigu / équilibré |
| +1 | Plutôt favorable à la Palestine / cessez-le-feu |
| +2 | Très favorable à la Palestine |

### 3.2 Versions

- **v3** : corpus complet, prompt standard
- **v4** : corpus par fenêtres, prompt enrichi (contexte temporel, événements)
- **Accord inter-version** : Spearman ρ = 0,86 ; accord exact 61,6 % ; accord à 1 pt 95,3 %

### 3.3 Variables annexes

- `primary_frame_v3` : cadrage (HUM, SEC, LEG, DIP, MOR, ECO, HIS, POL)
- `primary_target_v3` : cible principale (ISRAEL_GOV, HAMAS, FRANCE, etc.)
- Variables batch-spécifiques (v4) : `genocide_framing`, `condemns_hamas_attack`, `state_recognition_mention`, `transpartisan_convergence`, etc.

---

## 4. Classification politique (blocs)

| Bloc | Groupes |
|------|---------|
| Gauche radicale | LFI, NFP, GDR |
| Gauche modérée | SOC, PS, ECO |
| Centre / Majorité | REN, MODEM, HOR, EPR, DEM |
| Droite | LR, RN, UDR, NI (regroupés) |

Justification du regroupement Droite : insuffisance de données pour séparer LR et RN sur certaines analyses ; rapport d’exploration dans `docs/`.

---

## 5. Fenêtres temporelles (batches)

| Batch | Période | Événement pivot |
|-------|---------|------------------|
| CHOC | 7 oct. – 31 déc. 2023 | Attaque du 7 octobre |
| POST_CIJ | 26 jan. – 30 avr. 2024 | Ordonnance CIJ |
| RAFAH | 7 mai – 15 oct. 2024 | Offensive Rafah |
| POST_SINWAR | 16 oct. – 20 nov. 2024 | Mort Sinwar |
| MANDATS_CPI | 21 nov. 2024 – 14 janv. 2025 | Mandats CPI |
| CEASEFIRE_BREACH | 15 janv. – 17 mars 2025 | Cessez-le-feu |
| NEW_OFFENSIVE | 18 mars 2025 – 31 janv. 2026 | Reprise offensive |

---

## 6. Pipeline de préparation (étapes exécutables)

### 6.1 Étape 1 : `python src/prepare_data.py`

- **Rôle** : copier les corpus (`corpus_v3.parquet`, `corpus_v4.parquet`) et les CSV de résultats depuis le projet source
- **Source** : variable `GAZA_SOURCE_PROJECT` ou `fr_assemblee_discourse_analysis` (sibling)
- **Sortie** : `data/processed/` (corpus), `data/results/` (CSV si disponibles)

### 6.2 Étape 2 : `python scripts/run_analysis.py`

- **Prérequis** : `corpus_v3.parquet` et `corpus_v4.parquet` dans `data/processed/`
- **Génère** : tous les CSV dans `data/results/`, toutes les figures dans `figures/`, rapport dans `data/results/RAPPORT_RESULTATS.txt`
- **Équivalent** : exécution consolidée des notebooks 01 → 10

---

## 7. Analyses par notebook (détail pas à pas)

### 7.1 NB01 — Portrait du corpus

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Chargement | corpus v3, v4 | — |
| Volume | empilé par bloc, par arène | fig01, fig02 |
| Attrition | députés actifs par mois | fig03 |
| Déséquilibre | répartition blocs | fig04 |
| Stance | violin par bloc | fig05 |
| Panel B4 | 76 députés, 4 mois continus | composition, fig08 |

**CSV produits** : `volume_mensuel.csv`, `volume_par_groupe.csv`, `attrition_mensuelle.csv`, `stance_panel_vs_complet.csv`

### 7.2 NB02 — Validation annotation

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Matrice confusion | v3 vs v4 (textes communs) | fig06 |
| Calibration | stance moyen par bloc | fig07 |
| Panel B4 vs complet | comparaison des moyennes | fig08 |
| Lexical vs stance | corrélation proxy lexical – stance | fig09 |

**Validation** : Spearman, Pearson, accord de signe.

### 7.3 NB03 — Dynamiques temporelles

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Stance mensuel | par bloc, IC 95 % | fig10 |
| Panel B4 | stance ribbon B4 | fig11 |
| Shift temporel | avant/après × bloc (Mann-Whitney) | fig12 |
| Zoom Centre | évolution Centre | fig13 |
| Volume vs stance | Centre | fig14 |
| Twitter vs AN | Centre | fig15 |
| Attrition diff. | profil des sortants | fig16 |
| Heatmap volume | bloc × mois | fig17 |
| Mann-Kendall | tendance par bloc | fig18 |

**CSV produits** : `stance_mensuel.csv`, `event_impact_diff_in_diff.csv`, `mann_kendall_bloc.csv`

### 7.4 NB04 — Polarisation lexicale

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Distance cosinus | G. radicale – Droite (TF-IDF) | fig18–20 |
| Fighting words | log-odds (Monroe 2008) | fig21–22 |
| Diffusion « cessez-le-feu » | % par bloc × mois | fig24 |
| Lag adoption | mois premier 10 % | fig25 |
| Indice polarisation | agrégé | fig26 |

**CSV produits** : `cosine_distance_mensuelle.csv`, `fighting_words.csv`, `ceasefire_lexical.csv`, `polarisation_index.csv`

### 7.5 NB05 — Événements pivot

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Variables batch | condemns_hamas, genocide_framing, etc. | fig28 |
| Cessez-le-feu par batch | conditionnalité | fig29–30 |
| Régression | stance ~ bloc × batch + cadres | fig31 |
| ANOVA | effets bloc, batch, interaction | fig32 |

**CSV produits** : `variables_batch_specifiques.csv`, `ceasefire_call_batch_bloc.csv`, `anova_*.csv`

### 7.6 NB06 — Convergence transpartisane

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Convergence batch | % textes « cessez-le-feu » par bloc × batch | fig33 |
| Movers | députés à trajectoire variable | fig35 |
| PCA | projection députés PC1–PC2 | fig38 |

**CSV produits** : `convergence_batch_bloc.csv`

### 7.7 NB07 — Émotions et registres

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Registre émotionnel | v4 | fig40+ |

**CSV** : `emotional_register_v4.csv`

### 7.8 NB08 — Analyses de fond

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Sensibilité corpus | sous-échantillonnage stratifié (n_min par bloc) | fig48 |
| Panel B4 vs complet | ribbon comparatif | fig49 |
| Limites | 4 blocs vs 5, biais Panel B4, pas de causalité | Synthèse |

### 7.9 NB09 — Engagement Twitter (optionnel)

| Étape | Contenu | Figure / Fichier |
|-------|---------|------------------|
| Engagement | retweets, likes, replies (si colonnes présentes) | Selon données |
| Radicalité vs engagement | corrélation | — |

---

## 8. Event studies (shift temporel)

**Design** : pas de diff-in-diff classique (pas de groupe contrôle, pas de tendances parallèles testées). Analyse descriptive de type « avant/après » :

- Fenêtre : 30 jours avant / 30 jours après chaque événement
- Test : Mann-Whitney U entre les deux périodes, par bloc
- Résultats : delta stance (post − pré), p-value

**Événements** : CIJ, Rafah, Sinwar, Mandats CPI, Cessez-le-feu, Rupture CLF.

---

## 9. Validation humaine (optionnelle)

### 9.1 Échantillonnage

```bash
python src/validation_humaine.py
```

- 150 textes stratifiés par bloc (40 par bloc si possible)
- Export : `data/validation/sample_150.csv` (colonnes : id, text, bloc — sans stance)

### 9.2 Annotation manuelle

- Annoter chaque texte sur l’échelle -2 à +2 (manuel ou avec un collègue)
- Sauvegarder : `data/validation/annotations.csv`

### 9.3 Métriques

```bash
python src/validation_metrics.py
```

- Cohen’s Kappa (accord inter-annotateurs)
- Spearman ρ (humain vs annotation de référence)

---

## 10. Limites

| Limite | Description |
|--------|-------------|
| Validation | Pas de validation humaine systématique ; scores = proxy |
| Déséquilibre | Gauche radicale ≈ 63 % du corpus |
| Panel B4 | Biais de sélection (députés les plus actifs) |
| Causalité | Aucune inférence causale stricte ; analyses associatives |
| Regroupement | LR + RN en « Droite » — perte de granularité |

---

## 11. Références

- Monroe, B. L. et al. (2008). *Fighting with Words*. *American Political Science Review*.
- Échelle de stance : conception ad hoc pour le conflit israélo-palestinien.
