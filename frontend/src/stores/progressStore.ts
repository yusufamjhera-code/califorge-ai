import { create } from 'zustand';
import type { ProgressEntry, Streak, Achievement } from '../types';

interface ProgressState {
  entries: ProgressEntry[];
  streak: Streak;
  achievements: Achievement[];
  loading: boolean;
  error: string | null;

  loadProgress: () => Promise<void>;
  addEntry: (entry: Omit<ProgressEntry, 'id'>) => void;
  loadAchievements: () => Promise<void>;
}

const mockEntries: ProgressEntry[] = Array.from({ length: 30 }, (_, i) => {
  const date = new Date();
  date.setDate(date.getDate() - (29 - i));
  return {
    id: `entry-${i}`,
    userId: 'mock-user',
    date: date.toISOString(),
    weight: 78 - i * 0.15 + Math.random() * 0.5,
    workoutCompleted: Math.random() > 0.3,
    scores: i % 7 === 0 ? { overall: 55 + i, upperBody: 50 + i, core: 45 + i } : undefined,
  };
});

const mockStreak: Streak = {
  current: 7,
  longest: 14,
  lastWorkoutDate: new Date().toISOString(),
};

const mockAchievements: Achievement[] = [
  { id: 'first-workout', title: 'First Rep', description: 'Complete your first workout', icon: '🎯', category: 'workout', requirement: 1, progress: 1, status: 'unlocked', unlockedAt: new Date().toISOString() },
  { id: 'week-streak', title: 'Week Warrior', description: 'Maintain a 7-day streak', icon: '🔥', category: 'streak', requirement: 7, progress: 7, status: 'unlocked', unlockedAt: new Date().toISOString() },
  { id: 'ten-workouts', title: 'Getting Serious', description: 'Complete 10 workouts', icon: '💪', category: 'workout', requirement: 10, progress: 8, status: 'locked' },
  { id: 'two-week-streak', title: 'Unstoppable', description: 'Maintain a 14-day streak', icon: '⚡', category: 'streak', requirement: 14, progress: 7, status: 'locked' },
  { id: 'first-pushup-milestone', title: 'Push-up Pro', description: 'Do 100 total push-ups', icon: '🏆', category: 'milestone', requirement: 100, progress: 45, status: 'locked' },
  { id: 'flexibility-master', title: 'Bendy', description: 'Complete 20 mobility sessions', icon: '🧘', category: 'milestone', requirement: 20, progress: 5, status: 'locked' },
  { id: 'month-streak', title: 'Iron Will', description: '30-day workout streak', icon: '👑', category: 'streak', requirement: 30, progress: 7, status: 'locked' },
  { id: 'fifty-workouts', title: 'Half Century', description: 'Complete 50 workouts', icon: '🌟', category: 'workout', requirement: 50, progress: 8, status: 'locked' },
];

export const useProgressStore = create<ProgressState>((set) => ({
  entries: [],
  streak: { current: 0, longest: 0 },
  achievements: [],
  loading: false,
  error: null,

  loadProgress: async () => {
    set({ loading: true });
    await new Promise((r) => setTimeout(r, 600));
    set({ entries: mockEntries, streak: mockStreak, loading: false });
  },

  addEntry: (entry) => {
    set((state) => ({
      entries: [...state.entries, { ...entry, id: `entry-${Date.now()}` }],
    }));
  },

  loadAchievements: async () => {
    set({ loading: true });
    await new Promise((r) => setTimeout(r, 500));
    set({ achievements: mockAchievements, loading: false });
  },
}));
