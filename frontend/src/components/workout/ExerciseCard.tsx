import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Clock, Flame, AlertTriangle, Play } from 'lucide-react';
import type { Exercise } from '../../types';

interface ExerciseCardProps {
  exercise: Exercise;
  sets?: number;
  reps?: number;
  duration?: number;
  restTime?: number;
  index?: number;
}

export const ExerciseCard: React.FC<ExerciseCardProps> = ({
  exercise,
  sets = 3,
  reps,
  duration,
  restTime = 60,
  index = 0,
}) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08 }}
      className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl overflow-hidden hover:border-white/[0.12] transition-colors"
    >
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-4 p-5 text-left"
      >
        {/* Exercise number */}
        <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-sm font-bold text-primary-light">
          {index + 1}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-text-primary truncate">{exercise.name}</h3>
          <div className="flex items-center gap-3 mt-1 text-xs text-text-muted">
            <span>{sets} sets × {reps ? `${reps} reps` : `${duration}s`}</span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {restTime}s rest
            </span>
          </div>
        </div>

        {/* Difficulty dots */}
        <div className="flex gap-1 mr-2">
          {[1, 2, 3].map((d) => (
            <div
              key={d}
              className={`w-2 h-2 rounded-full ${
                d <= (['beginner', 'intermediate', 'advanced'].indexOf(exercise.difficulty) + 1)
                  ? 'bg-primary'
                  : 'bg-border'
              }`}
            />
          ))}
        </div>

        {/* Expand icon */}
        {expanded ? (
          <ChevronUp className="w-5 h-5 text-text-muted" />
        ) : (
          <ChevronDown className="w-5 h-5 text-text-muted" />
        )}
      </button>

      {/* Expanded content */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-5 border-t border-white/[0.06] pt-4 space-y-4">
              {/* Video placeholder */}
              {exercise.videoUrl && (
                <div className="aspect-video bg-surface rounded-xl flex items-center justify-center border border-border">
                  <div className="flex flex-col items-center gap-2 text-text-muted">
                    <Play className="w-10 h-10" />
                    <span className="text-sm">Watch Tutorial</span>
                  </div>
                </div>
              )}

              {/* Description */}
              <p className="text-sm text-text-secondary">{exercise.description}</p>

              {/* Muscle groups */}
              <div>
                <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Muscles Worked</h4>
                <div className="flex flex-wrap gap-2">
                  {exercise.muscleGroups.map((m) => (
                    <span
                      key={m}
                      className="px-3 py-1 rounded-full text-xs bg-primary/10 text-primary-light border border-primary/20"
                    >
                      {m.replace('_', ' ')}
                    </span>
                  ))}
                </div>
              </div>

              {/* Instructions */}
              <div>
                <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Instructions</h4>
                <ol className="space-y-2">
                  {exercise.instructions.map((step, i) => (
                    <li key={i} className="flex gap-3 text-sm text-text-secondary">
                      <span className="flex-shrink-0 w-5 h-5 rounded-full bg-surface border border-border flex items-center justify-center text-xs text-text-muted">
                        {i + 1}
                      </span>
                      {step}
                    </li>
                  ))}
                </ol>
              </div>

              {/* Tips / Common Mistakes */}
              {exercise.tips.length > 0 && (
                <div className="bg-warning/5 border border-warning/20 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertTriangle className="w-4 h-4 text-warning" />
                    <h4 className="text-xs font-semibold text-warning uppercase tracking-wider">Common Mistakes</h4>
                  </div>
                  <ul className="space-y-1">
                    {exercise.tips.map((tip, i) => (
                      <li key={i} className="text-sm text-text-secondary flex items-start gap-2">
                        <span className="text-warning mt-1">•</span>
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Calories */}
              <div className="flex items-center gap-2 text-sm text-text-muted">
                <Flame className="w-4 h-4 text-orange-400" />
                <span>~{exercise.caloriesPerMinute} cal/min</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};
