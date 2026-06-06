import React from 'react';
import { motion } from 'framer-motion';

interface SliderInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
  unit?: string;
  showValue?: boolean;
}

export const SliderInput: React.FC<SliderInputProps> = ({
  label,
  value,
  onChange,
  min,
  max,
  step = 1,
  unit = '',
  showValue = true,
}) => {
  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-md mx-auto glass p-8 rounded-3xl"
    >
      <div className="flex items-center justify-between mb-8">
        <label className="text-base text-text-secondary font-medium">{label}</label>
        {showValue && (
          <span className="text-3xl font-heading font-bold text-primary-light glow-primary inline-block">
            {value}{unit}
          </span>
        )}
      </div>
      <div className="relative mb-6">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-3 appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, #6C5CE7 0%, #A29BFE ${percentage}%, rgba(255,255,255,0.05) ${percentage}%, rgba(255,255,255,0.05) 100%)`,
            borderRadius: '6px',
            boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.3)'
          }}
        />
      </div>
      <div className="flex justify-between text-sm text-text-muted font-medium">
        <span>{min}{unit}</span>
        <span>{max}{unit}</span>
      </div>
    </motion.div>
  );
};
