import { z } from 'zod';

/* ─── Question Type Enum ─── */
export const QuestionTypeSchema = z.enum([
  'single_select',
  'multi_select',
  'slider',
  'number',
  'text',
]);
export type QuestionType = z.infer<typeof QuestionTypeSchema>;

/* ─── Complete Assessment Schema ─── */
export const AssessmentSchema = z.object({
  ageCategory: z.string(),
  experience: z.string(),
  mainGoal: z.string(),
  additionalGoals: z.array(z.string()),
  physicalBuild: z.string(),
  bodyGoal: z.string(),
  bestShape: z.string(),
  weightTrend: z.string(),
  pushupCapacity: z.string(),
  squatCapacity: z.string(),
  plankHold: z.string(),
  flexibility: z.string(),
  workoutFrequency: z.string(),
  targetZone: z.array(z.string()),
  weeklyTraining: z.string(),
  workoutDuration: z.string(),
  physicalLimitations: z.array(z.string()),
  workSchedule: z.string(),
  dailyActivity: z.string(),
  energyLevel: z.string(),
  waterIntake: z.string(),
  sleepDuration: z.string(),
  eatingHabits: z.array(z.string()),
  foodCravings: z.string(),
  smokingStatus: z.string(),
  alcoholFrequency: z.string(),
  dietPreference: z.string(),
  lifeEvents: z.array(z.string()),
  height: z.number().min(0),
  currentWeight: z.number().min(0),
  goalWeight: z.number().min(0),
  actualAge: z.number().min(0),
  fitnessObstacles: z.array(z.string()),
  motivation: z.array(z.string()),
  confidenceLevel: z.string(),
  gender: z.string(),
});

export type AssessmentData = z.infer<typeof AssessmentSchema>;

/* ─── Partial Assessment (for step-by-step) ─── */
export const PartialAssessmentSchema = AssessmentSchema.partial();
export type PartialAssessmentData = z.infer<typeof PartialAssessmentSchema>;

/* ─── Assessment Question Definition ─── */
export interface AssessmentOption {
  value: string;
  label: string;
  description?: string;
  icon?: string;
}

export interface AssessmentQuestion {
  id: keyof AssessmentData;
  number: number;
  title: string;
  subtitle?: string;
  type: QuestionType;
  options?: AssessmentOption[];
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  placeholder?: string;
  category: 'basics' | 'goals' | 'fitness' | 'lifestyle' | 'nutrition' | 'measurements' | 'mindset';
}
