import React from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Card } from './Card';
import { affectiveGap, blocColors, blocLabels, eventImpact } from '../data/article1';

const impactRows = eventImpact.map((row) => ({
  ...row,
  key: `${row.event}-${row.bloc}`,
  label: `${row.event} / ${blocLabels[row.bloc]}`,
}));

const shockTicks = ['2023-10', '2024-01', '2024-05', '2025-01', '2026-01'];

export function SubstackFigure3Chocs() {
  return (
    <Card className="space-y-8">
      <div>
        <h3 className="font-sans font-semibold text-[18px] text-text-primary mb-2">
          Reactions par choc, pas tendance seculaire
        </h3>
        <p className="font-sans text-[13px] text-text-secondary mb-5">
          Effets diff-in-diff (delta de stance) par bloc et evenement. Les barres hachurees
          indiquent des effets non significatifs.
        </p>
        <div className="h-[430px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={impactRows} margin={{ top: 8, right: 12, left: 0, bottom: 80 }}>
              <CartesianGrid stroke="#E5E7EB" vertical={false} />
              <XAxis
                dataKey="label"
                angle={-35}
                textAnchor="end"
                interval={0}
                height={90}
                tick={{ fill: '#475467', fontSize: 11 }}
              />
              <YAxis tick={{ fill: '#475467', fontSize: 11 }} />
              <ReferenceLine y={0} stroke="#98A2B3" />
              <Tooltip
                formatter={(value: number, _name, props: any) => [
                  `${value >= 0 ? '+' : ''}${value.toFixed(2)} (p=${props.payload.p.toFixed(3)})`,
                  'Delta',
                ]}
              />
              <Bar dataKey="delta">
                {impactRows.map((row) => (
                  <Cell
                    key={row.key}
                    fill={blocColors[row.bloc]}
                    fillOpacity={row.p < 0.05 ? 0.95 : 0.45}
                    stroke={row.p < 0.05 ? 'none' : '#667085'}
                    strokeDasharray={row.p < 0.05 ? undefined : '3 2'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div>
        <h4 className="font-sans font-medium text-[14px] text-text-primary mb-2">
          Polarisation affective (gap VAD)
        </h4>
        <p className="font-sans text-[12px] text-text-secondary mb-4">
          Le gap passe de 0.012 (oct. 2023) a 0.067 (janv. 2026).
        </p>
        <div className="h-[210px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={affectiveGap} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="#E5E7EB" vertical={false} />
              <XAxis
                dataKey="month"
                ticks={shockTicks}
                tick={{ fill: '#667085', fontSize: 11 }}
              />
              <YAxis tick={{ fill: '#667085', fontSize: 11 }} width={36} />
              <Tooltip formatter={(value: number) => value.toFixed(3)} />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#0F766E"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <p className="font-sans text-[11px] text-text-muted mt-3">
          Mann-Kendall: aucune tendance monotone significative par bloc (p&gt;0.15). Lecture:
          regime de chocs, pas convergence lineaire.
        </p>
      </div>
    </Card>
  );
}
