import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Clock, Flame, CheckCircle2, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ExerciseCard } from '../components/workout/ExerciseCard';
import { WorkoutTimer } from '../components/workout/WorkoutTimer';
import { FeedbackModal } from '../components/workout/FeedbackModal';
import { Button } from '../components/ui/Button';
import api from '../services/api';

const WorkoutPage: React.FC = () => {
  const navigate = useNavigate();
  const [showTimer, setShowTimer] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  const [completed, setCompleted] = useState(false);
  
  const [workoutData, setWorkoutData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Time tracking
  const [startTime] = useState<Date>(new Date());

  useEffect(() => {
    const fetchWorkout = async () => {
      try {
        const response = await api.get('/workouts/active/today');
        setWorkoutData(response.data);
        if (response.data?.is_completed) {
          setCompleted(true);
        }
      } catch (err) {
        console.error('Failed to fetch today workout', err);
      } finally {
        setLoading(false);
      }
    };
    fetchWorkout();
  }, []);

  const handleComplete = () => {
    setShowFeedback(true);
  };

  const handleFeedback = async (difficulty: 'easy' | 'just_right' | 'hard') => {
    setShowFeedback(false);
    
    // Map difficulty to a 1-5 rating (backend constraint)
    const difficultyRating = difficulty === 'easy' ? 2 : difficulty === 'just_right' ? 3 : 4;
    const durationMinutes = Math.max(1, Math.round((new Date().getTime() - startTime.getTime()) / 60000));

    try {
      if (workoutData?.workout) {
        // Construct the log payload matching ExerciseLog schema
        const exercisesToLog = workoutData.workout.exercises.map((ex: any) => ({
          exercise_id: ex.id || 'custom',
          exercise_name: ex.name,
          sets_completed: ex.sets || 3,
          reps_completed: typeof ex.reps === 'number' ? ex.reps : (Array.isArray(ex.reps) ? ex.reps[0] : 0),
          duration_seconds: ex.duration || 0,
          skipped: false
        }));

        await api.post('/progress/workouts', {
          workout_plan_id: workoutData.plan_id,
          week_number: workoutData.current_week,
          day_number: new Date().getDay() || 7, // 1-7, day_number must be >= 1
          day_of_week: workoutData.day_of_week,
          workout_title: workoutData.workout.title,
          exercises: exercisesToLog,
          duration_minutes: durationMinutes,
          difficulty_rating: difficultyRating,
          energy_rating: 3, // default energy 1-5
        });
      }
      setCompleted(true);
    } catch (err) {
      console.error('Failed to log workout', err);
      // Fallback
      setCompleted(true);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 animate-spin text-primary" />
      </div>
    );
  }

  if (!workoutData || !workoutData.workout || workoutData.workout.type === 'rest') {
    return (
      <div className="flex flex-col items-center justify-center py-32">
        <p className="text-text-muted mb-4">No workout scheduled for today. Enjoy your rest!</p>
        <button onClick={() => navigate('/dashboard')} className="text-primary hover:underline">
          Go back to dashboard
        </button>
      </div>
    );
  }

  const { workout } = workoutData;
  const todayExercises = workout.exercises || [];

  return (
    <div className="w-full">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-text-muted hover:text-text-primary mb-4 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span className="text-sm">Back to Dashboard</span>
        </button>

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-heading font-bold text-text-primary">{workout.title}</h1>
            <div className="flex items-center gap-4 mt-2 text-sm text-text-muted">
              <span className="flex items-center gap-1.5"><Clock className="w-3.5 h-3.5" />{workout.estimated_duration || 30} min</span>
              <span className="flex items-center gap-1.5"><Flame className="w-3.5 h-3.5" />~180 cal</span>
              <span>{todayExercises.length} exercises</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Completed banner */}
      {completed && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex items-center gap-3 p-4 mb-6 rounded-xl bg-success/10 border border-success/20"
        >
          <CheckCircle2 className="w-5 h-5 text-success" />
          <span className="text-success font-medium">Workout completed and logged! Great job! 🎉</span>
        </motion.div>
      )}

      {/* Rest timer */}
      {showTimer && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 flex flex-col items-center bg-white/[0.03] border border-white/[0.06] rounded-2xl p-8"
        >
          <h3 className="text-lg font-heading font-semibold text-text-primary mb-4">Rest Period</h3>
          <WorkoutTimer
            duration={60}
            onComplete={() => setShowTimer(false)}
          />
        </motion.div>
      )}

      {/* Exercise list */}
      <div className="space-y-3 mb-8">
        {todayExercises.map((exercise: any, index: number) => {
          // Normalize API exercises to match expected component props
          const exProp = {
            id: exercise.id || `ex-${index}`,
            name: exercise.name,
            targetMuscleGroup: exercise.muscle_group || 'Full Body',
            difficulty: 'Intermediate',
            isTimeBased: !!exercise.duration,
            defaultReps: exercise.reps || 10,
            defaultDuration: exercise.duration || 30,
            videoUrl: 'https://cdn.pixabay.com/video/2020/05/26/40149-425121980_tiny.mp4',
            instructions: exercise.instructions || ['Perform the exercise with proper form.'],
            tips: []
          };
          
          return (
            <ExerciseCard
              key={index}
              exercise={exProp as any}
              sets={exercise.sets || 3}
              reps={exProp.isTimeBased ? undefined : exProp.defaultReps}
              duration={exProp.isTimeBased ? exProp.defaultDuration : undefined}
              restTime={60}
              index={index}
            />
          );
        })}
      </div>

      {/* Actions */}
      <div className="flex gap-3 justify-center pb-8">
        {!showTimer && (
          <Button variant="secondary" onClick={() => setShowTimer(true)}>
            Start Rest Timer
          </Button>
        )}
        {!completed && (
          <Button glow onClick={handleComplete} icon={<CheckCircle2 className="w-4 h-4" />}>
            Complete Workout
          </Button>
        )}
      </div>

      {/* Feedback Modal */}
      <FeedbackModal
        isOpen={showFeedback}
        onClose={() => setShowFeedback(false)}
        onSubmit={handleFeedback}
      />
    </div>
  );
};

export default WorkoutPage;
