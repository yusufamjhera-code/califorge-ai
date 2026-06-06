import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Search, Edit2, Trash2 } from 'lucide-react';
import { exercises } from '../../data/exercises';
import { Button } from '../../components/ui/Button';

const ExerciseManager: React.FC = () => {
  const [search, setSearch] = useState('');

  const filtered = exercises.filter((e) =>
    e.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-heading font-bold text-text-primary mb-1">Exercise Manager</h1>
            <p className="text-text-muted">{exercises.length} exercises in library</p>
          </div>
          <Button icon={<Plus className="w-4 h-4" />}>Add Exercise</Button>
        </div>
      </motion.div>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
        <input
          type="text"
          placeholder="Search exercises..."
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
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Exercise</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Category</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Difficulty</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Muscles</th>
                <th className="text-right text-xs font-semibold text-text-muted uppercase tracking-wider px-6 py-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((exercise, i) => (
                <motion.tr
                  key={exercise.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.03 }}
                  className="border-b border-white/[0.03] last:border-0 hover:bg-white/[0.02] transition-colors"
                >
                  <td className="px-6 py-4">
                    <span className="font-medium text-text-primary">{exercise.name}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 text-xs rounded-md bg-primary/10 text-primary-light border border-primary/20 capitalize">
                      {exercise.category}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-text-secondary capitalize">{exercise.difficulty}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-text-muted">
                      {exercise.muscleGroups.slice(0, 2).join(', ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button className="w-8 h-8 rounded-lg bg-white/[0.03] border border-white/[0.06] flex items-center justify-center hover:bg-white/[0.06] transition-colors">
                        <Edit2 className="w-3.5 h-3.5 text-text-muted" />
                      </button>
                      <button className="w-8 h-8 rounded-lg bg-error/5 border border-error/15 flex items-center justify-center hover:bg-error/10 transition-colors">
                        <Trash2 className="w-3.5 h-3.5 text-error" />
                      </button>
                    </div>
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

export default ExerciseManager;
