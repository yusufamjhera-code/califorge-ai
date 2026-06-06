import React from 'react';
import { motion } from 'framer-motion';
import { ProgressRing } from '../ui/ProgressRing';

interface ScoreRingProps {
  title: string;
  score: number;
  color?: string;
  delay?: number;
}

export const ScoreRing: React.FC<ScoreRingProps> = ({ title, score, color, delay = 0 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay }}
      className="flex flex-col items-center gap-2"
    >
      <ProgressRing value={score} size={90} strokeWidth={5} color={color} label={`${score}`} />
      <span className="text-xs font-medium text-text-muted">{title}</span>
    </motion.div>
  );
};
