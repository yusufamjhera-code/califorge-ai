import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, Star, Quote } from 'lucide-react';

const testimonials = [
  {
    name: 'Marcus J.',
    role: 'Lost 15kg in 4 months',
    avatar: 'M',
    rating: 5,
    text: "I couldn't do a single push-up when I started. CaliForge started me with wall push-ups and gradually progressed me. Now I'm doing diamonds. The AI knew exactly when to push me harder.",
    color: '#6C5CE7',
  },
  {
    name: 'Sarah K.',
    role: 'Busy Mom, 3 kids',
    avatar: 'S',
    rating: 5,
    text: "15-minute workouts in my living room while the kids nap. No excuses, no equipment, no gym commute. CaliForge fit perfectly into my chaotic schedule. I'm in the best shape of my life.",
    color: '#00D2FF',
  },
  {
    name: 'David R.',
    role: 'Former gym-goer',
    avatar: 'D',
    rating: 5,
    text: "I was skeptical that bodyweight-only could build real muscle. The progressive overload system proved me wrong. The adaptive difficulty keeps every workout challenging.",
    color: '#00E676',
  },
  {
    name: 'Priya M.',
    role: 'Complete beginner',
    avatar: 'P',
    rating: 5,
    text: "The assessment was so thorough — it asked about my sleep, stress, eating habits, everything. My plan felt like it was made by a personal trainer who actually knew me.",
    color: '#FFD600',
  },
];

export const Testimonials: React.FC = () => {
  const [current, setCurrent] = useState(0);

  const next = () => setCurrent((p) => (p + 1) % testimonials.length);
  const prev = () => setCurrent((p) => (p - 1 + testimonials.length) % testimonials.length);

  return (
    <section style={{ position: 'relative', width: '100%', paddingTop: '120px', paddingBottom: '120px', paddingLeft: '24px', paddingRight: '24px', overflow: 'hidden' }}>
      <div style={{ width: '100%', maxWidth: '960px', marginLeft: 'auto', marginRight: 'auto' }}>
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          style={{ textAlign: 'center', marginBottom: '80px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
        >
          <h2 className="text-4xl md:text-6xl font-heading font-bold" style={{ marginBottom: '24px' }}>
            Real People. <span className="gradient-text">Real Results.</span>
          </h2>
          <p className="text-text-secondary text-xl" style={{ maxWidth: '560px', textAlign: 'center' }}>
            Join thousands who have transformed their bodies with nothing but calisthenics.
          </p>
        </motion.div>

        {/* Testimonial carousel */}
        <div style={{ position: 'relative' }}>
          <AnimatePresence mode="wait">
            <motion.div
              key={current}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.4 }}
              className="bg-white/[0.03] backdrop-blur-xl border border-white/[0.06] rounded-3xl"
              style={{ padding: '48px', width: '100%' }}
            >
              <Quote className="w-10 h-10 text-primary/30" style={{ marginBottom: '24px' }} />

              <p className="text-lg md:text-xl text-text-primary leading-relaxed" style={{ marginBottom: '32px' }}>
                "{testimonials[current].text}"
              </p>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div
                    className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg"
                    style={{ backgroundColor: testimonials[current].color }}
                  >
                    {testimonials[current].avatar}
                  </div>
                  <div>
                    <div className="font-semibold text-text-primary">{testimonials[current].name}</div>
                    <div className="text-sm text-text-muted">{testimonials[current].role}</div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '4px' }}>
                  {Array.from({ length: testimonials[current].rating }).map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-warning text-warning" />
                  ))}
                </div>
              </div>
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '32px' }}>
            <button
              onClick={prev}
              className="w-10 h-10 rounded-full bg-surface border border-border flex items-center justify-center hover:bg-surface-hover hover:border-primary/30 transition-all"
            >
              <ChevronLeft className="w-5 h-5 text-text-secondary" />
            </button>

            {/* Dots */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              {testimonials.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrent(i)}
                  className={`h-2 rounded-full transition-all duration-300 ${
                    i === current ? 'w-6 bg-primary' : 'w-2 bg-border hover:bg-text-muted'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={next}
              className="w-10 h-10 rounded-full bg-surface border border-border flex items-center justify-center hover:bg-surface-hover hover:border-primary/30 transition-all"
            >
              <ChevronRight className="w-5 h-5 text-text-secondary" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};
