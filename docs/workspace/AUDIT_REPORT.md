# AUDIT PROJET AN-GAZA

## 1. ETAT DES LIEUX

### Donnees disponibles
- Periode couverte (scraping brut): 2023-01-09 -> 2025-06-05 (sessions AN v3)
- Periode couverte (jeux filtres existants): 2022-07-06 -> 2025-06-05
- Nombre de locuteurs uniques (brut): 2 440
- Interventions totales collecteess (brut): 353 251
- Interventions identifiees comme pertinentes (dernier filtrage): 1 589
- Taux de couverture des interventions pertinentes: 0,45 % du corpus brut (v3)
- Jeux CSV legacy (V2 et final): 4 099 lignes (final) et 354 lignes (V2) avec recouvrements partiels

### Fichiers de donnees
| Fichier | Type | Taille | Periode | Qualite | Notes |
|---------|------|--------|---------|---------|-------|
| an_scraper_v3/assemblee_nationale_interventions.json | JSON | 194.6 MB | 2023-01-09 -> 2025-06-05 | 4/5 | Donnees brutes par seance (~353k interventions), depend d un config.py manquant |
| resultats_analyse/seances_pertinentes.json | JSON | 58.6 MB | 2023-01-09 -> 2025-06-05 | 3/5 | Sous-ensemble sessions retenues (200), volume lourd et redondant |
| resultats_analyse/interventions_pertinentes.json | JSON | 2.4 MB | 2023-01-09 -> 2025-06-05 | 3/5 | 1 589 interventions etiquetees, groupes partiellement manquants |
| scrapping_V2/interventions.csv | CSV | 0.6 MB | 2022-08-02 -> 2025-06-03 | 2/5 | Scraper V2, accents corrompus, duplications possibles |
| scrapping_V2/interventions_analysees.csv | CSV | 0.5 MB | 2022-08-02 -> 2025-06-03 | 2/5 | Version enrichie (periode/groupe) mais 148 orateurs uniquement |
| final/interventions_gaza_final.csv | CSV | 7.2 MB | 2022-07-06 -> 2024-06-07 | 2/5 | Export agrege (4 099 lignes) mais colonnes keywords et affiliation vides |

### Scripts Python
| Script | Fonction | Etat | Dependances | Recommandation |
|--------|----------|------|-------------|----------------|
| an_scraper_v3/scraper_an.py | Scraping complet AN (v3) | Bloque (config absent) | requests, bs4, lxml, tqdm | Restaurer config.py, externaliser parametres et valider reprise |
| an_scraper_v3/process_interventions.py | Filtrage mots-cles + mapping groupes | Partiel (groupes manquants) | pandas, tqdm | Mettre les mots-cles a jour, completer mapping deputes 17e |
| an_scraper_v3/authenticated_deputy_scraper.py | Scraper Twitter connecte (prototype) | Non teste/stable | undetected_chromedriver, selenium | Evaluer besoins, passer sur Nitter si possible |
| an_scraper_v3/improved_creator.py | Creation comptes X automatisee | Prototype risque | undetected_chromedriver, faker | Mettre de cote (risque legal et maintenance) |
| scrapping_V2/main_v3.py | Scraper legacy par recherche mot cle | Fonctionnel mais obsolete | requests, bs4, csv | Deprecier apres validation v3 |
| scrapping_V2/analyse_finale_complete.py | Analyse lexicale avancee | Fonctionnel (lourd) | pandas, numpy, nltk, wordcloud | Factoriser en modules reutilisables |
| scrapping_V2/analyse_discursive.py | Analyse discursive (plots) | Fonctionnel (legacy) | pandas, seaborn | Migrer vers notebooks/modulaire |
| scrapping_V2/analyse_lexicale_complete.py | Extraction mots-cles themes | Fonctionnel | pandas, wordcloud | Mutualiser avec pipeline NLP |
| scrapping_V2/analyse_revirements_2024.py | Revirements 2024 | Fonctionnel (ad hoc) | pandas, seaborn | Integrer dans pipeline temporel |
| scrapping_V2/analyse_revirements_2025_avancee.py | Revirements 2025 detaille | Fonctionnel (lourd) | pandas, nltk | Consolider avec module unique |
| scrapping_V2/analyse_2025_simple.py | Diagnostic rapide 2025 | Fonctionnel | pandas | Fusionner avec analyse_revirements |
| scrapping_V2/check_2025_data.py | Verification 2025 | Fonctionnel | pandas | Conserver comme verification rapide |
| scrapping_V2/test_analyse_avancee.py | Test pipeline NLP | Fonctionnel (tests manuels) | pandas, nltk | Convertir en notebook ou tests unitaires |
| archive/pocs/nitter-scraper-basics/scraper.js | Proof of concept Puppeteer Nitter | POC isole | puppeteer, json2csv | Refondre dans future archi Twitter |

## 2. PROBLEMES IDENTIFIES
- [x] config.py introuvable pour an_scraper_v3 : le scraper principal ne peut pas tourner tel quel
- [x] Export final interventions_gaza_final.csv incomplet (keywords, affiliation, periode vides)
- [x] Donnees legacy (V2) corrompues en encodage et partiellement redondantes avec v3
- [x] Mapping groupes politiques incomplet -> 27 % des interventions marquees "Groupe non identifie"
- [x] Aucun pipeline unifie (scraping -> filtrage -> analyses) : scripts multiples sans orchestration
- [x] Module Twitter/Nitter absent; prototypes Selenium risquent de devenir obsoletes

## 3. POINTS FORTS
- V3 du scraper capitalise un dump massif (353k interventions) pret a etre retravaille
- Ensemble d analyses Python deja riche (lexical, temporel, revirements) couvrant plusieurs axes
- Keywords configures et reutilisables pour filtrage initial
- Presence de journaux (scraping.log, processed_urls.log) facilitant la reprise

## 4. LACUNES DANS LES DONNEES
- Absence de normalisation pour les noms/prenoms et affiliations dans le CSV final
- Pas de dictionnaire fiable Deputes -> Groupes pour la 17e legislature (depuis juillet 2024)
- Donnees Twitter totalement manquantes; aucun mapping Deputes -> comptes valide
- Champs keywords_found, relevance_score non renseignes ou heuristiques basiques

## 5. RECOMMANDATIONS
1. Restaurer et versionner la configuration du scraper v3 (config.py, keywords, pagination) puis relancer pour couvrir Oct 2023 -> present
2. Rejouer le filtrage via process_interventions.py avec mapping deputes mis a jour pour corriger les groupes manquants
3. Deprecier les CSV legacy v2 apres migration et documenter le format cible (processed/interventions_gaza.csv)
4. Industrialiser les analyses en modules (preprocessing, detection keywords, sentiment) reutilisables entre AN et Twitter
5. Concevoir un module Nitter robuste (sans Selenium) et un mapping semi-automatise Deputes -> comptes avant toute collecte Twitter
6. Mettre en place un entrepot de donnees structure (raw/processed/analysis) avec versionnage clair et scripts d ETL
