import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, LogOut, Settings, Shield, Edit2, Info } from 'lucide-react';
import { useAuthStore } from '../stores/authStore';
import { Button } from '../components/ui/Button';
import { Modal } from '../components/ui/Modal';
import { useNavigate } from 'react-router-dom';
import { updateProfile } from 'firebase/auth';
import { auth } from '../services/firebase';

const ProfilePage: React.FC = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const [showEditProfile, setShowEditProfile] = useState(false);
  const [showPreferences, setShowPreferences] = useState(false);
  const [displayName, setDisplayName] = useState(user?.displayName || '');
  const [isUpdating, setIsUpdating] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleUpdateProfile = async () => {
    if (!auth.currentUser) return;
    setIsUpdating(true);
    try {
      await updateProfile(auth.currentUser, {
        displayName: displayName
      });
      // Force reload to pick up new display name locally
      window.location.reload();
    } catch (err) {
      console.error('Failed to update profile', err);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="w-full max-w-3xl">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-heading font-bold text-text-primary mb-8">Profile</h1>
      </motion.div>

      {/* Avatar & Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/[0.03] border border-white/[0.06] rounded-2xl p-8 mb-6 text-center relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 p-4">
           <button onClick={() => setShowEditProfile(true)} className="p-2 bg-white/5 hover:bg-white/10 rounded-full transition-colors text-text-muted hover:text-text-primary">
             <Edit2 className="w-4 h-4" />
           </button>
        </div>
        <div className="w-20 h-20 rounded-full gradient-primary flex items-center justify-center text-3xl font-heading font-bold text-white mx-auto mb-4">
          {user?.displayName?.[0]?.toUpperCase() || 'U'}
        </div>
        <h2 className="text-xl font-heading font-semibold text-text-primary">{user?.displayName || 'User'}</h2>
        <p className="text-sm text-text-muted mt-1">{user?.email || 'user@example.com'}</p>
      </motion.div>

      {/* Settings list */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white/[0.03] border border-white/[0.06] rounded-2xl overflow-hidden mb-6"
      >
        {[
          { icon: User, label: 'Edit Profile', action: () => setShowEditProfile(true) },
          { icon: Settings, label: 'Preferences', action: () => setShowPreferences(true) },
          { icon: Shield, label: 'Retake Assessment', action: () => navigate('/assessment') },
        ].map((item) => (
          <button
            key={item.label}
            onClick={item.action}
            className="w-full flex items-center gap-4 p-5 text-left hover:bg-white/[0.03] transition-colors border-b border-white/[0.04] last:border-b-0 group"
          >
            <item.icon className="w-5 h-5 text-text-muted group-hover:text-primary transition-colors" />
            <span className="text-text-primary font-medium">{item.label}</span>
          </button>
        ))}
      </motion.div>

      {/* Logout */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Button
          variant="danger"
          className="w-full"
          icon={<LogOut className="w-4 h-4" />}
          onClick={handleLogout}
        >
          Sign Out
        </Button>
      </motion.div>

      {/* Edit Profile Modal */}
      <Modal isOpen={showEditProfile} onClose={() => setShowEditProfile(false)} title="Edit Profile">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text-muted mb-1">Display Name</label>
            <input 
              type="text" 
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="w-full px-4 py-3 bg-background border border-white/10 rounded-xl text-text-primary focus:border-primary focus:outline-none transition-colors"
              placeholder="Your name"
            />
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button variant="ghost" onClick={() => setShowEditProfile(false)}>Cancel</Button>
            <Button onClick={handleUpdateProfile} disabled={isUpdating}>
              {isUpdating ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </div>
      </Modal>

      {/* Preferences Modal */}
      <Modal isOpen={showPreferences} onClose={() => setShowPreferences(false)} title="Preferences">
        <div className="py-6 flex flex-col items-center justify-center text-center">
          <div className="w-12 h-12 bg-primary/10 text-primary rounded-full flex items-center justify-center mb-4">
            <Info className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-heading font-semibold text-text-primary mb-2">Coming Soon</h3>
          <p className="text-text-muted">
            Advanced application preferences (theme, notification toggles, units) are currently under development. 
            Check back in a future update!
          </p>
          <div className="mt-6">
            <Button onClick={() => setShowPreferences(false)}>Got it</Button>
          </div>
        </div>
      </Modal>

    </div>
  );
};

export default ProfilePage;
