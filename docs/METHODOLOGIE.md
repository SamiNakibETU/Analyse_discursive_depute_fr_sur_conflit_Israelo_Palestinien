# Méthodologie

## Vue d'ensemble

Analyse computationnelle du discours parlementaire français sur le conflit israélo-palestinien (octobre 2023 – janvier 2026). Corpus : tweets et interventions à l'Assemblée nationale, annotés par LLM.

## Données

| Élément | Description |
|--------|-------------|
| Corpus principal (v3) | 10 774 textes, 459 députés |
| Corpus événementiel (v4) | 5 905 textes, fenêtres autour d'événements pivot |
| Annotation | LLM (score stance -2 à +2), accord v3↔v4 : Spearman 0,86, accord exact 61,6 % |

## Fenêtres temporelles (batches)

| Batch | Période |
|-------|---------|
| CHOC | 7 oct. – 31 déc. 2023 |
| POST_CIJ | 26 jan. – 30 avr. 2024 |
| RAFAH | 7 mai – 15 oct. 2024 |
| POST_SINWAR | 16 oct. – 20 nov. 2024 |
| MANDATS_CPI | 21 nov. 2024 – 14 janv. 2025 |
| CEASEFIRE_BREACH | 15 janv. – 17 mars 2025 |
| NEW_OFFENSIVE | 18 mars 2025 – 31 janv. 2026 |

## Event studies (shift temporel)

Nous mesurons un **changement de position moyenne avant/après** chaque événement pivot, par bloc. Il s'agit d'une analyse descriptive de type « shift temporel » — pas d'un diff-in-diff classique (groupe traité vs contrôle, tendances parallèles). Pour chaque événement et bloc, on calcule la différence des moyennes (post – pré) et un test de significativité (Mann-Whitney ou équivalent).

## Blocs politiques

- Gauche radicale
- Gauche modérée
- Centre / Majorité
- Droite (LR, RN regroupés)

## Limites

- Pas de validation humaine de l'annotation LLM — les scores sont un proxy.
- Corpus déséquilibré par bloc — la Gauche radicale domine en volume.
- Panel B4 : sous-ensemble des députés les plus actifs sur 18 mois — biais de sélection possible.
- Aucune inférence causale stricte — les évolutions observées sont associatives.
