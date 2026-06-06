import React, { useEffect, lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { useAuthStore } from './stores/authStore';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { LoadingSpinner } from './components/ui/LoadingSpinner';
import { AdminLayout } from './components/admin/AdminLayout';
import { AppLayout } from './components/layout/AppLayout';

// Lazy-loaded pages for code splitting
const LandingPage = lazy(() => import('./pages/LandingPage'));
const AuthPage = lazy(() => import('./pages/AuthPage'));
const AssessmentPage = lazy(() => import('./pages/AssessmentPage'));
const AnalysisPage = lazy(() => import('./pages/AnalysisPage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const WorkoutPage = lazy(() => import('./pages/WorkoutPage'));
const WeeklyPlanPage = lazy(() => import('./pages/WeeklyPlanPage'));
const ExerciseLibraryPage = lazy(() => import('./pages/ExerciseLibraryPage'));
const ProgressPage = lazy(() => import('./pages/ProgressPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard'));
const ExerciseManager = lazy(() => import('./pages/admin/ExerciseManager'));
const UserManager = lazy(() => import('./pages/admin/UserManager'));

const PageLoader = () => (
  <div className="min-h-screen bg-bg flex items-center justify-center">
    <LoadingSpinner size="lg" />
  </div>
);

const App: React.FC = () => {
  const { initialize, initialized } = useAuthStore();

  useEffect(() => {
    const unsubscribe = initialize();
    return unsubscribe;
  }, [initialize]);

  if (!initialized) {
    return <PageLoader />;
  }

  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <AnimatePresence mode="wait">
          <Routes>
            {/* Public routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/auth" element={<AuthPage />} />

            {/* Assessment flow (requires auth) */}
            <Route element={<ProtectedRoute />}>
              <Route path="/assessment" element={<AssessmentPage />} />
              <Route path="/analysis" element={<AnalysisPage />} />
            </Route>

            {/* App routes with sidebar layout */}
            <Route element={<ProtectedRoute />}>
              <Route element={<AppLayout />}>
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/workout" element={<WorkoutPage />} />
                <Route path="/plan" element={<WeeklyPlanPage />} />
                <Route path="/exercises" element={<ExerciseLibraryPage />} />
                <Route path="/progress" element={<ProgressPage />} />
                <Route path="/profile" element={<ProfilePage />} />
              </Route>
            </Route>

            {/* Admin routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/admin" element={<AdminLayout />}>
                <Route index element={<AdminDashboard />} />
                <Route path="exercises" element={<ExerciseManager />} />
                <Route path="users" element={<UserManager />} />
              </Route>
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AnimatePresence>
      </Suspense>
    </BrowserRouter>
  );
};

export default App;
