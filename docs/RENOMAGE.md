# Nommage professionnel du projet

## Contexte

Le dossier local `repo_propre` est un nom de travail interne. Pour un usage professionnel (portfolio, recrutement), il est recommandé de le renommer.

## Recommandations

| Option | Nom proposé | Usage |
|--------|-------------|-------|
| **A** | `Analyse_discursive_depute_fr_sur_conflit_Israelo_Palestinien` | Alignement exact avec le dépôt GitHub |
| **B** | `analyse-discursive-gaza` | Nom court, kebab-case, lisible |
| **C** | `gaza-discourse-analysis` | Nom anglais, international |

Le dépôt GitHub est déjà nommé : `SamiNakibETU/Analyse_discursive_depute_fr_sur_conflit_Israelo_Palestinien`

## Procédure de renommage (Windows PowerShell)

À exécuter depuis le dossier **parent** (`Revirement_politique_fr_gaza` ou `Projets`) :

```powershell
# Option B (recommandé — court et pro)
Rename-Item -Path "repo_propre" -NewName "analyse-discursive-gaza"

# OU Option A (aligné GitHub)
Rename-Item -Path "repo_propre" -NewName "Analyse_discursive_depute_fr_sur_conflit_Israelo_Palestinien"
```

## Après le renommage

1. **Cursor/VS Code** : rouvrir le dossier renommé (File → Open Folder).
2. **Chemins** : aucun chemin dans le projet ne référence `repo_propre` — les scripts utilisent `Path(__file__).parent` et `config.ROOT`.
3. **Git** : le remote GitHub reste identique, le renommage local n'affecte pas le dépôt distant.
