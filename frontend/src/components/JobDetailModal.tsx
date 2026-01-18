/**
 * Premium Job Detail Modal - FFX NOVA
 * Full-screen modal with comprehensive job details, skill breakdown, and apply actions
 */

import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Building2,
  MapPin,
  DollarSign,
  Shield,
  Clock,
  Wifi,
  ExternalLink,
  Bookmark,
  Share2,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  GraduationCap,
  Briefcase,
  Users,
  Calendar,
  Globe,
  ChevronRight,
  Sparkles,
  Target,
  Award,
  BookOpen,
} from 'lucide-react';
import { ScoreGauge, ScoreBar } from './ScoreGauge';
import type { JobMatch } from './JobMatchCard';

interface JobDetailModalProps {
  job: JobMatch | null;
  isOpen: boolean;
  onClose: () => void;
  onSave?: () => void;
  onApply?: () => void;
  saved?: boolean;
}

// Extended job details for the modal
interface JobDetails extends JobMatch {
  description?: string;
  responsibilities?: string[];
  requirements?: string[];
  benefits?: string[];
  companyInfo?: {
    size: string;
    industry: string;
    founded: string;
    website?: string;
  };
  applicationDeadline?: string;
  hiringManager?: string;
}

const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
};

const modalVariants = {
  hidden: { opacity: 0, scale: 0.95, y: 20 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: { type: 'spring', stiffness: 300, damping: 30 },
  },
  exit: { opacity: 0, scale: 0.95, y: 20 },
};

function getClearanceColor(clearance: JobMatch['clearance']) {
  switch (clearance) {
    case 'TS/SCI':
      return 'from-red-500 to-red-600';
    case 'Top Secret':
      return 'from-amber-500 to-amber-600';
    case 'Secret':
      return 'from-blue-500 to-blue-600';
    case 'Public Trust':
      return 'from-purple-500 to-purple-600';
    default:
      return 'from-slate-400 to-slate-500';
  }
}

export function JobDetailModal({
  job,
  isOpen,
  onClose,
  onSave,
  onApply,
  saved = false,
}: JobDetailModalProps) {
  if (!job) return null;

  // Mock extended details for demonstration
  const details: JobDetails = {
    ...job,
    description:
      'Join our team of innovative engineers building next-generation solutions for federal clients. You will work on cutting-edge cloud infrastructure, implementing secure and scalable systems that support critical government missions.',
    responsibilities: [
      'Design and implement secure cloud architectures on AWS/Azure/GCP',
      'Lead technical discussions and code reviews with team members',
      'Collaborate with cross-functional teams to deliver mission-critical solutions',
      'Mentor junior engineers and promote best practices',
      'Participate in Agile ceremonies and contribute to sprint planning',
    ],
    requirements: [
      '5+ years of experience in software engineering',
      'Strong proficiency in Python, Java, or Go',
      'Experience with containerization (Docker, Kubernetes)',
      'Active Secret clearance or higher',
      'Bachelor\'s degree in Computer Science or related field',
    ],
    benefits: [
      'Competitive salary with annual bonuses',
      'Comprehensive health, dental, and vision insurance',
      '401(k) with 6% company match',
      'Unlimited PTO policy',
      'Professional development budget',
      'Remote work flexibility',
    ],
    companyInfo: {
      size: '500-1000 employees',
      industry: 'Defense & Government IT',
      founded: '2005',
      website: 'https://example.com',
    },
    applicationDeadline: 'Open until filled',
  };

  const isExcellent = job.matchScore >= 85;
  const isStrong = job.matchScore >= 70 && job.matchScore < 85;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial="hidden"
          animate="visible"
          exit="hidden"
          variants={overlayVariants}
          className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/50 backdrop-blur-sm p-4 md:p-8"
          onClick={onClose}
        >
          <motion.div
            variants={modalVariants}
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-5xl bg-white dark:bg-slate-900 rounded-3xl shadow-2xl overflow-hidden my-8"
          >
            {/* Close Button */}
            <motion.button
              whileHover={{ scale: 1.1, rotate: 90 }}
              whileTap={{ scale: 0.9 }}
              onClick={onClose}
              className="absolute top-6 right-6 z-20 p-2 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm rounded-full shadow-lg hover:bg-white dark:hover:bg-slate-700 transition-colors"
            >
              <X className="w-5 h-5 text-slate-600 dark:text-slate-300" />
            </motion.button>

            {/* Header Banner */}
            <div className={`relative h-48 md:h-56 bg-gradient-to-br ${isExcellent ? 'from-green-600 via-emerald-600 to-teal-600' : isStrong ? 'from-blue-600 via-primary-600 to-indigo-600' : 'from-slate-600 via-slate-700 to-slate-800'}`}>
              {/* Decorative Elements */}
              <div className="absolute inset-0 overflow-hidden">
                <div className="absolute -top-20 -right-20 w-64 h-64 bg-white/10 rounded-full blur-2xl" />
                <div className="absolute -bottom-10 -left-10 w-48 h-48 bg-white/10 rounded-full blur-2xl" />
                <div
                  className="absolute inset-0 opacity-10"
                  style={{
                    backgroundImage:
                      'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
                    backgroundSize: '32px 32px',
                  }}
                />
              </div>

              {/* Match Badge */}
              {isExcellent && (
                <motion.div
                  initial={{ x: 100, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="absolute top-6 left-6 flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full"
                >
                  <Sparkles className="w-4 h-4 text-yellow-300" />
                  <span className="text-sm font-bold text-white">EXCELLENT MATCH</span>
                </motion.div>
              )}

              {/* Score Gauge */}
              <div className="absolute -bottom-16 left-8 md:left-12">
                <div className="p-2 bg-white dark:bg-slate-800 rounded-2xl shadow-xl">
                  <ScoreGauge score={job.matchScore} size="lg" />
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="pt-24 pb-8 px-6 md:px-12">
              {/* Title & Company */}
              <div className="mb-8">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div>
                    <h2 className="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white mb-2">
                      {job.title}
                    </h2>
                    <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-slate-600 dark:text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <Building2 className="w-4 h-4" />
                        <span className="font-medium">{job.company}</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <MapPin className="w-4 h-4" />
                        <span>{job.location}</span>
                      </div>
                      {job.isRemote && (
                        <div className="flex items-center gap-1.5 text-green-600 dark:text-green-400">
                          <Wifi className="w-4 h-4" />
                          <span>Remote</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center gap-3">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={onSave}
                      className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-colors ${
                        saved
                          ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                      }`}
                    >
                      <Bookmark className={`w-4 h-4 ${saved ? 'fill-current' : ''}`} />
                      {saved ? 'Saved' : 'Save'}
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 font-medium transition-colors"
                    >
                      <Share2 className="w-4 h-4" />
                      Share
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={onApply}
                      className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30 transition-shadow"
                    >
                      Apply Now
                      <ExternalLink className="w-4 h-4" />
                    </motion.button>
                  </div>
                </div>

                {/* Badges Row */}
                <div className="flex flex-wrap gap-2 mt-4">
                  {job.clearance !== 'None' && (
                    <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-semibold text-white bg-gradient-to-r ${getClearanceColor(job.clearance)}`}>
                      <Shield className="w-4 h-4" />
                      {job.clearance} Clearance
                    </span>
                  )}
                  <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-semibold bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
                    <DollarSign className="w-4 h-4" />
                    {job.salary}
                  </span>
                  {job.postedAt && (
                    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                      <Clock className="w-4 h-4" />
                      Posted {job.postedAt}
                    </span>
                  )}
                </div>
              </div>

              {/* Two Column Layout */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Content */}
                <div className="lg:col-span-2 space-y-8">
                  {/* Match Analysis */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-800/50 rounded-2xl p-6"
                  >
                    <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 dark:text-white mb-4">
                      <Target className="w-5 h-5 text-primary-500" />
                      Match Analysis
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                      <ScoreBar score={job.semanticScore} label="Semantic Match" />
                      <ScoreBar score={job.skillScore} label="Skills Match" />
                      <ScoreBar score={job.experienceScore} label="Experience" />
                    </div>

                    {/* Skills */}
                    <div className="space-y-4">
                      <div>
                        <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                          <CheckCircle className="w-4 h-4 text-green-500" />
                          Matching Skills ({job.matchedSkills.length})
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {job.matchedSkills.map((skill) => (
                            <motion.span
                              key={skill}
                              initial={{ opacity: 0, scale: 0.8 }}
                              animate={{ opacity: 1, scale: 1 }}
                              className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800"
                            >
                              <CheckCircle className="w-3.5 h-3.5 mr-1.5" />
                              {skill}
                            </motion.span>
                          ))}
                        </div>
                      </div>

                      {job.missingSkills.length > 0 && (
                        <div>
                          <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                            <AlertCircle className="w-4 h-4 text-orange-500" />
                            Skills to Develop ({job.missingSkills.length})
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {job.missingSkills.map((skill) => (
                              <motion.span
                                key={skill}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 border border-orange-200 dark:border-orange-800"
                              >
                                <GraduationCap className="w-3.5 h-3.5 mr-1.5" />
                                {skill}
                              </motion.span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </motion.div>

                  {/* Job Description */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                  >
                    <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 dark:text-white mb-4">
                      <Briefcase className="w-5 h-5 text-primary-500" />
                      About This Role
                    </h3>
                    <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                      {details.description}
                    </p>
                  </motion.div>

                  {/* Responsibilities */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                  >
                    <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 dark:text-white mb-4">
                      <TrendingUp className="w-5 h-5 text-primary-500" />
                      Responsibilities
                    </h3>
                    <ul className="space-y-2">
                      {details.responsibilities?.map((item, i) => (
                        <li key={i} className="flex items-start gap-3 text-slate-600 dark:text-slate-400">
                          <ChevronRight className="w-5 h-5 text-primary-500 flex-shrink-0 mt-0.5" />
                          {item}
                        </li>
                      ))}
                    </ul>
                  </motion.div>

                  {/* Requirements */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                  >
                    <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 dark:text-white mb-4">
                      <Award className="w-5 h-5 text-primary-500" />
                      Requirements
                    </h3>
                    <ul className="space-y-2">
                      {details.requirements?.map((item, i) => (
                        <li key={i} className="flex items-start gap-3 text-slate-600 dark:text-slate-400">
                          <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                          {item}
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                </div>

                {/* Sidebar */}
                <div className="space-y-6">
                  {/* Company Info */}
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                    className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6"
                  >
                    <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 dark:text-white mb-4">
                      <Building2 className="w-5 h-5 text-primary-500" />
                      About {job.company}
                    </h3>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <Users className="w-4 h-4 text-slate-400" />
                        <span className="text-sm text-slate-600 dark:text-slate-400">
                          {details.companyInfo?.size}
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <Briefcase className="w-4 h-4 text-slate-400" />
                        <span className="text-sm text-slate-600 dark:text-slate-400">
                          {details.companyInfo?.industry}
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <Calendar className="w-4 h-4 text-slate-400" />
                        <span className="text-sm text-slate-600 dark:text-slate-400">
                          Founded {details.companyInfo?.founded}
                        </span>
                      </div>
                      {details.companyInfo?.website && (
                        <a
                          href={details.companyInfo.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-3 text-primary-600 dark:text-primary-400 hover:underline"
                        >
                          <Globe className="w-4 h-4" />
                          <span className="text-sm">Company Website</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  </motion.div>

                  {/* Benefits */}
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 }}
                    className="bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-2xl border border-primary-200 dark:border-primary-800 p-6"
                  >
                    <h3 className="flex items-center gap-2 text-lg font-bold text-slate-900 dark:text-white mb-4">
                      <Sparkles className="w-5 h-5 text-primary-500" />
                      Benefits & Perks
                    </h3>
                    <ul className="space-y-2">
                      {details.benefits?.map((item, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-400">
                          <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                          {item}
                        </li>
                      ))}
                    </ul>
                  </motion.div>

                  {/* Upskilling CTA */}
                  {job.missingSkills.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.4 }}
                      className="bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl p-6 text-white"
                    >
                      <div className="flex items-center gap-2 mb-3">
                        <BookOpen className="w-5 h-5" />
                        <h3 className="font-bold">Bridge Your Skill Gaps</h3>
                      </div>
                      <p className="text-sm text-white/90 mb-4">
                        Get personalized learning recommendations to develop {job.missingSkills.length} missing skills.
                      </p>
                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full py-2.5 bg-white text-orange-600 font-semibold rounded-xl hover:bg-orange-50 transition-colors"
                      >
                        View Learning Path
                      </motion.button>
                    </motion.div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
