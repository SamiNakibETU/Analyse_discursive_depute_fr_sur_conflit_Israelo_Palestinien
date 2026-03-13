/**
 * Section 1 — Ils ne parlent pas de la même chose
 * Direction A : deux preuves séparées, ultra lisibles
 *
 * SPÉCIFICATION :
 * — Grille : 0 25 50 75 100 sur X (frames) ; pas d’axe numérique butterfly
 * — Axes : trait 1px #c8c7c2, ticks 11px mono
 * — Chiffres : tabular-nums, 11px mono sur segments >12%
 * — Couleurs : palette sémantique fixe (HUM/SEC/MOR/OTH + gauche/droite)
 * — Typo : labels 12px sans, captions 11px sans
 */

import React from 'react';
import { frameRows, lexicalContrast } from '../data/article1';

const FRAME_COLORS = {
  HUM: '#0f6b50',
  SEC: '#1a4a8e',
  MOR: '#5c3d7a',
  OTH: '#8a8a85',
} as const;

const LEX_LEFT = '#a82e22';
const LEX_RIGHT = '#1a4a8e';

const BLOC_ORDER = ['Gauche radicale', 'Gauche moderee', 'Centre / Majorite', 'Droite'] as const;
const FRAME_ORDER = ['HUM', 'SEC', 'MOR', 'OTH'] as const;

const GRID_TICKS = [0, 25, 50, 75, 100];

export function Section1DataViz() {
  const leftWords = lexicalContrast.gauche.slice(0, 8);
  const rightWords = lexicalContrast.droite.slice(0, 8);
  const maxZ = Math.max(
    ...leftWords.map((d) => d.z),
    ...rightWords.map((d) => d.z)
  );

  const rows = BLOC_ORDER.map((id) => frameRows.find((r) => r.bloc === id)!).filter(Boolean);

  return (
    <div className="viz-section1">
      <div className="viz-wrapper">
        {/* PART 1 — Cadres par bloc (stacked 100%) */}
        <div className="viz-chart frames-chart">
          <div className="chart-y-axis">
            {rows.map((r) => (
              <div key={r.bloc} className="y-tick-row">
                <span className="y-label">{r.bloc.replace(' / ', '/')}</span>
              </div>
            ))}
          </div>
          <div className="chart-body">
            <div className="x-grid">
              {GRID_TICKS.map((t) => (
                <div
                  key={t}
                  className="grid-line"
                  style={{ left: `${t}%` }}
                  aria-hidden
                />
              ))}
            </div>
            <div className="x-ticks">
              {GRID_TICKS.map((t) => (
                <span key={t} className="x-tick" style={{ left: `${t}%` }}>
                  {t}%
                </span>
              ))}
            </div>
            <div className="bars-area">
              {rows.map((row) => (
                <div key={row.bloc} className="stacked-row">
                  <div className="stacked-bar">
                    {FRAME_ORDER.map((key) => {
                      const pct = row[key];
                      return (
                        <div
                          key={key}
                          className="segment"
                          style={{
                            width: `${pct}%`,
                            backgroundColor: FRAME_COLORS[key],
                          }}
                          title={`${key}: ${pct.toFixed(1)}%`}
                        >
                          {pct >= 12 && (
                            <span className="seg-value">{pct.toFixed(0)}</span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="frames-legend">
          {FRAME_ORDER.map((k) => (
            <span key={k} className="legend-item">
              <i style={{ background: FRAME_COLORS[k] }} />
              {k}
            </span>
          ))}
        </div>

        {/* PART 2 — Butterfly lexical */}
        <div className="viz-chart butterfly-chart">
          <div className="butterfly-axis" />
          <div className="butterfly-half left">
            {leftWords.map((d) => (
              <div key={d.word} className="lex-row">
                <span className="lex-word">{d.word}</span>
                <span
                  className="lex-bar"
                  style={{
                    width: `${(d.z / maxZ) * 100}%`,
                    backgroundColor: LEX_LEFT,
                  }}
                >
                  <span className="lex-z">{d.z.toFixed(1)}</span>
                </span>
              </div>
            ))}
          </div>
          <div className="butterfly-half right">
            {rightWords.map((d) => (
              <div key={d.word} className="lex-row">
                <span
                  className="lex-bar"
                  style={{
                    width: `${(d.z / maxZ) * 100}%`,
                    backgroundColor: LEX_RIGHT,
                  }}
                >
                  <span className="lex-z">{d.z.toFixed(1)}</span>
                </span>
                <span className="lex-word">{d.word}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="viz-caption">
          Les cadres dominants (humanitaire, sécuritaire, moral) et les lexiques discriminants
          ne se recoupent pas. Source : frames_par_bloc.csv, fighting_words.csv.
        </p>
      </div>
    </div>
  );
}
