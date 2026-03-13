# Migration Plan (Safe, Dependency-Verified)

## 1) Audit de dependances (resume operationnel)

### Tableau de verification

| Chemin | Role suppose | Role verifie | Utilise | Risque si deplacement | Action recommandee |
| --- | --- | --- | --- | --- | --- |
| `final/src/final_pipeline/` | collecte AN | pipeline Python modulaire (scraping + enrichment + outputs) | oui | eleve | conserver, migrer plus tard vers `pipeline/collect/` |
| `final/scripts_scraîng/` | scripts scraping X/Nitter | scripts d'orchestration + tests + extraction | oui | eleve | conserver, classer scripts prod vs debug |
| `final/data/` | sorties collecte | source amont pour `projet_gaza` | oui | eleve | ne pas deplacer avant abstraction config |
| `projet_gaza/src/preprocessing/` | consolidation/filtrage | depend explicitement de `../final/data/...` | oui | eleve | introduire config de chemin avant deplacement |
| `projet_gaza/src/annotation/` | annotation LLM v3/v4 | scripts actifs appeles par run_*.py | oui | eleve | conserver tel quel lot 0 |
| `projet_gaza/outputs/` | sorties annotation et NLP | alimente `fr_assemblee_discourse_analysis/src/prepare_data.py` (`annotations_v4_*.parquet`) | oui | eleve | conserver |
| `analyse_discursive_depute/scripts/run_analysis.py` | moteur analytics principal | produit la majorite des CSV/figures | oui | eleve | coeur canonique recommande |
| `analyse_discursive_depute/src/prepare_data.py` | pont vers source | copie corpus/resultats depuis `fr_assemblee_discourse_analysis` | oui | eleve | garder compatibilite, externaliser chemins |
| `analyse_discursive_depute/notebooks/` | analyses detaillees | 01-13, references relatives `../data/results` | oui | moyen-eleve | conserver structure interne |
| `fr_assemblee_discourse_analysis/src/prepare_data.py` | pipeline publication | depend de `ROOT.parent/projet_gaza` | oui | eleve | maintenir tant que non refactore |
| `fr_assemblee_discourse_analysis/src/build_analyses_extended.py` | exports publication | complete les CSV au-dela de `run_analysis.py` | oui | eleve | garder comme couche publication |
| `fr_assemblee_discourse_analysis/docs/` | docs publication-ready | references de structure et commandes | oui | moyen | mettre a jour apres migration |
| racine `index.html` + `scripts/` + `data/*.csv` | dataviz editoriale | consommation directe CSV statiques | oui | moyen | migrer ensemble vers `site/` sans casser paths |
| `.cache/deputes/` | cache scraping | scripts js locaux lisent/ecrivent ce dossier | partiel | faible-moyen | sortir du repo suivi / archiver snapshot |
| `archive/legacy_workspaces/_archive/` | archives historiques | pas d'import runtime detecte | non (runtime) | faible | deja archive |
| `archive/pocs/nitter-scraper-basics/` | POC | non reference par pipeline principal | non | faible | deja archive |
| `analyse_discursive_depute/DATA_VIZ_Article/AI_protype/` | prototype React dataviz | projet independant Vite | partiel | moyen | conserver, classer en `site/prototypes/` plus tard |
| `requirements.txt` (racine) | deps globales | minimale (puppeteer via `package.json` root; deps Python surtout en sous-projets) | partiel | moyen | harmoniser politique deps |

### Doublons de noms (risque de confusion)

- `README.md` (racine + sous-projets)
- `requirements.txt` (racine + `final/` + `projet_gaza/` + `analyse_discursive_depute/` + `fr_assemblee_discourse_analysis/`)
- `config.py` (au moins 3 variantes actives)
- `prepare_data.py` (deux variantes avec semantiques differentes)

### Fichiers morts probables (a verifier avant move)

- POC `archive/pocs/nitter-scraper-basics/`
- scripts tests ad hoc `projet_gaza/test_*.py`
- artefacts HTML de debug dans `final/logs/` et `.cache/deputes/`

## 2) Choix repo canonique (decision)

### Comparaison courte

- **Completude analytique**: `analyse_discursive_depute` > `fr_assemblee_discourse_analysis`
- **Qualite docs publication**: `fr_assemblee_discourse_analysis` > `analyse_discursive_depute`
- **Reproductibilite locale**: mixte pour les deux (dependances cross-folder)
- **Valeur publicationnelle immediate**: `fr_assemblee_discourse_analysis` forte, mais pipeline incomplet seul
- **Dette technique**: la plus faible dans `fr_assemblee_discourse_analysis`, mais couverture analytique plus reduite

### Recommandation nette

- **Repo canonique recommande**: `analyse_discursive_depute` (coeur analytique)
- **Couches a conserver dans le meme repo**:
  - `publication/` derive de `fr_assemblee_discourse_analysis`
  - `pipeline/collect+annotation` derives de `final` et `projet_gaza`
  - `site/` derive de la racine editoriale
- **A archiver**: `archive/legacy_workspaces/_archive/`, `archive/pocs/nitter-scraper-basics/`, logs/cache non canoniques
- **Hors repo eventuel**: datasets lourds bruts/interim et snapshots de scraping

## 3) Plan de migration securise (avant mouvements)

### Lot 0 (non destructif, immediat)

1. Ecrire docs de migration (`MIGRATION_PLAN.md`, `REPO_STRUCTURE_PROPOSED.md`, `FILES_TO_ARCHIVE.md`, `PATHS_TO_UPDATE.md`).
2. Durcir `.gitignore`.
3. Ajouter `ROOT_README.md` (README racine de publication GitHub).

### Lot 1 (safe move faible risque)

1. Creer `archive/`.
2. Deplacer `_archive/` -> `archive/legacy_workspaces/_archive/` (fait).
3. Deplacer `nitter-scraper-basics/` -> `archive/pocs/nitter-scraper-basics/` (fait).
4. Mettre a jour docs mentionnant ces chemins.

Verification lot 1:
- `rg` references mortes sur anciens chemins archive.

### Lot 2 (normalisation chemins, sans deplacement majeur)

1. Introduire variables de chemin centralisees pour `final`, `projet_gaza`, `fr_assemblee_discourse_analysis`, `analyse_discursive_depute`.
2. Remplacer chemins `ROOT.parent/...` par env vars explicites.
3. Stabiliser notebooks (cellule `PROJECT_ROOT` commune).

Verification lot 2:
- `python .../prepare_data.py` (les deux variantes)
- `python analyse_discursive_depute/scripts/run_analysis.py` (smoke mode)
- presence des CSV cles.

### Lot 3 (migration logique vers structure cible)

1. Migrer couches vers `pipeline/`, `publication/`, `site/` (par sous-dossier complet).
2. Reecrire imports et chemins references.
3. Harmoniser documentation.

Verification lot 3:
- scripts principaux executables
- docs sans liens morts
- dataviz web lit toujours les CSV attendus.

## 4) Points non verifies (bloquants de deplacement massif)

- scripts/tests executes manuellement hors repo mais non traces dans code;
- notebooks contenant sorties executees avec chemins machine locaux (non bloquants runtime, mais bruit);
- statut reel du repo imbrique git dans `fr_assemblee_discourse_analysis` (a decider avant fusion finale).
