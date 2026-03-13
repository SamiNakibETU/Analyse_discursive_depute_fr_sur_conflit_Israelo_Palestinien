import {
  blocLabels,
  tweetsPerDeputy,
  twitterVsAnByBloc,
  visibilityByQuintile,
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
const BLOC_FILL: Record<string, string> = {
  'Gauche radicale':   '#C8102E',
  'Gauche moderee':    '#D4623A',
  'Centre / Majorite': '#2055A5',
  'Droite':            '#1A3F6E',
};

const signed = (n: number, d = 2) => (n >= 0 ? `+${n.toFixed(d)}` : n.toFixed(d));

const maxTweets = Math.max(...tweetsPerDeputy.map((d) => d.value));
const maxVis    = Math.max(...visibilityByQuintile.map((d) => d.value));
const maxDelta  = Math.max(...twitterVsAnByBloc.map((d) => Math.abs(d.delta)));

/* ─── Composant ─────────────────────────────────────────────────── */
export function Layer2Visibility() {
  return (
    <section style={{ borderTop: `3px solid ${ACCENT}`, paddingTop: 20 }}>

      {/* ── Kicker ── */}
      <div style={{ fontFamily: MONO, fontSize: 9, color: ACCENT, letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 14, fontWeight: 700 }}>
        II&ensp;—&ensp;Visibilité publique
      </div>

      {/* ── Titre ── */}
      <h2 style={{ margin: '0 0 22px', fontFamily: MATTONE, fontSize: 44, lineHeight: 0.96, letterSpacing: '-0.01em', color: INK, fontWeight: 900 }}>
        Ils ne le disent pas aux mêmes personnes
      </h2>

      {/* ── Chapeau 2 colonnes ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, marginBottom: 22 }}>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          La gauche radicale publie 122&nbsp;tweets par député sur X, contre 17 au Centre.
          Le débat vu en ligne ne reflète pas l&apos;Assemblée&nbsp;: il reflète une suractivité
          différentielle, structurée par les blocs, pas par le sujet.
        </p>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          Le quintile le plus visible a un |stance| moyen de 1,57 contre 1,00 pour le moins visible.
          Seule la gauche radicale présente un décalage significatif entre hémicycle et Twitter
          (+0,50,&nbsp;p&nbsp;=&nbsp;0,011).
        </p>
      </div>

      <div style={{ borderTop: `1px solid ${RULE}`, marginBottom: 22 }} />

      {/* ═══════════════════════════════════════════════════════════
          Premier rang : barres tweets + Encadré ×7
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 228px', gap: 18, alignItems: 'start', marginBottom: 18 }}>

        {/* Figure principale : tweets/député */}
        <div style={{ background: FIG_BG, padding: '18px 22px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 18, fontWeight: 700 }}>
            Tweets publiés par député — moyenne par bloc politique
          </div>

          {tweetsPerDeputy.map((row, idx) => {
            const fill   = BLOC_FILL[row.bloc] ?? DIM;
            const isMax  = idx === 0;
            const barH   = isMax ? 50 : 34;
            return (
              <div
                key={row.bloc}
                style={{ display: 'grid', gridTemplateColumns: '188px 1fr 72px', gap: 0, alignItems: 'center', borderTop: `1px solid rgba(0,0,0,0.07)`, padding: '10px 0' }}
              >
                <div style={{ paddingRight: 18 }}>
                  <div style={{ fontFamily: SANS, fontSize: 12, fontWeight: isMax ? 700 : 600, color: INK }}>
                    {blocLabels[row.bloc]}
                  </div>
                </div>

                <div style={{ position: 'relative', height: barH }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: 'rgba(0,0,0,0.05)' }} />
                  <div style={{ position: 'absolute', inset: 0, width: `${(row.value / maxTweets) * 100}%`, backgroundColor: fill }} />
                </div>

                <div style={{ paddingLeft: 14, textAlign: 'right' }}>
                  <span style={{ fontFamily: MONO, fontSize: isMax ? 26 : 17, fontWeight: 700, color: fill }}>
                    {Math.round(row.value)}
                  </span>
                </div>
              </div>
            );
          })}

          <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 9 }}>
            Nombre moyen de tweets publiés sur X par député, sur l&apos;ensemble de la période 2023–2026
          </div>
        </div>

        {/* ── Encadré ×7 ── */}
        <div style={{ border: `1px solid ${RULE}` }}>
          <div style={{ background: ACCENT, padding: '9px 16px' }}>
            <div style={{ fontFamily: MONO, fontSize: 7.5, color: 'rgba(255,255,255,0.85)', textTransform: 'uppercase', letterSpacing: '0.16em', fontWeight: 700 }}>
              Paradoxe de visibilité
            </div>
          </div>
          <div style={{ padding: '18px 16px' }}>
            <div style={{ fontFamily: MONO, fontSize: 52, fontWeight: 700, color: INK, letterSpacing: '-0.04em', lineHeight: 1, marginBottom: 6 }}>
              ×7
            </div>
            <div style={{ fontFamily: MONO, fontSize: 8, color: ACCENT, textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 700, marginBottom: 14 }}>
              LFI vs Centre — tweets/député
            </div>
            <div style={{ borderTop: `1px solid ${RULE}`, paddingTop: 12, fontFamily: SANS, fontSize: 12, color: MID, lineHeight: 1.6 }}>
              122 tweets vs 17. L&apos;impression d&apos;unanimité en ligne sur Gaza est le produit d&apos;une suractivité d&apos;un seul camp, pas d&apos;un consensus.
            </div>
          </div>
        </div>

      </div>

      {/* ═══════════════════════════════════════════════════════════
          Second rang : Quintile × stance + Twitter vs AN
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18 }}>

        {/* Col A : Quintile */}
        <div style={{ background: FIG_BG, padding: '16px 20px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 14, fontWeight: 700 }}>
            Visibilité × radicalité de position
          </div>
          <div style={{ fontFamily: SANS, fontSize: 11.5, color: MID, marginBottom: 14, lineHeight: 1.5 }}>
            |stance| moyen par quintile de visibilité Twitter
          </div>
          {visibilityByQuintile.map((row, idx) => {
            const isTop = idx === visibilityByQuintile.length - 1;
            return (
              <div key={row.quintile} style={{ display: 'grid', gridTemplateColumns: '136px 1fr 44px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: SANS, fontSize: 10, color: isTop ? INK : MID, fontWeight: isTop ? 700 : 400 }}>
                  {row.quintile}
                </span>
                <div style={{ position: 'relative', height: 18 }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: 'rgba(0,0,0,0.07)' }} />
                  <div style={{ position: 'absolute', inset: 0, width: `${(row.value / maxVis) * 100}%`, backgroundColor: isTop ? ACCENT : '#2055A5' }} />
                </div>
                <span style={{ fontFamily: MONO, fontSize: 11, fontWeight: 700, color: isTop ? ACCENT : DIM, textAlign: 'right' }}>
                  {row.value.toFixed(2)}
                </span>
              </div>
            );
          })}
          <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 8 }}>
            Q5 = +57&nbsp;% de radicalité vs Q1
          </div>
        </div>

        {/* Col B : Twitter vs AN delta */}
        <div style={{ background: FIG_BG, padding: '16px 20px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 14, fontWeight: 700 }}>
            Surjeu Twitter vs hémicycle — delta de stance
          </div>
          <div style={{ fontFamily: SANS, fontSize: 11.5, color: MID, marginBottom: 14, lineHeight: 1.5 }}>
            Différence stance X&nbsp;− stance AN, par bloc. Rouge&nbsp;: p&nbsp;{'<'}&nbsp;0,05
          </div>
          {twitterVsAnByBloc.map((row) => {
            const sig  = row.significant;
            const pct  = (Math.abs(row.delta) / maxDelta) * 50;
            const fill = BLOC_FILL[row.bloc] ?? DIM;
            return (
              <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '148px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: SANS, fontSize: 10, color: sig ? INK : MID, fontWeight: sig ? 700 : 400 }}>
                  {blocLabels[row.bloc]}
                </span>
                <div style={{ position: 'relative', height: 18 }}>
                  <div style={{ position: 'absolute', left: '50%', top: -2, bottom: -2, width: 1.5, backgroundColor: DIM, opacity: 0.4 }} />
                  <div style={{
                    position: 'absolute', top: 0, bottom: 0,
                    left: row.delta >= 0 ? '50%' : `calc(50% - ${pct}%)`,
                    width: `${pct}%`,
                    backgroundColor: sig ? fill : '#BBBBBB',
                    opacity: sig ? 1 : 0.6,
                  }} />
                </div>
                <span style={{ fontFamily: MONO, fontSize: 11, fontWeight: 700, color: sig ? fill : DIM, textAlign: 'right' }}>
                  {signed(row.delta, 2)}
                </span>
              </div>
            );
          })}
          <div style={{ fontFamily: MONO, fontSize: 7.5, color: ACCENT, marginTop: 8, fontWeight: 700 }}>
            Seule la gauche radicale surjoue significativement (p&nbsp;=&nbsp;0,011)
          </div>
        </div>

      </div>
    </section>
  );
}
