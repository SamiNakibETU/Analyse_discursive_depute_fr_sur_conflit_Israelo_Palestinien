import React, { useState } from 'react';
import { Card } from './Card';
import { Pill } from './Pill';
const dataGauche = [
{
  word: 'gaza',
  z: 25.5
},
{
  word: 'génocide',
  z: 21.0
},
{
  word: 'palestine',
  z: 15.3
},
{
  word: 'gouvernement',
  z: 15.2
},
{
  word: 'massacres',
  z: 14.5
},
{
  word: 'cessez',
  z: 14.2
},
{
  word: 'feu',
  z: 13.9
},
{
  word: 'palestiniens',
  z: 12.9
},
{
  word: 'netanyahou',
  z: 12.8
},
{
  word: 'armée',
  z: 12.7
}];

const dataDroite = [
{
  word: 'hamas',
  z: 34.9
},
{
  word: 'terroristes',
  z: 18.7
},
{
  word: 'otages',
  z: 18.4
},
{
  word: 'antisémitisme',
  z: 18.4
},
{
  word: 'octobre',
  z: 18.3
},
{
  word: 'haine',
  z: 17.2
},
{
  word: 'juifs',
  z: 16.7
},
{
  word: 'nos',
  z: 16.7
},
{
  word: 'lfi',
  z: 15.7
},
{
  word: 'terroriste',
  z: 15.6
}];

const MAX_Z = 34.9;
const COLOR_GAUCHE = '#F87171';
const COLOR_DROITE = '#A78BFA';
export function Figure1Butterfly() {
  const [hoveredWord, setHoveredWord] = useState<string | null>(null);
  return (
    <Card>
      <div className="flex justify-between items-center mb-8 px-4">
        <Pill label="← Vocabulaire gauche" color={COLOR_GAUCHE} />
        <Pill label="Vocabulaire droite →" color={COLOR_DROITE} />
      </div>

      <div className="relative flex w-full max-w-4xl mx-auto">
        {/* Center Axis */}
        <div className="absolute left-1/2 top-0 bottom-0 w-[1px] bg-border -translate-x-1/2 z-0" />

        {/* Left Column (Gauche) */}
        <div className="flex-1 flex flex-col gap-1 pr-4 z-10">
          {dataGauche.map((item) => {
            const widthPct = item.z / MAX_Z * 100;
            const isHovered = hoveredWord === item.word;
            const isDimmed = hoveredWord !== null && !isHovered;
            return (
              <div
                key={item.word}
                className="flex items-center justify-end h-8 group cursor-default"
                onMouseEnter={() => setHoveredWord(item.word)}
                onMouseLeave={() => setHoveredWord(null)}>

                <span
                  className={`mr-3 font-sans text-[13px] transition-opacity duration-200 ${isDimmed ? 'opacity-30' : 'opacity-100 text-text-secondary group-hover:text-text-primary'}`}>

                  {item.word}
                </span>
                <div
                  className="relative h-full flex items-center justify-start overflow-visible transition-all duration-200 ease-in-out"
                  style={{
                    width: `${widthPct}%`,
                    backgroundColor: COLOR_GAUCHE,
                    borderTopLeftRadius: '6px',
                    borderBottomLeftRadius: '6px',
                    opacity: isDimmed ? 0.3 : 1,
                    boxShadow: isHovered ?
                    `0 0 12px 2px ${COLOR_GAUCHE}40` :
                    'none'
                  }}>

                  <span className="absolute right-2 font-mono text-[11px] text-deep font-medium opacity-80">
                    {item.z.toFixed(1)}
                  </span>

                  {/* Tooltip */}
                  {isHovered &&
                  <div className="absolute right-full mr-2 top-1/2 -translate-y-1/2 bg-subtle border border-border rounded-lg p-2 shadow-lg z-50 whitespace-nowrap pointer-events-none">
                      <div className="font-sans text-[11px] text-text-muted mb-1">
                        z-score
                      </div>
                      <div
                      className="font-mono text-[13px] text-text-primary"
                      style={{
                        color: COLOR_GAUCHE
                      }}>

                        {item.z.toFixed(2)}
                      </div>
                    </div>
                  }
                </div>
              </div>);

          })}
        </div>

        {/* Right Column (Droite) */}
        <div className="flex-1 flex flex-col gap-1 pl-4 z-10">
          {dataDroite.map((item) => {
            const widthPct = item.z / MAX_Z * 100;
            const isHovered = hoveredWord === item.word;
            const isDimmed = hoveredWord !== null && !isHovered;
            return (
              <div
                key={item.word}
                className="flex items-center justify-start h-8 group cursor-default"
                onMouseEnter={() => setHoveredWord(item.word)}
                onMouseLeave={() => setHoveredWord(null)}>

                <div
                  className="relative h-full flex items-center justify-end overflow-visible transition-all duration-200 ease-in-out"
                  style={{
                    width: `${widthPct}%`,
                    backgroundColor: COLOR_DROITE,
                    borderTopRightRadius: '6px',
                    borderBottomRightRadius: '6px',
                    opacity: isDimmed ? 0.3 : 1,
                    boxShadow: isHovered ?
                    `0 0 12px 2px ${COLOR_DROITE}40` :
                    'none'
                  }}>

                  <span className="absolute left-2 font-mono text-[11px] text-deep font-medium opacity-80">
                    {item.z.toFixed(1)}
                  </span>

                  {/* Tooltip */}
                  {isHovered &&
                  <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 bg-subtle border border-border rounded-lg p-2 shadow-lg z-50 whitespace-nowrap pointer-events-none">
                      <div className="font-sans text-[11px] text-text-muted mb-1">
                        z-score
                      </div>
                      <div
                      className="font-mono text-[13px] text-text-primary"
                      style={{
                        color: COLOR_DROITE
                      }}>

                        {item.z.toFixed(2)}
                      </div>
                    </div>
                  }
                </div>
                <span
                  className={`ml-3 font-sans text-[13px] transition-opacity duration-200 ${isDimmed ? 'opacity-30' : 'opacity-100 text-text-secondary group-hover:text-text-primary'}`}>

                  {item.word}
                </span>
              </div>);

          })}
        </div>
      </div>
    </Card>);

}