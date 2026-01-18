/**
 * Register Form Component
 */

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Mail, Lock, User } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

const registerSchema = z
  .object({
    first_name: z.string().min(1, 'First name is required'),
    last_name: z.string().min(1, 'Last name is required'),
    email: z.string().email('Please enter a valid email address'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
      .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
      .regex(/[0-9]/, 'Password must contain at least one number'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

type RegisterFormData = z.infer<typeof registerSchema>;

interface RegisterFormProps {
  onSuccess?: () => void;
}

export function RegisterForm({ onSuccess }: RegisterFormProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { register: registerUser } = useAuth();
  const { error, success } = useToast();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    try {
      await registerUser({
        email: data.email,
        password: data.password,
        first_name: data.first_name,
        last_name: data.last_name,
      });
      success('Welcome to FFX NOVA!', 'Your account has been created successfully.');
      onSuccess?.();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Registration failed. Please try again.';
      error('Registration failed', message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Input
          {...register('first_name')}
          label="First Name"
          placeholder="John"
          error={errors.first_name?.message}
          leftIcon={<User className="w-5 h-5" />}
          autoComplete="given-name"
        />

        <Input
          {...register('last_name')}
          label="Last Name"
          placeholder="Doe"
          error={errors.last_name?.message}
          autoComplete="family-name"
        />
      </div>

      <Input
        {...register('email')}
        type="email"
        label="Email"
        placeholder="you@example.com"
        error={errors.email?.message}
        leftIcon={<Mail className="w-5 h-5" />}
        autoComplete="email"
      />

      <Input
        {...register('password')}
        type={showPassword ? 'text' : 'password'}
        label="Password"
        placeholder="Create a strong password"
        error={errors.password?.message}
        hint="At least 8 characters with uppercase, lowercase, and number"
        leftIcon={<Lock className="w-5 h-5" />}
        rightIcon={
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        }
        autoComplete="new-password"
      />

      <Input
        {...register('confirmPassword')}
        type={showConfirmPassword ? 'text' : 'password'}
        label="Confirm Password"
        placeholder="Confirm your password"
        error={errors.confirmPassword?.message}
        leftIcon={<Lock className="w-5 h-5" />}
        rightIcon={
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
          >
            {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        }
        autoComplete="new-password"
      />

      <div className="text-sm text-slate-600 dark:text-slate-400">
        By creating an account, you agree to our{' '}
        <a href="/terms" className="text-primary-600 dark:text-primary-400 hover:underline">
          Terms of Service
        </a>{' '}
        and{' '}
        <a href="/privacy" className="text-primary-600 dark:text-primary-400 hover:underline">
          Privacy Policy
        </a>
        .
      </div>

      <Button type="submit" className="w-full" size="lg" isLoading={isLoading}>
        Create Account
      </Button>
    </form>
  );
}
