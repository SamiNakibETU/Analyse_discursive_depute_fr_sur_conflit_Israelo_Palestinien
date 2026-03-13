# Convention de nommage — Lot 2c

Convention unique applicable au projet, alignée sur les objectifs : cohérence, clarté, neutralité, stabilité, compatibilité GitHub, lisibilité externe.

---

## 1. Principes généraux

| Principe | Règle |
|----------|-------|
| **Descriptivité** | Le nom décrit le rôle ou le contenu, pas une étape historique ("final", "v2"). |
| **Neutralité éditoriale** | Ne pas suggérer de causalité, d'interprétation ou de conclusion dans les noms techniques. |
| **Cohérence FR/EN** | Pipeline et artefacts techniques en **anglais** ; documents éditoriaux/publication peuvent rester en français si c'est la cible. |
| **Snake_case** | Pour tous les fichiers techniques (scripts, CSV, configs). |
| **Pas de suffixes vides** | Éviter `final`, `new`, `clean`, `full`, `complete`, `extended`, `v2/v3` sauf signification métier documentée. |

---

## 2. Dossiers

| Type | Convention | Exemples |
|------|-------------|----------|
| Racine projet | `snake_case` ou `kebab-case` ; nom descriptif | `data/`, `scripts/`, `reports/` |
| Données | `raw/`, `interim/`, `processed/` pour pipeline ; `results/` pour sorties analyse | cohérent avec usage réel |
| Documentation | `docs/` (anglais) ou `docs/` selon projet | `fr_assemblee_discourse_analysis/docs/` |
| Archive | `archive/` + sous-dossiers explicites | `archive/pocs/`, `archive/debug_logs/` |
| Éviter | `final/`, `outputs/`, `results/` quand ambigu avec d'autres couches | — |

**Note** : Le dossier `final/` est un nom historique pour la collecte. Son renommage est **différé** (chaîne canonique, nombreuses références).

---

## 3. Scripts Python

| Règle | Exemple |
|-------|---------|
| `snake_case` | `run_analysis.py`, `prepare_data.py` |
| Verbe d'action en premier | `build_*`, `run_*`, `prepare_*`, `merge_*` |
| Suffixe descriptif (pas `extended`, `supplementaires` si vague) | `build_publication_exports.py` plutôt que `build_analyses_extended.py` |
| Nom reflétant la fonction | `run_annotation.py` (version en variable ou chemin) |

---

## 4. Notebooks

| Règle | Exemple |
|-------|---------|
| Numéro + description courte | `01_portrait_corpus.ipynb`, `03_dynamiques_temporelles.ipynb` |
| Pas de `final`, `test` sauf notebook de test explicite | — |

---

## 5. Fichiers CSV / parquet

| Règle | Exemple |
|-------|---------|
| `snake_case` | `frames_par_bloc.csv`, `stance_mensuel.csv` |
| Nom descriptif et neutre | `event_window_comparison.csv` plutôt que nom suggérant causalité |
| Version explicite si nécessaire | `corpus_v3.parquet` (v3 = schéma annotation documenté) |

**Exemple de neutralité** :
- ❌ `event_impact_diff_in_diff.csv` → suggère un diff-in-diff causal
- ✅ `event_window_comparison.csv` ou `before_after_event_comparison.csv` → descriptif

---

## 6. Documents Markdown

| Règle | Exemple |
|-------|---------|
| UPPER_SNAKE pour docs racine projet (legacy) | `MIGRATION_PLAN.md` (reste pour cohérence livrables Lot 0–1) |
| `snake_case` ou `UPPER_SNAKE` selon sous-projet | `COMPTE_RENDU_RESULTATS.md` → `results_report.md` (proposé) |
| Titre descriptif, pas conclusif si contenu exploratoire | `results_summary.md` plutôt que `RESULTATS_FINAUX.md` |
| Brief/synthèse | `analytical_brief.md` ou `results_brief.md` |

---

## 7. Figures et assets

| Règle | Exemple |
|-------|---------|
| Préfixe catalogue si applicable | `fig25_twitter_vs_an.png` |
| Nom descriptif | `stance_ribbon_by_bloc.png` |

---

## 8. Scripts JavaScript / Node

| Règle | Exemple |
|-------|---------|
| `snake_case` | `scrape_nitter_search_monthly.js` |
| Préfixe `test_` seulement pour tests unitaires ou scripts de validation | `test_nitter_rate_limits.js` (OK) |
| Éviter `test_simple_20_tweets.js` → nommer par objectif | `scrape_sample_tweets.js` |

---

## 9. Fichiers de configuration

| Règle | Exemple |
|-------|---------|
| `snake_case` ou `kebab-case` | `project_settings.json`, `twitter_corrections.json` |

---

## 10. Exceptions documentées

| Élément | Raison |
|--------|--------|
| `corpus_v3`, `corpus_v4` | Version = schéma d'annotation, documenté dans méthodo |
| `tweets_v3_full_clean.parquet` | Historique pipeline projet_gaza ; trop de dépendances pour renommer sans lot dédié |
| `final/` (dossier) | Nom historique, chaîne canonique |
| `scripts_scraîng/` | Typo (î) ; renommage = risques chemins multiplés |

---

## 11. Checklist avant tout renommage

- [ ] Vérifier imports et appels (grep)
- [ ] Vérifier références dans docs, notebooks, configs, HTML
- [ ] Vérifier qu'aucune ambiguïté nouvelle n'est créée
- [ ] Patcher toutes les références en même temps que le renommage
- [ ] Consigner dans RENAME_MAPPING.md
