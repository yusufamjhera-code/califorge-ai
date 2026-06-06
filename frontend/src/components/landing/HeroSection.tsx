import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';

export const HeroSection: React.FC = () => {
  const navigate = useNavigate();

  return (
    <section style={{ position: 'relative', width: '100%', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
      {/* Animated gradient background */}
      <div className="absolute inset-0 gradient-hero" />

      {/* Floating orbs */}
      <motion.div
        animate={{ y: [-20, 20, -20], x: [-10, 10, -10] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-primary/10 blur-3xl"
      />
      <motion.div
        animate={{ y: [20, -20, 20], x: [10, -10, 10] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full bg-accent/10 blur-3xl"
      />
      <motion.div
        animate={{ y: [10, -30, 10] }}
        transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute top-1/3 right-1/3 w-48 h-48 rounded-full bg-primary-light/5 blur-3xl"
      />

      {/* Content */}
      <div style={{ position: 'relative', zIndex: 10, width: '100%', maxWidth: '1024px', paddingLeft: '24px', paddingRight: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20"
          style={{ marginBottom: '32px' }}
        >
          <Sparkles className="w-4 h-4 text-primary-light" />
          <span className="text-sm font-medium text-primary-light">AI-Powered Calisthenics Coach</span>
        </motion.div>

        {/* Main heading */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="text-5xl md:text-7xl lg:text-8xl font-heading font-black leading-[0.95]"
          style={{ marginBottom: '24px' }}
        >
          Your Body Is
          <br />
          <span className="gradient-text">The Gym</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="text-lg md:text-xl text-text-secondary leading-relaxed"
          style={{ maxWidth: '672px', marginLeft: 'auto', marginRight: 'auto', marginBottom: '40px' }}
        >
          Get a personalized calisthenics transformation plan crafted by AI.
          No gym. No equipment. Just your body and a custom roadmap to your best physique.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
          style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', justifyContent: 'center', alignItems: 'center' }}
        >
          <Button
            size="lg"
            glow
            onClick={() => navigate('/auth')}
            icon={<ArrowRight className="w-5 h-5" />}
            className="text-base px-10"
          >
            Start Your Transformation
          </Button>
          <Button
            variant="secondary"
            size="lg"
            onClick={() => {
              document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
            }}
            className="text-base"
          >
            Learn More
          </Button>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.5 }}
          style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '64px', marginTop: '80px', width: '100%' }}
        >
          {[
            { value: '100%', label: 'Bodyweight' },
            { value: '0', label: 'Equipment Needed' },
            { value: '30+', label: 'Exercises' },
            { value: 'AI', label: 'Personalized' },
          ].map((stat) => (
            <div key={stat.label} style={{ textAlign: 'center' }}>
              <div className="text-2xl md:text-3xl font-heading font-bold gradient-text">{stat.value}</div>
              <div className="text-sm text-text-muted" style={{ marginTop: '4px' }}>{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <div className="w-6 h-10 rounded-full border-2 border-white/20 flex items-start justify-center p-1.5">
          <motion.div
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-1.5 h-1.5 rounded-full bg-primary-light"
          />
        </div>
      </motion.div>
    </section>
  );
};
