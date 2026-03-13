# Compte rendu exhaustif - Analyse discursive Assemblée nationale

**Auteur : Sami Nakib**  
**Date : février 2026**

*Document de synthèse des résultats chiffrés. Posture académique et descriptive.*

---

## 1. État du projet

### 1.1 Structure actuelle

| Composant | État | Détail |
|-----------|------|--------|
| **Données** | ⚠️ | 39 CSV visibles dans `data/results/` ; `corpus_v3.parquet` et `corpus_v4.parquet` sont attendus dans `data/processed/` mais peuvent être absents du repo cloné |
| **Notebooks** | ✅ | 4 notebooks (01, 02, 03, 04) + scripts analyses_supplementaires, build_analyses_extended |
| **Code source** | ✅ | `src/config.py`, `src/prepare_data.py`, `src/analyses_supplementaires.py`, `src/build_analyses_extended.py` |
| **Figures** | ⚠️ | documentation des figures dans `reports/figures/`, mais présence effective des PNG à vérifier selon l'état local du workspace |
| **Documentation** | ✅ | README, data/README, notebooks/README |

### 1.2 Fichiers de résultats (data/results/)

| Fichier | Description |
|---------|-------------|
| `vue_ensemble.csv` | Vue d'ensemble par bloc (n_textes, stance, etc.) |
| `accord_v3_v4.csv` | Accord Spearman entre annotations v3 et v4 |
| `coherence_v4.csv` | Cohérence du corpus v4 |
| `attrition_mensuelle.csv` | Députés actifs et textes par mois |
| `volume_mensuel.csv` | Volume par bloc et mois |
| `stance_mensuel.csv` | Stance moyen mensuel par bloc |
| `cosine_distance_mensuelle.csv` | Distance lexicale entre paires de blocs |
| `cosine_distance_3paires.csv` | Sous-ensemble de paires clés |
| `polarisation_index.csv` | Indice de polarisation mensuel |
| `event_impact_diff_in_diff.csv` | Comparaisons événementielles avant/après par bloc |
| `convergence_batch_bloc.csv` | Convergence transpartisane par batch |
| `ceasefire_lexical_v3.csv` | Adoption lexicale du cessez-le-feu (v3) |
| `ceasefire_call_v4.csv` | Appel explicite au cessez-le-feu (v4) |
| `ceasefire_call_batch_bloc.csv` | % cessez-le-feu par batch et bloc |
| `frames_par_bloc.csv` | Répartition des cadres (HUM, LEG, SEC, etc.) |
| `emotional_register.csv` | Registres émotionnels par bloc |
| `conditionality.csv` | Conditionnalité du discours |
| `rapport_synthese.csv` | Synthèse par bloc (delta stance, Mann-Kendall) |
| `panel_b4.csv` | Panel fixe B4 |
| `panel_b4_composition.csv` | Composition du panel B4 |
| `arc_narratif.csv` | Arc narratif |
| `variables_batch_specifiques.csv` | Variables par batch |
| `fighting_words.csv` | Mots discriminants |
| `engagement_bloc_stance.csv` | Engagement par bloc et stance |
| `twitter_vs_an.csv` | Régression Twitter vs AN (analyses_supplementaires) |
| `droite_stance_par_batch.csv` | Stance Droite par batch |
| `droite_stance_mensuel.csv` | Stance mensuel Droite |
| `stance_par_groupe.csv` | Stance par groupe politique |
| `stance_panel_vs_complet.csv` | Comparaison panel B4 vs corpus complet |
| `trajectoires_individuelles.csv` | Profils individuels députés |
| `variance_intra_bloc.csv` | Variance et % movers par bloc |
| `movers_top20.csv` | Top 20 députés à amplitude stance maximale |
| `coherence_twitter_an_par_depute.csv` | Cohérence inter-arène par député |
| `target_primary_par_bloc.csv` | Cibles primaires par bloc |
| `target_primary_par_batch_bloc.csv` | Cibles par batch et bloc |
| `key_demands_par_batch_bloc.csv` | Demandes clés par batch |
| `conditionality_par_batch_bloc.csv` | Conditionnalité par batch et bloc |
| `ceasefire_type.csv` | Type de cessez-le-feu (unconditional, conditional, etc.) |

---

## 2. Résultats chiffrés exhaustifs

### 2.1 Corpus - Vue d'ensemble (vue_ensemble.csv)

| Bloc | Textes | % corpus | Députés | Textes/député | Twitter | AN | Ratio TW/AN | Stance v3 moy | Stance v3 std | Confiance moy | Engagement médian TW |
|------|--------|---------|---------|---------------|---------|-----|-------------|---------------|---------------|---------------|----------------------|
| Gauche radicale | 6 838 | 63,47 % | 138 | 49,6 | 6 227 | 611 | 10,19 | 1,574 | 0,849 | 0,924 | 372 |
| Gauche modérée | 971 | 9,01 % | 67 | 14,5 | 814 | 157 | 5,18 | 0,926 | 0,950 | 0,88 | 113,5 |
| Centre / Majorité | 1 489 | 13,82 % | 130 | 11,5 | 944 | 545 | 1,73 | -0,769 | 0,950 | 0,868 | 61,5 |
| Droite | 1 476 | 13,70 % | 124 | 11,9 | 1 150 | 326 | 3,53 | -1,378 | 0,730 | 0,897 | 63,0 |

**Total : 10 774 textes**, 459 députés, période oct. 2023 - jan. 2026.

### 2.2 Validation LLM (accord_v3_v4.csv)

| Métrique | Valeur |
|----------|--------|
| Textes communs v3/v4 | 5 905 |
| **Spearman ρ** | **0,8599** |
| p-value | < 0,001 |
| Accord exact (même score) | 61,59 % |
| Accord à ±1 point | 95,33 % |

### 2.3 Cohérence v4 (coherence_v4.csv)

| Check | Valeur |
|-------|--------|
| ceasefire_type non-null & call=False | 0,0 |
| stance_v4=-2 & ceasefire_call=True | 1,0 |
| Textes avec flags d'incohérence | 0,0 |
| neutral+absolute (incohérence potentielle) | 96 |
| **Accord frame v3/v4** | **60,23 %** |

### 2.4 Panel B4 (panel_b4_composition.csv)

| Bloc | Députés total | Députés panel | % panel | Textes panel |
|------|---------------|---------------|---------|--------------|
| Gauche radicale | 138 | 42 | 30,4 % | 6 069 |
| Gauche modérée | 67 | 9 | 13,4 % | 615 |
| Centre / Majorité | 130 | 10 | 7,7 % | 723 |
| Droite | 124 | 15 | 12,1 % | 848 |

**Biais :** 75 % des députés du panel sont Gauche radicale (42/76).

### 2.5 Attrition mensuelle (attrition_mensuelle.csv) – exhaustif

| Mois | Députés actifs | Textes | Mois | Députés actifs | Textes |
|------|----------------|--------|------|----------------|--------|
| 2023-10 | 211 | 1 353 | 2025-01 | 96 | 319 |
| 2023-11 | 148 | 601 | 2025-02 | 70 | 175 |
| 2023-12 | 55 | 199 | 2025-03 | 87 | 257 |
| 2024-01 | 91 | 352 | 2025-04 | 64 | 294 |
| 2024-02 | 95 | 377 | 2025-05 | 124 | 555 |
| 2024-03 | 103 | 407 | 2025-06 | 137 | 822 |
| 2024-04 | 104 | 494 | 2025-07 | 109 | 490 |
| 2024-05 | 130 | 867 | 2025-08 | 49 | 183 |
| 2024-06 | 79 | 227 | 2025-09 | 85 | 468 |
| 2024-07 | 64 | 244 | 2025-10 | 87 | 367 |
| 2024-08 | 59 | 184 | 2025-11 | 60 | 147 |
| 2024-09 | 57 | 280 | 2025-12 | 52 | 137 |
| 2024-10 | 116 | 435 | 2026-01 | 34 | 86 |
| 2024-11 | 87 | 320 | | | |
| 2024-12 | 45 | 134 | | | |

### 2.6 Polarisation lexicale - Distance cosinus (cosine_distance_mensuelle.csv)

*Données complètes : 6 paires × 28 mois (168 lignes).*

**Paire Gauche radicale ↔ Droite :** oct. 2023: 0,69 ; déc. 2023: 0,90 ; janv. 2025: 0,87 ; juin 2025: 0,79 ; janv. 2026: 0,92.

**Toutes paires, mois clés :**

| Mois | GR↔Gmod | GR↔Centre | GR↔Droite | Gmod↔Centre | Gmod↔Droite | Centre↔Droite |
|------|---------|-----------|-----------|-------------|-------------|---------------|
| 2023-10 | 0,65 | 0,66 | 0,69 | 0,68 | 0,71 | 0,64 |
| 2024-12 | 0,88 | 0,95 | 0,91 | 0,97 | 0,94 | 0,95 |
| 2025-06 | 0,73 | 0,74 | 0,79 | 0,73 | 0,79 | 0,73 |
| 2026-01 | 0,98 | 0,97 | 0,92 | 0,98 | 0,99 | 0,97 |

**Plage globale :** 0,64 (oct. 2023, Centre↔Droite) à 0,99 (janv. 2026, G.mod↔Droite).

### 2.7 Indice de polarisation (polarisation_index.csv) – exhaustif

| Mois | Variance inter-blocs | Distance cosinus moy | Mois | Variance inter-blocs | Distance cosinus moy |
|------|----------------------|----------------------|------|----------------------|----------------------|
| 2023-10 | 1,62 | 0,67 | 2024-11 | 2,03 | 0,86 |
| 2023-11 | 1,46 | 0,85 | 2024-12 | 1,65 | 0,93 |
| 2023-12 | 1,34 | 0,90 | 2025-01 | 1,23 | 0,84 |
| 2024-01 | 2,33 | 0,86 | 2025-02 | 1,94 | 0,90 |
| 2024-02 | 2,14 | 0,86 | 2025-03 | 1,84 | 0,88 |
| 2024-03 | 2,44 | 0,85 | 2025-04 | 2,04 | 0,90 |
| 2024-04 | 1,83 | 0,87 | 2025-05 | 1,89 | 0,82 |
| 2024-05 | 2,33 | 0,82 | 2025-06 | 1,87 | 0,75 |
| 2024-06 | 1,95 | 0,88 | 2025-07 | 2,41 | 0,87 |
| 2024-07 | 2,35 | 0,90 | 2025-08 | 2,88 | 0,92 |
| 2024-08 | 2,14 | 0,90 | 2025-09 | 1,76 | 0,87 |
| 2024-09 | 2,20 | 0,91 | 2025-10 | 1,67 | 0,86 |
| 2024-10 | 1,96 | 0,84 | 2025-11 | 1,85 | 0,91 |
| | | | 2025-12 | 1,82 | 0,92 |
| | | | 2026-01 | 1,80 | **0,97** |

### 2.8 Impact des événements - Comparaisons avant/après (event_impact_diff_in_diff.csv)

**Stance (variable : stance_v3)**

| Événement | Date | Bloc | Δ stance | p (Mann-Whitney) | Sig |
|-----------|------|------|----------|------------------|-----|
| Ordonnance CIJ | 2024-01-26 | Centre / Majorité | **-0,44** | 0,018 | * |
| Offensive Rafah | 2024-05-28 | Gauche radicale | +0,20 | 0,0009 | ** |
| Offensive Rafah | 2024-05-28 | Centre / Majorité | **+0,40** | 0,0075 | ** |
| Cessez-le-feu | 2025-01-19 | Centre / Majorité | -0,67 | 0,0049 | ** |
| Cessez-le-feu | 2025-01-19 | Droite | -1,10 | 0,045 | * |
| Rupture CLF | 2025-03-15 | Centre / Majorité | -0,92 | 0,0048 | ** |

**Cessez-le-feu lexical (ceasefire_lexical)**

| Événement | Bloc | Δ % | p | Sig |
|-----------|------|-----|---|-----|
| Offensive Rafah | Centre / Majorité | +19,7 pp | 0,0051 | ** |
| Mort Sinwar | Gauche radicale | -24,9 pp | < 0,001 | ** |
| Rupture CLF | Centre / Majorité | -24,4 pp | 0,0317 | * |

### 2.9 Convergence transpartisane (convergence_batch_bloc.csv)

**Batch NEW_OFFENSIVE (mi-2025) - % convergence transpartisane :**

| Bloc | % |
|------|---|
| Gauche radicale | 6,9 % |
| Gauche modérée | **35,5 %** |
| Centre / Majorité | **30,3 %** |
| Droite | 3,5 % |

### 2.10 Adoption du cessez-le-feu par batch (ceasefire_call_batch_bloc.csv)

| Batch | G. radicale | G. modérée | Centre | Droite |
|-------|-------------|------------|--------|--------|
| CHOC | 36,6 % (289/789) | 41,8 % (76/182) | 3,5 % (10/287) | 0,6 % (2/352) |
| POST_CIJ | 35,0 % (76/217) | 52,2 % (24/46) | 10,9 % (6/55) | 3,1 % (1/32) |
| RAFAH | 16,0 % (107/670) | 17,9 % (19/106) | 14,6 % (19/130) | 4,2 % (3/71) |
| POST_SINWAR | 11,0 % (17/154) | 0,0 % (0/7) | 15,2 % (5/33) | 2,3 % (1/43) |
| MANDATS_CPI | 5,8 % (13/226) | 9,7 % (3/31) | 12,5 % (2/16) | 11,1 % (4/36) |
| CEASEFIRE_BREACH | 12,2 % (54/443) | 11,9 % (7/59) | 10,6 % (14/132) | 0,0 % (0/117) |
| NEW_OFFENSIVE | 7,6 % (83/1087) | 12,4 % (15/121) | 11,4 % (30/264) | 0,0 % (0/199) |

### 2.11 Synthèse longitudinale (rapport_synthese.csv)

| Bloc | Δ stance | Mann-Kendall τ | p | Tendance | clf_lex début | clf_lex fin |
|------|----------|----------------|---|----------|---------------|-------------|
| Gauche radicale | -0,06 | 0,19 | 0,16 | no trend | 26,5 % | 6,9 % |
| Gauche modérée | -1,65 | -0,19 | 0,16 | no trend | 27,5 % | 0,0 % |
| Centre / Majorité | +0,15 | 0,09 | 0,51 | no trend | 3,1 % | 0,0 % |
| Droite | -0,55 | -0,11 | 0,41 | no trend | 2,7 % | 0,0 % |

### 2.12 Cadres discursifs (frames_par_bloc.csv) - Top 3 par bloc

| Bloc | Frame 1 | Frame 2 | Frame 3 |
|------|---------|---------|---------|
| Gauche radicale | HUM 77,2 % | LEG 9,5 % | MOR 8,1 % |
| Gauche modérée | HUM 64,1 % | LEG 15,5 % | MOR 8,9 % |
| Centre / Majorité | SEC 30,6 % | HUM 29,1 % | MOR 20,9 % |
| Droite | SEC 44,8 % | MOR 34,1 % | HUM 11,1 % |

*HUM = humanitaire, LEG = légal, MOR = moral, SEC = sécurité, DIP = diplomatique*

### 2.13 Registres émotionnels (emotional_register.csv) – exhaustif

| Bloc | indignation | solidarity | neutral | grief | anger | defiance | fear |
|------|-------------|------------|---------|-------|-------|----------|------|
| Gauche radicale | 63,7 % | 12,5 % | 11,4 % | 7,4 % | 4,1 % | 0,8 % | 0,2 % |
| Gauche modérée | 37,1 % | 13,4 % | 29,9 % | 17,8 % | 1,1 % | 0,2 % | 0,5 % |
| Centre / Majorité | 26,7 % | 5,5 % | 44,0 % | 10,9 % | 0,1 % | 9,4 % | 3,3 % |
| Droite | 36,5 % | 2,6 % | 11,5 % | 2,9 % | 1,5 % | 41,2 % | 3,8 % |

### 2.14 Conditionnalité (conditionality.csv) – exhaustif

| Bloc | absolute | balanced | conditional | neutral |
|------|----------|----------|--------------|---------|
| Gauche radicale | 74,3 % | 24,7 % | 0,5 % | 0,5 % |
| Gauche modérée | 39,5 % | 58,2 % | 2,0 % | 0,4 % |
| Centre / Majorité | 46,0 % | 49,6 % | 3,2 % | 1,2 % |
| Droite | 86,6 % | 12,8 % | 0,4 % | 0,2 % |

### 2.15 Panel B4 vs corpus complet (stance_panel_vs_complet.csv)

| Bloc | Stance complet | Stance panel B4 | Δ | n_complet | n_panel |
|------|----------------|-----------------|---|-----------|---------|
| Gauche radicale | 1,574 | 1,633 | +0,059 | 6 838 | 5 549 |
| Gauche modérée | 0,926 | 0,965 | +0,039 | 971 | 402 |
| Centre / Majorité | -0,769 | -1,158 | **-0,389** | 1 489 | 475 |
| Droite | -1,378 | -1,543 | -0,165 | 1 476 | 427 |

**Le panel B4 biaise le Centre vers des positions plus pro-israéliennes** (Δ = -0,39).

### 2.16 Stance Droite par batch (droite_stance_par_batch.csv)

| Batch | Stance moyen | Écart-type | n |
|-------|-------------|------------|---|
| CHOC | -1,42 | 0,70 | 352 |
| POST_CIJ | -1,31 | 0,69 | 32 |
| RAFAH | -1,55 | 0,67 | 71 |
| POST_SINWAR | -0,88 | 1,20 | 43 |
| MANDATS_CPI | -1,00 | 1,04 | 36 |
| CEASEFIRE_BREACH | -1,34 | 0,84 | 117 |
| NEW_OFFENSIVE | -1,45 | 0,61 | 199 |

### 2.17 Twitter vs AN – régression (twitter_vs_an.csv)

| Coefficient arena Twitter | p-value |
|---------------------------|---------|
| -0,023 | 0,336 |

*Contrôlant le bloc et le mois, l’arène Twitter n’a pas d’effet significatif sur le stance.*

### 2.18 Variance intra-bloc et movers (variance_intra_bloc.csv)

| Bloc | Députés | Stance moyen | Écart-type | % movers |
|------|---------|--------------|------------|----------|
| Gauche radicale | 162 | 1,19 | 0,79 | 52,5 % |
| Gauche modérée | 73 | 0,59 | 0,71 | 38,4 % |
| Centre / Majorité | 141 | -0,61 | 0,67 | 41,1 % |
| Droite | 125 | -1,19 | 0,57 | 30,4 % |

### 2.19 Engagement par bloc et stance (engagement_bloc_stance.csv)

| Bloc | stance -2 | stance -1 | stance 0 | stance +1 | stance +2 |
|------|-----------|-----------|----------|-----------|-----------|
| Gauche radicale | n=90, méd=379 | n=166, méd=285 | n=116, méd=202 | n=1212, méd=250 | n=4643, méd=411 |
| Gauche modérée | n=9, méd=711 | n=89, méd=102 | n=66, méd=157 | n=441, méd=82 | n=209, méd=137 |
| Centre / Majorité | n=193, méd=142 | n=560, méd=71 | n=105, méd=20 | n=79, méd=18 | n=7, méd=26 |
| Droite | n=563, méd=98 | n=542, méd=50 | n=29, méd=32 | n=15, méd=11 | n=1, méd=153 |

*Les textes stance +2 (Gauche radicale) ont l’engagement médian le plus élevé (411).*

### 2.20 Variables par batch – extrait (variables_batch_specifiques.csv)

| Batch | Variable | G. radicale | G. modérée | Centre | Droite |
|-------|----------|-------------|------------|--------|--------|
| CHOC | condemns_hamas_attack | 11 % | 23 % | 57 % | 67 % |
| CHOC | proportionality_issue | 30 % | 31 % | 2 % | 1 % |
| POST_CIJ | icj_reference | 39 % | 17 % | 0 % | 0 % |
| RAFAH | icc_mention | 29 % | 21 % | 9 % | 1 % |
| POST_SINWAR | ethnic_cleansing_frame | 53 % | 29 % | 0 % | 0 % |
| NEW_OFFENSIVE | transpartisan_convergence | 7 % | 36 % | 30 % | 4 % |

### 2.21 Top cibles primaires par bloc (target_primary_par_bloc.csv – top 5)

| Bloc | Top 1 | Top 2 | Top 3 | Top 4 | Top 5 |
|------|-------|-------|-------|-------|-------|
| Gauche radicale | ISRAEL_GOV 25,3 % | ISRAEL 12,4 % | ISRAEL_ARMY 10,3 % | NETANYAHU 6,7 % | NETANYAHOU 4,4 % |
| Centre / Majorité | HAMAS 29,9 % | ISRAEL_GOV 9,3 % | ISRAEL 9,1 % | FRANCE_GOV 2,1 % | LFI 2,6 % |
| Droite | HAMAS 34,2 % | ISRAEL 9,8 % | LFI 8,7 % | MACRON 2,6 % | FRANCE_INSOUMISE 1,2 % |
| Gauche modérée | ISRAEL_GOV 28,3 % | ISRAEL_ARMY 8,9 % | ISRAEL 6,5 % | NETANYAHOU 4,0 % | FRANCE_GOV 6,5 % |

### 2.22 Type de cessez-le-feu (ceasefire_type.csv) – CHOC et NEW_OFFENSIVE

*CHOC :* G. radicale unconditional 280, humanitarian_pause 8 ; G. modérée unconditional 70, humanitarian_pause 6 ; Centre humanitarian_pause 8, unconditional 2 ; Droite unconditional 1, conditional_other 1.

*NEW_OFFENSIVE :* G. radicale unconditional 76, humanitarian_pause 1, conditional_other 1 ; Centre unconditional 23, conditional_other 3, humanitarian_pause 3 ; Droite 0 % ceasefire.

### 2.23 Cadres discursifs v4 (frames_par_bloc.csv – version v4)

| Bloc | Top 3 frames v4 |
|------|-----------------|
| Gauche radicale | HUM 64,4 %, DIP 18,0 %, IND 10,8 % |
| Gauche modérée | HUM 54,7 %, DIP 34,2 %, IND 4,2 % |
| Centre / Majorité | SEC 40,5 %, DIP 39,4 %, HUM 16,1 % |
| Droite | SEC 81,8 %, DIP 10,6 %, HUM 5,1 % |

### 2.24 Fighting words – Top 20 (Gauche vs Droite, CHOC)

gaza (z=5,66), cessez-le-feu (z=4,47), paix (z=3,60), palestinien (z=3,34), guerre (z=3,12), international (z=3,11), israélien (z=2,80), bombardement (z=2,65), immédiat (z=2,64), crime (z=2,63), génocide (z=2,56), gouvernement (z=2,54), droit (z=2,40), ethnique (z=2,36), humanitaire (z=2,34), onu (z=2,30), nettoyage (z=2,27), massacre (z=2,15), civil (z=2,14), sud (z=2,05).

### 2.25 Movers – Top 10 (movers_top20.csv)

Députés avec stance_range=4 (amplitude maximale) : Alma Dufour, Aurélien Saintoul, Aurélien Taché, Ayda Hadizadeh, Aymeric Caron, Carlos Martens Bilongo, Caroline Yadan, Danièle Obono, Edwige Diaz, Emmanuel Fernandes.

### 2.26 Chi² émotions (analyses_supplementaires B7)

Chi² = 2594,50, p < 0,001. Résidus standardisés notables : Droite × defiance r=34,5 ; Centre × neutral r=18,3 ; Gauche radicale × indignation r=10,1 ; Gauche radicale × solidarity r=4,6 ; Centre × defense r=3,0.

### 2.27 Données temporelles exhaustives

- **stance_mensuel.csv** : stance_mean, stance_std, n, se, ci95_lo, ci95_hi par bloc et mois (112 lignes).
- **volume_mensuel.csv** : n_textes par bloc et mois (112 lignes).
- **ceasefire_lexical_v3.csv** : pct_ceasefire par bloc et mois.

---

## 3. Synthèse des résultats clés

| Résultat | Chiffre |
|----------|---------|
| Corpus total | 10 774 textes, 459 députés |
| Accord LLM v3/v4 | ρ = 0,86 |
| Polarisation Gauche↔Droite | 0,69–0,92 (distance cosinus) |
| Centre - shift Rafah | +0,40 (p=0,008) |
| Centre - shift CIJ | -0,44 (p=0,018) |
| Convergence NEW_OFFENSIVE | 35,5 % G.mod, 30,3 % Centre |
| Diffusion cessez-le-feu | ~14 mois (Gauche → Droite) |

---

## 4. Notebooks et scripts

Convention notebooks : **`nn_objet1_objet2`**.

| # | Fichier | Contenu |
|---|---------|---------|
| 01 | `01_corpus_validation` | Validation du corpus, accord LLM, biais, Panel B4 |
| 02 | `02_framing_lexique_emotions` | Cadres, stance, polarisation, émotions, adoption lexicale |
| 03 | `03_evenements_convergence` | Impact des événements, diff-in-diff, convergence |
| 04 | `04_ml_validation` | Validation ML (embeddings, logistic regression) |

**Scripts Python :**
- `analyses_supplementaires.py` : fig21–fig25 (attrition différentielle, RN vs LR, fighting words temporel, droite cessez-le-feu, Twitter vs AN, Chi² émotions)
- `build_analyses_extended.py` : trajectoires, variance intra-bloc, movers, cohérence Twitter-AN, targets, conditionality par batch, stance Droite

---

## 5. Cadre méthodologique

Ce compte rendu présente des résultats mesurés et descriptifs. Aucune prise de position normative n'est défendue. Les variables (stance, polarisation, convergence) sont des indicateurs quantitatifs du discours parlementaire.
