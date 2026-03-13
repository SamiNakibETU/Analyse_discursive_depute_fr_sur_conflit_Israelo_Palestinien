# Checklist avant push

## 1. Fichiers sensibles

- [ ] `.Env` pas commité (dans .gitignore)
- [ ] `archive/` ignoré
- [ ] Aucun secret en clair

## 2. Structure

- [ ] Les 5 CSV dans `site/data/` : frames_par_bloc, vue_ensemble, stance_mensuel, event_impact_diff_in_diff, emotional_register
- [ ] `config/twitter_sources/` contient les sources pour merge_twitter_sources.py
- [ ] `site/index.html` charge `data/*.csv` (chemins relatifs dans site/)

## 3. Chaîne

- [ ] `pipeline/collection/` → `pipeline/annotation/` → `publication/` → `analysis/`
- [ ] README à jour
