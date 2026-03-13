/**
 * ARTICLE VISUAL SYSTEM
 * Swiss-minimal skeleton with controlled emphasis.
 */

export const GU = 8;

export const FIG = {
  width: 840,
  contentWidth: 640,
  marginWidth: 168,
  gap: 24,
} as const;

/**
 * Palette candidates requested:
 * - Option 1: black/gray/deep red
 * - Option 2: black/gray/editorial blue
 */
export const PALETTE_OPTIONS = {
  option1_red: {
    paper: '#ffffff',
    ink: '#111111',
    muted: '#595959',
    light: '#949494',
    rule: '#d9d9d9',
    ruleStrong: '#9d9d9d',
    accent: '#a32317',
    frames: ['#111111', '#3b3b3b', '#6b6b6b', '#a7a7a7'] as const,
  },
  option2_blue: {
    paper: '#ffffff',
    ink: '#101010',
    muted: '#545b63',
    light: '#8f98a3',
    rule: '#d8dde2',
    ruleStrong: '#8d98a5',
    accent: '#1f4e87',
    frames: ['#101010', '#38414a', '#697480', '#a4adb8'] as const,
  },
} as const;

/** Final recommendation retained for implementation */
export const P = PALETTE_OPTIONS.option1_red;

export const T = {
  serif: '"Source Serif 4", Georgia, serif',
  sans: '"IBM Plex Sans", sans-serif',
  mono: '"IBM Plex Mono", monospace',
} as const;

export const F = {
  pct: (n: number) => `${Math.round(n)} %`,
  z: (n: number) => n.toFixed(1),
  signed: (n: number, digits = 2) => `${n >= 0 ? '+' : ''}${n.toFixed(digits)}`,
} as const;
