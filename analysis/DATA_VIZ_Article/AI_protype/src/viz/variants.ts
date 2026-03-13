/**
 * Palettes et paramètres par variante — Figure 1
 * Chaque variante a une direction graphique distincte.
 */

export type VariantId = 'A' | 'B' | 'C';

/** Variant A — Duo intégré : bichromie stricte, champ unique, marge intégrée */
export const VARIANT_A = {
  id: 'A' as const,
  name: 'Duo intégré',
  frames: {
    HUM: '#1a1a18',
    SEC: '#3a3a38',
    MOR: '#5a5a58',
    OTH: '#8a8a86',
  },
  lexical: {
    gauche: '#1a1a18',
    droite: '#2c4a6a',
  },
  panelBg: '#fafaf8',
  gridStroke: '#e8e7e4',
  axisStroke: '#8a8984',
  ink: '#1a1a18',
  inkMuted: '#5a5954',
  marginBg: '#f4f3f0',
  /** Largeur viz, marge analytique */
  vizWidth: 520,
  marginWidth: 140,
  barHeight: 18,
  barGap: 4,
  labelWidth: 108,
  titleSize: 24,
  captionSize: 9,
} as const;

/** Variant B — Séparation assumée : deux couleurs distinctes, rupture nette */
export const VARIANT_B = {
  id: 'B' as const,
  name: 'Séparation',
  frames: {
    HUM: '#1a1a18',
    SEC: '#40403e',
    MOR: '#6a6a68',
    OTH: '#90908e',
  },
  lexical: {
    gauche: '#5c2424',
    droite: '#1a3250',
  },
  panelBg: '#ffffff',
  gridStroke: '#eae9e6',
  axisStroke: '#7a7974',
  ink: '#1a1a18',
  inkMuted: '#545350',
  dividerStroke: '#1a1a18',
  barHeight: 20,
  barGap: 5,
  labelWidth: 116,
  titleSize: 26,
  captionSize: 9,
} as const;

/** Variant C — Condensation formelle : gamme chaude, dense */
export const VARIANT_C = {
  id: 'C' as const,
  name: 'Condensation',
  frames: {
    HUM: '#282624',
    SEC: '#4c4a48',
    MOR: '#6c6a68',
    OTH: '#8c8a86',
  },
  lexical: {
    gauche: '#282624',
    droite: '#7a4232',
  },
  panelBg: '#f6f5f2',
  gridStroke: '#e4e3df',
  axisStroke: '#7a7974',
  ink: '#1a1a18',
  inkMuted: '#4a4946',
  marginBg: '#f0efec',
  vizWidth: 480,
  marginWidth: 120,
  barHeight: 16,
  barGap: 3,
  labelWidth: 100,
  titleSize: 22,
  captionSize: 8,
} as const;

export const VARIANTS = { A: VARIANT_A, B: VARIANT_B, C: VARIANT_C } as const;
