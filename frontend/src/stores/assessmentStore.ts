import { create } from 'zustand';
import type { PartialAssessmentData } from '../types/assessment';
import type { AnalysisResult } from '../types';

interface AssessmentState {
  currentStep: number;
  totalSteps: number;
  answers: PartialAssessmentData;
  isSubmitting: boolean;
  isComplete: boolean;
  analysisResult: AnalysisResult | null;
  error: string | null;

  setAnswer: (key: string, value: unknown) => void;
  nextStep: () => void;
  prevStep: () => void;
  goToStep: (step: number) => void;
  submitAssessment: () => Promise<void>;
  reset: () => void;
}

const mockAnalysis: AnalysisResult = {
  scores: {
    overall: 62,
    upperBody: 55,
    core: 48,
    lowerBody: 70,
    flexibility: 40,
    endurance: 65,
    balance: 58,
  },
  level: 'beginner',
  summary:
    'You have a solid foundation to build on. Your lower body strength is your biggest asset. Let\'s focus on core stability and flexibility while progressively building upper body pushing strength.',
  strengths: [
    'Good lower body baseline',
    'Decent cardiovascular endurance',
    'Consistent daily activity level',
  ],
  improvements: [
    'Core stability needs development',
    'Upper body pushing strength is below average',
    'Flexibility is limited and may restrict progress',
  ],
  recommendations: [
    'Start with 3-day training program',
    'Include daily mobility work',
    'Focus on progressive overload for push-ups',
    'Add core exercises to every session',
  ],
};

export const useAssessmentStore = create<AssessmentState>((set, get) => ({
  currentStep: 0,
  totalSteps: 36,
  answers: {},
  isSubmitting: false,
  isComplete: false,
  analysisResult: null,
  error: null,

  setAnswer: (key, value) => {
    set((state) => ({
      answers: { ...state.answers, [key]: value },
    }));
  },

  nextStep: () => {
    const { currentStep, totalSteps } = get();
    if (currentStep < totalSteps - 1) {
      set({ currentStep: currentStep + 1 });
    }
  },

  prevStep: () => {
    const { currentStep } = get();
    if (currentStep > 0) {
      set({ currentStep: currentStep - 1 });
    }
  },

  goToStep: (step) => {
    set({ currentStep: step });
  },

  submitAssessment: async () => {
    set({ isSubmitting: true, error: null });
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 3000));
      set({
        isSubmitting: false,
        isComplete: true,
        analysisResult: mockAnalysis,
      });
    } catch (err) {
      set({
        isSubmitting: false,
        error: err instanceof Error ? err.message : 'Submission failed',
      });
    }
  },

  reset: () => {
    set({
      currentStep: 0,
      answers: {},
      isSubmitting: false,
      isComplete: false,
      analysisResult: null,
      error: null,
    });
  },
}));
