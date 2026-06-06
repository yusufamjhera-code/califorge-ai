import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Dumbbell,
  Calendar,
  Library,
  BarChart3,
  User,
  Zap,
} from 'lucide-react';

const sidebarLinks = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/workout', label: 'Today', icon: Dumbbell },
  { path: '/plan', label: 'Weekly Plan', icon: Calendar },
  { path: '/exercises', label: 'Exercises', icon: Library },
  { path: '/progress', label: 'Progress', icon: BarChart3 },
  { path: '/profile', label: 'Profile', icon: User },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <aside className="hidden lg:flex flex-col w-64 min-w-[16rem] h-screen sticky left-0 top-0 bg-surface/50 backdrop-blur-xl border-r border-white/5 z-30">
      {/* Logo */}
      <div className="px-6 h-16 flex items-center gap-2 border-b border-white/5">
        <div className="p-1.5 rounded-lg bg-gradient-to-br from-primary to-accent">
          <Zap className="w-5 h-5 text-white" />
        </div>
        <span className="text-lg font-heading font-bold gradient-text">CaliForge</span>
        <span className="text-[10px] font-medium text-accent px-1 py-0.5 rounded bg-accent/10 border border-accent/20">AI</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
        {sidebarLinks.map((link) => {
          const isActive = location.pathname === link.path;
          const Icon = link.icon;
          return (
            <Link key={link.path} to={link.path}>
              <motion.div
                whileHover={{ x: 4 }}
                whileTap={{ scale: 0.98 }}
                className={`
                  flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium
                  transition-all duration-200 relative
                  ${isActive
                    ? 'text-text-primary bg-white/10'
                    : 'text-text-secondary hover:text-text-primary hover:bg-white/5'
                  }
                `}
              >
                {isActive && (
                  <motion.div
                    layoutId="sidebar-active"
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 rounded-r-full bg-gradient-to-b from-primary to-primary-light"
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
                <Icon className="w-5 h-5 flex-shrink-0" />
                <span>{link.label}</span>
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="px-4 py-4 border-t border-white/5">
        <div className="p-4 rounded-xl bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20">
          <p className="text-xs font-heading font-semibold text-primary-light mb-1">Pro Tip</p>
          <p className="text-xs text-text-secondary leading-relaxed">
            Consistency beats intensity. Aim for 80% completion over perfection.
          </p>
        </div>
      </div>
    </aside>
  );
};
