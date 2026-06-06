import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Zap } from 'lucide-react';
import { Button } from '../ui/Button';
import { useAuthStore } from '../../stores/authStore';

const navLinks = [
  { path: '/', label: 'Home' },
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/workout', label: 'Workout' },
  { path: '/progress', label: 'Progress' },
];

export const Navbar: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuthStore();

  return (
    <nav className="fixed top-0 left-0 right-0 z-40 bg-bg/80 backdrop-blur-xl border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <motion.div
              whileHover={{ rotate: 20 }}
              className="p-1.5 rounded-lg bg-gradient-to-br from-primary to-accent"
            >
              <Zap className="w-5 h-5 text-white" />
            </motion.div>
            <span className="text-lg font-heading font-bold gradient-text">
              CaliForge
            </span>
            <span className="text-xs font-medium text-accent px-1.5 py-0.5 rounded-md bg-accent/10 border border-accent/20">
              AI
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {user &&
              navLinks.map((link) => {
                const isActive = location.pathname === link.path;
                return (
                  <Link key={link.path} to={link.path}>
                    <motion.div
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className={`
                        px-4 py-2 rounded-lg text-sm font-medium transition-colors
                        ${isActive
                          ? 'text-text-primary bg-white/10'
                          : 'text-text-secondary hover:text-text-primary hover:bg-white/5'
                        }
                      `}
                    >
                      {link.label}
                    </motion.div>
                  </Link>
                );
              })}
          </div>

          {/* Auth Actions */}
          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  {user.photoURL ? (
                    <img src={user.photoURL} alt="" className="w-8 h-8 rounded-full border border-white/20" />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-xs font-bold">
                      {user.displayName[0]?.toUpperCase()}
                    </div>
                  )}
                  <span className="text-sm text-text-secondary">{user.displayName}</span>
                </div>
                <Button variant="ghost" size="sm" onClick={() => void logout()}>
                  Sign out
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/auth">
                  <Button variant="ghost" size="sm">Log in</Button>
                </Link>
                <Link to="/auth?mode=signup">
                  <Button variant="primary" size="sm">Get Started</Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-white/10 text-text-secondary"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </motion.button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-white/5 bg-bg/95 backdrop-blur-xl overflow-hidden"
          >
            <div className="px-4 py-4 space-y-2">
              {user &&
                navLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={() => setMobileOpen(false)}
                    className={`
                      block px-4 py-3 rounded-xl text-sm font-medium transition-colors
                      ${location.pathname === link.path
                        ? 'text-text-primary bg-white/10'
                        : 'text-text-secondary hover:bg-white/5'
                      }
                    `}
                  >
                    {link.label}
                  </Link>
                ))}
              <div className="pt-3 border-t border-white/10">
                {user ? (
                  <Button variant="ghost" size="sm" className="w-full" onClick={() => { void logout(); setMobileOpen(false); }}>
                    Sign out
                  </Button>
                ) : (
                  <Link to="/auth" onClick={() => setMobileOpen(false)}>
                    <Button variant="primary" size="sm" className="w-full">Get Started</Button>
                  </Link>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};
