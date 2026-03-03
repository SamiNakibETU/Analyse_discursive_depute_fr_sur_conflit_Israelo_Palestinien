# Stratégie de contenu — X Threads et Série Substack

*Comment transformer 50 figures et 28 mois de données en contenu éditorial
pour les réseaux sociaux et une série longue.*

---

## 1. Principes éditoriaux

### Positionnement de l'auteur
**Sciences Po + Ingénieur + Data Scientist** : c'est précisément ce mix qui est
rare et crédible. Ne pas choisir entre les deux — c'est la valeur ajoutée.

> *« Je construis des ponts entre la donnée brute et l'interprétation politique.
> Je peux vous montrer le code ET vous expliquer ce que ça veut dire politiquement. »*

### Ton
- X/Bluesky : **incisif, chiffres d'abord, question à la fin** (engagement).
- Substack : **rigoureux mais accessible**, avec des histoires politiques qui donnent envie
  de lire et des méthodes expliquées simplement.

### Règle d'or des threads X
```
Hook (1 tweet) → Contexte (1-2 tweets) → Données / figure (2-3 tweets) 
→ Interprétation politique (1-2 tweets) → Limite / nuance (1 tweet) 
→ CTA → thread prochain
```

---

## 2. Série Substack — Architecture en 8 épisodes

### Titre de la série : *« Parole de député·e : 28 mois de discours sur Gaza »*

**Sous-titre** : *Une analyse computationnelle de ce que 459 élu·e·s français·es ont
vraiment dit — et comment ils l'ont dit.*

---

### Épisode 1 — **L'introduction : pourquoi compter les mots des députés ?**
**Angle** : La question de départ. Pourquoi construire ce corpus ?
Qu'est-ce qu'on apprend qu'on ne savait pas déjà ?

**Structure** :
- Le 7 octobre et le choc discursif immédiat
- Ce que les sondages ne voient pas : le positionnement *actif* des élus
- Présentation du corpus (10 774 textes, 459 députés, 28 mois)
- Carte de la série à venir

**Figures clés** : fig01 (volume), fig04 (déséquilibre), fig05 (violin stance)
**Longueur** : ~1 200 mots

---

### Épisode 2 — **Le Centre bouge, les extrêmes restent**
**Angle** : la dynamique la plus contre-intuitive du corpus.

**Structure** :
- Hypothèse naïve : la guerre polarise tout le monde
- Données : fig10 (stance ribbon 28 mois)
- Résultat : Gauche radicale et Droite stable ; Centre varie
- Pourquoi ? Théorie du *position-taking* (Mayhew 1974) expliquée simplement
- Limite : est-ce que LFI a toujours été pro-Palestine ou l'a-t-elle *devenu* ?

**Figures clés** : fig10, fig13 (zoom Centre)
**Longueur** : ~1 500 mots

---

### Épisode 3 — **Le paradoxe de la Droite** *(épisode phare)*
**Angle** : le résultat le plus fort du corpus, et le plus publiable.

**Structure** :
- Janvier 2025 : Macron appelle au cessez-le-feu
- Attendu : la Droite s'aligne ou se divise
- Réel : la Droite *durcit* (Δ stance = -1,03, p≈0,008)
- Explication : stratégie de différenciation partisane (Meguid 2005)
- Comparaison : RN a historiquement une posture pro-palestinienne sur certains sujets
  (anti-OTAN, souverainisme) → mais dans les données, ce n'est pas ce qu'on voit
- Question ouverte : est-ce spécifique à la France ou pan-européen ?

**Figures clés** : fig12 (event study), fig29 (ceasefire par batch)
**Longueur** : ~1 800 mots

---

### Épisode 4 — **Les mots qui séparent**
**Angle** : la polarisation lexicale.

**Structure** :
- Qu'est-ce que la distance cosinus ? (explication en 3 tweets reformatés)
- Les *fighting words* (Monroe 2008) expliqués
- Résultats : les 20 mots les plus discriminants gauche/droite
- Focus : l'évolution du mot « génocide » dans le corpus
- Diffusion lexicale du cessez-le-feu : qui adopte le mot en premier ?

**Figures clés** : fig21 (fighting words), fig24 (diffusion cessez-le-feu), fig19 (cosinus)
**Longueur** : ~1 500 mots

---

### Épisode 5 — **Twitter vs Assemblée nationale : deux masques du même député ?**
**Angle** : la question la plus politique de la série.

**Structure** :
- Hypothèse : les élus sont plus extrêmes sur Twitter que dans l'hémicycle
- Données : Δ stance = stance_Twitter − stance_AN par bloc
- Résultat : Centre et Gauche modérée ont un grand Δ ; Gauche radicale moins
  (cohérence de discours)
- Interprétation : la contrainte institutionnelle modère l'AN ; Twitter est
  l'arène du positionnement non filtré
- Implication : lequel des deux discours « compte » pour les électeurs ?

**Figures clés** : fig15 (Twitter vs AN Centre), fig64 (Δ stance violin), fig65 (Δ temporel)
**Longueur** : ~1 500 mots

---

### Épisode 6 — **La convergence tardive : gauche et centre ensemble, mais pourquoi ?**
**Angle** : la convergence transpartisane de fin de période.

**Structure** :
- Données : 35,5 % Gauche modérée + 30,3 % Centre → vocabulaire cessez-le-feu
- Timing : convergence s'accélère après mandats CPI (nov. 2024)
- Les « movers » : quels députés ont le plus changé de vocabulaire ?
- Convergence *lexicale* sans nécessairement convergence *politique*
- Limites : on ne sait pas si ces blocs se parlent (réseau manquant)

**Figures clés** : fig33 (convergence batch), fig35 (movers)
**Longueur** : ~1 400 mots

---

### Épisode 7 — **Les émotions dans le débat : colère, peur, dignité**
**Angle** : la dimension affective du discours.

**Structure** :
- Qu'est-ce que la Valence–Arousal–Dominance (VAD) ?
- La Gauche radicale a le niveau d'arousal le plus élevé (activations émotionnelles fortes)
- Le Centre a la valence la plus positive (discours d'espoir / solution)
- La Droite : forte dominance (assertivité) + faible valence
- Moral Foundations : Care vs Authority comme fracture gauche-droite

**Figures clés** : fig57 (VAD temporal), fig59 (MFT par bloc), fig62 (discours conflictuel)
**Longueur** : ~1 500 mots

---

### Épisode 8 — **Ce que les données ne peuvent pas dire — et ce qu'il faudrait faire**
**Angle** : les limites et la route vers une publication académique.

**Structure** :
- Récapitulatif des résultats principaux
- Ce que les données ne prouvent pas : causalité, représentativité des électeurs
- Ce qu'il manque : réseau, topic modeling, validation humaine
- Pourquoi c'est important politiquement
- Invitation à collaborer / commenter

**Longueur** : ~1 200 mots

---

## 3. Threads X/Bluesky — Architecture par résultat

### Thread 1 — Le hook de lancement

```
🧵 J'ai analysé 10 774 tweets et interventions à l'Assemblée nationale
de 459 députés français sur Gaza.

28 mois. 4 blocs politiques. 7 événements pivot.

Voici ce que les données disent — et ça va vous surprendre. 👇
```

**Tweets 2-3** : présenter le corpus (chiffres, fig01)
**Tweets 4-5** : le résultat principal (fig10 ribbon)
**Tweet 6** : le paradoxe de la Droite (cliff-hanger)
**Tweet 7** : CTA → série Substack

---

### Thread 2 — Le paradoxe de la Droite (thread phare)

```
🧵 En janvier 2025, quand Macron a appelé au cessez-le-feu,
j'attendais que la Droite s'aligne ou se divise.

Elle a fait l'inverse : elle a DURCI son discours.

Δ stance = -1,03 (p≈0,008). Voici pourquoi. 👇
```

**Tweets 2-3** : contexte politique (cessez-le-feu Centre)
**Tweets 4-5** : données + fig12
**Tweets 6-7** : interprétation (stratégie de différenciation partisane)
**Tweet 8** : question ouverte (est-ce que RN et LR divergent sur ce point ?)
**Tweet 9** : limite + CTA

---

### Thread 3 — Twitter vs AN (le masque et le visage)

```
🧵 Les députés français sont-ils les mêmes sur Twitter et à l'hémicycle ?

Spoiler : non. Et la différence varie selon le parti.

Thread 🧵 avec données sur 459 élu·e·s.
```

**Tweets 2-3** : présenter le design (Δ stance)
**Tweets 4-5** : résultats par bloc + fig64
**Tweet 6** : interprétation (contrainte institutionnelle)
**Tweet 7** : limite (causalité inconnue)
**Tweet 8** : CTA

---

### Thread 4 — Les mots qui séparent

```
🧵 Qu'est-ce qui distingue vraiment le discours de la Gauche radicale
de celui de la Droite sur Gaza ?

J'ai calculé les "fighting words" (Monroe 2008) sur 10 774 textes.

Résultat : 👇
```

**Tweets 2-3** : méthode en 2 tweets (log-odds, pas de jargon)
**Tweets 4-6** : les mots les plus discriminants (fig21)
**Tweet 7** : évolution du mot « génocide »
**Tweet 8** : CTA

---

### Thread 5 — Les émotions

```
🧵 La Gauche radicale parle de Gaza avec beaucoup plus d'émotion
que la Droite. Mais pas de la façon dont vous croyez.

VAD (Valence–Arousal–Dominance) sur 10 774 textes 👇
```

**Tweets 2-3** : expliquer VAD simplement
**Tweets 4-5** : résultats + fig57
**Tweet 6** : arousal prédit l'engagement (lien Vosoughi 2018)
**Tweet 7** : limite + CTA

---

## 4. LinkedIn — Format académique/professionnel

### Post type « résultat »
```
📊 [Résultat clé en 1 phrase]

Contexte : [2-3 lignes]
Méthode : [1-2 lignes]
Données : [chiffres clés]
Interprétation : [1-2 lignes]
Limite : [1 ligne]

→ Série complète sur Substack [lien]
```

### Post type « méthode »
Expliquer une méthode (fighting words, Wasserstein, BERTopic) en langage simple,
avec une application concrète au corpus. Cible : recruteurs tech + chercheurs.

---

## 5. Calendrier de publication suggéré

| Semaine | Contenu |
|---------|---------|
| S1 | Thread X #1 lancement + Substack Épisode 1 |
| S2 | Thread X #2 paradoxe Droite + Substack Épisode 2 |
| S3 | Substack Épisode 3 (paradoxe Droite, long) |
| S4 | Thread X #3 Twitter vs AN + Substack Épisode 4 |
| S5 | Thread X #4 fighting words + Substack Épisode 5 |
| S6 | Substack Épisode 6 (convergence) |
| S7 | Thread X #5 émotions + Substack Épisode 7 |
| S8 | Substack Épisode 8 (limites) + thread récap |

---

## 6. Ce qu'il te manque pour publier

| Élément manquant | Priorité | Action |
|-----------------|----------|--------|
| Figures export social (1080×1080) | ★★★ | `python src/export_figures_social.py` |
| Profil Substack créé | ★★★ | Créer + bio positionnée Sciences Po + Data |
| 3–4 figures « lisibles » pour grand public | ★★★ | Simplifier axes, ajouter annotations |
| Validation humaine (crédibilité) | ★★ | `python src/validation_humaine.py` |
| Résultat RN vs LR séparés | ★★ | Pour thread controversé mais intéressant |
| 1 figure animée / GIF temporel | ★ | Matplotlib animation ou Flourish |
