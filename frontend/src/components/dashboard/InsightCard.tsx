import React from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, TrendingUp, AlertCircle, PartyPopper } from 'lucide-react';

interface InsightCardProps {
  type: 'tip' | 'motivation' | 'warning' | 'celebration';
  title: string;
  message: string;
}

const config = {
  tip: { icon: Lightbulb, color: 'text-accent', bg: 'bg-accent/5', border: 'border-accent/15' },
  motivation: { icon: TrendingUp, color: 'text-success', bg: 'bg-success/5', border: 'border-success/15' },
  warning: { icon: AlertCircle, color: 'text-warning', bg: 'bg-warning/5', border: 'border-warning/15' },
  celebration: { icon: PartyPopper, color: 'text-primary-light', bg: 'bg-primary/5', border: 'border-primary/15' },
};

export const InsightCard: React.FC<InsightCardProps> = ({ type, title, message }) => {
  const { icon: Icon, color, bg, border } = config[type];

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      whileHover={{ x: 4 }}
      className={`flex gap-4 p-4 rounded-xl ${bg} border ${border} transition-all`}
    >
      <div className="flex-shrink-0 mt-0.5">
        <Icon className={`w-5 h-5 ${color}`} />
      </div>
      <div>
        <h4 className="text-sm font-semibold text-text-primary mb-1">{title}</h4>
        <p className="text-sm text-text-secondary">{message}</p>
      </div>
    </motion.div>
  );
};
