/**
 * DIRECTION A — Presse dense (Le Point)
 * Boîtes crème, encadrés à bandeau rouge, grands nombres en colonne dédiée,
 * labels intégrés dans les barres, palette chaude.
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
const ACC = '#C8102E';
const INK = '#141414';
const MID = '#3A3A3A';
const DIM = '#7A7A7A';
const RL  = '#D8D6CE';
const BG  = '#F4F3ED';         /* fond figure */

const MO = '"IBM Plex Mono", monospace';
const SA = '"IBM Plex Sans", sans-serif';
const MA = '"Mattone", sans-serif';

/* ── Couleurs frames & blocs ─────────────────────────────────────── */
const FC = { HUM: '#2055A5', SEC: '#C8102E', MOR: '#7A7A7A', OTH: '#BDB9AD' } as const;
const FL = { HUM: 'Humanitaire', SEC: 'Sécuritaire', MOR: 'Moral', OTH: 'Autres' } as const;
const SG = ['HUM', 'SEC', 'MOR', 'OTH'] as const;
type Sg = (typeof SG)[number];
type FR = (typeof frameRows)[0];

const BF: Record<string, string> = {
  'Gauche radicale':   '#C8102E',
  'Gauche moderee':    '#D4623A',
  'Centre / Majorite': '#2055A5',
  'Droite':            '#1A3F6E',
};
const BL: Record<string, string> = {
  'Gauche radicale':   'Gauche radicale',
  'Gauche moderee':    'Gauche modérée',
  'Centre / Majorite': 'Centre / Majorité',
  'Droite':            'Droite',
};
const EL: Record<string, string> = {
  indignation: 'Indignation', solidarite: 'Solidarité', neutral: 'Neutre',
  grief: 'Tristesse', anger: 'Colère', defiance: 'Défiance', fear: 'Peur',
};

const domFR = (row: FR) => SG.map((k) => ({ k, v: row[k] })).reduce((a, b) => b.v > a.v ? b : a);
const signed = (n: number, d = 2) => (n >= 0 ? `+${n.toFixed(d)}` : n.toFixed(d));

const maxTw = Math.max(...tweetsPerDeputy.map((d) => d.value));
const maxVis = Math.max(...visibilityByQuintile.map((d) => d.value));
const maxDlt = Math.max(...twitterVsAnByBloc.map((d) => Math.abs(d.delta)));
const maxEv  = Math.max(...eventImpact.map((d) => Math.abs(d.delta)));
const maxWd  = Math.max(...wassersteinDriftSnapshots.flatMap((d) => [d.gaucheRadicale, d.gaucheModeree, d.centreMajorite, d.droite]));
const maxZ   = Math.max(...['gaza','génocide','massacres'].flatMap((w) => [
  lexicalContrast.gauche.find((d) => d.word === w)?.z ?? 0,
  lexicalContrast.droite.find((d) => d.word === { 'gaza':'hamas','génocide':'terroristes','massacres':'antisémitisme' }[w])?.z ?? 0,
]));

const PAIRS = [
  { g: 'gaza', d: 'hamas' },
  { g: 'génocide', d: 'terroristes' },
  { g: 'massacres', d: 'antisémitisme' },
];
const EVENTS = [
  { key: 'CIJ (janv. 2024)',          lb: 'CIJ',           dt: 'janv. 2024' },
  { key: 'Rafah (mai 2024)',           lb: 'Rafah',         dt: 'mai 2024' },
  { key: 'Cessez-le-feu (janv. 2025)', lb: 'Cessez-le-feu', dt: 'janv. 2025' },
] as const;
const BLOCS = ['Gauche radicale','Gauche moderee','Centre / Majorite','Droite'] as const;

function Box({ children, label, footer }: { children: React.ReactNode; label: string; footer?: string }) {
  return (
    <div style={{ background: BG, padding: '18px 22px', marginBottom: 18 }}>
      <div style={{ fontFamily: MO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.14em', fontWeight: 700, marginBottom: 16 }}>{label}</div>
      {children}
      {footer && <div style={{ fontFamily: MO, fontSize: 7.5, color: DIM, marginTop: 10 }}>{footer}</div>}
    </div>
  );
}

function Encadre({ title, big, label, body }: { title: string; big: string; label: string; body: string }) {
  return (
    <div style={{ border: `1px solid ${RL}` }}>
      <div style={{ background: ACC, padding: '9px 16px' }}>
        <div style={{ fontFamily: MO, fontSize: 7.5, color: 'rgba(255,255,255,0.85)', textTransform: 'uppercase', letterSpacing: '0.16em', fontWeight: 700 }}>{title}</div>
      </div>
      <div style={{ padding: '18px 16px' }}>
        <div style={{ fontFamily: MA, fontSize: 48, fontWeight: 900, color: INK, letterSpacing: '-0.04em', lineHeight: 1, marginBottom: 5 }}>{big}</div>
        <div style={{ fontFamily: MO, fontSize: 8, color: ACC, textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 700, marginBottom: 14 }}>{label}</div>
        <div style={{ borderTop: `1px solid ${RL}`, paddingTop: 12, fontFamily: SA, fontSize: 12, color: MID, lineHeight: 1.6 }}>{body}</div>
      </div>
    </div>
  );
}

/* ─────────────────── EXPORTS ─────────────────────────────────────── */

export function A_Frames() {
  return (
    <div>
      {/* Cadres + butterfly + encadré */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 228px', gap: 18, marginBottom: 18 }}>
        <Box label="Répartition des cadres discursifs par bloc — % des interventions" footer="577 députés · AN française · 2023–2026">
          {/* Légende */}
          <div style={{ display: 'flex', gap: 18, marginBottom: 14 }}>
            {SG.map((k) => (
              <span key={k} style={{ display: 'flex', alignItems: 'center', gap: 5, fontFamily: MO, fontSize: 7.5, color: DIM, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                <span style={{ width: 9, height: 9, backgroundColor: FC[k], display: 'inline-block' }} /> {FL[k]}
              </span>
            ))}
          </div>
          {frameRows.map((row) => {
            const dom = domFR(row);
            let acc = 0;
            return (
              <div key={row.bloc} style={{ display: 'grid', gridTemplateColumns: '182px 1fr 100px', alignItems: 'center', borderTop: `1px solid rgba(0,0,0,0.07)`, padding: '11px 0' }}>
                <div style={{ paddingRight: 16 }}>
                  <div style={{ fontFamily: SA, fontSize: 12, fontWeight: 700, color: INK, marginBottom: 3 }}>{blocLabels[row.bloc]}</div>
                  <div style={{ fontFamily: MO, fontSize: 8, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: dom.k === 'HUM' ? FC.HUM : dom.k === 'SEC' ? FC.SEC : DIM }}>
                    {FL[dom.k as Sg]}
                  </div>
                </div>
                <div style={{ position: 'relative', height: 40 }}>
                  {[25,50,75].map((t) => <div key={t} aria-hidden style={{ position: 'absolute', left: `${t}%`, top:0, bottom:0, width:1, backgroundColor:'rgba(255,255,255,0.55)', zIndex:2 }} />)}
                  {SG.map((k) => {
                    const sl = acc; const w = row[k]; acc += w;
                    return (
                      <div key={k} style={{ position:'absolute', left:`${sl}%`, width:`${w}%`, top:0, bottom:0, backgroundColor:FC[k], display:'flex', alignItems:'center', justifyContent:'center', overflow:'hidden', zIndex:1 }}>
                        {w > 10 && <span style={{ fontFamily:MO, fontSize: w > 20 ? 10 : 8.5, fontWeight:700, color: k==='OTH'?MID:'rgba(255,255,255,0.95)', whiteSpace:'nowrap' }}>{Math.round(w)}%</span>}
                      </div>
                    );
                  })}
                </div>
                <div style={{ paddingLeft: 14, borderLeft:`1px solid rgba(0,0,0,0.1)`, textAlign:'center' }}>
                  <div style={{ fontFamily:MA, fontSize:26, fontWeight:900, letterSpacing:'-0.02em', lineHeight:1, color: dom.k==='HUM'?FC.HUM:dom.k==='SEC'?FC.SEC:DIM }}>
                    {Math.round(dom.v)}%
                  </div>
                </div>
              </div>
            );
          })}
          <div style={{ display:'flex', justifyContent:'space-between', fontFamily:MO, fontSize:7.5, color:DIM, paddingLeft:182, marginTop:7 }}>
            {['0','25','50','75','100%'].map((v) => <span key={v}>{v}</span>)}
          </div>
        </Box>
        <Encadre title="Corrélation clé" big={registerPositionCorrelation.toFixed(3)} label="ρ registre ↔ position" body="Le ton du discours ne prédit pas la position politique." />
      </div>

      {/* Butterfly */}
      <Box label="Mots discriminants — score Z normalisé par camp">
        <div style={{ display:'grid', gridTemplateColumns:'1fr 2px 1fr', marginBottom:14 }}>
          <div style={{ fontFamily:SA, fontSize:11, fontWeight:700, color:FC.HUM, textAlign:'right', paddingRight:14 }}>Gauche</div>
          <div style={{ background:DIM }} />
          <div style={{ fontFamily:SA, fontSize:11, fontWeight:700, color:FC.SEC, paddingLeft:14 }}>Droite</div>
        </div>
        {PAIRS.map(({ g, d }) => {
          const lw = lexicalContrast.gauche.find((x) => x.word === g);
          const rw = lexicalContrast.droite.find((x) => x.word === d);
          if (!lw || !rw) return null;
          return (
            <div key={g} style={{ display:'grid', gridTemplateColumns:'110px 1fr 2px 1fr 110px', alignItems:'center', marginBottom:16 }}>
              <span style={{ fontFamily:SA, fontSize:16, fontWeight:700, color:FC.HUM, textAlign:'right', paddingRight:14 }}>{lw.word}</span>
              <div style={{ height:28, display:'flex', justifyContent:'flex-end' }}>
                <div style={{ width:`${(lw.z/maxZ)*100}%`, height:'100%', backgroundColor:FC.HUM }} />
              </div>
              <div style={{ background:DIM, alignSelf:'stretch' }} />
              <div style={{ height:28 }}><div style={{ width:`${(rw.z/maxZ)*100}%`, height:'100%', backgroundColor:FC.SEC }} /></div>
              <span style={{ fontFamily:SA, fontSize:16, fontWeight:700, color:FC.SEC, paddingLeft:14 }}>{rw.word}</span>
            </div>
          );
        })}
      </Box>
    </div>
  );
}

export function A_Visibility() {
  return (
    <div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 228px', gap:18, marginBottom:18 }}>
        <Box label="Tweets publiés par député — moyenne par bloc politique" footer="Corpus X/Twitter, 577 députés, 2023–2026">
          {tweetsPerDeputy.map((row, idx) => {
            const fill = BF[row.bloc] ?? DIM;
            const isMx = idx === 0;
            return (
              <div key={row.bloc} style={{ display:'grid', gridTemplateColumns:'188px 1fr 72px', alignItems:'center', borderTop:`1px solid rgba(0,0,0,0.07)`, padding:'10px 0' }}>
                <div style={{ paddingRight:18 }}><div style={{ fontFamily:SA, fontSize:12, fontWeight: isMx?700:600, color:INK }}>{blocLabels[row.bloc]}</div></div>
                <div style={{ position:'relative', height: isMx?50:34 }}>
                  <div style={{ position:'absolute', inset:0, backgroundColor:'rgba(0,0,0,0.05)' }} />
                  <div style={{ position:'absolute', inset:0, width:`${(row.value/maxTw)*100}%`, backgroundColor:fill }} />
                </div>
                <div style={{ paddingLeft:14, textAlign:'right' }}>
                  <span style={{ fontFamily:MA, fontSize: isMx?26:17, fontWeight:700, color:fill }}>{Math.round(row.value)}</span>
                </div>
              </div>
            );
          })}
        </Box>
        <Encadre title="Paradoxe de visibilité" big="×7" label="LFI vs Centre — tweets/député" body="122 tweets vs 17. L'illusion d'unanimité en ligne est produite par la suractivité d'un seul camp." />
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:18 }}>
        <Box label="Visibilité × radicalité de position — |stance| par quintile Twitter">
          {visibilityByQuintile.map((row, idx) => {
            const isTop = idx === visibilityByQuintile.length - 1;
            return (
              <div key={row.quintile} style={{ display:'grid', gridTemplateColumns:'136px 1fr 44px', gap:8, alignItems:'center', marginBottom:10 }}>
                <span style={{ fontFamily:SA, fontSize:10, color: isTop?INK:MID, fontWeight: isTop?700:400 }}>{row.quintile}</span>
                <div style={{ position:'relative', height:18 }}>
                  <div style={{ position:'absolute', inset:0, backgroundColor:'rgba(0,0,0,0.07)' }} />
                  <div style={{ position:'absolute', inset:0, width:`${(row.value/maxVis)*100}%`, backgroundColor: isTop?ACC:'#2055A5' }} />
                </div>
                <span style={{ fontFamily:MO, fontSize:11, fontWeight:700, color: isTop?ACC:DIM, textAlign:'right' }}>{row.value.toFixed(2)}</span>
              </div>
            );
          })}
        </Box>
        <Box label="Surjeu Twitter vs hémicycle — delta de stance (rouge : p < 0,05)" footer="Seule la gauche radicale surjoue sig. (p = 0,011)">
          {twitterVsAnByBloc.map((row) => {
            const sig = row.significant;
            const pct = (Math.abs(row.delta) / maxDlt) * 50;
            const fill = BF[row.bloc] ?? DIM;
            return (
              <div key={row.bloc} style={{ display:'grid', gridTemplateColumns:'148px 1fr 54px', gap:8, alignItems:'center', marginBottom:10 }}>
                <span style={{ fontFamily:SA, fontSize:10, color: sig?INK:MID, fontWeight: sig?700:400 }}>{blocLabels[row.bloc]}</span>
                <div style={{ position:'relative', height:18 }}>
                  <div style={{ position:'absolute', left:'50%', top:-2, bottom:-2, width:1.5, backgroundColor:DIM, opacity:0.4 }} />
                  <div style={{ position:'absolute', top:0, bottom:0, left: row.delta>=0?'50%':`calc(50% - ${pct}%)`, width:`${pct}%`, backgroundColor: sig?fill:'#BBBBBB', opacity: sig?1:0.6 }} />
                </div>
                <span style={{ fontFamily:MO, fontSize:11, fontWeight:700, color: sig?fill:DIM, textAlign:'right' }}>{signed(row.delta, 2)}</span>
              </div>
            );
          })}
        </Box>
      </div>
    </div>
  );
}

export function A_Rhythms() {
  return (
    <div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 228px', gap:18, marginBottom:18 }}>
        <Box label="Réaction des blocs aux événements — delta de stance (centré sur zéro)" footer="Rouge : delta positif sig. (p < 0,05) · Bleu : delta négatif sig. · Gris : non sig.">
          <div style={{ display:'grid', gridTemplateColumns:'156px 1fr 1fr 1fr', gap:8, marginBottom:10 }}>
            <div />
            {EVENTS.map((ev) => (
              <div key={ev.key} style={{ textAlign:'center' }}>
                <div style={{ fontFamily:SA, fontSize:12, fontWeight:700, color:INK, marginBottom:2 }}>{ev.lb}</div>
                <div style={{ fontFamily:MO, fontSize:7.5, color:DIM }}>{ev.dt}</div>
              </div>
            ))}
          </div>
          {BLOCS.map((bloc) => (
            <div key={bloc} style={{ display:'grid', gridTemplateColumns:'156px 1fr 1fr 1fr', gap:8, alignItems:'center', borderTop:`1px solid rgba(0,0,0,0.07)`, padding:'10px 0' }}>
              <span style={{ fontFamily:SA, fontSize:11, fontWeight:600, color:INK }}>{blocLabels[bloc]}</span>
              {EVENTS.map((ev) => {
                const row = eventImpact.find((d) => d.event === ev.key && d.bloc === bloc);
                if (!row) return <div key={ev.key} />;
                const sig = row.p < 0.05;
                const bp  = (Math.abs(row.delta) / maxEv) * 46;
                const bc  = sig ? (row.delta > 0 ? ACC : '#1A3F6E') : '#C0C0C0';
                return (
                  <div key={ev.key} style={{ position:'relative', height:44 }}>
                    <div style={{ position:'absolute', left:'50%', top:0, height:30, width:1.5, backgroundColor:DIM, opacity:0.35 }} />
                    <div style={{ position:'absolute', top:6, height:18, left: row.delta>=0?'50%':`calc(50% - ${bp}%)`, width:`${bp}%`, backgroundColor:bc }} />
                    <div style={{ position:'absolute', bottom:0, width:'100%', textAlign:'center', fontFamily:MO, fontSize:8.5, fontWeight: sig?700:400, color: sig?bc:DIM }}>{signed(row.delta,2)}</div>
                  </div>
                );
              })}
            </div>
          ))}
        </Box>
        <div style={{ border:`1px solid ${RL}` }}>
          <div style={{ background:ACC, padding:'9px 16px' }}>
            <div style={{ fontFamily:MO, fontSize:7.5, color:'rgba(255,255,255,0.85)', textTransform:'uppercase', letterSpacing:'0.16em', fontWeight:700 }}>À retenir</div>
          </div>
          <div style={{ padding:'18px 16px' }}>
            <div style={{ fontFamily:SA, fontSize:14, fontWeight:700, color:INK, lineHeight:1.35, marginBottom:14 }}>Aucune tendance lente vers la convergence.</div>
            <div style={{ borderTop:`1px solid ${RL}`, paddingTop:12, fontFamily:SA, fontSize:12, color:MID, lineHeight:1.6 }}>Pas de trajectoire séculaire (Mann-Kendall). Wasserstein oscille sans direction. Le système réagit par chocs ponctuels puis retourne à l'état initial.</div>
          </div>
        </div>
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:18 }}>
        <Box label="Mann-Kendall — tau de Kendall par bloc (aucun p < 0,15)" footer="Aucun tau significatif — pas de trajectoire lente">
          {mannKendallByBloc.map((row) => (
            <div key={row.bloc} style={{ display:'grid', gridTemplateColumns:'148px 1fr 54px', gap:8, alignItems:'center', marginBottom:10 }}>
              <span style={{ fontFamily:SA, fontSize:10, color:MID }}>{blocLabels[row.bloc]}</span>
              <div style={{ position:'relative', height:14 }}>
                <div style={{ position:'absolute', left:'50%', top:-2, bottom:-2, width:1.5, backgroundColor:DIM, opacity:0.35 }} />
                <div style={{ position:'absolute', top:0, bottom:0, left: row.tau>=0?'50%':`calc(50% - ${(Math.abs(row.tau)/0.25)*50}%)`, width:`${(Math.abs(row.tau)/0.25)*50}%`, backgroundColor:'#AAAAAA' }} />
              </div>
              <span style={{ fontFamily:MO, fontSize:9.5, color:DIM, textAlign:'right' }}>{signed(row.tau,2)}</span>
            </div>
          ))}
        </Box>
        <Box label="Distance de Wasserstein — oscillation irrégulière" footer="Oscillation sans pente — pas de convergence">
          {wassersteinDriftSnapshots.map((snap) => {
            const avg = (snap.gaucheRadicale + snap.gaucheModeree + snap.centreMajorite + snap.droite) / 4;
            const hot = avg > 0.12;
            return (
              <div key={snap.month} style={{ display:'grid', gridTemplateColumns:'72px 1fr 54px', gap:8, alignItems:'center', marginBottom:10 }}>
                <span style={{ fontFamily:MO, fontSize:8.5, color:INK }}>{snap.month}</span>
                <div style={{ position:'relative', height:14 }}>
                  <div style={{ position:'absolute', inset:0, backgroundColor:'rgba(0,0,0,0.07)' }} />
                  <div style={{ position:'absolute', top:0, left:0, bottom:0, width:`${(avg/maxWd)*100}%`, backgroundColor: hot?ACC:'#2055A5' }} />
                </div>
                <span style={{ fontFamily:MO, fontSize:9.5, fontWeight: hot?700:400, color: hot?ACC:DIM, textAlign:'right' }}>{avg.toFixed(3)}</span>
              </div>
            );
          })}
        </Box>
      </div>
    </div>
  );
}

export function A_Emotions() {
  const vadS = affectiveGap[0]?.value ?? 0;
  const vadE = affectiveGap[affectiveGap.length - 1]?.value ?? 0;
  const ecS  = entropicPolarizationSeries[0]?.value ?? 0;
  const ecE  = entropicPolarizationSeries[entropicPolarizationSeries.length - 1]?.value ?? 0;
  const edS  = effectiveDimensionalitySeries[0]?.value ?? 0;
  const edE  = effectiveDimensionalitySeries[effectiveDimensionalitySeries.length - 1]?.value ?? 0;
  const SVG_W = 540; const SVG_H = 80;
  const pts = affectiveGap.map((d, i) => {
    const mn = Math.min(...affectiveGap.map((x) => x.value));
    const mx = Math.max(...affectiveGap.map((x) => x.value));
    const x = (i / (affectiveGap.length - 1)) * SVG_W;
    const y = SVG_H - ((d.value - mn) / (mx - mn || 1)) * (SVG_H - 12) - 6;
    return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  return (
    <div>
      <Box label="Registre émotionnel dominant par bloc — % des interventions" footer="Classifieur BERT — 577 députés, 2023–2026">
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
          {(['Gauche radicale','Gauche moderee','Centre / Majorite','Droite'] as const).map((bloc) => {
            const vals  = emotionalRegisterByBloc[bloc as keyof typeof emotionalRegisterByBloc];
            const ents  = (Object.entries(vals) as [string,number][]).sort((a,b) => b[1]-a[1]);
            const [mk, mv] = ents[0];
            const col = BF[bloc] ?? DIM;
            return (
              <div key={bloc} style={{ background:'#fff', borderTop:`3px solid ${col}`, padding:'14px 16px' }}>
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:6 }}>
                  <div>
                    <div style={{ fontFamily:SA, fontSize:12, fontWeight:700, color:INK, marginBottom:4 }}>{BL[bloc]}</div>
                    <div style={{ fontFamily:MO, fontSize:8, color:col, textTransform:'uppercase', letterSpacing:'0.12em', fontWeight:700 }}>{EL[mk] ?? mk}</div>
                  </div>
                  <div style={{ fontFamily:MA, fontSize:34, fontWeight:900, color:col, letterSpacing:'-0.04em', lineHeight:1 }}>{mv.toFixed(0)}%</div>
                </div>
                <div style={{ borderTop:`1px solid rgba(0,0,0,0.08)`, paddingTop:10, marginTop:8 }}>
                  {ents.map(([reg, val]) => (
                    <div key={reg} style={{ display:'grid', gridTemplateColumns:'88px 1fr 36px', gap:6, alignItems:'center', marginBottom:7 }}>
                      <span style={{ fontFamily:SA, fontSize:9.5, color: reg===mk?INK:MID, fontWeight: reg===mk?700:400 }}>{EL[reg] ?? reg}</span>
                      <div style={{ position:'relative', height:14 }}>
                        <div style={{ position:'absolute', inset:0, backgroundColor:'rgba(0,0,0,0.07)' }} />
                        <div style={{ position:'absolute', inset:0, width:`${(val/mv)*100}%`, backgroundColor: reg===mk?col:'#BBBBBB' }} />
                      </div>
                      <span style={{ fontFamily:MO, fontSize:9, color: reg===mk?col:DIM, textAlign:'right', fontWeight: reg===mk?700:400 }}>{val.toFixed(1)}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </Box>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 228px', gap:18 }}>
        <Box label="Gap affectif VAD — montée continue depuis oct. 2023">
          <svg viewBox={`0 0 ${SVG_W} ${SVG_H}`} style={{ width:'100%', height:SVG_H+4, display:'block' }} aria-hidden>
            {[0.25,0.5,0.75].map((f) => <line key={f} x1="0" y1={SVG_H*(1-f)} x2={SVG_W} y2={SVG_H*(1-f)} stroke={RL} strokeWidth="0.75" />)}
            <line x1="0" y1={SVG_H} x2={SVG_W} y2={SVG_H} stroke={DIM} strokeWidth="1" />
            <path d={pts} fill="none" stroke={ACC} strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" />
          </svg>
          <div style={{ display:'flex', justifyContent:'space-between', fontFamily:MO, fontSize:8, color:DIM, marginTop:7 }}>
            <span>oct. 2023 · {vadS.toFixed(3)}</span>
            <span>janv. 2026 · <strong style={{ color:ACC }}>{vadE.toFixed(3)}</strong></span>
          </div>
        </Box>
        <div style={{ border:`1px solid ${RL}` }}>
          <div style={{ background:ACC, padding:'9px 16px' }}>
            <div style={{ fontFamily:MO, fontSize:7.5, color:'rgba(255,255,255,0.85)', textTransform:'uppercase', letterSpacing:'0.16em', fontWeight:700 }}>Structure stable</div>
          </div>
          <div style={{ padding:'18px 16px' }}>
            {[['Entropie Ec', ecS, ecE],['Dim. effective ED', edS, edE]].map(([lb, s, e]) => (
              <div key={String(lb)} style={{ marginBottom:16 }}>
                <div style={{ fontFamily:MO, fontSize:7.5, color:DIM, textTransform:'uppercase', letterSpacing:'0.1em', marginBottom:5 }}>{lb}</div>
                <div style={{ fontFamily:MO, fontSize:19, fontWeight:700, color:INK, letterSpacing:'-0.02em' }}>
                  {Number(s).toFixed(3)}&ensp;<span style={{ fontSize:12, color:DIM }}>{'→'}</span>&ensp;{Number(e).toFixed(3)}
                </div>
              </div>
            ))}
            <div style={{ borderTop:`1px solid ${RL}`, paddingTop:12, fontFamily:SA, fontSize:12, color:MID, lineHeight:1.6 }}>
              La structure du désaccord reste intacte. Seule l&apos;intensité émotionnelle monte.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
