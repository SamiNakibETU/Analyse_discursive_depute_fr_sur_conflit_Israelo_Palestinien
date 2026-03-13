import React from 'react';
import { Card } from './Card';
import { Pill } from './Pill';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  ComposedChart } from
'recharts';
const rawData = {
  months: [
  '2023-10',
  '2023-11',
  '2023-12',
  '2024-01',
  '2024-02',
  '2024-03',
  '2024-04',
  '2024-05',
  '2024-06',
  '2024-07',
  '2024-08',
  '2024-09',
  '2024-10',
  '2024-11',
  '2024-12',
  '2025-01',
  '2025-02',
  '2025-03',
  '2025-04',
  '2025-05',
  '2025-06',
  '2025-07',
  '2025-08',
  '2025-09',
  '2025-10',
  '2025-11',
  '2025-12',
  '2026-01'],

  'Gauche radicale': [
  23, 18, 15, 12, 10, 8, 7, 9, 8, 7, 6, 5, 8, 10, 12, 11, 8, 7, 9, 8, 7, 10,
  9, 8, 7, 9, 8, 6],

  'Gauche moderee': [
  20, 14, 12, 15, 13, 10, 8, 12, 10, 9, 7, 6, 9, 11, 13, 10, 8, 7, 10, 9, 8,
  11, 10, 8, 7, 10, 9, 5],

  'Centre / Majorite': [
  0, 2, 30, 5, 4, 3, 3, 5, 4, 3, 3, 2, 5, 8, 12, 15, 10, 8, 11, 10, 9, 12, 11,
  9, 8, 11, 10, 7],

  Droite: [
  0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 13, 2, 0, 0, 1, 0, 0, 2, 1, 0, 0,
  2, 1, 0]

};
const data = rawData.months.map((month, index) => {
  const [year, m] = month.split('-');
  const dateObj = new Date(parseInt(year), parseInt(m) - 1);
  const formattedMonth = dateObj.
  toLocaleDateString('fr-FR', {
    month: 'short',
    year: '2-digit'
  }).
  replace('.', '');
  return {
    month,
    displayMonth: formattedMonth,
    'Gauche radicale': rawData['Gauche radicale'][index],
    'Gauche moderee': rawData['Gauche moderee'][index],
    'Centre / Majorite': rawData['Centre / Majorite'][index],
    Droite: rawData['Droite'][index]
  };
});
const COLORS = {
  'Gauche radicale': '#F87171',
  'Gauche moderee': '#FBBF24',
  'Centre / Majorite': '#60A5FA',
  Droite: '#A78BFA'
};
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-subtle border border-border rounded-lg p-3 shadow-xl">
        <p className="font-sans text-[12px] text-text-muted mb-2">
          {payload[0].payload.displayMonth}
        </p>
        <div className="flex flex-col gap-1.5">
          {payload.map((entry: any) =>
          <div
            key={entry.name}
            className="flex items-center justify-between gap-4">

              <div className="flex items-center gap-2">
                <div
                className="w-2 h-2 rounded-full"
                style={{
                  backgroundColor: entry.color
                }} />

                <span className="font-sans text-[12px] text-text-secondary">
                  {entry.name}
                </span>
              </div>
              <span className="font-mono text-[13px] text-text-primary font-medium">
                {entry.value}%
              </span>
            </div>
          )}
        </div>
      </div>);

  }
  return null;
};
export function Figure2Timeline() {
  return (
    <Card>
      <div className="flex flex-wrap gap-3 mb-8">
        <Pill label="Gauche radicale" color={COLORS['Gauche radicale']} />
        <Pill label="Gauche modérée" color={COLORS['Gauche moderee']} />
        <Pill label="Centre / Majorité" color={COLORS['Centre / Majorite']} />
        <Pill label="Droite" color={COLORS['Droite']} />
      </div>

      <div className="h-[400px] w-full relative">
        {/* Custom Annotation for 14 months */}
        <div className="absolute top-[15%] left-[10%] right-[45%] flex flex-col items-center z-10 pointer-events-none">
          <span className="text-accent font-sans font-semibold text-[13px] mb-1 bg-card px-2">
            14 mois de retard
          </span>
          <div className="w-full h-[1px] bg-accent relative flex items-center">
            <div className="absolute left-0 w-[1px] h-3 bg-accent" />
            <div className="absolute right-0 w-[1px] h-3 bg-accent" />
            <div className="absolute right-0 w-2 h-2 border-t border-r border-accent transform rotate-45 translate-x-[1px]" />
          </div>
        </div>

        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 0,
              bottom: 0
            }}>

            <defs>
              {Object.entries(COLORS).map(([key, color]) =>
              <linearGradient
                key={`gradient-${key}`}
                id={`fill-${key}`}
                x1="0"
                y1="0"
                x2="0"
                y2="1">

                  <stop offset="5%" stopColor={color} stopOpacity={0.08} />
                  <stop offset="95%" stopColor={color} stopOpacity={0} />
                </linearGradient>
              )}
              {Object.entries(COLORS).map(([key, color]) =>
              <filter
                key={`glow-${key}`}
                id={`glow-${key}`}
                x="-20%"
                y="-20%"
                width="140%"
                height="140%">

                  <feDropShadow
                  dx="0"
                  dy="0"
                  stdDeviation="4"
                  floodColor={color}
                  floodOpacity="0.3" />

                </filter>
              )}
            </defs>

            <CartesianGrid
              stroke="rgba(63,63,70,0.5)"
              vertical={false}
              strokeDasharray="none" />


            <XAxis
              dataKey="displayMonth"
              axisLine={false}
              tickLine={false}
              tick={{
                fill: '#71717A',
                fontSize: 12,
                fontFamily: 'Inter'
              }}
              dy={10}
              interval={2} />


            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{
                fill: '#71717A',
                fontSize: 12,
                fontFamily: 'Inter'
              }}
              dx={-10}
              tickFormatter={(val) => `${val}%`} />


            <Tooltip
              content={<CustomTooltip />}
              cursor={{
                stroke: '#3F3F46',
                strokeWidth: 1,
                strokeDasharray: '4 4'
              }} />


            <ReferenceLine
              y={10}
              stroke="#71717A"
              strokeDasharray="4 4"
              label={{
                position: 'insideTopRight',
                value: 'seuil 10%',
                fill: '#71717A',
                fontSize: 11,
                fontFamily: 'Inter',
                dy: -5
              }} />


            {Object.entries(COLORS).map(([key, color]) =>
            <Area
              key={`area-${key}`}
              type="monotone"
              dataKey={key}
              stroke="none"
              fill={`url(#fill-${key})`}
              activeDot={false} />

            )}

            {Object.entries(COLORS).map(([key, color]) =>
            <Line
              key={`line-${key}`}
              type="monotone"
              dataKey={key}
              stroke={color}
              strokeWidth={2}
              dot={false}
              activeDot={{
                r: 4,
                fill: color,
                stroke: '#18181B',
                strokeWidth: 2
              }}
              style={{
                filter: `url(#glow-${key})`
              }} />

            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </Card>);

}