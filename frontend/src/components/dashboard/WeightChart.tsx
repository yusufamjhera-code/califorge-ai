import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';

interface WeightChartProps {
  data: { date: string; weight: number }[];
  goalWeight?: number;
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.[0]) return null;
  return (
    <div className="bg-surface border border-border rounded-xl px-4 py-3 shadow-xl">
      <p className="text-xs text-text-muted mb-1">{label}</p>
      <p className="text-lg font-heading font-bold text-text-primary">
        {payload[0].value} <span className="text-sm text-text-muted">kg</span>
      </p>
    </div>
  );
};

export const WeightChart: React.FC<WeightChartProps> = ({ data, goalWeight }) => {
  return (
    <div className="w-full h-[250px]">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="weightGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6C5CE7" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6C5CE7" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="date"
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6B6B7B', fontSize: 11 }}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6B6B7B', fontSize: 11 }}
            domain={['dataMin - 2', 'dataMax + 2']}
          />
          <Tooltip content={<CustomTooltip />} />
          {goalWeight && (
            <ReferenceLine
              y={goalWeight}
              stroke="#00E676"
              strokeDasharray="6 4"
              strokeWidth={1.5}
              label={{
                value: 'Goal',
                fill: '#00E676',
                fontSize: 11,
                position: 'right',
              }}
            />
          )}
          <Area
            type="monotone"
            dataKey="weight"
            stroke="#6C5CE7"
            strokeWidth={2.5}
            fill="url(#weightGradient)"
            dot={false}
            activeDot={{
              r: 5,
              fill: '#6C5CE7',
              stroke: '#A29BFE',
              strokeWidth: 2,
            }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
