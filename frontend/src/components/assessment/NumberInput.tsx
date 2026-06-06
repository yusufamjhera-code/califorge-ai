import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface NumberInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  unit?: string;
  placeholder?: string;
}

export const NumberInput: React.FC<NumberInputProps> = ({
  label,
  value,
  onChange,
  min,
  max,
  unit,
  placeholder = '0',
}) => {
  const [localStr, setLocalStr] = useState(value ? String(value) : '');

  useEffect(() => {
    if (value !== Number(localStr)) {
      setLocalStr(value ? String(value) : '');
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setLocalStr(val);
    const num = Number(val);
    if (!isNaN(num)) {
      onChange(num);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-sm mx-auto glass p-8 rounded-3xl"
    >
      <label className="text-base text-text-secondary mb-6 block text-center font-medium">{label}</label>
      <div className="flex items-center justify-center">
        <div className="relative">
          <input
            type="number"
            value={localStr}
            onChange={handleChange}
            placeholder={placeholder}
            min={min}
            max={max}
            className="w-32 h-20 text-center text-4xl font-heading font-bold bg-white/[0.03] border border-white/[0.1] rounded-2xl text-primary-light focus:outline-none focus:border-primary/50 focus:shadow-[0_0_20px_rgba(108,92,231,0.2)] transition-all [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          />
          {unit && (
            <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-sm text-text-muted font-medium">
              {unit}
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
};
