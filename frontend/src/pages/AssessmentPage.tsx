import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { ProgressBar } from '../components/assessment/ProgressBar';
import { QuestionCard } from '../components/assessment/QuestionCard';
import { SingleSelect } from '../components/assessment/SingleSelect';
import { MultiSelect } from '../components/assessment/MultiSelect';
import { SliderInput } from '../components/assessment/SliderInput';
import { AssessmentTextInput } from '../components/assessment/TextInput';
import { NumberInput } from '../components/assessment/NumberInput';
import { HeightInput } from '../components/assessment/HeightInput';
import { assessmentQuestions } from '../data/assessmentQuestions';
import { useAssessmentStore } from '../stores/assessmentStore';

const AssessmentPage: React.FC = () => {
  const navigate = useNavigate();
  const { answers, setAnswer } = useAssessmentStore();
  const [currentStep, setCurrentStep] = useState(0);
  const [direction, setDirection] = useState<'forward' | 'back'>('forward');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const question = assessmentQuestions[currentStep];
  const totalSteps = assessmentQuestions.length;

  const goNext = useCallback(async () => {
    if (currentStep < totalSteps - 1) {
      setDirection('forward');
      setCurrentStep((prev) => prev + 1);
    } else {
      // Submit assessment
      setIsSubmitting(true);
      try {
        const { default: api } = await import('../services/api');
        
        // 1. Submit answers
        const assessmentData = {
          ...answers,
          // Extract specific metrics the backend needs natively
          height_cm: Number(answers['height']) || 170,
          current_weight_kg: Number(answers['currentWeight']) || 70,
          goal_weight_kg: Number(answers['goalWeight']) || 70,
          actual_age: Number(answers['actualAge']) || 25,
          gender: answers['gender'] || 'prefer_not_to_say',
        };

        await api.post('/assessments/', { data: assessmentData });
        
        // 2. Trigger fitness score calculation
        await api.post('/fitness/calculate');

        // 3. Generate initial workout plan (4 weeks)
        await api.post('/workouts/generate?duration_weeks=4');

        // 4. Log initial weight
        await api.post('/progress/weight', {
          weight_kg: assessmentData.current_weight_kg,
          notes: 'Initial weight from assessment'
        });
        
        // 5. Navigate
        navigate('/analysis');
      } catch (error) {
        console.error('Failed to submit assessment:', error);
        // Fallback navigation even if it fails for now, or we could show an error toast
        navigate('/analysis');
      } finally {
        setIsSubmitting(false);
      }
    }
  }, [currentStep, totalSteps, navigate, answers]);

  const goBack = useCallback(() => {
    if (currentStep > 0) {
      setDirection('back');
      setCurrentStep((prev) => prev - 1);
    }
  }, [currentStep]);

  const currentAnswer = answers[question.id];
  const hasAnswer = currentAnswer !== undefined && currentAnswer !== '' &&
    !(Array.isArray(currentAnswer) && currentAnswer.length === 0);

  const renderInput = () => {
    switch (question.type) {
      case 'single_select':
        return (
          <SingleSelect
            options={(question.options || []).map(o => ({
              value: o.value,
              label: o.label,
              description: o.description,
            }))}
            value={currentAnswer as string}
            onChange={(v) => setAnswer(question.id, v)}
          />
        );
      case 'multi_select':
        return (
          <MultiSelect
            options={(question.options || []).map(o => ({
              value: o.value,
              label: o.label,
            }))}
            value={(currentAnswer as string[]) || []}
            onChange={(v) => setAnswer(question.id, v)}
          />
        );
      case 'slider':
        return (
          <SliderInput
            label={question.title}
            value={(currentAnswer as number) ?? question.min ?? 0}
            onChange={(v) => setAnswer(question.id, v)}
            min={question.min ?? 0}
            max={question.max ?? 100}
            step={question.step ?? 1}
            unit={question.unit ?? ''}
          />
        );
      case 'number':
        if (question.id === 'height') {
          return (
            <HeightInput
              label={question.title}
              value={(currentAnswer as number) || 0}
              onChange={(v) => setAnswer(question.id, v)}
            />
          );
        }
        return (
          <NumberInput
            label={question.title}
            value={(currentAnswer as number) || 0}
            onChange={(v) => setAnswer(question.id, v)}
            min={question.min ?? 0}
            max={question.max ?? 999}
            unit={question.unit}
          />
        );
      case 'text':
        return (
          <AssessmentTextInput
            label={question.title}
            value={(currentAnswer as string) || ''}
            onChange={(v) => setAnswer(question.id, v)}
            placeholder={question.placeholder}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-bg flex flex-col">
      {/* Header */}
      <div className="px-6 pt-6 pb-4">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary-light" />
              <span className="font-heading font-bold text-lg">CaliForge <span className="text-primary-light">AI</span></span>
            </div>
            <button
              onClick={() => navigate('/')}
              className="text-sm text-text-muted hover:text-text-primary transition-colors"
            >
              Exit
            </button>
          </div>
          <ProgressBar
            current={currentStep + 1}
            total={totalSteps}
            category={question.category}
          />
        </div>
      </div>

      {/* Question area */}
      <div className="flex-1 flex items-center justify-center px-6 py-16">
        <QuestionCard
          title={question.title}
          subtitle={question.subtitle}
          direction={direction}
        >
          {renderInput()}
        </QuestionCard>
      </div>

      {/* Navigation */}
      <div className="px-6 pb-8">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={goBack}
            disabled={currentStep === 0}
            icon={<ArrowLeft className="w-4 h-4" />}
          >
            Back
          </Button>

          <motion.div className="flex items-center gap-1">
            {assessmentQuestions.slice(
              Math.max(0, currentStep - 2),
              Math.min(totalSteps, currentStep + 3)
            ).map((_, i) => {
              const idx = Math.max(0, currentStep - 2) + i;
              return (
                <div
                  key={idx}
                  className={`w-1.5 h-1.5 rounded-full transition-all ${
                    idx === currentStep ? 'w-4 bg-primary' : idx < currentStep ? 'bg-primary/40' : 'bg-border'
                  }`}
                />
              );
            })}
          </motion.div>

          <Button
            onClick={goNext}
            disabled={(!hasAnswer && question.type !== 'text') || isSubmitting}
            loading={isSubmitting}
            icon={currentStep === totalSteps - 1 ? <Sparkles className="w-4 h-4" /> : <ArrowRight className="w-4 h-4" />}
          >
            {currentStep === totalSteps - 1 ? 'Analyze' : 'Next'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AssessmentPage;
