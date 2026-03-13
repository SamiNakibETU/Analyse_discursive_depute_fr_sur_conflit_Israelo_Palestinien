# Méthodologie détaillée

**Projet** : fr_assemblee_discourse_analysis - Analyse discursive sur le conflit israélo-palestinien  
**Date** : février 2026

---

## 1. Collecte des données

### Twitter / X

- Dans ce repo nettoyé, les tweets arrivent comme corpus déjà préparé via `src/config.py` (`SOURCE_DIR`)
- Dans le workspace parent, le code visible de collecte repose sur un scraping Nitter mensuel (`final/scripts_scraîng/scrape_nitter_search_monthly.js`)
- Le chemin d'acquisition initial exact n'est donc pas démontré ici comme un pipeline Twitter API autonome
- Filtrage thématique par mots-clés puis filtres qualité en aval
- Période visible : 7 oct. 2023 – 31 jan. 2026
- Volume filtré exploité dans ce repo : 9 135 tweets

### Assemblée nationale

- Questions au gouvernement, débats, propositions de résolution
- Source : données ouvertes assemblee-nationale.fr
- Filtrage thématique identique
- Volume : 1 639 interventions

### Total

- **10 774 textes** (9 135 Twitter + 1 639 AN)
- **459 députés**
- **28 mois** (oct. 2023 – jan. 2026)

---

## 2. Pipeline d'annotation

### Étape 1 - Annotation v3 (corpus complet)

- **Modèle** : GPT-4o-mini
- **Schéma** : stance (-2 à +2), frame, target, intensity, confidence
- **Reproductibilité** : température 0, structured outputs
- **Variables** : stance_v3, primary_frame_v3, intensity_v3, confidence_v3, has_both_sides_v3

### Étape 2 - Annotation v4 (fenêtres enrichies)

- **Modèle** : GPT-4o-mini
- **Corpus** : 5 905 textes dans 7 fenêtres événementielles
- **Prompt enrichi** : briefings contextuels par période, variables batch-spécifiques
- **Variables supplémentaires** : ceasefire_call, ceasefire_type, emotional_register, frame_primary, etc.
- **Voir** : `docs/CODEBOOK.md` pour le détail des variables et du prompt

---

## 3. Validation

### Accord inter-version (v3 / v4)

| Métrique | Valeur |
|---------|--------|
| Spearman ρ | 0,86 (p < 0,001) |
| Accord exact | 61,59 % |
| Accord à ±1 point | 95,33 % |

### Validation externe

| Méthode | Corrélation avec stance |
|---------|-------------------------|
| Wordscores | ρ = 0,92 |
| Wordfish | ρ = 0,88 |
| PCA (1ère composante) | Cohérente avec stance |

### Référence méthodologique

Gilardi et al. (2023) montrent que les LLM rivalisent avec les annotateurs humains sur des tâches de classification politique. Ici, le résultat visible le plus robuste est un **accord inter-version** (v3/v4) de ρ = 0,86. Cela ne remplace pas une validation humaine systématique.

---

## 4. Analyses statistiques

### Régression multivariée

- **Méthode** : OLS avec erreurs robustes HC3
- **Modèle** : `stance ~ bloc * batch + frame + arena`
- **Référence** : Centre / Majorité
- **Terme d'interaction** : bloc × batch - teste si l'effet d'un événement diffère selon le bloc politique
- **ANOVA Type II** : décomposition de la variance (bloc, batch, interaction, frame, etc.)

### Comparaisons événementielles avant/après

- **Événements** : 6 à 7 selon les sorties mobilisées
- **Blocs** : 4
- **Fenêtre** : 30 jours avant/après selon la table auditée
- **Test** : Mann-Whitney U (non-paramétrique)
- **Important** : il ne s'agit pas d'un diff-in-diff canonique. Le design visible ne fournit ni groupe contrôle stable, ni test convaincant de tendances parallèles pour une inférence causale stricte.

### Détection de ruptures

- **Algorithme** : Pelt (`ruptures`)
- **Séries** : 3 paires de distance cosinus mensuelle (G.rad↔Droite, G.mod↔Centre, etc.)
- **Pénalité** : pen ∈ {1, 2, 3, 5}

### Polarisation lexicale

- **Représentation** : TF-IDF sur textes lemmatisés
- **Métrique** : distance cosinus entre centroïdes de blocs
- **Granularité** : mensuelle

### Fighting words (Monroe et al. 2008)

- **Méthode** : log-odds ratio avec prior Dirichlet (α = 0,01)
- **Application** : vocabulaire distinctif Gauche vs Droite par batch
- **Output** : z-scores par mot, heatmap mots × batch

---

## 5. Structure des blocs

| Bloc | Groupes |
|------|---------|
| Gauche radicale | LFI-NFP, LFI, GDR |
| Gauche modérée | PS-NFP, SOC, ECO-NFP, ECO |
| Centre / Majorité | EPR, REN, MODEM, HOR, DEM |
| Droite | RN, LR, UDR, NI |

Droite et extrême droite sont regroupées (voir justification dans `docs/RAPPORT_EXPLORATION_CLASSIFICATION_GROUPES.md`).

---

## Références

- Gilardi, F., Alizadeh, M., Kubli, M. (2023). *ChatGPT outperforms crowd workers for text-annotation tasks*. PNAS.
- Monroe, B. L., Colaresi, M. P., Quinn, K. M. (2008). *Fightin' words: Lexical feature selection and evaluation for identifying the content of political conflict*. Political Analysis.
- Truong, C., Oudre, L., Vayatis, N. (2020). *Selective review of offline change point detection methods*. Signal Processing.
