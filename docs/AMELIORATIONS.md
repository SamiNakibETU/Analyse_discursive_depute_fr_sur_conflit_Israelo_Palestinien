# Améliorations méthodologiques — Roadmap priorisée

*Ce document traduit la réflexion critique en actions concrètes, classées par priorité
et impact estimé. Objectif : porter le projet au niveau d'un article soumettable en
*Computational Communication Research* ou *Political Analysis*.*

---

## Priorité 1 — Crédibilité de l'annotation (Haute urgence)

### A1. Déclarer le modèle LLM d'annotation

**Problème** : le codebook ne précise pas quel modèle a produit stance_v3 / stance_v4,
ni le prompt exact, ni la date d'annotation.

**Action** :
1. Ajouter dans `docs/CODEBOOK.md` : modèle (ex. GPT-4-turbo-2024-04-09), version API,
   prompt complet (verbatim), date de lancement, température.
2. Ajouter dans `docs/METHODOLOGIE.md` : discussion des biais documentés des LLM sur
   le conflit israélo-palestinien (Navigli et al. 2023).

**Fichiers à modifier** : `docs/CODEBOOK.md`, `docs/METHODOLOGIE.md`

---

### A2. Validation humaine systématique (150 textes → métriques publiables)

**Problème** : le Spearman 0,86 entre v3 et v4 est une mesure de consistance du même
annotateur LLM, pas un accord inter-annotateurs humains.

**Action** :
```bash
python src/validation_humaine.py    # génère sample_150.csv
# → annoter manuellement data/validation/annotations.csv
python src/validation_metrics.py    # Cohen's Kappa + Spearman humain vs LLM
```

**Cible publiable** : Cohen's κ > 0,60 (accord substantiel) sur l'échelle ordinale.
Si κ < 0,60, retravailler le prompt ou passer en binaire (pro-Palestine / pro-Israël / neutre).

**Impact recruteur** : montre la démarche scientifique rigoureuse (validation externe).

---

## Priorité 2 — Robustesse politique (Haute urgence)

### B1. Séparer LR et RN dans toutes les analyses

**Problème** : la fusion LR + RN en « Droite » est la décision analytique la plus contestable.
LR et RN ont des cultures de politique étrangère différentes.

**Action** :
1. Ajouter un paramètre `granularity="fine"` dans `src/config.py` avec un mapping 5 blocs :
   ```python
   BLOC_COLORS_FINE = {
       "Gauche radicale": "#c0392b",
       "Gauche moderee": "#e67e22",
       "Centre / Majorite": "#2980b9",
       "LR": "#7f8c8d",
       "RN / extreme droite": "#1a1a2e",
   }
   ```
2. Exécuter les analyses principales (stance mensuel, fighting words, convergence)
   en parallèle avec la granularité fine.
3. Documenter les différences dans un tableau de robustesse.

---

### B2. Pondération par volume (correction du déséquilibre)

**Problème** : Gauche radicale ≈ 63 % du corpus. Les moyennes de stance par bloc
sont influencées par les blocs les plus actifs.

**Action** : utiliser une moyenne pondérée par l'inverse du volume de chaque bloc-mois
dans les agrégations temporelles. Ajouter ce calcul dans `scripts/run_analysis.py`.

```python
# Exemple de pondération inverse-fréquence
weights = 1 / df.groupby("bloc")["text"].transform("count")
df["stance_weighted"] = df["stance_v3"] * weights
```

---

## Priorité 3 — Nouvelles analyses (Impact maximal)

### C1. Analyse de réseau des co-mentions et retweets

**Nouveau fichier** : `src/network_analysis.py` (voir code détaillé dans le repo)

**Ce que ça apporte** :
- Graphe biparti député–thème (co-occurrence) pour visualiser les clusters discursifs.
- Graphe de retweet pour valider la convergence interactionnelle vs lexicale.
- Centralité de betweenness pour identifier les *brokers* transpartisans.

**Méthode** : NetworkX, résolution de Louvain, visualisation spring layout.

**Résultat attendu** : les « movers » (fig35) sont-ils des brokers dans le réseau ?
Si oui, la convergence lexicale est aussi une convergence structurelle → publication forte.

---

### C2. Topic modeling inductif avec BERTopic (CamemBERT)

**Nouveau fichier** : `src/topic_modeling.py` (voir code dans le repo)

**Ce que ça apporte** :
- Topics émergents non définis *a priori* par les cadres HUM/SEC/LEG…
- Comparaison entre topics par bloc : est-ce que LFI parle de « génocide »
  quand LR parle de « sécurité » sur les mêmes événements ?
- Évolution temporelle des topics par batch → narratives shift visualization.

**Pipeline** :
```
Textes → CamemBERT embeddings → UMAP → HDBSCAN → BERTopic topics
```

**Dépendances à ajouter** : `bertopic>=0.16`, `umap-learn>=0.5`, `hdbscan>=0.8`.

---

### C3. Détection de changepoints sur les séries VAD

**Ce que ça apporte** :
- Tester si les ruptures affectives (Evkoski 2025) précèdent les ruptures lexicales.
- `ruptures` est déjà dans requirements.txt — à appliquer aux séries de valence/arousal.

**Code** :
```python
import ruptures as rpt
signal = df_vad.groupby("month")["valence"].mean().values
model = rpt.Pelt(model="rbf").fit(signal)
breakpoints = model.predict(pen=10)
```

Ajouter dans `scripts/run_analysis.py` et notebook `03_dynamiques_temporelles.ipynb`.

---

### C4. Intégration des named entities (acteurs cités)

**Ce que ça apporte** :
- Identifier les acteurs nommés : Netanyahou, Hamas, Biden, Macron, ONU, CPI…
- Calculer la fréquence de citation par bloc → qui est l'ennemi/l'allié dans chaque bloc ?
- Corrélation : la citation de Hamas est-elle associée à un stance pro-Israël ?

**Dépendances** : `spacy>=3.6` + modèle `fr_core_news_lg`.

---

## Priorité 4 — Visualisations et communication (Impact recruteur)

### D1. Dashboard interactif (Plotly / Streamlit)

Transformer les figures statiques en dashboard interactif :
- Filtre par bloc, par batch, par arène.
- Slider temporel.
- Tooltip avec exemples de textes.

**Code minimal** :
```bash
pip install streamlit plotly
streamlit run src/dashboard.py
```

**Impact recruteur** : démo live > PDF statique.

---

### D2. Figures export social (améliorées)

Le script `src/export_figures_social.py` existe déjà. Améliorer :
- Ajouter le titre du projet + date en bas de chaque image.
- Générer une version 9:16 (Stories) en plus des formats existants.
- Ajouter un mode « dark theme » pour les threads X nocturnes.

---

### D3. Retitrer les event studies pour éviter la sur-interprétation

**fig12** : remplacer « diff-in-diff » par « shift temporel associatif (avant/après) »
dans la légende et dans le brief analytique.

---

## Priorité 5 — Documentation et reproductibilité

### E1. Fichier ANNOTATION_PROTOCOL.md

Documenter le prompt complet utilisé pour l'annotation LLM, les décisions de codage
pour les cas ambigus, et les instructions données pour la v4 (prompt enrichi).

### E2. Environnement reproductible

Ajouter un `Makefile` ou un script `reproduce.sh` pour les reviewers :
```bash
make data     # prepare_data.py
make analysis # run_analysis.py
make figures  # toutes les figures
make validate # validation_humaine + validation_metrics
```

### E3. Tests unitaires pour les métriques

Ajouter des tests dans `tests/` pour :
- `vendeville.py` : valider `entropic_polarization_bao_gill` sur des cas limites.
- `registre_discursif.py` : valider `score_registre_discursif` sur des textes connus.
- `vad_lexicon.py` : valider le fallback quand le lexique NRC-VAD est absent.

---

## Tableau récapitulatif

| ID | Action | Effort | Impact recruteur | Impact académique |
|----|--------|--------|-----------------|-------------------|
| A1 | Déclarer modèle LLM | Faible | ★★★ | ★★★ |
| A2 | Validation humaine 150 | Moyen | ★★★ | ★★★ |
| B1 | Séparer LR / RN | Moyen | ★★ | ★★★ |
| B2 | Pondération volume | Faible | ★★ | ★★ |
| C1 | Réseau co-mentions | Fort | ★★★ | ★★★ |
| C2 | BERTopic topic modeling | Moyen | ★★★ | ★★ |
| C3 | Changepoints VAD | Faible | ★★ | ★★★ |
| C4 | Named entities | Moyen | ★★ | ★★ |
| D1 | Dashboard Streamlit | Fort | ★★★ | ★ |
| D2 | Export social amélioré | Faible | ★★ | ★ |
| D3 | Retitrer fig12 | Très faible | ★ | ★★★ |
| E1 | ANNOTATION_PROTOCOL.md | Faible | ★★ | ★★★ |
| E2 | Makefile reproductible | Faible | ★★ | ★★ |
| E3 | Tests unitaires métriques | Moyen | ★★ | ★★ |
