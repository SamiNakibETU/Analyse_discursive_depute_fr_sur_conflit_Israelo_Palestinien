# Prompt — Design de pictogrammes SVG

## Contexte

Tu es un designer graphique spécialisé en infographie éditoriale de style suisse/néerlandais. Tu travailles sur une publication dataviz pour une analyse de l'Assemblée nationale française, dans le style strict de **Joost Grootens** (Port City Atlas, Vinex Atlas, Metropolitan World Atlas).

Le projet utilise un design system minimaliste : fond blanc pur, palette noir/rouge/gris, typographie Barlow Condensed + Courier Prime, grille 880px. Les références visuelles sont transmises en pièces jointes (pages du Port City Atlas de Grootens).

## Ta mission

Dessiner **6 pictogrammes SVG** qui s'intègrent dans ce design system. Chaque pictogramme est un petit symbole fonctionnel placé en marge d'un graphique pour en indiquer la nature — exactement comme Grootens utilise des silhouettes de bateaux, d'avions ou de bâtiments dans ses atlas.

## Contraintes formelles absolues

### Grille
- Chaque pictogramme est dessiné dans une boîte de **14 × 14 unités**
- Le viewBox SVG est `0 0 14 14`
- Taille d'affichage : 14px (parfois 12px)

### Trait
- `stroke-width: 1.2` (jamais plus épais)
- `stroke-linecap: round`
- `stroke-linejoin: round`
- `fill: none` par défaut — le fill ne sert que pour les formes pleines intentionnelles (un point, une flèche pleine)

### Style
- **Géométrique** : lignes droites, arcs réguliers, angles à 90° ou 45°
- **Fonctionnel** : le pictogramme doit être compris en 0.5 seconde
- **Pas de détail superflu** : si un trait ne change pas la compréhension, le supprimer
- **Pas de décoration** : pas d'ombres, pas de dégradés, pas de coins arrondis décoratifs
- **Pas de remplissage massif** : le pictogramme reste aéré, il doit "respirer" dans le blanc de la page

### Couleur
- Mono-couleur : `#111` (noir) ou `#888` (gris) selon le contexte
- Pas de rouge dans les pictogrammes eux-mêmes (le rouge est réservé aux données)

### Cohérence
- Les 6 pictogrammes doivent former une **famille visuelle cohérente** :
  - Même épaisseur de trait
  - Même densité visuelle (pas un très simple à côté d'un très complexe)
  - Même "poids optique" à 14px
  - Si l'un utilise des angles arrondis, tous le font. Si l'un est strict, tous le sont.

## Les 6 pictogrammes à dessiner

### 1. `grid` — Matrice thématique (Chart 01)
**Concept** : grille de carrés, évoquant un tableau croisé ou une classification.
**Inspiration Grootens** : les matrices de données dans Port City Atlas (population structure, distribution built area).
**Placement** : à côté de la légende du chart 01, dans la zone de titre.

### 2. `doc` — Document parlementaire (Chart 02)
**Concept** : page de document avec lignes de texte, coin replié optionnel.
**Inspiration Grootens** : les pictogrammes de cargo/fret dans Port City Atlas — silhouettes simples, reconnaissables.
**Placement** : marge gauche du chart 02, en face de la rangée "Textes par élu".

### 3. `tweet` — Publication / message court (Chart 02)
**Concept** : bulle de message avec lignes, évoquant un tweet ou message social.
**Inspiration Grootens** : même logique que les silhouettes de bateaux — un objet concret réduit à sa forme essentielle.
**Placement** : marge gauche du chart 02, en face de la rangée "Tweets / intervention".

### 4. `timeline` — Trajectoire temporelle (Chart 03)
**Concept** : ligne brisée avec un ou deux points aux inflexions, évoquant un graphique temporel.
**Inspiration Grootens** : les profils topographiques (elevation profiles) dans Port City Atlas — lignes noires sur fond blanc avec points d'intérêt.
**Placement** : coin supérieur gauche du chart 03.

### 5. `impact` — Choc / événement (Chart 04)
**Concept** : éclair ou symbole d'impact, évoquant un choc soudain qui perturbe un système.
**Inspiration Grootens** : les marqueurs d'événements ponctuels dans les timelines — discrets mais sans ambiguïté.
**Placement** : coin supérieur gauche du chart 04.

### 6. `emotion` — Registre émotionnel (Chart 05)
**Concept** : visage schématique ou expression — deux points pour les yeux, une courbe pour la bouche.
**Inspiration Grootens** : les pictogrammes de passagers dans Port City Atlas — silhouettes humaines ultra-simplifiées.
**Placement** : coin supérieur gauche du chart 05.

## Format de livraison attendu

Pour chaque pictogramme, fournir le code SVG inline en `<path>` et/ou `<line>`, `<circle>`, `<polyline>`, `<rect>` — utilisables directement dans D3.js via la fonction suivante :

```javascript
function picto(svg, x, y, type, sz, col) {
  const g = svg.append('g')
    .attr('transform', `translate(${x},${y}) scale(${sz/14})`)
    .attr('fill', 'none')
    .attr('stroke', col || '#111')
    .attr('stroke-width', 1.2)
    .attr('stroke-linecap', 'round')
    .attr('stroke-linejoin', 'round');

  if (type === 'grid') {
    // → tes éléments SVG ici
  }
  // etc.
}
```

## Ce qu'il ne faut PAS faire

- ❌ Pictogrammes trop détaillés (style Noun Project avec 20 traits)
- ❌ Pictogrammes "mignons" ou illustratifs (style app mobile)
- ❌ Fill massif qui crée un bloc noir (sauf si c'est un point intentionnel)
- ❌ Traits de 2px ou plus (trop lourds à 14px)
- ❌ Formes non-géométriques, courbes organiques
- ❌ Incohérence de style entre les 6 (certains ronds, d'autres anguleux)

## Ce qu'il faut viser

- ✓ La rigueur d'un système de signalétique suisse (style Otl Aicher / Adrian Frutiger)
- ✓ La retenue de Grootens : chaque pictogramme est un **outil**, pas une illustration
- ✓ La lisibilité à 14px : le pictogramme doit être lisible sans zoom
- ✓ L'élégance par la contrainte : le moins de traits possible pour le maximum de clarté
