# Résultats

Tous les chiffres de ce document sont produits par `python -m analyse` et listés, avec leur source et la nature de la mesure, dans `sorties/chiffres_cles.md`. Les figures citées sont dans `sorties/figures/`. La méthode et ses limites sont dans `docs/methodologie.md`.

## En bref

Le 7 octobre n'a converti aucun bloc. Les camps étaient formés avant la guerre, et un débat de mai 2023 en donnait déjà la distribution des rôles. La guerre a multiplié par vingt-sept le volume de parole en séance, puis l'attention est retombée en se concentrant sur la gauche radicale, propriétaire de l'enjeu.

Ce qui a bougé, ce sont les composantes du discours. La gauche a abandonné la demande de cessez-le-feu pour la qualification du conflit, quand le Centre reprenait cette demande à son compte. La droite, puis le Centre, ont tourné leurs critiques vers des adversaires français, d'abord pendant la campagne européenne de 2024, puis durablement.

On peut le résumer d'une formule : des positions figées, des cadrages mobiles. La guerre à Gaza a moins changé ce que les députés pensent que ce dont ils parlent quand ils en parlent.

| | Résultat | Solidité |
|---|---|---|
| H5 | Avant le 7 octobre, le conflit est un sujet de niche, porté par un seul débat ; après, il devient une question de guerre et non plus d'occupation | Établi (texte intégral, sans modèle) |
| H1 | Les écarts entre blocs sont maximaux dès octobre 2023 et ne se réduisent pas | Établi pour la séparation lexicale ; l'ampleur de l'écart de position est un plafond |
| H3 | L'attention retombe et se concentre : vingt personnes produisent la moitié du corpus, la gauche radicale une part croissante | Établi (comptages) |
| H2 | L'appel au cessez-le-feu quitte la gauche et gagne le Centre ; la gauche n'accuse plus qu'Israël | Établi (extraction confirmée par le texte seul) |
| H4 | La droite, puis le Centre, font de Gaza une affaire de politique intérieure | Établi (extraction), pic électoral sur un effectif réduit |

## 1. Avant le 7 octobre, un seul débat (H5)

De juillet 2022 au 6 octobre 2023, les interventions en séance qui nomment Gaza, Israël, la Palestine, le Hamas ou la Cisjordanie sont rares : 123 en quatorze mois. 79 d'entre elles ont eu lieu le même jour, le 4 mai 2023, lors de l'examen de la proposition de résolution n° 1082, déposée par le groupe de la Gauche démocrate et républicaine (Jean-Paul Lecoq), qui condamnait « l'institutionnalisation par l'État d'Israël d'un régime d'apartheid ». En dehors de ce débat, l'hémicycle évoque le conflit trois fois par mois en moyenne.

Après le 7 octobre, la moyenne passe à 84 interventions par mois de séance, soit vingt-sept fois plus que le rythme de fond (figure 10). Le nombre de députés qui en parlent passe de 42 en quatorze mois à 154 en neuf mois.

Le débat du 4 mai 2023 compte parce qu'il donne la distribution des rôles. Y prennent la parole Aurore Bergé, Meyer Habib, Julien Odoul, Jérôme Guedj, Aymeric Caron, Sabrina Sebaihi et Elsa Faucillon : plusieurs des voix qui domineront le débat après le 7 octobre. Aymeric Caron, premier producteur du corpus 2023-2026, en fait partie, comme Julien Odoul, premier à droite. Au total, les trente personnes qui étaient déjà intervenues sur le sujet avant la guerre produisent 18 % du corpus suivant. La guerre n'a pas inventé les porte-parole de chaque camp. Elle leur a donné une audience, et en a fait entrer de nouveaux, comme Thomas Portes ou Alma Dufour.

Le vocabulaire change de nature (figure 11). Avant le 7 octobre, la question posée au Parlement est celle de l'occupation : « apartheid » revient 31 fois pour 10 000 mots, « colonisation » et « deux États » une dizaine de fois chacun. Après, c'est une question de guerre : « terrorisme » triple (de 11 à 34 pour 10 000 mots), « otages » est multiplié par neuf, « humanitaire » par dix, et « cessez-le-feu », absent auparavant, apparaît. « Apartheid » tombe à 1. Le lexique de la solution politique (« deux États », « colonisation ») recule d'environ 60 %. Seul « droit international » garde à peu près la même fréquence.

Un détail compte : l'antisémitisme est déjà très présent avant la guerre (20 occurrences pour 10 000 mots). Le 4 mai 2023, 24 des 103 interventions de la journée l'évoquent. Une députée RN y décrit un « antisionisme virulent rarement très loin de l'antisémitisme » ; Aymeric Caron répond au « bruit » selon lequel le mot « apartheid » relèverait de l'antisémitisme, sous les « Bien sûr ! » des bancs du RN. Le répertoire qui opposera les camps après le 7 octobre était en place sept mois plus tôt.

Limite : l'« avant » repose pour les deux tiers sur une seule journée de débat, consacrée à un texte qui mettait l'apartheid à l'ordre du jour. La comparaison montre un changement d'agenda, pas l'évolution d'un vocabulaire qui aurait été stable auparavant.

## 2. Des camps figés (H1)

Sur 28 mois, les positions moyennes des quatre blocs dessinent quatre lignes à peu près horizontales (figure 1). La gauche radicale se tient autour de +1,6 sur une échelle de −2 à +2, la gauche modérée autour de +1,0, le Centre autour de −0,8, la droite autour de −1,4. L'écart entre gauche radicale et droite vaut 2,9 points en moyenne, entre 2,4 et 3,3 selon les mois, sans aucune tendance (τ de Kendall, p = 0,71).

Les moyennes mensuelles bougent un peu plus que ne le voudrait le seul hasard de l'échantillonnage : le test d'hétérogénéité est significatif dans les quatre blocs. Mais l'ampleur de ces mouvements, une fois le bruit retiré, est faible : un écart-type de 0,13 point pour la gauche radicale, 0,15 pour la droite, 0,19 pour le Centre, 0,26 pour la gauche modérée. L'écart entre les deux pôles est onze fois plus grand que la plus forte de ces fluctuations. Et elles ne s'accumulent pas : aucun bloc ne dérive.

Le Centre se situe en moyenne à 20 % du chemin entre la droite et la gauche radicale. Cette position glisse un peu vers le milieu en 2025 (0,33 en mai, 0,38 en septembre, le mois où la France reconnaît l'État de Palestine), mais la tendance n'est pas significative (p = 0,13) et repose sur des mois à faible effectif.

Ces chiffres de position sont des jugements du modèle, qui connaissait le groupe de l'auteur. Ils exagèrent probablement la séparation des blocs. La part de variance qu'ils attribuent au bloc (62 %, contre 3 % au moment et 0,2 % à l'arène, figure 2) est donc un plafond.

La stabilité du clivage se lit pourtant aussi dans le texte seul, sans passer par le modèle. Chaque mois, on peut calculer quels mots distinguent le plus le vocabulaire de la gauche de celui de la droite. « Hamas » est un mot distinctif de la droite 27 mois sur 27. « Gaza » est un mot distinctif de la gauche 26 mois sur 27. La gauche nomme un lieu et ses habitants ; la droite nomme un acteur et sa responsabilité. Ce partage ne varie pas de toute la période.

## 3. Une attention qui retombe et se resserre (H3)

Le volume suit le cycle décrit par Anthony Downs : un pic, puis un plateau bas. 1 353 textes en octobre 2023, puis une médiane de 319 par mois, avec des rebonds lors des grands épisodes militaires ou diplomatiques (figure 7).

Le déclin n'est pas réparti également. La part de la gauche radicale dans le volume mensuel passe de 48 % en octobre 2023 à 85 % en janvier 2026 (tendance significative, p = 0,03). Le nombre effectif de blocs qui prennent la parole, qui vaudrait 4 si chacun parlait autant, passe de 3,1 à 1,4. Sur X, un député de la gauche radicale qui s'exprime sur le sujet publie en moyenne 122 tweets, contre 20 à droite et 17 au Centre.

La parole est aussi très concentrée entre les personnes (figure 8). Sur 332 personnes, la première produit 8 % du corpus, les dix premières un tiers, les vingt premières près de la moitié (49 %). La moitié des auteurs ont écrit 6 textes ou moins en 28 mois. L'indice de Gini de cette distribution vaut 0,77.

Le résultat a une conséquence pratique pour quiconque lit ce débat : l'image qu'il donne de l'Assemblée est celle d'un petit nombre de députés, très majoritairement de gauche radicale. La gauche radicale représente 27 % des personnes du corpus et 62 % de ses textes. Une moyenne « de l'Assemblée » calculée sur les textes serait une moyenne de ces vingt voix.

C'est la logique de la propriété des enjeux. La France insoumise a fait de la Palestine un marqueur, jusqu'à placer Rima Hassan sur sa liste aux élections européennes de 2024. Les autres partis n'ont pas intérêt à occuper durablement un terrain où leur électorat est divisé ou indifférent. Ils parlent lors des pics, puis se taisent.

## 4. Des cadrages qui bougent (H2)

Une position sur une échelle de −2 à +2 écrase quatre choses distinctes : la définition du problème, la désignation d'un responsable, l'évaluation morale et le remède proposé. Pris séparément, ces quatre éléments ne bougent pas de la même façon.

### Le remède : le cessez-le-feu change de camp

C'est le mouvement le plus net du corpus (figure 3). Dans les cinq semaines qui suivent le 7 octobre, 37 % des textes de la gauche radicale et 42 % de ceux de la gauche modérée appellent explicitement à un cessez-le-feu, contre 3 % au Centre et 1 % à droite. Puis la demande s'effondre à gauche : 16 % au printemps 2024, 6 % fin 2024, 8 % au printemps 2025 pour la gauche radicale (tendance, z = −16,9). Au Centre, elle progresse de 3 % à 11-15 % et s'y maintient (z = +2,8). Dès la mort de Sinwar, en octobre 2024, le Centre appelle plus souvent au cessez-le-feu que la gauche radicale.

Ce résultat ne dépend pas du biais du modèle. La simple présence des mots « cessez-le-feu », « trêve » ou « cessation des hostilités » dans le texte donne la même pente : de 19 % à 7 % des textes de la gauche radicale entre la première et la seconde moitié de la période, de 6 % à 9 % au Centre.

La gauche n'a pas changé de camp. Elle a changé de registre. À la demande s'est substituée la qualification : « génocide » devient un mot distinctif de la gauche à partir de janvier 2024, au moment de l'ordonnance de la Cour internationale de justice, et le reste ensuite, avec un pic au printemps 2025. On ne réclame plus l'arrêt des combats, on qualifie ce qui se passe. Le Centre, à l'inverse, adopte la demande à mesure qu'elle devient la ligne du gouvernement.

### L'attribution : la gauche n'accuse plus qu'Israël, le Centre quitte le pôle Hamas

L'indice d'attribution vaut +1 si un bloc ne vise qu'Israël et −1 s'il ne vise que le Hamas et ses alliés (figure 4). Dans la fenêtre du 7 octobre, la gauche radicale est à +0,73 et la gauche modérée à +0,47 : une partie de leurs textes vise encore le Hamas. Dès la fenêtre suivante, les deux gauches dépassent +0,85 et n'en redescendent plus. Le Centre part de −0,45, proche de la droite (−0,56), puis oscille autour de zéro à partir du printemps 2024. La droite reste du côté Hamas presque toute la période.

Le 7 octobre lui-même se lit dans ces données. Dans les cinq semaines qui suivent l'attaque, 67 % des textes de droite et 57 % de ceux du Centre condamnent explicitement l'attaque du Hamas, contre 23 % à gauche modérée et 11 % à gauche radicale. Inversement, 30 % des textes de gauche soulèvent la question de la proportionnalité de la riposte, contre 2 % au Centre et moins de 1 % à droite. Les deux camps commentent deux événements différents : l'attaque pour les uns, la riposte pour les autres.

### L'évaluation morale : le deuil s'éteint, l'indignation s'installe

À gauche radicale, le deuil passe de 14 % des textes dans la fenêtre du 7 octobre à 3 % au printemps 2025, pendant que l'indignation monte de 51 % à 68 % (figure 6). À droite, la défiance, une émotion tournée vers un adversaire plutôt que vers une victime, domine dès le premier jour (50 % des textes) puis recule (37 %), sans que le deuil ne s'installe jamais : 4 textes sur 352 dans la première fenêtre. Ces registres sont des jugements du modèle et doivent être confirmés par la validation humaine.

### Où se situe le Centre ?

La divergence de Jensen-Shannon mesure, pour chaque fonction du cadrage, à quel point deux blocs parlent différemment (figure 5). Le Centre est presque indiscernable de la droite sur l'attribution (0,03) et la définition du problème (0,08) : il désigne les mêmes responsables et pose le problème en termes de sécurité. Il est en revanche plus proche de la gauche modérée que de la droite sur l'évaluation morale (0,09 contre 0,18) : son registre est neutre ou attristé, rarement défiant. Le Centre pense le conflit comme la droite et en parle sur le ton de la gauche modérée.

Entre gauche radicale et droite, la divergence la plus forte porte sur la définition du problème (0,47), devant l'attribution (0,34). Le désaccord est en amont : il porte sur la nature de la question avant de porter sur sa réponse.

### Qui propose quelque chose ?

89 % des textes de droite ne formulent aucune demande, contre 70 % au Centre, 48 % à gauche radicale et 40 % à gauche modérée. La gauche modérée est le bloc le plus programmatique : pression internationale, arrêt des livraisons d'armes, reconnaissance de l'État de Palestine. Le discours de droite sur Gaza dénonce ; il prescrit rarement.

## 5. Un conflit domestiqué (H4)

Quand un député parle de Gaza, qui vise-t-il ? Sur l'ensemble des fenêtres, 26 % des textes de droite ont pour cible principale un acteur politique français, et 20 % un adversaire partisan, au premier rang duquel La France insoumise. C'est 13 % et 9 % au Centre. À gauche radicale, la cible intérieure est surtout le gouvernement : 16 %, dont 3 % seulement d'adversaires partisans.

La part des cibles intérieures à droite double presque pendant la fenêtre du 1er mai au 15 juin 2024 : 45 % contre 24 % dans les autres fenêtres (p < 0,001, sur 67 textes, figure 9). Cette fenêtre couvre la campagne des élections européennes, l'épisode du drapeau palestinien brandi dans l'hémicycle le 28 mai et la dissolution du 9 juin. Le mot « lfi » est un mot distinctif de la droite chacun des 23 mois où il apparaît, avec un maximum en mai 2024.

Le pic n'est pas une parenthèse. Après la campagne, la part de cibles intérieures à droite ne revient pas à son niveau d'octobre 2023 (17 %) : entre 25 % et 41 % dans les fenêtres suivantes. Sur l'ensemble de la période, la tendance est nettement croissante à droite (z = +4,4) et au Centre (z = +3,4). Elle est décroissante à gauche radicale (z = −4,0), qui vise de plus en plus Israël et de moins en moins le gouvernement.

Les deux camps cessent ainsi de parler de la même chose. Pour la gauche radicale, Gaza reste une question internationale dont le responsable est Israël. Pour la droite et, de plus en plus, pour le Centre, c'est aussi une question française, dont l'objet est La France insoumise. C'est le mécanisme décrit par la compétition sur les enjeux : faute de pouvoir disputer à la gauche la propriété de la cause palestinienne, ses adversaires déplacent le débat sur un terrain qu'ils possèdent, l'antisémitisme et les limites de l'arc républicain.

## 6. Ce que les données ne confirment pas

Plusieurs résultats présentés dans les versions antérieures de ce projet ne résistent pas à la vérification.

**Le basculement du Centre après l'ordonnance de la CIJ.** Les deux chaînes d'analyse donnent des résultats opposés pour le même événement et le même bloc (−0,10, non significatif, contre −0,44, p = 0,02). Le résultat dépend des bornes retenues et n'est pas utilisé.

**Les « convertis » du Centre.** Les députés présentés comme ayant le plus changé d'avis ont souvent écrit moins de dix textes, et l'ampleur des changements individuels est corrélée à l'écart initial au bloc (ρ = −0,39), signature d'une régression vers la moyenne.

**La polarisation lexicale croissante.** Les deux chaînes mesurent la distance cosinus entre les vocabulaires des blocs avec des vectorisations différentes. L'une donne des valeurs entre 0,09 et 0,56, l'autre entre 0,64 et 0,99. Aucune des deux ne montre de tendance robuste.

**Le marché de l'indignation.** Les textes les plus tranchés reçoivent plus d'engagement sur X que les textes neutres : deux fois plus à gauche radicale, sept fois plus au Centre. Mais ce sont aussi ceux des comptes les plus suivis. Sans données par auteur, on ne peut pas attribuer l'écart au contenu plutôt qu'à l'audience.

**Le ton et la morale mesurés par dictionnaire.** Les scores de valence, d'activation et de fondements moraux varient très peu (valence entre 0,49 et 0,52 pour tous les blocs et tous les mois). La polarisation de ce débat n'est pas dans le ton général ni dans le vocabulaire moral ; elle est dans les objets nommés et dans les actes de langage, demander ou dénoncer.

**Twitter contre hémicycle.** Une fois le bloc et le mois contrôlés, l'arène n'a pas d'effet sur la position (−0,02, p = 0,34). L'écart propre à la gauche radicale (+0,50 sur X, p = 0,01) repose sur un jugement du modèle et sur des député-mois souvent faiblement fournis.

## 7. Interprétation

Les études de campagne distinguent depuis longtemps trois effets possibles d'un choc d'information : il peut activer des prédispositions latentes, renforcer des convictions existantes ou convertir (Lazarsfeld, Berelson et Gaudet, 1944). Le 7 octobre et la guerre qui suit ont produit les deux premiers, pas le troisième. Le clivage existait, ses porte-parole aussi. La guerre l'a rendu central pendant quelques mois, puis l'a laissé à ceux qui le possédaient.

Cette absence de conversion n'empêche pas le mouvement. Elle le déplace. Les positions agrégées ne bougent pas parce que chaque bloc ajuste les composantes de son discours dans des directions qui se compensent : la gauche durcit sa qualification en renonçant à sa demande, le Centre adoucit son attribution en adoptant la demande abandonnée par la gauche, la droite garde sa position en changeant d'adversaire. Un indicateur unique de position ne voit rien de tout cela. C'est l'argument principal pour décomposer le cadrage.

Deux mécanismes de compétition partisane rendent compte de ces déplacements. Le premier est l'appropriation : un parti qui fait d'une cause son marqueur la garde quand l'attention retombe, et finit par être le seul à en parler, ce qui en fait aussi la cible naturelle de ses adversaires. Le second est la domestication : un conflit étranger devient un instrument de la compétition intérieure, plus fortement en campagne électorale, puis de façon durable. Le cas français montre les deux à l'œuvre en même temps, et leur combinaison produit le dialogue de sourds que l'on observe : un camp parle de Gaza, l'autre de ceux qui parlent de Gaza.

## 8. Ce qu'il reste à établir

La validation humaine en aveugle des positions (`docs/validation.md`) dira si le biais partisan du prompt est important. Si l'écart entre modèle et humain est faible, les résultats de position pourront être cités sans réserve ; s'il est fort, seuls les résultats de type texte et extraction resteront.

Une ré-annotation des textes qui subsistent, sans indiquer au modèle l'auteur ni son groupe, permettrait de mesurer ce biais à grande échelle. Les interventions en séance peuvent être recollectées intégralement depuis l'open data de l'Assemblée nationale, y compris pour la 17e législature.

Enfin, la comparaison avant/après pourrait être étendue aux tweets de 2022-2023, si une source d'archives est accessible, pour vérifier que la distribution des rôles observée le 4 mai 2023 en séance vaut aussi sur les réseaux.

## Référence ajoutée

Lazarsfeld, P. F., Berelson, B. et Gaudet, H. (1944). *The People's Choice: How the Voter Makes Up His Mind in a Presidential Campaign*. New York, Duell, Sloan and Pearce.
