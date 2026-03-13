# Rapport de validation - Analyse discursive Assemblée nationale

**Objectif** : Document exhaustif pour permettre à un agent de valider l'intégrité des analyses et des résultats chiffrés.

**Auteur** : Sami Nakib  
**Date** : février 2026  
**Dossier projet** : `fr_assemblee_discourse_analysis` (anciennement `gaza_discourse_analysis`)

---

## 1. Structure attendue

### 1.1 Arborescence

```
fr_assemblee_discourse_analysis/
├── data/results/          # 26 fichiers CSV
├── notebooks/             # 3 notebooks (01, 02, 03)
├── src/
├── docs/
└── reports/figures/
```

### 1.2 Notebooks actifs (sans doublon)

| Fichier | Contenu |
|---------|---------|
| `01_corpus_validation.ipynb` | Validation corpus, accord LLM, biais |
| `02_framing_lexique_emotions.ipynb` | Framing, stance, polarisation, émotions |
| `03_evenements_convergence.ipynb` | Impact événements, convergence |

**Vérification** : Aucun doublon (01_validation_corpus, 02_cadres_lexique_emotions, 03_impact_evenements_convergence, 03_event_impact_convergence, etc. doivent être absents).

---

## 2. Résultats chiffrés - Tables de référence

### 2.1 vue_ensemble.csv

| bloc | n_textes | pct_corpus | n_deputes | stance_v3_moyen | stance_v3_std |
|------|----------|------------|-----------|-----------------|---------------|
| Gauche radicale | 6838 | 63.47 | 138 | 1.574 | 0.849 |
| Gauche moderee | 971 | 9.01 | 67 | 0.926 | 0.950 |
| Centre / Majorite | 1489 | 13.82 | 130 | -0.769 | 0.950 |
| Droite | 1476 | 13.70 | 124 | -1.378 | 0.730 |

**Somme n_textes** : 10774  
**Somme n_deputes** : 459

### 2.2 accord_v3_v4.csv

| n_textes_communs | spearman_rho | p_value | accord_exact_pct | accord_a_1pt_pres_pct |
|------------------|--------------|---------|------------------|------------------------|
| 5905 | 0.8599 | 0.0 | 61.59 | 95.33 |

### 2.3 coherence_v4.csv

| check | valeur |
|-------|--------|
| ceasefire_type non-null & call=False | 0.0 |
| stance_v4=-2 & ceasefire_call=True | 1.0 |
| textes avec flags d'incohérence | 0.0 |
| neutral+absolute (incohérence potentielle) | 96 |
| accord_frame_v3_v4_pct | 60.23 |

### 2.4 panel_b4_composition.csv

| bloc | n_deputes_total | n_deputes_panel | pct_deputes_panel | n_textes_panel |
|------|-----------------|-----------------|-------------------|----------------|
| Gauche radicale | 138 | 42 | 30.4 | 6069 |
| Gauche moderee | 67 | 9 | 13.4 | 615 |
| Centre / Majorite | 130 | 10 | 7.7 | 723 |
| Droite | 124 | 15 | 12.1 | 848 |

**Total panel** : 76 députés, 8255 textes

### 2.5 attrition_mensuelle.csv - Extrait

| month | n_deputes_actifs | n_textes |
|-------|------------------|----------|
| 2023-10 | 211 | 1353 |
| 2023-11 | 148 | 601 |
| 2024-05 | 130 | 867 |
| 2024-12 | 45 | 134 |
| 2025-06 | 137 | 822 |
| 2026-01 | 34 | 86 |

**Somme n_textes** : doit être cohérente avec 10774 (ou corpus filtré).

### 2.6 stance_mensuel.csv - Extrait (oct. 2023)

| month | bloc | stance_mean | n |
|-------|------|-------------|---|
| 2023-10 | Gauche radicale | 1.265 | 645 |
| 2023-10 | Gauche moderee | 0.647 | 153 |
| 2023-10 | Centre / Majorite | -0.898 | 255 |
| 2023-10 | Droite | -1.447 | 300 |

### 2.7 cosine_distance_mensuelle.csv - Paire G.rad ↔ Droite

| month | cosine_dist (G.rad ↔ Droite) |
|-------|------------------------------|
| 2023-10 | 0.690 |
| 2023-12 | 0.896 |
| 2025-06 | 0.786 |
| 2026-01 | 0.922 |

**Plage** : 0.64 à 0.99

### 2.8 polarisation_index.csv - Extrait

| month_ts | variance_inter_blocs | cosine_dist_mean |
|----------|----------------------|------------------|
| 2023-10-01 | 1.624 | 0.671 |
| 2024-12-01 | 1.652 | 0.934 |
| 2025-06-01 | 1.875 | 0.751 |
| 2026-01-01 | 1.799 | 0.969 |

### 2.9 event_impact_diff_in_diff.csv - Stance (p < 0.05)

| event | date | bloc | variable | delta | p_mannwhitney | sig |
|-------|------|------|----------|-------|---------------|-----|
| Ordonnance CIJ | 2024-01-26 | Centre / Majorite | stance_v3 | -0.4356 | 0.0179 | * |
| Offensive Rafah | 2024-05-28 | Gauche radicale | stance_v3 | 0.2047 | 0.0009 | ** |
| Offensive Rafah | 2024-05-28 | Centre / Majorite | stance_v3 | 0.4037 | 0.0075 | ** |
| Cessez-le-feu | 2025-01-19 | Centre / Majorite | stance_v3 | -0.6697 | 0.0049 | ** |
| Cessez-le-feu | 2025-01-19 | Droite | stance_v3 | -1.1039 | 0.045 | * |
| Rupture CLF | 2025-03-15 | Centre / Majorite | stance_v3 | -0.9167 | 0.0048 | ** |

### 2.10 event_impact_diff_in_diff.csv - ceasefire_lexical (p < 0.05)

| event | bloc | delta | p_mannwhitney | sig |
|-------|------|-------|---------------|-----|
| Offensive Rafah | Centre / Majorite | 19.67 | 0.0051 | ** |
| Mort Sinwar | Gauche radicale | -24.91 | < 0.001 | ** |
| Rupture CLF | Centre / Majorite | -24.44 | 0.0317 | * |

### 2.11 convergence_batch_bloc.csv

| batch | variable | bloc | pct |
|-------|----------|------|-----|
| NEW_OFFENSIVE | transpartisan_convergence | Gauche radicale | 6.9 |
| NEW_OFFENSIVE | transpartisan_convergence | Gauche moderee | 35.5 |
| NEW_OFFENSIVE | transpartisan_convergence | Centre / Majorite | 30.3 |
| NEW_OFFENSIVE | transpartisan_convergence | Droite | 3.5 |

### 2.12 ceasefire_call_v4.csv - Extrait

| batch | bloc | pct_ceasefire_v4 | n |
|-------|------|------------------|---|
| CHOC | Gauche radicale | 36.63 | 789 |
| CHOC | Gauche moderee | 41.76 | 182 |
| CHOC | Centre / Majorite | 3.48 | 287 |
| CHOC | Droite | 0.57 | 352 |
| NEW_OFFENSIVE | Gauche radicale | 7.64 | 1087 |
| NEW_OFFENSIVE | Centre / Majorite | 11.36 | 264 |

### 2.13 rapport_synthese.csv

| bloc | delta_stance | mk_tau | mk_p | clf_lex_pct_debut | clf_lex_pct_fin |
|------|--------------|--------|------|-------------------|-----------------|
| Gauche radicale | -0.0596 | 0.1905 | 0.1607 | 26.51 | 6.85 |
| Gauche moderee | -1.6471 | -0.1905 | 0.1605 | 27.45 | 0.0 |
| Centre / Majorite | 0.148 | 0.0899 | 0.5144 | 3.14 | 0.0 |
| Droite | -0.5533 | -0.1138 | 0.4066 | 2.67 | 0.0 |

### 2.14 frames_par_bloc.csv - Top frame par bloc (v3)

| bloc | frame | pct |
|------|-------|-----|
| Gauche radicale | HUM | 77.22 |
| Gauche moderee | HUM | 64.05 |
| Centre / Majorite | SEC | 30.58 |
| Droite | SEC | 44.81 |

### 2.15 emotional_register.csv - Top registre par bloc

| bloc | register | pct |
|------|----------|-----|
| Gauche radicale | indignation | 63.66 |
| Gauche moderee | indignation | 37.14 |
| Centre / Majorite | neutral | 43.95 |
| Droite | defiance | 41.18 |

### 2.16 conditionality.csv - Top par bloc

| bloc | conditionality | pct |
|------|---------------|-----|
| Gauche radicale | absolute | 74.29 |
| Gauche moderee | balanced | 58.15 |
| Centre / Majorite | balanced | 49.62 |
| Droite | absolute | 86.59 |

### 2.17 engagement_bloc_stance.csv - Extrait

| bloc | stance_v3 | n | engagement_median |
|------|-----------|---|-------------------|
| Gauche radicale | 2 | 4643 | 411 |
| Gauche radicale | -2 | 90 | 379 |
| Centre / Majorite | -1 | 560 | 70.5 |
| Droite | -2 | 563 | 98 |

### 2.18 ceasefire_lexical_v3.csv - Oct. 2023

| month | bloc | pct_ceasefire | n |
|-------|------|---------------|---|
| 2023-10 | Gauche radicale | 26.51 | 645 |
| 2023-10 | Gauche moderee | 27.45 | 153 |
| 2023-10 | Centre / Majorite | 3.14 | 255 |
| 2023-10 | Droite | 2.67 | 300 |

### 2.19 fighting_words.csv - Top 10 (Gauche vs Droite CHOC)

| word | z | count1 | count2 |
|------|---|--------|--------|
| gaza | 5.65 | 846 | 45 |
| cessez-le-feu | 4.47 | 370 | 5 |
| paix | 3.60 | 417 | 29 |
| palestinien | 3.34 | 557 | 59 |
| guerre | 3.12 | 346 | 27 |
| international | 3.11 | 327 | 24 |
| israélien | 2.80 | 502 | 62 |
| bombardement | 2.65 | 127 | 1 |
| immédiat | 2.64 | 149 | 4 |
| crime | 2.63 | 234 | 17 |

### 2.20 volume_mensuel.csv - Extrait

| month | bloc | n_textes |
|-------|------|----------|
| 2023-10 | Gauche radicale | 645 |
| 2023-10 | Gauche moderee | 153 |
| 2023-10 | Centre / Majorite | 255 |
| 2023-10 | Droite | 300 |

**Somme 2023-10** : 1353

### 2.21 arc_narratif.csv

| batch | variable | Gauche radicale | Gauche moderee | Centre / Majorite | Droite |
|-------|----------|-----------------|----------------|-------------------|--------|
| CHOC | condemns_hamas_attack | 11% | 23% | 57% | 67% |
| POST_CIJ | icj_reference | 39% | 17% | 0% | 0% |
| RAFAH | icc_mention | 29% | 21% | 9% | 1% |
| POST_SINWAR | ethnic_cleansing_frame | 53% | 29% | 0% | 0% |
| NEW_OFFENSIVE | transpartisan_convergence | 7% | 36% | 30% | 4% |

### 2.22 variables_batch_specifiques.csv - Extrait

| batch | variable | bloc | pct |
|-------|----------|------|-----|
| CHOC | condemns_hamas_attack | Gauche radicale | 11.4 |
| CHOC | condemns_hamas_attack | Droite | 67.2 |
| CHOC | proportionality_issue | Gauche radicale | 30.0 |
| CHOC | proportionality_issue | Droite | 0.6 |

### 2.23 ceasefire_type.csv - Extrait

| batch | bloc | ceasefire_type | n |
|-------|------|----------------|---|
| CHOC | Gauche radicale | unconditional | 280 |
| CHOC | Gauche moderee | unconditional | 70 |
| CHOC | Centre / Majorite | humanitarian_pause | 8 |

---

## 3. Checklist de validation

### 3.1 Fichiers

- [ ] `data/results/` contient 26 fichiers CSV
- [ ] Aucun fichier `*_validation_corpus`, `*_cadres_lexique_emotions`, `*_impact_evenements_convergence`, `*_event_impact_convergence` dans notebooks/
- [ ] Dossier projet nommé `fr_assemblee_discourse_analysis`

### 3.2 Cohérence numérique

- [ ] `vue_ensemble` : somme n_textes = 10774
- [ ] `accord_v3_v4` : spearman_rho ≈ 0.86
- [ ] `panel_b4_composition` : somme n_deputes_panel = 76
- [ ] `convergence_batch_bloc` : NEW_OFFENSIVE G.mod = 35.5, Centre = 30.3

### 3.3 Notebooks

- [ ] 01_corpus_validation.ipynb s'exécute sans erreur
- [ ] 02_framing_lexique_emotions.ipynb s'exécute sans erreur
- [ ] 03_evenements_convergence.ipynb s'exécute sans erreur
- [ ] Chemins : RESULTS_DIR = data/results, FIG_DIR = reports/figures

### 3.4 Config

- [ ] `src/config.py` : RESULTS_DIR = DATA_DIR / "results"
- [ ] `src/config.py` : BLOC_ORDER = ["Gauche radicale", "Gauche moderee", "Centre / Majorite", "Droite"]

---

## 4. Synthèse pour validation

| Indicateur | Valeur attendue |
|------------|-----------------|
| Corpus total | 10 774 textes |
| Députés | 459 |
| Accord LLM v3/v4 | ρ = 0,86 |
| Panel B4 | 76 députés |
| Distance cosinus G.rad↔Droite | 0,69–0,92 |
| Convergence NEW_OFFENSIVE (G.mod) | 35,5 % |
| Convergence NEW_OFFENSIVE (Centre) | 30,3 % |
| Événements sig. (stance) | 6 (CIJ, Rafah×2, CF×2, Rupture) |
| Événements sig. (ceasefire_lexical) | 3 (Rafah, Sinwar, Rupture) |

---

## 5. Fichiers CSV complets (liste)

| Fichier | Lignes (approx) | Colonnes clés |
|---------|-----------------|---------------|
| vue_ensemble.csv | 5 | bloc, n_textes, stance_v3_moyen |
| accord_v3_v4.csv | 2 | spearman_rho, accord_exact_pct |
| coherence_v4.csv | 6 | check, valeur |
| attrition_mensuelle.csv | 29 | month, n_deputes_actifs, n_textes |
| volume_mensuel.csv | 114 | month, bloc, n_textes |
| stance_mensuel.csv | 114 | month, bloc, stance_mean, n |
| cosine_distance_mensuelle.csv | 150 | month, bloc1, bloc2, cosine_dist |
| cosine_distance_3paires.csv | 164 | idem |
| polarisation_index.csv | 29 | month_ts, variance_inter_blocs, cosine_dist_mean |
| event_impact_diff_in_diff.csv | 46 | event, bloc, variable, delta, p_mannwhitney, sig |
| convergence_batch_bloc.csv | 5 | batch, variable, bloc, pct |
| ceasefire_lexical_v3.csv | 114 | month, bloc, pct_ceasefire, n |
| ceasefire_call_v4.csv | 28 | batch, bloc, pct_ceasefire_v4, n |
| ceasefire_call_batch_bloc.csv | 28 | idem |
| ceasefire_type.csv | 43 | batch, bloc, ceasefire_type, n |
| frames_par_bloc.csv | 86 | version, bloc, frame, pct |
| emotional_register.csv | 31 | bloc, register, pct |
| emotional_register_v4.csv | 28 | batch, bloc, register, pct |
| conditionality.csv | 17 | bloc, conditionality, pct |
| rapport_synthese.csv | 5 | bloc, delta_stance, mk_tau, mk_p |
| panel_b4.csv | variable | députés, textes |
| panel_b4_composition.csv | 5 | bloc, n_deputes_panel, n_textes_panel |
| arc_narratif.csv | 8 | batch, variable, blocs |
| variables_batch_specifiques.csv | 74 | batch, variable, bloc, pct |
| fighting_words.csv | 18613 | word, z, count1, count2, comparison |
| engagement_bloc_stance.csv | 21 | bloc, stance_v3, n, engagement_median |

---

*Fin du rapport de validation.*
