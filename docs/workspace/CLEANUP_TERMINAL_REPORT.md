# Rapport Cleanup Terminal — Workspace Revirement politique fr gaza

**Date** : 2025-03-13  
**Mission** : Cleanup physique complet, structure cohérente, maintenable, publiable

---

## I. État initial réel

| Catégorie | Éléments |
|-----------|----------|
| **Canonique** | `analyse_discursive_depute/` (moteur analytique) |
| **Publication** | `fr_assemblee_discourse_analysis/` (prepare_data, exports) |
| **Web** | `index.html`, `scripts/`, `styles/`, `data/` à la racine |
| **Archive** | `archive/`, `logs/`, `.claude/`, `.cache/` |
| **Debug/ambigu** | Noms `final/`, `projet_gaza/` peu lisibles |

---

## II. Structure finale réelle

```
Revirement_politique_fr_gaza/
├── analysis/              # Moteur analytique canonique (ex analyse_discursive_depute)
├── publication/           # Couche publication (ex fr_assemblee_discourse_analysis)
├── pipeline/
│   ├── collection/        # Collecte AN + Twitter (ex final)
│   └── annotation/        # Consolidation, annotation LLM (ex projet_gaza)
├── site/                  # Dataviz éditoriale (index, scripts, styles, data)
├── archive/               # Hors flux
├── config/                # Configs (twitter_sources)
├── docs/                  # Documentation
├── figures/               # Figures générées
├── reports/               # Rapports
├── index.html             # Redirection → site/index.html
├── README.md
└── ...
```

---

## III. Mouvements appliqués

| # | Action | Détail |
|---|--------|--------|
| 1 | Déplacement | `final/` → `pipeline/collection/` |
| 2 | Déplacement | `projet_gaza/` → `pipeline/annotation/` |
| 3 | Déplacement | `analyse_discursive_depute/` → `analysis/` |
| 4 | Déplacement | `fr_assemblee_discourse_analysis/` → `publication/` |
| 5 | Déplacement | `index.html`, `scripts/`, `styles/`, `data/` → `site/` |
| 6 | Création | `index.html` racine (redirection vers site/index.html) |
| 7 | Création | Dossiers `pipeline/`, `site/` |

---

## IV. Renommages appliqués

| Ancien | Nouveau |
|--------|---------|
| `final` | `pipeline/collection` |
| `projet_gaza` | `pipeline/annotation` |
| `analyse_discursive_depute` | `analysis` |
| `fr_assemblee_discourse_analysis` | `publication` |

---

## V. Éléments archivés

- `logs/`, `.claude/`, `.cache/` : hors flux, déjà dans `.gitignore`
- `archive/` : reliquats des migrations précédentes (non versionné)

---

## VI. Documentation finale

| Fichier | Rôle |
|---------|------|
| `docs/workspace/WORKSPACE_FINAL_AUDIT.md` | Audit d'entrée |
| `docs/workspace/WORKSPACE_CLEANUP_REPORT.md` | Rapport cleanup |
| `docs/workspace/FINAL_STRUCTURE.md` | Structure cible |
| `docs/workspace/PATH_MIGRATION_MAP.md` | Ancien → Nouveau chemin |
| `docs/workspace/CANONICAL_ARTIFACTS.md` | Manifeste artefacts canoniques |
| `docs/workspace/PUBLICATION_ALIAS_MAP.md` | Alias publication |
| `docs/workspace/ARCHIVE_INDEX.md` | Index archive |
| `docs/workspace/QUICKSTART.md` | Guide de démarrage |
| `docs/workspace/SCRIPT_DATA_MATRIX.md` | Script → Données → Résultats |
| `README.md` | Racine mis à jour |

---

## VII. Références patchées

| Fichier | Modification |
|---------|--------------|
| `pipeline/annotation/src/preprocessing/consolidate_tweets.py` | `final` → `COLLECTION_ROOT` (pipeline/collection) |
| `pipeline/annotation/src/preprocessing/filter_gaza_corpus.py` | `final` → `pipeline/collection` |
| `pipeline/annotation/notebooks/00_data_consolidation.py` | `final` → `collection` |
| `pipeline/collection/scripts_scraîng/merge_twitter_sources.py` | base_path workspace root, `final` → `pipeline/collection` |
| `publication/src/config.py` | `projet_gaza` → `pipeline/annotation` |
| `analysis/src/config.py` | `fr_assemblee_discourse_analysis` → `publication` |
| `.gitignore` | Anciens chemins → nouveaux (pipeline/collection, pipeline/annotation) |
| `config/twitter_sources/README.md` | Référence merge script mise à jour |

---

## VIII. Vérifications effectuées

- [x] Imports Python (publication/config, analysis/config) résolvent correctement
- [x] publication SOURCE_DIR pointe vers pipeline/annotation
- [x] analysis SOURCE_PROJECT pointe vers publication
- [ ] Exécution complète prepare_data, run_analysis, ouverture site/index.html (à valider manuellement)

---

## IX. Risques restants

1. **Sous-module Git** : si `fr_assemblee_discourse_analysis` était un submodule, vérifier `.gitmodules` après renommage en `publication/`.
2. **Typo scripts_scraîng** : conservée pour éviter rupture d'imports.
3. **Legacy fallback** : analysis/config conserve un fallback vers `fr_assemblee_discourse_analysis` si `publication` absent.

---

## X. Recommandation d'usage du repo final

| Rôle | Action |
|------|--------|
| **Analyste** | `analysis/` → lancer `run_analysis.py` |
| **Publication** | `publication/` → `prepare_data.py` puis exports |
| **Dataviz** | Ouvrir `site/index.html` ou `index.html` (redir.) |
| **Pipeline** | `pipeline/collection/` (collecte), `pipeline/annotation/` (annotation) |
| **Lecture rapide** | `docs/workspace/QUICKSTART.md` |

Un lecteur comprend en 30 secondes :
- **Canonique** : `analysis/`
- **Publication** : `publication/`
- **Dataviz** : `site/index.html`
- **Archive** : `archive/`
- **Pipelines** : `pipeline/collection/`, `pipeline/annotation/`
