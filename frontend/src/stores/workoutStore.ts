import { create } from 'zustand';
import type { Workout, WeeklyPlan, WorkoutExercise } from '../types';
import { exercises } from '../data/exercises';

interface WorkoutState {
  currentWorkout: Workout | null;
  weeklyPlan: WeeklyPlan | null;
  activeExerciseIndex: number;
  activeSetIndex: number;
  isResting: boolean;
  restTimeRemaining: number;
  isWorkoutActive: boolean;
  loading: boolean;
  error: string | null;

  loadTodayWorkout: () => Promise<void>;
  loadWeeklyPlan: () => Promise<void>;
  startWorkout: () => void;
  completeSet: (exerciseIndex: number, setIndex: number, reps?: number) => void;
  nextExercise: () => void;
  startRest: (seconds: number) => void;
  tickRest: () => void;
  skipRest: () => void;
  finishWorkout: (difficulty: number, notes?: string) => Promise<void>;
}

const createMockWorkout = (): Workout => {
  const workoutExercises: WorkoutExercise[] = [
    {
      exerciseId: 'pushup',
      exercise: exercises.find((e) => e.id === 'pushup'),
      sets: [
        { exerciseId: 'pushup', setNumber: 1, targetReps: 10, completed: false },
        { exerciseId: 'pushup', setNumber: 2, targetReps: 10, completed: false },
        { exerciseId: 'pushup', setNumber: 3, targetReps: 8, completed: false },
      ],
      restBetweenSets: 60,
    },
    {
      exerciseId: 'squat',
      exercise: exercises.find((e) => e.id === 'squat'),
      sets: [
        { exerciseId: 'squat', setNumber: 1, targetReps: 15, completed: false },
        { exerciseId: 'squat', setNumber: 2, targetReps: 15, completed: false },
        { exerciseId: 'squat', setNumber: 3, targetReps: 12, completed: false },
      ],
      restBetweenSets: 60,
    },
    {
      exerciseId: 'plank',
      exercise: exercises.find((e) => e.id === 'plank'),
      sets: [
        { exerciseId: 'plank', setNumber: 1, targetDuration: 30, completed: false },
        { exerciseId: 'plank', setNumber: 2, targetDuration: 30, completed: false },
        { exerciseId: 'plank', setNumber: 3, targetDuration: 20, completed: false },
      ],
      restBetweenSets: 45,
    },
    {
      exerciseId: 'reverse-lunge',
      exercise: exercises.find((e) => e.id === 'reverse-lunge'),
      sets: [
        { exerciseId: 'reverse-lunge', setNumber: 1, targetReps: 12, completed: false },
        { exerciseId: 'reverse-lunge', setNumber: 2, targetReps: 12, completed: false },
        { exerciseId: 'reverse-lunge', setNumber: 3, targetReps: 10, completed: false },
      ],
      restBetweenSets: 60,
    },
    {
      exerciseId: 'mountain-climbers',
      exercise: exercises.find((e) => e.id === 'mountain-climbers'),
      sets: [
        { exerciseId: 'mountain-climbers', setNumber: 1, targetDuration: 30, completed: false },
        { exerciseId: 'mountain-climbers', setNumber: 2, targetDuration: 30, completed: false },
      ],
      restBetweenSets: 45,
    },
    {
      exerciseId: 'cat-cow',
      exercise: exercises.find((e) => e.id === 'cat-cow'),
      sets: [
        { exerciseId: 'cat-cow', setNumber: 1, targetReps: 10, completed: false },
      ],
      restBetweenSets: 0,
    },
  ];

  return {
    id: 'workout-day1',
    userId: 'mock-user',
    dayNumber: 1,
    weekNumber: 1,
    title: 'Full Body Foundation',
    description: 'Build your base with this full-body workout focusing on fundamental movement patterns.',
    exercises: workoutExercises,
    estimatedDuration: 30,
    status: 'upcoming',
    scheduledDate: new Date().toISOString(),
  };
};

export const useWorkoutStore = create<WorkoutState>((set, get) => ({
  currentWorkout: null,
  weeklyPlan: null,
  activeExerciseIndex: 0,
  activeSetIndex: 0,
  isResting: false,
  restTimeRemaining: 0,
  isWorkoutActive: false,
  loading: false,
  error: null,

  loadTodayWorkout: async () => {
    set({ loading: true });
    await new Promise((r) => setTimeout(r, 800));
    set({ currentWorkout: createMockWorkout(), loading: false });
  },

  loadWeeklyPlan: async () => {
    set({ loading: true });
    await new Promise((r) => setTimeout(r, 800));
    const today = new Date();
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - today.getDay() + 1);

    const workouts: Workout[] = [
      { ...createMockWorkout(), id: 'w1', dayNumber: 1, title: 'Full Body Foundation', scheduledDate: new Date(startOfWeek).toISOString() },
      { ...createMockWorkout(), id: 'w2', dayNumber: 2, title: 'Rest Day', exercises: [], estimatedDuration: 0, status: 'upcoming', scheduledDate: new Date(startOfWeek.getTime() + 86400000).toISOString() },
      { ...createMockWorkout(), id: 'w3', dayNumber: 3, title: 'Upper Body Push', scheduledDate: new Date(startOfWeek.getTime() + 2 * 86400000).toISOString() },
      { ...createMockWorkout(), id: 'w4', dayNumber: 4, title: 'Rest Day', exercises: [], estimatedDuration: 0, status: 'upcoming', scheduledDate: new Date(startOfWeek.getTime() + 3 * 86400000).toISOString() },
      { ...createMockWorkout(), id: 'w5', dayNumber: 5, title: 'Lower Body & Core', scheduledDate: new Date(startOfWeek.getTime() + 4 * 86400000).toISOString() },
      { ...createMockWorkout(), id: 'w6', dayNumber: 6, title: 'Active Recovery', exercises: [], estimatedDuration: 15, status: 'upcoming', scheduledDate: new Date(startOfWeek.getTime() + 5 * 86400000).toISOString() },
      { ...createMockWorkout(), id: 'w7', dayNumber: 7, title: 'Rest Day', exercises: [], estimatedDuration: 0, status: 'upcoming', scheduledDate: new Date(startOfWeek.getTime() + 6 * 86400000).toISOString() },
    ];

    set({
      weeklyPlan: {
        id: 'week-1',
        userId: 'mock-user',
        weekNumber: 1,
        startDate: startOfWeek.toISOString(),
        endDate: new Date(startOfWeek.getTime() + 6 * 86400000).toISOString(),
        workouts,
        focus: 'Building Foundation',
        progressionNotes: 'Focus on form and consistency. Increase reps before adding difficulty.',
      },
      loading: false,
    });
  },

  startWorkout: () => {
    set({
      isWorkoutActive: true,
      activeExerciseIndex: 0,
      activeSetIndex: 0,
    });
    const workout = get().currentWorkout;
    if (workout) {
      set({ currentWorkout: { ...workout, status: 'in_progress' } });
    }
  },

  completeSet: (exerciseIndex, setIndex, reps) => {
    const workout = get().currentWorkout;
    if (!workout) return;
    const updatedExercises = [...workout.exercises];
    const updatedSets = [...updatedExercises[exerciseIndex].sets];
    updatedSets[setIndex] = {
      ...updatedSets[setIndex],
      completed: true,
      completedReps: reps ?? updatedSets[setIndex].targetReps,
    };
    updatedExercises[exerciseIndex] = {
      ...updatedExercises[exerciseIndex],
      sets: updatedSets,
    };
    set({
      currentWorkout: { ...workout, exercises: updatedExercises },
      activeSetIndex: setIndex + 1,
    });
  },

  nextExercise: () => {
    const { activeExerciseIndex, currentWorkout } = get();
    if (currentWorkout && activeExerciseIndex < currentWorkout.exercises.length - 1) {
      set({ activeExerciseIndex: activeExerciseIndex + 1, activeSetIndex: 0 });
    }
  },

  startRest: (seconds) => {
    set({ isResting: true, restTimeRemaining: seconds });
  },

  tickRest: () => {
    const { restTimeRemaining } = get();
    if (restTimeRemaining <= 1) {
      set({ isResting: false, restTimeRemaining: 0 });
    } else {
      set({ restTimeRemaining: restTimeRemaining - 1 });
    }
  },

  skipRest: () => {
    set({ isResting: false, restTimeRemaining: 0 });
  },

  finishWorkout: async (difficulty, notes) => {
    const workout = get().currentWorkout;
    if (!workout) return;
    set({
      currentWorkout: {
        ...workout,
        status: 'completed',
        completedAt: new Date().toISOString(),
        difficulty,
        notes,
      },
      isWorkoutActive: false,
    });
  },
}));
