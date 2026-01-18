/**
 * Job Types for FFX NOVA
 */

import type { ClearanceLevel } from './user';

export interface Job {
  id: string;
  title: string;
  company: string;
  description: string;
  location: string;
  clearance_level: ClearanceLevel;
  required_skills: string[];
  preferred_skills: string[];
  min_experience_years: number;
  salary_min?: number;
  salary_max?: number;
  is_remote: boolean;
  job_type: 'federal' | 'military' | 'contractor' | 'private';
  posted_at: string;
  expires_at?: string;
  application_url?: string;
}

export interface JobFilter {
  query?: string;
  location?: string;
  clearance_level?: ClearanceLevel;
  job_type?: Job['job_type'][];
  is_remote?: boolean;
  min_salary?: number;
  max_experience_years?: number;
  skills?: string[];
}

export interface SavedJob {
  id: string;
  job: Job;
  saved_at: string;
  notes?: string;
  applied: boolean;
  applied_at?: string;
}
