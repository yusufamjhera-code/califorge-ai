import React from 'react';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  current: number;
  total: number;
  category?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ current, total, category }) => {
  const percentage = Math.round((current / total) * 100);

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-text-muted">
          {category && <span className="text-primary-light font-medium">{category} · </span>}
          Step {current} of {total}
        </span>
        <span className="text-sm font-medium text-text-secondary">{percentage}%</span>
      </div>
      <div className="w-full h-2 bg-surface rounded-full overflow-hidden">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-primary to-primary-light"
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
};
