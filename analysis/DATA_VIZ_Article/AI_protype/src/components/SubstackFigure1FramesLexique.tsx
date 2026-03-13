import React from 'react';
import { Card } from './Card';
import { ButterflyChart } from './ButterflyChart';
import { blocColors, blocLabels, frameRows, lexicalContrast } from '../data/article1';

const frameSegments = [
  { key: 'HUM', label: 'Humanitaire', color: '#087443' },
  { key: 'SEC', label: 'Securitaire', color: '#1D4ED8' },
  { key: 'MOR', label: 'Moral', color: '#7E22CE' },
  { key: 'OTH', label: 'Autres', color: '#CBD5E1' },
] as const;

export function SubstackFigure1FramesLexique() {
  return (
    <Card className="space-y-8">
      <div>
        <h3 className="font-sans font-semibold text-[18px] text-text-primary mb-2">
          Cadrages dominants par bloc
        </h3>
        <p className="font-sans text-[13px] text-text-secondary mb-5">
          Chaque barre represente 100% du discours du bloc. Les segments montrent les
          familles de cadrage.
        </p>

        <div className="space-y-3">
          {frameRows.map((row) => (
            <div key={row.bloc} className="grid grid-cols-[150px_1fr] gap-3 items-center">
              <div
                className="font-sans text-[12px] font-medium"
                style={{ color: blocColors[row.bloc] }}
              >
                {blocLabels[row.bloc]}
              </div>
              <div className="h-6 w-full rounded overflow-hidden border border-border flex">
                {frameSegments.map((segment) => (
                  <div
                    key={segment.key}
                    style={{
                      width: `${row[segment.key]}%`,
                      background: segment.color,
                    }}
                    title={`${segment.label}: ${row[segment.key].toFixed(1)}%`}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="flex flex-wrap gap-3 mt-4">
          {frameSegments.map((segment) => (
            <div key={segment.key} className="flex items-center gap-2">
              <span
                className="w-3 h-3 rounded-sm"
                style={{ background: segment.color }}
                aria-hidden
              />
              <span className="font-sans text-[11px] text-text-muted">{segment.label}</span>
            </div>
          ))}
        </div>
      </div>

      <ButterflyChart
        data={lexicalContrast}
        title="Lexiques les plus discriminants"
        subtitle="Top mots sur-representes (z-score) entre les poles du debat."
        source="Source: fighting_words.csv. Le score z mesure le pouvoir discriminant du mot."
      />
    </Card>
  );
}
