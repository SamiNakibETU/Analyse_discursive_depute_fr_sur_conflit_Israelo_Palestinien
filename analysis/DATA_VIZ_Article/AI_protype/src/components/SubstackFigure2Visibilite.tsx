import React from 'react';
import { Card } from './Card';
import { blocColors, blocLabels, tweetsPerDeputy, twitterVsAnByBloc, visibilityByQuintile } from '../data/article1';

const maxTweets = Math.max(...tweetsPerDeputy.map((d) => d.value));
const maxVisibility = Math.max(...visibilityByQuintile.map((d) => d.value));

export function SubstackFigure2Visibilite() {
  return (
    <Card className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h3 className="font-sans font-semibold text-[18px] text-text-primary mb-2">
            Activite differentielle sur X
          </h3>
          <p className="font-sans text-[13px] text-text-secondary mb-5">
            Nombre moyen de tweets par depute. Le volume d&apos;emission est tres asymetrique.
          </p>
          <div className="space-y-3">
            {tweetsPerDeputy.map((row) => (
              <div key={row.bloc} className="grid grid-cols-[150px_1fr_auto] gap-3 items-center">
                <div className="font-sans text-[12px]" style={{ color: blocColors[row.bloc] }}>
                  {blocLabels[row.bloc]}
                </div>
                <div className="h-5 bg-subtle rounded overflow-hidden border border-border">
                  <div
                    className="h-full rounded"
                    style={{
                      width: `${(row.value / maxTweets) * 100}%`,
                      background: blocColors[row.bloc],
                    }}
                  />
                </div>
                <div className="font-mono text-[12px] text-text-primary">{row.value.toFixed(1)}</div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="font-sans font-semibold text-[18px] text-text-primary mb-2">
            Paradoxe de visibilite
          </h3>
          <p className="font-sans text-[13px] text-text-secondary mb-5">
            Plus un depute est visible, plus son |stance| moyen est eleve.
          </p>
          <div className="space-y-3">
            {visibilityByQuintile.map((row) => (
              <div key={row.quintile} className="grid grid-cols-[145px_1fr_auto] gap-3 items-center">
                <div className="font-sans text-[12px] text-text-secondary">{row.quintile}</div>
                <div className="h-5 bg-subtle rounded overflow-hidden border border-border">
                  <div
                    className="h-full rounded bg-accent"
                    style={{ width: `${(row.value / maxVisibility) * 100}%` }}
                  />
                </div>
                <div className="font-mono text-[12px] text-text-primary">{row.value.toFixed(2)}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="border border-border rounded-card p-4 bg-subtle/35">
        <h4 className="font-sans font-medium text-[14px] text-text-primary mb-3">
          Twitter vs Assemblee (delta stance Twitter - AN)
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {twitterVsAnByBloc.map((row) => (
            <div key={row.bloc} className="flex items-center justify-between border-b border-border/60 pb-2">
              <span className="font-sans text-[12px]" style={{ color: blocColors[row.bloc] }}>
                {blocLabels[row.bloc]}
              </span>
              <span className="font-mono text-[12px] text-text-primary">
                {row.delta >= 0 ? '+' : ''}
                {row.delta.toFixed(2)} {row.significant ? '(p<0.05)' : '(n.s.)'}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
