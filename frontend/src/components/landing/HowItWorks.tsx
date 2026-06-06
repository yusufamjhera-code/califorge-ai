import React from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, BarChart3, Play, TrendingUp } from 'lucide-react';

const steps = [
  {
    icon: ClipboardList,
    number: '01',
    title: 'Assess',
    description: 'Complete a comprehensive 36-question assessment covering your fitness, lifestyle, recovery, and goals.',
    color: '#6C5CE7',
  },
  {
    icon: BarChart3,
    number: '02',
    title: 'Analyze',
    description: 'Our AI engine calculates your Fitness, Strength, Recovery, Consistency, and Mobility scores.',
    color: '#00D2FF',
  },
  {
    icon: Play,
    number: '03',
    title: 'Train',
    description: 'Follow your personalized weekly workout plan with guided exercises, sets, reps, and rest periods.',
    color: '#00E676',
  },
  {
    icon: TrendingUp,
    number: '04',
    title: 'Progress',
    description: 'Track your improvements, unlock harder exercises, and watch your transformation unfold.',
    color: '#FFD600',
  },
];

export const HowItWorks: React.FC = () => {
  return (
    <section style={{ position: 'relative', width: '100%', paddingTop: '120px', paddingBottom: '120px', paddingLeft: '24px', paddingRight: '24px', overflow: 'hidden' }}>
      {/* Background accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/[0.02] to-transparent" />

      <div style={{ position: 'relative', width: '100%', maxWidth: '1280px', marginLeft: 'auto', marginRight: 'auto' }}>
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ duration: 0.6 }}
          style={{ textAlign: 'center', marginBottom: '80px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
        >
          <h2 className="text-4xl md:text-6xl font-heading font-bold" style={{ marginBottom: '24px' }}>
            How <span className="gradient-text">CaliForge</span> Works
          </h2>
          <p className="text-text-secondary text-xl" style={{ maxWidth: '560px', textAlign: 'center' }}>
            From assessment to transformation in four simple steps.
          </p>
        </motion.div>

        {/* Steps */}
        <div style={{ position: 'relative', width: '100%' }}>
          {/* Connecting line */}
          <div className="hidden lg:block absolute top-24 left-[12.5%] right-[12.5%] h-px bg-gradient-to-r from-transparent via-border to-transparent" />

          <div className="steps-grid">
            {steps.map((step, index) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
              >
                {/* Step number circle */}
                <div style={{ position: 'relative', display: 'inline-flex', marginBottom: '24px' }}>
                  <motion.div
                    whileHover={{ scale: 1.1 }}
                    className="w-24 h-24 rounded-2xl bg-surface border border-border flex items-center justify-center group-hover:border-primary/30 transition-colors duration-300"
                    style={{
                      boxShadow: `0 0 30px ${step.color}10`,
                    }}
                  >
                    <step.icon className="w-10 h-10" style={{ color: step.color }} />
                  </motion.div>
                  <span
                    className="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white"
                    style={{ backgroundColor: step.color }}
                  >
                    {step.number}
                  </span>
                </div>

                {/* Content */}
                <h3 className="text-2xl font-heading font-semibold text-text-primary" style={{ marginBottom: '12px' }}>
                  {step.title}
                </h3>
                <p className="text-text-secondary text-base leading-relaxed" style={{ maxWidth: '280px', textAlign: 'center' }}>
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};
