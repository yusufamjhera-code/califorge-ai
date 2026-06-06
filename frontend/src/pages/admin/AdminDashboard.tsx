import React from 'react';
import { motion } from 'framer-motion';
import { Users, Dumbbell, Activity, TrendingUp } from 'lucide-react';

const stats = [
  { label: 'Total Users', value: '1,247', change: '+42 this week', icon: Users, color: '#6C5CE7' },
  { label: 'Active Users', value: '892', change: '71.5% active', icon: Activity, color: '#00D2FF' },
  { label: 'Workouts Done', value: '8,340', change: '+380 this week', icon: Dumbbell, color: '#00E676' },
  { label: 'Avg. Completion', value: '87%', change: '+3% vs last week', icon: TrendingUp, color: '#FFD600' },
];

const AdminDashboard: React.FC = () => {
  return (
    <div>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-heading font-bold text-text-primary mb-2">Admin Dashboard</h1>
        <p className="text-text-muted mb-8">Platform overview and analytics</p>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
            className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-6"
          >
            <div className="flex items-center justify-between mb-3">
              <stat.icon className="w-5 h-5" style={{ color: stat.color }} />
              <span className="text-xs text-success">{stat.change}</span>
            </div>
            <div className="text-2xl font-heading font-bold text-text-primary">{stat.value}</div>
            <div className="text-sm text-text-muted mt-1">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-6"
      >
        <h3 className="font-heading font-semibold text-text-primary mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {[
            { user: 'Marcus J.', action: 'completed Upper Body workout', time: '2 min ago' },
            { user: 'Sarah K.', action: 'signed up', time: '15 min ago' },
            { user: 'David R.', action: 'completed assessment', time: '1 hour ago' },
            { user: 'Priya M.', action: 'achieved 7-day streak', time: '2 hours ago' },
          ].map((activity, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b border-white/[0.04] last:border-0">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary-light">
                  {activity.user[0]}
                </div>
                <div>
                  <span className="text-sm text-text-primary font-medium">{activity.user}</span>
                  <span className="text-sm text-text-muted"> {activity.action}</span>
                </div>
              </div>
              <span className="text-xs text-text-muted">{activity.time}</span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default AdminDashboard;
