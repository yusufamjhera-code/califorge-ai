import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Dumbbell, Clock, Loader2, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const WeeklyPlanPage: React.FC = () => {
  const navigate = useNavigate();
  const [plan, setPlan] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPlan = async () => {
      try {
        const response = await api.get('/workouts/active');
        setPlan(response.data);
      } catch (err) {
        console.error('Failed to fetch active plan', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPlan();
  }, []);

  const today = new Date().getDay();
  const dayIndex = today === 0 ? 6 : today - 1; // Convert to Mon=0

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 animate-spin text-primary" />
      </div>
    );
  }

  if (!plan) {
    return (
      <div className="flex flex-col items-center justify-center py-32">
        <p className="text-text-muted mb-4">No active workout plan found.</p>
        <button onClick={() => navigate('/dashboard')} className="text-primary hover:underline">
          Go back to dashboard
        </button>
      </div>
    );
  }

  const currentWeek = plan.current_week || 1;
  // Get the schedule for the current week, fallback to first week
  const weekSchedule = plan.weekly_schedules?.[currentWeek - 1] || plan.weekly_schedules?.[0] || { days: [] };
  const days = weekSchedule.days || [];

  return (
    <div className="w-full">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-text-muted hover:text-text-primary mb-4 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span className="text-sm">Back to Dashboard</span>
        </button>
        <h1 className="text-3xl font-heading font-bold text-text-primary mb-2">Weekly Plan</h1>
        <p className="text-text-muted mb-8">Week {currentWeek} of {plan.duration_weeks}</p>
      </motion.div>

      <div className="space-y-3">
        {days.map((day: any, index: number) => {
          const isActive = day.type === 'workout';
          const isToday = index === dayIndex;
          
          return (
            <motion.div
              key={day.day}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.06 }}
              className={`p-5 rounded-2xl border transition-all ${
                isToday
                  ? 'bg-primary/5 border-primary/25 ring-1 ring-primary/15'
                  : isActive
                    ? 'bg-white/[0.03] border-white/[0.06] hover:bg-white/[0.05]'
                    : 'bg-white/[0.01] border-white/[0.03] opacity-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-12 text-center ${isToday ? 'text-primary-light' : 'text-text-muted'}`}>
                    <div className="text-xs uppercase tracking-wider">{day.day.slice(0, 3)}</div>
                  </div>
                  <div>
                    <h3 className={`font-semibold ${isActive ? 'text-text-primary' : 'text-text-muted'}`}>
                      {day.title || 'Rest Day'}
                    </h3>
                    {isActive && (
                      <div className="flex items-center gap-3 mt-1 text-xs text-text-muted">
                        <span className="flex items-center gap-1"><Dumbbell className="w-3 h-3" />{day.exercises?.length || 0} exercises</span>
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{day.estimated_duration || 0} min</span>
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {isActive && day.focus && (
                    <div className="hidden sm:flex gap-1.5">
                      {(Array.isArray(day.focus) ? day.focus : [day.focus]).map((f: string) => (
                        <span key={f} className="px-2 py-1 rounded-md text-xs bg-primary/10 text-primary-light border border-primary/20">
                          {f}
                        </span>
                      ))}
                    </div>
                  )}
                  {isToday && isActive && (
                    <button 
                      onClick={() => navigate('/workout')}
                      className="ml-2 w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white shadow-lg hover:scale-105 transition-transform"
                    >
                      <Play className="w-4 h-4 ml-1" />
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default WeeklyPlanPage;
