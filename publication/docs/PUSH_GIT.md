# Pousser vers GitHub sans déclencher Cursor Agent

> **Checklist complète** : voir [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md)

Pour pousser vos commits vers GitHub **sans que Cursor n'exécute d'agent ou d'automatisation** :

## Option 1 : Terminal (recommandé)

Utilisez le terminal intégré de Cursor ou un terminal externe (PowerShell, cmd) :

```bash
cd d:\Users\Proprietaire\Desktop\Projet_perso\Projets\Revirement_politique_fr_gaza\fr_assemblee_discourse_analysis

git add .
git status
git commit -m "votre message"
git push origin main
```

*(Remplacez `main` par `master` si c'est le nom de votre branche.)*

Le `git push` depuis le terminal est une commande standard et n'active pas les fonctionnalités Cursor (agent, règles, etc.).

## Option 2 : Interface Source Control de Cursor

Si vous utilisez l’onglet Source Control (icône branche) :

1. Faites vos modifications
2. Cochez les fichiers à inclure
3. Saisissez le message de commit
4. Cliquez sur **Commit**
5. Cliquez sur **Sync** ou **Push**

Si Cursor propose des actions liées à l’agent lors du push, ignorez-les ou annulez.

## Option 3 : GitHub Desktop ou autre client Git

Utiliser un client Git externe (GitHub Desktop, GitKraken, etc.) évite toute interaction avec les outils Cursor.

## Commits suggérés (brief 28 fév. 2026)

```bash
git add docs/CODEBOOK.md docs/METHODOLOGIE.md
git commit -m "docs: add codebook and methodology documentation"

git add notebooks/03_evenements_convergence.ipynb
git commit -m "analysis: add bloc×batch interaction forest plot to regression"

git add src/analyses_supplementaires.py data/results/twitter_vs_an.csv
git commit -m "analysis: add Twitter vs AN comparison (fig25)"

git add .
git commit -m "analysis: add RN vs LR temporal, attrition, fighting words, Droite shift"

git add README.md
git commit -m "readme: add key figures, citation, research directions"
```

## Actions manuelles sur GitHub (Settings → General → About)

- **Description** : "Analyse computationnelle du discours de 459 députés français sur le conflit israélo-palestinien (oct. 2023 – jan. 2026). 10 774 textes annotés par LLM, science politique computationnelle."
- **Topics** : `nlp`, `computational-social-science`, `political-discourse`, `french-politics`, `text-analysis`, `llm-annotation`, `stance-detection`, `discourse-analysis`

## Vérifications

- Le dossier `.cursor/` est dans `.gitignore` - il ne sera pas poussé.
- Les dossiers `archive/` et `data/raw/` sont également exclus.
- Vérifiez avec `git status` avant de committer qu’aucun fichier sensible n’est inclus.
