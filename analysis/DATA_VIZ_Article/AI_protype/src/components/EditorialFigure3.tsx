import {
  blocLabels,
  eventImpact,
  mannKendallByBloc,
  wassersteinDriftSnapshots,
} from '../data/article1';
import { F, P, T } from '../viz/tokens';

const EVENTS = [
  'CIJ (janv. 2024)',
  'Rafah (mai 2024)',
  'Cessez-le-feu (janv. 2025)',
] as const;

const BLOCS = [
  'Gauche radicale',
  'Gauche moderee',
  'Centre / Majorite',
  'Droite',
] as const;

const maxAbsDelta = Math.max(...eventImpact.map((d) => Math.abs(d.delta)));

const maxWd = Math.max(
  ...wassersteinDriftSnapshots.flatMap((d) => [
    d.gaucheRadicale,
    d.gaucheModeree,
    d.centreMajorite,
    d.droite,
  ]),
);

const EVENT_NOTES: Record<string, string> = {
  'CIJ (janv. 2024)': 'Aucun effet significatif',
  'Rafah (mai 2024)': 'Gauche modérée et Centre bougent',
  'Cessez-le-feu (janv. 2025)': 'Mouvement le plus fort, surtout à droite',
};

export function EditorialFigure3() {
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
          III.
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
          Ils ne bougent pas
          <br />
          au même rythme
        </h3>
      </div>

      {/* Master: Matrice événements × blocs */}
      <div style={{ padding: '0 24px' }}>
        {/* En-têtes de colonnes */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '144px 1fr 1fr 1fr',
            gap: 10,
            marginBottom: 10,
          }}
        >
          <div />
          {EVENTS.map((ev) => (
            <div
              key={ev}
              style={{
                fontFamily: T.mono,
                fontSize: 8,
                color: P.light,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                textAlign: 'center',
                lineHeight: 1.45,
              }}
            >
              {ev}
            </div>
          ))}
        </div>

        {/* Lignes : blocs */}
        {BLOCS.map((bloc) => (
          <div
            key={bloc}
            style={{
              display: 'grid',
              gridTemplateColumns: '144px 1fr 1fr 1fr',
              gap: 10,
              alignItems: 'center',
              borderTop: `1px solid ${P.rule}`,
              padding: '12px 0',
            }}
          >
            <span
              style={{
                fontFamily: T.sans,
                fontSize: 11,
                fontWeight: 600,
                color: P.ink,
              }}
            >
              {blocLabels[bloc]}
            </span>
            {EVENTS.map((ev) => {
              const row = eventImpact.find((d) => d.event === ev && d.bloc === bloc);
              if (!row) return <div key={ev} />;
              const sig = row.p < 0.05;
              const barPct = (Math.abs(row.delta) / maxAbsDelta) * 50;

              return (
                <div key={ev} style={{ position: 'relative', height: 38 }}>
                  {/* Ligne zéro */}
                  <div
                    style={{
                      position: 'absolute',
                      left: '50%',
                      top: 0,
                      height: 26,
                      width: 1,
                      backgroundColor: P.ruleStrong,
                    }}
                  />
                  {/* Barre divergente */}
                  <div
                    style={{
                      position: 'absolute',
                      top: 4,
                      height: 18,
                      left:
                        row.delta >= 0
                          ? '50%'
                          : `calc(50% - ${barPct}%)`,
                      width: `${barPct}%`,
                      backgroundColor: sig ? P.accent : P.frames[2],
                      opacity: sig ? 1 : 0.5,
                    }}
                  />
                  {/* Valeur sous la barre */}
                  <div
                    style={{
                      position: 'absolute',
                      bottom: 0,
                      width: '100%',
                      textAlign: 'center',
                      fontFamily: T.mono,
                      fontSize: 8,
                      color: sig ? P.accent : P.light,
                    }}
                  >
                    {F.signed(row.delta, 2)}
                  </div>
                </div>
              );
            })}
          </div>
        ))}

        {/* Notes d'événement */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '144px 1fr 1fr 1fr',
            gap: 10,
            borderTop: `1px solid ${P.rule}`,
            paddingTop: 8,
            paddingBottom: 20,
          }}
        >
          <div />
          {EVENTS.map((ev) => (
            <div
              key={ev}
              style={{
                fontFamily: T.mono,
                fontSize: 8,
                color: P.accent,
                textAlign: 'center',
                lineHeight: 1.4,
              }}
            >
              {EVENT_NOTES[ev]}
            </div>
          ))}
        </div>

        <div
          style={{
            fontFamily: T.mono,
            fontSize: 8,
            color: P.muted,
            marginBottom: 20,
          }}
        >
          {'Barres rouges : p < 0.05. Axe centré sur zéro.'}
        </div>
      </div>

      {/* Divider */}
      <div style={{ height: 1, backgroundColor: P.ruleStrong, margin: '0 24px 18px' }} />

      {/* Secondary: Mann-Kendall + Wasserstein */}
      <div
        style={{
          padding: '0 24px 22px',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 28,
        }}
      >
        {/* Mann-Kendall */}
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
            Tendance séculaire — absente
          </div>
          {mannKendallByBloc.map((row) => (
            <div
              key={row.bloc}
              style={{
                display: 'grid',
                gridTemplateColumns: '132px 1fr 52px',
                gap: 8,
                alignItems: 'center',
                marginBottom: 9,
              }}
            >
              <span style={{ fontFamily: T.sans, fontSize: 10, color: P.ink }}>
                {blocLabels[row.bloc]}
              </span>
              <div style={{ position: 'relative', height: 14 }}>
                <div
                  style={{
                    position: 'absolute',
                    left: '50%',
                    top: -1,
                    bottom: -1,
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
                      row.tau >= 0
                        ? '50%'
                        : `calc(50% - ${(Math.abs(row.tau) / 0.25) * 50}%)`,
                    width: `${(Math.abs(row.tau) / 0.25) * 50}%`,
                    backgroundColor: P.frames[2],
                  }}
                />
              </div>
              <span
                style={{
                  fontFamily: T.mono,
                  fontSize: 9,
                  color: P.muted,
                  textAlign: 'right',
                }}
              >
                {F.signed(row.tau, 2)}
              </span>
            </div>
          ))}
          <div
            style={{
              fontFamily: T.mono,
              fontSize: 8,
              color: P.muted,
              marginTop: 4,
            }}
          >
            {'Aucun tau significatif (p > 0.15)'}
          </div>
        </div>

        {/* Wasserstein drift */}
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
            Drift lexical — sans direction
          </div>
          {wassersteinDriftSnapshots.map((snap) => {
            const avg =
              (snap.gaucheRadicale +
                snap.gaucheModeree +
                snap.centreMajorite +
                snap.droite) /
              4;
            const hot = avg > 0.12;
            return (
              <div
                key={snap.month}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '66px 1fr 48px',
                  gap: 8,
                  alignItems: 'center',
                  marginBottom: 9,
                }}
              >
                <span
                  style={{ fontFamily: T.mono, fontSize: 8, color: P.ink }}
                >
                  {snap.month}
                </span>
                <div style={{ position: 'relative', height: 14 }}>
                  <div
                    style={{ position: 'absolute', inset: 0, backgroundColor: '#efefef' }}
                  />
                  <div
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      bottom: 0,
                      width: `${(avg / maxWd) * 100}%`,
                      backgroundColor: hot ? P.accent : P.frames[2],
                    }}
                  />
                </div>
                <span
                  style={{
                    fontFamily: T.mono,
                    fontSize: 9,
                    color: hot ? P.accent : P.muted,
                    textAlign: 'right',
                  }}
                >
                  {avg.toFixed(3)}
                </span>
              </div>
            );
          })}
          <div
            style={{ fontFamily: T.mono, fontSize: 8, color: P.muted, marginTop: 4 }}
          >
            Oscillation irrégulière, sans pente lente
          </div>
        </div>
      </div>
    </figure>
  );
}
