# Matrice de traçabilité des figures et claims

Ce tableau relie les surfaces éditoriales principales aux tables et scripts visibles, et borne les interprétations autorisées.

## Dataviz racine

| Surface / figure | Table source | Code visible | Interprétation autorisée | Interprétation à éviter |
| --- | --- | --- | --- | --- |
| `index.html` planche 01 cadres discursifs | `data/frames_par_bloc.csv` | `scripts/main.js` ou données inline dans `index.html` | les cadres dominants diffèrent fortement entre blocs | inférer une causalité politique ou une stabilité conceptuelle parfaite des classes |
| `index.html` planche 02 intensité de production | `data/vue_ensemble.csv` | `scripts/main.js` ou données inline dans `index.html` | le corpus est très déséquilibré et la gauche radicale sur-produit | conclure que ce bloc est "plus représentatif" de l'opinion parlementaire |
| `index.html` planche 03 trajectoires de stance | `data/stance_mensuel.csv` | `scripts/main.js` ou données inline dans `index.html` | le Centre varie davantage dans les séries mensuelles visibles | dire que seuls les autres blocs sont totalement immobiles |
| `index.html` planche 04 chocs événementiels | `data/event_impact_diff_in_diff.csv` | `scripts/main.js` ou données inline dans `index.html` | certains shifts avant/après sont significatifs dans certaines fenêtres | parler de causalité ou de diff-in-diff canonique |
| `index.html` planche 05 registres émotionnels | `data/emotional_register.csv` | `scripts/main.js` ou données inline dans `index.html` | la distribution des registres varie selon les blocs | traiter ces scores comme une mesure psychologique directe des acteurs |

## Sous-projet `fr_assemblee_discourse_analysis`

| Table / figure attendue | Table source | Script visible | Interprétation autorisée | Interprétation à éviter |
| --- | --- | --- | --- | --- |
| `stance_mensuel.csv` / figures de stance | `fr_assemblee_discourse_analysis/data/results/stance_mensuel.csv` | notebooks + corpus préparé via `src/prepare_data.py` | trajectoires descriptives par bloc | tendance monotone ferme si `mann_kendall_bloc.csv` n'est pas significatif |
| `event_impact_diff_in_diff.csv` | `fr_assemblee_discourse_analysis/data/results/event_impact_diff_in_diff.csv` | notebook événementiel ou export antérieur | comparaison avant/après par bloc et par variable | diff-in-diff causal avec groupe contrôle |
| `convergence_batch_bloc.csv` | `fr_assemblee_discourse_analysis/data/results/convergence_batch_bloc.csv` | export publication pré-calculé | convergence telle que codée par `transpartisan_convergence` dans `NEW_OFFENSIVE` | assimiler cette table à la métrique homonyme de `analyse_discursive_depute/` |
| `twitter_vs_an.csv` | `fr_assemblee_discourse_analysis/data/results/twitter_vs_an.csv` | `src/analyses_supplementaires.py` | pas d'effet global significatif de l'arène Twitter une fois contrôlés bloc et frame | prétendre à un écart moyen robuste Twitter vs AN |

## Sous-projet `analyse_discursive_depute`

| Table / figure attendue | Table source | Script visible | Interprétation autorisée | Interprétation à éviter |
| --- | --- | --- | --- | --- |
| `regression_delta_stance.csv` | `analyse_discursive_depute/data/results/regression_delta_stance.csv` | `analyse_discursive_depute/scripts/run_analysis.py` | dans cette spécification, seule la gauche radicale diverge significativement entre Twitter et AN | généraliser cette conclusion à toutes les spécifications |
| `RAPPORT_VALIDATION_HUMAINE.txt` | `analyse_discursive_depute/data/results/RAPPORT_VALIDATION_HUMAINE.txt` | `src/validation_metrics.py` | la chaîne de validation existe et un résultat parfait a été exporté | considérer ce 100 % comme crédible sans auditer l'échantillon et le merge |
| `lag_adoption.csv` | `analyse_discursive_depute/data/results/lag_adoption.csv` | `run_analysis.py` | la droite adopte plus tardivement le lexique du cessez-le-feu au seuil retenu | raconter une diffusion linéaire simple entre tous les blocs |
| `polarisation_index.csv` + `cosine_distance_mensuelle.csv` | `analyse_discursive_depute/data/results/` | `run_analysis.py` | les univers lexicaux restent fortement séparés | prétendre à une hausse monotone propre si les séries sont volatiles |

## Claims éditoriaux robustes, prudents et réutilisables

- Le corpus visible est très déséquilibré en faveur de la gauche radicale.
- Les cadres humanitaire et sécuritaire structurent fortement l'opposition entre blocs.
- Le Centre / Majorité est le bloc le plus mobile dans plusieurs fenêtres événementielles visibles.
- La comparaison globale Twitter vs Assemblée n'est pas significative dans `fr_assemblee_discourse_analysis/data/results/twitter_vs_an.csv`.
- La convergence tardive existe dans certains exports, mais sa définition varie selon les sous-projets.

## Claims à reformuler ou à abandonner sans audit complémentaire

- "diff-in-diff" si le design réel est une comparaison avant/après sans groupe contrôle ;
- "seul le Centre bouge" ;
- "Twitter est plus pro-israélien que l'Assemblée" dans le repo nettoyé ;
- "validation humaine parfaite" ;
- toute formule laissant croire à une causalité événementielle ou à une mesure affective directe.
