# Audit final — repo_propre (27 fév. 2026)

## État du dépôt Git

| Élément | Statut |
|--------|--------|
| `git init` | ✅ Fait |
| Premier commit | ✅ `ffec248` — 142 fichiers |
| Remote GitHub | ⏳ À configurer (voir ci-dessous) |

---

## Contenu versionné

### Exclus (`.gitignore`)
- `data/processed/` (corpus parquet)
- `data/raw/`
- `*.parquet`, `__pycache__/`, `.ipynb_checkpoints/`, `.cursor/`

### Inclus
- **8 notebooks** (01 → 08) : corpus, validation, dynamiques, polarisation, événements, convergence, émotions, analyses de fond
- **4 scripts** : `config.py`, `prepare_data.py`, `build_extra_analyses.py`, `export_figures_social.py`
- **24 CSV** dans `data/results/` (event_impact, panel_b4, stance, convergence, etc.)
- **~100 figures** PNG (figures/ + figures/social/)
- **Docs** : METHODOLOGIE, DONNEES, CATALOGUE_FIGURES, PUSH_GUIDE

---

## Vérifications effectuées

| Point | Résultat |
|-------|----------|
| Traceback / erreurs dans notebooks | ✅ Aucune sortie d’erreur visible |
| BRIEF, KEY_FINDINGS, TODO.md | ✅ Absents |
| Panel B4 | ✅ 44 députés (panel_b4.csv) |
| Config centralisée (BATCHES, SOURCE_PROJECT) | ✅ |

---

## Push vers GitHub — action requise

**GitHub CLI (`gh`) n’est pas installé.** Pour pousser :

1. **Créer le dépôt sur GitHub** (interface web)  
   Ex. : `revirement-gaza-fr` ou `gaza-parliamentary-discourse`

2. **Ajouter le remote et pousser** :
   ```powershell
   cd "d:\Users\Proprietaire\Desktop\Projet_perso\Projets\Revirement_politique_fr_gaza\repo_propre"
   git remote add origin https://github.com/VOTRE_USER/VOTRE_REPO.git
   git branch -M main
   git push -u origin main
   ```

   Pour **remplacer** un dépôt existant :
   ```powershell
   git push -u origin main --force
   ```

3. **Alternative** : installer [GitHub CLI](https://cli.github.com/) et lancer :
   ```powershell
   gh auth login
   gh repo create revirement-gaza-fr --public --source=. --push
   ```
