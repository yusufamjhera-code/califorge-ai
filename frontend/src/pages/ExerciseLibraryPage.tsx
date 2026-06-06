import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter } from 'lucide-react';
import { exercises } from '../data/exercises';
import { ExerciseCard } from '../components/workout/ExerciseCard';
import type { ExerciseCategory } from '../types';

const categories: { value: ExerciseCategory | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'push', label: 'Push' },
  { value: 'pull', label: 'Pull' },
  { value: 'legs', label: 'Legs' },
  { value: 'core', label: 'Core' },
  { value: 'conditioning', label: 'Conditioning' },
  { value: 'mobility', label: 'Mobility' },
];

const ExerciseLibraryPage: React.FC = () => {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<ExerciseCategory | 'all'>('all');

  const filtered = useMemo(() => {
    return exercises.filter((e) => {
      const matchesCategory = category === 'all' || e.category === category;
      const matchesSearch = search === '' || e.name.toLowerCase().includes(search.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [search, category]);

  return (
    <div className="w-full">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-heading font-bold text-text-primary mb-2">Exercise Library</h1>
        <p className="text-text-muted mb-6">{exercises.length} bodyweight exercises — no equipment needed</p>
      </motion.div>

      {/* Search & Filter */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="space-y-4 mb-8"
      >
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Search exercises..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-11 pr-4 py-3 bg-surface border border-border rounded-xl text-text-primary placeholder:text-text-muted focus:outline-none focus:border-primary/40 transition-colors"
          />
        </div>

        {/* Category tabs */}
        <div className="flex gap-2 overflow-x-auto pb-1">
          {categories.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setCategory(cat.value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                category === cat.value
                  ? 'bg-primary text-white'
                  : 'bg-surface text-text-muted hover:text-text-secondary border border-border'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </motion.div>

      {/* Results */}
      <div className="space-y-3">
        {filtered.map((exercise, index) => (
          <ExerciseCard
            key={exercise.id}
            exercise={exercise}
            sets={exercise.defaultSets}
            reps={exercise.isTimeBased ? undefined : exercise.defaultReps}
            duration={exercise.isTimeBased ? exercise.defaultDuration : undefined}
            index={index}
          />
        ))}
        {filtered.length === 0 && (
          <div className="text-center py-16 text-text-muted">
            <Filter className="w-10 h-10 mx-auto mb-3 opacity-30" />
            <p>No exercises match your search.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExerciseLibraryPage;
