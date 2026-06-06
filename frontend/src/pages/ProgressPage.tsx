import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { WeightChart } from '../components/dashboard/WeightChart';
import { ProgressRing } from '../components/ui/ProgressRing';
import { TrendingUp, TrendingDown, Scale, Calendar, Trophy, Target, Loader2 } from 'lucide-react';
import api from '../services/api';

const ProgressPage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, weightRes, fitnessRes] = await Promise.allSettled([
          api.get('/progress/overview'),
          api.get('/progress/weight?limit=30&days=90'),
          api.get('/fitness/overview')
        ]);

        setData({
          overview: overviewRes.status === 'fulfilled' ? overviewRes.value.data : null,
          weights: weightRes.status === 'fulfilled' ? weightRes.value.data : [],
          fitness: fitnessRes.status === 'fulfilled' ? fitnessRes.value.data : null,
        });
      } catch (err) {
        console.error('Failed to fetch progress data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-32">
        <Loader2 className="w-10 h-10 animate-spin text-primary" />
      </div>
    );
  }

  const overview = data?.overview || {};
  const stats = overview.stats || {};
  const fitness = data?.fitness || {};
  const weights = data?.weights || [];

  const weightData = weights.length > 0 
    ? weights.slice().reverse().map((e: any) => ({
        date: new Date(e.recorded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        weight: e.weight_kg
      }))
    : [{ date: 'Start', weight: 0 }];

  const currentWeightChange = stats.weight_change_kg || 0;
  
  const topStats = [
    { label: 'Workouts Done', value: `${stats.total_workouts || 0}`, icon: Calendar, change: `${stats.workouts_this_month || 0} this month`, up: true },
    { label: 'Weight Change', value: `${currentWeightChange > 0 ? '+' : ''}${currentWeightChange} kg`, icon: Scale, change: 'Lifetime', up: currentWeightChange <= 0 },
    { label: 'Best Streak', value: `${stats.longest_streak || 0} days`, icon: Trophy, change: `Current: ${stats.current_streak || 0}`, up: (stats.current_streak || 0) > 0 },
    { label: 'Plan Progress', value: `${stats.plan_completion_percent || 0}%`, icon: Target, change: 'Active Plan', up: true },
  ];

  const categoryScores = fitness.category_scores || {};
  const fitnessScores = [
    { title: 'Fitness', now: fitness.overall_score || 0 },
    { title: 'Strength', now: categoryScores.strength || 0 },
    { title: 'Endurance', now: categoryScores.endurance || 0 },
    { title: 'Mobility', now: categoryScores.mobility || 0 },
    { title: 'Core', now: categoryScores.core || 0 },
  ];

  return (
    <div className="w-full">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-heading font-bold text-text-primary mb-2">Progress</h1>
        <p className="text-text-muted mb-8">Track your transformation journey</p>
      </motion.div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {topStats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-5"
          >
            <stat.icon className="w-5 h-5 text-primary-light mb-3" />
            <div className="text-2xl font-heading font-bold text-text-primary">{stat.value}</div>
            <div className="text-xs text-text-muted mt-1">{stat.label}</div>
            <div className="flex items-center gap-1 mt-2 text-xs">
              {stat.up ? (
                <TrendingUp className="w-3 h-3 text-success" />
              ) : (
                <TrendingDown className="w-3 h-3 text-error" />
              )}
              <span className={stat.up ? 'text-success' : 'text-error'}>{stat.change}</span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Weight chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-6 mb-8"
      >
        <h3 className="font-heading font-semibold text-text-primary mb-4">Weight History</h3>
        <WeightChart data={weightData} goalWeight={0} />
      </motion.div>

      {/* Fitness scores over time */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-6 mb-8"
      >
        <h3 className="font-heading font-semibold text-text-primary mb-6">Fitness Score Progress</h3>
        <div className="flex flex-wrap justify-center gap-8">
          {fitnessScores.map((s) => (
            <div key={s.title} className="text-center">
              <ProgressRing value={s.now} size={80} strokeWidth={5} label={`${s.now}`} />
              <div className="mt-2 text-xs text-text-muted">{s.title}</div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default ProgressPage;
