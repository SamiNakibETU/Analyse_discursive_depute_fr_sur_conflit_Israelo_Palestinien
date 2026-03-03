# Brief analytique — Discours parlementaire français sur Gaza (2023–2026)

## 1. Contexte et question de recherche

**Contexte** : Entre octobre 2023 et janvier 2026, le conflit israélo-palestinien a mobilisé une part significative du débat public français. Les députés s’expriment via Twitter/X et à l’Assemblée nationale.

**Question** : Comment ont évolué les positions discursives des députés par bloc politique ? Y a-t-il une réaction différenciée aux événements pivot (CIJ, mandats CPI, cessez-le-feu) selon le positionnement gauche–droite ?

---

## 2. Données et méthode

**Corpus** : 10 774 textes (tweets + interventions AN) de 459 députés. Fenêtre : oct. 2023 – janv. 2026.

**Méthode** :
- Annotation du positionnement (-2 pro-Israël à +2 pro-Palestine) par LLM ; accord v3↔v4 : Spearman 0,86.
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

- Pas de validation humaine de l’annotation LLM.
- Corpus déséquilibré par bloc (Gauche radicale majoritaire).
- Aucune inférence causale stricte (shift temporel descriptif).
- Pistes : validation humaine, granularité parti (LR/RN séparés).

---

## 8. Annexe méthodo

Voir [METHODOLOGIE.md](docs/METHODOLOGIE.md) et [DONNEES.md](docs/DONNEES.md).
