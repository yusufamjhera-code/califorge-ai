import React from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Mail, Lock, Chrome } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useAuthStore } from '../../stores/authStore';

const loginSchema = z.object({
  email: z.string().email('Enter a valid email'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

interface LoginFormProps {
  onSwitchToSignup: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToSignup }) => {
  const { login, loginWithGoogle, loading, error, clearError } = useAuthStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    clearError();
    try {
      await login(data.email, data.password);
    } catch {
      // Error handled in store
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-md"
    >
      <h2 className="text-3xl font-heading font-bold mb-2">Welcome back</h2>
      <p className="text-text-secondary mb-8">Sign in to continue your training</p>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 p-4 rounded-xl bg-error/10 border border-error/30 text-error text-sm"
        >
          {error}
        </motion.div>
      )}

      <form onSubmit={(e) => void handleSubmit(onSubmit)(e)} className="space-y-5">
        <Input
          label="Email"
          type="email"
          icon={<Mail className="w-4 h-4" />}
          error={errors.email?.message}
          {...register('email')}
        />
        <Input
          label="Password"
          type="password"
          icon={<Lock className="w-4 h-4" />}
          error={errors.password?.message}
          {...register('password')}
        />

        <Button type="submit" variant="primary" size="lg" className="w-full" loading={loading}>
          Sign In
        </Button>
      </form>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-white/10" />
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="px-4 bg-bg text-text-muted">or continue with</span>
        </div>
      </div>

      <Button
        variant="secondary"
        size="lg"
        className="w-full"
        icon={<Chrome className="w-5 h-5" />}
        onClick={() => void loginWithGoogle()}
        loading={loading}
      >
        Google
      </Button>

      <p className="mt-8 text-center text-sm text-text-secondary">
        Don't have an account?{' '}
        <button onClick={onSwitchToSignup} className="text-primary hover:text-primary-light font-medium transition-colors">
          Sign up
        </button>
      </p>
    </motion.div>
  );
};
