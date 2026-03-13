import React from 'react';
import { blocLabels, frameRows, lexicalContrast } from '../data/article1';
import { FORMAT } from '../viz/tokens';
import { VARIANT_A, VARIANT_B, VARIANT_C } from '../viz/variants';

const FRAME_SEGMENTS = [
  { key: 'HUM' as const, label: 'Humanitaire' },
  { key: 'SEC' as const, label: 'Sécuritaire' },
  { key: 'MOR' as const, label: 'Moral' },
  { key: 'OTH' as const, label: 'Autres' },
] as const;

function getDominant(row: (typeof frameRows)[0]) {
  const entries = FRAME_SEGMENTS.map((s) => [s.key, row[s.key]] as const);
  return entries.reduce((a, b) => (b[1] > a[1] ? b : a));
}

type VariantConfig = typeof VARIANT_A | typeof VARIANT_B | typeof VARIANT_C;

function renderFramesBlock(
  config: VariantConfig,
  monoLabel = '"IBM Plex Mono", monospace'
) {
  const leftWords = lexicalContrast.gauche.slice(0, 8);
  const rightWords = lexicalContrast.droite.slice(0, 8);
  const maxZ = Math.max(
    ...leftWords.map((d) => d.z),
    ...rightWords.map((d) => d.z)
  );

  return (
    <>
      {/* Frames */}
      <div
        style={{
          position: 'relative',
          padding: config.id === 'A' ? '12px 16px 14px' : config.id === 'B' ? '16px 20px 18px' : '10px 12px 12px',
          backgroundColor: config.panelBg,
          overflow: 'hidden',
        }}
      >
        <div
          aria-hidden
          style={{
            position: 'absolute',
            left: config.labelWidth + 6,
            right: 16,
            top: (config.id === 'A' ? 12 : config.id === 'B' ? 16 : 10) + 18,
            bottom: config.id === 'A' ? 14 : config.id === 'B' ? 18 : 12,
            backgroundImage: `linear-gradient(to right, ${config.gridStroke} 1px, transparent 1px)`,
            backgroundSize: '25% 100%',
            pointerEvents: 'none',
          }}
        />
        <div style={{ position: 'relative' }}>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: `${config.labelWidth}px 1fr`,
              gap: 6,
              alignItems: 'baseline',
              marginBottom: 4,
            }}
          >
            <span />
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontFamily: monoLabel,
                fontSize: config.captionSize,
                color: config.inkMuted,
                letterSpacing: '0.03em',
              }}
            >
              {[0, 25, 50, 75, 100].map((t) => (
                <span key={t}>{t} %</span>
              ))}
            </div>
          </div>
          {frameRows.map((row) => {
            const [, domVal] = getDominant(row);
            return (
              <div
                key={row.bloc}
                style={{
                  display: 'grid',
                  gridTemplateColumns: `${config.labelWidth}px 1fr`,
                  gap: 6,
                  alignItems: 'center',
                  height: config.barHeight,
                  marginBottom: config.barGap,
                }}
              >
                <span
                  style={{
                    fontFamily: '"IBM Plex Sans", sans-serif',
                    fontSize: config.id === 'C' ? 10 : 11,
                    fontWeight: 500,
                    color: config.ink,
                  }}
                >
                  {blocLabels[row.bloc]}
                </span>
                <div
                  style={{
                    height: config.barHeight - 6,
                    display: 'flex',
                    overflow: 'hidden',
                    position: 'relative',
                  }}
                >
                  {FRAME_SEGMENTS.map((seg) => (
                    <div
                      key={seg.key}
                      style={{
                        width: `${row[seg.key]}%`,
                        minWidth: row[seg.key] > 0 ? 1 : 0,
                        height: '100%',
                        backgroundColor: (config.frames as Record<string, string>)[seg.key],
                      }}
                    />
                  ))}
                  {domVal >= 25 && (
                    <span
                      style={{
                        position: 'absolute',
                        right: 4,
                        top: '50%',
                        transform: 'translateY(-50%)',
                        fontFamily: monoLabel,
                        fontSize: config.captionSize,
                        fontWeight: 600,
                        color: '#ffffff',
                      }}
                    >
                      {FORMAT.percent(domVal)}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
          <div
            style={{
              display: 'flex',
              gap: 12,
              marginTop: 10,
              fontFamily: '"IBM Plex Sans", sans-serif',
              fontSize: config.captionSize,
              color: config.inkMuted,
            }}
          >
            {FRAME_SEGMENTS.map((seg) => (
              <span key={seg.key} style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                <span
                  style={{
                    width: 5,
                    height: 5,
                    backgroundColor: (config.frames as Record<string, string>)[seg.key],
                  }}
                />
                {seg.label}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Lexical butterfly */}
      <div
        style={{
          position: 'relative',
          marginTop: config.id === 'A' ? 2 : config.id === 'C' ? 1 : 0,
          padding: config.id === 'A' ? '14px 18px' : config.id === 'B' ? '20px 24px' : '12px 14px',
          backgroundColor: config.panelBg,
          overflow: 'hidden',
          borderTop: config.id === 'B' ? `2px solid ${config.dividerStroke}` : 'none',
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: '50%',
            top: config.id === 'A' ? 32 : config.id === 'B' ? 42 : 28,
            bottom: config.id === 'A' ? 14 : config.id === 'B' ? 20 : 12,
            width: 1,
            backgroundColor: config.axisStroke,
          }}
        />
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: config.id === 'C' ? 12 : 16,
            marginBottom: 6,
          }}
        >
          <div style={{ textAlign: 'right' }}>
            <span
              style={{
                fontFamily: '"IBM Plex Sans", sans-serif',
                fontSize: config.id === 'C' ? 8 : 9,
                fontWeight: 600,
                color: (config.lexical as Record<string, string>).gauche,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
              }}
            >
              Gauche
            </span>
          </div>
          <div>
            <span
              style={{
                fontFamily: '"IBM Plex Sans", sans-serif',
                fontSize: config.id === 'C' ? 8 : 9,
                fontWeight: 600,
                color: (config.lexical as Record<string, string>).droite,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
              }}
            >
              Droite
            </span>
          </div>
        </div>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: config.id === 'C' ? 12 : 16,
          }}
        >
          <div>
            {leftWords.map((word) => (
              <div
                key={word.word}
                style={{
                  height: config.barHeight,
                  marginBottom: config.barGap,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-end',
                  gap: 5,
                }}
              >
                <span
                  style={{
                    fontFamily: '"IBM Plex Sans", sans-serif',
                    fontSize: config.id === 'C' ? 10 : 11,
                    color: config.ink,
                    flexShrink: 0,
                  }}
                >
                  {word.word}
                </span>
                <span
                  style={{
                    width: `${(word.z / maxZ) * 42}%`,
                    minWidth: 32,
                    height: config.id === 'C' ? 10 : 12,
                    backgroundColor: (config.lexical as Record<string, string>).gauche,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'flex-end',
                    paddingRight: 4,
                    fontFamily: monoLabel,
                    fontSize: config.id === 'C' ? 8 : 9,
                    fontWeight: 600,
                    color: '#ffffff',
                    overflow: 'hidden',
                  }}
                >
                  {FORMAT.zScore(word.z)}
                </span>
              </div>
            ))}
          </div>
          <div>
            {rightWords.map((word) => (
              <div
                key={word.word}
                style={{
                  height: config.barHeight,
                  marginBottom: config.barGap,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-start',
                  gap: 5,
                }}
              >
                <span
                  style={{
                    width: `${(word.z / maxZ) * 42}%`,
                    minWidth: 32,
                    height: config.id === 'C' ? 10 : 12,
                    backgroundColor: (config.lexical as Record<string, string>).droite,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'flex-start',
                    paddingLeft: 4,
                    fontFamily: monoLabel,
                    fontSize: config.id === 'C' ? 8 : 9,
                    fontWeight: 600,
                    color: '#ffffff',
                    overflow: 'hidden',
                  }}
                >
                  {FORMAT.zScore(word.z)}
                </span>
                <span
                  style={{
                    fontFamily: '"IBM Plex Sans", sans-serif',
                    fontSize: config.id === 'C' ? 10 : 11,
                    color: config.ink,
                    flexShrink: 0,
                  }}
                >
                  {word.word}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}

/** Marge analytique intégrée (variantes A et C) */
function MarginBlock({
  config,
  showMargin,
}: {
  config: VariantConfig;
  showMargin: boolean;
}) {
  if (!showMargin || (config.id !== 'A' && config.id !== 'C')) return null;
  const marginBg = 'marginBg' in config ? config.marginBg : config.panelBg;
  return (
    <div
      style={{
        width: 'marginWidth' in config ? config.marginWidth : 0,
        paddingLeft: 16,
        borderLeft: `1px solid ${config.axisStroke}`,
        alignSelf: 'stretch',
        backgroundColor: marginBg,
        paddingTop: 12,
        paddingBottom: 12,
        paddingRight: 12,
      }}
    >
      <div
        style={{
          fontFamily: '"IBM Plex Mono", monospace',
          fontSize: config.captionSize,
          color: config.inkMuted,
          lineHeight: 1.5,
          display: 'flex',
          flexDirection: 'column',
          gap: 10,
        }}
      >
        <div>
          <span style={{ fontWeight: 600, color: config.ink }}>Sources</span>
          <br />
          frames_par_bloc.csv
          <br />
          fighting_words.csv
        </div>
        <div>
          <span style={{ fontWeight: 600, color: config.ink }}>Lecture</span>
          <br />
          Comparaison bloc par bloc puis contraste gauche/droite (z-score).
        </div>
      </div>
    </div>
  );
}

/** Variant A — Duo intégré : champ unique, marge droite */
export function EditorialFigure1VariantA() {
  const config = VARIANT_A;
  return (
    <figure
      style={{
        maxWidth: config.vizWidth + config.marginWidth,
        margin: 0,
        display: 'flex',
        flexDirection: 'row',
        overflow: 'hidden',
      }}
    >
      <div style={{ flex: '0 0 auto', width: config.vizWidth }}>
        <figcaption
          style={{
            margin: 0,
            fontFamily: '"IBM Plex Sans", sans-serif',
            fontSize: 9,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: config.inkMuted,
            marginBottom: 4,
          }}
        >
          Figure 1
        </figcaption>
        <h3
          style={{
            margin: '0 0 6px',
            fontFamily: '"Source Serif 4", Georgia, serif',
            fontSize: config.titleSize,
            lineHeight: 1.15,
            fontWeight: 600,
            color: config.ink,
            letterSpacing: '-0.01em',
          }}
        >
          Cadrages et lexiques ne se recouvrent pas
        </h3>
        <p
          style={{
            margin: '0 0 16px',
            fontFamily: '"IBM Plex Sans", sans-serif',
            fontSize: 12,
            lineHeight: 1.5,
            color: config.inkMuted,
            maxWidth: '38ch',
          }}
        >
          Répartition des cadres interprétatifs par bloc, puis mots les plus
          discriminants entre pôles.
        </p>
        {renderFramesBlock(config)}
      </div>
      <MarginBlock config={config} showMargin={true} />
    </figure>
  );
}

/** Variant B — Séparation : rupture nette, palette bordeaux/marine */
export function EditorialFigure1VariantB() {
  const config = VARIANT_B;
  return (
    <figure
      style={{
        maxWidth: 580,
        margin: 0,
      }}
    >
      <figcaption
        style={{
          margin: 0,
          fontFamily: '"IBM Plex Sans", sans-serif',
          fontSize: 9,
          letterSpacing: '0.08em',
          textTransform: 'uppercase',
          color: config.inkMuted,
          marginBottom: 4,
        }}
      >
        Figure 1
      </figcaption>
      <h3
        style={{
          margin: '0 0 8px',
          fontFamily: '"Source Serif 4", Georgia, serif',
          fontSize: config.titleSize,
          lineHeight: 1.12,
          fontWeight: 600,
          color: config.ink,
          letterSpacing: '-0.015em',
        }}
      >
        Cadrages et lexiques ne se recouvrent pas
      </h3>
      <p
        style={{
          margin: '0 0 20px',
          fontFamily: '"IBM Plex Sans", sans-serif',
          fontSize: 13,
          lineHeight: 1.5,
          color: config.inkMuted,
          maxWidth: '42ch',
        }}
      >
        Répartition des cadres interprétatifs par bloc, puis mots les plus
        discriminants entre pôles.
      </p>
      {renderFramesBlock(config)}
      {/* Bande analytique en bas */}
      <div
        style={{
          marginTop: 16,
          paddingTop: 12,
          borderTop: `1px solid ${config.axisStroke}`,
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 16,
          fontFamily: '"IBM Plex Mono", monospace',
          fontSize: config.captionSize,
          color: config.inkMuted,
          lineHeight: 1.45,
        }}
      >
        <div>
          <strong style={{ color: config.ink }}>Sources</strong> — frames_par_bloc.csv, fighting_words.csv
        </div>
        <div>
          <strong style={{ color: config.ink }}>Lecture</strong> — Comparaison bloc par bloc, contraste gauche/droite (z-score)
        </div>
      </div>
    </figure>
  );
}

/** Variant C — Condensation : plus dense, gamme chaude */
export function EditorialFigure1VariantC() {
  const config = VARIANT_C;
  return (
    <figure
      style={{
        maxWidth: config.vizWidth + config.marginWidth,
        margin: 0,
        display: 'flex',
        flexDirection: 'row',
        overflow: 'hidden',
      }}
    >
      <div style={{ flex: '0 0 auto', width: config.vizWidth }}>
        <figcaption
          style={{
            margin: 0,
            fontFamily: '"IBM Plex Sans", sans-serif',
            fontSize: 8,
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            color: config.inkMuted,
            marginBottom: 2,
          }}
        >
          Figure 1
        </figcaption>
        <h3
          style={{
            margin: '0 0 4px',
            fontFamily: '"Source Serif 4", Georgia, serif',
            fontSize: config.titleSize,
            lineHeight: 1.2,
            fontWeight: 600,
            color: config.ink,
            letterSpacing: '-0.02em',
          }}
        >
          Cadrages et lexiques ne se recouvrent pas
        </h3>
        <p
          style={{
            margin: '0 0 12px',
            fontFamily: '"IBM Plex Sans", sans-serif',
            fontSize: 11,
            lineHeight: 1.45,
            color: config.inkMuted,
            maxWidth: '36ch',
          }}
        >
          Répartition des cadres interprétatifs par bloc, puis mots les plus
          discriminants entre pôles.
        </p>
        {renderFramesBlock(config)}
      </div>
      <MarginBlock config={config} showMargin={true} />
    </figure>
  );
}
