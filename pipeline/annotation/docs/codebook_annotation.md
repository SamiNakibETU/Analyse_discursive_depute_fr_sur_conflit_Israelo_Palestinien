# 📘 Codebook d'Annotation - Stance Detection Gaza/Palestine

## 1. Objectif

Ce document définit les règles d'annotation pour classifier le positionnement (stance) des députés français sur le conflit Gaza/Palestine.

## 2. Schéma d'annotation

### 2.1 Variable principale : STANCE

| Code | Label | Description |
|------|-------|-------------|
| **1** | Pro-Palestine | Critique explicite d'Israël, soutien à la cause palestinienne |
| **0** | Neutre/Équilibré | Position équidistante, appel à la paix sans blâme clair |
| **-1** | Pro-Israël | Soutien explicite à Israël, critique du Hamas/Palestine |
| **NA** | Hors-sujet | Le texte ne concerne pas le conflit (faux positif du filtre) |

### 2.2 Variables secondaires

| Variable | Valeurs | Description |
|----------|---------|-------------|
| `intensity` | 1-3 | Intensité du positionnement (1=modéré, 3=fort) |
| `target` | Israel, Palestine, Hamas, Civils, France, Autre | Cible principale du discours |
| `frame` | Voir §3 | Cadrage dominant |
| `call_to_action` | 0/1 | Présence d'un appel à l'action concret |

## 3. Frames (cadrages)

| Code | Frame | Exemples de formulations |
|------|-------|--------------------------|
| `HUM` | Humanitaire | "catastrophe humanitaire", "civils innocents", "famine" |
| `SEC` | Sécuritaire | "terrorisme", "droit de se défendre", "otages" |
| `LEG` | Juridique | "droit international", "CIJ", "crimes de guerre" |
| `HIS` | Historique | "occupation depuis 1967", "Nakba", "colonisation" |
| `DIP` | Diplomatique | "solution à deux États", "reconnaissance", "négociations" |
| `MOR` | Moral | "génocide", "apartheid", "barbarie", "massacre" |

## 4. Règles de décision

### 4.1 Classification STANCE

```
SI critique explicite d'Israël/Netanyahu/Tsahal 
   ET/OU soutien explicite Palestine/Gaza/civils palestiniens
   ET/OU utilisation de "génocide", "apartheid", "nettoyage ethnique"
   → STANCE = 1 (Pro-Palestine)

SI soutien explicite à Israël
   ET/OU critique explicite Hamas/terrorisme palestinien
   ET/OU mention "droit de se défendre" sans critique
   ET/OU focalisation sur les otages/victimes israéliennes
   → STANCE = -1 (Pro-Israël)

SI appel au cessez-le-feu/paix sans blâme
   ET/OU mention symétrique des victimes des deux côtés
   ET/OU position institutionnelle neutre
   → STANCE = 0 (Neutre)

SI le texte ne concerne pas réellement le conflit
   (ex: utilisation métaphorique, sujet connexe)
   → STANCE = NA (Hors-sujet)
```

### 4.2 Cas ambigus

| Situation | Décision |
|-----------|----------|
| Critique du Hamas ET d'Israël | Regarder la balance : quelle critique est plus développée ? |
| "Condamnation du terrorisme du 7 octobre" seul | Pro-Israël (-1) sauf si suivi de critique d'Israël |
| "Cessez-le-feu immédiat" seul | Neutre (0) - position humanitaire non-alignée |
| Citation d'un tiers sans commentaire | NA si simple relais, sinon selon le commentaire |
| Retweet sans commentaire | Annoter selon le contenu retweeté |

### 4.3 Intensité

| Niveau | Critères |
|--------|----------|
| 1 (Modéré) | Formulation diplomatique, nuancée, institutionnelle |
| 2 (Marqué) | Position claire mais sans termes extrêmes |
| 3 (Fort) | Termes forts ("génocide", "barbarie", "terroristes"), émotion, majuscules |

## 5. Exemples annotés

### Exemple 1 : Pro-Palestine (1), Intensité 3

> "Le gouvernement Netanyahu commet un génocide à Gaza sous nos yeux. La France doit reconnaître l'État palestinien immédiatement et suspendre les ventes d'armes."

- **STANCE** : 1 (Pro-Palestine)
- **Intensité** : 3 (terme "génocide", appel à l'action fort)
- **Target** : Israel
- **Frame** : MOR + DIP
- **call_to_action** : 1

### Exemple 2 : Pro-Israël (-1), Intensité 2

> "Je réaffirme le soutien de la France à Israël face au terrorisme du Hamas. Les otages doivent être libérés immédiatement."

- **STANCE** : -1 (Pro-Israël)
- **Intensité** : 2 (position claire, pas de termes extrêmes)
- **Target** : Israel, Hamas
- **Frame** : SEC
- **call_to_action** : 1

### Exemple 3 : Neutre (0), Intensité 1

> "La France appelle à une solution politique et à la reprise du dialogue en vue d'une paix juste et durable au Proche-Orient."

- **STANCE** : 0 (Neutre)
- **Intensité** : 1 (formulation diplomatique standard)
- **Target** : Autre (processus de paix)
- **Frame** : DIP
- **call_to_action** : 0

### Exemple 4 : Hors-sujet (NA)

> "Le conflit entre la majorité et l'opposition sur le budget est une véritable guerre de tranchées."

- **STANCE** : NA (métaphore, pas le conflit Gaza)

## 6. Procédure d'annotation

### 6.1 Phase pilote
1. 2-3 annotateurs annotent 50 exemples communs
2. Calcul du Kappa de Cohen
3. Discussion des désaccords
4. Ajustement du codebook si nécessaire
5. Objectif : Kappa > 0.7

### 6.2 Phase production
1. Chaque texte annoté par 1 annotateur principal
2. 20% en double annotation pour contrôle qualité
3. Résolution des désaccords par 3e annotateur

### 6.3 Format de sortie

```json
{
  "id": "tweet_12345",
  "text": "...",
  "stance": 1,
  "intensity": 2,
  "target": "Israel",
  "frames": ["HUM", "LEG"],
  "call_to_action": 1,
  "annotator": "A1",
  "confidence": "high",
  "notes": ""
}
```

## 7. Calcul de l'accord inter-annotateurs

```python
from sklearn.metrics import cohen_kappa_score
import krippendorff

# Cohen's Kappa (2 annotateurs)
kappa = cohen_kappa_score(annotations_A, annotations_B)

# Krippendorff's Alpha (>2 annotateurs, données manquantes possibles)
alpha = krippendorff.alpha(reliability_data, level_of_measurement='ordinal')

# Seuils acceptables
# Kappa/Alpha > 0.8 : Excellent
# 0.6-0.8 : Bon
# 0.4-0.6 : Modéré (nécessite révision du codebook)
# < 0.4 : Insuffisant
```

## 8. Changelog

| Version | Date | Modifications |
|---------|------|---------------|
| 1.0 | 2026-01-08 | Création initiale |


