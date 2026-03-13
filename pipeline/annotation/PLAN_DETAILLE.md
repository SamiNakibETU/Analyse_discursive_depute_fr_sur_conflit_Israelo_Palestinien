# 📋 PLAN DÉTAILLÉ - Projet Gaza/Palestine

## 🎯 Objectif final

Produire une analyse rigoureuse de l'évolution des positions des députés français sur Gaza/Palestine, avec trois outputs :
1. **Article académique** (revue de science politique)
2. **Dashboard interactif** (exploration des données)
3. **Repository GitHub** (code + données)

---

## 📅 PHASE 0 : CONSOLIDATION (3-5 jours)

### Objectifs
- Consolider les données brutes en formats exploitables
- Valider la qualité des données
- Établir les statistiques descriptives de base

### Tâches

| # | Tâche | Durée | Script | Output |
|---|-------|-------|--------|--------|
| 0.1 | Consolider les tweets (8466 JSON → Parquet) | 2h | `consolidate_tweets.py` | `tweets_all.parquet` |
| 0.2 | Consolider les interventions AN | 1h | (existant) | `interventions_all.parquet` |
| 0.3 | Vérifier les doublons et incohérences | 2h | notebook | Rapport qualité |
| 0.4 | Statistiques descriptives | 4h | notebook | Figures de base |

### Commandes

```bash
cd projet_gaza

# Installer les dépendances
pip install -r requirements.txt

# Consolider les tweets
python src/preprocessing/consolidate_tweets.py

# Filtrer Gaza/Palestine
python src/preprocessing/filter_gaza_corpus.py
```

### Livrables Phase 0
- [ ] `data/consolidated/tweets_all.parquet` (~257K tweets)
- [ ] `data/consolidated/interventions_all.parquet` (~1900 interventions)
- [ ] `notebooks/00_data_quality.ipynb`

---

## 📅 PHASE 1 : FILTRAGE ET EDA (1 semaine)

### Objectifs
- Extraire le corpus pertinent Gaza/Palestine
- Analyse exploratoire complète
- Identifier les patterns temporels et partisans

### Tâches

| # | Tâche | Durée | Output |
|---|-------|-------|--------|
| 1.1 | Appliquer filtre Gaza/Palestine aux tweets | 2h | `tweets_gaza.parquet` |
| 1.2 | Valider le filtre (échantillon manuel) | 4h | Taux faux positifs/négatifs |
| 1.3 | Ajuster le dictionnaire si nécessaire | 2h | `filtering_keywords.json` v2 |
| 1.4 | EDA temporelle | 8h | Figures + insights |
| 1.5 | EDA par groupe politique | 8h | Figures + insights |
| 1.6 | Comparaison Twitter/AN | 4h | Analyse croisée |

### Analyses EDA à produire

```
📊 Analyses temporelles
├── Volume tweets/interventions par mois
├── Pics d'activité vs événements-clés
├── Distribution horaire (tweets)
└── Saisonnalité

📊 Analyses partisanes
├── Volume par groupe politique
├── Evolution temporelle par groupe
├── Députés les plus actifs
└── Répartition gauche/droite

📊 Analyses textuelles
├── Nuage de mots par période
├── Bigrammes/trigrammes fréquents
├── Longueur moyenne des textes
└── Présence de médias/liens
```

### Livrables Phase 1
- [ ] `data/filtered/tweets_gaza.parquet` (~25-35K tweets estimés)
- [ ] `data/filtered/interventions_gaza.parquet`
- [ ] `notebooks/01_filtering.ipynb`
- [ ] `notebooks/02_eda_temporal.ipynb`
- [ ] `notebooks/03_eda_partisan.ipynb`
- [ ] `outputs/figures/eda_*.png`

---

## 📅 PHASE 2 : ANNOTATION (2-3 semaines)

### Objectifs
- Créer un gold standard annoté pour le stance detection
- Calculer l'accord inter-annotateurs
- Documenter le processus d'annotation

### Tâches

| # | Tâche | Durée | Output |
|---|-------|-------|--------|
| 2.1 | Échantillonner les textes à annoter | 4h | 1300 textes stratifiés |
| 2.2 | Former les annotateurs (codebook) | 2h | Session de formation |
| 2.3 | Phase pilote (50 textes × 2 annotateurs) | 4h | Kappa initial |
| 2.4 | Résoudre désaccords, ajuster codebook | 4h | Codebook v2 |
| 2.5 | Annotation production (1000 tweets) | 40h | `gold_tweets.jsonl` |
| 2.6 | Annotation production (300 interventions) | 15h | `gold_interventions.jsonl` |
| 2.7 | Double annotation 20% + Kappa final | 8h | Rapport inter-annotateurs |

### Stratification de l'échantillon

```
TWEETS (1000 total)
├── Période P0 (pré-7 oct): 100 tweets
├── Période P1 (choc): 150 tweets
├── Période P2 (offensive): 200 tweets
├── Période P3 (post-CIJ): 150 tweets
├── Période P4 (Rafah): 150 tweets
├── Période P5-P7: 250 tweets
└── Stratifié par groupe politique (proportionnel)

INTERVENTIONS (300 total)
├── Même distribution temporelle
└── Tous les groupes représentés
```

### Outils d'annotation recommandés
1. **Label Studio** (self-hosted, gratuit)
2. **Prodigy** (payant, très efficace)
3. **Google Sheets** (simple, collaboratif)

### Livrables Phase 2
- [ ] `data/annotated/gold_standard/tweets_annotated.jsonl`
- [ ] `data/annotated/gold_standard/interventions_annotated.jsonl`
- [ ] `docs/codebook_annotation_v2.md`
- [ ] `docs/inter_annotator_agreement.md` (Kappa > 0.7)

---

## 📅 PHASE 3 : MODÉLISATION (2 semaines)

### Objectifs
- Fine-tuner CamemBERT pour stance detection
- Évaluer les performances
- Appliquer au corpus complet

### Tâches

| # | Tâche | Durée | Output |
|---|-------|-------|--------|
| 3.1 | Préparer datasets train/val/test | 4h | Splits 70/15/15 |
| 3.2 | Baseline CamemBERT | 8h | Modèle v1 |
| 3.3 | Hyperparameter tuning | 16h | Modèle v2 |
| 3.4 | Analyse des erreurs | 8h | Rapport erreurs |
| 3.5 | Prédiction corpus complet | 4h | Corpus annoté |
| 3.6 | Topic modeling (BERTopic) | 8h | Topics extraits |

### Architecture modèle

```python
# Fine-tuning CamemBERT
from transformers import CamembertForSequenceClassification

model = CamembertForSequenceClassification.from_pretrained(
    "camembert-base",
    num_labels=3,  # Pro-Palestine, Neutre, Pro-Israël
    problem_type="single_label_classification"
)

# Training args
training_args = TrainingArguments(
    output_dir="./outputs/models/camembert-stance",
    num_train_epochs=5,
    per_device_train_batch_size=16,
    learning_rate=2e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1_macro"
)
```

### Métriques cibles

| Métrique | Objectif minimum | Objectif souhaité |
|----------|------------------|-------------------|
| F1 macro | 0.65 | 0.75 |
| F1 Pro-Palestine | 0.70 | 0.80 |
| F1 Neutre | 0.55 | 0.65 |
| F1 Pro-Israël | 0.60 | 0.70 |

### Livrables Phase 3
- [ ] `outputs/models/camembert-stance/` (checkpoint)
- [ ] `data/annotated/predictions/tweets_predicted.parquet`
- [ ] `data/annotated/predictions/interventions_predicted.parquet`
- [ ] `notebooks/04_model_training.ipynb`
- [ ] `notebooks/05_model_evaluation.ipynb`

---

## 📅 PHASE 4 : ANALYSE (2 semaines)

### Objectifs
- Tester les hypothèses H1-H4
- Produire les visualisations finales
- Rédiger les résultats

### Tests des hypothèses

#### H1 : Évolution temporelle

```python
# Change point detection
import ruptures as rpt

# Détecter les ruptures dans la série temporelle du stance moyen
algo = rpt.Pelt(model="rbf").fit(stance_series)
change_points = algo.predict(pen=10)

# Régression segmentée
import statsmodels.api as sm
model = sm.OLS(stance, events_dummies).fit()
```

#### H2 : Trajectoires partisanes

```python
# ANOVA par groupe politique
from scipy.stats import f_oneway, kruskal

# Évolution par groupe
for group in groups:
    stance_before = data[(data.group == group) & (data.date < oct_7)].stance
    stance_after = data[(data.group == group) & (data.date >= oct_7)].stance
    ttest_result = ttest_ind(stance_before, stance_after)
```

#### H3 : Comparaison Twitter/AN

```python
# Pour chaque député présent dans les deux arènes
for depute in deputes_both:
    stance_twitter = tweets[tweets.depute == depute].stance.mean()
    stance_an = interventions[interventions.depute == depute].stance.mean()
    coherence = 1 - abs(stance_twitter - stance_an) / 2
```

#### H4 : Trajectoires individuelles

```python
# Identifier les "retournements"
for depute in deputes:
    trajectory = get_monthly_stance(depute)
    if detect_reversal(trajectory, threshold=0.5):
        flag_for_qualitative_analysis(depute)
```

### Livrables Phase 4
- [ ] `notebooks/06_hypothesis_testing.ipynb`
- [ ] `notebooks/07_visualizations.ipynb`
- [ ] `outputs/figures/` (figures finales)
- [ ] `outputs/tables/` (tableaux résultats)

---

## 📅 PHASE 5 : PUBLICATION (2-3 semaines)

### Objectifs
- Finaliser l'article académique
- Déployer le dashboard
- Publier le repository

### Tâches

| # | Tâche | Durée | Output |
|---|-------|-------|--------|
| 5.1 | Rédaction article (draft) | 40h | Article v1 |
| 5.2 | Révision + feedback | 16h | Article v2 |
| 5.3 | Développement dashboard Streamlit | 16h | Dashboard |
| 5.4 | Documentation GitHub | 8h | README, CONTRIBUTING |
| 5.5 | Nettoyage code + tests | 8h | Code propre |
| 5.6 | Publication données | 4h | Zenodo/Dataverse |

### Structure article

```
1. Introduction
   - Contexte conflit Gaza
   - Question de recherche
   - Contributions

2. Revue de littérature
   - Stance detection
   - Discours parlementaire français
   - Réseaux sociaux et politique

3. Données et méthodes
   - Corpus
   - Annotation
   - Modèle

4. Résultats
   - H1: Évolution temporelle
   - H2: Trajectoires partisanes
   - H3: Twitter vs AN
   - H4: Retournements

5. Discussion
   - Interprétation
   - Limites
   - Implications

6. Conclusion
```

### Dashboard Streamlit

```python
# app.py
import streamlit as st

st.title("Députés français et Gaza/Palestine")

# Filtres
group = st.selectbox("Groupe politique", groups)
period = st.slider("Période", min_date, max_date)

# Visualisations
st.plotly_chart(fig_temporal)
st.plotly_chart(fig_partisan)

# Exploration individuelle
depute = st.selectbox("Député", deputes)
show_deputy_profile(depute)
```

### Livrables Phase 5
- [ ] Article (PDF, Word)
- [ ] Dashboard déployé (Streamlit Cloud / HuggingFace Spaces)
- [ ] Repository GitHub public
- [ ] Données sur Zenodo (DOI)

---

## 📊 PLANNING GLOBAL

```
Semaine 1  : Phase 0 (Consolidation)
Semaine 2  : Phase 1 (Filtrage + EDA)
Semaine 3-4: Phase 2 (Annotation)
Semaine 5-6: Phase 3 (Modélisation)
Semaine 7-8: Phase 4 (Analyse)
Semaine 9-10: Phase 5 (Publication)
```

**Durée totale estimée : 10 semaines**

---

## ✅ CHECKLIST FINALE

### Qualité scientifique
- [ ] Kappa inter-annotateurs > 0.7
- [ ] F1 macro modèle > 0.65
- [ ] Événements définis a priori (pas post-hoc)
- [ ] Tests statistiques appropriés

### Reproductibilité
- [ ] Données brutes archivées
- [ ] Code versionné et documenté
- [ ] Environment reproductible (requirements.txt)
- [ ] Random seeds fixés

### Éthique
- [ ] Pas de données personnelles sensibles publiées
- [ ] Respect CGU Twitter (scraping via Nitter)
- [ ] Données publiques uniquement

### Publication
- [ ] Article formaté pour revue cible
- [ ] Dashboard accessible
- [ ] DOI pour données
- [ ] License claire (MIT / CC-BY)

---

## 🔗 RESSOURCES

### Académiques
- Küçük & Can (2022) - Stance Detection Survey
- MediaLab Sciences Po - Analyse discours parlementaire
- Mohammad et al. (2016) - Stance and Sentiment

### Techniques
- [CamemBERT](https://huggingface.co/camembert)
- [BERTopic](https://maartengr.github.io/BERTopic/)
- [ruptures](https://centre-borelli.github.io/ruptures-docs/)
- [Streamlit](https://streamlit.io/)

### Données complémentaires
- [NosDéputés.fr API](https://www.nosdeputes.fr/api)
- [Scrutins AN](https://data.assemblee-nationale.fr/)


