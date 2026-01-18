/**
 * Resume API
 */

import { apiClient } from './client';
import type { Resume, ParsedResume } from '../types';

export const resumeApi = {
  async upload(file: File, onProgress?: (progress: number) => void): Promise<Resume> {
    return apiClient.upload<Resume>('/resumes/upload', file, onProgress);
  },

  async getAll(): Promise<Resume[]> {
    return apiClient.get<Resume[]>('/resumes');
  },

  async getById(id: string): Promise<Resume> {
    return apiClient.get<Resume>(`/resumes/${id}`);
  },

  async delete(id: string): Promise<void> {
    return apiClient.delete(`/resumes/${id}`);
  },

  async getParsedData(id: string): Promise<ParsedResume> {
    return apiClient.get<ParsedResume>(`/resumes/${id}/parsed`);
  },

  async reparse(id: string): Promise<Resume> {
    return apiClient.post<Resume>(`/resumes/${id}/reparse`);
  },
};

export default resumeApi;
