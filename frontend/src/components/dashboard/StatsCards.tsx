/**
 * Dashboard Stats Cards
 */

import { motion } from 'framer-motion';
import { Briefcase, FileText, TrendingUp, Target, ArrowUp, ArrowDown } from 'lucide-react';
import { Card } from '../ui/Card';

interface Stat {
  label: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: React.ComponentType<{ className?: string }>;
  color: 'primary' | 'secondary' | 'green' | 'purple';
}

interface StatsCardsProps {
  stats?: Stat[];
}

const defaultStats: Stat[] = [
  {
    label: 'Job Matches',
    value: 47,
    change: 12,
    changeLabel: 'from last week',
    icon: Briefcase,
    color: 'primary',
  },
  {
    label: 'Excellent Matches',
    value: 8,
    change: 3,
    changeLabel: 'new this week',
    icon: Target,
    color: 'green',
  },
  {
    label: 'Resumes Uploaded',
    value: 2,
    icon: FileText,
    color: 'secondary',
  },
  {
    label: 'Avg Match Score',
    value: '76%',
    change: 5,
    changeLabel: 'improvement',
    icon: TrendingUp,
    color: 'purple',
  },
];

const colorStyles = {
  primary: 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400',
  secondary: 'bg-secondary-100 dark:bg-secondary-900/30 text-secondary-600 dark:text-secondary-400',
  green: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
  purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
};

export function StatsCards({ stats = defaultStats }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <Card className="relative overflow-hidden">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400">
                  {stat.label}
                </p>
                <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">
                  {stat.value}
                </p>
                {stat.change !== undefined && (
                  <div className="mt-2 flex items-center gap-1 text-sm">
                    {stat.change > 0 ? (
                      <ArrowUp className="w-4 h-4 text-green-500" />
                    ) : (
                      <ArrowDown className="w-4 h-4 text-red-500" />
                    )}
                    <span className={stat.change > 0 ? 'text-green-600' : 'text-red-600'}>
                      {Math.abs(stat.change)}
                    </span>
                    {stat.changeLabel && (
                      <span className="text-slate-500 dark:text-slate-400">
                        {stat.changeLabel}
                      </span>
                    )}
                  </div>
                )}
              </div>
              <div className={`p-3 rounded-xl ${colorStyles[stat.color]}`}>
                <stat.icon className="w-6 h-6" />
              </div>
            </div>
          </Card>
        </motion.div>
      ))}
    </div>
  );
}
