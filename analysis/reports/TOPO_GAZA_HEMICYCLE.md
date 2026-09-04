# Gaza dans l'hémicycle : une polarisation sans dynamique

**Lecture d'ensemble des 78 tables de résultats, à destination d'un lectorat non spécialiste.**
Sami Nakib, septembre 2026. Sources : `analysis/data/results/` et `publication/data/results/`.

---

## La thèse en trois phrases

Vingt-huit mois de guerre, des dizaines de milliers de morts, sept événements majeurs, et aucun des quatre blocs de l'Assemblée nationale n'a changé de position sur Gaza. Ce qui a changé, ce sont les mots employés, le nombre de gens qui parlent, et l'usage intérieur que l'on fait du conflit. Le 7 octobre n'a pas divisé l'Assemblée : il a révélé une division qui préexistait, et il l'a figée.

Le corpus dit cela avec une netteté rare. Voici comment.

---

## 1. La loi de l'étiquette

Une analyse de variance sur 5 905 textes annotés décompose ce qui explique la position d'un texte (de −2, défense d'Israël, à +2, soutien à la Palestine).

| Facteur | Part de variance expliquée |
|---|---|
| Le bloc politique de l'auteur | **61,0 %** |
| La période (7 fenêtres événementielles) | 1,1 % |
| L'interaction bloc × période | 0,4 % |
| L'arène (Twitter ou hémicycle) | 0,08 % |
| Résidu (différences individuelles, bruit) | 37,5 % |

Traduction : pour prédire ce qu'un député dit de Gaza, il suffit de connaître son groupe. Deux ans d'histoire pèsent un centième. Le test de tendance de Mann-Kendall, appliqué bloc par bloc sur 28 mois, ne détecte aucune tendance significative nulle part (p entre 0,16 et 0,52). Les positions d'octobre 2023 sont celles de janvier 2026.

*Source : `anova_type2.csv`, `mann_kendall_bloc.csv`, `stance_mensuel.csv`.*

---

## 2. L'Assemblée ne parle pas de Gaza. Vingt députés en parlent.

Le corpus compte 10 774 textes signés par 501 noms. Leur répartition est d'une inégalité extrême.

| Part du corpus | Produite par |
|---|---|
| 7,4 % | un seul député (Aymeric Caron, 795 textes) |
| 13,4 % | deux députés (Caron et Thomas Portes) |
| 31,2 % | les 10 premiers |
| 45,1 % | les 20 premiers |
| 68,6 % | les 50 premiers |
| 100 % | 501 députés |

Le coefficient de Gini de cette distribution est de 0,78, un niveau d'inégalité supérieur à celui des revenus dans n'importe quel pays du monde. Le député médian a produit **4 textes en 28 mois**. 296 députés sur 501 en ont produit 5 ou moins.

Le « panel B4 » retenu pour les analyses longitudinales illustre l'ampleur du phénomène : 42 députés de la gauche radicale y produisent 6 069 textes, soit 56 % de tout ce que l'Assemblée a dit de Gaza.

Ce que l'on appelle « le débat parlementaire sur Gaza » est donc, quantitativement, l'activité d'un petit groupe de spécialistes-militants. Le reste de l'hémicycle se tait.

*Source : `trajectoires_individuelles.csv`, `panel_b4_composition.csv`.*

---

## 3. Le silence a une couleur

Ce petit groupe qui parle n'est pas politiquement neutre.

| Bloc | Tweets par député actif |
|---|---|
| Gauche radicale | 122,1 |
| Gauche modérée | 35,4 |
| Droite | 19,8 |
| Centre / Majorité | 16,9 |

Un député de la gauche radicale tweete sept fois plus sur le sujet qu'un député du Centre. Quand on classe les 188 députés du panel par visibilité (engagement reçu), le quintile le plus visible a une position moyenne de **+1,20** (nettement pro-palestinienne) ; le quintile le moins visible, **−0,78**. Ceux qu'on entend sont à gauche. Ceux qui se taisent sont au centre et à droite.

D'où un effet d'optique : 63 % des textes viennent de la gauche radicale, qui ne représente que 30 % des députés du corpus (138 sur 459). L'impression d'une Assemblée pro-palestinienne est un effet de volume, pas de majorité.

*Source : `activity_bias_by_bloc.csv`, `visibility_paradox_quintiles.csv`, `vue_ensemble.csv`.*

---

## 4. Deux noms propres

La mesure des « fighting words » (mots qui distinguent statistiquement le vocabulaire de gauche de celui de droite) donne, mois après mois, le même résultat sans une seule exception sur 27 mois :

- **« Hamas »** est le mot de la droite. Score de −11,1 en octobre 2023, encore −6,1 en octobre 2025.
- **« Gaza »** est le mot de la gauche. Score de +8,0 en octobre 2023, encore +3,1 en octobre 2025.

La gauche nomme un lieu, donc des habitants, donc des victimes. La droite nomme un acteur, donc un coupable. Ce n'est pas un désaccord sur la réponse à une question commune : c'est un désaccord sur la question posée.

Les cadres discursifs confirment. Le cadre humanitaire domine 77 % des textes de la gauche radicale ; le cadre sécuritaire domine 45 % de ceux de la droite (82 % dans l'annotation v4). Les cibles primaires disent la même chose : la gauche radicale vise Israël dans 61 % de ses textes et le Hamas dans 2 % ; la droite vise le Hamas dans 36 % et Israël dans 15 %.

Le Centre est le seul bloc dont les cibles sont équilibrées : Hamas 32 %, Israël 22,5 %. Il est aussi le seul dont les cadres se partagent presque à égalité entre sécurité (31 %) et humanitaire (29 %). C'est le seul bloc qui essaie de répondre aux deux questions.

*Source : `fighting_words_temporal.csv`, `frames_par_bloc.csv`, `target_primary_par_bloc.csv`.*

---

## 5. Le mot qui a changé de camp, et le mot qui a été abandonné

Si les positions ne bougent pas, les mots, eux, bougent. Trois trajectoires lexicales racontent l'évolution de la gauche.

**« Cessez-le-feu » : de la demande à l'oubli.** En octobre-novembre 2023, 26 à 34 % des textes de la gauche radicale contiennent le mot. C'est le fighting word de gauche le plus fort du premier mois (z = 6,0). À partir de l'été 2024, la fréquence s'effondre : 3 % en août 2024, 3,6 % en mai 2025, 1,2 % en septembre 2025. Un sursaut en janvier 2025 (25,7 %) quand un cessez-le-feu réel est signé, puis rien. La gauche a cessé de demander.

**« Génocide » : de l'absence à la sentence.** Absent des fighting words d'octobre à décembre 2023, le mot apparaît en janvier 2024, au moment de l'ordonnance de la Cour internationale de justice. Il culmine une première fois en mai 2024 (Rafah, z = 3,0), puis en mai-juillet 2025 (z = 4,6 ; 3,7 ; 3,2). Le mouvement est celui d'un passage de la revendication (un cessez-le-feu) à la qualification (un génocide). On ne demande plus, on nomme.

**« Israël » : de la droite à la gauche.** En 2023-2024, « Israël » est un mot de droite (z = −6,9 en octobre 2023, −4,5 en février 2024) : on défend Israël. À partir de mi-2025, il devient un mot de gauche (z = +2,4 en juillet, +2,3 en septembre). La gauche, qui ciblait « Netanyahou » et « le gouvernement israélien », en vient à nommer « Israël » tout court. L'adversaire n'est plus un gouvernement, c'est un État.

Pendant ce temps, la droite ne prononce pas « cessez-le-feu ». Jamais. Son maximum sur 28 mois est 13 % (décembre 2024, sur 15 textes). En janvier 2025, quand le cessez-le-feu est signé et que tous les autres blocs en parlent (Centre 29 %, gauche modérée 28 %, gauche radicale 26 %), la droite est à 0 %.

*Source : `ceasefire_lexical_v3.csv`, `fighting_words_temporal.csv`, `lag_adoption.csv`.*

---

## 6. La droite ne demande rien

L'annotation v4 relève la « demande clé » de chaque texte (cessez-le-feu, aide humanitaire, libération des otages, sanctions, reconnaissance d'un État, etc.).

| Bloc | Textes sans aucune demande |
|---|---|
| Droite | **près de 9 sur 10** (85,9 % « none », plus 11,8 % vides) |
| Centre / Majorité | 6 sur 10 |
| Gauche radicale | 4,6 sur 10 |
| Gauche modérée | 3,6 sur 10 |

Le discours de la droite sur Gaza est un discours de dénonciation, pas de politique : ses demandes les plus fréquentes après « rien » sont l'interdiction d'un jeu vidéo (4,9 %) et, loin derrière, un cessez-le-feu (4,5 %). La solution à deux États y pèse 2,6 %. Le bloc programmatique, c'est la gauche modérée : pression internationale (13 %), livraisons d'armes (12,5 %), responsabilité des médias (12,5 %), reconnaissance de l'État palestinien (9,4 %).

Même dans la fenêtre du 7 octobre, la droite ne mobilise l'argument de la légitime défense d'Israël que dans 12 % de ses textes. Elle ne défend pas une position israélienne ; elle condamne un ennemi.

*Source : `key_demands_par_batch_bloc.csv`, `variables_batch_specifiques.csv` (publication).*

---

## 7. Gaza comme arme intérieure

Cet ennemi est souvent français. Chez la droite, 18,6 % des cibles primaires sont des adversaires politiques nationaux (LFI 8,7 %, « extrême gauche », « la gauche », NUPES), auxquels s'ajoutent 4,7 % pour le gouvernement. Près d'un texte de droite sur quatre, parlant de Gaza, parle en réalité de politique française. Le mot « lfi » est un fighting word de droite chaque mois du corpus.

Et cette part obéit au calendrier électoral :

| Fenêtre | Part des cibles de droite tournées vers la politique intérieure |
|---|---|
| CHOC (oct.-déc. 2023) | 15,0 % |
| POST_CIJ (janv.-avr. 2024) | 12,5 % |
| **RAFAH (7 mai – 15 oct. 2024)** | **42,3 %** |
| POST_SINWAR (oct.-nov. 2024) | 34,9 % |
| MANDATS_CPI (nov. 2024 – janv. 2025) | 22,2 % |
| CEASEFIRE_BREACH (janv.-mars 2025) | 23,9 % |
| NEW_OFFENSIVE (mars 2025 – janv. 2026) | 29,6 % |

La fenêtre RAFAH contient les élections européennes du 9 juin 2024 et les législatives des 30 juin et 7 juillet. C'est le moment où la droite parle le plus de LFI en parlant de Gaza, et c'est aussi celui où « lfi » atteint son score le plus fort (z = −7,4 en mai 2024). Le miroir existe à gauche, plus discret : la gauche radicale vise le gouvernement français dans 10,7 % de ses textes.

*Source : `target_primary_par_batch_bloc.csv`, `fighting_words_temporal.csv`.*

---

## 8. Le 7 octobre, chiffré

La question de la condamnation de l'attaque du Hamas a occupé le débat public pendant des mois. Le corpus permet de la mesurer, dans la fenêtre CHOC (7 octobre – 31 décembre 2023).

| Bloc | Textes condamnant explicitement l'attaque | Textes soulevant la proportionnalité de la riposte |
|---|---|---|
| Gauche radicale | 11,4 % | 30,0 % |
| Gauche modérée | 23,2 % | 30,8 % |
| Centre / Majorité | 57,3 % | 2,4 % |
| Droite | 67,2 % | 0,6 % |

Deux blocs ont commenté deux événements différents. L'un parle de l'attaque, l'autre de la riposte. Les deux ont raison de dire que l'autre ne parle pas de ce qui compte.

*Source : `variables_batch_specifiques.csv` (publication).*

---

## 9. Le deuil dure trois mois, l'indignation dure toujours

Le registre émotionnel de chaque texte a été codé (indignation, deuil, solidarité, défiance, peur, colère, neutre). Sa distribution par fenêtre révèle une économie des émotions.

| | Fenêtre CHOC | Fenêtre NEW_OFFENSIVE |
|---|---|---|
| Gauche radicale, deuil | 14,1 % | 3,4 % |
| Gauche radicale, indignation | 50,8 % | 67,8 % |
| Droite, deuil | 1,1 % | 0,0 % |
| Droite, défiance | 50,3 % | 36,7 % |

Le deuil disparaît. L'indignation s'installe et croît. La droite, elle, n'a pratiquement jamais été dans le deuil, même en octobre 2023 (4 textes sur 352) : elle était dans la défiance, une émotion tournée vers un adversaire plutôt que vers une victime. Sur l'ensemble du corpus, la défiance représente 41 % des textes de droite, contre moins de 1 % à gauche.

Le Centre est le seul bloc où la peur apparaît de façon mesurable (11 textes en CHOC, 16 en NEW_OFFENSIVE). C'est aussi le seul bloc majoritairement neutre (44 %).

*Source : `emotional_register_v4.csv`, `emotional_register.csv`.*

---

## 10. Le marché de l'indignation

Twitter récompense-t-il la nuance ? Le corpus permet de croiser la position d'un tweet et l'engagement médian qu'il reçoit.

| Bloc | Engagement médian, texte neutre (0) | Engagement médian, texte extrême du camp | Rapport |
|---|---|---|---|
| Gauche radicale | 201 | 411 (stance +2) | × 2,0 |
| Centre / Majorité | 20 | 142 (stance −2) | × 7,1 |
| Droite | 32 | 98 (stance −2) | × 3,1 |

Dans trois blocs sur quatre, le texte le plus tranché est le plus partagé et le texte neutre le moins. Un député du Centre qui tweete une position nuancée reçoit sept fois moins d'attention que s'il tweete une position tranchée. Ce n'est pas que les députés sont extrêmes : c'est que seuls leurs textes extrêmes existent socialement. La gauche modérée fait exception, avec un profil plat, mais sur des effectifs faibles.

*Source : `engagement_bloc_stance.csv`.*

---

## 11. Deux scènes, deux grammaires

Globalement, l'arène ne change rien : contrôlant le bloc et le mois, le coefficient « Twitter » sur la position vaut −0,02 (p = 0,34). Mais ce résultat moyen cache deux choses.

D'abord une exception : la gauche radicale est significativement plus pro-palestinienne sur Twitter qu'en séance (+0,50, p = 0,011). Ses discours d'hémicycle sont plus mesurés que ses tweets. La gauche modérée fait l'inverse (−0,42, non significatif).

Ensuite un changement de grammaire. Les mots qui distinguent les discours en séance des tweets, pour la gauche radicale, sont : « vous » (z = −21,7), « avez » (−9,8), « allez » (−7,8), « votre » (−6,7), « bancs » (−6,6), « êtes » (−6,0). Côté Twitter : « victimes », « barbarie », « cessez ». Dans l'hémicycle, on s'adresse à un adversaire présent. Sur Twitter, on parle d'une victime absente. Même député, même sujet, deux actes de langage.

*Source : `twitter_vs_an.csv`, `regression_delta_stance.csv`, `fighting_words_twitter_vs_an.csv`.*

---

## 12. Le Centre : l'illusion du mouvement, et les vrais convertis

Le Centre passe pour le bloc « mobile ». Il faut regarder de plus près. Sur 28 mois, 7 mois comptent moins de 20 textes du Centre (6 en décembre 2024, 8 en janvier 2026). L'intervalle de confiance à 95 % de sa position mensuelle a une largeur moyenne de 0,66 point. Une bonne partie de sa « mobilité » est du bruit d'échantillonnage.

Sur les seuls mois où le Centre produit plus de 100 textes, la série est : −0,90 (oct. 2023), −0,81 (nov. 2023), −0,62 (mai 2024), −0,48 (mai 2025), −0,56 (juin 2025). Un adoucissement réel d'environ 0,4 point, lent, sans rupture événementielle nette.

Là où le Centre bouge vraiment, c'est individuellement. Les « movers forts » du corpus, ceux dont la position finale diffère le plus de la position initiale dans le sens pro-palestinien, sont presque tous du Centre : Erwan Balanant (−1,5 → +1,0), Pierre Cazeneuve (−1,0 → +1,0), Marie Lebec (−1,5 → +0,25), Constance Le Grip (−1,5 → 0), Laurent Croizier, Amélia Lakrafi. La droite, elle, a un déplacement individuel moyen de 0,00. Le Centre est le seul bloc où des personnes changent d'avis.

*Source : `stance_mensuel.csv`, `movers_caches.csv`.*

---

## 13. Ce que les outils sophistiqués n'ont pas vu

Le moteur d'analyse a aussi calculé des mesures affectives (valence, activation, dominance par lexique NRC-VAD), des fondements moraux (soin, équité, loyauté, autorité, sainteté), une polarisation entropique et une dimensionnalité effective. Résultat : rien. La valence oscille entre 0,49 et 0,52 pour tous les blocs et tous les mois. Les fondements moraux entre 0,16 et 0,21. L'analyse en composantes principales du vocabulaire individuel ne classe correctement que 43 % des députés dans leur bloc.

Ce n'est pas un échec sans intérêt. Cela dit que la polarisation n'est ni dans le ton, ni dans le vocabulaire moral, ni même dans le lexique pris globalement. Elle est dans deux choses précises : **les objets que l'on nomme** (Gaza ou Hamas, Israël ou LFI) et **les actes de langage** (demander ou dénoncer, pleurer ou défier). Les dictionnaires ne voient pas cela. La lecture des cibles et des demandes, oui.

*Source : `affective_vad_by_bloc_month.csv`, `moral_foundations_by_bloc_month.csv`, `entropic_polarization_temporal.csv`, `pca_coordonnees.csv`.*

---

## Synthèse : le conflit gelé de l'hémicycle

Mis bout à bout, ces treize résultats décrivent une **polarisation sans dynamique**.

1. Les positions sont fixées dès octobre 2023 et ne bougent plus (1, 12).
2. Ce qui évolue, c'est *qui* parle : de moins en moins de monde (211 députés actifs en octobre 2023, 34 en janvier 2026), de plus en plus concentré, de plus en plus à gauche (2, 3).
3. Ce qui évolue, ce sont les *mots* : la gauche passe de la demande à la sentence, de « cessez-le-feu » à « génocide », de « Netanyahou » à « Israël » (5).
4. Ce qui évolue, c'est l'*usage* : la droite convertit Gaza en argument contre LFI au rythme des élections (7).
5. Ce qui ne bouge jamais, c'est la question posée : pour un camp, que faire des victimes de Gaza ; pour l'autre, que faire du Hamas et de ceux qui ne le condamnent pas (4, 6, 8).

Gaza n'a pas changé les députés. Elle a montré qui ils étaient, et le mécanisme de récompense des réseaux sociaux s'est chargé de figer le portrait (10).

---

## Six articles possibles

| # | Titre de travail | Résultats mobilisés | Figure centrale |
|---|---|---|---|
| 1 | **Vingt députés** | 2, 3 | Courbe de concentration (top 1 / 5 / 20 / 50) |
| 2 | **Gaza ou Hamas : deux mots, deux questions** | 4, 8 | Double série mensuelle des scores de « gaza » et « hamas » |
| 3 | **Le mot abandonné et le mot qui a changé de camp** | 5 | « Cessez-le-feu » et « génocide » sur 28 mois |
| 4 | **Ce que la droite dit quand elle parle de Gaza** | 6, 7, 9 | Part de cibles intérieures par fenêtre, pic électoral |
| 5 | **Le marché de l'indignation** | 10, 11 | Engagement médian par position, trois blocs |
| 6 | **Deux ans de guerre, un pour cent** | 1, 12, 13 | Décomposition de variance ; série du Centre sur les mois pleins |

Chaque article tient sur des tables concordantes entre les deux moteurs, ou sur des tables uniques dont la spécification est nommée. Aucun ne dépend du diff-in-diff événementiel, qui reste à trancher.

---

## Ce que ces chiffres ne disent pas

- **Les positions sont annotées par un modèle de langage**, pas par des humains. L'accord entre deux versions du modèle est bon (ρ = 0,86), mais la validation humaine n'a pas encore été faite correctement. Tant qu'elle ne l'est pas, les positions individuelles sont des estimations.
- **Le corpus est déséquilibré** : 63 % des textes viennent d'un bloc. Toute moyenne « toutes tendances confondues » est trompeuse et n'apparaît nulle part ici.
- **Le design est descriptif**, avant/après, sans groupe de contrôle. Rien ici n'est causal.
- **Le texte brut n'est plus disponible.** Ces résultats sont des agrégats. On ne peut plus y revenir pour lire un tweet ou vérifier un cas.
