/**
 * Saved Jobs Component
 */

import { motion } from 'framer-motion';
import { Bookmark, MapPin, Building2, ExternalLink, Trash2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';

interface SavedJob {
  id: string;
  title: string;
  company: string;
  location: string;
  matchScore: number;
  savedAt: string;
  applied: boolean;
}

interface SavedJobsProps {
  jobs?: SavedJob[];
  onRemove?: (id: string) => void;
  onApply?: (id: string) => void;
}

const defaultJobs: SavedJob[] = [
  {
    id: '1',
    title: 'Senior Python Developer',
    company: 'Federal Contractor Inc',
    location: 'Fairfax, VA',
    matchScore: 92,
    savedAt: '2 days ago',
    applied: false,
  },
  {
    id: '2',
    title: 'DevOps Engineer',
    company: 'Defense Systems LLC',
    location: 'Arlington, VA',
    matchScore: 85,
    savedAt: '5 days ago',
    applied: true,
  },
  {
    id: '3',
    title: 'Cloud Solutions Architect',
    company: 'AWS GovCloud',
    location: 'Reston, VA',
    matchScore: 78,
    savedAt: '1 week ago',
    applied: false,
  },
];

function getScoreColor(score: number): string {
  if (score >= 85) return 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/30';
  if (score >= 70) return 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30';
  if (score >= 55) return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/30';
  return 'text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/30';
}

export function SavedJobs({ jobs = defaultJobs, onRemove, onApply }: SavedJobsProps) {
  return (
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <Bookmark className="w-5 h-5" />
          Saved Jobs
        </CardTitle>
        <Button variant="ghost" size="sm">
          View All
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {jobs.map((job, index) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="p-3 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-primary-300 dark:hover:border-primary-600 transition-colors"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <h4 className="font-medium text-slate-900 dark:text-white truncate">
                    {job.title}
                  </h4>
                  <div className="flex items-center gap-3 mt-1 text-sm text-slate-600 dark:text-slate-400">
                    <span className="flex items-center gap-1">
                      <Building2 className="w-3.5 h-3.5" />
                      {job.company}
                    </span>
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5" />
                      {job.location}
                    </span>
                  </div>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreColor(job.matchScore)}`}>
                  {job.matchScore}%
                </div>
              </div>
              <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 dark:border-slate-700">
                <span className="text-xs text-slate-500">Saved {job.savedAt}</span>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onRemove?.(job.id)}
                    className="p-1.5 text-slate-400 hover:text-red-500 transition-colors"
                    title="Remove"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  {job.applied ? (
                    <span className="text-xs text-green-600 dark:text-green-400 font-medium">
                      Applied
                    </span>
                  ) : (
                    <button
                      onClick={() => onApply?.(job.id)}
                      className="flex items-center gap-1 text-xs text-primary-600 dark:text-primary-400 hover:underline"
                    >
                      Apply <ExternalLink className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
