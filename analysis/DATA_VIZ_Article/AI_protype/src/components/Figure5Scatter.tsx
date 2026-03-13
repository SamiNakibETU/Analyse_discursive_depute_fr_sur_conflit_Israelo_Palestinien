import React from 'react';
import { blocLabels, eventImpact } from '../data/article1';
import { F, P, T } from '../viz/tokens';

const events = ['CIJ (janv. 2024)', 'Rafah (mai 2024)', 'Cessez-le-feu (janv. 2025)'] as const;
const maxAbsDelta = Math.max(...eventImpact.map((d) => Math.abs(d.delta)));

export function Figure5Scatter() {
  const width = 760;
  const height = 320;
  const pad = 36;
  const xMin = 0;
  const xMax = 0.95;

  const toX = (p: number) => pad + ((p - xMin) / (xMax - xMin)) * (width - pad * 2);
  const toY = (d: number) => pad + ((maxAbsDelta - d) / (maxAbsDelta * 2)) * (height - pad * 2);

  return (
    <figure
      style={{
        maxWidth: 860,
        margin: 0,
        backgroundColor: P.paper,
        borderTop: `2px solid ${P.ink}`,
        padding: '20px 20px 18px',
      }}
    >
      <div style={{ fontFamily: T.mono, fontSize: 8, color: P.light, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 8 }}>
        Fig. 5
      </div>
      <h3 style={{ margin: 0, fontFamily: T.serif, fontSize: 28, lineHeight: 1.05, letterSpacing: '-0.02em', color: P.ink }}>
        Chocs : ampleur vs significativite
      </h3>
      <p style={{ margin: '8px 0 16px', fontFamily: T.sans, fontSize: 12, color: P.muted, lineHeight: 1.5, maxWidth: '48ch' }}>
        Chaque point est un bloc x evenement. Axe X : p-value. Axe Y : delta. Les points
        rouges sont significatifs (p &lt; 0.05).
      </p>

      <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: 340, display: 'block' }}>
        <line x1={pad} y1={height - pad} x2={width - pad} y2={height - pad} stroke={P.ruleStrong} strokeWidth="1" />
        <line x1={pad} y1={pad} x2={pad} y2={height - pad} stroke={P.ruleStrong} strokeWidth="1" />
        <line x1={pad} y1={toY(0)} x2={width - pad} y2={toY(0)} stroke={P.rule} strokeWidth="1" />

        {[0.05, 0.2, 0.4, 0.6, 0.8].map((x) => (
          <line key={x} x1={toX(x)} y1={pad} x2={toX(x)} y2={height - pad} stroke={P.rule} strokeWidth="1" />
        ))}

        {eventImpact.map((pt, i) => {
          const x = toX(pt.p);
          const y = toY(pt.delta);
          const sig = pt.p < 0.05;
          return (
            <g key={`${pt.event}-${pt.bloc}-${i}`}>
              <circle cx={x} cy={y} r={sig ? 6 : 4} fill={sig ? P.accent : P.frames[2]} />
              {sig && (
                <text x={x + 8} y={y - 6} fontFamily={T.mono} fontSize="8" fill={P.accent}>
                  {blocLabels[pt.bloc]}
                </text>
              )}
            </g>
          );
        })}

        <text x={pad} y={pad - 10} fontFamily={T.mono} fontSize="9" fill={P.light}>
          delta
        </text>
        <text x={width - pad - 56} y={height - 10} fontFamily={T.mono} fontSize="9" fill={P.light}>
          p-value
        </text>
      </svg>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12, marginTop: 8 }}>
        {events.map((event) => (
          <div key={event} style={{ borderTop: `1px solid ${P.rule}`, paddingTop: 8 }}>
            <div style={{ fontFamily: T.mono, fontSize: 8, color: P.ink, marginBottom: 4 }}>{event}</div>
            <div style={{ fontFamily: T.mono, fontSize: 8, color: P.light }}>
              {eventImpact.filter((d) => d.event === event && d.p < 0.05).length} points significatifs
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 10, fontFamily: T.mono, fontSize: 8, color: P.accent }}>
        {'-> concentration des points significatifs sur Rafah et Cessez-le-feu'}
      </div>

      <div style={{ marginTop: 12, fontFamily: T.mono, fontSize: 8, color: P.light, lineHeight: 1.55 }}>
        <span style={{ color: P.ink, fontWeight: 700 }}>Source</span> — event_impact_diff_in_diff.csv
      </div>
    </figure>
  );
}