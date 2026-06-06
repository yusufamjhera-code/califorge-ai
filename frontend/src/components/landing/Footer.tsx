import React from 'react';
import { Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-border py-8 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="text-xl font-heading font-bold gradient-text">CaliForge</span>
          <span className="text-text-muted text-sm">AI</span>
        </div>

        <div className="flex items-center gap-1 text-sm text-text-muted">
          <span>Built with</span>
          <Heart className="w-3.5 h-3.5 text-error fill-error" />
          <span>for the calisthenics community</span>
        </div>

        <div className="flex gap-6 text-sm text-text-muted">
          <a href="#" className="hover:text-text-primary transition-colors">Privacy</a>
          <a href="#" className="hover:text-text-primary transition-colors">Terms</a>
          <a href="#" className="hover:text-text-primary transition-colors">Contact</a>
        </div>
      </div>
    </footer>
  );
};
