/**
 * Match Score Chart
 */

import { useMemo } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';

interface MatchChartProps {
  variant?: 'area' | 'bar';
  title?: string;
  data?: { date: string; score: number; matches?: number }[];
}

const defaultData = [
  { date: 'Mon', score: 72, matches: 8 },
  { date: 'Tue', score: 75, matches: 12 },
  { date: 'Wed', score: 78, matches: 15 },
  { date: 'Thu', score: 74, matches: 10 },
  { date: 'Fri', score: 82, matches: 18 },
  { date: 'Sat', score: 79, matches: 6 },
  { date: 'Sun', score: 85, matches: 5 },
];

export function MatchChart({
  variant = 'area',
  title = 'Match Score Trend',
  data = defaultData,
}: MatchChartProps) {
  const chartColors = useMemo(() => ({
    primary: 'hsl(217, 91%, 60%)',
    primaryLight: 'hsl(217, 91%, 95%)',
    secondary: 'hsl(280, 87%, 63%)',
  }), []);

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            {variant === 'area' ? (
              <AreaChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={chartColors.primary} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={chartColors.primary} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
                <XAxis
                  dataKey="date"
                  tick={{ fill: 'currentColor', fontSize: 12 }}
                  className="text-slate-500"
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  domain={[0, 100]}
                  tick={{ fill: 'currentColor', fontSize: 12 }}
                  className="text-slate-500"
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--tooltip-bg, white)',
                    border: '1px solid var(--tooltip-border, #e2e8f0)',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                  }}
                  labelStyle={{ fontWeight: 600 }}
                />
                <Area
                  type="monotone"
                  dataKey="score"
                  stroke={chartColors.primary}
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorScore)"
                  name="FFX Score"
                />
              </AreaChart>
            ) : (
              <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
                <XAxis
                  dataKey="date"
                  tick={{ fill: 'currentColor', fontSize: 12 }}
                  className="text-slate-500"
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  tick={{ fill: 'currentColor', fontSize: 12 }}
                  className="text-slate-500"
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--tooltip-bg, white)',
                    border: '1px solid var(--tooltip-border, #e2e8f0)',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="matches" fill={chartColors.primary} radius={[4, 4, 0, 0]} name="Matches" />
              </BarChart>
            )}
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
