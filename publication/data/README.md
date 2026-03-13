# Données

## Structure

```
data/
├── raw/           # Données brutes (non versionnées - sources externes)
├── processed/     # Corpus annotés (corpus_v3.parquet, corpus_v4.parquet)
└── results/       # Résultats d'analyse (CSV)
```

## Sources

Les données brutes proviennent d'un projet source sibling pointé par `src/config.py` :

- **Tweets** : `[projet_source]/data/annotated/predictions/tweets_v3_full_clean.parquet`
- **Interventions AN** : `[projet_source]/data/annotated/predictions/interventions_v3_full_clean.parquet`
- **Annotations v4** : `[projet_source]/outputs/annotations_v4_*.parquet`

*Voir `src/config.py` pour le chemin exact (SOURCE_DIR).*

## Génération

```bash
make data
# ou
python src/prepare_data.py
```

Produit `processed/corpus_v3.parquet` (10 774 textes) et `processed/corpus_v4.parquet` (5 905 textes).

## Limite de reproductibilité

Ce repo versionne de nombreux CSV finaux dans `results/`, mais ne contient pas à lui seul toute la chaîne raw -> outputs. Certaines sorties sont pré-calculées et certaines dépendent du projet source sibling.

## Résultats

Les CSV dans `results/` correspondent à des sorties d'analyse versionnées. Ils améliorent la traçabilité, mais tous ne sont pas régénérés par un script unique visible dans ce repo seul.

| Fichier | Description |
|---------|-------------|
| `stance_panel_vs_complet.csv` | Comparaison stance : corpus complet vs Panel B4 (par bloc) |
| `stance_par_groupe.csv` | Stance moyen par groupe politique (LFI, RN, LR, etc.) |

Pour régénérer : `python src/export_stance_par_groupe.py` (nécessite corpus_v3.parquet).
