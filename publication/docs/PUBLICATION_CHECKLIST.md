# Checklist publication - Repo GitHub

**Projet** : Analyse discursive Assemblée nationale  
**Repo** : [SamiNakibETU/Analyse-discursive-sur-le-conflit-Israelo-Palestinien](https://github.com/SamiNakibETU/Analyse-discursive-sur-le-conflit-Israelo-Palestinien)

---

## Avant le push

- [ ] `make figures` ou `make analyses` exécuté (génère fig21-25)
- [ ] `make notebooks` exécuté si corpus disponible (génère fig04, fig11, fig12, fig17)
- [ ] Les figures dans `reports/figures/` sont commitées (ou le README affiche des liens cassés jusqu'au premier run)
- [ ] `git status` : aucun fichier sensible (data/raw, data/processed/*.parquet exclus par .gitignore)

---

## Sur GitHub (Settings → General → About)

- [ ] **Description** : "Analyse computationnelle du discours de 459 députés français sur le conflit israélo-palestinien (oct. 2023 - jan. 2026). 10 774 textes annotés par LLM, science politique computationnelle."
- [ ] **Topics** : `nlp`, `computational-social-science`, `political-discourse`, `french-politics`, `text-analysis`, `llm-annotation`, `stance-detection`, `discourse-analysis`

---

## Push (terminal, sans Cursor Agent)

```bash
cd d:\Users\Proprietaire\Desktop\Projet_perso\Projets\Revirement_politique_fr_gaza\fr_assemblee_discourse_analysis

git add .
git status
git commit -m "final: publication-ready repo"
git push origin main
```

Voir [PUSH_GIT.md](PUSH_GIT.md) pour le détail.

---

## Contenu livré

| Élément | Statut |
|--------|--------|
| README avec figures | ✓ |
| CODEBOOK.md | ✓ |
| METHODOLOGIE.md | ✓ |
| RAPPORT_VALIDATION_AGENT.md | ✓ |
| COMPTE_RENDU_RESULTATS.md | ✓ |
| 4 notebooks (01 à 04) | ✓ |
| Régression bloc×batch + ANOVA + forest plot | ✓ |
| Analyses fig21-25 (Twitter vs AN, attrition, RN vs LR, fighting words, Droite CF) | ✓ |
| Pipeline ML (embeddings, validation) | ✓ |

---

*Dernière mise à jour : février 2026*
