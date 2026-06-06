import React from 'react';
import { motion } from 'framer-motion';
import { Flame } from 'lucide-react';

interface StreakCounterProps {
  streak: number;
  longest: number;
}

export const StreakCounter: React.FC<StreakCounterProps> = ({ streak, longest }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center gap-4 p-5 bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl"
    >
      <motion.div
        animate={{ scale: [1, 1.15, 1] }}
        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
        className="w-14 h-14 rounded-2xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center shadow-lg shadow-orange-500/20"
      >
        <Flame className="w-7 h-7 text-white" />
      </motion.div>
      <div>
        <div className="text-3xl font-heading font-bold text-text-primary">
          {streak} <span className="text-lg text-text-muted">days</span>
        </div>
        <div className="text-sm text-text-muted">
          Current Streak · Best: {longest}
        </div>
      </div>
    </motion.div>
  );
};
