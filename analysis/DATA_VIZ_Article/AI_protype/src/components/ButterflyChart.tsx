import React, { useState, useEffect } from 'react';

export interface FightingWord {
  word: string;
  z: number;
}

export interface FightingWordsData {
  gauche: FightingWord[];
  droite: FightingWord[];
}

interface ButterflyChartProps {
  data: FightingWordsData;
  title?: string;
  subtitle?: string;
  source?: string;
}

const COLOR_GAUCHE = 'var(--bloc-gauche)';
const COLOR_DROITE = 'var(--bloc-droite)';

const MOBILE_BREAKPOINT = 640;
const MOBILE_WORDS_LIMIT = 6;

export function ButterflyChart({
  data,
  title = "DEUX LANGUES, UNE GUERRE",
  subtitle = "Mots sur-représentés (z-score) selon le bord politique",
  source = "Source : Analyse textuelle des interventions AN + Twitter. 10 774 textes, 459 députés.",
}: ButterflyChartProps) {
  const [hoveredWord, setHoveredWord] = useState<string | null>(null);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT}px)`);
    const handler = () => setIsMobile(mq.matches);
    handler();
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);

  const gaucheData = isMobile ? data.gauche.slice(0, MOBILE_WORDS_LIMIT) : data.gauche;
  const droiteData = isMobile ? data.droite.slice(0, MOBILE_WORDS_LIMIT) : data.droite;

  const maxZ = Math.max(
    ...data.gauche.map((d) => d.z),
    ...data.droite.map((d) => Math.abs(d.z))
  );

  return (
    <div
      className="w-full max-w-[720px] mx-auto rounded-lg overflow-hidden"
      style={{
        backgroundColor: 'var(--butterfly-bg-card)',
        border: '1px solid var(--butterfly-border)',
      }}
      aria-label="Graphique en barres divergentes : mots sur-représentés à gauche et à droite"
    >
      <div className="p-6">
        {/* Header */}
        <h2
          className="font-sans font-semibold text-[18px] tracking-tight mb-1"
          style={{ color: 'var(--butterfly-text-primary)' }}
        >
          {title}
        </h2>
        <p
          className="font-sans text-[13px] mb-6"
          style={{ color: 'var(--butterfly-text-secondary)' }}
        >
          {subtitle}
        </p>

        {/* Legend pills */}
        <div className="flex justify-between items-center mb-6">
          <span
            className="inline-flex items-center px-2.5 py-1 rounded text-[11px] font-medium"
            style={{
              backgroundColor: `${COLOR_GAUCHE}20`,
              color: COLOR_GAUCHE,
            }}
          >
            Gauche
          </span>
          <span
            className="inline-flex items-center px-2.5 py-1 rounded text-[11px] font-medium"
            style={{
              backgroundColor: `${COLOR_DROITE}20`,
              color: COLOR_DROITE,
            }}
          >
            Droite
          </span>
        </div>

        {/* Chart */}
        <div
          className={`relative flex w-full ${isMobile ? 'flex-col gap-8' : ''}`}
        >
          {/* Center axis (hidden on mobile when stacked) */}
          {!isMobile && (
            <div
              className="absolute left-1/2 top-0 bottom-0 w-px -translate-x-1/2 z-0"
              style={{ backgroundColor: 'var(--butterfly-border)' }}
            />
          )}

          {/* Left column (Gauche) */}
          <div
            className={`flex-1 flex flex-col gap-1 z-10 ${isMobile ? 'pr-0' : 'pr-4'}`}
          >
            {gaucheData.map((item) => {
              const widthPct = (item.z / maxZ) * 100;
              const isHovered = hoveredWord === `gauche-${item.word}`;
              const isDimmed = hoveredWord !== null && !isHovered;
              return (
                <div
                  key={`gauche-${item.word}`}
                  className="flex items-center justify-end h-7 group cursor-default rounded focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-1 focus-visible:ring-[var(--bloc-gauche)]"
                  tabIndex={0}
                  onMouseEnter={() => setHoveredWord(`gauche-${item.word}`)}
                  onMouseLeave={() => setHoveredWord(null)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setHoveredWord((prev) =>
                        prev === `gauche-${item.word}` ? null : `gauche-${item.word}`
                      );
                    }
                  }}
                  role="img"
                  aria-label={`${item.word}: z-score ${item.z.toFixed(1)}`}
                >
                  <span
                    className="mr-3 font-sans text-[13px] tabular-nums transition-opacity duration-200"
                    style={{
                      color: isDimmed
                        ? 'var(--butterfly-text-muted)'
                        : 'var(--butterfly-text-secondary)',
                      opacity: isDimmed ? 0.5 : 1,
                    }}
                  >
                    {item.word}
                  </span>
                  <div
                    className="relative h-full flex items-center justify-start overflow-visible transition-all duration-200 ease-in-out"
                    style={{
                      width: `${widthPct}%`,
                      minWidth: '24px',
                      backgroundColor: COLOR_GAUCHE,
                      borderTopLeftRadius: '4px',
                      borderBottomLeftRadius: '4px',
                      opacity: isDimmed ? 0.4 : 1,
                      boxShadow: isHovered
                        ? `0 0 0 2px ${COLOR_GAUCHE}40`
                        : 'none',
                    }}
                  >
                    <span
                      className="absolute right-2 font-mono text-[11px] font-medium tabular-nums"
                      style={{
                        color: 'var(--butterfly-bg-card)',
                        opacity: 0.95,
                      }}
                    >
                      {item.z.toFixed(1)}
                    </span>
                    {isHovered && (
                      <div
                        className="absolute right-full mr-2 top-1/2 -translate-y-1/2 rounded px-2 py-1.5 shadow-lg z-50 whitespace-nowrap pointer-events-none"
                        style={{
                          backgroundColor: 'var(--butterfly-text-primary)',
                          color: 'var(--butterfly-bg-card)',
                          fontSize: '11px',
                        }}
                      >
                        z = {item.z.toFixed(2)}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right column (Droite) */}
          <div
            className={`flex-1 flex flex-col gap-1 z-10 ${isMobile ? 'pl-0' : 'pl-4'}`}
          >
            {droiteData.map((item) => {
              const absZ = Math.abs(item.z);
              const widthPct = (absZ / maxZ) * 100;
              const isHovered = hoveredWord === `droite-${item.word}`;
              const isDimmed = hoveredWord !== null && !isHovered;
              return (
                <div
                  key={`droite-${item.word}`}
                  className="flex items-center justify-start h-7 group cursor-default rounded focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-1 focus-visible:ring-[var(--bloc-droite)]"
                  tabIndex={0}
                  onMouseEnter={() => setHoveredWord(`droite-${item.word}`)}
                  onMouseLeave={() => setHoveredWord(null)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setHoveredWord((prev) =>
                        prev === `droite-${item.word}` ? null : `droite-${item.word}`
                      );
                    }
                  }}
                  role="img"
                  aria-label={`${item.word}: z-score ${absZ.toFixed(1)}`}
                >
                  <div
                    className="relative h-full flex items-center justify-end overflow-visible transition-all duration-200 ease-in-out"
                    style={{
                      width: `${widthPct}%`,
                      minWidth: '24px',
                      backgroundColor: COLOR_DROITE,
                      borderTopRightRadius: '4px',
                      borderBottomRightRadius: '4px',
                      opacity: isDimmed ? 0.4 : 1,
                      boxShadow: isHovered
                        ? `0 0 0 2px ${COLOR_DROITE}40`
                        : 'none',
                    }}
                  >
                    <span
                      className="absolute left-2 font-mono text-[11px] font-medium tabular-nums"
                      style={{
                        color: 'var(--butterfly-bg-card)',
                        opacity: 0.95,
                      }}
                    >
                      {absZ.toFixed(1)}
                    </span>
                    {isHovered && (
                      <div
                        className="absolute left-full ml-2 top-1/2 -translate-y-1/2 rounded px-2 py-1.5 shadow-lg z-50 whitespace-nowrap pointer-events-none"
                        style={{
                          backgroundColor: 'var(--butterfly-text-primary)',
                          color: 'var(--butterfly-bg-card)',
                          fontSize: '11px',
                        }}
                      >
                        z = {absZ.toFixed(2)}
                      </div>
                    )}
                  </div>
                  <span
                    className="ml-3 font-sans text-[13px] tabular-nums transition-opacity duration-200"
                    style={{
                      color: isDimmed
                        ? 'var(--butterfly-text-muted)'
                        : 'var(--butterfly-text-secondary)',
                      opacity: isDimmed ? 0.5 : 1,
                    }}
                  >
                    {item.word}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Source */}
        <p
          className="font-sans text-[11px] italic mt-6"
          style={{ color: 'var(--butterfly-text-muted)' }}
        >
          {source}
        </p>
      </div>
    </div>
  );
}
