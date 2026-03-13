# Résultats du pipeline NLP

Corpus de députés français sur le conflit israélo-palestinien (oct. 2023 - jan. 2026)

## 1) Périmètre et filtrage

- Tweets bruts: 11 735
- Interventions AN brutes: 5 633
- Critères de filtrage: `is_off_topic_v3 == False`, `confidence_v3 >= 0.70`, groupe politique connu
- Corpus filtré total: 11 113 textes
- Corpus principal post-7 octobre utilisé pour les comparaisons: 10 774 textes

Le filtrage exclut une part importante des interventions AN. Cette perte est attendue avec des critères stricts, mais elle doit être rappelée dans toute comparaison Twitter/AN.

## 2) Validation de `stance_v3` (triangulation)

### Score lexical inductif

- Corrélation texte: Pearson `r = 0.756`, Spearman `rho = 0.708`
- Corrélation député (moyenne): Pearson `r = 0.947`, Spearman `rho = 0.916`

Lecture: la cohérence est forte au niveau agrégé député. Au niveau texte, le signal est plus bruité, ce qui est cohérent avec des messages courts et contextuels.

### Positionnement latent (Wordfish/CA)

- `rho(theta, stance_v3) = 0.882`
- `rho(theta, score_lexical) = 0.963`

Lecture: les méthodes non supervisées retrouvent une dimension proche de l'échelle de stance. Cela soutient la stabilité du signal, sans transformer cette convergence en validation parfaite.

### PCA diagnostique sur TF-IDF

- Corrélation `PC1` vs `stance_v3`: `rho = 0.595`
- Silhouette blocs: `-0.004`

Lecture: la séparation est limitée au niveau texte individuel; les blocs se distinguent davantage à un niveau agrégé. Cette limite doit être maintenue explicitement.

### Synthèse validation

- Corrélation moyenne inter-mesures (niveau député): `rho = 0.898`
- Twitter: `rho = 0.911` (`stance_v3` vs lexical)
- AN: `rho = 0.886` (`stance_v3` vs lexical)

Conclusion prudente: `stance_v3` est suffisamment cohérent pour une analyse descriptive comparée, avec des zones grises pour les profils intermédiaires.

## 3) Text mining approfondi

### Vocabulaire distinctif (log-odds)

- Gauche radicale: lexique davantage humanitaire/juridique
- Droite: lexique davantage sécuritaire/identitaire
- Twitter vs AN: registre plus émotionnel sur Twitter, plus institutionnel à l'AN
- RN vs LR: différence de registre intra-droite observable

Ces résultats décrivent des écarts de vocabulaire. Ils n'impliquent pas, à eux seuls, des écarts de causalité politique.

### Dynamique lexicale temporelle

Des tendances de baisse sont observées sur plusieurs registres (tests Kendall significatifs dans plusieurs couples bloc-registre).  
Interprétation retenue: décroissance du volume de discussion et reconfiguration des priorités lexicales dans le temps.

### Polarisation lexicale

- Tendance globale: `tau = +0.376`, `p = 0.005`

Lecture: la distance lexicale augmente au fil de la période. Cette mesure reste sensible au volume mensuel et aux événements de calendrier.

### Vocabulaire et engagement Twitter

Les mots associés à un engagement plus élevé relèvent plus souvent de registres émotionnels et d'interpellation.  
Point de vigilance: l'association mot-engagement est descriptive et peut refléter des effets de contexte (événement, notoriété auteur, temporalité).

### Cibles discursives

Les associations cible x bloc sont fortes (chi2 significatifs) et évoluent dans le temps:
- baisse de la saillance de certaines cibles comme `HAMAS` dans plusieurs blocs
- montée de cibles gouvernementales selon les périodes

Lecture: le débat se déplace partiellement de l'événement initial vers l'attribution de responsabilités politiques.

## 4) Points robustes pour l'écriture

- La structure de clivage lexicale est nette à l'échelle des blocs.
- La comparaison Twitter/AN montre un code-switching de registre.
- La dynamique temporelle montre des reconfigurations, pas une trajectoire linéaire unique.
- Les cibles discursives sont un angle central pour dépasser la seule échelle de stance.

## 5) Limites à conserver explicitement

- Résultats descriptifs: ne pas inférer de causalité.
- Sensibilité aux volumes inégaux entre blocs et arènes.
- Performances différentes selon granularité (texte vs agrégé député).
- Variantes de libellés sur certaines cibles (`target`) à harmoniser avant publication.
- Les analyses lexicales bag-of-words ont des limites sémantiques connues.
