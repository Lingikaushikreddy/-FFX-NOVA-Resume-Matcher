/**
 * Register Page
 */

import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { RegisterForm } from '../components/forms/RegisterForm';
import { CheckCircle } from 'lucide-react';

export function RegisterPage() {
  const navigate = useNavigate();

  const benefits = [
    'AI-powered job matching tailored for Federal & Military careers',
    'Security clearance-aware recommendations',
    'Skill gap analysis with upskilling paths',
    'Personalized career insights dashboard',
    'Save and track your job applications',
  ];

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Decorative */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-secondary-600 to-primary-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20" />
        <div className="relative z-10 flex flex-col items-start justify-center p-12 text-white">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="max-w-lg"
          >
            <h2 className="text-3xl font-bold mb-6">
              Start Your Federal Career Journey
            </h2>
            <p className="text-lg text-white/80 mb-8">
              Create your free account and unlock the power of AI-driven job matching for Northern Virginia's workforce.
            </p>

            <div className="space-y-4">
              {benefits.map((benefit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  className="flex items-start gap-3"
                >
                  <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                  <span className="text-white/90">{benefit}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right Side - Form */}
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
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Create your account</h1>
            <p className="mt-2 text-slate-600 dark:text-slate-400">
              Join FFX NOVA and find your perfect career match
            </p>
          </div>

          <RegisterForm onSuccess={() => navigate('/dashboard')} />

          <p className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
            Already have an account?{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 dark:text-primary-400 hover:underline"
            >
              Sign in
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
}
