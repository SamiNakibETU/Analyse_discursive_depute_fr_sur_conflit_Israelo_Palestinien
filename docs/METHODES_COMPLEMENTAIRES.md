# Méthodes complémentaires

*D’après une revue de littérature 2024–2025 : polarisation affective, fondements moraux, registre discursif, Twitter–AN.*

---

## Vue d’ensemble

Le pipeline mesure la polarisation idéologique (stance, distance cosinus) et les métriques temporelles (Wasserstein, polarisation entropique, effective dimensionality). Quatre analyses complémentaires enrichissent l’étude : polarisation affective (VAD), Moral Foundations Theory, registre discursif (coopération vs conflit), comparaison formalisée Twitter–AN.

| Méthode | Fichiers produits | Notebook |
|---------|-------------------|----------|
| Polarisation affective (VAD) | affective_vad_by_bloc_month.csv, affective_polarization_temporal.csv | NB04 |
| Moral Foundations Theory | moral_foundations_by_bloc_month.csv | NB04 |
| Registre discursif | deliberative_intensity_by_bloc_month.csv | NB03 |
| Twitter vs AN | stance_twitter_vs_an_by_deputy.csv, regression_delta_stance.csv | NB10 |
| NER cibles discursives | entités PER/ORG/GPE, humanization_score | NB13 |

---

## Polarisation affective (Valence–Arousal–Dominance)

Lexique NRC-VAD (Mohammad, NRC Canada), version française. Trois axes : Valence (positif/négatif), Arousal (activation), Dominance (assertivité). Score moyen par texte, agrégation par bloc-mois. Gap VAD entre blocs : distance euclidienne des distributions.

Références : Goldin et al. (2025), Evkoski et al. (2025), NRC-VAD (http://saifmohammad.com/WebPages/nrc-vad.html).

---

## Moral Foundations Theory

Cinq fondements : Care, Fairness, Loyalty, Authority, Sanctity. Lexique minimal français (fallback ; eMFD Hopp et al. 2021, traduction Husson & Palma 2024 pour version complète). Proportion de mots par fondement par texte, agrégation par bloc-mois.

**C1** : Lexique étendu à 40+ mots par fondement (Haidt 2012, eMFD, termes corpus frames MOR/HUM). Couverture : % de textes avec ≥1 hit par fondement. `compute_mfd_coverage()` dans mfd_lexicon.py.

Références : Amjadi & John (2025), Song et al. (2025), eMFD Hopp et al. (2021).

---

## Registre discursif

Score 0 (coopératif) à 1 (conflictuel) basé sur des marqueurs lexicaux (critiquer, accuser, exiger vs proposer, informer, etc.). Proportion de discours conflictuel par bloc et mois. Si les positions convergent mais le discours reste conflictuel, la convergence est lexicale plutôt que délibérative.

**C2** : Mots à contexte ambigu (ex. « responsable ») gérés via `CONTEXTES_AMBIGU` : conflictuel si « responsable de la mort de », coopératif si « responsable politique ». Corrélation Spearman registre ↔ stance : ρ < 0,1 → limitation documentée ; ρ > 0,3 → module utile. Figure fig75 : registre conflictuel moyen par bloc × batch (CEASEFIRE_BREACH).

Références : travaux sur l’intensité délibérative en parlements (Irani et al. 2025, Bundestag 2024).

---

## Twitter vs Assemblée nationale

Pour chaque député actif sur les deux arènes : Δ = stance_Twitter − stance_AN. Régression Δ ~ bloc + n_tweets + engagement + batch. Distribution et évolution temporelle de Δ par bloc.

Références : Çetinkaya et al. (2025, AAAI), comparaison cross-plateforme.

---

## Polarisation entropique Bao & Gill (C3)

Métrique Ec (arXiv:2603.02102) : polarisation entropique sur la distribution des stance. Échelle 0 (consensus) à 1 (polarisation maximale). Figure fig76 : évolution mensuelle Ec vs distance cosinus TF-IDF, avec événements pivot en overlay.

**Interprétation Ec** : Ec élevé → positions fortement polarisées ; Ec faible → convergence des positions.

**Interprétation Effective Dimensionality (ED)** : ED diminue → l'espace discursif se réduit à un seul axe (positionnement binaire pour/contre). ED augmente → le débat se complexifie, plusieurs dimensions en jeu.

---

## Poids inverses à la fréquence (A4)

Pour les analyses agrégées sur plusieurs blocs, le déséquilibre du corpus (Gauche radicale ≈ 63,5 %) peut biaiser les métriques. Poids inverses : w_i = n_min_bloc / n_bloc_i où n_min_bloc = min(n_bloc). Ces poids peuvent être appliqués aux moyennes de polarisation entropique ou de distance cosinus lorsque l'on agrège par bloc. Les figures de robustesse (fig66–68) utilisent un sous-échantillonnage stratifié (n_min textes par bloc) plutôt que les poids.
