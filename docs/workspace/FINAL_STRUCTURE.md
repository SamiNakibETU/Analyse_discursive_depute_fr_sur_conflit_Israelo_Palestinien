# Structure finale du workspace

**Post-cleanup** — arborescence canonique

---

## Vue d'ensemble

```
Revirement_politique_fr_gaza/
├── analysis/                  # Moteur analytique canonique (ex analyse_discursive_depute)
│   ├── scripts/run_analysis.py
│   ├── src/config.py
│   ├── notebooks/
│   └── data/results/
├── publication/                # Couche publication (ex fr_assemblee_discourse_analysis)
│   ├── src/prepare_data.py
│   ├── src/build_analyses_extended.py
│   └── data/results/
├── pipeline/
│   ├── collection/            # Collecte AN + Twitter (ex final)
│   │   ├── data/
│   │   ├── config/
│   │   └── scripts_scraîng/
│   └── annotation/            # Consolidation, annotation (ex projet_gaza)
│       ├── src/preprocessing/
│       └── data/
├── site/                      # Dataviz éditoriale
│   ├── index.html
│   ├── scripts/
│   ├── styles/
│   └── data/                  # 5 CSV (frames_par_bloc, vue_ensemble, etc.)
├── config/
├── docs/
├── archive/
├── reports/
├── figures/
├── index.html                 # Redirection vers site/index.html
├── README.md
├── AGENTS.md
├── DESIGN_SYSTEM.md
├── PUSH_CHECKLIST.md
├── package.json
└── requirements.txt
```

---

## Rôles par dossier

| Dossier | Rôle |
|---------|------|
| `analysis/` | **Repo analytique canonique** — run_analysis, notebooks, CSV results |
| `publication/` | **Couche publication** — prepare_data, exports complémentaires |
| `pipeline/collection/` | **Collecte** — AN, scraping Twitter, merge sources |
| `pipeline/annotation/` | **Annotation** — consolidation, filtrage, annotation LLM |
| `site/` | **Dataviz éditoriale** — index.html, scripts D3, 5 CSV |
| `archive/` | Hors flux, reliquats, debug |
| `config/` | Configurations partagées (twitter_sources, etc.) |

---

## Chaîne de données

```
pipeline/collection/  →  pipeline/annotation/  →  publication/prepare_data  →  analysis/run_analysis
                                                                                    ↓
                                                                            site/data/*.csv
```
