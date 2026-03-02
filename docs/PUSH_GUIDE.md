# Guide push GitHub — version finale

## Pré-push : checklist

### À vérifier avant de committer

- [ ] Aucune sortie d'erreur dans les notebooks (pas de traceback)
- [ ] README et chiffres cohérents avec `data/results/` (event_impact, panel_b4, etc.)
- [ ] `python src/prepare_data.py` et `python src/build_extra_analyses.py` tournent sans erreur (avec corpus si dispo)
- [ ] Pas de fichiers sensibles (tokens, clés API)
- [ ] `.gitignore` exclut bien `data/processed/`, `*.parquet`, `.ipynb_checkpoints/`, `.cursor/`

### Structure finale à pousser

```
├── notebooks/01-08
├── src/ (config, prepare_data, build_extra_analyses, export_figures_social)
├── data/
│   ├── README.md
│   └── results/*.csv  (versionnés)
├── figures/.gitkeep
├── docs/ (METHODOLOGIE, DONNEES, CATALOGUE_FIGURES, PUSH_GUIDE)
├── README.md, LICENSE, pyproject.toml
├── requirements.txt, requirements-lock.txt
└── .gitignore
```

### Non versionnés (déjà dans .gitignore)

- `data/processed/` (corpus parquet)
- `data/raw/`
- `*.parquet`, `__pycache__/`, `.ipynb_checkpoints/`, `.cursor/`

---

## Push vers GitHub

### Cas 1 : Nouveau dépôt (repo_propre devient la racine)

```bash
cd repo_propre
git init
git add .
git status   # Vérifier les fichiers ajoutés
git commit -m "Version finale : analyse discursive Gaza (2023-2026)"
git branch -M main
git remote add origin https://github.com/VOTRE_USER/VOTRE_REPO.git
git push -u origin main
```

### Cas 2 : Remplacer un dépôt existant (écraser l'ancien)

```bash
cd repo_propre
git init
git add .
git commit -m "Version finale : analyse discursive Gaza (2023-2026)"
git branch -M main
git remote add origin https://github.com/VOTRE_USER/VOTRE_REPO.git
git push -u origin main --force
```

> `--force` écrase l'historique distant. À utiliser uniquement si vous acceptez de perdre les anciens commits.

### Cas 3 : repo_propre est dans un projet déjà versionné

Si le parent `Revirement_politique_fr_gaza` est le dépôt Git, deux options :

**A.** Pousser uniquement le contenu de repo_propre à la racine du dépôt :

```bash
cd Revirement_politique_fr_gaza
# Supprimer tout sauf repo_propre, déplacer contenu de repo_propre à la racine
# Puis git add, commit, push
```

**B.** Garder repo_propre comme sous-dossier et pousser le tout. Les anciens fichiers restent ; si vous voulez les retirer :

```bash
git rm -r --cached .   # Unstage tout
# Modifier .gitignore si besoin
git add .
git status
git commit -m "Nettoyage : repo_propre comme version finale"
git push
```

---

## Après le push

1. Vérifier sur GitHub que les notebooks s'affichent correctement
2. Exécuter `pip freeze > requirements-lock.txt` dans l'environnement de travail, puis committer et pousser (optionnel, pour reproductibilité stricte)
3. Si besoin, activer GitHub Pages pour la doc (optionnel)
