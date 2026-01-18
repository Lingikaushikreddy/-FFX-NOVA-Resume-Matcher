/**
 * Dashboard Page
 */

import { motion } from 'framer-motion';
import { Plus, Upload } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sidebar } from '../components/layout/Sidebar';
import { Button } from '../components/ui/Button';
import { StatsCards } from '../components/dashboard/StatsCards';
import { MatchChart } from '../components/dashboard/MatchChart';
import { RecentActivity } from '../components/dashboard/RecentActivity';
import { SavedJobs } from '../components/dashboard/SavedJobs';

export function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />

      <main className="pl-64 pt-16">
        <div className="p-8">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8"
          >
            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                Welcome back, {user?.first_name || 'there'}!
              </h1>
              <p className="text-slate-600 dark:text-slate-400 mt-1">
                Here's what's happening with your job search
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link to="/resumes/upload">
                <Button variant="outline" leftIcon={<Upload className="w-4 h-4" />}>
                  Upload Resume
                </Button>
              </Link>
              <Link to="/matches">
                <Button leftIcon={<Plus className="w-4 h-4" />}>
                  Find Matches
                </Button>
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-8"
          >
            <StatsCards />
          </motion.div>

          {/* Charts and Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-2"
            >
              <MatchChart />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <RecentActivity />
            </motion.div>
          </div>

          {/* Saved Jobs and Quick Actions */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="lg:col-span-2"
            >
              <SavedJobs />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              {/* Quick Actions Card */}
              <div className="bg-gradient-to-br from-primary-600 to-secondary-600 rounded-xl p-6 text-white">
                <h3 className="text-lg font-semibold mb-2">Optimize Your Profile</h3>
                <p className="text-sm text-white/80 mb-4">
                  Complete your profile to get better job matches tailored to your skills and experience.
                </p>
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span>Profile Completion</span>
                    <span className="font-semibold">75%</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-white rounded-full h-2 w-3/4" />
                  </div>
                </div>
                <Link to="/profile">
                  <Button
                    variant="outline"
                    className="w-full mt-4 border-white/50 text-white hover:bg-white/10"
                  >
                    Complete Profile
                  </Button>
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  );
}
