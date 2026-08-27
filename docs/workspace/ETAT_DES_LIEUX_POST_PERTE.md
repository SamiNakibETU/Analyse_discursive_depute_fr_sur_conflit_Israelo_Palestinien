# État des lieux après perte du corpus source

Audit des deux dépôts, réalisé après la perte de `corpus_v3.parquet` / `corpus_v4.parquet`.
Objectif : déterminer ce qui reste exploitable pour produire des articles Substack.

Dépôts audités :
- `Analyse_discursive_depute_fr_sur_conflit_Israelo_Palestinien` (moteur canonique) — noté **R1**
- `Analyse-discursive-sur-le-conflit-Israelo-Palestinien` (couche publication) — noté **R2**

---

## 1. Ce qui a survécu

### 1.1 Résultats agrégés — intacts

| Actif | Emplacement | Volume |
|---|---|---|
| CSV de résultats | `R1/analysis/data/results/`, `R1/publication/data/results/`, `R2/data/results/` | **63 CSV uniques** (39 par dossier, recouvrement partiel) |
| Export exhaustif des tables | `R1/analysis/reports/RESULTATS_NUMERIQUES.md` | 176 Ko, toutes les séries ligne à ligne |
| Log complet du run | `R1/analysis/data/results/RAPPORT_RESULTATS.txt` | 2,5 Mo |
| Compte rendu chiffré rédigé | `R2/docs/COMPTE_RENDU_RESULTATS.md` | 389 lignes, 27 sections de tableaux |

Toutes les statistiques publiées dans les articles peuvent sortir de ces fichiers **sans jamais rouvrir le corpus**.

### 1.2 Figures — intactes côté R2

- **88 PNG uniques** dans `R2/figures/` (80) et `R2/reports/figures/` (88, sur-ensemble).
- 60 figures supplémentaires sont **embarquées en base64 dans les notebooks** `R1/analysis/notebooks/*.ipynb` (01, 03, 04, 05, 06, 07, 10 ont des sorties conservées).
- En revanche les PNG produits par le moteur avancé (`fig01`–`fig76` référencés dans `R1/analysis/docs/CATALOGUE_FIGURES.md`, 73 entrées) sont perdus : `figures/` est gitignoré côté R1.

### 1.3 Code — intact

| Actif | Emplacement |
|---|---|
| Moteur d'analyse complet | `R1/analysis/scripts/run_analysis.py` (78 Ko, 1 600 lignes, 20 fonctions `run_*`) |
| Modules | `R1/analysis/src/` : VAD, MFD, NER cibles, registre discursif, validation |
| Pipeline de collecte AN + Twitter | `R1/pipeline/collection/src/final_pipeline/` |
| Pipeline d'annotation LLM | `R1/pipeline/annotation/src/` (v2, v3, v4) |
| Lexique NRC-VAD complet | `R1/analysis/data/lexicons/` (156 Mo, versionné) |

### 1.4 Reliquats de texte brut — les seuls restants

| Fichier | Contenu | Ce qu'il permet |
|---|---|---|
| `R1/analysis/data/validation/sample_150.csv` | **149 textes bruts** + auteur, date, bloc, arène, batch | Ré-annotation humaine réelle ; citations verbatim vérifiées |
| `R1/pipeline/collection/interventions_gaza_final.csv` | **4 099 interventions AN**, texte intégral, `url_source` vers les XML open data | Reconstruction complète du volet Assemblée ; verbatims de séance |
| `R1/pipeline/annotation/data/annotated/to_annotate/*.csv` | ~2 100 tweets + 280 interventions, texte brut | Verbatims Twitter, échantillon de contrôle |
| `R1/config/twitter_sources/`, `R1/pipeline/collection/config/twitter_handles*.json` | Mapping députés → comptes X | Rescraping ciblé si jamais |

Couverture temporelle de `interventions_gaza_final.csv` : juillet 2022 → juin 2024 (4 099 lignes).
Elle ne couvre donc pas mi-2024 → janvier 2026, mais l'open data AN est permanent et le scraper est présent.

### 1.5 Surfaces éditoriales — prêtes

| Actif | Emplacement | État |
|---|---|---|
| Dataviz D3, 5 planches | `R1/site/` + `R1/site/data/*.csv` | Fonctionnel, autonome |
| Prototype React/Vite d'article | `R1/analysis/DATA_VIZ_Article/AI_protype/` | Composants `SubstackFigure1/2/3`, `EditorialFigure1-3`, 3 directions graphiques |
| Chiffres déjà figés pour l'article 1 | `.../src/data/article1.ts` | 186 lignes, valeurs en dur |
| Charte dataviz | `R1/DESIGN_SYSTEM.md` | 20 Ko, complète (Grootens / suisse-néerlandais) |
| Garde-fous interprétatifs | `R1/docs/traceability/FIGURE_TRACEABILITY_MATRIX.md` | Claims autorisés / interdits, figure par figure |
| Méthodo, codebook | `R1/analysis/docs/`, `R2/docs/` | METHODOLOGIE, CODEBOOK, METHODES_COMPLEMENTAIRES, DONNEES |

---

## 2. Ce qui est perdu

1. `corpus_v3.parquet` (10 774 textes) et `corpus_v4.parquet` (5 905 textes) — texte + annotations LLM.
2. Les ~9 135 tweets bruts (10 774 − 1 639 interventions AN).
3. Les PNG du moteur avancé côté R1.
4. Par conséquent : impossible de créer une **nouvelle** variable, de refaire une passe d'annotation, de rééchantillonner, ou de citer un verbatim hors des reliquats du §1.4.

---

## 3. Ce qui bloque réellement la publication

### 3.1 La validation humaine n'en est pas une — bloquant

`R1/analysis/data/results/RAPPORT_VALIDATION_HUMAINE.txt` affiche :

```
Cohen's Kappa : 1.000
Spearman rho  : 1.000 (p = 0.0)
Accord exact  : 100.0 %
Biais par bloc : 0.000 partout
```

Un kappa de 1,000 sur 149 items, avec un biais nul dans les quatre blocs, n'est pas un résultat d'annotation humaine.
`R1/analysis/data/validation/annotations.csv` (149 lignes, colonne `stance_humain`) a été rempli avec les labels LLM eux-mêmes,
ou le merge de `validation_metrics.py` a rapatrié `stance_v3` des deux côtés.
La matrice de traçabilité le signalait déjà : *« considérer ce 100 % comme crédible sans auditer l'échantillon et le merge »* est une interprétation interdite.

Conséquence : **tout l'appareil `stance` est indéfendable dans un article tant que ce chiffre n'est pas remplacé.**
C'est le seul verrou vraiment bloquant — et il est levable : les 149 textes sont dans `sample_150.csv`, la ré-annotation à la main
est un chantier de 2 à 3 heures, et `validation_metrics.py` tourne sans le corpus si l'on y injecte `stance_v3`
depuis un CSV plutôt que depuis le parquet.

### 3.2 Métriques homonymes, définitions divergentes

`convergence_batch_bloc`, `twitter_vs_an`, `event_impact_diff_in_diff` existent dans R1 **et** dans R2 avec des valeurs différentes
(ex. « shift Droite au cessez-le-feu » : −1,03 dans `R1/analysis/README.md`, −1,10 dans `R2/docs/COMPTE_RENDU_RESULTATS.md`).
Il faut trancher une source canonique par chiffre avant d'écrire une seule ligne. Proposition : R1 `analysis/data/results/` fait foi,
R2 sert de contrôle.

### 3.3 Déséquilibre du corpus

63,47 % du corpus est Gauche radicale ; le panel B4 est à 75 % Gauche radicale (42 députés sur 76).
Ce n'est pas un défaut à cacher — c'est un résultat en soi (surproduction : 122,1 tweets/député contre 16,9 au Centre).
Mais aucune moyenne « toutes tendances confondues » ne doit apparaître dans les articles.

### 3.4 Reproductibilité

Le corpus n'étant plus là, personne ne peut rejouer le pipeline. Deux options honnêtes :
publier en assumant « données agrégées disponibles, corpus non redistribuable », ou reconstruire le volet AN (§4).

---

## 4. Ce qui est reconstructible

| Volet | Faisabilité | Moyen |
|---|---|---|
| Assemblée nationale (1 639 textes) | **Élevée** | Open data AN permanent ; `url_source` présent dans `interventions_gaza_final.csv` ; scraper dans `pipeline/collection/src/final_pipeline/scraping/` |
| Twitter (~9 135 tweets) | **Faible** | Nitter hors service (cf. `pipeline/collection/DIAGNOSTIC_NITTER_DOWN.md`), API X payante. Reconstruction partielle au mieux |
| Figures du moteur avancé | **Élevée pour la majorité** | `run_analysis.py` produit 33 figures pour 41 écritures CSV : la plupart sont tracées depuis une table exportée dans la même fonction, donc un script de replot lisant `analysis/data/results/*.csv` les régénère sans le corpus. Les figures restantes du catalogue (73 entrées) viennent des notebooks 01–13 et sont à vérifier une par une |
| Annotations LLM | **Impossible** sans le texte | — |

---

## 5. Verdict

Les articles Substack sont faisables **sans le corpus**, parce que la couche agrégée est complète :
63 tables, 88 figures, un compte rendu chiffré de 389 lignes, une charte graphique et un prototype d'article.

Chantiers, par ordre de priorité :

1. **Ré-annoter à la main les 149 textes de `sample_150.csv`** et recalculer κ et ρ. Sans cela, pas de publication défendable.
2. **Figer une table canonique de chiffres** (un fichier, une valeur par claim, une source par valeur) en arbitrant les divergences R1/R2.
3. **Script de replot** `analysis/data/results/*.csv` → figures, à la charte `DESIGN_SYSTEM.md`.
4. **Reconstruire le volet AN** depuis l'open data, si l'on veut une reproductibilité affichable.
5. **Écrire une note « données et limites »** publiée avec le premier article : corpus déséquilibré, design descriptif avant/après sans inférence causale, corpus non redistribuable.

Angles d'articles entièrement couverts par ce qui reste :

- **Le Centre est le seul bloc mobile** — `event_impact_diff_in_diff.csv`, `stance_mensuel.csv`, `mann_kendall_bloc.csv`, fig12, fig13.
- **La diffusion du mot « cessez-le-feu »**, ~14 mois de la gauche à la droite — `ceasefire_lexical.csv`, `lag_adoption.csv`, `ceasefire_call_batch_bloc.csv`, fig24, fig25.
- **Deux vocabulaires qui cessent de se parler** — `cosine_distance_mensuelle.csv` (0,64 → 0,99), `fighting_words.csv` (25 700 lignes), `polarisation_index.csv`.
- **Indignation contre défiance** : la structure émotionnelle des blocs — `emotional_register.csv`, `frames_par_bloc.csv`, Chi² = 2 594,5.
- **Qui parle, et combien** : le paradoxe de visibilité — `activity_bias_by_bloc.csv`, `visibility_paradox_quintiles.csv`, `attrition_mensuelle.csv`.

---

## 6. Rapport entre les deux dépôts

**R2 n'est pas un autre projet : c'est `R1/publication/` extrait en dépôt autonome, plus les figures.**

`diff -rq R1/publication/data/results R2/data/results` ne renvoie **rien** : les 39 CSV sont identiques octet pour octet.
Seuls diffèrent quatre fichiers de documentation (`README.md`, `data/README.md`, `COMPTE_RENDU_RESULTATS.md`, `METHODOLOGIE.md`)
et `src/config.py`. R2 contient en plus `figures/` (80 PNG) et `reports/figures/` (88 PNG) — précisément ce que R1 a perdu.

Il existe en revanche **deux moteurs d'analyse distincts**, et c'est là que se joue la difficulté :

| | Moteur `publication` (= R2) | Moteur `analysis` (R1) |
|---|---|---|
| Script | `src/analyses_supplementaires.py`, `build_analyses_extended.py` | `scripts/run_analysis.py` (1 600 l.) |
| Notebooks | 4 (01–04) | 13 (01–13) |
| Tables produites | 39 CSV | 39 CSV |
| Figures | 88 PNG conservés | perdues, régénérables |
| Spécialité | variables v4 (conditionality, targets, key_demands, ceasefire_type, trajectoires individuelles, arc narratif) | métriques avancées (Wasserstein, VAD, fondements moraux, polarisation entropique, dimensionnalité effective, PCA, NER, Mann-Kendall) |

Ces deux jeux de 39 CSV **ne se recouvrent que sur 15 noms de fichiers**. Les 48 autres sont complémentaires,
d'où les 63 tables uniques.

---

## 7. Concordance des 15 tables partagées

Comparaison valeur à valeur (tolérance 0,01).

### 7.1 Concordantes — 9 tables

| Table | Valeurs comparées | Écarts |
|---|---|---|
| `stance_mensuel` | 112 | 0 |
| `volume_mensuel` | 112 | 0 |
| `attrition_mensuelle` | 28 | 0 |
| `ceasefire_call_batch_bloc` | 28 | 0 |
| `frames_par_bloc` | 4 blocs × frames | 0 |
| `emotional_register` | 4 blocs × registres | 0 |
| `stance_panel_vs_complet` | 4 | 0 |
| `panel_b4` | 44 députés | ensembles identiques |
| `emotional_register_v4` | — | identique octet pour octet |

Les différences de `cmp` sur ces fichiers sont **de forme uniquement** : large vs long, arrondi vs pleine précision, BOM.

### 7.2 Contradictoires — 6 tables

Même nom de fichier, mesure différente. À ne pas citer sans préciser la source.

| Table | Moteur `analysis` | Moteur `publication` | Nature de l'écart |
|---|---|---|---|
| `event_impact_diff_in_diff` | 3 événements, 1 variable, 12 lignes | 6 événements, 2 variables, 48 lignes | **Dates d'événement différentes** (Rafah 07/05 vs 28/05 ; cessez-le-feu 15/01 vs 19/01) et conclusions divergentes |
| `cosine_distance_mensuelle` | plage 0,086–0,557 (moy. 0,257) | plage 0,642–0,990 (moy. 0,867) | Vectorisations différentes ; corrélation des deux séries Gauche radicale ↔ Droite : **r = 0,66** seulement |
| `polarisation_index` | colonnes `dist`, `wd_mean` | colonnes `variance_inter_blocs`, `cosine_dist_mean` | Indices sans rapport |
| `convergence_batch_bloc` | pct sur 7 batchs (Centre 79,5 % en CEASEFIRE_BREACH) | variable v4 `transpartisan_convergence`, NEW_OFFENSIVE seul (Centre 30,3 %) | Deux définitions de « convergence » |
| `fighting_words` | log-odds global, 25 700 mots (`hamas` z = −34,9 ; `gaza` z = +25,5) | log-odds par batch, 18 611 lignes (`gaza` z = +5,66) | Scores z non comparables |
| `variables_batch_specifiques` | stance moyen par batch (7 l.) | pct de variable par batch × bloc (72 l.) | Tables sans rapport |

### 7.3 Le cas de l'ordonnance CIJ

Illustration de ce que coûte le §7.2 :

| Source | Δ stance Centre / Majorité | p | Verdict |
|---|---|---|---|
| `analysis` (coupure 2024-01-26) | −0,103 | 0,339 | non significatif |
| `publication` (coupure 2024-01-26) | −0,436 | 0,018 | significatif * |

Même événement, même date de coupure, même bloc — résultats opposés, donc fenêtres avant/après ou filtres différents.
**Le claim « le Centre bascule à l'ordonnance CIJ » ne tient que dans une des deux spécifications.**
Tant que la fenêtre n'est pas tranchée et documentée, il ne doit pas être publié.

---

## 8. Volume total des données disponibles

| Catégorie | Volume |
|---|---|
| Tables de résultats | **78 fichiers, 74 796 lignes** (63 noms uniques ; les doublons de nom sont les 15 du §7) |
| Figures PNG rendues | **88 uniques** (R2) + 60 embarquées dans les notebooks R1 |
| Textes bruts uniques | **4 755** — voir détail ci-dessous |
| Notebooks | 13 (R1 `analysis`) + 4 (publication) + ~15 (pipeline) |
| Lexiques | NRC-VAD complet, MFD, marqueurs de stance pro-israélien / pro-palestinien |

Détail des textes bruts survivants (dédoublonnés sur le texte normalisé) :

| Source | Textes uniques |
|---|---|
| `interventions_gaza_final.csv` (AN, juil. 2022 – juin 2024) | 3 925 |
| `corpus_to_annotate.csv` | 697 |
| `tweets_to_annotate.csv` | 497 |
| `annotation_v2.csv` / `annotation_corpus.csv` | 449 chacun |
| `interventions_to_annotate.csv` | 200 |
| `sample_150.csv` | 148 |
| **Union dédoublonnée** | **4 755** |

Attention : les 3 925 interventions AN sont un **sur-ensemble non filtré** (2022–2024), pas les 1 639 textes AN
du corpus final. Le recouvrement avec le corpus publié est donc partiel.

---

## 9. Classement des résultats par solidité

**Solides — deux moteurs indépendants, valeurs identiques.** Publiables tels quels.
Composition du corpus (10 774 textes, 459 députés, répartition par bloc) · stance mensuel par bloc sur 28 mois ·
attrition (211 → 34 députés actifs) · cadres discursifs (HUM 77,2 % à gauche radicale, SEC 44,8 % à droite) ·
registres émotionnels (indignation 63,7 % / défiance 41,2 %) · appels au cessez-le-feu par batch ·
biais du panel B4 (Centre −0,389).

**Uniques mais non contredits.** Publiables en nommant la source et la spécification.
Côté `analysis` : Wasserstein, VAD, fondements moraux, polarisation entropique, dimensionnalité effective, PCA,
NER cibles, Mann-Kendall, lag d'adoption, régression delta stance, movers cachés, intensité délibérative.
Côté `publication` : conditionnalité, cibles primaires, demandes clés, trajectoires individuelles,
variance intra-bloc, cohérence Twitter/AN, arc narratif, régression Twitter vs AN, accord v3/v4 (ρ = 0,86).

**Contredits — à trancher avant publication.**
Diff-in-diff événementiel · distance cosinus et indice de polarisation · convergence transpartisane ·
fighting words · variables par batch. Voir §7.2.

**Invalide.** Validation humaine (κ = 1,000). Voir §3.1.

---

*Audit établi le 27 août 2026.*
