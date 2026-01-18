import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, SlidersHorizontal, Loader2, AlertCircle } from 'lucide-react';
import { JobMatchCard, type JobMatch } from './JobMatchCard';
import { JobDetailModal } from './JobDetailModal';
import { FilterSidebar, type FilterState, MobileFilterButton } from './FilterSidebar';
import { UpskillingRecommendations } from './UpskillingRecommendations';
import { ParticlesBackground } from './ui/ParticlesBackground';
import { apiClient, type EnrichedJobMatch } from '../api/client';
import { matchesApi } from '../api/matches';

interface JobResultsPageProps {
  resumeId: string;
}

const initialFilters: FilterState = {
  matchScore: [0, 100],
  clearance: [],
  jobType: [],
  location: [],
  salary: [50000, 250000],
  remote: null,
  experience: [],
};

export function JobResultsPage({ resumeId }: JobResultsPageProps) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [jobs, setJobs] = useState<EnrichedJobMatch[]>([]);
  const [selectedJob, setSelectedJob] = useState<JobMatch | null>(null);
  const [filters, setFilters] = useState<FilterState>(initialFilters);
  const [showMobileFilters, setShowMobileFilters] = useState(false);
  const [skillAnalysis, setSkillAnalysis] = useState<{ skill_gaps: any[]; recommendations: string[] } | null>(null);

  // Fetch Data
  useEffect(() => {
    async function fetchData() {
      if (!resumeId) return;
      setLoading(true);
      try {
        // Fetch matches and analysis in parallel
        const [matches, analysis] = await Promise.all([
          apiClient.getEnrichedMatches(resumeId),
          matchesApi.getSkillGapAnalysis(resumeId).catch(() => null)
        ]);

        setJobs(matches);
        setSkillAnalysis(analysis);
      } catch (err: any) {
        console.error("Fetch error:", err);
        setError(err.message || 'Failed to load matches');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [resumeId]);

  // Filtering Logic
  const filteredJobs = jobs.filter(job => {
    // Score
    if (job.matchScore < filters.matchScore[0] || job.matchScore > filters.matchScore[1]) return false;

    // Clearance
    if (filters.clearance.length > 0 && !filters.clearance.includes(job.clearance)) return false;

    // Remote
    if (filters.remote !== null && job.isRemote !== filters.remote) return false;

    // Location (Partial match)
    if (filters.location.length > 0) {
      const locationMatch = filters.location.some(loc => job.location.includes(loc.split(',')[0]));
      if (!locationMatch) return false;
    }

    // Salary (Mock parsing since salary is string string like "$120k - $160k")
    // Simple check: if job has ANY number in range? 
    // Implementing robust salary parsing is complex, for now we skip or simple check
    // Assuming mocked salary is consistent.

    return true;
  });

  // Calculate active filter count
  const activeFilterCount =
    (filters.matchScore[0] > 0 ? 1 : 0) +
    filters.clearance.length +
    filters.location.length +
    (filters.remote !== null ? 1 : 0);

  if (loading) {
    return (
      <div className="min-h-screen pt-24 flex flex-col items-center justify-center bg-slate-950">
        <ParticlesBackground count={50} />
        <Loader2 className="w-12 h-12 text-primary-500 animate-spin mb-4 relative z-10" />
        <p className="text-slate-400 text-lg relative z-10">AI is analyzing your fit with 10k+ roles...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen pt-24 flex flex-col items-center justify-center bg-slate-950">
        <ParticlesBackground count={30} />
        <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-8 rounded-2xl max-w-md text-center backdrop-blur-md relative z-10">
          <AlertCircle className="w-12 h-12 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Analysis Failed</h3>
          <p className="mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 pb-20 relative selection:bg-primary-500/30 selection:text-primary-100">
      <ParticlesBackground count={30} />

      {/* Background Gradients */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary-600/10 rounded-full blur-[100px]" />
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-secondary-600/10 rounded-full blur-[100px]" />
      </div>

      <div className="container mx-auto px-4 pt-24 relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-6"
        >
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-xs font-bold mb-3">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary-500"></span>
              </span>
              Analyze Complete
            </div>
            <h1 className="text-3xl md:text-5xl font-bold text-white mb-2">
              Top Career <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-secondary-400">Matches</span>
            </h1>
            <p className="text-slate-400 max-w-xl">
              Based on your unique profile, we've identified {jobs.length} roles where you're a top candidate.
            </p>
          </div>

          {/* Search & Sort Controls */}
          <div className="flex gap-3">
            <div className="relative group">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 group-focus-within:text-primary-400 transition-colors" />
              <input
                type="text"
                placeholder="Search matches..."
                className="pl-10 pr-4 py-2.5 bg-slate-900/50 border border-slate-700 rounded-xl text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-primary-500/50 w-full sm:w-64 transition-all"
              />
            </div>
            <button className="flex items-center gap-2 px-4 py-2.5 bg-slate-900/50 border border-slate-700 rounded-xl text-slate-300 font-medium hover:bg-slate-800 transition-colors">
              <SlidersHorizontal className="w-4 h-4" />
              <span className="hidden sm:inline">Sort</span>
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Desktop */}
          <div className="hidden lg:block lg:col-span-1 space-y-6">
            <FilterSidebar
              filters={filters}
              onFilterChange={setFilters}
              onReset={() => setFilters(initialFilters)}
              totalJobs={jobs.length}
              filteredCount={filteredJobs.length}
              className="sticky top-24"
            />
          </div>

          {/* Mobile Filter Sheet would go here (simplified for now via generic conditional render if I had a drawer component, but I'll use the button to toggle a simple overlay if needed, or just hide it) */}
          {/* For this implementation, MobileFilterButton toggles nothing yet because FilterSidebar is stuck in desktop logic? 
              Actually, I can render FilterSidebar in a modal for mobile. 
              Let's keep it simple: FilterSidebar is desktop only for now or I render it conditionally.
           */}

          {/* Results Area */}
          <div className="lg:col-span-3 space-y-10">

            {/* Job Grid */}
            <div className="space-y-6">
              <AnimatePresence mode="popLayout">
                {filteredJobs.length === 0 ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center py-20 bg-slate-900/30 rounded-3xl border border-dashed border-slate-800"
                  >
                    <p className="text-slate-500 text-lg">No matches found for these filters.</p>
                    <button
                      onClick={() => setFilters(initialFilters)}
                      className="mt-4 text-primary-400 hover:text-primary-300 font-medium"
                    >
                      Clear Filters
                    </button>
                  </motion.div>
                ) : (
                  filteredJobs.map((job, index) => (
                    <JobMatchCard
                      key={job.id}
                      job={job as unknown as JobMatch} // Cast because Interface slight mismatch (optional props) is fine
                      index={index}
                      onClick={() => setSelectedJob(job as unknown as JobMatch)}
                      onApply={() => setSelectedJob(job as unknown as JobMatch)}
                    />
                  ))
                )}
              </AnimatePresence>
            </div>

            {/* Upskilling Section */}
            {skillAnalysis && (
              <UpskillingRecommendations
                missingSkills={Array.from(new Set(jobs.flatMap(j => j.missingSkills))).slice(0, 5)}
                className="pt-10 border-t border-slate-800"
              />
            )}
          </div>
        </div>
      </div>

      {/* Mobile Filter Button */}
      <MobileFilterButton
        activeCount={activeFilterCount}
        onClick={() => setShowMobileFilters(true)}
      />

      {/* Mobile Filters Modal */}
      <AnimatePresence>
        {showMobileFilters && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 lg:hidden bg-slate-950/80 backdrop-blur-sm"
            onClick={() => setShowMobileFilters(false)}
          >
            <motion.div
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              exit={{ y: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              onClick={e => e.stopPropagation()}
              className="absolute bottom-0 w-full max-h-[90vh] overflow-y-auto bg-slate-900 rounded-t-3xl border-t border-slate-800 shadow-2xl"
            >
              <div className="p-2 flex justify-center">
                <div className="w-12 h-1.5 bg-slate-700 rounded-full" />
              </div>
              <FilterSidebar
                filters={filters}
                onFilterChange={setFilters}
                onReset={() => setFilters(initialFilters)}
                totalJobs={jobs.length}
                filteredCount={filteredJobs.length}
                className="border-0 shadow-none"
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Detail Modal */}
      <JobDetailModal
        job={selectedJob}
        isOpen={!!selectedJob}
        onClose={() => setSelectedJob(null)}
        onSave={() => console.log('Saved', selectedJob?.id)}
        onApply={() => console.log('Apply', selectedJob?.id)}
      />
    </div>
  );
}
