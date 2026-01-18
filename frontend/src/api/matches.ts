/**
 * Matches API
 */

import { apiClient } from './client';
import type { MatchResult, MatchSession } from '../types';

export const matchesApi = {
  async getTopMatches(resumeId: string, limit = 10): Promise<MatchResult[]> {
    return apiClient.get<MatchResult[]>(`/match/top-matches/${resumeId}`, {
      params: { limit },
    });
  },

  async getMatchSession(sessionId: string): Promise<MatchSession> {
    return apiClient.get<MatchSession>(`/match/sessions/${sessionId}`);
  },

  async getAllSessions(): Promise<MatchSession[]> {
    return apiClient.get<MatchSession[]>('/match/sessions');
  },

  async runMatching(resumeId: string, options?: {
    min_score?: number;
    clearance_filter?: boolean;
    location?: string;
  }): Promise<MatchSession> {
    return apiClient.post<MatchSession>('/match/run', {
      resume_id: resumeId,
      ...options,
    });
  },

  async getMatchDetails(matchId: string): Promise<MatchResult> {
    return apiClient.get<MatchResult>(`/match/results/${matchId}`);
  },

  async getSkillGapAnalysis(resumeId: string): Promise<{
    skill_gaps: { skill: string; frequency: number; priority: string }[];
    recommendations: string[];
  }> {
    return apiClient.get(`/match/skill-gaps/${resumeId}`);
  },
};

export default matchesApi;
