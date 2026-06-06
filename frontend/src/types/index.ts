/* ─── User ─── */
export interface User {
  id: string;
  email: string;
  displayName: string;
  photoURL?: string;
  role: 'user' | 'admin';
  createdAt: string;
  assessmentCompleted: boolean;
  currentPlanId?: string;
}

/* ─── Muscle Groups ─── */
export type MuscleGroup =
  | 'chest'
  | 'shoulders'
  | 'triceps'
  | 'biceps'
  | 'back'
  | 'core'
  | 'quads'
  | 'hamstrings'
  | 'glutes'
  | 'calves'
  | 'hip_flexors'
  | 'full_body';

/* ─── Exercise ─── */
export type ExerciseCategory = 'push' | 'pull' | 'legs' | 'core' | 'conditioning' | 'mobility';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export interface Exercise {
  id: string;
  name: string;
  category: ExerciseCategory;
  difficulty: DifficultyLevel;
  muscleGroups: MuscleGroup[];
  description: string;
  instructions: string[];
  tips: string[];
  videoUrl?: string;
  imageUrl?: string;
  caloriesPerMinute: number;
  isTimeBased: boolean;
  defaultDuration?: number; // seconds
  defaultReps?: number;
  defaultSets: number;
}

/* ─── Workout Set ─── */
export interface WorkoutSet {
  exerciseId: string;
  setNumber: number;
  targetReps?: number;
  targetDuration?: number;
  completedReps?: number;
  completedDuration?: number;
  completed: boolean;
}

/* ─── Workout Exercise ─── */
export interface WorkoutExercise {
  exerciseId: string;
  exercise?: Exercise;
  sets: WorkoutSet[];
  restBetweenSets: number; // seconds
  notes?: string;
}

/* ─── Workout ─── */
export type WorkoutStatus = 'upcoming' | 'in_progress' | 'completed' | 'skipped';

export interface Workout {
  id: string;
  userId: string;
  dayNumber: number;
  weekNumber: number;
  title: string;
  description: string;
  exercises: WorkoutExercise[];
  estimatedDuration: number; // minutes
  status: WorkoutStatus;
  scheduledDate: string;
  completedAt?: string;
  difficulty?: number; // 1-5 user feedback
  notes?: string;
  caloriesBurned?: number;
}

/* ─── Weekly Plan ─── */
export interface WeeklyPlan {
  id: string;
  userId: string;
  weekNumber: number;
  startDate: string;
  endDate: string;
  workouts: Workout[];
  focus: string;
  progressionNotes: string;
}

/* ─── Fitness Scores ─── */
export interface FitnessScores {
  overall: number;
  upperBody: number;
  core: number;
  lowerBody: number;
  flexibility: number;
  endurance: number;
  balance: number;
}

/* ─── Analysis Result ─── */
export interface AnalysisResult {
  scores: FitnessScores;
  level: DifficultyLevel;
  summary: string;
  strengths: string[];
  improvements: string[];
  recommendations: string[];
}

/* ─── Progress Entry ─── */
export interface ProgressEntry {
  id: string;
  userId: string;
  date: string;
  weight?: number;
  workoutCompleted: boolean;
  workoutId?: string;
  scores?: Partial<FitnessScores>;
  notes?: string;
}

/* ─── Achievement ─── */
export type AchievementStatus = 'locked' | 'unlocked' | 'claimed';

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'streak' | 'workout' | 'milestone' | 'special';
  requirement: number;
  progress: number;
  status: AchievementStatus;
  unlockedAt?: string;
}

/* ─── Streak ─── */
export interface Streak {
  current: number;
  longest: number;
  lastWorkoutDate?: string;
}

/* ─── AI Insight ─── */
export interface AIInsight {
  id: string;
  type: 'tip' | 'motivation' | 'warning' | 'celebration';
  title: string;
  message: string;
  createdAt: string;
  read: boolean;
}

/* ─── Notification ─── */
export type ToastVariant = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: string;
  variant: ToastVariant;
  title: string;
  message?: string;
  duration?: number;
}

/* ─── API Response ─── */
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

/* ─── Pagination ─── */
export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
