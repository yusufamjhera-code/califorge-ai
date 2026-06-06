import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, MoreVertical } from 'lucide-react';

const mockUsers = [
  { id: '1', name: 'Marcus Johnson', email: 'marcus@example.com', level: 'Novice', joined: 'Jan 15', workouts: 34, status: 'active' },
  { id: '2', name: 'Sarah Kim', email: 'sarah@example.com', level: 'Beginner', joined: 'Mar 2', workouts: 12, status: 'active' },
  { id: '3', name: 'David Rodriguez', email: 'david@example.com', level: 'Intermediate', joined: 'Nov 8', workouts: 87, status: 'active' },
  { id: '4', name: 'Priya Mehta', email: 'priya@example.com', level: 'Beginner', joined: 'Apr 20', workouts: 5, status: 'inactive' },
  { id: '5', name: 'Alex Chen', email: 'alex@example.com', level: 'Advanced', joined: 'Sep 1', workouts: 156, status: 'active' },
];

const UserManager: React.FC = () => {
  const [search, setSearch] = useState('');

  const filtered = mockUsers.filter(
    (u) => u.name.toLowerCase().includes(search.toLowerCase()) || u.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-heading font-bold text-text-primary mb-1">User Manager</h1>
        <p className="text-text-muted mb-8">{mockUsers.length} registered users</p>
      </motion.div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
        <input
          type="text"
          placeholder="Search users..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-11 pr-4 py-3 bg-surface border border-border rounded-xl text-text-primary placeholder:text-text-muted focus:outline-none focus:border-primary/40 transition-colors"
        />
      </div>

      {/* Table */}
      <div className="bg-white/[0.03] border border-white/[0.06] rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/[0.06]">
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">User</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Level</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Joined</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Workouts</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Status</th>
                <th className="text-right text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4"></th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((user, i) => (
                <motion.tr
                  key={user.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.05 }}
                  className="border-b border-white/[0.03] last:border-0 hover:bg-white/[0.02] transition-colors"
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold text-primary-light">
                        {user.name[0]}
                      </div>
                      <div>
                        <div className="font-medium text-text-primary text-sm">{user.name}</div>
                        <div className="text-xs text-text-muted">{user.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-text-secondary">{user.level}</span>
                  </td>
                  <td className="px-6 py-4 text-sm text-text-muted">{user.joined}</td>
                  <td className="px-6 py-4 text-sm text-text-primary">{user.workouts}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-md text-xs ${
                      user.status === 'active'
                        ? 'bg-success/10 text-success border border-success/20'
                        : 'bg-white/[0.03] text-text-muted border border-white/[0.06]'
                    }`}>
                      {user.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="w-8 h-8 rounded-lg bg-white/[0.03] flex items-center justify-center hover:bg-white/[0.06] transition-colors">
                      <MoreVertical className="w-4 h-4 text-text-muted" />
                    </button>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UserManager;
