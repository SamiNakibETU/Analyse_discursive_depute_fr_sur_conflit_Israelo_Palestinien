# Codebook — Variables du corpus

## Colonnes principales

| Variable | Type | Description |
|----------|------|-------------|
| `author` | str | Nom du député (unifié Twitter/AN) |
| `bloc` | str | Bloc politique (Gauche radicale, Gauche modérée, Centre / Majorité, Droite) |
| `bloc_5` | str | Variante 5 blocs : Droite LR vs Droite RN séparés (NI exclus) |
| `group` | str | Groupe parlementaire (LR, RN, UDR, LFI, etc.) |
| `date` | datetime | Date du texte |
| `text` | str | Texte brut |
| `text_clean` | str | Texte nettoyé (si disponible) |
| `stance_v3` | int | Positionnement -2 à +2 (corpus principal) |
| `stance_v4` | int | Positionnement -2 à +2 (corpus événementiel) |
| `arena` | str | "Twitter" ou "Assemblée nationale" |
| `month` | str | Mois (YYYY-MM) |
| `batch` | str | Fenêtre temporelle (CHOC, POST_CIJ, etc.) |

## Échelle de stance

| Valeur | Interprétation |
|--------|----------------|
| -2 | Très favorable à Israël |
| -1 | Plutôt favorable à Israël |
| 0 | Neutre |
| +1 | Plutôt favorable à la Palestine / cessez-le-feu |
| +2 | Très favorable à la Palestine |

## Cadres (primary_frame_v3)

| Code | Signification | Référence théorique | Exemples de mots typiques | Lien MFD |
|------|---------------|---------------------|---------------------------|----------|
| HUM | Humanitaire | Semetko & Valkenburg (2000), Entman (1993) | victime, humanitaire, civil, souffrance, population | Care |
| SEC | Sécuritaire | Buzan, Wæver & de Wilde (1998) — sécuritisation | menace, sécurité, défense, terrorisme, attaque | — |
| LEG | Juridique | Droit international humanitaire (DIH) | droit, tribunal, crime, convention, violation | Fairness |
| DIP | Diplomatique | Entman (2004) — framing diplomatique | négociation, diplomatie, médiation, accord, relations | — |
| MOR | Moral | Haidt (2012), Moral Foundations Theory | justice, éthique, condamnable, immoral, responsabilité | Care, Fairness, Authority |
| ECO | Économique | Frame économique / sanctions | sanctions, embargo, économie, commerce, aide | — |
| HIS | Historique | Mémoire collective, framing historique | mémoire, histoire, colonisation, passé, origine | — |
| POL | Politique | Politique intérieure française | élection, parti, assemblée, débat, position | Authority |

## Batches

Voir [METHODOLOGIE.md](METHODOLOGIE.md) § 5.

## Variables batch-spécifiques (v4)

| Variable | Type | Description |
|----------|------|-------------|
| `genocide_framing` | bool | Mention du cadrage « génocide » |
| `condemns_hamas_attack` | bool | Condamnation de l'attaque du 7 octobre |
| `state_recognition_mention` | bool | Mention reconnaissance d'État |
| `transpartisan_convergence` | bool | Vocabulaire de convergence |

## Bloc 5 (LR vs RN)

Pour les analyses distinguant LR et RN : `bloc_5` dérive de `group`. Mapping `GROUP_TO_BLOC_5` : LR → Droite LR, RN → Droite RN, UDR → Droite RN, NI → exclu. Voir notebook 12 et [METHODOLOGIE.md](METHODOLOGIE.md) § 4.

## Panel B4

76 députés ayant au moins une intervention dans 4 mois distincts sur 18 mois (oct. 2023 – mars 2025). Sous-ensemble utilisé pour les analyses de robustesse.
