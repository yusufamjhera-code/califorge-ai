import { create } from 'zustand';
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  updateProfile,
  type User as FirebaseUser,
} from 'firebase/auth';
import { auth, googleProvider } from '../services/firebase';
import api from '../services/api';
import type { User } from '../types';

interface AuthState {
  user: User | null;
  firebaseUser: FirebaseUser | null;
  loading: boolean;
  error: string | null;
  initialized: boolean;

  initialize: () => () => void;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, displayName: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

const mapFirebaseUser = (fbUser: FirebaseUser): User => ({
  id: fbUser.uid,
  email: fbUser.email ?? '',
  displayName: fbUser.displayName ?? 'User',
  photoURL: fbUser.photoURL ?? undefined,
  role: 'user',
  createdAt: fbUser.metadata.creationTime ?? new Date().toISOString(),
  assessmentCompleted: false,
});

const syncWithBackend = async (fbUser: FirebaseUser): Promise<User> => {
  try {
    const response = await api.post('/auth/register');
    const data = response.data;
    return {
      id: data.firebase_uid,
      email: data.email ?? '',
      displayName: data.display_name ?? 'User',
      photoURL: data.photo_url ?? undefined,
      role: data.is_admin ? 'admin' : 'user',
      createdAt: data.created_at,
      assessmentCompleted: data.assessment_completed,
    };
  } catch (err) {
    console.error('Failed to sync user with backend', err);
    return mapFirebaseUser(fbUser);
  }
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  firebaseUser: null,
  loading: true,
  error: null,
  initialized: false,

  initialize: () => {
    const unsubscribe = onAuthStateChanged(auth, async (fbUser) => {
      if (fbUser) {
        // Optimistic UI update
        set({ firebaseUser: fbUser, user: mapFirebaseUser(fbUser), initialized: true });
        // Sync with backend
        const dbUser = await syncWithBackend(fbUser);
        set({ user: dbUser, loading: false });
      } else {
        set({
          firebaseUser: null,
          user: null,
          loading: false,
          initialized: true,
        });
      }
    });
    return unsubscribe;
  },

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      const dbUser = await syncWithBackend(result.user);
      set({ firebaseUser: result.user, user: dbUser, loading: false });
    } catch (err) {
      set({ error: err instanceof Error ? err.message : 'Login failed', loading: false });
      throw err;
    }
  },

  signup: async (email, password, displayName) => {
    set({ loading: true, error: null });
    try {
      const result = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(result.user, { displayName });
      const dbUser = await syncWithBackend(result.user);
      set({ firebaseUser: result.user, user: dbUser, loading: false });
    } catch (err) {
      set({ error: err instanceof Error ? err.message : 'Signup failed', loading: false });
      throw err;
    }
  },

  loginWithGoogle: async () => {
    set({ loading: true, error: null });
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const dbUser = await syncWithBackend(result.user);
      set({ firebaseUser: result.user, user: dbUser, loading: false });
    } catch (err) {
      set({ error: err instanceof Error ? err.message : 'Google login failed', loading: false });
      throw err;
    }
  },

  logout: async () => {
    set({ loading: true });
    await signOut(auth);
    set({ user: null, firebaseUser: null, loading: false });
  },

  clearError: () => set({ error: null }),
}));
