/**
 * Version fusion :
 * - Couleurs pleines pour les barres principales  → lisibilité maximale
 * - Symboles ●◆■▲ dans légendes + labels          → système graphique discret
 * - Hachures pour non-significatif uniquement     → sémantique fonctionnelle
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

/* ── Tokens ──────────────────────────────────────────────────────── */
const NM  = '"Necto Mono", monospace';
const INK = '#111111';
const MID = '#505050';
const DIM = '#9A9A9A';
const RL  = '#DEDEDE';
const WH  = '#FFFFFF';
const RD  = '#C8102E';

/* ── Couleurs blocs (primaire — lisibilité) ──────────────────────── */
const BC: Record<string,string> = {
  'Gauche radicale':   '#C8102E',
  'Gauche moderee':    '#D97706',
  'Centre / Majorite': '#1D4ED8',
  'Droite':            '#1E3A5F',
};
/* ── Symboles blocs (couche graphique) ───────────────────────────── */
const SYM: Record<string,string> = {
  'Gauche radicale':   '\u25cf',  /* ● */
  'Gauche moderee':    '\u25c6',  /* ◆ */
  'Centre / Majorite': '\u25a0',  /* ■ */
  'Droite':            '\u25b2',  /* ▲ */
};
const BL: Record<string,string> = {
  'Gauche radicale':   'Gauche radicale',
  'Gauche moderee':    'Gauche mod\u00e9r\u00e9e',
  'Centre / Majorite': 'Centre / Majorit\u00e9',
  'Droite':            'Droite',
};

/* ── Couleurs cadres discursifs ──────────────────────────────────── */
const FC: Record<string,string> = {
  HUM: '#1D4ED8', SEC: '#C8102E', MOR: '#6B7280', OTH: '#E4E4E4',
};
const FL: Record<string,string> = {
  HUM: 'Humanitaire', SEC: 'S\u00e9curitaire', MOR: 'Moral', OTH: 'Autres',
};
const SG = ['HUM','SEC','MOR','OTH'];
type FR = typeof frameRows[number];
const domFR = (r:FR) => SG.map(k=>({k, v:r[k as keyof FR] as number})).reduce((a,b)=>b.v>a.v?b:a);

/* ── Hachures — non-significatif uniquement ──────────────────────── */
const H_NSIG = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='5' height='5'%3E%3Cline x1='0' y1='5' x2='5' y2='0' stroke='%23C8C8C8' stroke-width='0.8'/%3E%3C/svg%3E")`;
const H_OTH  = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='6' height='6'%3E%3Cline x1='0' y1='6' x2='6' y2='0' stroke='%23C4C4C4' stroke-width='0.9'/%3E%3C/svg%3E")`;

/* ── Émotions ────────────────────────────────────────────────────── */
const EL: Record<string,string> = {
  indignation:'Indignation', solidarite:'Solidarit\u00e9', neutral:'Neutre',
  grief:'Tristesse', anger:'Col\u00e8re', defiance:'D\u00e9fiance', fear:'Peur',
};

const EVENTS = [
  { key:'CIJ (janv. 2024)',           lb:'CIJ',           dt:'janv. 2024' },
  { key:'Rafah (mai 2024)',            lb:'Rafah',         dt:'mai 2024'   },
  { key:'Cessez-le-feu (janv. 2025)', lb:'Cessez-le-feu', dt:'janv. 2025' },
] as const;
const BLOCS = ['Gauche radicale','Gauche moderee','Centre / Majorite','Droite'] as const;
const PAIRS = [
  { g:'gaza',           d:'hamas'           },
  { g:'g\u00e9nocide',  d:'terroristes'     },
  { g:'massacres',      d:'antis\u00e9mitisme' },
];

const signed = (n:number, dec=2) => (n>=0 ? `+${n.toFixed(dec)}` : n.toFixed(dec));
const maxTw  = Math.max(...tweetsPerDeputy.map(d=>d.value));
const maxVis = Math.max(...visibilityByQuintile.map(d=>d.value));
const maxDlt = Math.max(...twitterVsAnByBloc.map(d=>Math.abs(d.delta)));
const maxEv  = Math.max(...eventImpact.map(d=>Math.abs(d.delta)));
const maxZ   = Math.max(...PAIRS.flatMap(({g,d})=>[
  lexicalContrast.gauche.find(x=>x.word===g)?.z??0,
  lexicalContrast.droite.find(x=>x.word===d)?.z??0,
]));

/* ── Primitives ──────────────────────────────────────────────────── */

function FT({text}:{text:string}) {
  return <div style={{fontFamily:NM,fontSize:7.5,textTransform:'uppercase',letterSpacing:'0.15em',color:DIM,marginBottom:12}}>{text}</div>;
}
function Src({text}:{text:string}) {
  return <div style={{fontFamily:NM,fontSize:7,color:DIM,marginTop:10,lineHeight:1.5}}>Source · {text}</div>;
}

/* Légende : carré couleur + symbole + label */
function Leg({items}:{items:{color:string;sym?:string;label:string;hatch?:boolean}[]}) {
  return (
    <div style={{display:'flex',gap:18,flexWrap:'wrap',marginBottom:14}}>
      {items.map(({color,sym,label,hatch})=>(
        <span key={label} style={{display:'flex',alignItems:'center',gap:6,fontFamily:NM,fontSize:8,color:MID}}>
          <span style={{
            width:9,height:9,display:'inline-block',flexShrink:0,
            backgroundColor:hatch?'#F2F2F2':color,
            backgroundImage:hatch?H_OTH:'none',
            border:`0.5px solid ${hatch?RL:color}`,
          }}/>
          {sym&&<span style={{fontSize:10,color:INK,lineHeight:1,marginRight:-2}}>{sym}</span>}
          {label}
        </span>
      ))}
    </div>
  );
}

/* Swatch hachure inline */
function NSigKey() {
  return (
    <span style={{display:'inline-flex',alignItems:'center',gap:5,fontFamily:NM,fontSize:7.5,color:DIM,marginLeft:16}}>
      <span style={{width:10,height:10,display:'inline-block',backgroundColor:'#F2F2F2',backgroundImage:H_NSIG,border:`0.5px solid ${RL}`}}/>
      non significatif
    </span>
  );
}

function Gap() { return <div style={{height:36}}/>; }

/* ══════════════════════════════════════════════════════════════════
   LAYER 1
══════════════════════════════════════════════════════════════════ */
export function Mix_Frames() {
  const BH = 40;

  return (
    <div>
      {/* Stacked bars */}
      <FT text="R\u00e9partition des cadres discursifs par bloc — % des interventions"/>
      <Leg items={[
        {color:FC.HUM,label:FL.HUM},
        {color:FC.SEC,label:FL.SEC},
        {color:FC.MOR,label:FL.MOR},
        {color:'#F2F2F2',label:FL.OTH,hatch:true},
      ]}/>

      {frameRows.map(row=>{
        const dom=domFR(row); let acc=0;
        return (
          <div key={row.bloc} style={{display:'grid',gridTemplateColumns:'168px 1fr 68px',alignItems:'center',borderTop:`1px solid ${RL}`,padding:'8px 0'}}>
            {/* Label + symbole */}
            <div style={{paddingRight:14,display:'flex',alignItems:'center',gap:7}}>
              <span style={{fontSize:12,color:BC[row.bloc],lineHeight:1}}>{SYM[row.bloc]}</span>
              <span style={{fontFamily:NM,fontSize:11,color:INK}}>{blocLabels[row.bloc]}</span>
            </div>
            {/* Barre empilée */}
            <div style={{position:'relative',height:BH}}>
              {[25,50,75].map(t=>(
                <div key={t} style={{position:'absolute',left:`${t}%`,top:0,bottom:0,width:1,backgroundColor:'rgba(255,255,255,0.65)',zIndex:3}}/>
              ))}
              {SG.map(k=>{
                const sl=acc; const w=row[k as keyof FR] as number; acc+=w;
                const isOTH=k==='OTH';
                return (
                  <div key={k} style={{
                    position:'absolute',left:`${sl}%`,width:`${w}%`,top:0,bottom:0,zIndex:1,
                    backgroundColor:isOTH?'#F2F2F2':FC[k],
                    backgroundImage:isOTH?H_OTH:'none',
                    display:'flex',alignItems:'center',justifyContent:'center',overflow:'hidden',
                  }}>
                    {w>11&&(
                      <span style={{fontFamily:NM,fontSize:w>22?10:8,color:isOTH?DIM:'rgba(255,255,255,0.93)',whiteSpace:'nowrap',zIndex:4}}>
                        {Math.round(w)}%
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
            {/* Dominant % */}
            <div style={{paddingLeft:10,textAlign:'right'}}>
              <span style={{fontFamily:NM,fontSize:21,color:dom.k==='OTH'?DIM:FC[dom.k],letterSpacing:'-0.02em',lineHeight:1}}>
                {Math.round(dom.v)}%
              </span>
            </div>
          </div>
        );
      })}
      <div style={{display:'flex',justifyContent:'space-between',fontFamily:NM,fontSize:6.5,color:DIM,marginTop:3,paddingLeft:168}}>
        {[0,25,50,75,100].map(t=><span key={t}>{t}%</span>)}
      </div>
      <Src text="Classifieur BERT · 577 d\u00e9put\u00e9s · AN · 2023–2026"/>

      <Gap/>

      {/* Butterfly + rho */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 180px',gap:36}}>
        <div>
          <FT text="Mots discriminants — score Z — camps lexicaux"/>
          <div style={{display:'grid',gridTemplateColumns:'116px 1fr 1px 1fr 116px',gap:0,marginBottom:8}}>
            <div/>
            <div style={{fontFamily:NM,fontSize:7.5,color:FC.HUM,textTransform:'uppercase',letterSpacing:'0.1em',textAlign:'right',paddingRight:12}}>← Gauche</div>
            <div/><div style={{fontFamily:NM,fontSize:7.5,color:FC.SEC,textTransform:'uppercase',letterSpacing:'0.1em',paddingLeft:12}}>Droite →</div>
            <div/>
          </div>
          {PAIRS.map(({g,d})=>{
            const lw=lexicalContrast.gauche.find(x=>x.word===g);
            const rw=lexicalContrast.droite.find(x=>x.word===d);
            if (!lw||!rw) return null;
            const lp=(lw.z/maxZ)*100; const rp=(rw.z/maxZ)*100;
            return (
              <div key={g} style={{display:'grid',gridTemplateColumns:'116px 1fr 1px 1fr 116px',alignItems:'center',borderTop:`1px solid ${RL}`,padding:'9px 0',gap:0}}>
                <span style={{fontFamily:NM,fontSize:16,color:FC.HUM,textAlign:'right',paddingRight:16}}>{lw.word}</span>
                <div style={{position:'relative',height:26,display:'flex',justifyContent:'flex-end'}}>
                  <div style={{width:`${lp}%`,height:'100%',backgroundColor:FC.HUM}}/>
                </div>
                <div style={{backgroundColor:RL,alignSelf:'stretch'}}/>
                <div style={{position:'relative',height:26}}>
                  <div style={{width:`${rp}%`,height:'100%',backgroundColor:FC.SEC}}/>
                </div>
                <span style={{fontFamily:NM,fontSize:16,color:FC.SEC,paddingLeft:16}}>{rw.word}</span>
              </div>
            );
          })}
          <div style={{display:'grid',gridTemplateColumns:'116px 1fr 1px 1fr 116px',gap:0,marginTop:4}}>
            <div/>
            <div style={{fontFamily:NM,fontSize:6.5,color:DIM,textAlign:'right',paddingRight:12}}>Z max = {lexicalContrast.gauche[0]?.z.toFixed(1)}</div>
            <div/>
            <div style={{fontFamily:NM,fontSize:6.5,color:DIM,paddingLeft:12}}>Z max = {lexicalContrast.droite[0]?.z.toFixed(1)}</div>
            <div/>
          </div>
          <Src text="Score Z · corpus AN 2023–2026"/>
        </div>

        {/* rho */}
        <div style={{borderLeft:`2px solid ${RL}`,paddingLeft:20}}>
          <div style={{fontFamily:NM,fontSize:7.5,textTransform:'uppercase',letterSpacing:'0.12em',color:DIM,marginBottom:8}}>
            \u03c1 registre \u2194 position
          </div>
          <div style={{fontFamily:NM,fontSize:42,color:INK,letterSpacing:'-0.02em',lineHeight:1,marginBottom:10}}>
            {registerPositionCorrelation.toFixed(3)}
          </div>
          <div style={{height:1,backgroundColor:RL,marginBottom:10}}/>
          <div style={{fontFamily:NM,fontSize:10.5,color:MID,lineHeight:1.75}}>
            Le ton ne pr\u00e9dit pas la position. Registre et positionnement sont ind\u00e9pendants.
          </div>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════
   LAYER 2
══════════════════════════════════════════════════════════════════ */
export function Mix_Visibility() {
  return (
    <div>
      {/* Tweets */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:44}}>
        <div>
          <FT text="Tweets par d\u00e9put\u00e9 — moyenne par bloc"/>
          <Leg items={BLOCS.map(b=>({color:BC[b],sym:SYM[b],label:BL[b]}))}/>
          {tweetsPerDeputy.map((row,idx)=>{
            const isMax=idx===0;
            const pct=(row.value/maxTw)*100;
            const inside=pct>28;
            const H=isMax?44:28;
            return (
              <div key={row.bloc} style={{display:'grid',gridTemplateColumns:'172px 1fr',alignItems:'center',borderTop:`1px solid ${RL}`,padding:'7px 0'}}>
                <div style={{display:'flex',alignItems:'center',gap:7,paddingRight:14}}>
                  <span style={{fontSize:isMax?13:11,color:BC[row.bloc],lineHeight:1}}>{SYM[row.bloc]}</span>
                  <span style={{fontFamily:NM,fontSize:11,color:INK}}>{BL[row.bloc]}</span>
                </div>
                <div style={{position:'relative',height:H}}>
                  <div style={{position:'absolute',left:0,top:0,bottom:0,width:`${pct}%`,backgroundColor:BC[row.bloc],display:'flex',alignItems:'center',overflow:'hidden',justifyContent:inside?'flex-end':'flex-start'}}>
                    {inside&&<span style={{fontFamily:NM,fontSize:isMax?13:10,color:'rgba(255,255,255,0.93)',paddingRight:8,whiteSpace:'nowrap'}}>{row.value.toFixed(0)}</span>}
                  </div>
                  {!inside&&<div style={{position:'absolute',left:`calc(${pct}%+7px)`,top:0,bottom:0,display:'flex',alignItems:'center'}}>
                    <span style={{fontFamily:NM,fontSize:10,color:BC[row.bloc]}}>{row.value.toFixed(0)}</span>
                  </div>}
                </div>
              </div>
            );
          })}
          <div style={{display:'flex',justifyContent:'space-between',fontFamily:NM,fontSize:6.5,color:DIM,marginTop:3,paddingLeft:172}}>
            <span>0</span><span>61</span><span>122</span>
          </div>
          <Src text="X/Twitter · 577 d\u00e9put\u00e9s · 2023–2026"/>
        </div>

        <div>
          {/* Quintile */}
          <FT text="|stance| par quintile Twitter"/>
          <div style={{marginBottom:14}}/>
          {visibilityByQuintile.map((row,idx)=>{
            const isTop=idx===visibilityByQuintile.length-1;
            const pct=(row.value/maxVis)*100;
            return (
              <div key={row.quintile} style={{display:'grid',gridTemplateColumns:'140px 1fr 42px',gap:8,alignItems:'center',borderTop:`1px solid ${RL}`,padding:'8px 0'}}>
                <span style={{fontFamily:NM,fontSize:9.5,color:isTop?INK:MID}}>{row.quintile}</span>
                <div style={{position:'relative',height:18}}>
                  <div style={{position:'absolute',left:0,top:0,bottom:0,width:`${pct}%`,backgroundColor:isTop?RD:'#F2F2F2',backgroundImage:isTop?'none':H_NSIG}}/>
                </div>
                <span style={{fontFamily:NM,fontSize:9.5,color:isTop?RD:DIM,textAlign:'right'}}>{row.value.toFixed(2)}</span>
              </div>
            );
          })}
          <div style={{display:'flex',justifyContent:'space-between',fontFamily:NM,fontSize:6.5,color:DIM,marginTop:3,paddingLeft:148}}>
            <span>0</span><span>0.80</span><span>1.60</span>
          </div>
          <Src text="|stance| = radicalit\u00e9 absolue · quintiles Twitter"/>

          <Gap/>

          {/* Delta */}
          <FT text="Delta stance Twitter \u2212 AN"/>
          <div style={{marginBottom:8,display:'flex',alignItems:'center'}}>
            <span style={{fontFamily:NM,fontSize:7.5,color:DIM}}>Aplat = p &lt; 0,05</span>
            <NSigKey/>
          </div>
          {twitterVsAnByBloc.map(row=>{
            const sig=row.significant;
            const pct=(Math.abs(row.delta)/maxDlt)*50;
            const fill=BC[row.bloc]??RD;
            return (
              <div key={row.bloc} style={{display:'grid',gridTemplateColumns:'152px 1fr 48px',gap:8,alignItems:'center',borderTop:`1px solid ${RL}`,padding:'8px 0'}}>
                <div style={{display:'flex',alignItems:'center',gap:6}}>
                  <span style={{fontSize:10,color:BC[row.bloc],lineHeight:1}}>{SYM[row.bloc]}</span>
                  <span style={{fontFamily:NM,fontSize:9.5,color:sig?INK:MID}}>{BL[row.bloc]}</span>
                </div>
                <div style={{position:'relative',height:18}}>
                  <div style={{position:'absolute',left:'50%',top:0,bottom:0,width:1,backgroundColor:RL}}/>
                  <div style={{
                    position:'absolute',top:0,bottom:0,
                    left:row.delta>=0?'50%':`calc(50% - ${pct}%)`,width:`${pct}%`,
                    backgroundColor:sig?fill:'#F2F2F2',backgroundImage:sig?'none':H_NSIG,
                  }}/>
                </div>
                <span style={{fontFamily:NM,fontSize:9.5,color:sig?fill:DIM,textAlign:'right'}}>{signed(row.delta,2)}</span>
              </div>
            );
          })}
          <div style={{display:'flex',justifyContent:'space-between',fontFamily:NM,fontSize:6.5,color:DIM,marginTop:3,paddingLeft:160}}>
            <span>−{maxDlt.toFixed(1)}</span><span>0</span><span>+{maxDlt.toFixed(1)}</span>
          </div>
          <Src text="LFI seule : d\u00e9calage significatif (p = 0,011)"/>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════
   LAYER 3
══════════════════════════════════════════════════════════════════ */
export function Mix_Rhythms() {
  return (
    <div>
      <FT text="Delta de stance lors des \u00e9v\u00e9nements — centr\u00e9 sur z\u00e9ro"/>
      <div style={{marginBottom:8,display:'flex',alignItems:'center'}}>
        <span style={{display:'flex',gap:16}}>
          {[{c:RD,l:'Hausse sig.'},{c:'#1A3F6E',l:'Baisse sig.'}].map(({c,l})=>(
            <span key={l} style={{display:'flex',alignItems:'center',gap:5,fontFamily:NM,fontSize:7.5,color:DIM}}>
              <span style={{width:9,height:9,backgroundColor:c,display:'inline-block'}}/>
              {l}
            </span>
          ))}
        </span>
        <NSigKey/>
      </div>

      {/* Grille */}
      <div style={{display:'grid',gridTemplateColumns:'148px repeat(3,1fr)',gap:8,paddingBottom:8,borderBottom:`1px solid ${RL}`}}>
        <div/>
        {EVENTS.map(ev=>(
          <div key={ev.key} style={{textAlign:'center'}}>
            <div style={{fontFamily:NM,fontSize:11,color:INK}}>{ev.lb}</div>
            <div style={{fontFamily:NM,fontSize:7.5,color:DIM}}>{ev.dt}</div>
          </div>
        ))}
      </div>

      {BLOCS.map(bloc=>(
        <div key={bloc} style={{display:'grid',gridTemplateColumns:'148px repeat(3,1fr)',gap:8,alignItems:'center',borderTop:`1px solid ${RL}`,padding:'9px 0'}}>
          <div style={{display:'flex',alignItems:'center',gap:7}}>
            <span style={{fontSize:11,color:BC[bloc],lineHeight:1}}>{SYM[bloc]}</span>
            <span style={{fontFamily:NM,fontSize:10.5,color:INK}}>{BL[bloc]}</span>
          </div>
          {EVENTS.map(ev=>{
            const row=eventImpact.find(d=>d.event===ev.key&&d.bloc===bloc);
            if (!row) return <div key={ev.key}/>;
            const sig=row.p<0.05;
            const pct=(Math.abs(row.delta)/maxEv)*48;
            const fill=sig?(row.delta>0?RD:'#1A3F6E'):'#F2F2F2';
            const showIn=pct>18;
            return (
              <div key={ev.key} style={{position:'relative',height:44}}>
                <div style={{position:'absolute',left:'50%',top:4,height:24,width:1,backgroundColor:RL}}/>
                <div style={{
                  position:'absolute',top:4,height:24,
                  left:row.delta>=0?'50%':`calc(50% - ${pct}%)`,width:`${pct}%`,
                  backgroundColor:fill,backgroundImage:sig?'none':H_NSIG,
                  display:'flex',alignItems:'center',justifyContent:'center',overflow:'hidden',
                }}>
                  {showIn&&sig&&<span style={{fontFamily:NM,fontSize:8,color:WH}}>{signed(row.delta,2)}</span>}
                </div>
                {(!showIn||!sig)&&(
                  <div style={{position:'absolute',bottom:0,width:'100%',textAlign:'center'}}>
                    <span style={{fontFamily:NM,fontSize:7.5,color:sig?fill:DIM}}>{signed(row.delta,2)}</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ))}
      <Src text="Classifieur BERT · seuil p &lt; 0,05"/>

      <Gap/>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:44}}>
        <div>
          <FT text="Mann-Kendall tau — aucune tendance temporelle"/>
          <div style={{marginBottom:8}}><NSigKey/></div>
          {mannKendallByBloc.map(row=>{
            const w=(Math.abs(row.tau)/0.25)*50;
            return (
              <div key={row.bloc} style={{display:'grid',gridTemplateColumns:'152px 1fr 48px',gap:8,alignItems:'center',borderTop:`1px solid ${RL}`,padding:'8px 0'}}>
                <div style={{display:'flex',alignItems:'center',gap:6}}>
                  <span style={{fontSize:10,color:BC[row.bloc],lineHeight:1}}>{SYM[row.bloc]}</span>
                  <span style={{fontFamily:NM,fontSize:9.5,color:MID}}>{BL[row.bloc]}</span>
                </div>
                <div style={{position:'relative',height:16}}>
                  <div style={{position:'absolute',left:'50%',top:0,bottom:0,width:1,backgroundColor:RL}}/>
                  <div style={{position:'absolute',top:0,bottom:0,left:row.tau>=0?'50%':`calc(50% - ${w}%)`,width:`${w}%`,backgroundColor:'#F2F2F2',backgroundImage:H_NSIG}}/>
                </div>
                <span style={{fontFamily:NM,fontSize:9.5,color:DIM,textAlign:'right'}}>{signed(row.tau,2)}</span>
              </div>
            );
          })}
          <Src text="Aucune trajectoire s\u00e9culaire (p &gt; 0,15 pour tous)"/>
        </div>

        <div>
          <FT text="Distance de Wasserstein — oscillation"/>
          {wassersteinDriftSnapshots.map(snap=>{
            const avg=(snap.gaucheRadicale+snap.gaucheModeree+snap.centreMajorite+snap.droite)/4;
            const maxW=Math.max(...wassersteinDriftSnapshots.map(s=>(s.gaucheRadicale+s.gaucheModeree+s.centreMajorite+s.droite)/4));
            const pct=(avg/(maxW||1))*100;
            const hot=avg>0.12;
            return (
              <div key={snap.month} style={{display:'grid',gridTemplateColumns:'74px 1fr 52px',gap:8,alignItems:'center',borderTop:`1px solid ${RL}`,padding:'8px 0'}}>
                <span style={{fontFamily:NM,fontSize:8.5,color:INK}}>{snap.month}</span>
                <div style={{position:'relative',height:18}}>
                  <div style={{position:'absolute',left:0,top:0,bottom:0,width:`${pct}%`,backgroundColor:hot?RD:'#F2F2F2',backgroundImage:hot?'none':H_NSIG}}/>
                </div>
                <span style={{fontFamily:NM,fontSize:9,color:hot?RD:DIM,textAlign:'right'}}>{avg.toFixed(3)}</span>
              </div>
            );
          })}
          <Src text="Moyenne 4 blocs · oscillation sans pente"/>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════
   LAYER 4
══════════════════════════════════════════════════════════════════ */
export function Mix_Emotions() {
  const vadS=affectiveGap[0]?.value??0;
  const vadE=affectiveGap[affectiveGap.length-1]?.value??0;
  const mn=Math.min(...affectiveGap.map(d=>d.value));
  const mx=Math.max(...affectiveGap.map(d=>d.value));
  const SVW=500; const SVH=84; const pad=8;
  const yOf=(v:number)=>SVH-((v-mn)/(mx-mn||1))*(SVH-pad*2)-pad;
  const pts=affectiveGap.map((d,i)=>`${i===0?'M':'L'}${((i/(affectiveGap.length-1))*SVW).toFixed(1)},${yOf(d.value).toFixed(1)}`).join(' ');
  const ecS=entropicPolarizationSeries[0]?.value??0;
  const ecE=entropicPolarizationSeries[entropicPolarizationSeries.length-1]?.value??0;
  const edS=effectiveDimensionalitySeries[0]?.value??0;
  const edE=effectiveDimensionalitySeries[effectiveDimensionalitySeries.length-1]?.value??0;

  return (
    <div>
      {/* Panneaux blocs */}
      <FT text="Registre \u00e9motionnel dominant par bloc — % des interventions"/>
      <Leg items={BLOCS.map(b=>({color:BC[b],sym:SYM[b],label:BL[b]}))}/>

      <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:1,borderTop:`1px solid ${RL}`,marginBottom:30}}>
        {BLOCS.map(bloc=>{
          type EK=keyof typeof emotionalRegisterByBloc;
          const vals=emotionalRegisterByBloc[bloc as EK];
          const ents=(Object.entries(vals) as [string,number][]).sort((a,b)=>b[1]-a[1]);
          const [mk,mv]=ents[0];
          const col=BC[bloc]??DIM;
          return (
            <div key={bloc} style={{borderTop:`2px solid ${col}`,paddingTop:11,paddingRight:8,paddingBottom:10}}>
              {/* Bloc header */}
              <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:3}}>
                <span style={{fontSize:12,color:col,lineHeight:1}}>{SYM[bloc]}</span>
                <span style={{fontFamily:NM,fontSize:9.5,color:INK}}>{BL[bloc]}</span>
              </div>
              <div style={{fontFamily:NM,fontSize:7,textTransform:'uppercase',letterSpacing:'0.07em',color:DIM,marginBottom:7}}>
                {EL[mk]??mk}
              </div>
              <div style={{fontFamily:NM,fontSize:30,color:col,letterSpacing:'-0.02em',lineHeight:1,marginBottom:13}}>
                {mv.toFixed(0)}%
              </div>
              {ents.map(([reg,val])=>{
                const isDom=reg===mk;
                return (
                  <div key={reg} style={{display:'grid',gridTemplateColumns:'70px 1fr 24px',gap:3,alignItems:'center',marginBottom:5}}>
                    <span style={{fontFamily:NM,fontSize:8,color:isDom?INK:MID}}>{EL[reg]??reg}</span>
                    <div style={{position:'relative',height:10}}>
                      <div style={{position:'absolute',left:0,top:0,bottom:0,width:`${(val/mv)*100}%`,backgroundColor:isDom?col:'#F2F2F2',backgroundImage:isDom?'none':H_NSIG}}/>
                    </div>
                    <span style={{fontFamily:NM,fontSize:7.5,color:isDom?col:DIM,textAlign:'right'}}>{val.toFixed(1)}</span>
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
      <Src text="Classifieur BERT · 577 d\u00e9put\u00e9s · 2023–2026"/>

      <Gap/>

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:44}}>
        {/* VAD */}
        <div>
          <FT text="Gap affectif VAD — mont\u00e9e depuis oct. 2023"/>
          <svg viewBox={`0 0 ${SVW} ${SVH}`} style={{width:'100%',height:SVH+4,display:'block'}} aria-hidden>
            {[0.25,0.5,0.75].map(f=>(
              <line key={f} x1="0" y1={pad+f*(SVH-pad*2)} x2={SVW} y2={pad+f*(SVH-pad*2)} stroke={RL} strokeWidth="0.75" strokeDasharray="2,3"/>
            ))}
            <line x1="0" y1={SVH} x2={SVW} y2={SVH} stroke={RL} strokeWidth="1"/>
            <path d={pts} fill="none" stroke={RD} strokeWidth="1.5" strokeLinejoin="round" strokeLinecap="round"/>
            {/* □ début */}
            <rect x="-3" y={yOf(vadS)-3} width="6" height="6" fill={WH} stroke={INK} strokeWidth="1.5"/>
            {/* ● fin */}
            <circle cx={SVW} cy={yOf(vadE)} r="4" fill={RD}/>
          </svg>
          <div style={{display:'flex',justifyContent:'space-between',fontFamily:NM,fontSize:7.5,color:DIM,marginTop:5}}>
            <span style={{display:'flex',alignItems:'center',gap:5}}>
              <span style={{display:'inline-block',width:8,height:8,border:`1.5px solid ${INK}`,backgroundColor:WH}}/>
              oct. 2023 · {vadS.toFixed(3)}
            </span>
            <span style={{display:'flex',alignItems:'center',gap:5}}>
              <span style={{display:'inline-block',width:8,height:8,borderRadius:'50%',backgroundColor:RD}}/>
              janv. 2026 · {vadE.toFixed(3)}
            </span>
          </div>
          <Src text="Distance VAD (Valence-Arousal-Dominance) · gap inter-blocs"/>
        </div>

        {/* Ec / ED */}
        <div>
          <FT text="Entropie Ec et dimensionnalit\u00e9 ED — stables"/>
          {([['Entropie Ec',ecS,ecE],['Dim. effective ED',edS,edE]] as const).map(([lb,s,e])=>(
            <div key={String(lb)} style={{borderTop:`1px solid ${RL}`,padding:'13px 0'}}>
              <div style={{fontFamily:NM,fontSize:7.5,textTransform:'uppercase',letterSpacing:'0.1em',color:DIM,marginBottom:9}}>{lb}</div>
              <div style={{display:'flex',alignItems:'baseline',gap:12}}>
                <span style={{display:'flex',alignItems:'center',gap:6}}>
                  <span style={{display:'inline-block',width:7,height:7,border:`1.5px solid ${INK}`,backgroundColor:WH,flexShrink:0}}/>
                  <span style={{fontFamily:NM,fontSize:20,color:INK}}>{Number(s).toFixed(3)}</span>
                </span>
                <span style={{fontFamily:NM,fontSize:10,color:DIM}}>→</span>
                <span style={{display:'flex',alignItems:'center',gap:6}}>
                  <span style={{display:'inline-block',width:7,height:7,borderRadius:'50%',backgroundColor:INK,flexShrink:0}}/>
                  <span style={{fontFamily:NM,fontSize:20,color:INK}}>{Number(e).toFixed(3)}</span>
                </span>
              </div>
            </div>
          ))}
          <div style={{fontFamily:NM,fontSize:10.5,color:MID,lineHeight:1.8,marginTop:10,borderTop:`1px solid ${RL}`,paddingTop:10}}>
            □ = oct. 2023 \u2003 ● = janv. 2026<br/>
            Structure stable. Intensit\u00e9 en hausse.
          </div>
        </div>
      </div>
    </div>
  );
}
