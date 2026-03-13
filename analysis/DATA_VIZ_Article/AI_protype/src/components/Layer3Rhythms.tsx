import {
  blocLabels,
  eventImpact,
  mannKendallByBloc,
  wassersteinDriftSnapshots,
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
const EVENTS = [
  { key: 'CIJ (janv. 2024)',          label: 'CIJ',          date: 'janv. 2024', note: 'Aucun effet sig.' },
  { key: 'Rafah (mai 2024)',           label: 'Rafah',        date: 'mai 2024',   note: 'G. modérée + Centre' },
  { key: 'Cessez-le-feu (janv. 2025)', label: 'Cessez-le-feu', date: 'janv. 2025', note: 'Mouvement le plus fort' },
] as const;

const BLOCS = [
  'Gauche radicale',
  'Gauche moderee',
  'Centre / Majorite',
  'Droite',
] as const;

const signed = (n: number, d = 2) => (n >= 0 ? `+${n.toFixed(d)}` : n.toFixed(d));

const maxAbsDelta = Math.max(...eventImpact.map((d) => Math.abs(d.delta)));
const maxWd       = Math.max(
  ...wassersteinDriftSnapshots.flatMap((d) => [
    d.gaucheRadicale, d.gaucheModeree, d.centreMajorite, d.droite,
  ]),
);

/* ─── Composant ─────────────────────────────────────────────────── */
export function Layer3Rhythms() {
  return (
    <section style={{ borderTop: `3px solid ${ACCENT}`, paddingTop: 20 }}>

      {/* ── Kicker ── */}
      <div style={{ fontFamily: MONO, fontSize: 9, color: ACCENT, letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 14, fontWeight: 700 }}>
        III&ensp;—&ensp;Réponse aux chocs
      </div>

      {/* ── Titre ── */}
      <h2 style={{ margin: '0 0 22px', fontFamily: MATTONE, fontSize: 44, lineHeight: 0.96, letterSpacing: '-0.01em', color: INK, fontWeight: 900 }}>
        Ils ne bougent pas au même rythme
      </h2>

      {/* ── Chapeau 2 colonnes ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, marginBottom: 22 }}>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          Trois chocs extérieurs, trois réactions distinctes. La CIJ (janvier&nbsp;2024)
          ne déplace personne de façon significative. Rafah (mai&nbsp;2024) fait bouger
          la gauche modérée et le Centre. Le cessez-le-feu de janvier&nbsp;2025 produit
          le mouvement le plus fort — surtout à droite.
        </p>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          Aucun test Mann-Kendall n&apos;indique de tendance séculaire vers la convergence
          ou la divergence. La distance de Wasserstein oscille sans direction.
          Le système réagit par chocs ponctuels, puis retourne à son état initial.
        </p>
      </div>

      <div style={{ borderTop: `1px solid ${RULE}`, marginBottom: 22 }} />

      {/* ═══════════════════════════════════════════════════════════
          Premier rang : matrice Événements × Blocs + Encadré
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 228px', gap: 18, alignItems: 'start', marginBottom: 18 }}>

        {/* Figure principale : matrice */}
        <div style={{ background: FIG_BG, padding: '18px 22px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 18, fontWeight: 700 }}>
            Réaction des blocs aux événements — delta de stance (centré sur zéro)
          </div>

          {/* En-têtes colonnes événements */}
          <div style={{ display: 'grid', gridTemplateColumns: '156px 1fr 1fr 1fr', gap: 8, marginBottom: 10 }}>
            <div />
            {EVENTS.map((ev) => (
              <div key={ev.key} style={{ textAlign: 'center' }}>
                <div style={{ fontFamily: SANS, fontSize: 12, fontWeight: 700, color: INK, marginBottom: 2 }}>{ev.label}</div>
                <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, letterSpacing: '0.04em' }}>{ev.date}</div>
              </div>
            ))}
          </div>

          {/* Lignes de données */}
          {BLOCS.map((bloc) => (
            <div
              key={bloc}
              style={{ display: 'grid', gridTemplateColumns: '156px 1fr 1fr 1fr', gap: 8, alignItems: 'center', borderTop: `1px solid rgba(0,0,0,0.07)`, padding: '10px 0' }}
            >
              <span style={{ fontFamily: SANS, fontSize: 11, fontWeight: 600, color: INK }}>
                {blocLabels[bloc]}
              </span>
              {EVENTS.map((ev) => {
                const row = eventImpact.find((d) => d.event === ev.key && d.bloc === bloc);
                if (!row) return <div key={ev.key} />;
                const sig      = row.p < 0.05;
                const barPct   = (Math.abs(row.delta) / maxAbsDelta) * 46;
                const barColor = sig ? (row.delta > 0 ? ACCENT : '#1A3F6E') : '#C0C0C0';
                return (
                  <div key={ev.key} style={{ position: 'relative', height: 44 }}>
                    {/* Axe zéro */}
                    <div style={{ position: 'absolute', left: '50%', top: 0, height: 30, width: 1.5, backgroundColor: DIM, opacity: 0.35 }} />
                    {/* Barre */}
                    <div style={{
                      position: 'absolute', top: 6, height: 18,
                      left: row.delta >= 0 ? '50%' : `calc(50% - ${barPct}%)`,
                      width: `${barPct}%`,
                      backgroundColor: barColor,
                    }} />
                    {/* Valeur */}
                    <div style={{ position: 'absolute', bottom: 0, width: '100%', textAlign: 'center', fontFamily: MONO, fontSize: 8.5, fontWeight: sig ? 700 : 400, color: sig ? barColor : DIM }}>
                      {signed(row.delta, 2)}
                    </div>
                  </div>
                );
              })}
            </div>
          ))}

          {/* Interprétations par événement */}
          <div style={{ display: 'grid', gridTemplateColumns: '156px 1fr 1fr 1fr', gap: 8, borderTop: `1px solid rgba(0,0,0,0.07)`, paddingTop: 8 }}>
            <div />
            {EVENTS.map((ev) => (
              <div key={ev.key} style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, textAlign: 'center', lineHeight: 1.5 }}>
                {ev.note}
              </div>
            ))}
          </div>

          <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 10 }}>
            Rouge&nbsp;: delta positif sig. (p&nbsp;{'<'}&nbsp;0,05)&ensp;·&ensp;Bleu&nbsp;: delta négatif sig.&ensp;·&ensp;Gris&nbsp;: non significatif
          </div>
        </div>

        {/* ── Encadré absence de tendance ── */}
        <div style={{ border: `1px solid ${RULE}` }}>
          <div style={{ background: ACCENT, padding: '9px 16px' }}>
            <div style={{ fontFamily: MONO, fontSize: 7.5, color: 'rgba(255,255,255,0.85)', textTransform: 'uppercase', letterSpacing: '0.16em', fontWeight: 700 }}>
              À retenir
            </div>
          </div>
          <div style={{ padding: '18px 16px' }}>
            <div style={{ fontFamily: SANS, fontSize: 14, fontWeight: 700, color: INK, lineHeight: 1.35, marginBottom: 14 }}>
              Aucune tendance lente vers la convergence.
            </div>
            <div style={{ borderTop: `1px solid ${RULE}`, paddingTop: 12, fontFamily: SANS, fontSize: 12, color: MID, lineHeight: 1.6 }}>
              Les Mann-Kendall n&apos;indiquent aucune trajectoire séculaire.
              La Wasserstein oscille sans direction. Le système réagit par chocs,
              puis retourne à l&apos;état initial.
            </div>
          </div>
        </div>

      </div>

      {/* ═══════════════════════════════════════════════════════════
          Second rang : Mann-Kendall + Wasserstein
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18 }}>

        {/* Mann-Kendall */}
        <div style={{ background: FIG_BG, padding: '16px 20px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 14, fontWeight: 700 }}>
            Test Mann-Kendall — absence de tendance séculaire
          </div>
          <div style={{ fontFamily: SANS, fontSize: 11.5, color: MID, marginBottom: 14, lineHeight: 1.5 }}>
            Tau de Kendall par bloc — aucun p&nbsp;{'<'}&nbsp;0,15
          </div>
          {mannKendallByBloc.map((row) => (
            <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '148px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
              <span style={{ fontFamily: SANS, fontSize: 10, color: MID }}>
                {blocLabels[row.bloc]}
              </span>
              <div style={{ position: 'relative', height: 14 }}>
                <div style={{ position: 'absolute', left: '50%', top: -2, bottom: -2, width: 1.5, backgroundColor: DIM, opacity: 0.35 }} />
                <div style={{
                  position: 'absolute', top: 0, bottom: 0,
                  left:  row.tau >= 0 ? '50%' : `calc(50% - ${(Math.abs(row.tau) / 0.25) * 50}%)`,
                  width: `${(Math.abs(row.tau) / 0.25) * 50}%`,
                  backgroundColor: '#AAAAAA',
                }} />
              </div>
              <span style={{ fontFamily: MONO, fontSize: 9.5, color: DIM, textAlign: 'right' }}>
                {signed(row.tau, 2)}
              </span>
            </div>
          ))}
          <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 6 }}>
            Aucun tau significatif — pas de trajectoire lente
          </div>
        </div>

        {/* Wasserstein drift */}
        <div style={{ background: FIG_BG, padding: '16px 20px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 14, fontWeight: 700 }}>
            Distance de Wasserstein — oscillation irrégulière
          </div>
          <div style={{ fontFamily: SANS, fontSize: 11.5, color: MID, marginBottom: 14, lineHeight: 1.5 }}>
            Distance lexicale moyenne inter-blocs — pas de convergence
          </div>
          {wassersteinDriftSnapshots.map((snap) => {
            const avg = (snap.gaucheRadicale + snap.gaucheModeree + snap.centreMajorite + snap.droite) / 4;
            const hot = avg > 0.12;
            return (
              <div key={snap.month} style={{ display: 'grid', gridTemplateColumns: '72px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: MONO, fontSize: 8.5, color: INK }}>{snap.month}</span>
                <div style={{ position: 'relative', height: 14 }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: 'rgba(0,0,0,0.07)' }} />
                  <div style={{ position: 'absolute', top: 0, left: 0, bottom: 0, width: `${(avg / maxWd) * 100}%`, backgroundColor: hot ? ACCENT : '#2055A5' }} />
                </div>
                <span style={{ fontFamily: MONO, fontSize: 9.5, fontWeight: hot ? 700 : 400, color: hot ? ACCENT : DIM, textAlign: 'right' }}>
                  {avg.toFixed(3)}
                </span>
              </div>
            );
          })}
          <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 6 }}>
            Oscillation sans pente — pas de convergence inter-blocs
          </div>
        </div>

      </div>
    </section>
  );
}
