/**
 * Recent Activity Feed
 */

import { motion } from 'framer-motion';
import { Briefcase, FileText, Target, Star, Clock } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';

interface Activity {
  id: string;
  type: 'match' | 'upload' | 'save' | 'apply';
  title: string;
  description: string;
  timestamp: string;
}

interface RecentActivityProps {
  activities?: Activity[];
}

const defaultActivities: Activity[] = [
  {
    id: '1',
    type: 'match',
    title: 'New Excellent Match',
    description: 'Senior Python Developer at Federal Contractor Inc (92% match)',
    timestamp: '2 hours ago',
  },
  {
    id: '2',
    type: 'upload',
    title: 'Resume Uploaded',
    description: 'Resume_2024_v3.pdf processed successfully',
    timestamp: '5 hours ago',
  },
  {
    id: '3',
    type: 'save',
    title: 'Job Saved',
    description: 'DevOps Engineer at Defense Systems LLC',
    timestamp: '1 day ago',
  },
  {
    id: '4',
    type: 'apply',
    title: 'Application Submitted',
    description: 'Full Stack Developer at TechCorp Nova',
    timestamp: '2 days ago',
  },
  {
    id: '5',
    type: 'match',
    title: 'Strong Match Found',
    description: 'Cloud Engineer at AWS GovCloud (78% match)',
    timestamp: '3 days ago',
  },
];

const icons = {
  match: Target,
  upload: FileText,
  save: Star,
  apply: Briefcase,
};

const iconStyles = {
  match: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
  upload: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
  save: 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400',
  apply: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
};

export function RecentActivity({ activities = defaultActivities }: RecentActivityProps) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity, index) => {
            const Icon = icons[activity.type];
            return (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-start gap-3"
              >
                <div className={`p-2 rounded-lg ${iconStyles[activity.type]}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm text-slate-900 dark:text-white">
                    {activity.title}
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400 truncate">
                    {activity.description}
                  </p>
                </div>
                <div className="flex items-center gap-1 text-xs text-slate-500 dark:text-slate-500 flex-shrink-0">
                  <Clock className="w-3 h-3" />
                  {activity.timestamp}
                </div>
              </motion.div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
