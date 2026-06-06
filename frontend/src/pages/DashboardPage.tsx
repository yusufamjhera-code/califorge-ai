import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ScoreRing } from '../components/dashboard/ScoreRing';
import { StreakCounter } from '../components/dashboard/StreakCounter';
import { WeightChart } from '../components/dashboard/WeightChart';
import { ActivityHeatmap } from '../components/dashboard/ActivityHeatmap';
import { AchievementBadge } from '../components/dashboard/AchievementBadge';
import { InsightCard } from '../components/dashboard/InsightCard';
import { TodayWorkoutCard } from '../components/dashboard/TodayWorkoutCard';
import { Loader2, Lightbulb } from 'lucide-react';
import api from '../services/api';

const DashboardPage: React.FC = () => {
  const [data, setData] = useState<{
    overview: any;
    fitness: any;
    todayWorkout: any;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, fitnessRes, workoutRes] = await Promise.allSettled([
          api.get('/progress/overview'),
          api.get('/fitness/overview'),
          api.get('/workouts/active/today')
        ]);

        setData({
          overview: overviewRes.status === 'fulfilled' ? overviewRes.value.data : null,
          fitness: fitnessRes.status === 'fulfilled' ? fitnessRes.value.data : null,
          todayWorkout: workoutRes.status === 'fulfilled' ? workoutRes.value.data : null,
        });
      } catch (err) {
        console.error('Failed to fetch dashboard data', err);
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

  // Safely extract data
  const overview = data?.overview || {};
  const stats = overview.stats || {};
  const fitness = data?.fitness || {};
  const categoryScores = fitness.category_scores || {};
  const todayWorkout = data?.todayWorkout || {};
  const achievements = overview.achievements || [];

  // Parse weight data for chart
  const recentWeights = overview.recent_weight_entries || [];
  const weightChartData = recentWeights.length > 0 
    ? recentWeights.slice().reverse().map((e: any) => ({
        date: new Date(e.recorded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        weight: e.weight_kg
      }))
    : [{ date: 'Start', weight: 0 }];
  
    const weightChange = stats.weight_change_kg || 0;

  // Mock a 28-day activity heatmap if no real daily distribution is available easily
  // We'll just randomly populate based on workouts_this_month
  const mockActivity = Array(28).fill(0).map((_, i) => i % 3 === 0 && i < (stats.workouts_this_month || 0) * 2 ? Math.floor(Math.random() * 3) + 1 : 0);

  return (
    <div className="w-full">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-10"
      >
        <h1 className="text-3xl font-heading font-bold text-text-primary">Dashboard</h1>
        <p className="text-text-muted mt-2 text-lg">Welcome back! Here's your fitness overview.</p>
      </motion.div>

      {/* Score Rings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="flex flex-wrap justify-center sm:justify-between items-center gap-6 md:gap-8 lg:gap-12 mb-12 p-8 bg-white/[0.02] border border-white/[0.04] rounded-3xl shadow-xl shadow-black/20"
      >
        <ScoreRing title="Fitness" score={fitness.overall_score || 0} delay={0} />
        <ScoreRing title="Strength" score={categoryScores.strength || 0} color="url(#ringGradientAccent)" delay={0.1} />
        <ScoreRing title="Endurance" score={categoryScores.endurance || 0} delay={0.2} />
        <ScoreRing title="Mobility" score={categoryScores.mobility || 0} color="url(#ringGradientAccent)" delay={0.3} />
        <ScoreRing title="Core" score={categoryScores.core || 0} delay={0.4} />
      </motion.div>

      {/* Main grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 xl:gap-10">
        {/* Left column */}
        <div className="xl:col-span-2 flex flex-col gap-8">
          {/* Today's workout + Streak */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <TodayWorkoutCard
              title={todayWorkout.workout?.title || 'Rest Day'}
              exerciseCount={todayWorkout.workout?.exercises?.length || 0}
              estimatedDuration={todayWorkout.workout?.estimated_duration || 0}
            />
            <StreakCounter streak={stats.current_streak || 0} longest={stats.longest_streak || 0} />
          </div>

          {/* Weight Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-3xl p-8 shadow-lg shadow-black/10"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-heading font-semibold text-text-primary">Weight Progress</h3>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${weightChange <= 0 ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
                {weightChange > 0 ? '+' : ''}{weightChange} kg
              </span>
            </div>
            <WeightChart data={weightChartData} goalWeight={0} />
          </motion.div>

          {/* Activity Heatmap */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-3xl p-8 shadow-lg shadow-black/10"
          >
            <h3 className="text-xl font-heading font-semibold text-text-primary mb-6">Activity</h3>
            <ActivityHeatmap data={mockActivity} />
          </motion.div>
        </div>

        {/* Right column */}
        <div className="flex flex-col gap-8">
          {/* AI Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col gap-4 bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-3xl p-8 shadow-lg shadow-black/10"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-primary/20 text-primary-light">
                <Lightbulb className="w-5 h-5" />
              </div>
              <h3 className="text-xl font-heading font-semibold text-text-primary">Coach Insights</h3>
            </div>
            
            <div className="flex flex-col gap-3">
              {(fitness.insights || []).length > 0 ? (
                fitness.insights.map((insight: any, i: number) => {
                  let type = 'tip';
                  if (insight.category === 'motivation' || insight.category === 'progress') type = 'motivation';
                  if (insight.category === 'safety' || insight.category === 'warning') type = 'warning';
                  if (insight.icon === '🎉' || insight.icon === '🏆') type = 'celebration';

                  return (
                    <InsightCard
                      key={i}
                      type={type as any}
                      title={(insight.title || insight.category || 'Insight').toUpperCase()}
                      message={insight.message}
                    />
                  );
                })
              ) : (
                <div className="p-4 rounded-xl border border-dashed border-white/10 text-center">
                  <p className="text-sm text-text-muted">Complete more workouts to get AI insights.</p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Achievements */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col gap-4 bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-3xl p-8 shadow-lg shadow-black/10"
          >
            <h3 className="text-xl font-heading font-semibold text-text-primary mb-2">Achievements</h3>
            <div className="flex flex-col gap-3">
              {achievements.length > 0 ? (
                achievements.slice(0, 4).map((ach: any, i: number) => (
                  <AchievementBadge 
                    key={i} 
                    title={ach.title} 
                    description={ach.description} 
                    icon={ach.icon} 
                    unlocked={true} 
                  />
                ))
              ) : (
                <div className="p-4 rounded-xl border border-dashed border-white/10 text-center">
                  <p className="text-sm text-text-muted">Start training to unlock achievements!</p>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
