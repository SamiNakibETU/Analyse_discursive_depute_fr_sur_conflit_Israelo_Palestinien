import {
  affectiveGap,
  effectiveDimensionalitySeries,
  emotionalRegisterByBloc,
  entropicPolarizationSeries,
} from '../data/article1';
import { P, T } from '../viz/tokens';

const EMOTION_LABELS: Record<string, string> = {
  indignation: 'Indignation',
  solidarite: 'Solidarité',
  neutral: 'Neutre',
  grief: 'Tristesse',
  anger: 'Colère',
  defiance: 'Défiance',
  fear: 'Peur',
};

const BLOC_ORDER = [
  'Gauche radicale',
  'Gauche moderee',
  'Centre / Majorite',
  'Droite',
] as const;

const BLOC_LABELS: Record<string, string> = {
  'Gauche radicale': 'Gauche radicale',
  'Gauche moderee': 'Gauche modérée',
  'Centre / Majorite': 'Centre / Majorité',
  Droite: 'Droite',
};

function makeVadPath(
  series: { month: string; value: number }[],
  w: number,
  h: number,
): string {
  if (series.length < 2) return '';
  const min = Math.min(...series.map((d) => d.value));
  const max = Math.max(...series.map((d) => d.value));
  const range = max - min || 1;
  return series
    .map((d, i) => {
      const x = (i / (series.length - 1)) * w;
      const y = h - ((d.value - min) / range) * (h - 8) - 4;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');
}

export function Figure4Emotions() {
  const ecStart = entropicPolarizationSeries[0]?.value ?? 0;
  const ecEnd = entropicPolarizationSeries[entropicPolarizationSeries.length - 1]?.value ?? 0;
  const edStart = effectiveDimensionalitySeries[0]?.value ?? 0;
  const edEnd =
    effectiveDimensionalitySeries[effectiveDimensionalitySeries.length - 1]?.value ?? 0;
  const vadStart = affectiveGap[0]?.value ?? 0;
  const vadEnd = affectiveGap[affectiveGap.length - 1]?.value ?? 0;

  const SVG_W = 700;
  const SVG_H = 72;
  const path = makeVadPath(affectiveGap, SVG_W, SVG_H);

  return (
    <figure
      style={{
        maxWidth: 860,
        margin: 0,
        backgroundColor: P.paper,
        borderTop: `3px solid ${P.ink}`,
      }}
    >
      {/* Header */}
      <div style={{ padding: '22px 24px 16px' }}>
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 9,
            color: P.light,
            letterSpacing: '0.22em',
            textTransform: 'uppercase',
            marginBottom: 10,
          }}
        >
          IV.
        </div>
        <h3
          style={{
            margin: 0,
            fontFamily: T.serif,
            fontSize: 32,
            lineHeight: 1.0,
            letterSpacing: '-0.03em',
            color: P.ink,
          }}
        >
          Même les émotions
          <br />
          divergent
        </h3>
      </div>

      {/* Master: Grille 2×2 de panels affectifs */}
      <div
        style={{
          padding: '0 24px',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 22,
        }}
      >
        {BLOC_ORDER.map((bloc) => {
          const values =
            emotionalRegisterByBloc[bloc as keyof typeof emotionalRegisterByBloc];
          const entries = (Object.entries(values) as [string, number][]).sort(
            (a, b) => b[1] - a[1],
          );
          const [mainKey, mainVal] = entries[0];
          const maxVal = entries[0][1];
          const isHot = mainKey === 'indignation' || mainKey === 'defiance';

          return (
            <div
              key={bloc}
              style={{
                borderTop: `2px solid ${isHot ? P.accent : P.ink}`,
                paddingTop: 12,
              }}
            >
              {/* Bloc name + dominant % */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  marginBottom: 6,
                }}
              >
                <span
                  style={{
                    fontFamily: T.sans,
                    fontSize: 12,
                    fontWeight: 700,
                    color: P.ink,
                  }}
                >
                  {BLOC_LABELS[bloc]}
                </span>
                <span
                  style={{
                    fontFamily: T.mono,
                    fontSize: 28,
                    fontWeight: 700,
                    color: isHot ? P.accent : P.ink,
                    letterSpacing: '-0.04em',
                    lineHeight: 1,
                  }}
                >
                  {mainVal.toFixed(0)}%
                </span>
              </div>

              {/* Label registre dominant */}
              <div
                style={{
                  fontFamily: T.mono,
                  fontSize: 8,
                  color: isHot ? P.accent : P.muted,
                  textTransform: 'uppercase',
                  letterSpacing: '0.12em',
                  marginBottom: 12,
                }}
              >
                {EMOTION_LABELS[mainKey] ?? mainKey}
              </div>

              {/* Distribution complète */}
              {entries.map(([reg, val]) => (
                <div
                  key={reg}
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '88px 1fr 36px',
                    gap: 7,
                    alignItems: 'center',
                    marginBottom: 7,
                  }}
                >
                  <span
                    style={{ fontFamily: T.sans, fontSize: 10, color: P.ink }}
                  >
                    {EMOTION_LABELS[reg] ?? reg}
                  </span>
                  <div style={{ position: 'relative', height: 14 }}>
                    <div
                      style={{
                        position: 'absolute',
                        inset: 0,
                        backgroundColor: '#efefef',
                      }}
                    />
                    <div
                      style={{
                        position: 'absolute',
                        inset: 0,
                        width: `${(val / maxVal) * 100}%`,
                        backgroundColor:
                          reg === mainKey
                            ? isHot
                              ? P.accent
                              : P.ink
                            : P.frames[2],
                      }}
                    />
                  </div>
                  <span
                    style={{
                      fontFamily: T.mono,
                      fontSize: 9,
                      color:
                        reg === mainKey ? (isHot ? P.accent : P.ink) : P.light,
                      textAlign: 'right',
                    }}
                  >
                    {val.toFixed(1)}
                  </span>
                </div>
              ))}
            </div>
          );
        })}
      </div>

      {/* Divider */}
      <div style={{ height: 1, backgroundColor: P.ruleStrong, margin: '20px 24px 18px' }} />

      {/* Secondary: courbe VAD + Ec/ED stables */}
      <div
        style={{
          padding: '0 24px 22px',
          display: 'grid',
          gridTemplateColumns: '1fr 200px',
          gap: 28,
        }}
      >
        {/* Courbe VAD */}
        <div>
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.light,
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              marginBottom: 12,
            }}
          >
            Gap affectif VAD — montée continue
          </div>
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            style={{ width: '100%', height: SVG_H + 4, display: 'block' }}
            aria-hidden
          >
            <line
              x1="0"
              y1={SVG_H}
              x2={SVG_W}
              y2={SVG_H}
              stroke={P.ruleStrong}
              strokeWidth="1"
            />
            <path
              d={path}
              fill="none"
              stroke={P.accent}
              strokeWidth="2.5"
              strokeLinejoin="round"
            />
          </svg>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              fontFamily: T.mono,
              fontSize: 8,
              color: P.light,
              marginTop: 5,
            }}
          >
            <span>oct. 2023 · {vadStart.toFixed(3)}</span>
            <span>
              janv. 2026 ·{' '}
              <strong style={{ color: P.accent }}>{vadEnd.toFixed(3)}</strong>
            </span>
          </div>
        </div>

        {/* Ec / ED stabilité */}
        <div>
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.light,
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              marginBottom: 14,
            }}
          >
            Structure stable
          </div>
          <div style={{ marginBottom: 18 }}>
            <div
              style={{
                fontFamily: T.mono,
                fontSize: 8,
                color: P.muted,
                marginBottom: 5,
              }}
            >
              Entropie Ec
            </div>
            <div
              style={{
                fontFamily: T.mono,
                fontSize: 15,
                fontWeight: 700,
                color: P.ink,
                letterSpacing: '-0.02em',
              }}
            >
              {ecStart.toFixed(3)}{' '}
              <span style={{ fontFamily: T.mono, fontSize: 10, color: P.muted }}>
                →
              </span>{' '}
              {ecEnd.toFixed(3)}
            </div>
          </div>
          <div>
            <div
              style={{
                fontFamily: T.mono,
                fontSize: 8,
                color: P.muted,
                marginBottom: 5,
              }}
            >
              Dim. effective ED
            </div>
            <div
              style={{
                fontFamily: T.mono,
                fontSize: 15,
                fontWeight: 700,
                color: P.ink,
                letterSpacing: '-0.02em',
              }}
            >
              {edStart.toFixed(3)}{' '}
              <span style={{ fontFamily: T.mono, fontSize: 10, color: P.muted }}>
                →
              </span>{' '}
              {edEnd.toFixed(3)}
            </div>
          </div>
          <div
            style={{
              marginTop: 14,
              fontFamily: T.mono,
              fontSize: 8,
              color: P.muted,
              lineHeight: 1.5,
            }}
          >
            La température monte.
            <br />
            L&apos;architecture reste.
          </div>
        </div>
      </div>
    </figure>
  );
}
