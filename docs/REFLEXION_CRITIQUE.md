# Réflexion critique — Analyse socratique du projet

*Ce document adopte une posture de questionnement socratique : pas de complaisance, des questions
qui dérangent, des forces à confirmer et des failles à corriger avant toute publication.*

---

## 1. Ce que ce projet fait bien — les forces réelles

### 1.1 Originalité de la combinaison arènes × temps
Le projet est l'un des rares à analyser simultanément Twitter/X **et** l'Assemblée nationale
sur **28 mois consécutifs** pour le même corpus de locuteurs (459 députés identifiés).
La plupart des études (Barberá, Conover) traitent soit Twitter seul, soit le Parlement seul.
Cette double fenêtre est une contribution méthodologique réelle.

### 1.2 Richesse temporelle (7 batches, 6 event studies)
La segmentation en 7 périodes articulées autour d'événements géopolitiques réels (CIJ, mandats CPI,
cessez-le-feu) dépasse la majorité des études qui utilisent un unique avant/après.
Le *paradoxe de la Droite* (durcissement au moment du cessez-le-feu Centre, Δ = -1,03, p≈0,008)
est un résultat contre-intuitif et publiable.

### 1.3 Empilement des méthodes de polarisation
Cosinus + Wasserstein + entropique Bao & Gill + VAD + MFT : c'est cinq lentilles de mesure
de la polarisation sur le même corpus. C'est ce qui distingue une étude de niveau thèse/article
d'une étude de niveau rapport.

---

## 2. Les questions qui dérangent — les failles

### 2.1 « Annotation de stance » : qui annote ? Comment ? Avec quel modèle ?

> *Quelle est la nature exacte de l'annotation v3 et v4 ?*

Si l'annotation est faite par un LLM (GPT-4, Mistral…), il faut :
- Déclarer explicitement le modèle, la version, la date, le prompt complet.
- Calculer le biais du modèle : tous les LLM ont des biais documentés sur le conflit
  israélo-palestinien (voir Navigli et al. 2023, *LLMs are political*).
- Le Spearman 0,86 entre v3 et v4 mesure la *consistance d'un même annotateur (LLM)*, pas
  la *fiabilité* au sens psychométrique. Ce n'est pas un accord inter-annotateurs.

**Question socratique** : si deux instances du même modèle s'accordent à 86 %, est-ce une
validation ou une mesure de bruit stochastique ?

**Recommandation concrète** : annoter 150 textes avec au moins 2 annotateurs humains
(voir `src/validation_humaine.py`) et calculer le Cohen's Kappa. Un κ ≥ 0,60 (accord
substantiel) est le seuil standard pour valider l'annotation assistée par LLM.

### 2.2 Déséquilibre du corpus : Gauche radicale ≈ 63 %

> *LFI tweete plus que les autres partis. Est-on en train de mesurer une différence de stance
> ou une différence de volume d'expression ?*

Les métriques moyennées par bloc sont biaisées si les blocs ont des distributions de volume
radicalement différentes. Le sous-échantillonnage stratifié (fig48) partiellement répond,
mais la *méthodologie d'agrégation* n'est pas décrite avec assez de précision.

### 2.3 Fusion LR + RN = « Droite » : une décision analytique forte

> *LR (gaulliste libéral) et RN (nationaliste populiste) ont des positions très différentes
> sur la politique étrangère. Les regrouper crée-t-il artificiellement la « stabilité de la Droite » ?*

C'est probablement le choix le plus contestable. RN est historiquement pro-Poutine/eurosceptique
avec une posture pro-palestinienne croissante ; LR est plus pro-atlantiste.
Ce regroupement mérite un test de robustesse explicite (LR seul vs RN seul).

### 2.4 Event studies sans hypothèse de tendances parallèles

> *Peut-on appeler cela un « diff-in-diff » sans vérifier les tendances parallèles ?*

Le projet le signale lui-même dans METHODOLOGIE.md § 8 (analyse descriptive, pas diff-in-diff
classique). Mais le visuel (fig12) ressemble à un event study. Le risque de sur-interprétation
est réel si le lecteur non averti confond corrélation temporelle et causalité.

**Suggestion socratique** : retitrer fig12 « Shift temporel associatif » et ajouter un
avertissement explicite dans la légende.

### 2.5 Absence d'analyse de réseau

> *On sait ce que les députés disent, mais pas à qui ils parlent, qui les retweet, qui les cite.*

La structure sociale du discours est invisible. Est-ce que les « transfuges » (fig35–40)
constituent un cluster au sein du réseau de mention ? Ou sont-ils isolés ?
Sans cette analyse, la convergence transpartisane *lexicale* reste non vérifiable sur
le plan *interactionnel*.

### 2.6 Absence d'analyse thématique (topic modeling)

> *Quels sujets spécifiques mobilisent chaque bloc ?*

Les cadres (HUM, SEC, LEG…) sont définis *a priori* par le prompt LLM. Un topic modeling
inductif (BERTopic sur CamemBERT) permettrait de découvrir des thèmes *émergents* — peut-être
surprenants — et de valider la structure a priori.

---

## 3. Questions de positionnement

### 3.1 Quelle est la thèse centrale ?

> *Si tu devais résumer le projet en une phrase pour un jury de thèse, que dirais-tu ?*

Proposition actuelle des auteurs (implicite) :
*« Les députés français ont des positionnements discursifs différenciés par bloc face au conflit,
mais la convergence transpartisane tardive et le paradoxe de la Droite montrent que la géopolitique
peut perturber les alignements partisans attendus. »*

C'est **correct** mais **descriptif**. Pour un niveau article, il faudrait une thèse
causale ou une contribution théorique (ex. : *« les événements de haute saillance
internationale activent des mécanismes de différenciation partisane plutôt que de convergence »*).

### 3.2 À qui s'adresse ce projet ?

| Audience | Ce qui parle | Ce qui manque |
|----------|-------------|---------------|
| Recruteur data/NLP | Pipeline, 5 méthodes de polarisation | Benchmark de performance LLM annotation |
| Sciences Po | Résultats politiques, batches | Cadrage théorique en political science |
| Journaliste | Résultats sur le paradoxe de la Droite | Visualisations plus lisibles |
| Académique | Méthodes rigoureuses | Validation humaine, test de robustesse LR/RN |

**La force du projet est de pouvoir parler à toutes ces audiences. Sa faiblesse est
de ne pas avoir encore optimisé le message pour aucune.**

---

## 4. Les résultats vraiment cool — à mettre en avant

### 🔥 Résultat 1 : Le paradoxe de la Droite
Δ stance = -1,03 au moment où le Centre appelle au cessez-le-feu (p≈0,008).
C'est le résultat le plus publiable : contre-intuitif, significatif statistiquement,
interprétable en termes de *strategic differentiation* (Meguid 2005).

**Lecture politologique** : la Droite ne converge pas parce que le cessez-le-feu est devenu
un marqueur identitaire de la Gauche. Se rallier = perdre de la lisibilité politique.

### 🔥 Résultat 2 : Le Centre réagit, les extrêmes restent stables
Lois de cohésion partisane vs réactivité aux événements : les partis de gouvernement
(plus contraints par les positions diplomatiques officielles) bougent ; les partis d'opposition
(LFI, RN) restent sur leur position de départ indépendamment des événements.

**Lecture politologique** : stratégie de *position-taking* (Mayhew 1974) vs discours de
*gouvernance responsable*. L'érosion du Centre après Rafah est compatible avec une
pression interne des élus de circonscription à forte communauté.

### 🔥 Résultat 3 : Convergence lexicale sans convergence interactionnelle
35,5 % de la Gauche modérée et 30,3 % du Centre adoptent le vocabulaire cessez-le-feu —
mais on ne sait pas si ces blocs se parlent. C'est une convergence *de surface*, peut-être.

**Lecture politologique** : la diffusion lexicale sans réseau (Conover 2011) peut signifier
un effet de *bandwagon médiatique* plutôt qu'une vraie négociation discursive.

### 🔥 Résultat 4 : Polarisation lexicale maximale en décembre 2024
La distance cosinus GR–Droite est maximale exactement au moment des mandats CPI
(novembre–décembre 2024). L'événement juridique amplifie la polarisation lexicale.

---

## 5. Synthèse — Que faire avec ce projet ?

| Action | Priorité | Impact recruteur | Impact académique |
|--------|----------|-----------------|-------------------|
| Validation humaine 150 textes | ★★★ | Élevé | Indispensable |
| Séparer LR et RN | ★★★ | Moyen | Fort |
| Analyse réseau députés | ★★★ | Très élevé | Fort |
| BERTopic topic modeling | ★★ | Élevé | Moyen |
| Déclarer modèle LLM + biais | ★★★ | Élevé | Indispensable |
| Retitrer event study fig12 | ★★ | Faible | Fort |
| Changepoints sur séries VAD | ★★ | Moyen | Fort |
| Comparaison internationale | ★ | Moyen | Fort |
