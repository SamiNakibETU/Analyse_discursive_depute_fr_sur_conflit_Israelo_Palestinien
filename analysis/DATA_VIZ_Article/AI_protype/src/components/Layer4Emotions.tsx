import {
  affectiveGap,
  effectiveDimensionalitySeries,
  emotionalRegisterByBloc,
  entropicPolarizationSeries,
} from '../data/article1';

/* ─── Palette Le Point ─────────────────────────────────────────── */
const ACCENT  = '#C8102E';
const INK     = '#141414';
const MID     = '#3A3A3A';
const DIM     = '#7A7A7A';
const RULE    = '#D8D6CE';
const FIG_BG  = '#F4F3ED';

const MONO    = '"IBM Plex Mono", monospace';
const SANS    = '"IBM Plex Sans", sans-serif';
const MATTONE = '"Mattone", sans-serif';

/* ─── Données ───────────────────────────────────────────────────── */
const BLOC_COLORS: Record<string, string> = {
  'Gauche radicale':   '#C8102E',
  'Gauche moderee':    '#D4623A',
  'Centre / Majorite': '#2055A5',
  'Droite':            '#1A3F6E',
};

const BLOC_LABELS: Record<string, string> = {
  'Gauche radicale':   'Gauche radicale',
  'Gauche moderee':    'Gauche modérée',
  'Centre / Majorite': 'Centre / Majorité',
  'Droite':            'Droite',
};

const EMOTION_LABELS: Record<string, string> = {
  indignation: 'Indignation',
  solidarite:  'Solidarité',
  neutral:     'Neutre',
  grief:       'Tristesse',
  anger:       'Colère',
  defiance:    'Défiance',
  fear:        'Peur',
};

const BLOC_ORDER = [
  'Gauche radicale',
  'Gauche moderee',
  'Centre / Majorite',
  'Droite',
] as const;

function makeVadPath(
  series: { month: string; value: number }[],
  w: number,
  h: number,
): string {
  if (series.length < 2) return '';
  const min   = Math.min(...series.map((d) => d.value));
  const max   = Math.max(...series.map((d) => d.value));
  const range = max - min || 1;
  return series
    .map((d, i) => {
      const x = (i / (series.length - 1)) * w;
      const y = h - ((d.value - min) / range) * (h - 12) - 6;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');
}

/* ─── Composant ─────────────────────────────────────────────────── */
export function Layer4Emotions() {
  const ecStart = entropicPolarizationSeries[0]?.value    ?? 0;
  const ecEnd   = entropicPolarizationSeries[entropicPolarizationSeries.length - 1]?.value ?? 0;
  const edStart = effectiveDimensionalitySeries[0]?.value ?? 0;
  const edEnd   = effectiveDimensionalitySeries[effectiveDimensionalitySeries.length - 1]?.value ?? 0;
  const vadStart = affectiveGap[0]?.value ?? 0;
  const vadEnd   = affectiveGap[affectiveGap.length - 1]?.value ?? 0;

  const SVG_W = 580;
  const SVG_H = 82;
  const path  = makeVadPath(affectiveGap, SVG_W, SVG_H);

  return (
    <section style={{ borderTop: `3px solid ${ACCENT}`, paddingTop: 20 }}>

      {/* ── Kicker ── */}
      <div style={{ fontFamily: MONO, fontSize: 9, color: ACCENT, letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 14, fontWeight: 700 }}>
        IV&ensp;—&ensp;Registres affectifs
      </div>

      {/* ── Titre ── */}
      <h2 style={{ margin: '0 0 22px', fontFamily: MATTONE, fontSize: 44, lineHeight: 0.96, letterSpacing: '-0.01em', color: INK, fontWeight: 900 }}>
        Même les émotions divergent
      </h2>

      {/* ── Chapeau 2 colonnes ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, marginBottom: 22 }}>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          La gauche radicale est dominée à 64&nbsp;% par l&apos;indignation. La droite par la
          défiance (41&nbsp;%). Le centre reste à 44&nbsp;% neutre. L&apos;architecture affective
          de chaque bloc est stable, distincte, et structurellement persistante sur toute la période.
        </p>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          Le gap affectif VAD plus que double entre 2023 et 2026. L&apos;entropie Ec et la
          dimensionnalité effective ED restent stables&nbsp;: la structure du désaccord ne change
          pas, seule l&apos;intensité émotionnelle monte.
        </p>
      </div>

      <div style={{ borderTop: `1px solid ${RULE}`, marginBottom: 22 }} />

      {/* ═══════════════════════════════════════════════════════════
          Figure 1 : 2×2 panneaux émotionnels (pleine largeur)
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ background: FIG_BG, padding: '18px 22px', marginBottom: 18 }}>
        <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 18, fontWeight: 700 }}>
          Registre émotionnel dominant par bloc — % des interventions
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {BLOC_ORDER.map((bloc) => {
            const values  = emotionalRegisterByBloc[bloc as keyof typeof emotionalRegisterByBloc];
            const entries = (Object.entries(values) as [string, number][]).sort((a, b) => b[1] - a[1]);
            const [mainKey, mainVal] = entries[0];
            const color   = BLOC_COLORS[bloc] ?? DIM;

            return (
              <div key={bloc} style={{ background: '#ffffff', borderTop: `3px solid ${color}`, padding: '14px 16px' }}>
                {/* Header panneau */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 6 }}>
                  <div>
                    <div style={{ fontFamily: SANS, fontSize: 12, fontWeight: 700, color: INK, marginBottom: 4 }}>
                      {BLOC_LABELS[bloc]}
                    </div>
                    <div style={{ fontFamily: MONO, fontSize: 8, color, textTransform: 'uppercase', letterSpacing: '0.12em', fontWeight: 700 }}>
                      {EMOTION_LABELS[mainKey] ?? mainKey}
                    </div>
                  </div>
                  <div style={{ fontFamily: MONO, fontSize: 34, fontWeight: 700, color, letterSpacing: '-0.04em', lineHeight: 1 }}>
                    {mainVal.toFixed(0)}%
                  </div>
                </div>

                {/* Barres émotions */}
                <div style={{ borderTop: `1px solid rgba(0,0,0,0.08)`, paddingTop: 10, marginTop: 8 }}>
                  {entries.map(([reg, val]) => (
                    <div key={reg} style={{ display: 'grid', gridTemplateColumns: '88px 1fr 36px', gap: 6, alignItems: 'center', marginBottom: 7 }}>
                      <span style={{ fontFamily: SANS, fontSize: 9.5, color: reg === mainKey ? INK : MID, fontWeight: reg === mainKey ? 700 : 400 }}>
                        {EMOTION_LABELS[reg] ?? reg}
                      </span>
                      <div style={{ position: 'relative', height: 14 }}>
                        <div style={{ position: 'absolute', inset: 0, backgroundColor: 'rgba(0,0,0,0.07)' }} />
                        <div style={{ position: 'absolute', inset: 0, width: `${(val / mainVal) * 100}%`, backgroundColor: reg === mainKey ? color : '#BBBBBB' }} />
                      </div>
                      <span style={{ fontFamily: MONO, fontSize: 9, color: reg === mainKey ? color : DIM, textAlign: 'right', fontWeight: reg === mainKey ? 700 : 400 }}>
                        {val.toFixed(1)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 14 }}>
          Source&nbsp;: analyse des registres affectifs — classifieur BERT adapté, 577&nbsp;députés, 2023–2026
        </div>
      </div>

      {/* ═══════════════════════════════════════════════════════════
          Second rang : VAD line chart + Encadré Ec/ED
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 228px', gap: 18, alignItems: 'start' }}>

        {/* VAD line chart */}
        <div style={{ background: FIG_BG, padding: '16px 20px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 8, fontWeight: 700 }}>
            Gap affectif VAD — montée continue depuis 2023
          </div>
          <div style={{ fontFamily: SANS, fontSize: 11.5, color: MID, marginBottom: 14, lineHeight: 1.5 }}>
            Écart de valence-arousal-dominance entre blocs politiques
          </div>
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: '100%', height: SVG_H + 4, display: 'block' }}
            aria-hidden
          >
            {[0.25, 0.5, 0.75].map((f) => (
              <line key={f} x1="0" y1={SVG_H * (1 - f)} x2={SVG_W} y2={SVG_H * (1 - f)} stroke={RULE} strokeWidth="0.75" />
            ))}
            <line x1="0" y1={SVG_H} x2={SVG_W} y2={SVG_H} stroke={DIM} strokeWidth="1" />
            <path d={path} fill="none" stroke={ACCENT} strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" />
          </svg>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: MONO, fontSize: 8, color: DIM, marginTop: 7 }}>
            <span>oct. 2023&ensp;·&ensp;{vadStart.toFixed(3)}</span>
            <span>janv. 2026&ensp;·&ensp;<strong style={{ color: ACCENT }}>{vadEnd.toFixed(3)}</strong></span>
          </div>
        </div>

        {/* ── Encadré structure stable ── */}
        <div style={{ border: `1px solid ${RULE}` }}>
          <div style={{ background: ACCENT, padding: '9px 16px' }}>
            <div style={{ fontFamily: MONO, fontSize: 7.5, color: 'rgba(255,255,255,0.85)', textTransform: 'uppercase', letterSpacing: '0.16em', fontWeight: 700 }}>
              Structure stable
            </div>
          </div>
          <div style={{ padding: '18px 16px' }}>

            <div style={{ marginBottom: 18 }}>
              <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 6 }}>
                Entropie Ec
              </div>
              <div style={{ fontFamily: MONO, fontSize: 19, fontWeight: 700, color: INK, letterSpacing: '-0.02em' }}>
                {ecStart.toFixed(3)}&ensp;<span style={{ fontSize: 12, color: DIM }}>{'→'}</span>&ensp;{ecEnd.toFixed(3)}
              </div>
            </div>

            <div style={{ marginBottom: 18 }}>
              <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 6 }}>
                Dim. effective ED
              </div>
              <div style={{ fontFamily: MONO, fontSize: 19, fontWeight: 700, color: INK, letterSpacing: '-0.02em' }}>
                {edStart.toFixed(3)}&ensp;<span style={{ fontSize: 12, color: DIM }}>{'→'}</span>&ensp;{edEnd.toFixed(3)}
              </div>
            </div>

            <div style={{ borderTop: `1px solid ${RULE}`, paddingTop: 12, fontFamily: SANS, fontSize: 12, color: MID, lineHeight: 1.6 }}>
              La structure du désaccord reste intacte. Seule l&apos;intensité émotionnelle monte.
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
