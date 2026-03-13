import React, { useState } from 'react';
import {
  EditorialFigure1VariantA,
  EditorialFigure1VariantB,
  EditorialFigure1VariantC,
} from './EditorialFigure1Variants';

type VariantKey = 'A' | 'B' | 'C';

const VARIANTS: { key: VariantKey; label: string; desc: string }[] = [
  {
    key: 'A',
    label: 'Duo intégré',
    desc: 'Bichromie stricte, marge analytique droite, champ unique',
  },
  {
    key: 'B',
    label: 'Séparation',
    desc: 'Bordeaux / marine, rupture nette, bande analytique en bas',
  },
  {
    key: 'C',
    label: 'Condensation',
    desc: 'Gamme chaude, dense, marge intégrée',
  },
];

export function Figure1VariantsShowcase() {
  const [active, setActive] = useState<VariantKey>('A');

  return (
    <div
      style={{
        maxWidth: 900,
        margin: '0 auto',
        padding: '24px 20px 64px',
      }}
    >
      <div
        style={{
          marginBottom: 24,
          display: 'flex',
          gap: 12,
          flexWrap: 'wrap',
          borderBottom: '1px solid #e0dfdc',
          paddingBottom: 16,
        }}
      >
        {VARIANTS.map(({ key, label, desc }) => (
          <button
            key={key}
            type="button"
            onClick={() => setActive(key)}
            style={{
              padding: '8px 14px',
              border: `1px solid ${active === key ? '#1a1a18' : '#c8c6c2'}`,
              background: active === key ? '#1a1a18' : 'transparent',
              color: active === key ? '#ffffff' : '#1a1a18',
              fontFamily: '"IBM Plex Sans", sans-serif',
              fontSize: 12,
              fontWeight: 500,
              cursor: 'pointer',
            }}
          >
            {label}
          </button>
        ))}
      </div>

      <div style={{ marginBottom: 12 }}>
        <p
          style={{
            margin: 0,
            fontFamily: '"IBM Plex Sans", sans-serif',
            fontSize: 11,
            color: '#6a6966',
          }}
        >
          {VARIANTS.find((v) => v.key === active)?.desc}
        </p>
        {active === 'B' && (
          <p
            style={{
              margin: '4px 0 0',
              fontFamily: '"IBM Plex Sans", sans-serif',
              fontSize: 10,
              color: '#4a4946',
              fontStyle: 'italic',
            }}
          >
            Recommandation : articule le mieux les deux preuves, palette la plus décidée.
          </p>
        )}
      </div>

      <div
        style={{
          padding: 24,
          backgroundColor: '#f8f7f5',
          border: '1px solid #e8e7e4',
        }}
      >
        {active === 'A' && <EditorialFigure1VariantA />}
        {active === 'B' && <EditorialFigure1VariantB />}
        {active === 'C' && <EditorialFigure1VariantC />}
      </div>
    </div>
  );
}
