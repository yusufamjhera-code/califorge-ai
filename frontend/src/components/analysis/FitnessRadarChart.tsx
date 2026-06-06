import React from 'react';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts';

interface FitnessRadarChartProps {
  scores: {
    fitness: number;
    strength: number;
    recovery: number;
    consistency: number;
    mobility: number;
  };
}

export const FitnessRadarChart: React.FC<FitnessRadarChartProps> = ({ scores }) => {
  const data = [
    { subject: 'Fitness', value: scores.fitness },
    { subject: 'Strength', value: scores.strength },
    { subject: 'Recovery', value: scores.recovery },
    { subject: 'Consistency', value: scores.consistency },
    { subject: 'Mobility', value: scores.mobility },
  ];

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} cx="50%" cy="50%" outerRadius="75%">
          <PolarGrid
            stroke="rgba(255,255,255,0.06)"
            strokeDasharray="3 3"
          />
          <PolarAngleAxis
            dataKey="subject"
            tick={{ fill: '#A0A0B0', fontSize: 12 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={false}
            axisLine={false}
          />
          <Radar
            name="Scores"
            dataKey="value"
            stroke="#6C5CE7"
            fill="url(#radarGradient)"
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <defs>
            <linearGradient id="radarGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6C5CE7" stopOpacity={0.6} />
              <stop offset="100%" stopColor="#A29BFE" stopOpacity={0.1} />
            </linearGradient>
          </defs>
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
