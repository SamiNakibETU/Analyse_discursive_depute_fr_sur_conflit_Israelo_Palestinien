# Codebook - Annotation LLM

**Projet** : fr_assemblee_discourse_analysis - Analyse discursive sur le conflit israélo-palestinien  
**Date** : février 2026

---

## 1. Versions d'annotation

### v3 - Annotation baseline (corpus complet)

- **Modèle** : GPT-4o-mini
- **Corpus** : 10 774 textes (tous les textes post-7 octobre 2023)
- **Variables annotées** :
  - `stance_v3` : position sur une échelle de -2 (très pro-Israël) à +2 (très pro-Palestine)
  - `confidence_v3` : score de confiance du modèle (0.70–0.95)
  - `primary_frame_v3` : cadre discursif dominant
  - `intensity_v3` : intensité du positionnement
  - `has_both_sides_v3` : présence d'arguments des deux parties

### v4 - Annotation enrichie (fenêtres événementielles)

- **Modèle** : GPT-4o-mini
- **Corpus** : 5 905 textes (7 fenêtres événementielles)
- **Variables supplémentaires** :
  - `stance_v4` : même échelle que v3
  - `ceasefire_call` : booléen - appel explicite au cessez-le-feu
  - `ceasefire_type` : {unconditional, conditional, humanitarian_pause, balanced, neutral}
  - `emotional_register` : {indignation, grief, solidarity, defiance, neutral, anger, fear, defense}
  - `frame_primary` : cadre élargi (plus de catégories que v3)
  - Variables batch-spécifiques (genocide_framing, icc_warrants_position, etc.)

---

## 2. Échelle de stance

| Valeur | Label | Définition |
|--------|-------|------------|
| -2 | Très pro-Israël | Défense explicite d'Israël, justification des opérations militaires |
| -1 | Pro-Israël modéré | Solidarité avec Israël, accent sur sécurité/terrorisme |
| 0 | Neutre / Équilibré | Appels à la paix sans prise de parti, ou mention factuelle |
| +1 | Pro-Palestine modéré | Préoccupation humanitaire, appels au cessez-le-feu |
| +2 | Très pro-Palestine | Dénonciation explicite d'Israël, accusation de génocide |

---

## 3. Cadres discursifs (frames)

### v3 (simplifié)

| Code | Label | Exemple |
|------|-------|---------|
| HUM | Humanitaire | "catastrophe humanitaire à Gaza" |
| SEC | Sécuritaire | "droit d'Israël à se défendre" |
| LEG | Juridique | "violation du droit international" |
| MOR | Moral/Éthique | "devoir de mémoire", "valeurs républicaines" |
| DIP | Diplomatique | "solution à deux États" |
| HIS | Historique | "depuis 1948", "colonisation" |
| ECO | Économique | sanctions, embargo |

### v4 (élargi)

Mêmes cadres + SOL (Solidarité), IND (Indignation), DOM (politique domestique), etc.

---

## 4. Fenêtres événementielles (batches)

| Batch | Événement | Dates | n textes (v4) |
|-------|-----------|-------|---------------|
| CHOC | Attaque du 7 octobre | 7 oct. – 31 déc. 2023 | ~1 600 |
| POST_CIJ | Ordonnance CIJ | 26 jan. – 30 avr. 2024 | ~800 |
| RAFAH | Offensive sur Rafah | 6 mai – 31 juil. 2024 | ~700 |
| POST_SINWAR | Mort de Sinwar | 17 oct. – 20 nov. 2024 | ~300 |
| MANDATS_CPI | Mandats CPI | 21 nov. 2024 – 14 jan. 2025 | ~400 |
| CEASEFIRE_BREACH | Cessez-le-feu et violation | 15 jan. – 14 mar. 2025 | ~500 |
| NEW_OFFENSIVE | Nouvelle offensive | 15 mar. – 31 jan. 2026 | ~1 600 |

Voir `src/config.py` pour les dates exactes par batch.

---

## 5. Blocs politiques

| Bloc | Groupes parlementaires |
|------|------------------------|
| Gauche radicale | LFI-NFP, LFI, GDR |
| Gauche modérée | PS-NFP, SOC, ECO-NFP, ECO |
| Centre / Majorité | EPR, REN, MODEM, HOR, DEM |
| Droite | RN, LR, UDR, NI |

Voir `docs/RAPPORT_EXPLORATION_CLASSIFICATION_GROUPES.md` pour le détail des changements de dénomination (XVIe → XVIIe législature).

---

## 6. Prompt d'annotation

### Système (v4 - extrait principal)

```
Tu es un analyste politique spécialisé dans le discours parlementaire français sur le conflit israélo-palestinien.

ÉCHELLE DE STANCE (stance_v4) :
-2 = Pro-Israël fort : soutien explicite aux opérations militaires, défense inconditionnelle
-1 = Pro-Israël modéré : droit de se défendre, solidarité avec Israël, avec nuances
 0 = Neutre/équilibré : deux côtés, appel à la paix sans parti pris
+1 = Pro-Palestinien modéré : cessez-le-feu, préoccupation humanitaire, critique de la riposte
+2 = Pro-Palestinien fort : « génocide », sanctions, critique systémique d'Israël

RÈGLES DE CALIBRATION :
1. Cessez-le-feu seul = au minimum +1, sauf si conditionné à la destruction du Hamas (alors -1 ou 0).
2. « Droit de se défendre » sans nuance = -1 minimum. Avec « mais proportionné » = 0.
3. Mention de « génocide » place quasi-systématiquement à +2 (sauf citation juridique neutre).
4. Texte uniquement sur les otages sans mentionner Gaza = -1.
5. Texte procédural ou institutionnel = 0.
```

Le prompt complet (avec few-shot, variables batch-spécifiques et briefings contextuels) est disponible dans le projet source : `projet_gaza/outputs/prompt_annotation_v4.txt`.

---

## 7. Panel B4

- **Seuil** : députés actifs ≥ 18 mois sur la période
- **Effectif** : 76 députés (42 G.rad, 9 G.mod, 10 Centre, 15 Droite)
- **Textes** : 8 255 (76,6 % du corpus)
- **Biais documenté** : Centre/Majorité du panel est plus pro-Israël (Δ ≈ -0.39) que le corpus complet

---

## Référence

- Gilardi et al. (2023) - Les LLM rivalisent avec les annotateurs humains sur des tâches de classification politique.
- Mohammad et al. (2016) - SemEval-2016 Task 6: Stance Detection.
