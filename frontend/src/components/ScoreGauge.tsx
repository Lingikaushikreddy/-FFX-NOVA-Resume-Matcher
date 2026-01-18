/**
 * Premium Score Gauge - Animated circular progress indicator
 */

import { motion } from 'framer-motion';

/**
 * ScoreGauge Component
 * 
 * Displays a circular progress gauge for match scores.
 * Visualizes the score with a color-coded ring and percentage text.
 */
interface ScoreGaugeProps {
  score: number;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  animated?: boolean;
}

const sizeConfig = {
  sm: { width: 64, stroke: 6, fontSize: 'text-sm', labelSize: 'text-xs' },
  md: { width: 96, stroke: 8, fontSize: 'text-xl', labelSize: 'text-xs' },
  lg: { width: 128, stroke: 10, fontSize: 'text-3xl', labelSize: 'text-sm' },
};

function getScoreColor(score: number): { stroke: string; bg: string; text: string; gradient: string } {
  if (score >= 85) return {
    stroke: 'stroke-green-500',
    bg: 'bg-green-100 dark:bg-green-900/30',
    text: 'text-green-600 dark:text-green-400',
    gradient: 'from-green-400 to-emerald-500'
  };
  if (score >= 70) return {
    stroke: 'stroke-blue-500',
    bg: 'bg-blue-100 dark:bg-blue-900/30',
    text: 'text-blue-600 dark:text-blue-400',
    gradient: 'from-blue-400 to-primary-500'
  };
  if (score >= 55) return {
    stroke: 'stroke-yellow-500',
    bg: 'bg-yellow-100 dark:bg-yellow-900/30',
    text: 'text-yellow-600 dark:text-yellow-400',
    gradient: 'from-yellow-400 to-orange-500'
  };
  return {
    stroke: 'stroke-orange-500',
    bg: 'bg-orange-100 dark:bg-orange-900/30',
    text: 'text-orange-600 dark:text-orange-400',
    gradient: 'from-orange-400 to-red-500'
  };
}

function getTierLabel(score: number): string {
  if (score >= 85) return 'Excellent Match';
  if (score >= 70) return 'Strong Match';
  if (score >= 55) return 'Good Match';
  if (score >= 40) return 'Fair Match';
  return 'Weak Match';
}

export function ScoreGauge({ score, label, size = 'md', showLabel = true, animated = true }: ScoreGaugeProps) {
  const { width, stroke, fontSize, labelSize } = sizeConfig[size];
  const radius = (width - stroke) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (score / 100) * circumference;
  const colors = getScoreColor(score);
  const displayLabel = label || getTierLabel(score);

  return (
    <div className="relative inline-flex flex-col items-center">
      <div className="relative" style={{ width, height: width }}>
        {/* Glow Effect */}
        <div
          className={`absolute inset-0 rounded-full bg-gradient-to-br ${colors.gradient} opacity-20 blur-xl`}
          style={{ transform: 'scale(0.8)' }}
        />

        {/* Background Circle */}
        <svg
          className="transform -rotate-90 relative z-10"
          width={width}
          height={width}
        >
          <circle
            className="stroke-slate-200 dark:stroke-slate-700"
            strokeWidth={stroke}
            fill="none"
            r={radius}
            cx={width / 2}
            cy={width / 2}
          />
          {/* Progress Circle with gradient */}
          <defs>
            <linearGradient id={`scoreGradient-${score}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" className={colors.gradient.includes('green') ? 'stop-green-400' : colors.gradient.includes('blue') ? 'stop-blue-400' : colors.gradient.includes('yellow') ? 'stop-yellow-400' : 'stop-orange-400'} style={{ stopColor: score >= 85 ? '#4ade80' : score >= 70 ? '#60a5fa' : score >= 55 ? '#facc15' : '#fb923c' }} />
              <stop offset="100%" className={colors.gradient.includes('green') ? 'stop-emerald-500' : colors.gradient.includes('blue') ? 'stop-primary-500' : colors.gradient.includes('yellow') ? 'stop-orange-500' : 'stop-red-500'} style={{ stopColor: score >= 85 ? '#10b981' : score >= 70 ? '#3b82f6' : score >= 55 ? '#f97316' : '#ef4444' }} />
            </linearGradient>
          </defs>
          <motion.circle
            stroke={`url(#scoreGradient-${score})`}
            strokeWidth={stroke}
            strokeLinecap="round"
            fill="none"
            r={radius}
            cx={width / 2}
            cy={width / 2}
            initial={animated ? { strokeDashoffset: circumference } : { strokeDashoffset: offset }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: 'easeOut', delay: 0.2 }}
            style={{ strokeDasharray: circumference }}
          />
        </svg>

        {/* Score Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center z-20">
          <motion.span
            className={`font-bold ${fontSize} text-slate-900 dark:text-white`}
            initial={animated ? { opacity: 0, scale: 0.5 } : {}}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, delay: 0.6 }}
          >
            {score}
          </motion.span>
          <motion.span
            initial={animated ? { opacity: 0 } : {}}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-xs text-slate-500 dark:text-slate-400 -mt-1"
          >
            /100
          </motion.span>
        </div>
      </div>

      {showLabel && (
        <motion.span
          initial={animated ? { opacity: 0, y: 5 } : {}}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className={`mt-2 ${labelSize} font-semibold uppercase tracking-wide ${colors.text}`}
        >
          {displayLabel}
        </motion.span>
      )}
    </div>
  );
}

/**
 * Linear Score Bar - Alternative visualization
 */
export function ScoreBar({ score, label, className }: { score: number; label?: string; className?: string }) {
  const colors = getScoreColor(score);

  return (
    <div className={className}>
      {label && (
        <div className="flex justify-between items-center mb-1.5">
          <span className="text-sm text-slate-600 dark:text-slate-400">{label}</span>
          <span className={`text-sm font-bold ${colors.text}`}>{score}%</span>
        </div>
      )}
      <div className="h-2.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-full rounded-full bg-gradient-to-r ${colors.gradient}`}
        />
      </div>
    </div>
  );
}

/**
 * Mini Score Badge - Compact score display
 */
export function ScoreBadge({ score, className }: { score: number; className?: string }) {
  const colors = getScoreColor(score);

  return (
    <div className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full ${colors.bg} ${className}`}>
      <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${colors.gradient}`} />
      <span className={`text-sm font-bold ${colors.text}`}>{score}%</span>
    </div>
  );
}
