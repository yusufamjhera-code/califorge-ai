import React from 'react';
import { motion } from 'framer-motion';
import { Lock, Trophy } from 'lucide-react';

interface AchievementBadgeProps {
  title: string;
  description: string;
  icon?: string;
  unlocked: boolean;
  progress?: number;
  total?: number;
}

export const AchievementBadge: React.FC<AchievementBadgeProps> = ({
  title,
  description,
  icon = '🏆',
  unlocked,
  progress = 0,
  total = 1,
}) => {
  return (
    <motion.div
      whileHover={{ scale: 1.03 }}
      className={`relative p-4 rounded-2xl border transition-all ${
        unlocked
          ? 'bg-primary/5 border-primary/20'
          : 'bg-white/[0.02] border-white/[0.04] opacity-60'
      }`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${
            unlocked ? 'bg-primary/10' : 'bg-white/[0.03]'
          }`}
        >
          {unlocked ? icon : <Lock className="w-5 h-5 text-text-muted" />}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-semibold text-text-primary truncate">{title}</h4>
          <p className="text-xs text-text-muted truncate">{description}</p>
          {!unlocked && total > 1 && (
            <div className="mt-2 w-full h-1.5 bg-white/[0.04] rounded-full overflow-hidden">
              <div
                className="h-full bg-primary/40 rounded-full"
                style={{ width: `${(progress / total) * 100}%` }}
              />
            </div>
          )}
        </div>
        {unlocked && <Trophy className="w-4 h-4 text-warning flex-shrink-0" />}
      </div>
    </motion.div>
  );
};
