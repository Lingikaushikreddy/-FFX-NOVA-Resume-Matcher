/**
 * Premium Job Results Page - FFX NOVA
 * Full-featured job matching results with filters, sorting, and detailed views
 */

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  SlidersHorizontal,
  Grid3X3,
  List,
  ChevronDown,
  Sparkles,
  TrendingUp,
  Target,
  Briefcase,
  X,
  ArrowUpDown,
} from 'lucide-react';
import { JobMatchCard, JobMatchCardCompact, type JobMatch } from './JobMatchCard';
import { FilterSidebar, MobileFilterButton, type FilterState } from './FilterSidebar';
import { JobDetailModal } from './JobDetailModal';
import { UpskillingRecommendations } from './UpskillingRecommendations';
import { ScoreBadge } from './ScoreGauge';

// Extended Mock Data
const MOCK_JOBS: JobMatch[] = [
  {
    id: '1',
    title: 'Senior Full Stack Engineer',
    company: 'Northrop Grumman',
    location: 'McLean, VA',
    salary: '$140k - $180k',
    matchScore: 92,
    semanticScore: 95,
    skillScore: 88,
    experienceScore: 93,
    clearance: 'Secret',
    matchedSkills: ['React', 'TypeScript', 'Node.js', 'AWS', 'Python', 'PostgreSQL'],
    missingSkills: ['Kubernetes'],
    isRemote: false,
    jobType: 'contractor',
    postedAt: '2 days ago',
  },
  {
    id: '2',
    title: 'Frontend Developer (AI Platform)',
    company: 'Booz Allen Hamilton',
    location: 'Arlington, VA',
    salary: '$120k - $150k',
    matchScore: 88,
    semanticScore: 85,
    skillScore: 92,
    experienceScore: 87,
    clearance: 'None',
    matchedSkills: ['React', 'CSS', 'Figma', 'JavaScript', 'TypeScript'],
    missingSkills: ['Three.js', 'WebGL'],
    isRemote: true,
    jobType: 'contractor',
    postedAt: '1 day ago',
  },
  {
    id: '3',
    title: 'Cloud Security Architect',
    company: 'Leidos',
    location: 'Reston, VA',
    salary: '$160k - $200k',
    matchScore: 78,
    semanticScore: 82,
    skillScore: 72,
    experienceScore: 80,
    clearance: 'Top Secret',
    matchedSkills: ['AWS', 'Security+', 'Python', 'Linux'],
    missingSkills: ['CISSP', 'Docker', 'Terraform'],
    isRemote: false,
    jobType: 'federal',
    postedAt: '3 days ago',
  },
  {
    id: '4',
    title: 'DevOps Engineer - CI/CD Specialist',
    company: 'SAIC',
    location: 'Tysons, VA',
    salary: '$130k - $165k',
    matchScore: 85,
    semanticScore: 88,
    skillScore: 82,
    experienceScore: 85,
    clearance: 'Secret',
    matchedSkills: ['Docker', 'Jenkins', 'AWS', 'Python', 'Git'],
    missingSkills: ['Kubernetes', 'Terraform'],
    isRemote: true,
    jobType: 'contractor',
    postedAt: '5 hours ago',
  },
  {
    id: '5',
    title: 'Machine Learning Engineer',
    company: 'Palantir',
    location: 'Washington, DC',
    salary: '$180k - $220k',
    matchScore: 72,
    semanticScore: 75,
    skillScore: 68,
    experienceScore: 73,
    clearance: 'TS/SCI',
    matchedSkills: ['Python', 'TensorFlow', 'SQL'],
    missingSkills: ['PyTorch', 'Spark', 'Kubernetes'],
    isRemote: false,
    jobType: 'private',
    postedAt: '1 week ago',
  },
  {
    id: '6',
    title: 'Software Engineer - Backend',
    company: 'General Dynamics IT',
    location: 'Fairfax, VA',
    salary: '$115k - $145k',
    matchScore: 82,
    semanticScore: 80,
    skillScore: 85,
    experienceScore: 81,
    clearance: 'Public Trust',
    matchedSkills: ['Java', 'Spring Boot', 'PostgreSQL', 'AWS'],
    missingSkills: ['Go'],
    isRemote: false,
    jobType: 'federal',
    postedAt: '4 days ago',
  },
  {
    id: '7',
    title: 'Cybersecurity Analyst',
    company: 'Raytheon',
    location: 'Alexandria, VA',
    salary: '$100k - $130k',
    matchScore: 68,
    semanticScore: 72,
    skillScore: 65,
    experienceScore: 67,
    clearance: 'Secret',
    matchedSkills: ['SIEM', 'Python', 'Network Security'],
    missingSkills: ['CISSP', 'Splunk', 'Incident Response'],
    isRemote: false,
    jobType: 'military',
    postedAt: '6 days ago',
  },
  {
    id: '8',
    title: 'Data Scientist - Defense Analytics',
    company: 'MITRE',
    location: 'McLean, VA',
    salary: '$140k - $175k',
    matchScore: 76,
    semanticScore: 78,
    skillScore: 74,
    experienceScore: 76,
    clearance: 'Top Secret',
    matchedSkills: ['Python', 'R', 'SQL', 'Machine Learning'],
    missingSkills: ['Spark', 'Hadoop'],
    isRemote: true,
    jobType: 'federal',
    postedAt: '2 days ago',
  },
];

type SortOption = 'match' | 'salary' | 'recent';
type ViewMode = 'cards' | 'list';

const defaultFilters: FilterState = {
  matchScore: [0, 100],
  clearance: [],
  jobType: [],
  location: [],
  salary: [50000, 250000],
  remote: null,
  experience: [],
};

export function JobResultsPage() {
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('match');
  const [viewMode, setViewMode] = useState<ViewMode>('cards');
  const [selectedJob, setSelectedJob] = useState<JobMatch | null>(null);
  const [savedJobs, setSavedJobs] = useState<Set<string>>(new Set());
  const [showMobileFilters, setShowMobileFilters] = useState(false);
  const [showUpskilling, setShowUpskilling] = useState(false);

  // Filter and sort jobs
  const filteredJobs = useMemo(() => {
    let jobs = MOCK_JOBS.filter((job) => {
      // Match score filter
      if (job.matchScore < filters.matchScore[0] || job.matchScore > filters.matchScore[1]) {
        return false;
      }
      // Clearance filter
      if (filters.clearance.length > 0 && !filters.clearance.includes(job.clearance)) {
        return false;
      }
      // Job type filter
      if (filters.jobType.length > 0 && job.jobType && !filters.jobType.includes(job.jobType)) {
        return false;
      }
      // Location filter
      if (filters.location.length > 0 && !filters.location.includes(job.location)) {
        return false;
      }
      // Remote filter
      if (filters.remote !== null && job.isRemote !== filters.remote) {
        return false;
      }
      // Search query
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        return (
          job.title.toLowerCase().includes(query) ||
          job.company.toLowerCase().includes(query) ||
          job.matchedSkills.some((s) => s.toLowerCase().includes(query))
        );
      }
      return true;
    });

    // Sort
    switch (sortBy) {
      case 'match':
        jobs.sort((a, b) => b.matchScore - a.matchScore);
        break;
      case 'salary':
        // Extract max salary for sorting
        const getSalary = (s: string) => parseInt(s.replace(/[^0-9]/g, '').slice(-3)) || 0;
        jobs.sort((a, b) => getSalary(b.salary) - getSalary(a.salary));
        break;
      case 'recent':
        // Simple sort by posted time (mock)
        jobs.sort((a, b) => {
          const getHours = (s?: string) => {
            if (!s) return 999;
            if (s.includes('hour')) return parseInt(s);
            if (s.includes('day')) return parseInt(s) * 24;
            if (s.includes('week')) return parseInt(s) * 168;
            return 999;
          };
          return getHours(a.postedAt) - getHours(b.postedAt);
        });
        break;
    }

    return jobs;
  }, [filters, searchQuery, sortBy]);

  const toggleSaveJob = (jobId: string) => {
    setSavedJobs((prev) => {
      const next = new Set(prev);
      if (next.has(jobId)) {
        next.delete(jobId);
      } else {
        next.add(jobId);
      }
      return next;
    });
  };

  const activeFilterCount = [
    filters.clearance.length > 0,
    filters.jobType.length > 0,
    filters.location.length > 0,
    filters.experience.length > 0,
    filters.remote !== null,
    filters.matchScore[0] > 0 || filters.matchScore[1] < 100,
  ].filter(Boolean).length;

  // Collect all missing skills
  const allMissingSkills = [...new Set(MOCK_JOBS.flatMap((j) => j.missingSkills))];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-900">
      {/* Hero Header */}
      <div className="relative bg-gradient-to-br from-slate-900 via-primary-900 to-secondary-900 pt-24 pb-16 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-secondary-500/20 rounded-full blur-3xl" />
        </div>

        <div className="relative container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 mb-4">
              <Sparkles className="w-4 h-4 text-accent-400" />
              <span className="text-sm font-medium text-white/90">AI-Powered Matching</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Your Top Job Matches
            </h1>
            <p className="text-lg text-white/70 max-w-2xl mx-auto">
              Based on your resume analysis, we found{' '}
              <span className="text-white font-semibold">{MOCK_JOBS.length} positions</span> that match
              your skills and experience.
            </p>
          </motion.div>

          {/* Stats Row */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="flex flex-wrap justify-center gap-6"
          >
            {[
              { icon: Target, label: 'Avg Match', value: '82%' },
              { icon: TrendingUp, label: 'Excellent Matches', value: MOCK_JOBS.filter((j) => j.matchScore >= 85).length.toString() },
              { icon: Briefcase, label: 'Total Jobs', value: MOCK_JOBS.length.toString() },
            ].map((stat) => (
              <div
                key={stat.label}
                className="flex items-center gap-3 px-5 py-3 bg-white/10 backdrop-blur-sm rounded-xl border border-white/10"
              >
                <stat.icon className="w-5 h-5 text-primary-400" />
                <div>
                  <div className="text-xl font-bold text-white">{stat.value}</div>
                  <div className="text-xs text-white/60">{stat.label}</div>
                </div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Search & Controls Bar */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row gap-4 mb-8 -mt-12 relative z-10"
        >
          {/* Search */}
          <div className="flex-grow relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search jobs, skills, companies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-lg"
            />
          </div>

          {/* Sort Dropdown */}
          <div className="relative">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="appearance-none w-full md:w-48 px-4 py-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 shadow-lg cursor-pointer"
            >
              <option value="match">Best Match</option>
              <option value="salary">Highest Salary</option>
              <option value="recent">Most Recent</option>
            </select>
            <ArrowUpDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
          </div>

          {/* View Toggle */}
          <div className="flex bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-lg overflow-hidden">
            <button
              onClick={() => setViewMode('cards')}
              className={`px-4 py-4 flex items-center justify-center transition-colors ${
                viewMode === 'cards'
                  ? 'bg-primary-500 text-white'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'
              }`}
            >
              <Grid3X3 className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-4 py-4 flex items-center justify-center transition-colors ${
                viewMode === 'list'
                  ? 'bg-primary-500 text-white'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'
              }`}
            >
              <List className="w-5 h-5" />
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="hidden lg:block">
            <FilterSidebar
              filters={filters}
              onFilterChange={setFilters}
              onReset={() => setFilters(defaultFilters)}
              totalJobs={MOCK_JOBS.length}
              filteredCount={filteredJobs.length}
            />

            {/* Upskilling CTA */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="mt-6 p-5 bg-gradient-to-br from-orange-500 to-amber-500 rounded-2xl text-white"
            >
              <h4 className="font-bold mb-2">Boost Your Match Score</h4>
              <p className="text-sm text-white/90 mb-4">
                Learn {allMissingSkills.length} in-demand skills to unlock more opportunities.
              </p>
              <button
                onClick={() => setShowUpskilling(true)}
                className="w-full py-2.5 bg-white text-orange-600 font-semibold rounded-xl hover:bg-orange-50 transition-colors"
              >
                View Learning Path
              </button>
            </motion.div>
          </div>

          {/* Results */}
          <div className="lg:col-span-3">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                  {filteredJobs.length} Jobs Found
                </h2>
                {activeFilterCount > 0 && (
                  <button
                    onClick={() => setFilters(defaultFilters)}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
                  >
                    <X className="w-4 h-4" />
                    Clear filters
                  </button>
                )}
              </div>
            </div>

            {/* Job Cards */}
            <AnimatePresence mode="wait">
              {filteredJobs.length > 0 ? (
                viewMode === 'cards' ? (
                  <motion.div
                    key="cards"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="space-y-4"
                  >
                    {filteredJobs.map((job, index) => (
                      <JobMatchCard
                        key={job.id}
                        job={job}
                        index={index}
                        saved={savedJobs.has(job.id)}
                        onClick={() => setSelectedJob(job)}
                        onSave={() => toggleSaveJob(job.id)}
                        onApply={() => window.open('#', '_blank')}
                      />
                    ))}
                  </motion.div>
                ) : (
                  <motion.div
                    key="list"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="space-y-3"
                  >
                    {filteredJobs.map((job) => (
                      <JobMatchCardCompact
                        key={job.id}
                        job={job}
                        onClick={() => setSelectedJob(job)}
                      />
                    ))}
                  </motion.div>
                )
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center py-16 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700"
                >
                  <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center">
                    <Search className="w-8 h-8 text-slate-400" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                    No jobs match your filters
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 mb-6">
                    Try adjusting your filters or search query
                  </p>
                  <button
                    onClick={() => setFilters(defaultFilters)}
                    className="px-6 py-3 bg-primary-500 text-white font-medium rounded-xl hover:bg-primary-600 transition-colors"
                  >
                    Reset Filters
                  </button>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Load More */}
            {filteredJobs.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="text-center pt-8"
              >
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-8 py-3 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium rounded-xl hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors shadow-sm"
                >
                  Load More Jobs
                </motion.button>
              </motion.div>
            )}
          </div>
        </div>

        {/* Upskilling Section */}
        <AnimatePresence>
          {showUpskilling && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 40 }}
              className="mt-16 pt-16 border-t border-slate-200 dark:border-slate-700"
            >
              <div className="flex justify-end mb-4">
                <button
                  onClick={() => setShowUpskilling(false)}
                  className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <UpskillingRecommendations missingSkills={allMissingSkills} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Mobile Filter Button */}
      <MobileFilterButton onClick={() => setShowMobileFilters(true)} activeCount={activeFilterCount} />

      {/* Mobile Filter Drawer */}
      <AnimatePresence>
        {showMobileFilters && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 lg:hidden"
          >
            <div className="absolute inset-0 bg-black/50" onClick={() => setShowMobileFilters(false)} />
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 30 }}
              className="absolute right-0 top-0 bottom-0 w-full max-w-sm bg-white dark:bg-slate-900 overflow-y-auto"
            >
              <div className="sticky top-0 flex items-center justify-between p-4 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
                <h3 className="font-bold text-slate-900 dark:text-white">Filters</h3>
                <button onClick={() => setShowMobileFilters(false)} className="p-2">
                  <X className="w-5 h-5 text-slate-600 dark:text-slate-300" />
                </button>
              </div>
              <div className="p-4">
                <FilterSidebar
                  filters={filters}
                  onFilterChange={setFilters}
                  onReset={() => setFilters(defaultFilters)}
                  totalJobs={MOCK_JOBS.length}
                  filteredCount={filteredJobs.length}
                />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Job Detail Modal */}
      <JobDetailModal
        job={selectedJob}
        isOpen={!!selectedJob}
        onClose={() => setSelectedJob(null)}
        saved={selectedJob ? savedJobs.has(selectedJob.id) : false}
        onSave={() => selectedJob && toggleSaveJob(selectedJob.id)}
      />
    </div>
  );
}
