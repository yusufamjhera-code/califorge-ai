import React from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

interface SingleSelectProps {
  options: { value: string; label: string; icon?: React.ReactNode; description?: string }[];
  value: string | undefined;
  onChange: (value: string) => void;
}

export const SingleSelect: React.FC<SingleSelectProps> = ({ options, value, onChange }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
      {options.map((option, index) => {
        const isSelected = value === option.value;
        return (
          <motion.button
            key={option.value}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onChange(option.value)}
            className={`relative flex items-center gap-4 p-6 rounded-2xl border text-left transition-all duration-300 ${
              isSelected
                ? 'bg-primary/10 border-primary/40 shadow-[0_0_30px_rgba(108,92,231,0.15)]'
                : 'glass-subtle hover:bg-white/[0.06] hover:border-white/[0.12] hover:shadow-[0_8px_20px_rgba(0,0,0,0.2)]'
            }`}
          >
            {/* Selection indicator */}
            <div
              className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                isSelected ? 'border-primary bg-primary' : 'border-border'
              }`}
            >
              {isSelected && <Check className="w-3.5 h-3.5 text-white" />}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                {option.icon}
                <span className={`font-medium ${isSelected ? 'text-text-primary' : 'text-text-secondary'}`}>
                  {option.label}
                </span>
              </div>
              {option.description && (
                <p className="text-xs text-text-muted mt-1">{option.description}</p>
              )}
            </div>
          </motion.button>
        );
      })}
    </div>
  );
};
