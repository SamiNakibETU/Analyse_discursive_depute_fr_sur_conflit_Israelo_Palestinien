import { blocLabels, frameRows, lexicalContrast, registerPositionCorrelation } from '../data/article1';
import { P, T } from '../viz/tokens';

const SEGMENTS = [
  { key: 'HUM' as const, label: 'Humanitaire' },
  { key: 'SEC' as const, label: 'Sécuritaire' },
  { key: 'MOR' as const, label: 'Moral' },
  { key: 'OTH' as const, label: 'Autres' },
] as const;

const KEY_PAIRS = [
  { gauche: 'gaza', droite: 'hamas' },
  { gauche: 'génocide', droite: 'terroristes' },
  { gauche: 'massacres', droite: 'antisémitisme' },
];

function dominant(row: (typeof frameRows)[0]) {
  return SEGMENTS.map((s, i) => ({ ...s, val: row[s.key], idx: i })).reduce((a, b) =>
    b.val > a.val ? b : a,
  );
}

export function FigureV2Publication() {
  const maxZ = Math.max(
    ...KEY_PAIRS.flatMap((p) => [
      lexicalContrast.gauche.find((d) => d.word === p.gauche)?.z ?? 0,
      lexicalContrast.droite.find((d) => d.word === p.droite)?.z ?? 0,
    ]),
  );

  return (
    <figure
      style={{
        maxWidth: 860,
        margin: 0,
        backgroundColor: P.paper,
        borderTop: `3px solid ${P.ink}`,
      }}
    >
      {/* Section header */}
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
          I.
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
          Ils ne parlent pas
          <br />
          de la même chose
        </h3>
      </div>

      {/* Legend */}
      <div
        style={{
          padding: '0 24px',
          display: 'flex',
          gap: 16,
          marginBottom: 12,
        }}
      >
        {SEGMENTS.map((seg, i) => (
          <span
            key={seg.key}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              fontFamily: T.mono,
              fontSize: 8,
              color: P.muted,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
            }}
          >
            <span
              style={{
                width: 10,
                height: 10,
                backgroundColor: P.frames[i],
                display: 'inline-block',
                flexShrink: 0,
              }}
            />
            {seg.label}
          </span>
        ))}
      </div>

      {/* Master figure: Stacked bars — 34px height */}
      <div style={{ padding: '0 24px' }}>
        {frameRows.map((row) => {
          const dom = dominant(row);
          let acc = 0;

          return (
            <div
              key={row.bloc}
              style={{
                display: 'grid',
                gridTemplateColumns: '172px 1fr',
                gap: 16,
                alignItems: 'center',
                borderTop: `1px solid ${P.rule}`,
                padding: '13px 0',
              }}
            >
              <div>
                <div
                  style={{
                    fontFamily: T.sans,
                    fontSize: 12,
                    fontWeight: 700,
                    color: P.ink,
                    marginBottom: 4,
                  }}
                >
                  {blocLabels[row.bloc]}
                </div>
                <div
                  style={{
                    fontFamily: T.mono,
                    fontSize: 11,
                    fontWeight: 700,
                    color: dom.key === 'HUM' ? P.accent : P.muted,
                    letterSpacing: '0.06em',
                    textTransform: 'uppercase',
                  }}
                >
                  {Math.round(dom.val)}% {dom.label}
                </div>
              </div>
              <div style={{ position: 'relative', height: 34 }}>
                {[25, 50, 75].map((t) => (
                  <div
                    key={t}
                    aria-hidden
                    style={{
                      position: 'absolute',
                      left: `${t}%`,
                      top: -4,
                      bottom: -4,
                      width: 1,
                      backgroundColor: P.rule,
                    }}
                  />
                ))}
                {SEGMENTS.map((seg, i) => {
                  const sl = acc;
                  acc += row[seg.key];
                  return (
                    <div
                      key={seg.key}
                      style={{
                        position: 'absolute',
                        left: `${sl}%`,
                        width: `${row[seg.key]}%`,
                        top: 0,
                        bottom: 0,
                        backgroundColor: P.frames[i],
                      }}
                    />
                  );
                })}
              </div>
            </div>
          );
        })}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            fontFamily: T.mono,
            fontSize: 8,
            color: P.light,
            paddingLeft: 188,
            paddingTop: 5,
            paddingBottom: 20,
          }}
        >
          {[0, 25, 50, 75, 100].map((v) => (
            <span key={v}>{v}%</span>
          ))}
        </div>
      </div>

      {/* Divider */}
      <div style={{ height: 1, backgroundColor: P.ruleStrong, margin: '0 24px 18px' }} />

      {/* Butterfly lexical — 3 key pairs, bars 22px, words prominent */}
      <div style={{ padding: '0 24px' }}>
        {/* Column headers */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '120px 1fr 1px 1fr 120px',
            gap: 0,
            marginBottom: 10,
          }}
        >
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.light,
              textAlign: 'right',
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              paddingRight: 10,
            }}
          >
            Gauche
          </div>
          <div />
          <div style={{ backgroundColor: P.ruleStrong }} />
          <div />
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.light,
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              paddingLeft: 10,
            }}
          >
            Droite
          </div>
        </div>

        {KEY_PAIRS.map(({ gauche, droite }) => {
          const lw = lexicalContrast.gauche.find((d) => d.word === gauche);
          const rw = lexicalContrast.droite.find((d) => d.word === droite);
          if (!lw || !rw) return null;

          return (
            <div
              key={gauche}
              style={{
                display: 'grid',
                gridTemplateColumns: '120px 1fr 1px 1fr 120px',
                alignItems: 'center',
                gap: 0,
                marginBottom: 12,
              }}
            >
              <span
                style={{
                  fontFamily: T.sans,
                  fontSize: 13,
                  fontWeight: 700,
                  color: P.ink,
                  textAlign: 'right',
                  paddingRight: 12,
                }}
              >
                {lw.word}
              </span>
              <div style={{ display: 'flex', justifyContent: 'flex-end', height: 22 }}>
                <div
                  style={{
                    width: `${(lw.z / maxZ) * 100}%`,
                    height: '100%',
                    backgroundColor: P.ink,
                  }}
                />
              </div>
              <div style={{ backgroundColor: P.ruleStrong, alignSelf: 'stretch' }} />
              <div style={{ height: 22 }}>
                <div
                  style={{
                    width: `${(rw.z / maxZ) * 100}%`,
                    height: '100%',
                    backgroundColor: P.accent,
                  }}
                />
              </div>
              <span
                style={{
                  fontFamily: T.sans,
                  fontSize: 13,
                  fontWeight: 700,
                  color: P.accent,
                  paddingLeft: 12,
                }}
              >
                {rw.word}
              </span>
            </div>
          );
        })}
      </div>

      {/* Closing proof — ρ intégré dans la figure, pas dans une note latérale */}
      <div
        style={{
          borderTop: `1px solid ${P.rule}`,
          margin: '4px 24px 0',
          padding: '9px 0 22px',
          fontFamily: T.mono,
          fontSize: 9,
          color: P.muted,
        }}
      >
        {'ρ (registre discursif, positionnement) = '}
        <strong style={{ color: P.ink }}>{registerPositionCorrelation.toFixed(3)}</strong>
        {" — le ton d'un député ne prédit pas sa position"}
      </div>
    </figure>
  );
}
