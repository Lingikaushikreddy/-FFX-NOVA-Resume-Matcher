/**
 * Premium Job Match Card - FFX NOVA
 * Beautiful job card with score visualization, skill badges, and animations
 */

import { motion } from 'framer-motion';
import {
  Building2,
  MapPin,
  Shield,
  DollarSign,
  Bookmark,
  ExternalLink,
  Sparkles,
  Clock,
  Wifi,
  GraduationCap,
} from 'lucide-react';
import { ScoreGauge, ScoreBar } from './ScoreGauge';

export interface JobMatch {
  id: string;
  title: string;
  company: string;
  companyLogo?: string;
  location: string;
  salary: string;
  matchScore: number;
  semanticScore: number;
  skillScore: number;
  experienceScore: number;
  clearance: 'None' | 'Public Trust' | 'Secret' | 'Top Secret' | 'TS/SCI';
  matchedSkills: string[];
  missingSkills: string[];
  isRemote?: boolean;
  jobType?: 'federal' | 'military' | 'contractor' | 'private';
  postedAt?: string;
}

interface JobMatchCardProps {
  job: JobMatch;
  onClick?: () => void;
  onSave?: () => void;
  onApply?: () => void;
  index?: number;
  saved?: boolean;
}

function getClearanceStyle(clearance: JobMatch['clearance']) {
  switch (clearance) {
    case 'TS/SCI':
      return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800';
    case 'Top Secret':
      return 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800';
    case 'Secret':
      return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-800';
    case 'Public Trust':
      return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 border-purple-200 dark:border-purple-800';
    default:
      return 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700';
  }
}

function getJobTypeBadge(type?: JobMatch['jobType']) {
  switch (type) {
    case 'federal':
      return { label: 'Federal', class: 'bg-blue-500' };
    case 'military':
      return { label: 'Military', class: 'bg-green-600' };
    case 'contractor':
      return { label: 'Contractor', class: 'bg-purple-500' };
    case 'private':
      return { label: 'Private', class: 'bg-slate-500' };
    default:
      return null;
  }
}

export function JobMatchCard({ job, onClick, onSave, onApply, index = 0, saved = false }: JobMatchCardProps) {
  const jobTypeBadge = getJobTypeBadge(job.jobType);
  const isExcellent = job.matchScore >= 85;
  const isStrong = job.matchScore >= 70 && job.matchScore < 85;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.05 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="group relative bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-xl dark:hover:shadow-slate-900/50 transition-all duration-300 overflow-hidden cursor-pointer"
      onClick={onClick}
    >
      {/* Top Gradient Banner for High Matches */}
      {isExcellent && (
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-green-400 via-emerald-500 to-green-400" />
      )}
      {isStrong && !isExcellent && (
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-400 via-primary-500 to-blue-400" />
      )}

      {/* Excellent Match Banner */}
      {isExcellent && (
        <motion.div
          initial={{ x: 100 }}
          animate={{ x: 0 }}
          className="absolute top-4 right-0 flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-xs font-bold rounded-l-full shadow-lg"
        >
          <Sparkles className="w-3.5 h-3.5" />
          EXCELLENT MATCH
        </motion.div>
      )}

      <div className="p-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left: Score Visual */}
          <div className="flex-shrink-0 flex items-center justify-center lg:border-r lg:border-slate-200 dark:lg:border-slate-700 lg:pr-6">
            <ScoreGauge score={job.matchScore} size="md" />
          </div>

          {/* Middle: Job Details */}
          <div className="flex-grow min-w-0 space-y-4">
            {/* Header */}
            <div>
              <div className="flex items-start gap-3">
                {/* Company Logo */}
                <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center overflow-hidden">
                  {job.companyLogo ? (
                    <img src={job.companyLogo} alt={job.company} className="w-full h-full object-cover" />
                  ) : (
                    <Building2 className="w-6 h-6 text-slate-400" />
                  )}
                </div>

                <div className="flex-grow min-w-0">
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors truncate">
                    {job.title}
                  </h3>
                  <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                    <span className="font-medium text-slate-700 dark:text-slate-300">{job.company}</span>
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5" />
                      {job.location}
                    </span>
                    {job.isRemote && (
                      <span className="flex items-center gap-1 text-green-600 dark:text-green-400">
                        <Wifi className="w-3.5 h-3.5" />
                        Remote
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Badges Row */}
            <div className="flex flex-wrap gap-2">
              {/* Job Type Badge */}
              {jobTypeBadge && (
                <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold text-white ${jobTypeBadge.class}`}>
                  {jobTypeBadge.label}
                </span>
              )}

              {/* Clearance Badge */}
              {job.clearance !== 'None' && (
                <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold border ${getClearanceStyle(job.clearance)}`}>
                  <Shield className="w-3 h-3" />
                  {job.clearance}
                </span>
              )}

              {/* Salary */}
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-semibold bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800">
                <DollarSign className="w-3 h-3" />
                {job.salary}
              </span>

              {/* Posted Time */}
              {job.postedAt && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-700">
                  <Clock className="w-3 h-3" />
                  {job.postedAt}
                </span>
              )}
            </div>

            {/* Skills */}
            <div className="space-y-2">
              {/* Matched Skills */}
              <div className="flex flex-wrap gap-1.5">
                {job.matchedSkills.slice(0, 5).map((skill, i) => (
                  <motion.span
                    key={skill}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3 + i * 0.03 }}
                    className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5" />
                    {skill}
                  </motion.span>
                ))}
                {job.matchedSkills.length > 5 && (
                  <span className="inline-flex items-center px-2.5 py-1 text-xs text-slate-500 dark:text-slate-400">
                    +{job.matchedSkills.length - 5} more
                  </span>
                )}
              </div>

              {/* Missing Skills */}
              {job.missingSkills.length > 0 && (
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400 dark:text-slate-500">Skill gaps:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {job.missingSkills.slice(0, 3).map((skill) => (
                      <span
                        key={skill}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 border border-orange-200 dark:border-orange-800"
                      >
                        {skill}
                        <GraduationCap className="w-3 h-3 ml-0.5" />
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right: Score Breakdown & Actions */}
          <div className="flex-shrink-0 lg:w-48 flex flex-col justify-between gap-4 lg:border-l lg:border-slate-200 dark:lg:border-slate-700 lg:pl-6">
            {/* Score Breakdown */}
            <div className="space-y-2">
              <ScoreBar score={job.semanticScore} label="Semantic" />
              <ScoreBar score={job.skillScore} label="Skills" />
              <ScoreBar score={job.experienceScore} label="Experience" />
            </div>

            {/* Actions */}
            <div className="flex gap-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={(e) => {
                  e.stopPropagation();
                  onSave?.();
                }}
                className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
                  saved
                    ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400'
                    : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600'
                }`}
              >
                <Bookmark className={`w-4 h-4 ${saved ? 'fill-current' : ''}`} />
                {saved ? 'Saved' : 'Save'}
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={(e) => {
                  e.stopPropagation();
                  onApply?.();
                }}
                className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-primary-500 to-secondary-500 text-white hover:from-primary-600 hover:to-secondary-600 transition-all"
              >
                Apply
                <ExternalLink className="w-3.5 h-3.5" />
              </motion.button>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

/**
 * Compact version for sidebar or list view
 */
export function JobMatchCardCompact({ job, onClick }: { job: JobMatch; onClick?: () => void }) {
  return (
    <motion.div
      whileHover={{ x: 4 }}
      onClick={onClick}
      className="flex items-center gap-4 p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:border-primary-300 dark:hover:border-primary-600 cursor-pointer transition-colors"
    >
      <ScoreGauge score={job.matchScore} size="sm" showLabel={false} />
      <div className="flex-grow min-w-0">
        <h4 className="font-semibold text-slate-900 dark:text-white truncate">{job.title}</h4>
        <p className="text-sm text-slate-500 dark:text-slate-400 truncate">{job.company}</p>
      </div>
      <div className="text-right">
        <div className="text-lg font-bold text-primary-600 dark:text-primary-400">{job.matchScore}%</div>
        <div className="text-xs text-slate-500">{job.location}</div>
      </div>
    </motion.div>
  );
}
