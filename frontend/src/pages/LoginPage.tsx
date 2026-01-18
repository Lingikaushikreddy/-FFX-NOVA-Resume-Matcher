/**
 * Login Page
 */

import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LoginForm } from '../components/forms/LoginForm';

export function LoginPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex items-center gap-2 mb-6">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-xl" />
              <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-900 to-secondary-900 dark:from-primary-400 dark:to-secondary-400">
                FFX NOVA
              </span>
            </Link>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Welcome back</h1>
            <p className="mt-2 text-slate-600 dark:text-slate-400">
              Sign in to continue your job search journey
            </p>
          </div>

          <LoginForm onSuccess={() => navigate('/dashboard')} />

          <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-medium text-primary-600 dark:text-primary-400 hover:underline"
            >
              Create one now
            </Link>
          </p>
        </motion.div>
      </div>

      {/* Right Side - Decorative */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-primary-600 to-secondary-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20" />
        <div className="relative z-10 flex flex-col items-center justify-center p-12 text-white">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="text-center max-w-lg"
          >
            <h2 className="text-3xl font-bold mb-4">
              Your Dream Federal Career Awaits
            </h2>
            <p className="text-lg text-white/80 mb-8">
              Join thousands of professionals who've found their perfect match in Federal, Military, and Contractor positions.
            </p>
            <div className="grid grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-4xl font-bold">10K+</div>
                <div className="text-sm text-white/70">Active Jobs</div>
              </div>
              <div>
                <div className="text-4xl font-bold">95%</div>
                <div className="text-sm text-white/70">Match Rate</div>
              </div>
              <div>
                <div className="text-4xl font-bold">5K+</div>
                <div className="text-sm text-white/70">Placements</div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
