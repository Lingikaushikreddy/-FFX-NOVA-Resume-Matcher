/**
 * Jobs API
 */

import { apiClient } from './client';
import type { Job, JobFilter, SavedJob, PaginatedResponse } from '../types';

export const jobsApi = {
  async search(filter: JobFilter, page = 1, perPage = 20): Promise<PaginatedResponse<Job>> {
    return apiClient.post<PaginatedResponse<Job>>('/jobs/search', {
      ...filter,
      page,
      per_page: perPage,
    });
  },

  async getById(id: string): Promise<Job> {
    return apiClient.get<Job>(`/jobs/${id}`);
  },

  async getSaved(): Promise<SavedJob[]> {
    return apiClient.get<SavedJob[]>('/jobs/saved');
  },

  async saveJob(jobId: string, notes?: string): Promise<SavedJob> {
    return apiClient.post<SavedJob>(`/jobs/${jobId}/save`, { notes });
  },

  async unsaveJob(jobId: string): Promise<void> {
    return apiClient.delete(`/jobs/${jobId}/save`);
  },

  async markApplied(jobId: string): Promise<SavedJob> {
    return apiClient.post<SavedJob>(`/jobs/${jobId}/applied`);
  },

  async getRecommended(): Promise<Job[]> {
    return apiClient.get<Job[]>('/jobs/recommended');
  },
};

export default jobsApi;
