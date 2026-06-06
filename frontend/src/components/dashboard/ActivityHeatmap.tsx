import React from 'react';
import { motion } from 'framer-motion';

interface ActivityHeatmapProps {
  /** 7×4 (or variable) grid of activity values 0–3, most recent first */
  data: number[];
  weeks?: number;
}

const intensityColors = [
  'bg-white/[0.03]',   // 0 - no activity
  'bg-primary/20',     // 1 - light
  'bg-primary/50',     // 2 - medium
  'bg-primary',        // 3 - high
];

const dayLabels = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

export const ActivityHeatmap: React.FC<ActivityHeatmapProps> = ({ data, weeks = 4 }) => {
  // Fill to complete grid
  const totalCells = weeks * 7;
  const cells = [...Array(totalCells - data.length).fill(0), ...data];

  // Group into weeks (columns)
  const weekColumns: number[][] = [];
  for (let w = 0; w < weeks; w++) {
    weekColumns.push(cells.slice(w * 7, w * 7 + 7));
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-2"
    >
      <div className="flex gap-1">
        {/* Day labels */}
        <div className="flex flex-col gap-1 mr-1">
          {dayLabels.map((d, i) => (
            <div key={i} className="w-4 h-4 flex items-center justify-center text-[9px] text-text-muted">
              {i % 2 === 0 ? d : ''}
            </div>
          ))}
        </div>

        {/* Week columns */}
        {weekColumns.map((week, wi) => (
          <div key={wi} className="flex flex-col gap-1">
            {week.map((v, di) => (
              <motion.div
                key={`${wi}-${di}`}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: (wi * 7 + di) * 0.01 }}
                className={`w-4 h-4 rounded-sm ${intensityColors[Math.min(v, 3)]}`}
                title={`Week ${wi + 1}, ${dayLabels[di]}: ${v > 0 ? 'Trained' : 'Rest'}`}
              />
            ))}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex items-center gap-3 text-xs text-text-muted">
        <span>Less</span>
        {intensityColors.map((c, i) => (
          <div key={i} className={`w-3 h-3 rounded-sm ${c}`} />
        ))}
        <span>More</span>
      </div>
    </motion.div>
  );
};
