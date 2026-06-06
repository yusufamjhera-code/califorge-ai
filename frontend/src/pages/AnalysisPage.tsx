import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight,  } from 'lucide-react';
import { ScoreCard } from '../components/analysis/ScoreCard';
import { FitnessRadarChart } from '../components/analysis/FitnessRadarChart';
import { Button } from '../components/ui/Button';
import api from '../services/api';

const levelFromScore = (score: number) => {
  if (score <= 25) return { level: 'Beginner', color: '#00D2FF' };
  if (score <= 50) return { level: 'Novice', color: '#6C5CE7' };
  if (score <= 75) return { level: 'Intermediate', color: '#00E676' };
  return { level: 'Advanced', color: '#FFD600' };
};

const AnalysisPage: React.FC = () => {
  const navigate = useNavigate();
  const [phase, setPhase] = useState<'loading' | 'reveal' | 'complete'>('loading');
  const [loadingText, setLoadingText] = useState('Analyzing your profile...');
  
  const [scores, setScores] = useState({
    fitness: 0,
    strength: 0,
    recovery: 0,
    consistency: 0,
    mobility: 0,
  });
  const [insights, setInsights] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    const fetchOverview = async () => {
      try {
        const response = await api.get('/fitness/overview');
        if (mounted) {
          const data = response.data;
          setScores({
            fitness: data.overall_fitness,
            strength: data.strength,
            recovery: data.recovery,
            consistency: data.consistency,
            mobility: data.mobility,
          });
          setInsights(data.insights || []);
          
          // Switch to reveal phase after data is loaded and a minimum delay for UX
          setTimeout(() => setPhase('reveal'), 1500);
          setTimeout(() => setPhase('complete'), 3000);
        }
      } catch (err) {
        console.error('Failed to fetch fitness overview:', err);
        if (mounted) setError('Failed to load analysis. Please try again.');
      }
    };

    fetchOverview();

    const texts = [
      'Analyzing your profile...',
      'Calculating fitness scores...',
      'Evaluating recovery capacity...',
      'Building your personalized plan...',
    ];
    let i = 0;
    const textInterval = setInterval(() => {
      i = (i + 1) % texts.length;
      setLoadingText(texts[i]);
    }, 1500);

    return () => {
      mounted = false;
      clearInterval(textInterval);
    };
  }, []);

  const { level, color } = levelFromScore(scores.fitness);

  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-bg flex flex-col items-center justify-center px-6">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-16 h-16 rounded-2xl gradient-accent flex items-center justify-center mb-8"
        >
          <Sparkles className="w-8 h-8 text-white" />
        </motion.div>

        <motion.h2
          key={loadingText}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="text-2xl font-heading font-bold text-text-primary text-center mb-4"
        >
          {loadingText}
        </motion.h2>

        <div className="w-64 h-1.5 bg-surface rounded-full overflow-hidden">
          <motion.div
            className="h-full gradient-accent rounded-full"
            initial={{ width: '0%' }}
            animate={{ width: '100%' }}
            transition={{ duration: 4, ease: 'easeInOut' }}
          />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-bg flex flex-col items-center justify-center px-6 text-center">
        <p className="text-red-400 mb-6">{error}</p>
        <Button onClick={() => navigate('/assessment')}>Back to Assessment</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg px-6 py-12">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-heading font-bold mb-4">
            Your <span className="gradient-text">Fitness Analysis</span>
          </h1>
          <div className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full border" style={{ backgroundColor: `${color}10`, borderColor: `${color}30` }}>
            <span className="text-sm font-medium" style={{ color }}>Level: {level}</span>
          </div>
        </motion.div>

        {/* Score Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4 mb-12">
          <ScoreCard title="Fitness" score={scores.fitness} description="Overall fitness level" delay={0} />
          <ScoreCard title="Strength" score={scores.strength} description="Upper & lower body" delay={0.1} color="url(#ringGradientAccent)" />
          <ScoreCard title="Recovery" score={scores.recovery} description="Rest & nutrition" delay={0.2} />
          <ScoreCard title="Consistency" score={scores.consistency} description="Training habits" delay={0.3} color="url(#ringGradientAccent)" />
          <ScoreCard title="Mobility" score={scores.mobility} description="Flexibility & range" delay={0.4} />
        </div>

        {/* Radar Chart */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl p-6 mb-12"
        >
          <h3 className="text-lg font-heading font-semibold text-text-primary mb-4 text-center">Fitness Profile</h3>
          <FitnessRadarChart scores={scores} />
        </motion.div>

        {/* Insights */}
        {phase === 'complete' && insights.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-4 mb-12"
          >
            <h3 className="text-xl font-heading font-semibold text-text-primary">Key Insights</h3>
            <div className="grid gap-4">
               <div className="bg-white/[0.03] border border-white/[0.06] rounded-xl p-5">
                 <ul className="space-y-3">
                   {insights.map((item, idx) => (
                     <li key={idx} className="flex items-start gap-3 text-sm text-text-secondary">
                       <div className="w-1.5 h-1.5 rounded-full bg-primary mt-1.5 shrink-0" />
                       <span className="leading-relaxed">{item}</span>
                     </li>
                   ))}
                 </ul>
               </div>
            </div>
          </motion.div>
        )}

        {/* CTA */}
        {phase === 'complete' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="text-center"
          >
            <Button
              size="lg"
              glow
              onClick={() => navigate('/dashboard')}
              icon={<ArrowRight className="w-5 h-5" />}
              className="text-base px-10"
            >
              Generate My Plan
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default AnalysisPage;
