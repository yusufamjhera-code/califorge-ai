import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { Button } from '../ui/Button';

interface FeedbackModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (difficulty: 'easy' | 'just_right' | 'hard') => void;
}

const options = [
  { value: 'easy' as const, emoji: '😊', label: 'Easy', description: "Could've done more", color: '#00E676' },
  { value: 'just_right' as const, emoji: '💪', label: 'Just Right', description: 'Perfect challenge', color: '#6C5CE7' },
  { value: 'hard' as const, emoji: '🥵', label: 'Hard', description: 'Really struggled', color: '#FF5252' },
];

export const FeedbackModal: React.FC<FeedbackModalProps> = ({ isOpen, onClose, onSubmit }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', damping: 25 }}
            className="fixed inset-x-4 top-1/2 -translate-y-1/2 md:inset-x-auto md:left-1/2 md:-translate-x-1/2 md:w-full md:max-w-md z-50 bg-surface border border-border rounded-3xl p-8"
          >
            <button
              onClick={onClose}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/5 flex items-center justify-center hover:bg-white/10 transition-colors"
            >
              <X className="w-4 h-4 text-text-muted" />
            </button>

            <div className="text-center mb-8">
              <h3 className="text-2xl font-heading font-bold text-text-primary mb-2">
                Great Workout! 🎉
              </h3>
              <p className="text-text-secondary">
                How difficult was today's session?
              </p>
            </div>

            <div className="grid grid-cols-3 gap-3 mb-6">
              {options.map((option) => (
                <motion.button
                  key={option.value}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => onSubmit(option.value)}
                  className="flex flex-col items-center gap-2 p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.08] hover:border-white/[0.15] transition-all"
                >
                  <span className="text-4xl">{option.emoji}</span>
                  <span className="font-medium text-sm text-text-primary">{option.label}</span>
                  <span className="text-xs text-text-muted">{option.description}</span>
                </motion.button>
              ))}
            </div>

            <Button variant="ghost" className="w-full" onClick={onClose}>
              Skip for now
            </Button>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
