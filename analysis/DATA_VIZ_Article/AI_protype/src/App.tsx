import type { CSSProperties } from 'react';

const SANS = '"Archivo", "IBM Plex Sans", system-ui, sans-serif';
const MONO = '"Necto Mono", "IBM Plex Mono", monospace';

type Track = {
  id: 'A' | 'B' | 'C';
  title: string;
  subtitle: string;
  palette: [string, string, string, string];
  note: string;
};

const TRACKS: Track[] = [
  {
    id: 'A',
    title: 'Port City Atlas x Swiss Editorial',
    subtitle: 'Planche calme, cartographique, multicouche, lisible sans simplification.',
    palette: ['#F6F6F2', '#121419', '#1D4F8D', '#D8D0C2'],
    note: 'Contour lines, rails, dot-field, hierarchy silencieuse.',
  },
  {
    id: 'B',
    title: 'Le Point x Port City Atlas',
    subtitle: 'Energie dossier presse + rigueur atlas, dense mais tenue.',
    palette: ['#FBFBFA', '#111318', '#B70F2D', '#204A8A'],
    note: 'Intertitres forts, preuves compactes, figure maitresse editoriale.',
  },
  {
    id: 'C',
    title: 'Joost x Atlas Contemporain',
    subtitle: 'Architecture dure, contrastes nets, systeme visuel auteur.',
    palette: ['#F8F8FC', '#0A0B10', '#000BFF', '#FF0004'],
    note: 'Modules stricts, peigne, punctum, macro/micro tension.',
  },
];

export function App() {
  return (
    <main style={{ minHeight: '100vh', background: '#FFFFFF', color: '#0A0B10', fontFamily: SANS }}>
      <div style={{ maxWidth: 1440, margin: '0 auto', padding: '24px 22px 48px' }}>
        <header style={{ borderBottom: '1px solid #0A0B10', paddingBottom: 12, marginBottom: 18 }}>
          <p style={{ margin: 0, fontFamily: MONO, fontSize: 10, letterSpacing: '0.1em', color: '#636674' }}>
            VISUAL LANGUAGE PROPOSALS / EDITORIAL BOARDS / NO GENERIC SYSTEM CARDS
          </p>
          <h1 style={{ margin: '8px 0 6px', fontSize: 38, lineHeight: 0.96, letterSpacing: '-0.02em', fontWeight: 500 }}>
            Trois planches editoriales incarnees
          </h1>
          <p style={{ margin: 0, fontFamily: MONO, fontSize: 11, color: '#3D404A' }}>
            A: Port City Atlas x Swiss editorial / B: Le Point x Port City Atlas / C: Joost x atlas contemporain
          </p>
        </header>

        {TRACKS.map((t) => (
          <EditorialBoard key={t.id} t={t} />
        ))}
      </div>
    </main>
  );
}

function EditorialBoard({ t }: { t: Track }) {
  const [paper, ink, accentA, accentB] = t.palette;
  return (
    <section
      style={{
        marginBottom: 28,
        border: `1px solid ${ink}`,
        background: paper,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div style={gridOverlay(t.id, ink)} />

      <header
        style={{
          position: 'relative',
          zIndex: 2,
          borderBottom: `1px solid ${ink}`,
          background: '#FFFFFFE6',
          backdropFilter: 'blur(1px)',
          padding: '14px 16px 12px',
          display: 'grid',
          gridTemplateColumns: '1fr auto',
          gap: 10,
          alignItems: 'end',
        }}
      >
        <div style={{ display: 'grid', gap: 6 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
            <span style={{ width: 10, height: 10, background: ink }} />
            <span style={{ width: 10, height: 10, background: accentA }} />
            <span style={{ width: 10, height: 10, background: accentB }} />
            <span style={{ fontFamily: MONO, fontSize: 10, letterSpacing: '0.09em', color: '#5E616C' }}>DIRECTION {t.id}</span>
          </div>
          <h2 style={{ margin: 0, fontSize: 32, lineHeight: 0.95, letterSpacing: '-0.02em', fontWeight: 500 }}>{t.title}</h2>
          <p style={{ margin: 0, fontFamily: MONO, fontSize: 11, color: '#3C3F49' }}>{t.subtitle}</p>
        </div>
        <div style={{ border: `1px solid ${ink}`, padding: '5px 8px', fontFamily: MONO, fontSize: 10, letterSpacing: '0.08em', background: '#FFFFFF' }}>
          {t.note}
        </div>
      </header>

      <div style={{ position: 'relative', zIndex: 2, padding: 12, display: 'grid', gap: 12 }}>
        {t.id === 'A' && <PortCitySwiss ink={ink} a={accentA} b={accentB} />}
        {t.id === 'B' && <LePointAtlas ink={ink} a={accentA} b={accentB} />}
        {t.id === 'C' && <JoostAtlas ink={ink} a={accentA} b={accentB} />}
      </div>
    </section>
  );
}

function PortCitySwiss({ ink, a, b }: { ink: string; a: string; b: string }) {
  return (
    <>
      <div style={cols('8fr 4fr', 10)}>
        <article style={panel(ink)}>
          <Kicker text="Couche 1  -  Ils ne parlent pas de la meme chose" ink={ink} />
          <h3 style={figureTitle}>Les cadres dominants structurent deja la fracture</h3>
          <p style={deck}>
            77% humanitaire a gauche radicale, 45% securitaire a droite. Le centre se distribue entre les deux poles
            avec un registre moral intermediaire.
          </p>
          <StackedBars ink={ink} accent={a} alt={b} styleMode="contour" />
          <LegendStrip ink={ink} a={a} b={b} mode="shape-first" />
        </article>
        <aside style={panel(ink)}>
          <Kicker text="Preuve lexicale compacte" ink={ink} />
          <WordContrast ink={ink} a={a} b={b} />
        </aside>
      </div>

      <div style={cols('7fr 5fr', 10)}>
        <article style={panel(ink)}>
          <Kicker text="Atlas layer" ink={ink} />
          <h3 style={figureTitle}>Superposition lisible des signaux</h3>
          <ContourMatrix ink={ink} a={a} />
        </article>
        <article style={panel(ink)}>
          <Kicker text="Rythme editorial" ink={ink} />
          <TimelineShock ink={ink} a={a} b={b} calm />
        </article>
      </div>
    </>
  );
}

function LePointAtlas({ ink, a, b }: { ink: string; a: string; b: string }) {
  return (
    <>
      <div style={cols('1fr', 10)}>
        <article style={{ ...panel(ink), padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: 10, borderBottom: `1px solid ${ink}`, display: 'grid', gridTemplateColumns: '9fr 3fr', gap: 10 }}>
            <div>
              <Kicker text="Grande figure de dossier" ink={ink} />
              <h3 style={figureTitle}>Le biais de visibilite en ligne deformant l image de l hemicycle</h3>
              <p style={deck}>
                122 tweets/depute chez LFI contre 17 au centre. Le public voit un debat amplifie par la suractivite d un seul bloc.
              </p>
            </div>
            <div style={{ borderLeft: `1px solid ${ink}`, paddingLeft: 10 }}>
              <div style={{ fontFamily: MONO, fontSize: 45, lineHeight: 0.9, color: a }}>122</div>
              <div style={{ fontFamily: MONO, fontSize: 11 }}>tweets / depute</div>
            </div>
          </div>

          <div style={{ padding: 10, display: 'grid', gap: 10 }}>
            <DualFigure ink={ink} a={a} b={b} />
            <LegendStrip ink={ink} a={a} b={b} mode="press" />
          </div>
        </article>
      </div>

      <div style={cols('6fr 6fr', 10)}>
        <article style={panel(ink)}>
          <Kicker text="Section chocs" ink={ink} />
          <h3 style={figureTitle}>Chocs ponctuels, pas de convergence lente</h3>
          <TimelineShock ink={ink} a={a} b={b} />
        </article>
        <article style={panel(ink)}>
          <Kicker text="Section affects" ink={ink} />
          <h3 style={figureTitle}>Architecture affective stable, temperature en hausse</h3>
          <EmotionSplit ink={ink} a={a} b={b} />
        </article>
      </div>
    </>
  );
}

function JoostAtlas({ ink, a, b }: { ink: string; a: string; b: string }) {
  return (
    <>
      <div style={cols('5fr 7fr', 10)}>
        <article style={{ ...panel(ink), background: '#FFFFFF' }}>
          <Kicker text="System block / macro" ink={ink} />
          <h3 style={figureTitle}>Structure orthogonale, lecture immediate</h3>
          <div style={{ display: 'grid', gap: 8 }}>
            <div style={{ border: `1px solid ${ink}`, display: 'grid', gridTemplateColumns: '1fr 1fr', height: 62 }}>
              <div style={{ borderRight: `1px solid ${ink}`, background: peigneFill(ink) }} />
              <div style={{ background: '#F4F4FA' }} />
            </div>
            <div style={{ fontFamily: MONO, fontSize: 11 }}>■ principal  ● contexte  ▲ event  ◆ anomalie</div>
          </div>
        </article>
        <article style={panel(ink)}>
          <Kicker text="Figure centrale / micro-valeurs" ink={ink} />
          <h3 style={figureTitle}>Les preuves restent denses sans perdre la trajectoire</h3>
          <StackedBars ink={ink} accent={a} alt={b} styleMode="joost" />
          <TimelineShock ink={ink} a={a} b={b} />
        </article>
      </div>

      <div style={cols('4fr 4fr 4fr', 10)}>
        <article style={panel(ink)}>
          <Kicker text="Matrice" ink={ink} />
          <ContourMatrix ink={ink} a={a} />
        </article>
        <article style={panel(ink)}>
          <Kicker text="Lexique" ink={ink} />
          <WordContrast ink={ink} a={a} b={b} />
        </article>
        <article style={panel(ink)}>
          <Kicker text="Legende codee" ink={ink} />
          <LegendStrip ink={ink} a={a} b={b} mode="module" />
          <div style={{ marginTop: 8, fontFamily: MONO, fontSize: 11 }}>
            sequence: titre {'>'} preuve {'>'} contre-preuve {'>'} source
          </div>
        </article>
      </div>
    </>
  );
}

function StackedBars({
  ink,
  accent,
  alt,
  styleMode,
}: {
  ink: string;
  accent: string;
  alt: string;
  styleMode: 'contour' | 'joost';
}) {
  const rows = [
    ['Gauche radicale', 77, 14, 9],
    ['Centre', 34, 29, 37],
    ['Droite', 18, 45, 37],
  ] as const;

  return (
    <div style={{ display: 'grid', gap: 8 }}>
      {rows.map(([label, x, y, z]) => (
        <div key={label} style={{ display: 'grid', gridTemplateColumns: '116px 1fr 40px', gap: 8, alignItems: 'center' }}>
          <span style={{ fontFamily: MONO, fontSize: 11 }}>{label}</span>
          <div style={{ height: 16, border: `1px solid ${ink}`, display: 'flex' }}>
            <div style={{ width: `${x}%`, background: accent }} />
            <div style={{ width: `${y}%`, background: styleMode === 'joost' ? alt : '#FFFFFF', backgroundImage: styleMode === 'contour' ? diagFill(ink) : 'none' }} />
            <div style={{ width: `${z}%`, background: '#FFFFFF', backgroundImage: dotFill(ink), backgroundSize: '7px 7px' }} />
          </div>
          <span style={{ fontFamily: MONO, fontSize: 11 }}>{x}</span>
        </div>
      ))}
    </div>
  );
}

function DualFigure({ ink, a, b }: { ink: string; a: string; b: string }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '7fr 5fr', gap: 10 }}>
      <div>
        <StackedBars ink={ink} accent={a} alt={b} styleMode="contour" />
      </div>
      <div style={{ border: `1px solid ${ink}`, padding: 8 }}>
        <div style={{ fontFamily: MONO, fontSize: 10, color: '#666974', marginBottom: 5 }}>Ecart hemicycle vs X</div>
        {[
          ['LFI', '+0.50'],
          ['EELV', '+0.08'],
          ['REN', '+0.01'],
          ['LR', '-0.02'],
        ].map(([k, v]) => (
          <div key={k} style={{ display: 'grid', gridTemplateColumns: '1fr auto', fontFamily: MONO, fontSize: 11, marginBottom: 4 }}>
            <span>{k}</span>
            <span style={{ color: k === 'LFI' ? a : ink }}>{v}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function WordContrast({ ink, a, b }: { ink: string; a: string; b: string }) {
  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
        <div style={{ border: `1px solid ${ink}`, padding: 8, background: '#FFFFFF' }}>
          <div style={{ fontFamily: MONO, fontSize: 10, color: '#646874', marginBottom: 6 }}>Univers 1</div>
          <div style={{ fontFamily: SANS, fontSize: 19, lineHeight: 1.05, color: a }}>gaza</div>
          <div style={{ fontFamily: SANS, fontSize: 16, lineHeight: 1.05 }}>genocide</div>
          <div style={{ fontFamily: SANS, fontSize: 14, lineHeight: 1.05 }}>massacres</div>
        </div>
        <div style={{ border: `1px solid ${ink}`, padding: 8, background: '#FFFFFF' }}>
          <div style={{ fontFamily: MONO, fontSize: 10, color: '#646874', marginBottom: 6 }}>Univers 2</div>
          <div style={{ fontFamily: SANS, fontSize: 19, lineHeight: 1.05, color: b }}>hamas</div>
          <div style={{ fontFamily: SANS, fontSize: 16, lineHeight: 1.05 }}>terroristes</div>
          <div style={{ fontFamily: SANS, fontSize: 14, lineHeight: 1.05 }}>antisemitisme</div>
        </div>
      </div>
      <div style={{ fontFamily: MONO, fontSize: 11 }}>rho = 0.046 {'>'} registre discursif et position restent quasi independants</div>
    </div>
  );
}

function TimelineShock({ ink, a, b, calm }: { ink: string; a: string; b: string; calm?: boolean }) {
  return (
    <svg viewBox="0 0 620 140" style={{ width: '100%', height: 140, border: `1px solid ${ink}`, background: calm ? '#FFFFFF' : '#FAFAFD' }}>
      <line x1={40} y1={112} x2={592} y2={112} stroke={ink} />
      <line x1={40} y1={22} x2={40} y2={112} stroke={ink} />
      <polyline fill="none" stroke={a} strokeWidth="2" points="40,78 102,74 164,76 226,64 288,66 350,44 412,56 474,52 536,48 592,50" />
      <polyline fill="none" stroke={ink} strokeWidth="1.6" points="40,90 102,88 164,86 226,83 288,82 350,78 412,81 474,79 536,77 592,76" />
      <polyline fill="none" stroke={b} strokeWidth="1.5" points="40,96 102,95 164,94 226,92 288,91 350,86 412,90 474,88 536,84 592,82" />
      <line x1={226} y1={18} x2={226} y2={112} stroke={ink} strokeDasharray="3 3" />
      <line x1={350} y1={18} x2={350} y2={112} stroke={ink} strokeDasharray="3 3" />
      <line x1={536} y1={18} x2={536} y2={112} stroke={ink} strokeDasharray="3 3" />
      <text x={210} y={16} fontFamily={MONO} fontSize="10" fill={ink}>CIJ</text>
      <text x={336} y={16} fontFamily={MONO} fontSize="10" fill={ink}>Rafah</text>
      <text x={503} y={16} fontFamily={MONO} fontSize="10" fill={ink}>Ceasefire</text>
    </svg>
  );
}

function EmotionSplit({ ink, a, b }: { ink: string; a: string; b: string }) {
  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
        <div style={{ border: `1px solid ${ink}`, padding: 8 }}>
          <div style={{ fontFamily: MONO, fontSize: 10, marginBottom: 5 }}>Architecture stable</div>
          <StackedBars ink={ink} accent={a} alt={b} styleMode="contour" />
        </div>
        <div style={{ border: `1px solid ${ink}`, padding: 8 }}>
          <div style={{ fontFamily: MONO, fontSize: 10, marginBottom: 5 }}>Temperature monte</div>
          <div style={{ fontFamily: MONO, fontSize: 36, lineHeight: 0.9, color: a }}>x2</div>
          <div style={{ fontFamily: MONO, fontSize: 11 }}>gap VAD oct-2023 {'>'} jan-2026</div>
        </div>
      </div>
    </div>
  );
}

function ContourMatrix({ ink, a }: { ink: string; a: string }) {
  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(8,1fr)', gap: 2 }}>
        {Array.from({ length: 56 }, (_, i) => (
          <div
            key={i}
            style={{
              aspectRatio: '1 / 1',
              border: `1px solid ${ink}`,
              background: i % 9 === 0 ? '#FFFFFF' : '#F5F6FA',
              backgroundImage: i % 7 === 0 ? peigneFill(ink) : i % 5 === 0 ? dotFill(ink) : i % 4 === 0 ? diagFill(ink) : 'none',
              backgroundSize: i % 5 === 0 ? '7px 7px' : undefined,
            }}
          />
        ))}
      </div>
      <div style={{ fontFamily: MONO, fontSize: 11, color: a }}>
        lecture en couches: contour {'>'} trame {'>'} valeur {'>'} ecart
      </div>
    </div>
  );
}

function LegendStrip({ ink, a, b, mode }: { ink: string; a: string; b: string; mode: 'shape-first' | 'press' | 'module' }) {
  const text =
    mode === 'shape-first'
      ? '■ humanitaire  ● securitaire  ▲ moral  ◆ ecart'
      : mode === 'press'
        ? '■ position hemicycle  ● position X  ▲ deplacement  ◆ significatif'
        : '■ couche active  ● contexte  ▲ event  ◆ anomalie';
  return (
    <div style={{ borderTop: `1px solid ${ink}`, paddingTop: 7, display: 'grid', gridTemplateColumns: '1fr auto', gap: 8, alignItems: 'center' }}>
      <span style={{ fontFamily: MONO, fontSize: 11 }}>{text}</span>
      <span style={{ display: 'flex', gap: 5 }}>
        <i style={dot(ink)} />
        <i style={dot(a)} />
        <i style={dot(b)} />
      </span>
    </div>
  );
}

function Kicker({ text, ink }: { text: string; ink: string }) {
  return (
    <div style={{ fontFamily: MONO, fontSize: 10, letterSpacing: '0.08em', color: '#5F626E', marginBottom: 6 }}>
      <span style={{ display: 'inline-block', width: 9, height: 9, background: ink, marginRight: 6 }} />
      {text.toUpperCase()}
    </div>
  );
}

const figureTitle: CSSProperties = {
  margin: '0 0 6px',
  fontFamily: SANS,
  fontWeight: 500,
  fontSize: 27,
  lineHeight: 0.95,
  letterSpacing: '-0.015em',
};

const deck: CSSProperties = {
  margin: 0,
  fontFamily: MONO,
  fontSize: 11,
  lineHeight: 1.45,
  color: '#3E414B',
};

function panel(ink: string): CSSProperties {
  return {
    border: `1px solid ${ink}`,
    background: '#FFFFFF',
    padding: 10,
    position: 'relative',
  };
}

function cols(template: string, gap: number): CSSProperties {
  return { display: 'grid', gridTemplateColumns: template, gap };
}

function gridOverlay(id: Track['id'], ink: string): CSSProperties {
  const size = id === 'C' ? '56px 100%, 100% 20px' : id === 'B' ? '70px 100%, 100% 24px' : '76px 100%, 100% 24px';
  return {
    position: 'absolute',
    inset: 0,
    pointerEvents: 'none',
    backgroundImage:
      `linear-gradient(to right, ${ink}14 1px, transparent 1px), linear-gradient(to bottom, ${ink}10 1px, transparent 1px)`,
    backgroundSize: size,
  };
}

function dot(c: string): CSSProperties {
  return { width: 10, height: 10, border: '1px solid #0A0B10', background: c, display: 'inline-block' };
}

function diagFill(ink: string): string {
  return `repeating-linear-gradient(45deg, ${ink}55 0, ${ink}55 1px, transparent 1px, transparent 6px)`;
}

function dotFill(ink: string): string {
  return `radial-gradient(${ink} 1px, transparent 1px)`;
}

function peigneFill(ink: string): string {
  return `repeating-linear-gradient(90deg, ${ink}22 0, ${ink}22 2px, transparent 2px, transparent 6px)`;
}
