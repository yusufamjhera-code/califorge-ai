import React from 'react';
import { motion } from 'framer-motion';
import { ProgressRing } from '../ui/ProgressRing';

interface ScoreCardProps {
  title: string;
  score: number;
  description: string;
  color?: string;
  delay?: number;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  description,
  color = 'url(#ringGradient)',
  delay = 0,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
      className="flex flex-col items-center p-6 bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl"
    >
      <ProgressRing
        value={score}
        size={100}
        strokeWidth={6}
        color={color}
        label={`${score}`}
        sublabel={title}
      />
      <p className="text-xs text-text-muted mt-3 text-center max-w-[140px]">{description}</p>
    </motion.div>
  );
};
