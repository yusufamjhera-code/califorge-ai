import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface HeightInputProps {
  label: string;
  value: number; // always in cm from the parent
  onChange: (value: number) => void;
}

export const HeightInput: React.FC<HeightInputProps> = ({
  label,
  value,
  onChange,
}) => {
  const [unit, setUnit] = useState<'cm' | 'ft'>('cm');

  // Local string states to allow typing empty or partial numbers cleanly
  const [cmStr, setCmStr] = useState<string>(value ? String(value) : '');
  const [ftStr, setFtStr] = useState<string>('');
  const [inStr, setInStr] = useState<string>('');

  // Sync initial value if changed from outside (e.g. going back/forward)
  useEffect(() => {
    if (value) {
      if (unit === 'cm') {
        setCmStr(String(Math.round(value)));
      } else {
        // Convert cm to ft/in
        const totalInches = value / 2.54;
        const ft = Math.floor(totalInches / 12);
        const inches = Math.round(totalInches % 12);
        setFtStr(String(ft));
        setInStr(String(inches));
      }
    }
  }, [value, unit]);

  const handleCmChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setCmStr(val);
    const num = Number(val);
    if (!isNaN(num)) {
      onChange(num);
    }
  };

  const handleFtChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setFtStr(val);
    updateFromFtIn(val, inStr);
  };

  const handleInChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setInStr(val);
    updateFromFtIn(ftStr, val);
  };

  const updateFromFtIn = (f: string, i: string) => {
    const ftNum = Number(f) || 0;
    const inNum = Number(i) || 0;
    const cm = Math.round((ftNum * 30.48) + (inNum * 2.54));
    onChange(cm);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-sm mx-auto glass p-8 rounded-3xl"
    >
      <label className="text-base text-text-secondary mb-6 block text-center font-medium">{label}</label>
      
      {/* Unit Toggle */}
      <div className="flex justify-center gap-2 mb-8 bg-white/[0.03] p-1 rounded-xl w-fit mx-auto border border-white/[0.08]">
        <button
          onClick={() => setUnit('cm')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            unit === 'cm'
              ? 'bg-primary text-white shadow-[0_0_15px_rgba(108,92,231,0.4)]'
              : 'text-text-muted hover:text-text-primary'
          }`}
        >
          cm
        </button>
        <button
          onClick={() => setUnit('ft')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            unit === 'ft'
              ? 'bg-primary text-white shadow-[0_0_15px_rgba(108,92,231,0.4)]'
              : 'text-text-muted hover:text-text-primary'
          }`}
        >
          ft / in
        </button>
      </div>

      <div className="flex items-center justify-center">
        {unit === 'cm' ? (
          <div className="relative">
            <input
              type="number"
              value={cmStr}
              onChange={handleCmChange}
              placeholder="0"
              className="w-32 h-20 text-center text-4xl font-heading font-bold bg-white/[0.03] border border-white/[0.1] rounded-2xl text-primary-light focus:outline-none focus:border-primary/50 focus:shadow-[0_0_20px_rgba(108,92,231,0.2)] transition-all [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
            />
            <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-sm text-text-muted font-medium">
              cm
            </span>
          </div>
        ) : (
          <div className="flex gap-4">
            <div className="relative">
              <input
                type="number"
                value={ftStr}
                onChange={handleFtChange}
                placeholder="0"
                className="w-24 h-20 text-center text-4xl font-heading font-bold bg-white/[0.03] border border-white/[0.1] rounded-2xl text-primary-light focus:outline-none focus:border-primary/50 focus:shadow-[0_0_20px_rgba(108,92,231,0.2)] transition-all [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
              <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-sm text-text-muted font-medium">
                ft
              </span>
            </div>
            <div className="relative">
              <input
                type="number"
                value={inStr}
                onChange={handleInChange}
                placeholder="0"
                className="w-24 h-20 text-center text-4xl font-heading font-bold bg-white/[0.03] border border-white/[0.1] rounded-2xl text-primary-light focus:outline-none focus:border-primary/50 focus:shadow-[0_0_20px_rgba(108,92,231,0.2)] transition-all [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
              <span className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-sm text-text-muted font-medium">
                in
              </span>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};
