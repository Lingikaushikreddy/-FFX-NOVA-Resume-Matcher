/**
 * Upload Page - FFX NOVA
 * Resume upload experience with beautiful UI
 */

import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { FileUploadZone } from '../components/FileUploadZone';
import { Shield, Target, Zap, Award, ChevronLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export function UploadPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-900">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-primary-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-secondary-500/5 rounded-full blur-3xl" />
      </div>

      <div className="relative container mx-auto px-4 py-12">
        {/* Back Button */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-8"
        >
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
            Back to Home
          </Link>
        </motion.div>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 mb-6"
          >
            <Zap className="w-4 h-4" />
            <span className="text-sm font-semibold">AI-Powered Analysis</span>
          </motion.div>
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4">
            Upload Your Resume
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Our AI will analyze your skills, experience, and qualifications to find your
            perfect job matches in the Northern Virginia federal market.
          </p>
        </motion.div>

        {/* Upload Zone */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <FileUploadZone onMatchesComplete={() => navigate('/matches')} />
        </motion.div>

        {/* Trust Indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-16 pt-12 border-t border-slate-200 dark:border-slate-800"
        >
          <div className="text-center mb-8">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
              Trusted by Federal Professionals
            </h3>
            <p className="text-slate-600 dark:text-slate-400">
              Your data is secure and never shared without your consent
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {[
              { icon: Shield, title: 'Secure', desc: 'AES-256 encrypted' },
              { icon: Target, title: 'Accurate', desc: '95% match precision' },
              { icon: Zap, title: 'Fast', desc: 'Results in seconds' },
              { icon: Award, title: 'Trusted', desc: '10,000+ users' },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + i * 0.1 }}
                className="text-center"
              >
                <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-gradient-to-br from-primary-500/10 to-secondary-500/10 flex items-center justify-center">
                  <item.icon className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                </div>
                <div className="font-semibold text-slate-900 dark:text-white">{item.title}</div>
                <div className="text-sm text-slate-500 dark:text-slate-400">{item.desc}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
