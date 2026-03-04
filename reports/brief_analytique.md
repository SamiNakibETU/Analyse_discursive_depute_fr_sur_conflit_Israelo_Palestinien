# Brief analytique — Discours parlementaire français sur Gaza (2023–2026)

## 1. Contexte et question de recherche

**Contexte** : Entre octobre 2023 et janvier 2026, le conflit israélo-palestinien a mobilisé une part significative du débat public français. Les députés s’expriment via Twitter/X et à l’Assemblée nationale.

**Question** : Comment ont évolué les positions discursives des députés par bloc politique ? Y a-t-il une réaction différenciée aux événements pivot (CIJ, mandats CPI, cessez-le-feu) selon le positionnement gauche–droite ?

---

## 2. Données et méthode

**Corpus** : 10 774 textes (tweets + interventions AN) de 459 députés. Fenêtre : oct. 2023 – janv. 2026.

**Méthode** :
- Annotation du positionnement (-2 pro-Israël à +2 pro-Palestine) ; accord v3↔v4 : Spearman 0,86.
- Segmentation en 7 batches temporels (CHOC → NEW_OFFENSIVE).
- Analyses : stance mensuel par bloc, shift temporel avant/après événements, distance cosinus entre blocs, fighting words (log-odds).

---

## 3. Résultat 1 : Stabilité vs réactivité

Le Centre varie significativement après les événements pivot ; la Gauche radicale et la Droite restent stables sur 28 mois.

![fig10](../figures/fig10_stance_ribbon.png)

---

## 4. Résultat 2 : Paradoxe de la Droite au cessez-le-feu

Quand le Centre appelle au cessez-le-feu (janv. 2025), la Droite durcit son discours (Δ stance -1,03, p≈0,008). Interprétation : stratégie de différenciation plutôt qu’alignement.

![fig12](../figures/fig12_diff_in_diff.png)

---

## 5. Résultat 3 : Convergence transpartisane tardive

35,5 % des textes Gauche modérée et 30,3 % des textes Centre convergent vers le vocabulaire du cessez-le-feu en fin de période. La diffusion lexicale suit les positions implicites.

![fig33](../figures/fig33_convergence_batch.png)

---

## 6. Résultat 4 : Polarisation lexicale

Distance cosinus maximale Gauche radicale – Droite en décembre 2024. Les « fighting words » (log-odds) distinguent nettement les vocabulaires par bloc.

![fig18](../figures/fig18_distance_cosinus_gr_droite.png)

---

## 7. Limites et perspectives

- Pas de validation humaine de l’annotation.
- Corpus déséquilibré par bloc (Gauche radicale majoritaire).
- Aucune inférence causale stricte (shift temporel descriptif).
- Pistes : validation humaine, granularité parti (LR/RN séparés).

---

## 8. Annexe méthodo

- **Rapport complet** (toutes les métriques) : [data/results/RAPPORT_RESULTATS.txt](../data/results/RAPPORT_RESULTATS.txt)
- **Résultats numériques (MD)** : [RESULTATS_NUMERIQUES.md](RESULTATS_NUMERIQUES.md) — export exhaustif chiffres et séries temporelles
- Documentation : [METHODOLOGIE.md](../docs/METHODOLOGIE.md), [DONNEES.md](../docs/DONNEES.md)

*Les figures ci-dessus sont générées par `python scripts/run_analysis.py` (dossier `figures/`).*

---

## 9. Brief de finalisation — Récapitulatif des implémentations

### Phase 1 — Fondations (A1, A2, A3)
- **A1 — Validation humaine** : `validation_humaine.py` (échantillonnage triple stratification bloc×arène×batch), `validation_metrics.py` (Cohen Kappa, Spearman, biais par bloc, matrice confusion), notebook 11, fig51–52
- **A2 — LR vs RN** : `config.py` (`BLOC_ORDER_5`, `BLOC_COLORS_5`), notebook 12, analyses stance/effectifs LR–RN
- **A3 — Tendances pré-événement** : fenêtre 60 jours, Mann-Kendall pré-événement, fig53, METHODOLOGIE §8

### Phase 2 — Robustesse (A4, A5)
- **A4 — Corpus équilibré** : fig66–68 (stance ribbon, diff-in-diff, cosinus) corpus complet vs équilibré, tableau de robustesse
- **A5 — CODEBOOK** : références théoriques par frame (HUM, SEC, LEG, DIP, MOR, HIS, ECO, POL)

### Phase 3 — Enrichissements (B1, B4, B5)
- **B1 — NER cibles discursives** : `ner_analysis.py`, notebook 13, fig69–71 (entités, humanization_score)
- **B4 — Twitter vs AN** : extension NB10, fig72, régression delta_stance, fighting words différentiels
- **B5 — Trajectoires movers** : critères stance_initial/final, fig73–74 (spaghetti, distribution delta)

### Phase 4 — Raffinements (C1, C2, C3)
- **C1 — MFD étendu** : lexique 40+ mots/fondement (care, fairness, loyalty, authority, sanctity), `compute_mfd_coverage()` (~99 % couverture)
- **C2 — Registre discursif** : `CONTEXTES_AMBIGU` (« responsable » contextuel), Spearman registre vs stance, fig75 bloc×batch
- **C3 — Polarisation entropique** : fig76 Ec vs distance cosinus, METHODES_COMPLEMENTAIRES (interprétation ED)

### Export et reproductibilité
- **RESULTATS_NUMERIQUES.md** : un seul MD (synthèse métriques + tables CSV) produit par `run_analysis.py`, équivalent exhaustif des notebooks
