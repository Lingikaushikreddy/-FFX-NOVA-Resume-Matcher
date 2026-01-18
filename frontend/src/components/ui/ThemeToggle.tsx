/**
 * Theme Toggle Component
 */

import { Moon, Sun, Monitor } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { motion } from 'framer-motion';

interface ThemeToggleProps {
  variant?: 'icon' | 'full';
  className?: string;
}

export function ThemeToggle({ variant = 'icon', className }: ThemeToggleProps) {
  const { theme, resolvedTheme, setTheme, toggleTheme } = useTheme();

  if (variant === 'icon') {
    return (
      <button
        onClick={toggleTheme}
        className={`p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors ${className}`}
        aria-label={`Switch to ${resolvedTheme === 'light' ? 'dark' : 'light'} mode`}
      >
        <motion.div
          key={resolvedTheme}
          initial={{ rotate: -90, opacity: 0 }}
          animate={{ rotate: 0, opacity: 1 }}
          transition={{ duration: 0.2 }}
        >
          {resolvedTheme === 'light' ? (
            <Sun className="w-5 h-5" />
          ) : (
            <Moon className="w-5 h-5" />
          )}
        </motion.div>
      </button>
    );
  }

  const options = [
    { value: 'light', icon: Sun, label: 'Light' },
    { value: 'dark', icon: Moon, label: 'Dark' },
    { value: 'system', icon: Monitor, label: 'System' },
  ] as const;

  return (
    <div className={`inline-flex rounded-lg bg-slate-100 dark:bg-slate-800 p-1 ${className}`}>
      {options.map(({ value, icon: Icon, label }) => (
        <button
          key={value}
          onClick={() => setTheme(value)}
          className={`relative px-3 py-1.5 rounded-md text-sm font-medium transition-colors flex items-center gap-1.5 ${
            theme === value
              ? 'text-slate-900 dark:text-white'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          }`}
        >
          {theme === value && (
            <motion.div
              layoutId="theme-toggle-bg"
              className="absolute inset-0 bg-white dark:bg-slate-700 rounded-md shadow-sm"
              transition={{ type: 'spring', duration: 0.3 }}
            />
          )}
          <span className="relative z-10 flex items-center gap-1.5">
            <Icon className="w-4 h-4" />
            {label}
          </span>
        </button>
      ))}
    </div>
  );
}
