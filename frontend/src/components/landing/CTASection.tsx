import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';

export const CTASection: React.FC = () => {
  const navigate = useNavigate();

  return (
    <section style={{ position: 'relative', width: '100%', paddingTop: '120px', paddingBottom: '120px', paddingLeft: '24px', paddingRight: '24px', overflow: 'hidden' }}>
      {/* Background gradient orbs */}
      <motion.div
        animate={{ scale: [1, 1.2, 1], rotate: [0, 90, 0] }}
        transition={{ duration: 15, repeat: Infinity }}
        className="absolute top-0 left-1/4 w-96 h-96 rounded-full bg-primary/10 blur-[100px]"
      />
      <motion.div
        animate={{ scale: [1, 1.5, 1], rotate: [0, -90, 0] }}
        transition={{ duration: 20, repeat: Infinity }}
        className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-accent/10 blur-[100px]"
      />

      <div style={{ position: 'relative', width: '100%', maxWidth: '896px', marginLeft: 'auto', marginRight: 'auto', textAlign: 'center', zIndex: 10 }}>
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-success/10 border border-success/20"
          style={{ marginBottom: '32px' }}
        >
          <Zap className="w-4 h-4 text-success" />
          <span className="text-sm font-medium text-success">Free to get started</span>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <h2 className="text-4xl md:text-6xl font-heading font-bold" style={{ marginBottom: '32px', textAlign: 'center' }}>
            Ready to{' '}
            <span className="gradient-text-accent">
              Transform?
            </span>
          </h2>
          <p className="text-xl md:text-2xl text-text-secondary leading-relaxed" style={{ maxWidth: '672px', marginLeft: 'auto', marginRight: 'auto', textAlign: 'center', marginBottom: '48px' }}>
            Take the 5-minute assessment and receive your personalized calisthenics
            transformation plan. Your journey starts with a single step.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Button
            size="lg"
            glow
            onClick={() => navigate('/auth')}
            icon={<ArrowRight className="w-5 h-5" />}
            className="text-base px-12"
          >
            Begin Your Assessment
          </Button>
        </motion.div>
      </div>
    </section>
  );
};
