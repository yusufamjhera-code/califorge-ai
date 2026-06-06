import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LoginForm } from '../components/auth/LoginForm';
import { SignupForm } from '../components/auth/SignupForm';
import { Sparkles } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

const AuthPage: React.FC = () => {
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  React.useEffect(() => {
    if (user) {
      const from = (location.state as any)?.from?.pathname;
      const defaultDest = user.assessmentCompleted ? '/dashboard' : '/assessment';
      navigate(from || defaultDest, { replace: true });
    }
  }, [user, navigate, location]);

  return (
    <div className="min-h-screen flex">
      {/* Left side - branding (hidden on mobile) */}
      <div className="hidden lg:flex lg:w-1/2 relative gradient-hero items-center justify-center p-12">
        {/* Floating orbs */}
        <motion.div
          animate={{ y: [-20, 20, -20] }}
          transition={{ duration: 8, repeat: Infinity }}
          className="absolute top-1/4 left-1/4 w-48 h-48 rounded-full bg-primary/15 blur-3xl"
        />
        <motion.div
          animate={{ y: [20, -20, 20] }}
          transition={{ duration: 10, repeat: Infinity }}
          className="absolute bottom-1/3 right-1/4 w-64 h-64 rounded-full bg-accent/10 blur-3xl"
        />

        <div className="relative z-10 max-w-md">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-xl gradient-primary flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-3xl font-heading font-bold">CaliForge <span className="text-primary-light">AI</span></span>
          </div>
          <h1 className="text-4xl font-heading font-bold mb-4 leading-tight">
            Your AI-Powered
            <br />
            <span className="gradient-text">Calisthenics Coach</span>
          </h1>
          <p className="text-text-secondary text-lg">
            Personalized bodyweight workouts. No equipment needed.
            Just your body and a custom transformation plan.
          </p>

          {/* Feature pills */}
          <div className="flex flex-wrap gap-2 mt-8">
            {['No Equipment', 'AI Personalized', 'Adaptive', 'Beginner Friendly'].map((tag) => (
              <span
                key={tag}
                className="px-3 py-1.5 rounded-full text-xs font-medium bg-white/5 border border-white/10 text-text-secondary"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Right side - auth form */}
      <div className="flex-1 flex items-center justify-center p-6 md:p-12 bg-bg">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-3 mb-8 justify-center">
            <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-heading font-bold">CaliForge <span className="text-primary-light">AI</span></span>
          </div>

          {/* Tab toggle */}
          <div className="flex bg-surface rounded-xl p-1 mb-8">
            {(['login', 'signup'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setMode(tab)}
                className={`flex-1 py-3 rounded-lg text-sm font-medium transition-all ${
                  mode === tab
                    ? 'bg-primary text-white shadow-lg shadow-primary/20'
                    : 'text-text-muted hover:text-text-secondary'
                }`}
              >
                {tab === 'login' ? 'Sign In' : 'Create Account'}
              </button>
            ))}
          </div>

          {/* Form */}
          <AnimatePresence mode="wait">
            <motion.div
              key={mode}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {mode === 'login' ? (
                <LoginForm onSwitchToSignup={() => setMode('signup')} />
              ) : (
                <SignupForm onSwitchToLogin={() => setMode('login')} />
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
