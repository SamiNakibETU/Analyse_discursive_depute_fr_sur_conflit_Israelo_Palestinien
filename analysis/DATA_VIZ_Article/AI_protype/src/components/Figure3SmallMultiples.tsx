import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip } from
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
  1.27, 1.37, 1.49, 1.73, 1.56, 1.49, 1.58, 1.73, 1.46, 1.67, 1.62, 1.54,
  1.61, 1.28, 1.49, 1.56, 1.44, 1.49, 1.6, 1.56, 1.52, 1.54, 1.49, 1.4, 1.45,
  1.42, 1.38, 1.21],

  'Gauche moderee': [
  0.65, 0.65, 0.88, 1.27, 1.18, 1.39, 0.74, 1.22, 0.88, 1.0, 0.44, 1.1, 0.55,
  0.68, 0.39, 0.61, 0.73, 0.79, 1.1, 1.04, 0.89, 0.92, 0.85, 0.71, 0.77, 0.72,
  0.66, -1.0],

  'Centre / Majorite': [
  -0.9, -0.81, -0.2, -0.81, -0.86, -0.79, -0.88, -0.62, -0.71, -0.74, -1.31,
  -1.2, -0.87, -0.82, -0.8, -0.73, -0.82, -0.78, -0.71, -0.68, -0.86, -0.55,
  -0.57, -0.48, -0.51, -0.6, -0.55, -0.5],

  Droite: [
  -1.45, -1.19, -1.13, -1.38, -1.38, -1.62, -1.29, -1.52, -1.56, -1.65, -1.41,
  -1.26, -1.42, -1.6, -1.5, -1.44, -1.5, -1.58, -1.48, -1.36, -1.55, -1.42,
  -1.48, -1.44, -1.47, -1.56, -1.45, -0.38]

};
const BLOCS = [
{
  id: 'Gauche radicale',
  name: 'Gauche radicale',
  color: '#F87171'
},
{
  id: 'Gauche moderee',
  name: 'Gauche modérée',
  color: '#FBBF24'
},
{
  id: 'Centre / Majorite',
  name: 'Centre / Majorité',
  color: '#60A5FA'
},
{
  id: 'Droite',
  name: 'Droite',
  color: '#A78BFA'
}];

const data = rawData.months.map((month, index) => {
  const [year, m] = month.split('-');
  const dateObj = new Date(parseInt(year), parseInt(m) - 1);
  return {
    month,
    displayMonth: dateObj.
    toLocaleDateString('fr-FR', {
      month: 'short',
      year: '2-digit'
    }).
    replace('.', ''),
    'Gauche radicale': rawData['Gauche radicale'][index],
    'Gauche moderee': rawData['Gauche moderee'][index],
    'Centre / Majorite': rawData['Centre / Majorite'][index],
    Droite: rawData['Droite'][index]
  };
});
const MiniTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-subtle border border-border rounded-lg p-2 shadow-lg">
        <p className="font-sans text-[10px] text-text-muted mb-1">
          {payload[0].payload.displayMonth}
        </p>
        <p
          className="font-mono text-[12px] text-text-primary"
          style={{
            color: payload[0].color
          }}>

          {payload[0].value > 0 ? '+' : ''}
          {payload[0].value.toFixed(2)}
        </p>
      </div>);

  }
  return null;
};
export function Figure3SmallMultiples() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {BLOCS.map((bloc) => {
        const avgStance =
        rawData[bloc.id as keyof typeof rawData].reduce(
          (a: any, b: any) => a + b,
          0
        ) / rawData.months.length;
        return (
          <div
            key={bloc.id}
            className="bg-card border border-border rounded-card p-5 flex flex-col h-[280px]">

            <div className="flex justify-between items-start mb-4">
              <h3
                className="font-sans font-semibold text-[14px]"
                style={{
                  color: bloc.color
                }}>

                {bloc.name}
              </h3>
              <span
                className="font-mono text-[24px] leading-none opacity-60"
                style={{
                  color: bloc.color
                }}>

                {avgStance > 0 ? '+' : ''}
                {avgStance.toFixed(2)}
              </span>
            </div>

            <div className="flex-1 w-full relative">
              <span className="absolute top-0 left-0 text-[10px] text-text-muted z-10">
                Pro-pal.
              </span>
              <span className="absolute bottom-0 left-0 text-[10px] text-text-muted z-10">
                Pro-isr.
              </span>

              <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                  data={data}
                  margin={{
                    top: 20,
                    right: 0,
                    left: 0,
                    bottom: 20
                  }}>

                  <defs>
                    <linearGradient
                      id={`fill-${bloc.id}`}
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1">

                      <stop
                        offset="5%"
                        stopColor={bloc.color}
                        stopOpacity={0.2} />

                      <stop
                        offset="95%"
                        stopColor={bloc.color}
                        stopOpacity={0} />

                    </linearGradient>
                    <filter
                      id={`glow-${bloc.id}`}
                      x="-20%"
                      y="-20%"
                      width="140%"
                      height="140%">

                      <feDropShadow
                        dx="0"
                        dy="0"
                        stdDeviation="3"
                        floodColor={bloc.color}
                        floodOpacity="0.4" />

                    </filter>
                  </defs>

                  <YAxis domain={[-2, 2]} hide={true} />
                  <XAxis dataKey="displayMonth" hide={true} />

                  <ReferenceLine y={0} stroke="#3F3F46" strokeDasharray="3 3" />

                  <Tooltip
                    content={<MiniTooltip />}
                    cursor={{
                      stroke: '#3F3F46',
                      strokeWidth: 1
                    }} />


                  <Area
                    type="monotone"
                    dataKey={bloc.id}
                    stroke={bloc.color}
                    strokeWidth={2}
                    fill={`url(#fill-${bloc.id})`}
                    activeDot={{
                      r: 4,
                      fill: bloc.color,
                      stroke: '#18181B',
                      strokeWidth: 2
                    }}
                    style={{
                      filter: `url(#glow-${bloc.id})`
                    }} />

                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>);

      })}
    </div>);

}