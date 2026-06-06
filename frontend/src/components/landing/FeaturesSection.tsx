import React from 'react';
import { motion } from 'framer-motion';
import {
  Brain,
  Target,
  TrendingUp,
  Dumbbell,
  Flame,
  Users,
} from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Plans',
    description: 'Our intelligent engine analyzes 36+ data points to create a plan uniquely tailored to your body, goals, and lifestyle.',
    color: 'from-purple-500 to-indigo-500',
  },
  {
    icon: Dumbbell,
    title: 'Zero Equipment',
    description: 'Every exercise uses only your bodyweight. Train anywhere — your living room, park, or hotel room.',
    color: 'from-cyan-500 to-blue-500',
  },
  {
    icon: Target,
    title: 'Targeted Training',
    description: 'Focus on the areas that matter most to you. Full body, upper body, core, or legs — you choose.',
    color: 'from-orange-500 to-red-500',
  },
  {
    icon: TrendingUp,
    title: 'Adaptive Progression',
    description: 'Your plan evolves with you. As you get stronger, exercises automatically level up to keep challenging you.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: Flame,
    title: 'Smart Recovery',
    description: 'Built-in recovery scoring ensures you train optimally — no burnout, no overtraining, just consistent gains.',
    color: 'from-yellow-500 to-orange-500',
  },
  {
    icon: Users,
    title: 'Beginner Friendly',
    description: "Can't do a push-up? No problem. We start exactly where you are and build from there, step by step.",
    color: 'from-pink-500 to-rose-500',
  },
];

const containerVariants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.1 },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export const FeaturesSection: React.FC = () => {
  return (
    <section id="features" style={{ position: 'relative', width: '100%', paddingTop: '120px', paddingBottom: '120px', paddingLeft: '24px', paddingRight: '24px', overflow: 'hidden' }}>
      <div style={{ width: '100%', maxWidth: '1280px', marginLeft: 'auto', marginRight: 'auto' }}>
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6 }}
          style={{ textAlign: 'center', marginBottom: '80px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
        >
          <h2 className="text-4xl md:text-6xl font-heading font-bold" style={{ marginBottom: '24px' }}>
            Everything You Need.
            <br />
            <span className="gradient-text">Nothing You Don't.</span>
          </h2>
          <p className="text-text-secondary text-xl leading-relaxed" style={{ maxWidth: '672px', textAlign: 'center' }}>
            No gym memberships. No expensive equipment. Just science-backed calisthenics
            programs designed by artificial intelligence.
          </p>
        </motion.div>

        {/* Feature Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-50px' }}
          className="feature-grid"
        >
          {features.map((feature) => (
            <motion.div
              key={feature.title}
              variants={cardVariants}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className="group relative bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-2xl hover:bg-white/[0.06] hover:border-white/[0.12] transition-all duration-300"
              style={{ padding: '40px' }}
            >
              {/* Icon */}
              <div className={`inline-flex p-4 rounded-xl bg-gradient-to-br ${feature.color}`} style={{ marginBottom: '24px' }}>
                <feature.icon className="w-8 h-8 text-white" />
              </div>

              {/* Content */}
              <h3 className="text-2xl font-heading font-semibold text-text-primary" style={{ marginBottom: '12px' }}>
                {feature.title}
              </h3>
              <p className="text-text-secondary leading-relaxed text-lg">
                {feature.description}
              </p>

              {/* Hover glow */}
              <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none" />
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};
