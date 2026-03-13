# 🇫🇷 Analyse du Discours des Députés Français sur Gaza/Palestine

## 📋 Description

Ce projet analyse l'évolution des positions des députés français sur le conflit Gaza/Palestine, en comparant leurs interventions à l'Assemblée Nationale et leurs tweets sur X (Twitter).

**Période d'étude :** Janvier 2023 - Janvier 2026

**Corpus :**

- ~1,900 interventions parlementaires (filtrées Gaza/Palestine)
- ~257,000 tweets bruts de 291 députés

## 🎯 Hypothèses de recherche

| ID     | Hypothèse                                                                                                                                               | Type         |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **H1** | L'intensité et la tonalité des prises de position évoluent significativement après certains événements-clés (7 octobre, offensive Rafah, décisions CIJ) | Temporelle   |
| **H2** | Les trajectoires discursives varient selon l'appartenance politique, avec des dynamiques de convergence ou de polarisation inter-groupes                | Partisane    |
| **H3** | Le discours diffère entre Twitter (expression libre) et l'hémicycle (contrainte institutionnelle)                                                       | Arène        |
| **H4** | Certains députés présentent des trajectoires de "retournement" identifiables                                                                            | Individuelle |

## 📁 Structure du projet

```
projet_gaza/
├── data/
│   ├── raw/                    # Données brutes (tweets JSON, interventions)
│   ├── consolidated/           # Données consolidées (Parquet)
│   ├── filtered/              # Données filtrées Gaza/Palestine
│   └── annotated/             # Annotations manuelles et prédictions
├── lexicons/                   # Dictionnaires et marqueurs
├── notebooks/                  # Analyses exploratoires
├── src/                        # Code source
├── outputs/                    # Résultats, figures, modèles
└── docs/                       # Documentation méthodologique
```

## 🚀 Installation

```bash
# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt
```

## 📊 Pipeline d'analyse

1. **Consolidation** : Fusion des données brutes en format Parquet
2. **Filtrage** : Extraction du corpus Gaza/Palestine
3. **Annotation** : Annotation manuelle du gold standard
4. **Modélisation** : Fine-tuning CamemBERT pour stance detection
5. **Analyse** : Tests des hypothèses, visualisations
6. **Publication** : Article, dashboard, données

## 📚 Citation

```bibtex
@misc{revirement_gaza_2026,
  author = {[Votre nom]},
  title = {Évolution des positions des députés français sur Gaza/Palestine (2023-2026)},
  year = {2026},
  url = {https://github.com/[username]/revirement-gaza-fr}
}
```

## 📄 Licence

[À définir - MIT / CC-BY-4.0 pour les données]

