# Méthodologie

## 1. Question

Comment une crise internationale entre-t-elle dans la compétition partisane nationale ? Le cas étudié est la guerre à Gaza après l'attaque du Hamas du 7 octobre 2023, vue à travers ce qu'en disent les députés français, sur X et en séance, d'octobre 2023 à janvier 2026.

La question se décline en deux temps. Le 7 octobre a-t-il déplacé les positions des députés ? Et s'il ne les a pas déplacées, qu'a-t-il changé dans la manière d'en parler ?

## 2. Cadre d'analyse

Quatre notions organisent l'analyse.

Le cadrage, au sens de Robert Entman (1993), consiste à sélectionner certains aspects d'une réalité pour en proposer une définition du problème, une interprétation causale, une évaluation morale et un remède. Ces quatre fonctions correspondent presque terme à terme aux variables de l'annotation : le cadre dominant (humanitaire, sécuritaire, juridique…) définit le problème ; la cible principale désigne un responsable ; le registre émotionnel porte l'évaluation morale ; la demande formulée (cessez-le-feu, sanctions, libération des otages) propose un remède. Décomposer la « position » en ces quatre fonctions permet de voir bouger ce qu'un score unique écrase.

La propriété des enjeux (Petrocik, 1996) et, plus largement, la compétition sur les enjeux (Green-Pedersen, 2007) décrivent la tendance des partis à investir les sujets sur lesquels ils sont jugés crédibles et à ramener les autres vers leur propre terrain. On s'attend à ce qu'un parti « propriétaire » de la cause palestinienne en parle beaucoup, et à ce que ses adversaires reformulent le sujet dans des termes qu'ils maîtrisent (sécurité, antisémitisme, ordre public).

Le cycle d'attention (Downs, 1972) prévoit qu'un enjeu monte brutalement après un choc, puis décline à mesure que son coût et sa complexité apparaissent. Ce déclin n'est pas uniforme : ceux qui possèdent l'enjeu continuent d'en parler quand les autres se taisent.

La domestication, enfin, renvoie aux questions « intermestiques » (Manning, 1977) : des affaires étrangères qui deviennent des affaires intérieures parce qu'elles servent à départager des camps nationaux.

## 3. Hypothèses

| | Hypothèse | Observable |
|---|---|---|
| H1 | Cristallisation : les positions des blocs sont fixées dès le choc et ne bougent plus | Variance expliquée par le bloc et par le temps ; hétérogénéité mensuelle ; tendance de l'écart entre blocs ; stabilité des mots qui séparent les camps |
| H2 | Mobilité du cadrage : à position constante, les fonctions du cadrage évoluent | Appel au cessez-le-feu, attribution de responsabilité, registres émotionnels, par fenêtre |
| H3 | Cycle d'attention et appropriation : l'attention retombe et se concentre sur le bloc propriétaire de l'enjeu | Volume mensuel, part de chaque bloc, nombre effectif de blocs, concentration par personne |
| H4 | Domestication : une partie des blocs transforme le conflit en conflit intérieur, surtout en période électorale | Part des cibles qui sont des acteurs politiques français, par fenêtre |
| H5 | Redéfinition : le 7 octobre change la nature de la question posée au Parlement | Volume et vocabulaire des interventions en séance avant et après le 7 octobre |

## 4. Données

### Corpus annoté (2023-2026)

10 774 textes publiés entre le 7 octobre 2023 et janvier 2026 : 9 135 tweets et 1 639 interventions en séance. Les tweets ont été collectés via des instances Nitter à partir d'une liste de comptes de députés (`collecte/x/`), les interventions dans les comptes rendus de l'Assemblée nationale (`collecte/assemblee/`). Les deux sources ont été filtrées par mots-clés puis annotées.

Le texte de ce corpus a été perdu. Il reste les tables agrégées produites par deux chaînes d'analyse (`data/resultats/`), décrites dans `docs/donnees.md`. Toutes les analyses de `analyse/` partent de ces tables.

Après fusion des doublons de nom (section 7), le corpus compte 332 personnes. La gauche radicale représente 27 % d'entre elles et 62 % des textes.

### Interventions en séance (2022-2024)

4 099 interventions de la 16e législature, de juillet 2022 à juin 2024, avec leur texte intégral et l'adresse du compte rendu source (`data/an_2022_2024/interventions.csv`). Elles proviennent d'une collecte antérieure filtrée par mots-clés. Ce fichier est la seule source qui couvre la période antérieure au 7 octobre. Les analyses H5 n'y appliquent aucun modèle de langage : comptages et expressions régulières uniquement.

## 5. Instrument d'annotation et limites

L'annotation a été confiée à un modèle de langage (gpt-4o-mini) en deux passes : v3 sur l'ensemble du corpus, v4 sur les textes de sept fenêtres événementielles (`docs/codebook.md`). L'usage de modèles de langage pour annoter des textes politiques est désormais courant et peut égaler des annotateurs non experts (Gilardi, Alizadeh et Kubli, 2023), à condition d'être validé. Trois limites pèsent ici.

**Le modèle connaissait le camp de l'auteur.** Les deux prompts transmettaient le nom de l'auteur et son groupe parlementaire, et la v4 son bloc. La v3 fournissait en plus une table des « positions typiques » de chaque groupe. Un modèle placé dans ces conditions peut déduire la position d'un texte de l'étiquette de son auteur plutôt que de son contenu. L'effet attendu va toujours dans le même sens : il rapproche chaque texte de la position moyenne de son camp, ce qui gonfle les écarts entre blocs et réduit les écarts internes. La part de variance attribuée au bloc (H1) doit donc être lue comme un plafond.

**La position v4 est en partie lexicale.** Le prompt v4 imposait des règles : « cessez-le-feu » vaut au moins +1, « génocide » presque toujours +2. Une évolution du vocabulaire peut ainsi se traduire mécaniquement en évolution de la position.

**La validation humaine n'a pas été faite.** Le fichier présenté comme tel reproduisait les étiquettes du modèle (`docs/validation.md`). L'accord entre les annotations v3 et v4 (ρ de Spearman 0,86 sur 5 905 textes) mesure la stabilité du modèle d'une passe à l'autre, pas sa justesse : les deux passes partagent le même biais.

### Règle de lecture

Chaque chiffre est classé selon la nature de la mesure (`sorties/chiffres_cles.md`, colonne « Nature »).

| Nature | Exemples | Exposition au biais partisan du prompt |
|---|---|---|
| texte | volumes, concentration, mots discriminants, fréquence de « cessez-le-feu », interventions 2022-2024 | nulle |
| extraction | cible principale, appel au cessez-le-feu, demandes formulées | faible : le modèle relève une information présente dans le texte |
| jugement | position, registre émotionnel, cadre dominant | forte |

Un résultat n'est présenté comme établi que s'il repose sur une mesure de type texte ou extraction, ou si un jugement est confirmé par une mesure de type texte. C'est le cas de la baisse de l'appel au cessez-le-feu à gauche, retrouvée à l'identique par simple comptage du mot.

## 6. Mesures et tests

Toutes les mesures sont implémentées dans `analyse/mesures.py` et les tests dans `analyse/stats.py`.

**H1.** Part de variance de la position expliquée par le bloc, la fenêtre et l'arène : η² partiel tiré d'une analyse de variance de type II sur les 5 905 textes v4. Variation temporelle de chaque bloc : test d'hétérogénéité de Cochran sur les moyennes mensuelles pondérées par l'inverse de leur variance, avec I² (Higgins et Thompson, 2002) et τ, l'écart-type de la variation réelle une fois le bruit d'échantillonnage retiré (DerSimonian et Laird, 1986). Tendance de l'écart entre gauche radicale et droite et de la position relative du Centre (0 si le Centre est sur la droite, 1 s'il est sur la gauche radicale) : τ de Kendall sur les 18 mois où chaque bloc a au moins 15 textes. Appui textuel : signe mensuel des scores log-odds de « gaza » et « hamas » (Monroe, Colaresi et Quinn, 2008).

**H2.** Appel au cessez-le-feu, part de cibles israéliennes et de cibles « Hamas et alliés », registres émotionnels : proportions par fenêtre, tendance testée par le test de Cochran-Armitage (Armitage, 1955) en ordonnant les sept fenêtres. Indice d'attribution : (cibles israéliennes − cibles Hamas et alliés) / (somme des deux), de −1 à +1. Distance entre blocs pour chaque fonction du cadrage : divergence de Jensen-Shannon en base 2 (Lin, 1991), de 0 (distributions identiques) à 1 (disjointes). Triangulation : même test sur la part mensuelle de textes contenant « cessez-le-feu », « trêve » ou « cessation des hostilités ».

**H3.** Volume mensuel par bloc ; part de la gauche radicale ; nombre effectif de blocs, 1 / Σ pᵢ², qui vaut 4 si les quatre blocs parlent autant et 1 si un seul parle ; τ de Kendall sur 28 mois. Concentration : parts cumulées des N premiers auteurs et indice de Gini, sur les personnes dédoublonnées.

**H4.** Les 622 libellés libres de cible ont été regroupés en six familles par expressions régulières (`analyse/referentiel.py`) : Israël, Hamas et alliés, adversaires partisans français, exécutif français, populations et victimes, autres. Les victimes et les otages vont dans « populations », pas dans « Israël ». Part des cibles intérieures (adversaires et exécutif) par fenêtre ; comparaison de la fenêtre RAFAH aux autres par un khi² ; tendance par Cochran-Armitage.

**H5.** Interventions mentionnant explicitement Gaza, Israël, la Palestine, le Hamas ou la Cisjordanie (bornes de mot, pour que « Bahamas » ne compte pas). Volume mensuel, orateurs avant et après, recouvrement avec les auteurs du corpus 2023-2026. Fréquence de dix termes pour 10 000 mots avant et après, avec intervalles de confiance exacts de Poisson.

Les tests de tendance sur sept fenêtres ordonnées supposent des écarts comparables entre fenêtres, ce qui n'est pas le cas : ils indiquent une direction, pas une vitesse.

## 7. Corrections apportées aux données

1. **Doublons de nom.** Les comptes rendus écrivent « M. Aymeric Caron », les tweets « Aymeric Caron ». Les tables d'origine comptent 501 auteurs ; ils correspondent à 332 personnes. Les statistiques par personne sont recalculées après fusion. Les comptes de députés présents dans certaines tables d'origine (« 459 députés ») sont gonflés et ne sont plus cités.
2. **Deux définitions des fenêtres.** La chaîne variables et l'annotation v4 utilisent des fenêtres courtes (codebook). La chaîne lexicale a recalculé des fenêtres longues et contiguës sous les mêmes noms. Seules les fenêtres courtes sont utilisées ici.
3. **Tables homonymes divergentes.** Sur quinze tables portant le même nom dans les deux chaînes, neuf concordent exactement. Six mesurent autre chose : comparaisons avant/après événement, distances cosinus, indice de polarisation, convergence transpartisane, mots discriminants, variables par fenêtre. Exemple : pour l'ordonnance de la CIJ, le déplacement du Centre vaut −0,10 (p = 0,34) dans une chaîne et −0,44 (p = 0,02) dans l'autre. Aucun de ces résultats n'est utilisé.
4. **Variables dégénérées.** Sept variables v4 valent 100 % partout (codebook) et sont écartées.
5. **Mouvements individuels.** Les « députés qui changent d'avis » repérés par la chaîne lexicale reposent souvent sur très peu de textes (4 pour le premier cas du Centre), et l'ampleur du changement est corrélée négativement à l'écart initial au bloc (ρ = −0,39, p < 0,001). C'est la signature d'une régression vers la moyenne. Ces cas ne sont pas interprétés.

## 8. Ce que l'analyse ne permet pas de dire

Elle est descriptive. Les comparaisons avant/après n'ont pas de groupe témoin et ne mesurent pas d'effet causal des événements.

Elle porte sur la parole publique de ceux qui parlent. Les députés silencieux ne sont pas « neutres » : ils sont absents des données.

Elle ne distingue pas un député qui change d'avis d'un bloc dont la composition des orateurs change d'un mois à l'autre. Sans le texte, il n'est plus possible de suivre les mêmes personnes.

L'engagement sur X est plus fort pour les textes les plus tranchés, mais ces textes sont aussi ceux des comptes les plus suivis. Sans données par auteur, on ne peut pas séparer l'effet du contenu de celui de l'audience.

## 9. Reproduire

```
pip install -r requirements.txt
python -m analyse              # tables, chiffres clés et figures dans sorties/
python -m analyse.validation grille
```

Les chaînes `analyse_corpus/` exigent le corpus annoté (`data/corpus/`), qui n'est plus disponible ; leur code est conservé pour documenter la production des tables.

## Références

Armitage, P. (1955). Tests for linear trends in proportions and frequencies. *Biometrics*, 11(3), 375-386.

DerSimonian, R. et Laird, N. (1986). Meta-analysis in clinical trials. *Controlled Clinical Trials*, 7(3), 177-188.

Downs, A. (1972). Up and down with ecology: the « issue-attention cycle ». *The Public Interest*, 28, 38-50.

Entman, R. M. (1993). Framing: toward clarification of a fractured paradigm. *Journal of Communication*, 43(4), 51-58.

Gilardi, F., Alizadeh, M. et Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *Proceedings of the National Academy of Sciences*, 120(30).

Green-Pedersen, C. (2007). The growing importance of issue competition: the changing nature of party competition in Western Europe. *Political Studies*, 55(3), 607-628.

Higgins, J. P. T. et Thompson, S. G. (2002). Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine*, 21(11), 1539-1558.

Lin, J. (1991). Divergence measures based on the Shannon entropy. *IEEE Transactions on Information Theory*, 37(1), 145-151.

Manning, B. (1977). The Congress, the Executive and intermestic affairs: three proposals. *Foreign Affairs*, 55(2), 306-324.

Monroe, B. L., Colaresi, M. P. et Quinn, K. M. (2008). Fightin' words: lexical feature selection and evaluation for identifying the content of political conflict. *Political Analysis*, 16(4), 372-403.

Petrocik, J. R. (1996). Issue ownership in presidential elections, with a 1980 case study. *American Journal of Political Science*, 40(3), 825-850.
