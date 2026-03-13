# Editorial Dataviz Design System
## Style Groot­ens — Swiss / Dutch Graphic Standards

Version 1.0 · mars 2026

---

## 0. Principe fondateur

> **La figure est la page. Rien ne la comprime.**

Ce système s'applique à toute publication de dataviz éditoriale qui refuse le dashboard, le rapport de consulting et l'interface SaaS. Il s'inscrit dans la tradition de la publication imprimée néerlandaise et du graphisme suisse : rigueur structurelle, économie de moyens, autorité typographique.

Ce n'est pas un style décoratif. C'est une **méthode**.

**Références de studio** : Joost Grootens (Port City Atlas, Vinex Atlas, Metropolitan World Atlas), Catalogtree, Clever°Franke, Index Ventures.

---

## 1. Ce que ce système est. Ce qu'il n'est pas.

| ✓ Est | ✗ N'est pas |
|---|---|
| Publication feuilletable, planche par planche | Dashboard interactif |
| Objet éditorial qui se lit comme un livre | Rapport de consultant |
| Dataviz avec autorité graphique | Interface SaaS ou BI |
| Fond blanc pur, économie de couleur | Fond gris, cartes flottantes |
| Typographie décidée, signée | Fontes par défaut système |
| Annotation humaine | Exécution mécanique |
| Tension visuelle, hiérarchie tranchée | Tout au même niveau |

---

## 2. Palette

### Tokens structurels (invariants)

| Token    | Hex       | Rôle                                               |
|----------|-----------|----------------------------------------------------|
| `ink`    | `#111111` | Texte, lignes, formes structurelles                |
| `bg`     | `#FFFFFF` | Fond. Toujours blanc pur. Jamais gris, jamais crème |
| `rule`   | `#D4D0CA` | Filets, hachures, séparateurs de grille            |
| `mute`   | `#888888` | Métadonnées, sources, annotations secondaires      |
| `accent` | `[choix]` | Une seule couleur d'accent. Rouge Grootens : `#E8413C` |

### Couleurs d'accent — règles

- **Une seule couleur d'accent par publication.** Pas deux, pas trois.
- L'accent est réservé aux **données actives** et aux **codes de section**. Pas à la décoration.
- Les fills de fond (areas, bandes) sont toujours en **très faible opacité** (0.05–0.20). Jamais opaques.
- Si la donnée appelle deux pôles (positif/négatif, A/B), utiliser : `accent` + `ink`. Pas deux teintes d'accent.

### Palette ordonnée pour les catégories

Quand un graphique nécessite N catégories, ne pas choisir N couleurs distinctes. Construire un **dégradé monochrome** de l'accent vers le gris neutre :

```
Catégorie 1 (principale) → accent     (#E8413C)
Catégorie 2              → ink foncé   (#222)
Catégorie 3              → mute        (#888)
Catégorie 4              → gris clair  (#AAA)
Catégorie 5              → gris très clair (#CCC)
Catégorie 6+             → beige neutre (#E5E2DD)
```

**Règle** : le rouge est réservé à ce qui est le plus important analytiquement. Le gris = résiduel.

---

## 3. Typographie

### Système à 3 fontes

| Fonte              | Rôle                              | Raison du choix |
|--------------------|-----------------------------------|-----------------|
| **Barlow Condensed** | Structure, codes, titres, labels | Condensed = maximise l'info par ligne. Autorité sans arrogance. |
| **Barlow**         | Corps, descriptions, légendes      | Cohérence avec le condensed. Lisibilité texte courant. |
| **Courier Prime**  | Valeurs numériques, données brutes | Connotation journalistique/verbatim. Chasse fixe = alignement naturel. |

### Échelle typographique

| Rôle                 | Fonte              | Graisse | Taille    | Tracking     |
|----------------------|--------------------|---------|-----------|--------------|
| Titre principal      | Barlow Condensed   | 700     | 42–52px   | −0.02em      |
| Titre de planche     | Barlow Condensed   | 700     | 26–32px   | −0.015em     |
| Numéro de section    | Barlow Condensed   | 700     | 11px      | +0.10em      |
| Label de catégorie   | Barlow Condensed   | 700     | 11–13px   | +0.06em      |
| Section uppercase    | Barlow             | 500     | 7.5px     | +0.20em      |
| Description méthode  | Barlow             | 400     | 10px      | +0.01em      |
| Corps courant        | Barlow             | 400     | 12–14px   | 0            |
| Valeur principale    | Courier Prime      | 700     | 12–14px   | 0            |
| Valeur secondaire    | Courier Prime      | 400     | 8–10px    | 0            |
| Métadonnée / source  | Barlow italic      | 400     | 7–7.5px   | +0.03em      |
| Note technique       | Courier Prime      | 400     | 7px       | 0            |

### Interdits typographiques

- ❌ IBM Plex Mono — connotation "outil développeur"
- ❌ Inter, Roboto, Space Grotesk — connotation "template IA"
- ❌ Serif pour les données (illisible à petite taille)
- ❌ Tirets cadratin `—` dans les titres analytiques
- ❌ Majuscules décoratives sans raison structurelle
- ❌ Line-height > 1.6 dans les graphiques

---

## 4. Grille et espacement

### Mise en page

```
Largeur max du contenu : 880px (ajustable à 960px max)
Padding vertical haut  : 120–140px
Padding vertical bas   : 160–200px
Espacement inter-planche : 160–180px
```

### Structure d'une planche

Chaque figure est un module autonome. Ordre strict, inviolable :

```
┌──────────────────────────────────────────────────────────┐
│  [NUM] (accent)              [SECTION] (mute, uppercase)  │
├──────────────────────────────────────────────────────────┤
│  Titre analytique assertif — Barlow Condensed 700 28px   │
│  Description méthode lisible — Barlow 400 10px mute      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│         GRAPHIQUE SVG — pleine largeur                   │
│         La figure occupe tout l'espace disponible        │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  source.csv (italic mute)         Note méthodologique    │
└──────────────────────────────────────────────────────────┘
```

Espacements internes :
- Numéro/section → titre : 8px
- Titre → description méthode : 5px
- Description méthode → graphique : 36px
- Graphique → footer : 20px

---

## 5. Éléments graphiques

### 5.1 Hiérarchie des lignes

| Type                    | Épaisseur | Couleur  | Style         |
|-------------------------|-----------|----------|---------------|
| Séparateur principal    | 0.5px     | `ink`    | Solide        |
| Séparateur de grille    | 0.3–0.5px | `rule`   | Solide        |
| Référence / échelle     | 0.3px     | `rule`   | Dash `2,4`    |
| Tendance / moyenne      | 0.4px     | `mute`   | Dash `1,3`    |
| Axe zéro                | 0.3px     | `ink`    | Solide        |
| Tick d'axe              | 0.5px     | `mute`   | Solide, 4px   |
| Séparateur de colonne   | 0.5px     | `rule`   | Solide        |

**Règle** : jamais plus de 3 épaisseurs de trait dans un même graphique.

### 5.2 Barres

- Pas de `border-radius`. Jamais.
- Pas de séparation entre segments d'une barre empilée.
- La hauteur d'une barre horizontale : 8–34px selon densité.
- Pour signifier une hiérarchie (dominant / secondaire) : `opacity 1.0` vs `opacity 0.35`. Pas deux couleurs différentes.

### 5.3 Cercles proportionnels

- Scaling : `r = R_MAX × √(valeur / max)`. Toujours en racine carrée (surface proportionnelle à la valeur).
- Cercle de référence (max) en fond beige `#F5F0EB` — méthode Grootens.
- Rayon max typique : 22–28px.
- Couleur : `accent` (rouge). Jamais de cercle de couleur arbitraire.

### 5.4 Areas (graphiques temporels)

- Fill pôle positif : `accent`, opacity 0.06–0.10
- Fill pôle négatif : `ink`, opacity 0.04–0.08
- Les areas ne doivent jamais dominer — la **ligne** prime.
- Bandes d'événements : fill `yellow` #F5D54F, opacity 0.12–0.18, largeur 12–20px

### 5.5 Hachures

- Pattern SVG à 45°, espacement 5px, stroke `rule` 0.6px
- Usage exclusif : données non-significatives ou données manquantes dans une matrice
- Jamais décoratif

### 5.6 Marqueurs d'absence

- Caractère `×` (U+00D7), pas `x`, pas `–`
- Taille 12–13px, couleur `rule`
- Accompagné du mot "absent" (7px, `mute`) si l'espace le permet

### 5.7 Flèches directionnelles

- `▲` (U+25B2) pour une valeur positive / hausse
- `▼` (U+25BC) pour une valeur négative / baisse
- Taille 6–8px. Couleur identique à la barre.
- Positionnées à l'extrémité de la barre, jamais à côté du label

---

## 6. Niveaux de lecture

Toute figure doit être lisible à **3 distances** :

| Distance | Ce que l'œil capte | Élément responsable |
|----------|--------------------|---------------------|
| Vue d'ensemble (3m) | La forme générale, la hiérarchie | Structure SVG, zones de couleur |
| Lecture (50cm) | Les tendances, les catégories | Titres, labels de blocs, lignes |
| Étude (20cm) | Les valeurs, la méthode, les détails | Annotations Courier Prime, footer |

### Annotations obligatoires par type de graphique

| Type | Annotation minimum |
|---|---|
| Barres empilées | % sur tout segment ≥ 8px de large, dominant signalé à droite |
| Cercles proportionnels | Valeur numérique à gauche du cercle, multiplicateur ×N pour comparaison |
| Série temporelle | Valeur de début (gris), valeur de fin (noir gras), extremums (points colorés + valeur) |
| Matrice | Valeur dans chaque cellule, significativité (* / **), date de l'événement |
| Barres horizontales | Valeur à droite de la barre, label "dominant" pour la valeur max par ligne |

---

## 7. Pictogrammes

### Philosophie

Les pictogrammes signalent le **type de donnée ou de figure**, pas le sujet. Ils doivent être compris en 0.5 seconde. Ils appartiennent à la figure, pas à l'interface.

Référence : silhouettes de bateaux, avions, bâtiments dans Port City Atlas. Signalétique suisse Aicher/Frutiger.

### Spécifications formelles

```
Grille              : 14 × 14 unités (viewBox 0 0 14 14)
Taille d'affichage  : 12–16px
Trait               : 1.2px
stroke-linecap      : round
stroke-linejoin     : round
fill                : none (sauf points/solides intentionnels)
Couleur             : ink (#111) ou mute (#888)
Couleur interdite   : accent — le rouge est réservé aux données
```

### Règles de construction

1. **Le minimum de traits pour le maximum de clarté.** Si un trait peut être supprimé sans perte de sens, le supprimer.
2. **Géométrique strict.** Angles à 90° ou 45°. Courbes seulement si indispensables (ex : visage, globe).
3. **Poids optique homogène.** À 14px, tous les pictogrammes doivent avoir la même densité visuelle.
4. **Cohérence de style absolue.** Si l'un est angulaire, tous le sont.
5. **Pas de fill massif.** Un bloc noir n'est pas un pictogramme, c'est un carré.

### Catalogue de formes acceptables

| Concept          | Forme | Exemples de traits |
|------------------|-------|--------------------|
| Document / texte | Rectangle avec lignes horizontales | `rect` + 2–3 `line` |
| Message / tweet  | Bulle de dialogue avec queue | `path` ou `rect` + triangle |
| Temps / trajectoire | Ligne brisée avec 1–2 points | `polyline` + `circle` |
| Choc / impact    | Éclair (polygone anguleux) | `path` en zigzag |
| Émotion / humain | Cercle + 2 points + courbe | `circle` + `line` + arc |
| Matrice / grille | 3×3 carrés avec un rempli | 9× `rect` |
| Comparaison      | Deux formes de tailles différentes | 2× même forme |
| Localisation     | Épingle ou point d'ancrage | `circle` + `line` verticale |

---

## 8. Règles éditoriales

### Titres de planches

Le titre dit **ce que la données prouve**, pas ce qu'elle montre.

| ❌ Descriptif (à éviter) | ✓ Analytique (à viser) |
|--------------------------|------------------------|
| Distribution des cadres discursifs | La gauche parle souffrance. La droite parle sécurité. |
| Évolution temporelle du score | Les positions sont figées. Seul le Centre hésite. |
| Comparaison des volumes | G.RAD monopolise le sujet : 4× plus de textes |

### Descriptions techniques

- Formuler comme une **clé de lecture**, pas comme une définition.
- Exemple : "Chaque barre = 100 % du corpus d'un bloc · lecture : G.RAD consacre 77 % au cadre humanitaire, contre 11 % pour DRT"
- Pas de jargon sans explication immédiate dans la même phrase.

### Labels et identifiants

- Tout code court (G.RAD, E1, CTR) doit être accompagné de son **nom complet** au moins une fois dans la figure.
- Les événements portent toujours : code + nom complet + date (ex : E1 · Ordonnance CIJ · 26 jan. 2024).

### Données absentes ou non-significatives

- Donnée absente → `×` + "absent" (jamais un blanc vide non expliqué)
- Effet non-significatif → hachures + valeur en gris `rule` (jamais supprimé)
- Toujours montrer ce qui n'est pas là : l'absence est une information.

### Légendes

- **Intégrées au graphique**, positionnées à proximité de ce qu'elles décrivent.
- Jamais de légende flottante séparée du graphique.
- La légende globale (bandeau de codage) est définie **une seule fois** en haut de publication. Elle n'est pas répétée.

---

## 9. Ce qu'on ne fait jamais

| Interdit | Raison |
|----------|--------|
| Fond gris ou crème | Tue le blanc comme espace actif |
| Cards / panneaux | Fragmente la lecture, crée du bruit |
| KPI flottants | Dashboard, pas publication |
| Légende séparée du graphique | Force un aller-retour oculaire inutile |
| Arc-en-ciel de couleurs | Pas de sens sémantique, visuellement fatigant |
| Border-radius sur les barres | Connotation UI/app |
| Drop shadows | Connotation SaaS/BI |
| Animations CSS sur les données | Distraction, pas d'analyse |
| Titres descriptifs neutres | Perte d'autorité éditoriale |
| Polices par défaut (Inter, Roboto) | Connotation "généré par IA" |
| Emoji ou icônes Material | Rupture de registre graphique |

---

## 10. Tokens de référence (implémentation HTML/SVG)

```css
/* CSS Variables */
:root {
  --ink:    #111111;
  --bg:     #FFFFFF;
  --rule:   #D4D0CA;
  --mute:   #888888;
  --accent: #E8413C;  /* adapter par projet */
}
```

```javascript
/* D3.js / SVG — objet C (Color + Config) */
const C = {
  ink:    '#111',
  bg:     '#fff',
  rule:   '#D4D0CA',
  mute:   '#888',
  accent: '#E8413C',   // adapter par projet
  fill1:  '#F2B5B0',   // fill léger pôle A (opacity <0.15)
  fill2:  '#F5D54F',   // fill léger événements / marqueurs
  ref:    '#F5F0EB',   // fond cercle de référence

  fc: '"Barlow Condensed", sans-serif',
  fb: '"Barlow", sans-serif',
  fd: '"Courier Prime", monospace',

  W: 880              // largeur SVG (adapter au conteneur)
};

/* Fonctions utilitaires SVG standardisées */
// hr(svg, x1, x2, y, weight, color)  → ligne horizontale
// vr(svg, x, y1, y2, color)          → ligne verticale
// label(svg, x, y, text, opts)       → texte Barlow
// val(svg, x, y, text, opts)         → texte Courier Prime
// picto(svg, x, y, type, size, col)  → pictogramme
// mkSVG(id, W, H)                    → SVG D3 avec pattern hachures
```

---

## 11. Checklist avant livraison

Avant de finaliser une planche :

- [ ] Le titre dit quelque chose, il ne décrit pas
- [ ] La description technique donne une clé de lecture
- [ ] Chaque code est accompagné de son nom complet au moins une fois
- [ ] Les données absentes sont signalées (×, hachures, gris)
- [ ] La légende est intégrée au graphique, pas séparée
- [ ] Les valeurs sont lisibles à 3 distances
- [ ] Pas de border-radius sur les barres
- [ ] Pas de drop shadow
- [ ] Pas plus de 3 épaisseurs de trait dans un graphique
- [ ] Le fond est blanc pur (#FFF)
- [ ] La couleur d'accent est utilisée une seule fois (pas deux)
- [ ] Les pictogrammes ont le même poids optique
