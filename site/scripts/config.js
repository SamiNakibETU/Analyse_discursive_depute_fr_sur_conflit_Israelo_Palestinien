// ═══════════════════════════════════════════════════════════════════
// config.js — Source unique de vérité pour toutes les planches
// Aucune valeur magique ne doit apparaître dans les fichiers de charts.
// ═══════════════════════════════════════════════════════════════════

export const CFG = {

  // ─── GRILLE (px, référence 1440px desktop) ──────────────────────
  PAGE_W:    1440,
  CONTENT_W: 1040,
  MARGIN_L:   180,
  MARGIN_R:   220,
  RAIL_W:      72,   // rail gauche (codes, kickers)
  GUTTER:      24,   // gouttière interne

  // ─── RYTHME VERTICAL ────────────────────────────────────────────
  RHY: {
    codeToTitle:     12,
    titleToTech:     10,
    techToChart:     22,
    chartToFoot:     14,
    betweenPlanches: 96,
  },

  // ─── PALETTE ────────────────────────────────────────────────────
  COL: {
    bg:        '#F1EFEA',   // fond général — papier chaud
    ink:       '#111111',   // noir texte
    struct:    '#908A80',   // gris structure (labels techniques, unités)
    rule:      '#D8D1C7',   // filet léger
    ruleHeavy: '#6A6460',   // filet moyen

    // Blocs parlementaires — couleurs catégorielles stables
    bloc: {
      'G.RAD': '#6A46A6',
      'G.MOD': '#4C79C2',
      'CTR':   '#B8842F',
      'DRT':   '#B1453D',
    },

    // Frames discursifs — désaturés, imprimables, pas flashy
    frame: {
      HUM: '#2A5C8A',
      SEC: '#9B3030',
      MOR: '#6B6B55',
      LEG: '#3D5A3E',
      DIP: '#5A4A6B',
      OTH: '#908A80',
    },

    onDark:  '#ffffff',
    dimText: '#A09890',
    cross:   '#C0BAB4',   // couleur du × non-significatif
  },

  // ─── TYPOGRAPHIE ────────────────────────────────────────────────
  FONT: {
    title: "'IBM Plex Sans Condensed', sans-serif",
    body:  "'IBM Plex Sans', sans-serif",
    mono:  "'IBM Plex Mono', monospace",
  },

  // ─── ÉPAISSEURS DE TRAITS ───────────────────────────────────────
  STK: {
    heavy:  1.5,
    med:    0.8,
    light:  0.5,
    ghost:  0.25,
  },

  // ─── DIMENSIONS SVG (coordonnées internes des charts) ───────────
  CW:  860,   // largeur du viewBox de tous les charts
  LBL:  76,   // largeur colonne étiquettes dans les charts

  // ─── DONNÉES STABLES ────────────────────────────────────────────
  BLOCS: ['G.RAD', 'G.MOD', 'CTR', 'DRT'],

  // Correspondance clé CSV → label d'affichage
  CSV_BLOC_MAP: { GRAD: 'G.RAD', GMOD: 'G.MOD', CTR: 'CTR', DRT: 'DRT' },

  FRAMES: ['HUM', 'SEC', 'MOR', 'LEG', 'DIP', 'OTH'],
  FRAME_LABELS: {
    HUM: 'Humanitaire',
    SEC: 'Sécuritaire',
    MOR: 'Moral',
    LEG: 'Légal',
    DIP: 'Diplomatique',
    OTH: 'Autre',
  },

  // ─── FORMATEURS NUMÉRIQUES ──────────────────────────────────────
  FMT: {
    pct:    v => Math.round(+v) + '%',
    pct1:   v => (+v).toFixed(1) + '%',
    val1:   v => (+v).toFixed(1),
    val2:   v => (+v).toFixed(2),
    // Signe typographique (+ ou − unicode, pas tiret)
    sign2:  v => {
      const n = +v;
      const abs = Math.abs(n).toFixed(2);
      if (n > 0)  return '+' + abs;
      if (n < 0)  return '\u2212' + abs;
      return abs;
    },
  },
};
