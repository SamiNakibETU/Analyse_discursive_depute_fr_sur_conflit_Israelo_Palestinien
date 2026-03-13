# Lot 2c — Audit de nommage

Date : 2025-03-13  
Objectif : Identifier les problèmes de nommage sans casser la chaîne canonique.

> **Note** : Trois renommages ont été appliqués après cet audit (voir SAFE_RENAMES_APPLIED.md) : RESULTATS_FINAUX → scraping_results_summary, RAPPORT_FINAL_SCRAPING → scraping_report, brief_analytique → analytical_brief.

---

## 1. Dossiers

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `final/` | Collecte AN + scraping Twitter | Nom ambigu : suggère "version définitive" plutôt que "étape de collecte". Historique, devenu trompeur. | Élevé : référencé dans configs, consolidate_tweets.py, merge_twitter_sources.py, nombreux docs | Critique |
| `final/src/final_pipeline/` | Modules Python de collecte/scraping | Redondance "final" + "final". Ambiguïté sur "pipeline". | Élevé : imports `final_pipeline`, PYTHONPATH | Critique |
| `final/scripts_scraîng/` | Scripts scraping Nitter/Node | Typo : "scraîng" (î) au lieu de "scraping". Incohérence. | Élevé : nombreuses réf. docs, chemins relatifs dans scripts | Importante |
| `final/data/` | Données intermédiaires et sorties | Ambigu : raw/interim/processed mélangés sous un seul "data". | Moyen : chemins codés en dur dans plusieurs projets | Importante |
| `projet_gaza/outputs/` | Sorties annotation NLP | Nom éditorial ("projet_gaza") + "outputs" vague. | Moyen : prepare_data.py, config.py | Importante |
| `archive/` | Archives legacy, POCs | Acceptable. Nom clair. | — | — |
| `reports/` | Rapport d'audit racine | Acceptable. | — | — |
| `data/` (racine) | CSV dataviz éditoriale | Acceptable mais doublon avec fr_assemblee_discourse_analysis/data/results. | — | Optionnelle |
| `analyse_discursive_depute/DATA_VIZ_Article/` | Prototypes dataviz | Mélange MAJ/min. "Article" éditorial. | Faible | Optionnelle |
| `analyse_discursive_depute/DATA_VIZ_Article/AI_protype` | Prototype React/Viz | Typo : "protype" au lieu de "prototype". | Faible : interne au sous-dossier | Optionnelle |

---

## 2. Fichiers Markdown — Documents

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `final/RESULTATS_FINAUX.md` | Résultats tests scraping Mathilde Panot | "FINAL" redondant. Trop conclusif. Peu descriptif. | Faible : 2–3 réf. docs (RAPPORT_FINAL_SCRAPING, auto-ref) | Importante |
| `final/RAPPORT_FINAL_SCRAPING.md` | Rapport technique scraping | "FINAL" redondant. Mélange FR MAJ. | Faible : auto-ref, GUIDE_EXECUTION | Importante |
| `fr_assemblee_discourse_analysis/docs/COMPTE_RENDU_RESULTATS.md` | Compte rendu exhaustif analyses | "COMPTE_RENDU" long. Cohérent en FR. | Moyen : 5+ réf. (README, PUSH_GIT, PUBLICATION_CHECKLIST, REPO_STRUCTURE, FIGURE_TRACEABILITY) | Importante |
| `analyse_discursive_depute/reports/brief_analytique.md` | Synthèse analytique résultats | Mélange FR/EN. "brief" peut prêter à confusion. | Faible : 1 réf. README | Importante |
| `analyse_discursive_depute/reports/RESULTATS_NUMERIQUES.md` | Export MD chiffres/séries (run_analysis.py) | MAJ, long. Produit par script. | Moyen : script écrit le chemin, refs dans brief_analytique, DONNEES | Critique |
| `analyse_discursive_depute/data/results/RAPPORT_RESULTATS.txt` | Rapport métriques (run_analysis.py) | MAJ, redondant "RESULTATS". Produit par script. | Élevé : script, brief_analytique, METHODOLOGIE | Critique |
| `final/PIPELINE_SUMMARY.md` | Vue d’ensemble pipeline | Acceptable. "PIPELINE" cohérent. | — | Optionnelle |
| `final/PIPELINE_TWITTER_README.md` | Guide pipeline Twitter | Long. Redondance pipeline. | Faible | Optionnelle |
| `ARBORESCENCE_FINALE_PROPOSEE.md` | Structure proposée | "FINALE" trop conclusif. "PROPOSEE" correct. | Faible : peu de réf. | Optionnelle |
| `ROOT_README.md` | README racine migration | "ROOT" technique. Acceptable pour contexte migration. | — | Optionnelle |

---

## 3. Scripts Python

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `fr_assemblee_discourse_analysis/src/build_analyses_extended.py` | Exports CSV complémentaires (trajectoires, movers, etc.) | "extended" peu informatif. | Élevé : Makefile, README, COMPTE_RENDU, docs | Critique |
| `fr_assemblee_discourse_analysis/src/analyses_supplementaires.py` | Figures fig21–25 (Twitter vs AN, attrition, etc.) | "supplementaires" FR. Cohérence avec build_analyses_extended. | Élevé : Makefile, README, COMPTE_RENDU, docs | Critique |
| `final/scripts_scraîng/build_twitter_deputes_clean.py` | Construction mapping députés Twitter | "clean" peu informatif (quoi nettoyé ?). | Moyen : PIPELINE_TRACEABILITY, GUIDE_EXECUTION | Importante |
| `archive/.../scrapping_V2/analyse_finale_complete.py` | Analyse lexicale legacy | "finale", "complete" historiques. En archive. | Nul : archivé | Optionnelle |

---

## 4. Scripts JavaScript / Node

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `final/scripts_scraîng/test_simple_20_tweets.js` | Test scraping 20 tweets | "test" + "simple" : ad hoc, peu descriptif. | Faible : pas d’import détecté | Importante |
| `final/scripts_scraîng/test_one_depute.js` | Test scraping 1 député | "test" ad hoc. | Faible | Importante |
| `final/scripts_scraîng/test_mathilde_panot_full.js` | Test scraping MP complet | "full" peu informatif. "test" ad hoc. | Faible : output path codé | Importante |
| `final/scripts_scraîng/test_method_*.js` | Tests méthodes pagination | Mentionnés dans DIAGNOSTIC_COMPLET. En logs. | Faible | Optionnelle |

---

## 5. Fichiers de données — Parquet / JSON

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `tweets_v3_full_clean.parquet` | Tweets annotés v3 | "full_clean" : redondant, peu informatif. v3 explicite (corpus). | Très élevé : config.py, prepare_data.py, 5+ notebooks, nlp_pipeline, run_annotation_v*.py | Critique |
| `interventions_v3_full_clean.parquet` | Interventions AN annotées v3 | Idem. | Idem | Critique |
| `corpus_v3.parquet` / `corpus_v4.parquet` | Corpus préparés analyse | v3/v4 cohérents (version corpus). | Élevé : config.py | Critique |
| `deputes_twitter_clean.json` | Mapping députés Twitter | "clean" vague. | Moyen : scripts, GUIDE_EXECUTION | Importante |
| `twitter_deputes_final.jsonl` | Tweets consolidés (sortie pipeline) | "final" peu informatif. | Moyen : docs, scripts pipeline | Importante |
| `interventions_gaza_final.csv` | Export interventions filtrées | "final" + "gaza" éditorial. | Moyen : AUDIT_REPORT | Importante |

---

## 6. Fichiers CSV — Résultats canoniques

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `event_impact_diff_in_diff.csv` | Comparaisons avant/après événements par bloc | Nom suggère causalité (diff-in-diff) alors que pas de groupe contrôle. Peut prêter à surinterprétation. | Très élevé : main.js, run_analysis.py, notebooks, prepare_data.py, index.html, FIGURE_TRACEABILITY, composants TSX | Critique |
| `twitter_vs_an.csv` | Régression Twitter vs AN | Neutre. Descriptif. | Élevé : analyses_supplementaires, docs | — |
| `frames_par_bloc.csv` | Répartition cadres par bloc | Neutre. Cohérent. | Élevé : main.js, run_analysis, notebooks | — |
| `stance_mensuel.csv` | Stance moyen mensuel par bloc | Neutre. | Élevé | — |
| `emotional_register.csv` | Registres émotionnels | Neutre. | Élevé | — |
| `vue_ensemble.csv` | Vue d’ensemble par bloc | FR. Cohérent avec usage FR dans docs. | Élevé | Optionnelle |

---

## 7. Configs et autres

| Chemin actuel | Rôle réel | Problème | Risque si renommé | Priorité |
|---------------|-----------|----------|-------------------|----------|
| `PROMPT_PICTOGRAMMES.md` | Prompt pour pictogrammes | MAJ. Cohérent. | Faible | Optionnelle |
| `DESIGN_SYSTEM.md` | Design system dataviz | Cohérent. | Faible | Optionnelle |
| `twitter_account_deputés_2023_2024.txt` | Liste comptes Twitter | Accent "députés". Mélange. | Faible : peu réf. | Optionnelle |
| `twitter_account_député.md` | Doc comptes (si existe) | Idem. | Faible | Optionnelle |

---

## 8. Résumé des problèmes récurrents

- **Suffixes non informatifs** : `final`, `clean`, `full`, `complete`, `extended`, `supplementary`
- **Mélange FR/EN** : `brief_analytique`, `analyses_supplementaires`, `COMPTE_RENDU`, `vue_ensemble`
- **Noms éditoriaux** : `interventions_gaza_final`, `projet_gaza`, `event_impact_diff_in_diff` (causal)
- **Typo** : `scripts_scraîng`, `AI_protype`
- **MAJ incohérentes** : mélange `RESULTATS_FINAUX`, `brief_analytique`, `PIPELINE_SUMMARY`

---

## 9. Dépendances critiques (ne pas casser)

1. **Chaîne de données** : `tweets_v3_full_clean.parquet`, `interventions_v3_full_clean.parquet` → config.py, projet_gaza, fr_assemblee_discourse_analysis
2. **Chaîne CSV dataviz** : `data/*.csv` → `scripts/main.js`, `index.html`
3. **Scripts** : `build_analyses_extended.py`, `analyses_supplementaires.py` → Makefile, READMEs
4. **Chemins codés** : `final/`, `final_pipeline`, `scripts_scraîng` dans nombreux documents et configs
