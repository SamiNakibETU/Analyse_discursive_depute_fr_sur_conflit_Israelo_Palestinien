import { blocLabels, tweetsPerDeputy, twitterVsAnByBloc, visibilityByQuintile } from '../data/article1';
import { F, P, T } from '../viz/tokens';

const maxTweets = Math.max(...tweetsPerDeputy.map((d) => d.value));
const maxVis = Math.max(...visibilityByQuintile.map((d) => d.value));
const maxDelta = Math.max(...twitterVsAnByBloc.map((d) => Math.abs(d.delta)));

export function EditorialFigure2() {
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
          II.
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
          Ils ne le disent pas
          <br />
          aux mêmes personnes
        </h3>
      </div>

      {/* Master: Volume de publication — barres très épaisses (44px) */}
      <div style={{ padding: '0 24px' }}>
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
          Tweets publiés par député sur X — par bloc politique
        </div>
        {tweetsPerDeputy.map((row, idx) => (
          <div
            key={row.bloc}
            style={{
              display: 'grid',
              gridTemplateColumns: '172px 1fr 72px',
              gap: 16,
              alignItems: 'center',
              borderTop: `1px solid ${P.rule}`,
              padding: '11px 0',
            }}
          >
            <span
              style={{
                fontFamily: T.sans,
                fontSize: 12,
                fontWeight: idx === 0 ? 700 : 600,
                color: P.ink,
              }}
            >
              {blocLabels[row.bloc]}
            </span>
            <div style={{ position: 'relative', height: 44 }}>
              <div style={{ position: 'absolute', inset: 0, backgroundColor: '#efefef' }} />
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  width: `${(row.value / maxTweets) * 100}%`,
                  backgroundColor: idx === 0 ? P.accent : P.frames[1],
                }}
              />
            </div>
            <span
              style={{
                fontFamily: T.mono,
                fontSize: idx === 0 ? 20 : 15,
                fontWeight: 700,
                color: idx === 0 ? P.accent : P.ink,
                textAlign: 'right',
              }}
            >
              {Math.round(row.value)}
            </span>
          </div>
        ))}
        <div
          style={{
            marginTop: 8,
            fontFamily: T.mono,
            fontSize: 8,
            color: P.accent,
            marginBottom: 20,
          }}
        >
          {'-> Gauche radicale : ×7 plus active que le centre sur X'}
        </div>
      </div>

      {/* Divider */}
      <div style={{ height: 1, backgroundColor: P.ruleStrong, margin: '0 24px 18px' }} />

      {/* Secondary: 2 colonnes compactes */}
      <div
        style={{
          padding: '0 24px 22px',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 28,
        }}
      >
        {/* Col 1: Visibilité × stance */}
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
            Plus on est visible, plus la parole se tranche
          </div>
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.muted,
              marginBottom: 10,
            }}
          >
            |stance| moyen par quintile de visibilité
          </div>
          {visibilityByQuintile.map((row, idx) => (
            <div
              key={row.quintile}
              style={{
                display: 'grid',
                gridTemplateColumns: '112px 1fr 36px',
                gap: 8,
                alignItems: 'center',
                marginBottom: 9,
              }}
            >
              <span style={{ fontFamily: T.sans, fontSize: 10, color: P.ink }}>
                {row.quintile}
              </span>
              <div style={{ position: 'relative', height: 16 }}>
                <div style={{ position: 'absolute', inset: 0, backgroundColor: '#efefef' }} />
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    width: `${(row.value / maxVis) * 100}%`,
                    backgroundColor:
                      idx === visibilityByQuintile.length - 1 ? P.accent : P.frames[2],
                  }}
                />
              </div>
              <span
                style={{
                  fontFamily: T.mono,
                  fontSize: 10,
                  fontWeight: 700,
                  color: idx === visibilityByQuintile.length - 1 ? P.accent : P.ink,
                  textAlign: 'right',
                }}
              >
                {row.value.toFixed(2)}
              </span>
            </div>
          ))}
        </div>

        {/* Col 2: Twitter vs Assemblée */}
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
            Écart Twitter vs hémicycle, par bloc
          </div>
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.muted,
              marginBottom: 10,
            }}
          >
            {'delta de stance — en rouge si p < 0.05'}
          </div>
          {twitterVsAnByBloc.map((row) => (
            <div
              key={row.bloc}
              style={{
                display: 'grid',
                gridTemplateColumns: '122px 1fr 52px',
                gap: 8,
                alignItems: 'center',
                marginBottom: 9,
              }}
            >
              <span style={{ fontFamily: T.sans, fontSize: 10, color: P.ink }}>
                {blocLabels[row.bloc]}
              </span>
              <div style={{ position: 'relative', height: 16 }}>
                <div
                  style={{
                    position: 'absolute',
                    left: '50%',
                    top: -2,
                    bottom: -2,
                    width: 1,
                    backgroundColor: P.ruleStrong,
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    top: 0,
                    bottom: 0,
                    left:
                      row.delta >= 0
                        ? '50%'
                        : `calc(50% - ${(Math.abs(row.delta) / maxDelta) * 50}%)`,
                    width: `${(Math.abs(row.delta) / maxDelta) * 50}%`,
                    backgroundColor: row.significant ? P.accent : P.frames[2],
                    opacity: row.significant ? 1 : 0.6,
                  }}
                />
              </div>
              <span
                style={{
                  fontFamily: T.mono,
                  fontSize: 10,
                  fontWeight: 700,
                  color: row.significant ? P.accent : P.muted,
                  textAlign: 'right',
                }}
              >
                {F.signed(row.delta, 2)}
              </span>
            </div>
          ))}
          <div
            style={{
              marginTop: 4,
              fontFamily: T.mono,
              fontSize: 8,
              color: P.accent,
            }}
          >
            {'-> Seule la gauche radicale surjoue sur X (p = 0.01)'}
          </div>
        </div>
      </div>
    </figure>
  );
}
