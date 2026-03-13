# Rapport d'exploration - Classification des groupes et impact du panel

**Projet** : fr_assemblee_discourse_analysis - Analyse du discours sur le conflit israélo-palestinien  
**Date** : février 2026

---

## 1. Tableau groupe_politique → bloc (avec effectifs)

### 1.1 Mapping config (`src/config.py`)

| Bloc | Groupes mappés |
|------|----------------|
| **Gauche radicale** | LFI-NFP, LFI, GDR |
| **Gauche modérée** | SOC, PS-NFP, ECO, ECO-NFP |
| **Centre / Majorité** | REN, MODEM, HOR, EPR, DEM |
| **Droite** | LR, RN, UDR, NI |

### 1.2 Valeurs observées dans le corpus v3

Le corpus v3 (post 7 octobre 2023, filtré qualité) contient **16 groupes** distincts, tous correctement mappés vers un bloc :

| groupe_politique | bloc | n_textes | % corpus |
|------------------|------|----------|----------|
| LFI-NFP | Gauche radicale | 5 611 | 52,1 % |
| LFI | Gauche radicale | 832 | 7,7 % |
| GDR | Gauche radicale | 395 | 3,7 % |
| **Sous-total Gauche radicale** | | **6 838** | **63,5 %** |
| PS-NFP | Gauche modérée | 318 | 3,0 % |
| ECO-NFP | Gauche modérée | 483 | 4,5 % |
| SOC | Gauche modérée | 79 | 0,7 % |
| ECO | Gauche modérée | 91 | 0,8 % |
| **Sous-total Gauche modérée** | | **971** | **9,0 %** |
| EPR | Centre / Majorité | 706 | 6,6 % |
| REN | Centre / Majorité | 480 | 4,5 % |
| MODEM | Centre / Majorité | 182 | 1,7 % |
| HOR | Centre / Majorité | 68 | 0,6 % |
| DEM | Centre / Majorité | 53 | 0,5 % |
| **Sous-total Centre / Majorité** | | **1 489** | **13,8 %** |
| RN | Droite | 987 | 9,2 % |
| LR | Droite | 320 | 3,0 % |
| UDR | Droite | 87 | 0,8 % |
| NI | Droite | 82 | 0,8 % |
| **Sous-total Droite** | | **1 476** | **13,7 %** |
| **Total** | | **10 774** | 100 % |

**Aucun groupe UNKNOWN ni non mappé** dans le corpus filtré (les groupes hors mapping sont assignés à « Autre » puis exclus par `mask_bloc` dans `prepare_data.py`).

---

## 2. Comparaison stance : Panel B4 vs corpus complet

Le **Panel B4** regroupe les députés actifs sur **≥ 18 mois** sur la période du corpus. Il comporte **76 députés** et **8 255 textes** (76,6 % du corpus).

### 2.1 Stance moyen par bloc

| Bloc | Corpus complet | Panel B4 | Δ (B4 − complet) | n_complet | n_B4 |
|------|----------------|----------|-----------------|------------|------|
| Gauche radicale | 1,574 | 1,633 | +0,059 | 6 838 | 5 549 |
| Gauche modérée | 0,926 | 0,965 | +0,039 | 971 | 402 |
| Centre / Majorité | -0,769 | **-1,158** | **-0,389** | 1 489 | 475 |
| Droite | -1,378 | -1,543 | -0,165 | 1 476 | 427 |

### 2.2 Interprétation

1. **Centre / Majorité** : la différence est la plus marquée (Δ ≈ -0,39). Le panel B4 est nettement plus « pro-Israël » que le corpus complet, ce qui suggère une **surreprésentation des députés centristes les plus actifs** ayant une position plus alignée sur la majorité.
2. **Droite** : légère accentuation pro-Israël dans le panel (-0,17).
3. **Gauche radicale** et **Gauche modérée** : écarts faibles (+0,06 et +0,04).

### 2.3 Composition du panel B4

| Bloc | n_députés_panel | n_députés_total | % députés | n_textes_panel |
|------|-----------------|-----------------|-----------|----------------|
| Gauche radicale | 42 | 138 | 30,4 % | 6 069 |
| Gauche modérée | 9 | 67 | 13,4 % | 615 |
| Centre / Majorité | 10 | 130 | 7,7 % | 723 |
| Droite | 15 | 124 | 12,1 % | 848 |
| **Total** | **76** | **459** | 16,6 % | **8 255** |

Le panel B4 est très déséquilibré vers la **Gauche radicale** (75 % des textes du panel), alors que celle-ci représente 63,5 % du corpus complet.

---

## 3. Vérification de la classification - sources officielles

### 3.1 Groupes officiels AN (XVIIe législature, post-juillet 2024)

Sources : [assemblee-nationale.fr](https://www2.assemblee-nationale.fr/deputes/liste/groupe-politique), [data.gouv.fr](https://www.data.gouv.fr/datasets/groupes-politiques-actifs-de-lassemblee-nationale-informations-et-statistiques/)

| Dénomination officielle | Abréviation | Correspondance corpus |
|-------------------------|-------------|------------------------|
| Rassemblement National | RN | ✓ RN |
| Ensemble pour la République | EPR | ✓ EPR |
| La France insoumise - NFP | LFI-NFP | ✓ LFI-NFP |
| Socialistes et Apparentés | SOC / PS-NFP | ✓ PS-NFP, SOC |
| Écologiste et Social | ECO-NFP | ✓ ECO-NFP |
| Gauche Démocrate et Républicaine | GDR | ✓ GDR |
| Droite Républicaine (ex-LR) | LR | ✓ LR |
| Horizons & Indépendants | HOR | ✓ HOR |
| Union des Droites pour la République | UDR | ✓ UDR |
| Non inscrits | NI | ✓ NI |
| Libertés, Indépendants, Outre-mer et Territoires | LIOT | ❌ Non présent |
| Les Démocrates | DEM | ✓ DEM |
| Renaissance (ancien) | REN | ✓ REN (XVIe lég.) |

### 3.2 Changements de dénomination documentés

| Période | Changement | Impact sur le corpus |
|---------|------------|----------------------|
| **Juin–juillet 2024** | LFI → **LFI-NFP** (Nouveau Front populaire) | Le corpus contient LFI (avant élections) et LFI-NFP (après). Les deux sont mappés vers « Gauche radicale ». |
| **2024** | Renaissance → **Ensemble pour la République** (EPR) | REN et EPR sont tous deux mappés vers « Centre / Majorité ». |
| **2024** | PS → **PS-NFP** (Socialistes et Apparentés NFP) | SOC et PS-NFP mappés vers « Gauche modérée ». |
| **2024** | Écologistes → **ECO-NFP** | ECO et ECO-NFP mappés vers « Gauche modérée ». |
| **2024** | LR → **Droite Républicaine** | Abréviation LR conservée dans le corpus. |

### 3.3 Écarts et précautions

- **LIOT** : groupe présent à l’AN mais absent du corpus (ou non distingué).
- **Doublons temporels** : LFI vs LFI-NFP, SOC vs PS-NFP, etc. - le mapping par bloc agrège correctement ces variantes.
- **Période de validité** : le corpus couvre octobre 2023–juin 2026, donc **deux législatures** (XVIe partielle, XVIIe). Les regroupements en blocs assurent une cohérence temporelle.

---

## 4. Recommandations pour l’analyse par parti

### 4.1 Seuils n recommandés

| Analyse | Seuil n minimum | Commentaire |
|---------|------------------|-------------|
| Stance moyen par groupe | n ≥ 30 textes | Pour limiter la variance d’échantillonnage |
| Stance par député | n ≥ 10 textes | Pour une estimation individuelle fiable |
| Comparaison inter-groupes | n ≥ 15 par groupe | Pour des tests statistiques pertinents |
| Analyses temporelles (mensuelles) | n ≥ 20 par mois et par bloc | Pour des courbes lissées |

### 4.2 Précautions méthodologiques

1. **Effectifs par groupe** : les petits groupes (SOC 79, ECO 91, HOR 68, DEM 53) ont des intervalles de confiance larges - toujours rapporter n et écarts-types.
2. **Regroupements** : pour des analyses par parti « fin », distinguer LFI vs LFI-NFP selon la date ; pour des analyses par bloc, le regroupement actuel est cohérent.
3. **Période** : indiquer explicitement la plage temporelle et les changements de dénominations (XVIe vs XVIIe législature).
4. **Panel B4** : documenter le biais de sélection - le Centre / Majorité du panel est plus pro-Israël que le Centre / Majorité complet.
5. **Sources de groupe** : les tweets peuvent avoir une attribution de groupe différente des interventions AN (matched_group) ; vérifier la cohérence si on analyse par arène.

### 4.3 Groupes à surveiller

| Groupe | Effectif | Statut |
|--------|----------|--------|
| SOC | 79 | Faible n, possible chevauchement avec PS-NFP |
| ECO | 91 | Faible n |
| HOR | 68 | Faible n |
| DEM | 53 | Très faible n |
| NI | 82 | Hétérogène (députés sans groupe) |

---

## 5. Synthèse

- **Classification** : les 16 groupes du corpus sont correctement mappés vers 4 blocs ; aucun UNKNOWN ni groupe non traité dans le corpus filtré.
- **Sources officielles** : bonne correspondance avec les dénominations AN ; changements LFI→LFI-NFP, REN→EPR, etc. bien gérés via le mapping.
- **Impact du panel B4** : différence marquée pour le Centre / Majorité (Δ ≈ -0,39), à documenter dans les rapports utilisant le panel.
- **Recommandations** : seuils n, précautions temporelles et par groupe, documentation du biais du panel B4.

---

## 6. Fichiers générés

| Fichier | Description |
|---------|-------------|
| `data/results/stance_panel_vs_complet.csv` | Comparaison stance corpus complet vs Panel B4 par bloc |
| `data/results/stance_par_groupe.csv` | Stance moyen par groupe politique (LFI, RN, etc.) |

Pour régénérer ces fichiers avec les données exactes du corpus :
```bash
python src/export_stance_par_groupe.py
```
