# Revirement politique français — Conflit israélo-palestinien

Analyse des prises de position des députés français (tweets + Assemblée nationale), 2023–2026.

## Structure (post-cleanup)

| Dossier | Rôle |
|---------|------|
| `site/` | Dataviz éditoriale (5 planches D3) |
| `analysis/` | Moteur analytique canonique |
| `publication/` | Couche publication (prepare_data, exports) |
| `pipeline/collection/` | Collecte AN + scraping Twitter |
| `pipeline/annotation/` | Consolidation et annotation LLM |
| `archive/` | Hors flux principal |

## Chaîne

`pipeline/collection/` → `pipeline/annotation/` → `publication/prepare_data` → `analysis/run_analysis` → `site/data/*.csv`

## Par où commencer

| Objectif | Fichier |
|----------|---------|
| Guide de démarrage | [docs/workspace/QUICKSTART.md](docs/workspace/QUICKSTART.md) |
| Manifeste des artefacts | [docs/workspace/CANONICAL_ARTIFACTS.md](docs/workspace/CANONICAL_ARTIFACTS.md) |
| Traçabilité pipeline | [docs/traceability/PIPELINE_TRACEABILITY.md](docs/traceability/PIPELINE_TRACEABILITY.md) |
| Résultats canoniques | `analysis/data/results/` |
| Rapport exhaustif | `publication/docs/COMPTE_RENDU_RESULTATS.md` |
| Dataviz | Ouvrir `site/index.html` (ou `index.html` racine) |

## Docs

- **Workspace** : `docs/workspace/` (audit, structure, migration)
- **Traçabilité** : `docs/traceability/`
- **Migration** : `docs/migration/`
- **Design** : `DESIGN_SYSTEM.md`, `docs/design/`

Avant push : `PUSH_CHECKLIST.md`
