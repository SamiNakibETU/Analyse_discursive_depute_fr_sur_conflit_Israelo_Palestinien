# Table de correspondance — Renommages Lot 2c

| Ancien nom | Nouveau nom | Justification | Priorité | Statut |
|------------|-------------|---------------|----------|--------|
| `final/RESULTATS_FINAUX.md` | `final/scraping_results_summary.md` | Éviter "FINAL" redondant ; nom descriptif et neutre | Importante | Appliqué |
| `final/RAPPORT_FINAL_SCRAPING.md` | `final/scraping_report.md` | Éviter "FINAL" ; nom court et descriptif | Importante | Appliqué |
| `analyse_discursive_depute/reports/brief_analytique.md` | `analyse_discursive_depute/reports/analytical_brief.md` | Cohérence anglais ; descriptif | Importante | Appliqué |
| `fr_assemblee_discourse_analysis/docs/COMPTE_RENDU_RESULTATS.md` | `fr_assemblee_discourse_analysis/docs/results_report.md` | Nom neutre, cohérent ; nombreux refs | Importante | **Différé** |
| `analyse_discursive_depute/reports/RESULTATS_NUMERIQUES.md` | `analyse_discursive_depute/reports/numerical_results.md` | Produit par script ; renommage = modifier run_analysis.py | Critique | **Différé** |
| `analyse_discursive_depute/data/results/RAPPORT_RESULTATS.txt` | `analyse_discursive_depute/data/results/analysis_report.txt` | Produit par script ; chemins codés | Critique | **Différé** |
| `final/` (dossier) | `collect/` ou `pipeline_collect/` | Nom historique devenu trompeur | Critique | **Différé** |
| `final/src/final_pipeline/` | (dépend de renommage `final/`) | Redondance | Critique | **Différé** |
| `final/scripts_scraîng/` | `final/scripts_scraping/` | Corriger typo "scraîng" | Importante | **Différé** |
| `fr_assemblee_discourse_analysis/src/build_analyses_extended.py` | `build_publication_exports.py` | "extended" vague | Critique | **Différé** |
| `fr_assemblee_discourse_analysis/src/analyses_supplementaires.py` | `analyses_auxiliary.py` ou `supplementary_analyses.py` | Cohérence EN | Critique | **Différé** |
| `final/scripts_scraîng/build_twitter_deputes_clean.py` | `build_twitter_deputes_mapping.py` | "clean" vague | Importante | **Différé** |
| `final/scripts_scraîng/test_simple_20_tweets.js` | `scrape_sample_tweets.js` | Nom descriptif | Importante | **Différé** |
| `final/scripts_scraîng/test_one_depute.js` | `scrape_single_deputy.js` | Nom descriptif | Importante | **Différé** |
| `final/scripts_scraîng/test_mathilde_panot_full.js` | `scrape_deputy_full_timeline.js` | Éviter "full", "test" | Importante | **Différé** |
| `tweets_v3_full_clean.parquet` | `tweets_v3_annotated.parquet` | "full_clean" vague | Critique | **Différé** |
| `interventions_v3_full_clean.parquet` | `interventions_v3_annotated.parquet` | Idem | Critique | **Différé** |
| `deputes_twitter_clean.json` | `deputes_twitter_mapping.json` | "clean" vague | Importante | **Différé** |
| `twitter_deputes_final.jsonl` | `twitter_deputes_consolidated.jsonl` | "final" vague | Importante | **Différé** |
| `interventions_gaza_final.csv` | `interventions_filtered.csv` | Éviter "gaza", "final" | Importante | **Différé** |
| `event_impact_diff_in_diff.csv` | `event_window_comparison.csv` | Neutralité éditoriale ; pas de causalité implicite | Critique | **Différé** |
| `ARBORESCENCE_FINALE_PROPOSEE.md` | `proposed_structure.md` | Éviter "FINALE" conclusif | Optionnelle | Proposé |
| `analyse_discursive_depute/DATA_VIZ_Article/AI_protype` | `AI_prototype` | Corriger typo | Optionnelle | Proposé |

---

## Légende statuts

- **Appliqué** : Renommage effectué en Lot 2c, références patchées.
- **Différé** : Proposé mais non appliqué ; trop de dépendances ou risque élevé.
- **Proposé** : Recommandation pour lot ultérieur.
