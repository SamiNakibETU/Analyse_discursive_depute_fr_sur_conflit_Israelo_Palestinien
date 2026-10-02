# Codebook

Ce document décrit les variables telles qu'elles ont été effectivement produites. La source de vérité est le texte des prompts dans `annotation/v3/annotation_v3.py` et `annotation/v4/annotation_v4.py` ; en cas d'écart, le code fait foi.

Les deux annotations ont été réalisées avec gpt-4o-mini (OpenAI), à température 0,05 pour la v3.

## Unité d'analyse

Un texte : un tweet d'un député, ou une prise de parole en séance publique à l'Assemblée nationale. Les textes ont d'abord été filtrés par mots-clés (`config/mots_cles.json`), puis le modèle pouvait les déclarer hors sujet.

## Informations transmises au modèle

Pour chaque texte, le prompt contenait, en plus du texte lui-même : le type de source, le nom de l'auteur, son groupe politique (v3) ou son groupe et son bloc (v4), la date et la période. La v3 ajoutait une table des « positions typiques » de chaque groupe. La v4 ajoutait un résumé du contexte de la fenêtre et cinq exemples annotés, dont plusieurs mentionnent le parti de l'auteur.

Conséquence : les variables qui demandent un jugement au modèle (position, registre, cadre) peuvent refléter l'étiquette partisane autant que le texte. Voir `docs/methodologie.md`, section 4.

## Annotation v3 (corpus complet, 10 774 textes)

| Variable | Valeurs | Définition |
|---|---|---|
| `stance_v3` | −2 à +2 | Position sur le conflit : −2 soutien marqué à Israël, 0 neutre ou équilibré, +2 soutien marqué à la cause palestinienne |
| `intensity_v3` | weak, moderate, strong | Force de l'engagement |
| `confidence_v3` | 0 à 1 | Confiance déclarée par le modèle |
| `primary_frame` | HUM, SEC, LEG, DIP, MOR, HIS, ECO | Cadre dominant (voir ci-dessous) |
| `target` | libellé libre | Acteur visé |
| `is_off_topic` | booléen | Texte sans rapport avec le conflit |

Cadres : HUM humanitaire (victimes civiles, aide, souffrance) ; SEC sécuritaire (terrorisme, défense, menace) ; LEG juridique (droit international, CIJ, CPI, crimes) ; DIP diplomatique (relations internationales, reconnaissance) ; MOR moral (justice, valeurs, droits humains) ; HIS historique (histoire du conflit, mémoire) ; ECO économique (sanctions, boycott, aide financière).

## Annotation v4 (sept fenêtres, 5 905 textes)

Ré-annotation des textes publiés dans sept fenêtres événementielles. Le modèle devait d'abord justifier sa classification en deux ou trois phrases (`reasoning`).

| Fenêtre | Début | Fin |
|---|---|---|
| CHOC | 7 oct. 2023 | 15 nov. 2023 |
| POST_CIJ | 26 janv. 2024 | 15 févr. 2024 |
| RAFAH | 1er mai 2024 | 15 juin 2024 |
| POST_SINWAR | 15 oct. 2024 | 31 oct. 2024 |
| MANDATS_CPI | 21 nov. 2024 | 31 déc. 2024 |
| CEASEFIRE_BREACH | 1er janv. 2025 | 31 mars 2025 |
| NEW_OFFENSIVE | 1er avr. 2025 | 30 juin 2025 |

| Variable | Valeurs | Définition |
|---|---|---|
| `stance_v4` | −2 à +2 | Même échelle qu'en v3, avec des règles de calibration explicites (ci-dessous) |
| `ceasefire_call` | booléen | Le texte appelle à un cessez-le-feu |
| `ceasefire_type` | unconditional, conditional_hostages, conditional_other, humanitarian_pause | Nature de l'appel |
| `target_primary`, `target_secondary` | libellé libre | Acteur principalement visé |
| `frame_primary` | HUM, SEC, LEG, DIP, MOR, DOM, SOL | Cadre dominant (DOM politique intérieure, SOL solidarité) |
| `conditionality` | absolute, conditional, balanced | Position tranchée, assortie de réserves, ou présentant les deux côtés |
| `emotional_register` | anger, grief, indignation, fear, solidarity, neutral, defiance | Registre émotionnel dominant |
| `key_demands` | liste | Demandes formulées (cessez-le-feu, sanctions, reconnaissance, libération des otages, etc.) |
| variables de fenêtre | booléens ou modalités | Par exemple `condemns_hamas_attack`, `proportionality_issue`, `self_defense_mention` (CHOC), `icj_reference` (POST_CIJ), `transpartisan_convergence` (NEW_OFFENSIVE) |

Règles de calibration de la position v4, reprises du prompt :

1. Un texte qui condamne le Hamas et appelle au cessez-le-feu n'est pas neutre par défaut ; le poids relatif des deux parties décide.
2. « Cessez-le-feu » seul vaut au moins +1, sauf s'il est conditionné à la destruction du Hamas.
3. « Droit de se défendre » sans nuance vaut au moins −1 ; avec « mais proportionné », 0.
4. « Génocide » place presque toujours à +2, sauf citation neutre du terme juridique.
5. Un texte qui ne parle que des otages sans mentionner Gaza vaut −1.
6. Un texte purement procédural vaut 0.
7. Pour une question au gouvernement, on code la position de l'auteur de la question.

Ces règles rendent la position v4 en partie lexicale : l'apparition ou la disparition de certains mots la déplace mécaniquement.

## Variables inutilisables

Sept variables de fenêtre valent 100 % dans les quatre blocs, ce qui signifie qu'elles ont été codées comme « renseignées » plutôt que par leur valeur : `genocide_framing` (POST_CIJ, RAFAH, MANDATS_CPI), `icc_warrants_position`, `sinwar_reaction`, `rafah_reaction`, `ceasefire_breach_blame`. Elles ne sont pas exploitées.

## Blocs

| Bloc | Groupes |
|---|---|
| Gauche radicale | LFI, LFI-NFP, GDR |
| Gauche modérée | SOC, PS-NFP, ECO, ECO-NFP |
| Centre / Majorité | REN, EPR, MODEM, DEM, HOR |
| Droite | LR, RN, UDR, NI |

Le regroupement de LR et du RN dans un même bloc suit le choix initial du projet. Les tables `stance_par_groupe.csv` permettent de les séparer.
