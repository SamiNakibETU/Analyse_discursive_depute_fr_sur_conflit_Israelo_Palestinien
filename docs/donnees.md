# Données

## Ce que contient le dépôt

| Emplacement | Contenu | Origine |
|---|---|---|
| `data/resultats/chaine_lexicale/` | 39 tables et le journal d'exécution | `analyse_corpus/chaine_lexicale/run_analysis.py` |
| `data/resultats/chaine_variables/` | 39 tables | `analyse_corpus/chaine_variables/` |
| `data/resultats/MANIFESTE.csv` | Description, nature de mesure et statut de chaque table | |
| `data/an_2022_2024/interventions.csv` | 4 099 interventions en séance, juillet 2022 – juin 2024, texte intégral | Comptes rendus de l'Assemblée nationale |
| `data/validation/echantillon.csv` | 149 textes du corpus annoté, avec auteur, bloc, arène, fenêtre | Tirage stratifié |
| `data/validation/etiquettes_llm_v3.csv` | Position attribuée par le modèle à ces 149 textes | Annotation v3 |
| `data/validation/grille_annotation.csv` | Les mêmes textes, sans auteur ni bloc, à annoter | `python -m analyse.validation grille` |
| `config/` | Mots-clés de filtrage, groupes de la 17e législature, comptes X | |
| `sorties/` | Tables, chiffres clés et figures de l'analyse secondaire | `python -m analyse` |

## Ce qui n'est plus disponible

Le corpus annoté (`corpus_v3.parquet`, 10 774 textes ; `corpus_v4.parquet`, 5 905 textes) et les tweets bruts ont été perdus. Les tables de `data/resultats/` sont les sorties de ces corpus ; elles ne peuvent plus être recalculées, seulement réanalysées. Les chaînes de `analyse_corpus/` attendent le corpus dans `data/corpus/` et ne s'exécutent pas sans lui.

## Deux chaînes, des tables homonymes

Le projet a produit ses tables avec deux chaînes de traitement successives. Elles partagent quinze noms de fichiers. Neuf de ces tables concordent valeur pour valeur (par exemple les 112 positions mensuelles par bloc, ou les 28 taux d'appel au cessez-le-feu par fenêtre et par bloc). Six mesurent autre chose sous le même nom ; le manifeste les signale. L'analyse secondaire n'utilise jamais une table contradictoire sans nommer sa chaîne, et n'utilise pas du tout les comparaisons avant/après événement, qui dépendent de bornes différentes selon la chaîne.

Les deux chaînes nomment aussi les fenêtres de la même façon avec des dates différentes. Les dates de référence sont celles de l'annotation v4 (`docs/codebook.md`).

## Corrections

Les corrections appliquées par `analyse/chargement.py` sont détaillées dans `docs/methodologie.md`, section 7. La principale concerne les auteurs : les tables d'origine distinguent « M. X » (comptes rendus) et « X » (tweets), ce qui transforme 332 personnes en 501 auteurs. Toute table qui compte des députés (`vue_ensemble`, `attrition_mensuelle`, `variance_intra_bloc`, `trajectoires_individuelles`) surestime ce nombre.

## Interventions 2022-2024

Le fichier provient d'une collecte filtrée par mots-clés sur les comptes rendus de la 16e législature. Chaque ligne indique la date de séance, l'orateur et l'adresse du compte rendu XML d'origine sur `assemblee-nationale.fr`. Les colonnes `affiliation`, `periode` et `keywords_found` sont vides. Le filtre initial était large : seules 1 180 interventions mentionnent réellement le conflit, et l'analyse les isole par expression régulière (`analyse/chargement.py`, `MOTIF_CONFLIT`).

Les comptes rendus de l'Assemblée nationale sont diffusés sous Licence ouverte. Le fichier peut donc être redistribué, et reconstruit avec `collecte/assemblee/run_pipeline.py`.

## Tweets

Les tweets ne sont pas redistribués. Seules des statistiques agrégées en sont issues. Les identifiants de comptes utilisés pour la collecte sont dans `config/comptes_x.json`.

## Lexiques externes

Le lexique NRC-VAD utilisé par la chaîne lexicale n'est pas inclus : ses conditions d'utilisation le réservent à la recherche et il pèse 156 Mo. Il se télécharge sur la page de son auteur (Saif M. Mohammad, Conseil national de recherches du Canada) et se place dans `data/lexiques/nrc-vad/`.
