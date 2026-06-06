import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label: string;
  error?: string;
  hint?: string;
  icon?: React.ReactNode;
  inputSize?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'px-3 py-2 text-sm',
  md: 'px-4 py-3 text-sm',
  lg: 'px-5 py-4 text-base',
};

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    { label, error, hint, icon, inputSize = 'md', className = '', id, ...props },
    ref
  ) => {
    const [focused, setFocused] = useState(false);
    const inputId = id ?? label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`relative ${className}`}>
      <div className="relative">
        {icon && (
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted">
            {icon}
          </span>
        )}
        <input
          id={inputId}
          ref={ref}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          className={`
            w-full bg-white/5 border rounded-xl text-text-primary placeholder-transparent
            transition-all duration-200 outline-none peer
            ${icon ? 'pl-12' : ''}
            ${sizeClasses[inputSize]}
            ${error
              ? 'border-error/50 focus:border-error focus:ring-1 focus:ring-error/30'
              : 'border-white/10 focus:border-primary focus:ring-1 focus:ring-primary/30'
            }
          `}
          placeholder={label}
          {...props}
        />
        <label
          htmlFor={inputId}
          className={`
            absolute left-4 transition-all duration-200 pointer-events-none
            ${icon ? 'left-12' : 'left-4'}
            ${focused || props.value
              ? '-top-2.5 text-xs px-1 bg-bg'
              : 'top-1/2 -translate-y-1/2 text-sm'
            }
            ${error ? 'text-error' : focused ? 'text-primary' : 'text-text-muted'}
          `}
        >
          {label}
        </label>
      </div>

      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            className="mt-1.5 text-xs text-error"
          >
            {error}
          </motion.p>
        )}
        {hint && !error && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-1.5 text-xs text-text-muted"
          >
            {hint}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
});
