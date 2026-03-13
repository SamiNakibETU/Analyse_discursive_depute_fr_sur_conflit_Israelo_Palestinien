/**
 * DIRECTION B — Minimalisme typographique (Swiss / Groot)
 * Fond blanc pur, règles noires, GRANDS NOMBRES Mattone comme ancre visuelle,
 * barres fines (14px), MONO partout, une seule couleur accent.
 * Le chiffre EST le graphique.
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

/* ── Palette radicalement réduite ───────────────────────────────── */
const ACC = '#C8102E';         /* unique couleur accent */
const INK = '#0A0A0A';
const MID = '#444444';
const DIM = '#999999';
const RL  = '#E2E2E2';

const MO = '"IBM Plex Mono", monospace';
const SA = '"IBM Plex Sans", sans-serif';
const MA = '"Mattone", sans-serif';

/* ── Données ─────────────────────────────────────────────────────── */
const FC = { HUM: '#2055A5', SEC: '#C8102E', MOR: '#888888', OTH: '#CCCCCC' } as const;
const FL = { HUM: 'Humanitaire', SEC: 'Sécuritaire', MOR: 'Moral', OTH: 'Autres' } as const;
const SG = ['HUM', 'SEC', 'MOR', 'OTH'] as const;
type FR = (typeof frameRows)[0];
type Sg = (typeof SG)[number];
const domFR = (row: FR) => SG.map((k) => ({ k, v: row[k] })).reduce((a, b) => b.v > a.v ? b : a);

const BF: Record<string, string> = {
  'Gauche radicale': '#C8102E', 'Gauche moderee': '#D4623A',
  'Centre / Majorite': '#2055A5', 'Droite': '#1A3F6E',
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
  { key:'CIJ (janv. 2024)', lb:'CIJ', dt:'janv. 2024' },
  { key:'Rafah (mai 2024)', lb:'Rafah', dt:'mai 2024' },
  { key:'Cessez-le-feu (janv. 2025)', lb:'Cessez-le-feu', dt:'janv. 2025' },
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

/* ── Sous-composant : titre de section chart ─────────────────────── */
function ChLabel({ text }: { text: string }) {
  return (
    <div style={{ fontFamily: MO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.16em', marginBottom: 20, fontWeight: 700 }}>
      {text}
    </div>
  );
}

/* ─────────────── EXPORTS ─────────────────────────────────────────── */

export function B_Frames() {
  return (
    <div>
      {/* Cadres : GRAND NOMBRE + barre fine */}
      <div style={{ borderTop: `3px solid ${INK}`, paddingTop: 22, marginBottom: 32 }}>
        <ChLabel text="Cadres discursifs — % des interventions par bloc" />
        {frameRows.map((row) => {
          const dom = domFR(row);
          const domCol = dom.k === 'HUM' ? FC.HUM : dom.k === 'SEC' ? FC.SEC : DIM;
          let acc = 0;
          return (
            <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '100px 1fr 200px', alignItems: 'center', gap: 0, borderBottom: `1px solid ${RL}`, paddingBottom: 18, marginBottom: 18 }}>
              {/* Ancre numérique */}
              <div>
                <div style={{ fontFamily: MA, fontSize: 64, fontWeight: 900, color: domCol, lineHeight: 0.9, letterSpacing: '-0.03em' }}>
                  {Math.round(dom.v)}%
                </div>
                <div style={{ fontFamily: MO, fontSize: 7.5, color: domCol, textTransform: 'uppercase', letterSpacing: '0.1em', marginTop: 6 }}>
                  {FL[dom.k as Sg]}
                </div>
              </div>

              {/* Barre fine empilée */}
              <div style={{ paddingLeft: 24 }}>
                <div style={{ position: 'relative', height: 14, marginBottom: 8 }}>
                  {SG.map((k) => {
                    const sl = acc; const w = row[k]; acc += w;
                    return (
                      <div key={k} style={{ position: 'absolute', left: `${sl}%`, width: `${w}%`, top: 0, bottom: 0, backgroundColor: k === dom.k ? domCol : '#DDDDDD' }} />
                    );
                  })}
                </div>
                {/* mini légende */}
                <div style={{ display: 'flex', gap: 14 }}>
                  {SG.map((k) => (
                    <span key={k} style={{ fontFamily: MO, fontSize: 7, color: k === dom.k ? domCol : DIM }}>
                      {Math.round(row[k])}% {FL[k as Sg].slice(0,3).toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>

              {/* Bloc */}
              <div style={{ paddingLeft: 24, borderLeft: `2px solid ${RL}` }}>
                <div style={{ fontFamily: SA, fontSize: 13, fontWeight: 700, color: INK }}>{blocLabels[row.bloc]}</div>
              </div>
            </div>
          );
        })}
        {/* ρ inline */}
        <div style={{ display: 'flex', gap: 24, alignItems: 'baseline', marginTop: 8 }}>
          <div style={{ fontFamily: MA, fontSize: 36, fontWeight: 900, color: INK, letterSpacing: '-0.03em' }}>
            ρ&nbsp;=&nbsp;{registerPositionCorrelation.toFixed(3)}
          </div>
          <div style={{ fontFamily: SA, fontSize: 12, color: MID }}>Le registre discursif ne prédit pas la position politique.</div>
        </div>
      </div>

      {/* Butterfly : architecture typographique pure */}
      <div style={{ borderTop: `1px solid ${INK}`, paddingTop: 22, marginBottom: 32 }}>
        <ChLabel text="Mots discriminants — score Z par camp" />
        {PAIRS.map(({ g, d }) => {
          const lw = lexicalContrast.gauche.find((x) => x.word === g);
          const rw = lexicalContrast.droite.find((x) => x.word === d);
          if (!lw || !rw) return null;
          return (
            <div key={g} style={{ display: 'grid', gridTemplateColumns: '140px 1fr 2px 1fr 140px', alignItems: 'center', marginBottom: 18 }}>
              <span style={{ fontFamily: MA, fontSize: 20, fontWeight: 900, color: FC.HUM, textAlign: 'right', paddingRight: 16 }}>{lw.word}</span>
              <div style={{ height: 14, display: 'flex', justifyContent: 'flex-end' }}>
                <div style={{ width: `${(lw.z / maxZ) * 100}%`, height: '100%', backgroundColor: FC.HUM }} />
              </div>
              <div style={{ background: INK, alignSelf: 'stretch' }} />
              <div style={{ height: 14 }}>
                <div style={{ width: `${(rw.z / maxZ) * 100}%`, height: '100%', backgroundColor: ACC }} />
              </div>
              <span style={{ fontFamily: MA, fontSize: 20, fontWeight: 900, color: ACC, paddingLeft: 16 }}>{rw.word}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function B_Visibility() {
  return (
    <div>
      <div style={{ borderTop: `3px solid ${INK}`, paddingTop: 22, marginBottom: 32 }}>
        <ChLabel text="Tweets par député — moyenne par bloc" />
        {tweetsPerDeputy.map((row, idx) => {
          const isMx = idx === 0;
          const col  = isMx ? ACC : DIM;
          return (
            <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '80px 1fr 180px', alignItems: 'center', borderBottom: `1px solid ${RL}`, paddingBottom: 14, marginBottom: 14 }}>
              <div style={{ fontFamily: MA, fontSize: isMx ? 52 : 36, fontWeight: 900, color: col, letterSpacing: '-0.04em', lineHeight: 0.9 }}>
                {Math.round(row.value)}
              </div>
              <div style={{ paddingLeft: 20 }}>
                <div style={{ position: 'relative', height: isMx ? 16 : 10, marginBottom: 6 }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: '#EEEEEE' }} />
                  <div style={{ position: 'absolute', inset: 0, width: `${(row.value / maxTw) * 100}%`, backgroundColor: col }} />
                </div>
                <div style={{ fontFamily: MO, fontSize: 7.5, color: DIM }}>tweets/député</div>
              </div>
              <div style={{ paddingLeft: 24, borderLeft: `2px solid ${RL}` }}>
                <div style={{ fontFamily: SA, fontSize: 13, fontWeight: isMx ? 700 : 400, color: INK }}>{blocLabels[row.bloc]}</div>
              </div>
            </div>
          );
        })}
        <div style={{ marginTop: 12, display: 'flex', gap: 24, alignItems: 'baseline' }}>
          <div style={{ fontFamily: MA, fontSize: 48, fontWeight: 900, color: INK, letterSpacing: '-0.04em' }}>×7</div>
          <div style={{ fontFamily: SA, fontSize: 12, color: MID }}>LFI vs Centre. L&apos;illusion d&apos;unanimité est produite par la suractivité d&apos;un seul camp.</div>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, borderTop: `1px solid ${INK}`, paddingTop: 22 }}>
        <div>
          <ChLabel text="|stance| par quintile de visibilité Twitter" />
          {visibilityByQuintile.map((row, idx) => {
            const isT = idx === visibilityByQuintile.length - 1;
            return (
              <div key={row.quintile} style={{ display: 'grid', gridTemplateColumns: '130px 1fr 44px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: MO, fontSize: 9.5, color: isT ? INK : DIM, fontWeight: isT ? 700 : 400 }}>{row.quintile}</span>
                <div style={{ position: 'relative', height: 10 }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: '#EEEEEE' }} />
                  <div style={{ position: 'absolute', inset: 0, width: `${(row.value / maxVis) * 100}%`, backgroundColor: isT ? ACC : '#CCCCCC' }} />
                </div>
                <span style={{ fontFamily: MO, fontSize: 11, fontWeight: 700, color: isT ? ACC : DIM, textAlign: 'right' }}>{row.value.toFixed(2)}</span>
              </div>
            );
          })}
        </div>
        <div>
          <ChLabel text="Delta stance Twitter − AN (rouge = p < 0,05)" />
          {twitterVsAnByBloc.map((row) => {
            const sig = row.significant;
            const pct = (Math.abs(row.delta) / maxDlt) * 50;
            return (
              <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '140px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: MO, fontSize: 9.5, color: sig ? INK : DIM, fontWeight: sig ? 700 : 400 }}>{blocLabels[row.bloc]}</span>
                <div style={{ position: 'relative', height: 10 }}>
                  <div style={{ position: 'absolute', left: '50%', top: -2, bottom: -2, width: 1.5, backgroundColor: INK }} />
                  <div style={{ position: 'absolute', top: 0, bottom: 0, left: row.delta >= 0 ? '50%' : `calc(50% - ${pct}%)`, width: `${pct}%`, backgroundColor: sig ? ACC : '#CCCCCC' }} />
                </div>
                <span style={{ fontFamily: MO, fontSize: 11, fontWeight: 700, color: sig ? ACC : DIM, textAlign: 'right' }}>{signed(row.delta, 2)}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function B_Rhythms() {
  return (
    <div>
      <div style={{ borderTop: `3px solid ${INK}`, paddingTop: 22, marginBottom: 32 }}>
        <ChLabel text="Réaction aux événements — delta de stance par bloc (centré zéro)" />
        <div style={{ display: 'grid', gridTemplateColumns: '148px 1fr 1fr 1fr', gap: 10 }}>
          <div />
          {EVENTS.map((ev) => (
            <div key={ev.key} style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: SA, fontSize: 12, fontWeight: 700, color: INK }}>{ev.lb}</div>
              <div style={{ fontFamily: MO, fontSize: 8, color: DIM }}>{ev.dt}</div>
            </div>
          ))}
        </div>
        {BLOCS.map((bloc) => (
          <div key={bloc} style={{ display: 'grid', gridTemplateColumns: '148px 1fr 1fr 1fr', gap: 10, alignItems: 'center', borderTop: `1px solid ${RL}`, paddingTop: 12, marginTop: 12 }}>
            <span style={{ fontFamily: SA, fontSize: 11, fontWeight: 600, color: INK }}>{blocLabels[bloc]}</span>
            {EVENTS.map((ev) => {
              const row = eventImpact.find((d) => d.event === ev.key && d.bloc === bloc);
              if (!row) return <div key={ev.key} />;
              const sig = row.p < 0.05;
              const bp  = (Math.abs(row.delta) / maxEv) * 46;
              const bc  = sig ? (row.delta > 0 ? ACC : '#1A3F6E') : '#DDDDDD';
              return (
                <div key={ev.key} style={{ position: 'relative', height: 42 }}>
                  <div style={{ position: 'absolute', left: '50%', top: 0, height: 28, width: 1, backgroundColor: INK, opacity: 0.3 }} />
                  <div style={{ position: 'absolute', top: 7, height: 14, left: row.delta >= 0 ? '50%' : `calc(50% - ${bp}%)`, width: `${bp}%`, backgroundColor: bc }} />
                  <div style={{ position: 'absolute', bottom: 0, width: '100%', textAlign: 'center', fontFamily: MO, fontSize: 9, fontWeight: sig ? 700 : 400, color: sig ? bc : DIM }}>
                    {signed(row.delta, 2)}
                  </div>
                </div>
              );
            })}
          </div>
        ))}
        <div style={{ marginTop: 20, display: 'flex', gap: 24, alignItems: 'baseline', borderTop: `1px solid ${RL}`, paddingTop: 16 }}>
          <div style={{ fontFamily: MA, fontSize: 28, fontWeight: 900, color: INK }}>0 tendance</div>
          <div style={{ fontFamily: SA, fontSize: 12, color: MID }}>Aucun Mann-Kendall significatif. Wasserstein sans direction. Chocs ponctuels, retour au statu quo.</div>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, borderTop: `1px solid ${RL}`, paddingTop: 22 }}>
        <div>
          <ChLabel text="Mann-Kendall tau — aucune tendance séculaire" />
          {mannKendallByBloc.map((row) => (
            <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '140px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
              <span style={{ fontFamily: MO, fontSize: 9.5, color: DIM }}>{blocLabels[row.bloc]}</span>
              <div style={{ position: 'relative', height: 10 }}>
                <div style={{ position: 'absolute', left: '50%', top: -1, bottom: -1, width: 1, backgroundColor: INK }} />
                <div style={{ position: 'absolute', top: 0, bottom: 0, left: row.tau >= 0 ? '50%' : `calc(50% - ${(Math.abs(row.tau) / 0.25) * 50}%)`, width: `${(Math.abs(row.tau) / 0.25) * 50}%`, backgroundColor: '#CCCCCC' }} />
              </div>
              <span style={{ fontFamily: MO, fontSize: 9.5, color: DIM, textAlign: 'right' }}>{signed(row.tau, 2)}</span>
            </div>
          ))}
        </div>
        <div>
          <ChLabel text="Distance de Wasserstein — oscillation sans direction" />
          {wassersteinDriftSnapshots.map((snap) => {
            const avg = (snap.gaucheRadicale + snap.gaucheModeree + snap.centreMajorite + snap.droite) / 4;
            return (
              <div key={snap.month} style={{ display: 'grid', gridTemplateColumns: '64px 1fr 54px', gap: 8, alignItems: 'center', marginBottom: 10 }}>
                <span style={{ fontFamily: MO, fontSize: 8, color: DIM }}>{snap.month}</span>
                <div style={{ position: 'relative', height: 10 }}>
                  <div style={{ position: 'absolute', inset: 0, backgroundColor: '#EEEEEE' }} />
                  <div style={{ position: 'absolute', top: 0, left: 0, bottom: 0, width: `${(avg / maxWd) * 100}%`, backgroundColor: '#AAAAAA' }} />
                </div>
                <span style={{ fontFamily: MO, fontSize: 9, color: DIM, textAlign: 'right' }}>{avg.toFixed(3)}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function B_Emotions() {
  const vadS = affectiveGap[0]?.value ?? 0;
  const vadE = affectiveGap[affectiveGap.length - 1]?.value ?? 0;
  const ecS  = entropicPolarizationSeries[0]?.value ?? 0;
  const ecE  = entropicPolarizationSeries[entropicPolarizationSeries.length - 1]?.value ?? 0;
  const edS  = effectiveDimensionalitySeries[0]?.value ?? 0;
  const edE  = effectiveDimensionalitySeries[effectiveDimensionalitySeries.length - 1]?.value ?? 0;
  const SVG_W = 560; const SVG_H = 70;
  const mn = Math.min(...affectiveGap.map((d) => d.value));
  const mx = Math.max(...affectiveGap.map((d) => d.value));
  const pts = affectiveGap.map((d, i) => {
    const x = (i / (affectiveGap.length - 1)) * SVG_W;
    const y = SVG_H - ((d.value - mn) / (mx - mn || 1)) * (SVG_H - 10) - 5;
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  return (
    <div>
      {/* 4 blocs côte à côte : grand nombre + barres fines */}
      <div style={{ borderTop: `3px solid ${INK}`, paddingTop: 22, marginBottom: 32 }}>
        <ChLabel text="Registre émotionnel dominant — % des interventions par bloc" />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 2 }}>
          {(['Gauche radicale','Gauche moderee','Centre / Majorite','Droite'] as const).map((bloc) => {
            const vals = emotionalRegisterByBloc[bloc as keyof typeof emotionalRegisterByBloc];
            const ents = (Object.entries(vals) as [string,number][]).sort((a,b) => b[1]-a[1]);
            const [mk, mv] = ents[0];
            const col = BF[bloc] ?? DIM;
            return (
              <div key={bloc} style={{ borderTop: `2px solid ${INK}`, paddingTop: 14, paddingRight: 16 }}>
                <div style={{ fontFamily: MO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 10 }}>{BL[bloc]}</div>
                <div style={{ fontFamily: MA, fontSize: 56, fontWeight: 900, color: col, lineHeight: 0.9, letterSpacing: '-0.03em', marginBottom: 6 }}>
                  {mv.toFixed(0)}%
                </div>
                <div style={{ fontFamily: MO, fontSize: 8, color: col, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: 14 }}>{EL[mk] ?? mk}</div>
                {ents.map(([reg, val]) => (
                  <div key={reg} style={{ display: 'grid', gridTemplateColumns: '1fr 36px', gap: 6, alignItems: 'center', marginBottom: 6 }}>
                    <div>
                      <div style={{ fontFamily: MO, fontSize: 7.5, color: reg === mk ? INK : DIM }}>{EL[reg] ?? reg}</div>
                      <div style={{ height: 8, marginTop: 2 }}>
                        <div style={{ width: `${(val / mv) * 100}%`, height: '100%', backgroundColor: reg === mk ? col : '#DDDDDD' }} />
                      </div>
                    </div>
                    <span style={{ fontFamily: MO, fontSize: 9, color: reg === mk ? col : DIM, textAlign: 'right' }}>{val.toFixed(1)}</span>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </div>

      {/* VAD + stabilité */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, borderTop: `1px solid ${INK}`, paddingTop: 22 }}>
        <div>
          <ChLabel text="Gap affectif VAD — montée continue depuis oct. 2023" />
          <svg viewBox={`0 0 ${SVG_W} ${SVG_H}`} style={{ width: '100%', height: SVG_H + 4, display: 'block' }} aria-hidden>
            <line x1="0" y1={SVG_H} x2={SVG_W} y2={SVG_H} stroke={RL} strokeWidth="1" />
            <path d={pts} fill="none" stroke={ACC} strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" />
          </svg>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: MO, fontSize: 8, color: DIM, marginTop: 8 }}>
            <span>oct. 2023 · {vadS.toFixed(3)}</span>
            <span style={{ color: ACC }}>janv. 2026 · <strong>{vadE.toFixed(3)}</strong></span>
          </div>
        </div>
        <div>
          <ChLabel text="Entropie Ec et dimensionnalité ED — inchangées" />
          {[['Ec', ecS, ecE],['ED', edS, edE]].map(([lb, s, e]) => (
            <div key={String(lb)} style={{ display: 'grid', gridTemplateColumns: '40px 1fr', gap: 16, alignItems: 'baseline', marginBottom: 20 }}>
              <div style={{ fontFamily: MO, fontSize: 9, color: DIM, textTransform: 'uppercase' }}>{lb}</div>
              <div style={{ fontFamily: MA, fontSize: 28, fontWeight: 900, color: INK, letterSpacing: '-0.03em' }}>
                {Number(s).toFixed(3)}<span style={{ fontFamily: MO, fontSize: 14, color: DIM, margin: '0 8px' }}>→</span>{Number(e).toFixed(3)}
              </div>
            </div>
          ))}
          <div style={{ fontFamily: SA, fontSize: 12, color: MID, borderTop: `1px solid ${RL}`, paddingTop: 12, lineHeight: 1.6 }}>
            Structure stable. Seule l&apos;intensité émotionnelle (VAD) monte.
          </div>
        </div>
      </div>
    </div>
  );
}
