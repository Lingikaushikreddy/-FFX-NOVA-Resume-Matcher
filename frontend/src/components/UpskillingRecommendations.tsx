/**
 * Upskilling Recommendations - FFX NOVA
 * Beautiful learning path suggestions with course cards and progress tracking
 */

import { motion } from 'framer-motion';
import {
  BookOpen,
  PlayCircle,
  Clock,
  Star,
  TrendingUp,
  ExternalLink,
  ChevronRight,
  Zap,
  Target,
  GraduationCap,
  Sparkles,
  Users,
  BarChart,
} from 'lucide-react';

interface Course {
  id: string;
  title: string;
  provider: string;
  providerLogo?: string;
  duration: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  rating: number;
  enrollments: string;
  skill: string;
  url?: string;
  isFree?: boolean;
}

interface SkillGap {
  skill: string;
  currentLevel: number;
  requiredLevel: number;
  importance: 'High' | 'Medium' | 'Low';
  courses: Course[];
}

interface UpskillingRecommendationsProps {
  missingSkills: string[];
  skillGaps?: SkillGap[];
  className?: string;
}

// Mock course data
const mockCourses: Record<string, Course[]> = {
  Kubernetes: [
    {
      id: '1',
      title: 'Kubernetes for Developers',
      provider: 'Coursera',
      duration: '40 hours',
      level: 'Intermediate',
      rating: 4.8,
      enrollments: '125k+',
      skill: 'Kubernetes',
      isFree: false,
    },
    {
      id: '2',
      title: 'Kubernetes Fundamentals (LFS258)',
      provider: 'Linux Foundation',
      duration: '35 hours',
      level: 'Intermediate',
      rating: 4.7,
      enrollments: '80k+',
      skill: 'Kubernetes',
      isFree: false,
    },
  ],
  'Machine Learning': [
    {
      id: '3',
      title: 'Machine Learning Specialization',
      provider: 'Stanford Online',
      duration: '60 hours',
      level: 'Intermediate',
      rating: 4.9,
      enrollments: '500k+',
      skill: 'Machine Learning',
      isFree: false,
    },
    {
      id: '4',
      title: 'Intro to Machine Learning with Python',
      provider: 'Udacity',
      duration: '30 hours',
      level: 'Beginner',
      rating: 4.6,
      enrollments: '200k+',
      skill: 'Machine Learning',
      isFree: true,
    },
  ],
  Terraform: [
    {
      id: '5',
      title: 'HashiCorp Terraform Associate',
      provider: 'HashiCorp',
      duration: '20 hours',
      level: 'Intermediate',
      rating: 4.7,
      enrollments: '50k+',
      skill: 'Terraform',
      isFree: true,
    },
  ],
  Go: [
    {
      id: '6',
      title: 'Go: The Complete Developer\'s Guide',
      provider: 'Udemy',
      duration: '25 hours',
      level: 'Beginner',
      rating: 4.8,
      enrollments: '150k+',
      skill: 'Go',
      isFree: false,
    },
  ],
};

const defaultCourse: Course = {
  id: 'default',
  title: 'Professional Development Course',
  provider: 'LinkedIn Learning',
  duration: '15 hours',
  level: 'Intermediate',
  rating: 4.5,
  enrollments: '10k+',
  skill: '',
  isFree: false,
};

function getLevelColor(level: Course['level']) {
  switch (level) {
    case 'Beginner':
      return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400';
    case 'Intermediate':
      return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400';
    case 'Advanced':
      return 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400';
  }
}

function getImportanceColor(importance: SkillGap['importance']) {
  switch (importance) {
    case 'High':
      return 'from-red-500 to-orange-500';
    case 'Medium':
      return 'from-yellow-500 to-amber-500';
    case 'Low':
      return 'from-green-500 to-emerald-500';
  }
}

function CourseCard({ course, index }: { course: Course; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="group relative bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 overflow-hidden hover:shadow-xl transition-all duration-300"
    >
      {/* Free Badge */}
      {course.isFree && (
        <div className="absolute top-4 right-4 px-2.5 py-1 bg-green-500 text-white text-xs font-bold rounded-full">
          FREE
        </div>
      )}

      <div className="p-5">
        {/* Skill Tag */}
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-xs font-semibold rounded-lg mb-3">
          <Target className="w-3 h-3" />
          {course.skill}
        </div>

        {/* Title */}
        <h4 className="font-bold text-slate-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors line-clamp-2">
          {course.title}
        </h4>

        {/* Provider */}
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">{course.provider}</p>

        {/* Stats */}
        <div className="flex flex-wrap items-center gap-3 text-sm text-slate-500 dark:text-slate-400 mb-4">
          <div className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" />
            {course.duration}
          </div>
          <div className="flex items-center gap-1">
            <Star className="w-3.5 h-3.5 text-yellow-500 fill-yellow-500" />
            {course.rating}
          </div>
          <div className="flex items-center gap-1">
            <Users className="w-3.5 h-3.5" />
            {course.enrollments}
          </div>
        </div>

        {/* Level & CTA */}
        <div className="flex items-center justify-between">
          <span className={`px-2.5 py-1 rounded-lg text-xs font-medium ${getLevelColor(course.level)}`}>
            {course.level}
          </span>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-primary-500 hover:bg-primary-600 text-white text-sm font-medium rounded-lg transition-colors"
          >
            <PlayCircle className="w-4 h-4" />
            Start
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}

function SkillGapCard({ gap, index }: { gap: SkillGap; index: number }) {


  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-5"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h4 className="font-bold text-slate-900 dark:text-white mb-1">{gap.skill}</h4>
          <div className="flex items-center gap-2">
            <span className={`px-2 py-0.5 rounded text-xs font-medium bg-gradient-to-r ${getImportanceColor(gap.importance)} text-white`}>
              {gap.importance} Priority
            </span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-slate-900 dark:text-white">
            {gap.currentLevel}<span className="text-slate-400 text-lg">/{gap.requiredLevel}</span>
          </div>
          <div className="text-xs text-slate-500">Skill Level</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${(gap.currentLevel / gap.requiredLevel) * 100}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
            className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
          />
        </div>
        <div className="flex justify-between mt-1 text-xs text-slate-500">
          <span>Current</span>
          <span>{Math.round((gap.currentLevel / gap.requiredLevel) * 100)}% Complete</span>
        </div>
      </div>

      {/* Recommended Courses */}
      {gap.courses.length > 0 && (
        <div>
          <div className="text-xs font-medium text-slate-500 mb-2">Recommended Course:</div>
          <a
            href={gap.courses[0].url || '#'}
            className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-900/50 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                <BookOpen className="w-4 h-4 text-primary-600 dark:text-primary-400" />
              </div>
              <div>
                <div className="text-sm font-medium text-slate-900 dark:text-white line-clamp-1">
                  {gap.courses[0].title}
                </div>
                <div className="text-xs text-slate-500">{gap.courses[0].provider}</div>
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400" />
          </a>
        </div>
      )}
    </motion.div>
  );
}

export function UpskillingRecommendations({
  missingSkills,
  skillGaps,
  className = '',
}: UpskillingRecommendationsProps) {
  // Generate courses for missing skills
  const allCourses: Course[] = missingSkills.flatMap((skill) => {
    const courses = mockCourses[skill];
    if (courses) return courses;
    return [{ ...defaultCourse, id: skill, skill, title: `Master ${skill}` }];
  });

  // Generate skill gaps if not provided
  const gaps: SkillGap[] = skillGaps || missingSkills.map((skill, i) => ({
    skill,
    currentLevel: Math.floor(Math.random() * 3) + 1,
    requiredLevel: 5,
    importance: i === 0 ? 'High' : i === 1 ? 'Medium' : 'Low',
    courses: mockCourses[skill] || [{ ...defaultCourse, skill }],
  }));

  return (
    <div className={className}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-primary-500/10 to-secondary-500/10 border border-primary-200 dark:border-primary-800 mb-4">
          <Sparkles className="w-4 h-4 text-primary-500" />
          <span className="text-sm font-semibold text-primary-600 dark:text-primary-400">
            Personalized Learning Path
          </span>
        </div>
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
          Bridge Your Skill Gaps
        </h2>
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          Based on your resume analysis, here are personalized recommendations to boost your match score.
        </p>
      </motion.div>

      {/* Stats Banner */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12"
      >
        {[
          { icon: Target, label: 'Skills to Develop', value: missingSkills.length, color: 'from-orange-500 to-amber-500' },
          { icon: BookOpen, label: 'Recommended Courses', value: allCourses.length, color: 'from-primary-500 to-secondary-500' },
          { icon: TrendingUp, label: 'Potential Score Boost', value: '+15%', color: 'from-green-500 to-emerald-500' },
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + i * 0.1 }}
            className="relative overflow-hidden bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6"
          >
            <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${stat.color} opacity-10 blur-2xl`} />
            <div className="relative flex items-center gap-4">
              <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.color}`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="text-2xl font-bold text-slate-900 dark:text-white">{stat.value}</div>
                <div className="text-sm text-slate-500 dark:text-slate-400">{stat.label}</div>
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Skill Gaps Section */}
      {gaps.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-12"
        >
          <div className="flex items-center gap-2 mb-6">
            <BarChart className="w-5 h-5 text-primary-500" />
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">Skill Gap Analysis</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {gaps.map((gap, i) => (
              <SkillGapCard key={gap.skill} gap={gap} index={i} />
            ))}
          </div>
        </motion.div>
      )}

      {/* Recommended Courses */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-primary-500" />
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">Recommended Courses</h3>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2 text-sm text-primary-600 dark:text-primary-400 hover:underline"
          >
            View all courses
            <ExternalLink className="w-4 h-4" />
          </motion.button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {allCourses.slice(0, 8).map((course, i) => (
            <CourseCard key={course.id} course={course} index={i} />
          ))}
        </div>
      </motion.div>

      {/* CTA Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="mt-12 text-center"
      >
        <div className="inline-flex flex-col sm:flex-row gap-4 items-center justify-center p-8 bg-gradient-to-br from-primary-500/10 via-secondary-500/10 to-accent-500/10 rounded-3xl border border-primary-200 dark:border-primary-800">
          <div className="text-left">
            <h4 className="text-lg font-bold text-slate-900 dark:text-white mb-1">
              Ready to boost your career?
            </h4>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Create a free account to track your learning progress
            </p>
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold rounded-xl shadow-lg shadow-primary-500/25"
          >
            <Zap className="w-5 h-5" />
            Get Started Free
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
