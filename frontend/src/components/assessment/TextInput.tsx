import React from 'react';
import { motion } from 'framer-motion';

interface AssessmentTextInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  multiline?: boolean;
}

export const AssessmentTextInput: React.FC<AssessmentTextInputProps> = ({
  label,
  value,
  onChange,
  placeholder = 'Type your answer...',
  multiline = false,
}) => {
  const baseClasses =
    'w-full max-w-md mx-auto block bg-white/[0.03] border border-white/[0.08] rounded-xl px-5 py-4 text-text-primary placeholder:text-text-muted focus:outline-none focus:border-primary/40 focus:bg-white/[0.05] transition-all duration-200';

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full flex flex-col items-center"
    >
      <label className="text-sm text-text-secondary mb-3 block">{label}</label>
      {multiline ? (
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          rows={3}
          className={`${baseClasses} resize-none`}
        />
      ) : (
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={baseClasses}
        />
      )}
    </motion.div>
  );
};
