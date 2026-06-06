import React from 'react';
import { motion } from 'framer-motion';
import { Play, Clock, Dumbbell } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';

interface TodayWorkoutCardProps {
  title: string;
  exerciseCount: number;
  estimatedDuration: number;
  completed?: boolean;
}

export const TodayWorkoutCard: React.FC<TodayWorkoutCardProps> = ({
  title,
  exerciseCount,
  estimatedDuration,
  completed = false,
}) => {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`relative overflow-hidden p-6 rounded-2xl border ${
        completed
          ? 'bg-success/5 border-success/20'
          : 'bg-gradient-to-br from-primary/10 to-accent-purple/5 border-primary/20'
      }`}
    >
      {/* Background accent */}
      {!completed && (
        <div className="absolute -right-8 -bottom-8 w-32 h-32 rounded-full bg-primary/10 blur-2xl" />
      )}

      <div className="relative">
        <div className="flex items-center gap-2 mb-1">
          <Dumbbell className="w-4 h-4 text-primary-light" />
          <span className="text-xs font-medium text-primary-light uppercase tracking-wider">
            {completed ? '✓ Completed' : "Today's Workout"}
          </span>
        </div>

        <h3 className="text-xl font-heading font-bold text-text-primary mb-3">{title}</h3>

        <div className="flex items-center gap-4 mb-5 text-sm text-text-muted">
          <span className="flex items-center gap-1.5">
            <Dumbbell className="w-3.5 h-3.5" />
            {exerciseCount} exercises
          </span>
          <span className="flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5" />
            {estimatedDuration} min
          </span>
        </div>

        {!completed && (
          <Button
            size="md"
            onClick={() => navigate('/workout')}
            icon={<Play className="w-4 h-4" />}
          >
            Start Workout
          </Button>
        )}
      </div>
    </motion.div>
  );
};
