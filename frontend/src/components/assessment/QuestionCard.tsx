import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface QuestionCardProps {
  title: string;
  subtitle?: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  direction?: 'forward' | 'back';
}

const variants = {
  enter: (direction: 'forward' | 'back') => ({
    x: direction === 'forward' ? 80 : -80,
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: 'forward' | 'back') => ({
    x: direction === 'forward' ? -80 : 80,
    opacity: 0,
  }),
};

export const QuestionCard: React.FC<QuestionCardProps> = ({
  title,
  subtitle,
  icon,
  children,
  direction = 'forward',
}) => {
  return (
    <AnimatePresence mode="wait" custom={direction}>
      <motion.div
        key={title}
        custom={direction}
        variants={variants}
        initial="enter"
        animate="center"
        exit="exit"
        transition={{ duration: 0.35, ease: 'easeInOut' }}
        className="w-full max-w-2xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-12">
          {icon && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', delay: 0.1 }}
              className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/10 border border-primary/20 mb-6"
            >
              {icon}
            </motion.div>
          )}
          <h2 className="text-3xl md:text-4xl font-heading font-bold text-text-primary mb-4">
            {title}
          </h2>
          {subtitle && (
            <p className="text-lg text-text-secondary max-w-lg mx-auto">{subtitle}</p>
          )}
        </div>

        {/* Content */}
        <div className="space-y-6">{children}</div>
      </motion.div>
    </AnimatePresence>
  );
};
