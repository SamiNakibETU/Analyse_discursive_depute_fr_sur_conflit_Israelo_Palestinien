# Brief analytique — Discours parlementaire français sur Gaza (2023–2026)

*Document de synthèse pour présentation externe. Accompagnement CV / candidatures.*

---

## 1. Contexte et question de recherche

Le conflit israélo-palestinien a généré un flux important de prises de parole des députés français, tant sur Twitter qu’à l’Assemblée nationale. Ce projet pose une question simple : **comment le positionnement discursif des députés évolue-t-il face aux événements pivot** (ordonnance CIJ, mandats CPI, cessez-le-feu, etc.) ?

L’analyse porte sur **10 774 textes** de **459 députés** entre octobre 2023 et janvier 2026. Chaque texte est annoté par un LLM sur une échelle de stance (-2 pro-israélien à +2 pro-palestinien). Les méthodes de science politique computationnelle (event studies, polarisation lexicale, convergence) permettent de mesurer la réactivité des blocs politiques et la diffusion des cadres discursifs.

---

## 2. Données et méthode

**Corpus :** tweets (9 135) et interventions en séance (1 639), nettoyés et annotés. **Segmentation temporelle :** 7 périodes (batches) alignées sur les événements pivot. **Annotation stance :** LLM avec accord interne v3↔v4 élevé (Spearman 0,86). **Blocs :** Gauche radicale, Gauche modérée, Centre / Majorité, Droite.

Les event studies consistent en un **shift temporel** (différence de stance moyenne avant/après chaque événement, par bloc). La polarisation lexicale utilise la distance cosinus et les « fighting words » (log-odds entre blocs). Aucune inférence causale stricte — les résultats sont associatifs.

---

## 3. Résultat 1 : Stabilité vs réactivité

![Stance mensuel par bloc](../figures/fig10_stance_ribbon.png)

**Le Centre varie, les extrêmes restent stables.** Sur 28 mois, seule la position moyenne du Centre / Majorité réagit nettement aux événements (CIJ, mandats CPI, cessez-le-feu, rupture). La Gauche radicale et la Droite maintiennent des positions moyennes quasi constantes. La figure montre l’évolution mensuelle par bloc avec intervalles de confiance 95 %.

**Interprétation :** le centre de l’échiquier s’adapte à l’actualité ; les ailes restent ancrées dans leur cadre discursif initial.

---

## 4. Résultat 2 : Paradoxe de la Droite au cessez-le-feu

![Impact événements](../figures/fig12_diff_in_diff.png)

Au moment où le Centre appelle au cessez-le-feu (janvier 2025), la **Droite durcit son discours** : delta stance ≈ -1,03 (p ≈ 0,008). Alors que le Centre se rapproche du vocabulaire du cessez-le-feu, la Droite accentue sa distance. C’est un signe de **stratégie de différenciation** : quand le centre bouge, la droite se distancie pour maintenir une identité distinctive.

---

## 5. Résultat 3 : Convergence transpartisane tardive

![Convergence lexicale](../figures/fig33_convergence_batch.png)

En fin de période, **35,5 %** des textes Gauche modérée et **30,3 %** des textes Centre mobilisent le vocabulaire du cessez-le-feu. La diffusion lexicale suit les positions implicites : les blocs modérés convergent vers un cadrage commun, tandis que la Gauche radicale et la Droite conservent des vocabulaires distincts.

**Interprétation :** l’appel au cessez-le-feu devient un marqueur de modération, adopté progressivement par le centre gauche et le centre.

---

## 6. Résultat 4 : Polarisation lexicale

![Distance cosinus](../figures/fig18_distance_cosinus_gr_droite.png)

La **distance cosinus** entre les vocabulaires de la Gauche radicale et de la Droite atteint son maximum en décembre 2024. Les « fighting words » (termes sur/sous-représentés par bloc) distinguent nettement les discours. La polarisation lexicale reflète et renforce la polarisation politique observable dans les prises de position.

---

## 7. Limites et perspectives

- **Annotation LLM :** pas de validation humaine ; les scores sont un proxy cohérent mais non validé.
- **Corpus déséquilibré :** la Gauche radicale domine en volume ; analyses de sensibilité réalisées (sous-échantillonnage).
- **Pas de causalité :** shift temporel descriptif, pas de design diff-in-diff classique.
- **Pistes :** validation humaine (κ sur échantillon stratifié), analyse 5 blocs (LR/RN séparés), exploitation des métriques d’engagement Twitter.

---

## 8. Annexe méthodologique

| Élément | Détail |
|---------|--------|
| Fenêtres temporelles | CHOC, POST_CIJ, RAFAH, POST_SINWAR, MANDATS_CPI, CEASEFIRE_BREACH, NEW_OFFENSIVE |
| Event studies | Fenêtre ±30 j autour de chaque événement ; Mann-Whitney pour significativité |
| Polarisation | Monroe et al. 2008 (log-odds) ; distance cosinus mensuelle |
| Régressions | OLS avec HC3 ; interaction bloc × batch |

Code et données : [GitHub](https://github.com/SamiNakibETU/Analyse_discursive_depute_fr_sur_conflit_Israelo_Palestinien)
