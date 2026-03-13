import React from 'react';
import { frameRows, lexicalContrast } from '../data/article1';

const frameSegments = [
  { key: 'HUM', color: '#0b6e4f', label: 'HUM' },
  { key: 'SEC', color: '#1f4fd6', label: 'SEC' },
  { key: 'MOR', color: '#7b2cbf', label: 'MOR' },
  { key: 'OTH', color: '#d9d9d3', label: 'OTH' },
] as const;

function MiniCoreFigure({ compact = false }: { compact?: boolean }) {
  const left = lexicalContrast.gauche.slice(0, compact ? 4 : 6);
  const right = lexicalContrast.droite.slice(0, compact ? 4 : 6);
  const max = Math.max(...left.map((d) => d.z), ...right.map((d) => d.z));

  return (
    <div className={`mini-core ${compact ? 'compact' : ''}`}>
      <div className="mini-frames">
        {frameRows.map((row) => (
          <div key={row.bloc} className="mini-row">
            <span>{row.bloc.replace(' / ', '/')}</span>
            <div className="mini-track">
              {frameSegments.map((seg) => (
                <i
                  key={seg.key}
                  style={{
                    width: `${row[seg.key]}%`,
                    background: seg.color,
                  }}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
      <div className="mini-lex">
        <div className="col left">
          {left.map((d) => (
            <div key={`l-${d.word}`} className="word-row">
              <span>{d.word}</span>
              <i style={{ width: `${(d.z / max) * 100}%` }}>{d.z.toFixed(1)}</i>
            </div>
          ))}
        </div>
        <div className="col right">
          {right.map((d) => (
            <div key={`r-${d.word}`} className="word-row">
              <i style={{ width: `${(d.z / max) * 100}%` }}>{d.z.toFixed(1)}</i>
              <span>{d.word}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function SectionVariantsShowcase() {
  return (
    <div className="variants-page">
      <header className="variants-header">
        <p>Prototype comparatif - meme section, trois directions</p>
        <h1>Couche 1 - Ils ne parlent pas de la meme chose</h1>
      </header>

      <section className="variant-a">
        <p className="tag">A / Presse analytique haut de gamme</p>
        <div className="a-top">
          <h2>Des cadres incompatibles structurent le debat</h2>
          <p>
            Version de lecture continue. Le titre annonce la these, la figure porte la preuve, la
            marge qualifie la robustesse.
          </p>
        </div>
        <div className="a-grid">
          <div className="a-main">
            <MiniCoreFigure />
            <p className="caption">
              La divergence porte autant sur le cadre (humanitaire/securitaire) que sur le
              vocabulaire discriminant.
            </p>
          </div>
          <aside className="a-margin">
            <h4>Note analytique</h4>
            <p>77% de cadrage humanitaire a gauche radicale contre 45% securitaire a droite.</p>
            <h4>Limite</h4>
            <p>
              Les categories de frames simplifient des discours plus hybrides. Elles orientent la
              lecture mais ne l&apos;epuisent pas.
            </p>
          </aside>
        </div>
      </section>

      <section className="variant-b">
        <div className="b-rail">01</div>
        <div className="b-head">
          <p>B / Swiss editorial plus tendu</p>
          <h2>Ils ne parlent pas de la meme chose</h2>
        </div>
        <div className="b-stage">
          <div className="b-notes">
            <p>[1] Divergence de cadrage avant divergence de position.</p>
            <p>[2] Polarites lexicales stables sur la periode.</p>
          </div>
          <MiniCoreFigure compact />
          <div className="b-foot">
            <span>Frames</span>
            <span>Lexique</span>
            <span>Source: corpus AN + X</span>
          </div>
        </div>
      </section>

      <section className="variant-c">
        <div className="c-band">
          <p>C / Revue-magazine analytique signee</p>
          <h2>Deux scenes du meme conflit discursif</h2>
        </div>
        <div className="c-layout">
          <blockquote>
            &quot;Le desaccord n&apos;oppose pas seulement des positions. Il oppose des mondes de
            reference.&quot;
          </blockquote>
          <div className="c-main">
            <MiniCoreFigure />
          </div>
          <div className="c-meta">
            <p>
              La composition assume un geste de revue: ouverture expressive, puis stabilisation
              analytique dans la figure.
            </p>
            <p>Source/methode: frames_par_bloc.csv + fighting_words.csv.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
