/**
 * Match Result Types for FFX NOVA
 */

import type { Job } from './job';

export type MatchTier =
  | 'excellent'
  | 'strong'
  | 'good'
  | 'fair'
  | 'weak'
  | 'disqualified';

export interface SkillGap {
  skill: string;
  is_required: boolean;
  priority: 'high' | 'medium' | 'low';
  resources?: LearningResource[];
}

export interface LearningResource {
  title: string;
  url: string;
  provider: string;
  type: 'course' | 'certification' | 'tutorial' | 'documentation';
  estimated_hours?: number;
}

export interface ScoreBreakdown {
  semantic_score: number;
  semantic_contribution: number;
  skills_score: number;
  skills_contribution: number;
  experience_score: number;
  experience_contribution: number;
}

export interface MatchResult {
  id: string;
  job: Job;
  ffx_score: number;
  tier: MatchTier;
  score_breakdown: ScoreBreakdown;
  matched_skills: string[];
  missing_required_skills: string[];
  missing_preferred_skills: string[];
  skill_gaps: SkillGap[];
  upskilling_recommendations: string[];
  clearance_met: boolean;
  experience_met: boolean;
  explanation: string;
  disqualified: boolean;
  disqualification_reason?: string;
}

export interface MatchSession {
  id: string;
  resume_id: string;
  created_at: string;
  total_matches: number;
  excellent_count: number;
  strong_count: number;
  good_count: number;
  results: MatchResult[];
}

export interface Resume {
  id: string;
  filename: string;
  uploaded_at: string;
  parsed_data: ParsedResume;
  match_count: number;
}

export interface ParsedResume {
  candidate_name?: string;
  email?: string;
  phone?: string;
  summary?: string;
  skills: string[];
  experience: WorkExperience[];
  education: Education[];
  certifications: string[];
  clearance_detected?: string;
  years_experience: number;
}

export interface WorkExperience {
  company: string;
  title: string;
  start_date: string;
  end_date?: string;
  is_current: boolean;
  description?: string;
  skills_used?: string[];
}

export interface Education {
  institution: string;
  degree: string;
  field_of_study?: string;
  graduation_date?: string;
  gpa?: number;
}
