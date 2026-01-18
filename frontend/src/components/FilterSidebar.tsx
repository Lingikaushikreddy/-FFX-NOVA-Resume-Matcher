/**
 * Premium Filter Sidebar - FFX NOVA
 * Beautiful filtering panel with animations and smart defaults
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Filter,
  ChevronDown,
  ChevronUp,
  MapPin,
  Shield,
  DollarSign,
  Briefcase,
  Wifi,
  Building2,
  Star,
  RotateCcw,
  Sliders,
} from 'lucide-react';

export interface FilterState {
  matchScore: [number, number];
  clearance: string[];
  jobType: string[];
  location: string[];
  salary: [number, number];
  remote: boolean | null;
  experience: string[];
}

interface FilterSidebarProps {
  filters: FilterState;
  onFilterChange: (filters: FilterState) => void;
  onReset: () => void;
  totalJobs: number;
  filteredCount: number;
  className?: string;
}

const clearanceOptions = [
  { value: 'None', label: 'No Clearance' },
  { value: 'Public Trust', label: 'Public Trust' },
  { value: 'Secret', label: 'Secret' },
  { value: 'Top Secret', label: 'Top Secret' },
  { value: 'TS/SCI', label: 'TS/SCI' },
];

const jobTypeOptions = [
  { value: 'federal', label: 'Federal', icon: Building2 },
  { value: 'military', label: 'Military', icon: Shield },
  { value: 'contractor', label: 'Contractor', icon: Briefcase },
  { value: 'private', label: 'Private', icon: Star },
];

const locationOptions = [
  'Arlington, VA',
  'Alexandria, VA',
  'Fairfax, VA',
  'Tysons, VA',
  'Reston, VA',
  'McLean, VA',
  'Falls Church, VA',
  'Washington, DC',
];

const experienceOptions = [
  { value: 'entry', label: '0-2 years' },
  { value: 'mid', label: '3-5 years' },
  { value: 'senior', label: '6-10 years' },
  { value: 'expert', label: '10+ years' },
];

interface FilterSectionProps {
  title: string;
  icon: React.ComponentType<{ className?: string }>;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

function FilterSection({ title, icon: Icon, children, defaultOpen = true }: FilterSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border-b border-slate-200 dark:border-slate-700 last:border-b-0">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between py-4 text-left hover:bg-slate-50 dark:hover:bg-slate-800/50 px-1 -mx-1 rounded-lg transition-colors"
      >
        <div className="flex items-center gap-2">
          <Icon className="w-4 h-4 text-primary-500" />
          <span className="font-medium text-slate-900 dark:text-white">{title}</span>
        </div>
        {isOpen ? (
          <ChevronUp className="w-4 h-4 text-slate-400" />
        ) : (
          <ChevronDown className="w-4 h-4 text-slate-400" />
        )}
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="pb-4">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function RangeSlider({
  min,
  max,
  value,
  onChange,
  formatLabel,
}: {
  min: number;
  max: number;
  value: [number, number];
  onChange: (value: [number, number]) => void;
  formatLabel?: (value: number) => string;
}) {
  const percentage = ((value[0] - min) / (max - min)) * 100;
  const percentageMax = ((value[1] - min) / (max - min)) * 100;

  return (
    <div className="space-y-3">
      <div className="flex justify-between text-sm">
        <span className="text-slate-600 dark:text-slate-400">
          {formatLabel ? formatLabel(value[0]) : value[0]}
        </span>
        <span className="text-slate-600 dark:text-slate-400">
          {formatLabel ? formatLabel(value[1]) : value[1]}
        </span>
      </div>
      <div className="relative h-2 bg-slate-200 dark:bg-slate-700 rounded-full">
        <div
          className="absolute h-full bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
          style={{
            left: `${percentage}%`,
            right: `${100 - percentageMax}%`,
          }}
        />
        <input
          type="range"
          min={min}
          max={max}
          value={value[0]}
          onChange={(e) => onChange([parseInt(e.target.value), value[1]])}
          className="absolute w-full h-full opacity-0 cursor-pointer"
        />
        <input
          type="range"
          min={min}
          max={max}
          value={value[1]}
          onChange={(e) => onChange([value[0], parseInt(e.target.value)])}
          className="absolute w-full h-full opacity-0 cursor-pointer"
        />
      </div>
    </div>
  );
}

function Checkbox({
  checked,
  onChange,
  label,
  icon: Icon,
}: {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
  icon?: React.ComponentType<{ className?: string }>;
}) {
  return (
    <label className="flex items-center gap-3 py-1.5 cursor-pointer group">
      <div
        className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${checked
            ? 'bg-primary-500 border-primary-500'
            : 'border-slate-300 dark:border-slate-600 group-hover:border-primary-400'
          }`}
      >
        {checked && (
          <motion.svg
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="w-3 h-3 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
          </motion.svg>
        )}
      </div>
      {Icon && <Icon className="w-4 h-4 text-slate-400" />}
      <span className="text-sm text-slate-700 dark:text-slate-300">{label}</span>
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="sr-only"
      />
    </label>
  );
}

export function FilterSidebar({
  filters,
  onFilterChange,
  onReset,
  totalJobs,
  filteredCount,
  className = '',
}: FilterSidebarProps) {
  const hasActiveFilters =
    filters.clearance.length > 0 ||
    filters.jobType.length > 0 ||
    filters.location.length > 0 ||
    filters.experience.length > 0 ||
    filters.remote !== null ||
    filters.matchScore[0] > 0 ||
    filters.matchScore[1] < 100;

  const updateFilter = <K extends keyof FilterState>(key: K, value: FilterState[K]) => {
    onFilterChange({ ...filters, [key]: value });
  };

  const toggleArrayFilter = (key: 'clearance' | 'jobType' | 'location' | 'experience', value: string) => {
    const current = filters[key];
    const updated = current.includes(value)
      ? current.filter((v) => v !== value)
      : [...current, value];
    updateFilter(key, updated);
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className={`bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden ${className}`}
    >
      {/* Header */}
      <div className="p-5 border-b border-slate-200 dark:border-slate-700 bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-800">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500">
              <Sliders className="w-4 h-4 text-white" />
            </div>
            <h3 className="font-bold text-slate-900 dark:text-white">Filters</h3>
          </div>
          {hasActiveFilters && (
            <motion.button
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onReset}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Reset
            </motion.button>
          )}
        </div>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Showing{' '}
          <span className="font-semibold text-primary-600 dark:text-primary-400">{filteredCount}</span> of{' '}
          <span className="font-semibold">{totalJobs}</span> jobs
        </p>
      </div>

      {/* Filter Sections */}
      <div className="p-5 space-y-1">
        {/* Match Score */}
        <FilterSection title="Match Score" icon={Star}>
          <RangeSlider
            min={0}
            max={100}
            value={filters.matchScore}
            onChange={(value) => updateFilter('matchScore', value)}
            formatLabel={(v) => `${v}%`}
          />
          <div className="flex gap-2 mt-3">
            {[
              { min: 85, label: 'Excellent', class: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' },
              { min: 70, label: 'Strong', class: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' },
              { min: 50, label: 'Good', class: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' },
            ].map((tier) => (
              <button
                key={tier.min}
                onClick={() => updateFilter('matchScore', [tier.min, 100])}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${filters.matchScore[0] === tier.min
                    ? tier.class + ' ring-2 ring-offset-1 ring-primary-400'
                    : 'bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'
                  }`}
              >
                {tier.label}+
              </button>
            ))}
          </div>
        </FilterSection>

        {/* Security Clearance */}
        <FilterSection title="Security Clearance" icon={Shield}>
          <div className="space-y-1">
            {clearanceOptions.map((option) => (
              <Checkbox
                key={option.value}
                checked={filters.clearance.includes(option.value)}
                onChange={() => toggleArrayFilter('clearance', option.value)}
                label={option.label}
              />
            ))}
          </div>
        </FilterSection>

        {/* Job Type */}
        <FilterSection title="Job Type" icon={Briefcase}>
          <div className="space-y-1">
            {jobTypeOptions.map((option) => (
              <Checkbox
                key={option.value}
                checked={filters.jobType.includes(option.value)}
                onChange={() => toggleArrayFilter('jobType', option.value)}
                label={option.label}
                icon={option.icon}
              />
            ))}
          </div>
        </FilterSection>

        {/* Remote */}
        <FilterSection title="Work Location" icon={Wifi}>
          <div className="flex gap-2">
            {[
              { value: null, label: 'All' },
              { value: true, label: 'Remote' },
              { value: false, label: 'On-site' },
            ].map((option) => (
              <button
                key={String(option.value)}
                onClick={() => updateFilter('remote', option.value)}
                className={`flex-1 px-3 py-2 rounded-xl text-sm font-medium transition-all ${filters.remote === option.value
                    ? 'bg-primary-500 text-white shadow-md'
                    : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600'
                  }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </FilterSection>

        {/* Location */}
        <FilterSection title="Location" icon={MapPin} defaultOpen={false}>
          <div className="space-y-1 max-h-48 overflow-y-auto">
            {locationOptions.map((location) => (
              <Checkbox
                key={location}
                checked={filters.location.includes(location)}
                onChange={() => toggleArrayFilter('location', location)}
                label={location}
              />
            ))}
          </div>
        </FilterSection>

        {/* Experience Level */}
        <FilterSection title="Experience Level" icon={Briefcase} defaultOpen={false}>
          <div className="space-y-1">
            {experienceOptions.map((option) => (
              <Checkbox
                key={option.value}
                checked={filters.experience.includes(option.value)}
                onChange={() => toggleArrayFilter('experience', option.value)}
                label={option.label}
              />
            ))}
          </div>
        </FilterSection>

        {/* Salary Range */}
        <FilterSection title="Salary Range" icon={DollarSign} defaultOpen={false}>
          <RangeSlider
            min={50000}
            max={250000}
            value={filters.salary}
            onChange={(value) => updateFilter('salary', value)}
            formatLabel={(v) => `$${(v / 1000).toFixed(0)}k`}
          />
        </FilterSection>
      </div>
    </motion.div>
  );
}

/**
 * Mobile Filter Button - Shows filter count badge
 */
export function MobileFilterButton({
  onClick,
  activeCount,
}: {
  onClick: () => void;
  activeCount: number;
}) {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="lg:hidden fixed bottom-6 right-6 z-50 flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold rounded-2xl shadow-lg shadow-primary-500/30"
    >
      <Filter className="w-5 h-5" />
      Filters
      {activeCount > 0 && (
        <span className="flex items-center justify-center w-5 h-5 bg-white text-primary-600 text-xs font-bold rounded-full">
          {activeCount}
        </span>
      )}
    </motion.button>
  );
}
