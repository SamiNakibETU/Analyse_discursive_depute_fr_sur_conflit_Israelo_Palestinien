/**
 * DIRECTION C — Données brutes contrastées (Data journalism bold)
 * Bandeaux sombres (#141414) par figure, barres très épaisses (52px),
 * valeurs imprimées DANS les barres, couleurs blocs pleine saturation.
 * Impact immédiat, lecture en 3 secondes.
 */
import {
  affectiveGap,
  blocLabels,
  effectiveDimensionalitySeries,
  emotionalRegisterByBloc,
  entropicPolarizationSeries,
  eventImpact,
  frameRows,
  lexicalContrast,
  mannKendallByBloc,
  registerPositionCorrelation,
  tweetsPerDeputy,
  twitterVsAnByBloc,
  visibilityByQuintile,
  wassersteinDriftSnapshots,
} from '../data/article1';

/* ── Palette ─────────────────────────────────────────────────────── */
const DARK = '#141414';
const ACC  = '#C8102E';
const INK  = '#141414';
const MID  = '#4A4A4A';
const DIM  = '#888888';
const RL   = '#E0E0E0';
const LITE = '#F8F8F8';

const MO = '"IBM Plex Mono", monospace';
const SA = '"IBM Plex Sans", sans-serif';
const MA = '"Mattone", sans-serif';

/* ── Couleurs ────────────────────────────────────────────────────── */
const FC = { HUM: '#1D4ED8', SEC: '#C8102E', MOR: '#64748B', OTH: '#CBD5E1' } as const;
const FL = { HUM: 'Humanitaire', SEC: 'Sécuritaire', MOR: 'Moral', OTH: 'Autres' } as const;
const SG = ['HUM', 'SEC', 'MOR', 'OTH'] as const;
type Sg = (typeof SG)[number];
type FR = (typeof frameRows)[0];
const domFR = (row: FR) => SG.map((k) => ({ k, v: row[k] })).reduce((a, b) => b.v > a.v ? b : a);

const BF: Record<string, string> = {
  'Gauche radicale': '#B91C1C', 'Gauche moderee': '#C2410C',
  'Centre / Majorite': '#1D4ED8', 'Droite': '#1E3A8A',
};
const BL: Record<string, string> = {
  'Gauche radicale': 'Gauche radicale', 'Gauche moderee': 'Gauche modérée',
  'Centre / Majorite': 'Centre / Majorité', 'Droite': 'Droite',
};
const EL: Record<string, string> = {
  indignation:'Indignation', solidarite:'Solidarité', neutral:'Neutre',
  grief:'Tristesse', anger:'Colère', defiance:'Défiance', fear:'Peur',
};

const PAIRS = [
  { g:'gaza', d:'hamas' }, { g:'génocide', d:'terroristes' }, { g:'massacres', d:'antisémitisme' },
];
const EVENTS = [
  { key:'CIJ (janv. 2024)', lb:'CIJ', dt:'janv. 2024', note:'Aucun effet sig.' },
  { key:'Rafah (mai 2024)', lb:'Rafah', dt:'mai 2024', note:'G. modérée + Centre' },
  { key:'Cessez-le-feu (janv. 2025)', lb:'Cessez-le-feu', dt:'janv. 2025', note:'Mouvement max' },
] as const;
const BLOCS = ['Gauche radicale','Gauche moderee','Centre / Majorite','Droite'] as const;

const signed = (n: number, d = 2) => n >= 0 ? `+${n.toFixed(d)}` : n.toFixed(d);
const maxTw  = Math.max(...tweetsPerDeputy.map((d) => d.value));
const maxVis = Math.max(...visibilityByQuintile.map((d) => d.value));
const maxDlt = Math.max(...twitterVsAnByBloc.map((d) => Math.abs(d.delta)));
const maxEv  = Math.max(...eventImpact.map((d) => Math.abs(d.delta)));
const maxWd  = Math.max(...wassersteinDriftSnapshots.flatMap((d) => [d.gaucheRadicale, d.gaucheModeree, d.centreMajorite, d.droite]));
const maxZ   = Math.max(...['gaza','génocide','massacres'].flatMap((w) => [
  lexicalContrast.gauche.find((d) => d.word === w)?.z ?? 0,
  lexicalContrast.droite.find((d) => d.word === { 'gaza':'hamas','génocide':'terroristes','massacres':'antisémitisme' }[w])?.z ?? 0,
]));

/* ── Sous-composant : bandeau sombre ─────────────────────────────── */
function DarkHeader({ label }: { label: string }) {
  return (
    <div style={{ background: DARK, padding: '10px 18px', marginBottom: 0 }}>
      <div style={{ fontFamily: MO, fontSize: 8, color: 'rgba(255,255,255,0.65)', textTransform: 'uppercase', letterSpacing: '0.16em', fontWeight: 700 }}>
        {label}
      </div>
    </div>
  );
}

/* ─────────────── EXPORTS ─────────────────────────────────────────── */

export function C_Frames() {
  return (
    <div>
      {/* Barres empilées épaisses */}
      <div style={{ marginBottom: 20 }}>
        <DarkHeader label="Cadres discursifs — % des interventions par bloc" />
        <div style={{ background: LITE }}>
          {frameRows.map((row) => {
            const dom = domFR(row);
            let acc = 0;
            return (
              <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '190px 1fr', alignItems: 'center', borderBottom: `1px solid ${RL}` }}>
                <div style={{ padding: '14px 18px' }}>
                  <div style={{ fontFamily: SA, fontSize: 12, fontWeight: 700, color: INK, marginBottom: 3 }}>{blocLabels[row.bloc]}</div>
                  <div style={{ fontFamily: MA, fontSize: 22, fontWeight: 900, color: dom.k === 'HUM' ? FC.HUM : dom.k === 'SEC' ? FC.SEC : DIM, letterSpacing: '-0.02em', lineHeight: 1 }}>
                    {Math.round(dom.v)}%
                  </div>
                  <div style={{ fontFamily: MO, fontSize: 7.5, color: dom.k === 'HUM' ? FC.HUM : dom.k === 'SEC' ? FC.SEC : DIM, textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: 2 }}>
                    {FL[dom.k as Sg]}
                  </div>
                </div>
                <div style={{ position: 'relative', height: 52 }}>
                  {SG.map((k) => {
                    const sl = acc; const w = row[k]; acc += w;
                    return (
                      <div key={k} style={{ position: 'absolute', left: `${sl}%`, width: `${w}%`, top: 0, bottom: 0, backgroundColor: FC[k], display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
                        {w > 10 && (
                          <span style={{ fontFamily: MO, fontSize: w > 22 ? 11 : 9, fontWeight: 700, color: k === 'OTH' ? MID : 'rgba(255,255,255,0.95)', whiteSpace: 'nowrap' }}>
                            {Math.round(w)}%
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
        <div style={{ background: DARK, padding: '6px 18px', display: 'flex', gap: 24 }}>
          {SG.map((k) => (
            <span key={k} style={{ display: 'flex', alignItems: 'center', gap: 6, fontFamily: MO, fontSize: 7, color: 'rgba(255,255,255,0.6)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              <span style={{ width: 8, height: 8, backgroundColor: FC[k], display: 'inline-block' }} /> {FL[k as Sg]}
            </span>
          ))}
          <span style={{ fontFamily: MO, fontSize: 7, color: 'rgba(255,255,255,0.4)', marginLeft: 'auto' }}>ρ registre ↔ position = {registerPositionCorrelation.toFixed(3)}</span>
        </div>
      </div>

      {/* Butterfly */}
      <div>
        <DarkHeader label="Mots discriminants — score Z normalisé" />
        <div style={{ background: LITE, padding: '18px 20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr 1fr 120px', alignItems: 'center', marginBottom: 12 }}>
            <div style={{ fontFamily: SA, fontSize: 11, fontWeight: 700, color: FC.HUM, textAlign: 'right', paddingRight: 12 }}>Gauche</div>
            <div /><div />
            <div style={{ fontFamily: SA, fontSize: 11, fontWeight: 700, color: FC.SEC, paddingLeft: 12 }}>Droite</div>
          </div>
          {PAIRS.map(({ g, d }) => {
            const lw = lexicalContrast.gauche.find((x) => x.word === g);
            const rw = lexicalContrast.droite.find((x) => x.word === d);
            if (!lw || !rw) return null;
            return (
              <div key={g} style={{ display: 'grid', gridTemplateColumns: '120px 1fr 2px 1fr 120px', alignItems: 'center', marginBottom: 14 }}>
                <span style={{ fontFamily: MA, fontSize: 18, fontWeight: 900, color: FC.HUM, textAlign: 'right', paddingRight: 14 }}>{lw.word}</span>
                <div style={{ height: 32, display: 'flex', justifyContent: 'flex-end' }}>
                  <div style={{ width: `${(lw.z / maxZ) * 100}%`, height: '100%', backgroundColor: FC.HUM }} />
                </div>
                <div style={{ background: DARK, alignSelf: 'stretch' }} />
                <div style={{ height: 32 }}>
                  <div style={{ width: `${(rw.z / maxZ) * 100}%`, height: '100%', backgroundColor: FC.SEC }} />
                </div>
                <span style={{ fontFamily: MA, fontSize: 18, fontWeight: 900, color: FC.SEC, paddingLeft: 14 }}>{rw.word}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function C_Visibility() {
  return (
    <div>
      {/* Tweets — barres très épaisses */}
      <div style={{ marginBottom: 20 }}>
        <DarkHeader label="Tweets publiés par député — moyenne par bloc politique" />
        <div style={{ background: LITE }}>
          {tweetsPerDeputy.map((row, idx) => {
            const fill = BF[row.bloc] ?? DIM;
            const isMx = idx === 0;
            const barH = isMx ? 60 : 40;
            const pct  = (row.value / maxTw) * 100;
            return (
              <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '190px 1fr', alignItems: 'center', borderBottom: `1px solid ${RL}` }}>
                <div style={{ padding: '12px 18px' }}>
                  <div style={{ fontFamily: SA, fontSize: 12, fontWeight: isMx ? 700 : 600, color: INK }}>{blocLabels[row.bloc]}</div>
                </div>
                <div style={{ position: 'relative', height: barH, display: 'flex', alignItems: 'center' }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: `${fill}18` }} />
                  <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${pct}%`, backgroundColor: fill, display: 'flex', alignItems: 'center', justifyContent: 'flex-end', paddingRight: 12, overflow: 'hidden' }}>
                    {pct > 20 && <span style={{ fontFamily: MA, fontSize: isMx ? 28 : 20, fontWeight: 900, color: '#fff', letterSpacing: '-0.03em', whiteSpace: 'nowrap' }}>{Math.round(row.value)}</span>}
                  </div>
                  {pct <= 20 && (
                    <div style={{ position: 'absolute', left: `${pct + 2}%`, fontFamily: MA, fontSize: 20, fontWeight: 900, color: fill }}>{Math.round(row.value)}</div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
        <div style={{ background: DARK, padding: '8px 18px', display: 'flex', gap: 8, alignItems: 'center' }}>
          <span style={{ fontFamily: MA, fontSize: 20, fontWeight: 900, color: '#fff' }}>×7</span>
          <span style={{ fontFamily: MO, fontSize: 8, color: 'rgba(255,255,255,0.6)' }}>LFI vs Centre · 122 tweets vs 17</span>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div>
          <DarkHeader label="|stance| par quintile de visibilité Twitter" />
          <div style={{ background: LITE, padding: '16px 18px' }}>
            {visibilityByQuintile.map((row, idx) => {
              const isTop = idx === visibilityByQuintile.length - 1;
              const pct   = (row.value / maxVis) * 100;
              const fill  = isTop ? ACC : BF['Centre / Majorite'];
              return (
                <div key={row.quintile} style={{ display: 'grid', gridTemplateColumns: '140px 1fr', alignItems: 'center', marginBottom: 10 }}>
                  <span style={{ fontFamily: SA, fontSize: 10, color: isTop ? INK : MID, fontWeight: isTop ? 700 : 400 }}>{row.quintile}</span>
                  <div style={{ position: 'relative', height: 26, display: 'flex', alignItems: 'center' }}>
                    <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${pct}%`, backgroundColor: fill, display: 'flex', alignItems: 'center', justifyContent: 'flex-end', paddingRight: 8, overflow: 'hidden' }}>
                      <span style={{ fontFamily: MO, fontSize: 10, fontWeight: 700, color: '#fff', whiteSpace: 'nowrap' }}>{row.value.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <div>
          <DarkHeader label="Delta stance Twitter − AN (rouge = p < 0,05)" />
          <div style={{ background: LITE, padding: '16px 18px' }}>
            {twitterVsAnByBloc.map((row) => {
              const sig  = row.significant;
              const pct  = (Math.abs(row.delta) / maxDlt) * 50;
              const fill = sig ? BF[row.bloc] ?? ACC : '#CCCCCC';
              return (
                <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '148px 1fr 52px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                  <span style={{ fontFamily: SA, fontSize: 10, color: sig ? INK : MID, fontWeight: sig ? 700 : 400 }}>{blocLabels[row.bloc]}</span>
                  <div style={{ position: 'relative', height: 22 }}>
                    <div style={{ position: 'absolute', left: '50%', top: -2, bottom: -2, width: 2, backgroundColor: DARK }} />
                    <div style={{ position: 'absolute', top: 0, bottom: 0, left: row.delta >= 0 ? '50%' : `calc(50% - ${pct}%)`, width: `${pct}%`, backgroundColor: fill }} />
                  </div>
                  <span style={{ fontFamily: MO, fontSize: 11, fontWeight: 700, color: sig ? fill : DIM, textAlign: 'right' }}>{signed(row.delta, 2)}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export function C_Rhythms() {
  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <DarkHeader label="Réaction aux événements — delta de stance par bloc (centré zéro)" />
        <div style={{ background: LITE, padding: '16px 18px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '158px 1fr 1fr 1fr', gap: 10, marginBottom: 10 }}>
            <div />
            {EVENTS.map((ev) => (
              <div key={ev.key} style={{ textAlign: 'center' }}>
                <div style={{ fontFamily: SA, fontSize: 12, fontWeight: 700, color: INK }}>{ev.lb}</div>
                <div style={{ fontFamily: MO, fontSize: 7.5, color: DIM }}>{ev.dt}</div>
              </div>
            ))}
          </div>
          {BLOCS.map((bloc) => (
            <div key={bloc} style={{ display: 'grid', gridTemplateColumns: '158px 1fr 1fr 1fr', gap: 10, alignItems: 'center', borderTop: `1px solid ${RL}`, padding: '12px 0' }}>
              <span style={{ fontFamily: SA, fontSize: 11, fontWeight: 600, color: INK }}>{blocLabels[bloc]}</span>
              {EVENTS.map((ev) => {
                const row = eventImpact.find((d) => d.event === ev.key && d.bloc === bloc);
                if (!row) return <div key={ev.key} />;
                const sig = row.p < 0.05;
                const bp  = (Math.abs(row.delta) / maxEv) * 46;
                const bc  = sig ? (row.delta > 0 ? ACC : BF['Droite']) : '#CCCCCC';
                return (
                  <div key={ev.key} style={{ position: 'relative', height: 48 }}>
                    <div style={{ position: 'absolute', left: '50%', top: 0, height: 32, width: 2, backgroundColor: DARK, opacity: 0.3 }} />
                    <div style={{ position: 'absolute', top: 7, height: 20, left: row.delta >= 0 ? '50%' : `calc(50% - ${bp}%)`, width: `${bp}%`, backgroundColor: bc, display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
                      {bp > 14 && <span style={{ fontFamily: MO, fontSize: 8, fontWeight: 700, color: '#fff' }}>{signed(row.delta, 2)}</span>}
                    </div>
                    {bp <= 14 && <div style={{ position: 'absolute', bottom: 2, width: '100%', textAlign: 'center', fontFamily: MO, fontSize: 8, color: bc }}>{signed(row.delta, 2)}</div>}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
        <div style={{ background: DARK, padding: '6px 18px', display: 'flex', gap: 24 }}>
          {EVENTS.map((ev) => (
            <span key={ev.key} style={{ fontFamily: MO, fontSize: 7.5, color: 'rgba(255,255,255,0.6)' }}>{ev.lb} — {ev.note}</span>
          ))}
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div>
          <DarkHeader label="Mann-Kendall tau — aucune tendance séculaire" />
          <div style={{ background: LITE, padding: '16px 18px' }}>
            {mannKendallByBloc.map((row) => (
              <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '148px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: SA, fontSize: 10, color: MID }}>{blocLabels[row.bloc]}</span>
                <div style={{ position: 'relative', height: 18 }}>
                  <div style={{ position: 'absolute', left: '50%', top: -2, bottom: -2, width: 2, backgroundColor: DARK }} />
                  <div style={{ position: 'absolute', top: 0, bottom: 0, left: row.tau >= 0 ? '50%' : `calc(50% - ${(Math.abs(row.tau) / 0.25) * 50}%)`, width: `${(Math.abs(row.tau) / 0.25) * 50}%`, backgroundColor: '#AAAAAA' }} />
                </div>
                <span style={{ fontFamily: MO, fontSize: 9.5, color: DIM, textAlign: 'right' }}>{signed(row.tau, 2)}</span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <DarkHeader label="Distance de Wasserstein — oscillation irrégulière" />
          <div style={{ background: LITE, padding: '16px 18px' }}>
            {wassersteinDriftSnapshots.map((snap) => {
              const avg = (snap.gaucheRadicale + snap.gaucheModeree + snap.centreMajorite + snap.droite) / 4;
              const hot = avg > 0.12;
              return (
                <div key={snap.month} style={{ display: 'grid', gridTemplateColumns: '72px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                  <span style={{ fontFamily: MO, fontSize: 8, color: INK }}>{snap.month}</span>
                  <div style={{ position: 'relative', height: 18 }}>
                    <div style={{ position: 'absolute', inset: 0, backgroundColor: `${hot ? ACC : BF['Centre / Majorite']}20` }} />
                    <div style={{ position: 'absolute', top: 0, left: 0, bottom: 0, width: `${(avg / maxWd) * 100}%`, backgroundColor: hot ? ACC : BF['Centre / Majorite'] }} />
                  </div>
                  <span style={{ fontFamily: MO, fontSize: 9, fontWeight: hot ? 700 : 400, color: hot ? ACC : DIM, textAlign: 'right' }}>{avg.toFixed(3)}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export function C_Emotions() {
  const vadS = affectiveGap[0]?.value ?? 0;
  const vadE = affectiveGap[affectiveGap.length - 1]?.value ?? 0;
  const ecS  = entropicPolarizationSeries[0]?.value ?? 0;
  const ecE  = entropicPolarizationSeries[entropicPolarizationSeries.length - 1]?.value ?? 0;
  const edS  = effectiveDimensionalitySeries[0]?.value ?? 0;
  const edE  = effectiveDimensionalitySeries[effectiveDimensionalitySeries.length - 1]?.value ?? 0;
  const SVG_W = 540; const SVG_H = 80;
  const mn = Math.min(...affectiveGap.map((d) => d.value));
  const mx = Math.max(...affectiveGap.map((d) => d.value));
  const pts = affectiveGap.map((d, i) => {
    const x = (i / (affectiveGap.length - 1)) * SVG_W;
    const y = SVG_H - ((d.value - mn) / (mx - mn || 1)) * (SVG_H - 10) - 5;
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  return (
    <div>
      {/* Panneaux : fond couleur bloc + texte blanc */}
      <div style={{ marginBottom: 20 }}>
        <DarkHeader label="Registre émotionnel dominant par bloc — % des interventions" />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 2 }}>
          {(['Gauche radicale','Gauche moderee','Centre / Majorite','Droite'] as const).map((bloc) => {
            const vals = emotionalRegisterByBloc[bloc as keyof typeof emotionalRegisterByBloc];
            const ents = (Object.entries(vals) as [string,number][]).sort((a,b) => b[1]-a[1]);
            const [mk, mv] = ents[0];
            const col = BF[bloc] ?? DIM;
            return (
              <div key={bloc} style={{ background: col, padding: '18px 14px' }}>
                <div style={{ fontFamily: MO, fontSize: 7.5, color: 'rgba(255,255,255,0.7)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 8 }}>{BL[bloc]}</div>
                <div style={{ fontFamily: MA, fontSize: 52, fontWeight: 900, color: '#fff', lineHeight: 0.9, letterSpacing: '-0.03em', marginBottom: 6 }}>
                  {mv.toFixed(0)}%
                </div>
                <div style={{ fontFamily: MO, fontSize: 8.5, color: 'rgba(255,255,255,0.85)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 14 }}>{EL[mk] ?? mk}</div>
                <div style={{ borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: 12 }}>
                  {ents.map(([reg, val]) => (
                    <div key={reg} style={{ display: 'grid', gridTemplateColumns: '1fr 32px', gap: 6, alignItems: 'center', marginBottom: 7 }}>
                      <div>
                        <div style={{ fontFamily: MO, fontSize: 7.5, color: reg === mk ? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.55)', marginBottom: 2 }}>{EL[reg] ?? reg}</div>
                        <div style={{ height: 6 }}>
                          <div style={{ width: `${(val / mv) * 100}%`, height: '100%', backgroundColor: reg === mk ? 'rgba(255,255,255,0.9)' : 'rgba(255,255,255,0.3)' }} />
                        </div>
                      </div>
                      <span style={{ fontFamily: MO, fontSize: 9, color: reg === mk ? '#fff' : 'rgba(255,255,255,0.55)', textAlign: 'right' }}>{val.toFixed(1)}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* VAD + stabilité */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div>
          <DarkHeader label="Gap affectif VAD — montée continue depuis 2023" />
          <div style={{ background: LITE, padding: '16px 18px' }}>
            <svg viewBox={`0 0 ${SVG_W} ${SVG_H}`} style={{ width: '100%', height: SVG_H + 4, display: 'block' }} aria-hidden>
              {[0.25, 0.5, 0.75].map((f) => (
                <line key={f} x1="0" y1={SVG_H * (1 - f)} x2={SVG_W} y2={SVG_H * (1 - f)} stroke={RL} strokeWidth="0.75" />
              ))}
              <line x1="0" y1={SVG_H} x2={SVG_W} y2={SVG_H} stroke={DIM} strokeWidth="1" />
              <path d={pts} fill="none" stroke={ACC} strokeWidth="3.5" strokeLinejoin="round" strokeLinecap="round" />
            </svg>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: MO, fontSize: 8, color: DIM, marginTop: 8 }}>
              <span>oct. 2023 · {vadS.toFixed(3)}</span>
              <span style={{ color: ACC, fontWeight: 700 }}>janv. 2026 · {vadE.toFixed(3)}</span>
            </div>
          </div>
        </div>
        <div>
          <DarkHeader label="Structure stable — Ec et ED inchangés" />
          <div style={{ background: LITE, padding: '20px 18px' }}>
            {[['Entropie Ec', ecS, ecE],['Dim. effective ED', edS, edE]].map(([lb, s, e]) => (
              <div key={String(lb)} style={{ borderBottom: `1px solid ${RL}`, paddingBottom: 16, marginBottom: 16 }}>
                <div style={{ fontFamily: MO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 8 }}>{lb}</div>
                <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                  <div style={{ fontFamily: MA, fontSize: 30, fontWeight: 900, color: INK, letterSpacing: '-0.02em' }}>{Number(s).toFixed(3)}</div>
                  <div style={{ fontFamily: MO, fontSize: 18, color: DIM }}>→</div>
                  <div style={{ fontFamily: MA, fontSize: 30, fontWeight: 900, color: INK, letterSpacing: '-0.02em' }}>{Number(e).toFixed(3)}</div>
                </div>
              </div>
            ))}
            <div style={{ fontFamily: SA, fontSize: 12, color: MID, lineHeight: 1.6 }}>
              La structure du désaccord reste intacte. Seule l&apos;intensité émotionnelle monte.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
