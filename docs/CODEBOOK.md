# Codebook — Variables du corpus

## Colonnes principales

| Variable | Type | Description |
|----------|------|-------------|
| `author` | str | Nom du député (unifié Twitter/AN) |
| `bloc` | str | Bloc politique (Gauche radicale, Gauche modérée, Centre / Majorité, Droite) |
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
| -2 | Très pro-Israël |
| -1 | Plutôt pro-Israël |
| 0 | Neutre |
| +1 | Plutôt pro-Palestine / cessez-le-feu |
| +2 | Très pro-Palestine |

## Cadres (primary_frame_v3)

| Code | Signification |
|------|---------------|
| HUM | Humanitaire |
| SEC | Sécuritaire |
| LEG | Juridique |
| DIP | Diplomatique |
| MOR | Moral |
| ECO | Économique |
| HIS | Historique |
| POL | Politique |

## Batches

Voir [METHODOLOGIE.md](METHODOLOGIE.md) § 5.

## Variables batch-spécifiques (v4)

| Variable | Type | Description |
|----------|------|-------------|
| `genocide_framing` | bool | Mention du cadrage « génocide » |
| `condemns_hamas_attack` | bool | Condamnation de l'attaque du 7 octobre |
| `state_recognition_mention` | bool | Mention reconnaissance d'État |
| `transpartisan_convergence` | bool | Vocabulaire de convergence |

## Panel B4

76 députés ayant au moins une intervention dans 4 mois distincts sur 18 mois (oct. 2023 – mars 2025). Sous-ensemble utilisé pour les analyses de robustesse.
