/**
 * FIGURE 1 — Cadrages et lexiques
 *
 * Architecture : Le Point × Joost Grootens × Catalogtree
 *
 * Principes structurants :
 * — Grille à colonnes fixes (label / bar / value)
 * — Fond blanc uniquement — la structure vient de l'alignement, pas des fonds
 * — Règle 2px au-dessus : autorité éditoriale
 * — Règle 1px entre blocs : séparation nette, pas de gouttière
 * — Valeurs hors des barres, dans leur propre colonne
 * — Palette : échelle grise (frames) + 1 accent rouge (droite lexicale)
 * — Typographie : 3 voix (serif titre, sans labels, mono data)
 */

import React from 'react';
import { blocLabels, frameRows, lexicalContrast } from '../data/article1';
import { F, FIG, P, T } from '../viz/tokens';

const SEGMENTS = [
  { key: 'HUM' as const, label: 'Humanitaire' },
  { key: 'SEC' as const, label: 'Sécuritaire' },
  { key: 'MOR' as const, label: 'Moral' },
  { key: 'OTH' as const, label: 'Autres' },
] as const;

function dominant(row: (typeof frameRows)[0]) {
  return SEGMENTS
    .map((s) => ({ key: s.key, val: row[s.key], idx: SEGMENTS.indexOf(s) }))
    .reduce((a, b) => (b.val > a.val ? b : a));
}

export function EditorialFigure1() {
  const leftWords = lexicalContrast.gauche.slice(0, 8);
  const rightWords = lexicalContrast.droite.slice(0, 8);
  const maxZ = Math.max(...leftWords.map((d) => d.z), ...rightWords.map((d) => d.z));

  /* Colonnes frames */
  const LC = FIG.labelCol;
  const VC = FIG.valueCol;
  const BC = FIG.barCol;
  const GRID_FRAMES = `${LC}px ${BC}px ${VC}px`;

  /* Colonnes butterfly */
  const WC = FIG.bfWordCol;
  const ZC = FIG.bfZCol;
  const BBC = FIG.bfBarCol;
  const GRID_BF = `${WC}px ${ZC}px ${BBC}px 1px ${BBC}px ${ZC}px ${WC}px`;

  return (
    <figure
      style={{
        maxWidth: FIG.width,
        margin: 0,
        padding: 0,
        /* Règle lourde au-dessus — autorité éditoriale (ref. Prezzo, Grootens) */
        borderTop: `2px solid ${P.ruleHeavy}`,
        paddingTop: 20,
      }}
    >

      {/* ── EN-TÊTE ─────────────────────────────────────────────────── */}
      <div style={{ marginBottom: 20 }}>
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 9,
            fontWeight: 400,
            color: P.inkMuted,
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            marginBottom: 6,
          }}
        >
          Fig. 1
        </div>
        <h3
          style={{
            margin: 0,
            fontFamily: T.serif,
            fontSize: 26,
            fontWeight: 600,
            lineHeight: 1.1,
            letterSpacing: '-0.02em',
            color: P.ink,
          }}
        >
          Cadrages et lexiques ne se recouvrent pas
        </h3>
        <p
          style={{
            margin: '6px 0 0',
            fontFamily: T.sans,
            fontSize: 12,
            lineHeight: 1.5,
            color: P.inkMuted,
            maxWidth: '44ch',
          }}
        >
          Répartition des cadres interprétatifs par bloc politique, puis mots
          les plus discriminants entre gauche et droite (z-score fighting words).
        </p>
      </div>

      {/* ── BLOC A : CADRAGES ───────────────────────────────────────── */}
      <div style={{ marginBottom: 24 }}>

        {/* En-tête de bloc */}
        <div
          style={{
            display: 'flex',
            alignItems: 'baseline',
            gap: 10,
            marginBottom: 10,
            paddingBottom: 6,
            borderBottom: `1px solid ${P.ruleThin}`,
          }}
        >
          <span
            style={{
              fontFamily: T.mono,
              fontSize: 9,
              fontWeight: 600,
              color: P.inkLight,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
            }}
          >
            A
          </span>
          <span
            style={{
              fontFamily: T.sans,
              fontSize: 11,
              fontWeight: 500,
              color: P.inkMuted,
            }}
          >
            Répartition des cadres interprétatifs par bloc
          </span>
        </div>

        {/* Barres */}
        {frameRows.map((row) => {
          const dom = dominant(row);
          /* Positions cumulées pour les barres absolues */
          const offsets = SEGMENTS.reduce<number[]>((acc, seg) => {
            const last = acc[acc.length - 1] ?? 0;
            return [...acc, last + row[seg.key]];
          }, []);

          return (
            <div
              key={row.bloc}
              style={{
                display: 'grid',
                gridTemplateColumns: GRID_FRAMES,
                gap: '0 8px',
                alignItems: 'center',
                height: FIG.rowH,
                marginBottom: FIG.rowGap,
              }}
            >
              {/* Label */}
              <span
                style={{
                  fontFamily: T.sans,
                  fontSize: 11,
                  fontWeight: 500,
                  color: P.ink,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {blocLabels[row.bloc]}
              </span>

              {/* Barres stacked */}
              <div
                style={{
                  position: 'relative',
                  height: FIG.barH,
                  overflow: 'hidden',
                }}
              >
                {/* Grille verticale fine */}
                {[25, 50, 75].map((t) => (
                  <div
                    key={t}
                    aria-hidden
                    style={{
                      position: 'absolute',
                      left: `${t}%`,
                      top: 0,
                      bottom: 0,
                      width: 1,
                      backgroundColor: P.ruleThin,
                      zIndex: 0,
                    }}
                  />
                ))}
                {/* Segments */}
                {SEGMENTS.map((seg, i) => (
                  <div
                    key={seg.key}
                    title={`${seg.label}: ${F.pct(row[seg.key])}`}
                    style={{
                      position: 'absolute',
                      left: `${i === 0 ? 0 : offsets[i - 1]}%`,
                      width: `${row[seg.key]}%`,
                      top: 0,
                      height: '100%',
                      backgroundColor: P.frames[i],
                      zIndex: 1,
                    }}
                  />
                ))}
              </div>

              {/* Valeur dominante — colonne propre, hors de la barre */}
              <div
                style={{
                  fontFamily: T.mono,
                  fontSize: 11,
                  fontWeight: 600,
                  color: P.frames[dom.idx],
                  textAlign: 'right',
                }}
              >
                {F.pct(dom.val)}
              </div>
            </div>
          );
        })}

        {/* Axe — sous les barres, aligné sur la grille */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: GRID_FRAMES,
            gap: '0 8px',
            marginTop: 4,
          }}
        >
          <span />
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              fontFamily: T.mono,
              fontSize: 9,
              color: P.inkLight,
              letterSpacing: '0.02em',
            }}
          >
            {[0, 25, 50, 75, 100].map((t) => (
              <span key={t}>{t} %</span>
            ))}
          </div>
          <span />
        </div>

        {/* Légende — alignée sur l'axe */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: GRID_FRAMES,
            gap: '0 8px',
            marginTop: 10,
          }}
        >
          <span />
          <div
            style={{
              display: 'flex',
              gap: 14,
              fontFamily: T.sans,
              fontSize: 9,
              color: P.inkMuted,
            }}
          >
            {SEGMENTS.map((seg, i) => (
              <span key={seg.key} style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                <span
                  style={{
                    display: 'inline-block',
                    width: 5,
                    height: 5,
                    backgroundColor: P.frames[i],
                    flexShrink: 0,
                  }}
                />
                {seg.label}
              </span>
            ))}
          </div>
          <span />
        </div>
      </div>

      {/* ── RÈGLE DE SÉPARATION ──────────────────────────────────────── */}
      <div
        style={{
          height: 1,
          backgroundColor: P.ruleMid,
          marginBottom: 20,
        }}
      />

      {/* ── BLOC B : LEXIQUE DISCRIMINANT ────────────────────────────── */}
      <div>

        {/* En-tête de bloc */}
        <div
          style={{
            display: 'flex',
            alignItems: 'baseline',
            gap: 10,
            marginBottom: 10,
            paddingBottom: 6,
            borderBottom: `1px solid ${P.ruleThin}`,
          }}
        >
          <span
            style={{
              fontFamily: T.mono,
              fontSize: 9,
              fontWeight: 600,
              color: P.inkLight,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
            }}
          >
            B
          </span>
          <span
            style={{
              fontFamily: T.sans,
              fontSize: 11,
              fontWeight: 500,
              color: P.inkMuted,
            }}
          >
            Mots discriminants entre pôles (z-score)
          </span>
        </div>

        {/* En-têtes colonnes G/D */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: GRID_BF,
            gap: 0,
            marginBottom: 6,
          }}
        >
          <span />
          <span />
          <div style={{ textAlign: 'right' }}>
            <span
              style={{
                fontFamily: T.mono,
                fontSize: 9,
                fontWeight: 600,
                color: P.gauche,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
              }}
            >
              Gauche
            </span>
          </div>
          {/* Axe central — ligne verticale permanente */}
          <div />
          <div>
            <span
              style={{
                fontFamily: T.mono,
                fontSize: 9,
                fontWeight: 600,
                color: P.droite,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
              }}
            >
              Droite
            </span>
          </div>
          <span />
          <span />
        </div>

        {/* Lignes butterfly */}
        {leftWords.map((lw, idx) => {
          const rw = rightWords[idx];
          const lBarW = Math.round((lw.z / maxZ) * BBC);
          const rBarW = rw ? Math.round((rw.z / maxZ) * BBC) : 0;

          return (
            <div
              key={lw.word}
              style={{
                display: 'grid',
                gridTemplateColumns: GRID_BF,
                gap: 0,
                alignItems: 'center',
                height: FIG.bfRowH,
                marginBottom: 3,
              }}
            >
              {/* Mot gauche */}
              <div
                style={{
                  fontFamily: T.sans,
                  fontSize: 11,
                  color: P.ink,
                  textAlign: 'right',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {lw.word}
              </div>

              {/* z-score gauche */}
              <div
                style={{
                  fontFamily: T.mono,
                  fontSize: 9,
                  color: P.inkMuted,
                  textAlign: 'right',
                  paddingRight: 4,
                }}
              >
                {F.z(lw.z)}
              </div>

              {/* Barre gauche — croît vers le centre */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'flex-end',
                  alignItems: 'center',
                  height: '100%',
                }}
              >
                <div
                  style={{
                    width: lBarW,
                    height: FIG.bfBarH,
                    backgroundColor: P.gauche,
                  }}
                />
              </div>

              {/* Axe central (ligne 1px) */}
              <div
                style={{
                  width: 1,
                  height: FIG.bfBarH,
                  backgroundColor: P.ruleMid,
                  alignSelf: 'center',
                }}
              />

              {/* Barre droite — croît vers l'extérieur */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'flex-start',
                  alignItems: 'center',
                  height: '100%',
                }}
              >
                {rw && (
                  <div
                    style={{
                      width: rBarW,
                      height: FIG.bfBarH,
                      backgroundColor: P.droite,
                    }}
                  />
                )}
              </div>

              {/* z-score droite */}
              <div
                style={{
                  fontFamily: T.mono,
                  fontSize: 9,
                  color: P.inkMuted,
                  paddingLeft: 4,
                }}
              >
                {rw ? F.z(rw.z) : ''}
              </div>

              {/* Mot droite */}
              <div
                style={{
                  fontFamily: T.sans,
                  fontSize: 11,
                  color: P.ink,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {rw ? rw.word : ''}
              </div>
            </div>
          );
        })}
      </div>

      {/* ── PIED — SOURCE / MÉTHODE ──────────────────────────────────── */}
      <div
        style={{
          marginTop: 20,
          paddingTop: 10,
          borderTop: `1px solid ${P.ruleThin}`,
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 16,
        }}
      >
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 9,
            color: P.inkMuted,
            lineHeight: 1.5,
          }}
        >
          <span style={{ color: P.ink, fontWeight: 600 }}>Sources</span>
          {' '}— frames_par_bloc.csv · fighting_words.csv
        </div>
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 9,
            color: P.inkMuted,
            lineHeight: 1.5,
          }}
        >
          <span style={{ color: P.ink, fontWeight: 600 }}>Lecture</span>
          {' '}— Comparaison bloc par bloc. Contraste gauche/droite par z-score fighting words.
        </div>
      </div>
    </figure>
  );
}
