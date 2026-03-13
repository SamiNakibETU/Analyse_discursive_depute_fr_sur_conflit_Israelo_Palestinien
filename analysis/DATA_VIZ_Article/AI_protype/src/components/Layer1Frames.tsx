import {
  blocLabels,
  frameRows,
  lexicalContrast,
  registerPositionCorrelation,
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
const FRAME_COLORS = {
  HUM: '#2055A5',
  SEC: '#C8102E',
  MOR: '#7A7A7A',
  OTH: '#BDB9AD',
} as const;

const FRAME_LABELS = {
  HUM: 'Humanitaire',
  SEC: 'Sécuritaire',
  MOR: 'Moral',
  OTH: 'Autres',
} as const;

const SEGS = ['HUM', 'SEC', 'MOR', 'OTH'] as const;
type Seg = (typeof SEGS)[number];

const KEY_PAIRS = [
  { gauche: 'gaza',      droite: 'hamas'        },
  { gauche: 'génocide',  droite: 'terroristes'  },
  { gauche: 'massacres', droite: 'antisémitisme' },
];

function dominant(row: (typeof frameRows)[0]): { k: Seg; v: number } {
  return SEGS.map((k) => ({ k, v: row[k] })).reduce((a, b) => (b.v > a.v ? b : a));
}

/* ─── Composant ─────────────────────────────────────────────────── */
export function Layer1Frames() {
  const maxZ = Math.max(
    ...KEY_PAIRS.flatMap((p) => [
      lexicalContrast.gauche.find((d) => d.word === p.gauche)?.z ?? 0,
      lexicalContrast.droite.find((d) => d.word === p.droite)?.z ?? 0,
    ]),
  );

  return (
    <section style={{ borderTop: `3px solid ${ACCENT}`, paddingTop: 20 }}>

      {/* ── Kicker ── */}
      <div style={{ fontFamily: MONO, fontSize: 9, color: ACCENT, letterSpacing: '0.18em', textTransform: 'uppercase', marginBottom: 14, fontWeight: 700 }}>
        I&ensp;—&ensp;Cadrage discursif
      </div>

      {/* ── Titre ── */}
      <h2 style={{ margin: '0 0 22px', fontFamily: MATTONE, fontSize: 44, lineHeight: 0.96, letterSpacing: '-0.01em', color: INK, fontWeight: 900 }}>
        Ils ne parlent pas de la même chose
      </h2>

      {/* ── Chapeau 2 colonnes ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, marginBottom: 22 }}>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          77&nbsp;% du discours de la gauche radicale est cadré «&nbsp;humanitaire&nbsp;».
          45&nbsp;% de la droite est cadré «&nbsp;sécuritaire&nbsp;». Le centre se répartit
          entre trois registres sans dominant net. Ce ne sont pas les mêmes conflits qui sont décrits.
        </p>
        <p style={{ margin: 0, fontFamily: SANS, fontSize: 14, lineHeight: 1.65, color: MID }}>
          Les fighting words révèlent deux univers lexicaux irréconciliables&nbsp;:
          «&nbsp;génocide&nbsp;/&nbsp;massacres&nbsp;» contre «&nbsp;terroristes&nbsp;/&nbsp;antisémitisme&nbsp;».
          La corrélation registre&nbsp;↔&nbsp;position (ρ&nbsp;=&nbsp;0,046) confirme que le ton ne prédit pas la position.
        </p>
      </div>

      <div style={{ borderTop: `1px solid ${RULE}`, marginBottom: 22 }} />

      {/* ═══════════════════════════════════════════════════════════
          Figure 1 : Cadres discursifs par bloc (pleine largeur)
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ background: FIG_BG, padding: '18px 22px', marginBottom: 18 }}>

        {/* En-tête figure */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.14em', fontWeight: 700 }}>
            Répartition des cadres discursifs par bloc — % des interventions
          </div>
          {/* Légende inline */}
          <div style={{ display: 'flex', gap: 18, flexShrink: 0, marginLeft: 28 }}>
            {SEGS.map((k) => (
              <span key={k} style={{ display: 'flex', alignItems: 'center', gap: 5, fontFamily: MONO, fontSize: 7.5, color: DIM, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                <span style={{ width: 9, height: 9, backgroundColor: FRAME_COLORS[k], display: 'inline-block', flexShrink: 0 }} />
                {FRAME_LABELS[k]}
              </span>
            ))}
          </div>
        </div>

        {/* Barres empilées */}
        {frameRows.map((row) => {
          const dom = dominant(row);
          let acc = 0;
          return (
            <div
              key={row.bloc}
              style={{ display: 'grid', gridTemplateColumns: '188px 1fr 110px', gap: 0, alignItems: 'center', borderTop: `1px solid rgba(0,0,0,0.07)`, padding: '11px 0' }}
            >
              {/* Étiquette */}
              <div style={{ paddingRight: 18 }}>
                <div style={{ fontFamily: SANS, fontSize: 12, fontWeight: 700, color: INK, marginBottom: 4 }}>
                  {blocLabels[row.bloc]}
                </div>
                <div style={{ fontFamily: MONO, fontSize: 8, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', color: dom.k === 'HUM' ? FRAME_COLORS.HUM : dom.k === 'SEC' ? FRAME_COLORS.SEC : DIM }}>
                  Dominant&nbsp;: {FRAME_LABELS[dom.k]}
                </div>
              </div>

              {/* Barre empilée */}
              <div style={{ position: 'relative', height: 40 }}>
                {[25, 50, 75].map((t) => (
                  <div key={t} aria-hidden style={{ position: 'absolute', left: `${t}%`, top: 0, bottom: 0, width: 1, backgroundColor: 'rgba(255,255,255,0.55)', zIndex: 2 }} />
                ))}
                {SEGS.map((k) => {
                  const sl = acc;
                  const w = row[k];
                  acc += w;
                  return (
                    <div
                      key={k}
                      style={{ position: 'absolute', left: `${sl}%`, width: `${w}%`, top: 0, bottom: 0, backgroundColor: FRAME_COLORS[k], display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', zIndex: 1 }}
                    >
                      {w > 10 && (
                        <span style={{ fontFamily: MONO, fontSize: w > 20 ? 10 : 8.5, fontWeight: 700, color: k === 'OTH' ? MID : 'rgba(255,255,255,0.95)', whiteSpace: 'nowrap' }}>
                          {Math.round(w)}%
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Valeur dominante */}
              <div style={{ paddingLeft: 16, borderLeft: `1px solid rgba(0,0,0,0.1)`, textAlign: 'center' }}>
                <div style={{ fontFamily: MONO, fontSize: 26, fontWeight: 700, letterSpacing: '-0.02em', lineHeight: 1, color: dom.k === 'HUM' ? FRAME_COLORS.HUM : dom.k === 'SEC' ? FRAME_COLORS.SEC : DIM }}>
                  {Math.round(dom.v)}%
                </div>
              </div>
            </div>
          );
        })}

        {/* Axe */}
        <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: MONO, fontSize: 7.5, color: DIM, paddingLeft: 188, marginTop: 7 }}>
          {['0', '25', '50', '75', '100%'].map((v) => <span key={v}>{v}</span>)}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 7.5, color: DIM, marginTop: 9 }}>
          Source&nbsp;: analyse des interventions parlementaires — 577&nbsp;députés, 2023–2026
        </div>
      </div>

      {/* ═══════════════════════════════════════════════════════════
          Second rang : Butterfly + Encadré ρ
      ═══════════════════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 228px', gap: 18, alignItems: 'start' }}>

        {/* Butterfly : mots distinctifs */}
        <div style={{ background: FIG_BG, padding: '18px 22px' }}>
          <div style={{ fontFamily: MONO, fontSize: 8, color: DIM, textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 18, fontWeight: 700 }}>
            Mots discriminants — score Z normalisé par camp politique
          </div>

          {/* En-têtes colonnes */}
          <div style={{ display: 'grid', gridTemplateColumns: '110px 1fr 2px 1fr 110px', gap: 0, marginBottom: 14 }}>
            <div style={{ fontFamily: SANS, fontSize: 11, fontWeight: 700, color: FRAME_COLORS.HUM, textAlign: 'right', paddingRight: 14 }}>
              Gauche
            </div>
            <div />
            <div style={{ background: DIM }} />
            <div />
            <div style={{ fontFamily: SANS, fontSize: 11, fontWeight: 700, color: FRAME_COLORS.SEC, paddingLeft: 14 }}>
              Droite
            </div>
          </div>

          {KEY_PAIRS.map(({ gauche, droite }) => {
            const lw = lexicalContrast.gauche.find((d) => d.word === gauche);
            const rw = lexicalContrast.droite.find((d) => d.word === droite);
            if (!lw || !rw) return null;
            return (
              <div key={gauche} style={{ display: 'grid', gridTemplateColumns: '110px 1fr 2px 1fr 110px', alignItems: 'center', gap: 0, marginBottom: 16 }}>
                <span style={{ fontFamily: SANS, fontSize: 16, fontWeight: 700, color: FRAME_COLORS.HUM, textAlign: 'right', paddingRight: 14 }}>
                  {lw.word}
                </span>
                <div style={{ height: 28, display: 'flex', justifyContent: 'flex-end' }}>
                  <div style={{ width: `${(lw.z / maxZ) * 100}%`, height: '100%', backgroundColor: FRAME_COLORS.HUM }} />
                </div>
                <div style={{ background: DIM, alignSelf: 'stretch' }} />
                <div style={{ height: 28 }}>
                  <div style={{ width: `${(rw.z / maxZ) * 100}%`, height: '100%', backgroundColor: FRAME_COLORS.SEC }} />
                </div>
                <span style={{ fontFamily: SANS, fontSize: 16, fontWeight: 700, color: FRAME_COLORS.SEC, paddingLeft: 14 }}>
                  {rw.word}
                </span>
              </div>
            );
          })}
        </div>

        {/* ── Encadré corrélation ── */}
        <div style={{ border: `1px solid ${RULE}` }}>
          {/* Bandeau rouge */}
          <div style={{ background: ACCENT, padding: '9px 16px' }}>
            <div style={{ fontFamily: MONO, fontSize: 7.5, color: 'rgba(255,255,255,0.85)', textTransform: 'uppercase', letterSpacing: '0.16em', fontWeight: 700 }}>
              Corrélation clé
            </div>
          </div>
          <div style={{ padding: '18px 16px' }}>
            <div style={{ fontFamily: MONO, fontSize: 42, fontWeight: 700, color: INK, letterSpacing: '-0.03em', lineHeight: 1, marginBottom: 6 }}>
              {registerPositionCorrelation.toFixed(3)}
            </div>
            <div style={{ fontFamily: MONO, fontSize: 8, color: ACCENT, textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 700, marginBottom: 14 }}>
              ρ registre ↔ position
            </div>
            <div style={{ borderTop: `1px solid ${RULE}`, paddingTop: 12, fontFamily: SANS, fontSize: 12, color: MID, lineHeight: 1.6 }}>
              Le ton du discours ne prédit pas la position politique. Humanitaire et pro-Gaza ne sont pas synonymes.
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
