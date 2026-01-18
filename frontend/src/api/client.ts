// Use Vite proxy in development (avoids CORS issues)
const API_BASE_URL = '/api/v1';

export interface ResumeUploadResponse {
  resume_id: string;
  message: string;
  candidate_name?: string;
  candidate_email?: string;
  skills_count: number;
}

export interface Explainability {
  matched_skills: string[];
  missing_required_skills: string[];
  missing_preferred_skills: string[];
  skill_match_percentage: number;
  semantic_similarity: number;
  explanation_text?: string;
}

export interface MatchResponse {
  match_id?: string;
  resume_id: string;
  job_id: string;
  final_score: number;
  semantic_score: number;
  skill_score: number;
  match_tier: string;
  explainability: Explainability;
}

export interface JobMatch {
  match_id?: string;
  job_id: string;
  title: string;
}

export interface EnrichedJobMatch {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  matchScore: number;
  semanticScore: number;
  skillScore: number;
  experienceScore: number;
  clearance: 'None' | 'Secret' | 'Top Secret' | 'TS/SCI';
  matchedSkills: string[];
  missingSkills: string[];
  isRemote: boolean;
}

interface ApiRequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>;
}

export const apiClient = {
  _accessToken: localStorage.getItem('accessToken'),
  _refreshToken: localStorage.getItem('refreshToken'),

  setAccessToken(token: string) {
    this._accessToken = token;
    localStorage.setItem('accessToken', token);
  },

  setRefreshToken(token: string) {
    this._refreshToken = token;
    localStorage.setItem('refreshToken', token);
  },

  clearTokens() {
    this._accessToken = null;
    this._refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  async request<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
    let url = `${API_BASE_URL}${endpoint}`;

    if (options.params) {
      const params = new URLSearchParams();
      Object.entries(options.params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, String(value));
        }
      });
      const queryString = params.toString();
      if (queryString) {
        url += (url.includes('?') ? '&' : '?') + queryString;
      }
    }

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(this._accessToken ? { Authorization: `Bearer ${this._accessToken}` } : {}),
      ...options.headers,
    };

    const config: RequestInit = {
      ...options,
      headers,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `Request failed with status ${response.status}`);
    }

    if (response.status === 204) return {} as T;

    return response.json();
  },

  get<T>(url: string, options?: ApiRequestOptions) {
    return this.request<T>(url, { ...options, method: 'GET' });
  },

  post<T>(url: string, data?: any, options?: ApiRequestOptions) {
    return this.request<T>(url, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  delete<T>(url: string, options?: ApiRequestOptions) {
    return this.request<T>(url, { ...options, method: 'DELETE' });
  },

  /**
   * Upload file (generic)
   */
  upload<T>(url: string, file: File, onProgress?: (progress: number) => void): Promise<T> {
    const formData = new FormData();
    formData.append('file', file);

    const headers: HeadersInit = {
      ...(this._accessToken ? { Authorization: `Bearer ${this._accessToken}` } : {}),
    };

    if (onProgress) onProgress(10);

    return fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers,
      body: formData,
    }).then(async (response) => {
      if (onProgress) onProgress(100);

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(error.detail || 'Upload failed');
      }
      return response.json();
    });
  },

  /**
   * Upload a resume file (PDF/DOCX) - Specialized
   */
  uploadResume: async (file: File): Promise<ResumeUploadResponse> => {
    return apiClient.upload<ResumeUploadResponse>('/resumes/upload-file', file);
  },

  /**
   * Get matches for a resume - Specialized
   */
  getMatchesForResume: async (resumeId: string): Promise<MatchResponse[]> => {
    const data = await apiClient.post<{ matches: MatchResponse[] }>('/match/resume-matches', {
      resume_id: resumeId,
      limit: 10
    });
    return data.matches;
  },

  /**
   * Get Job Details (to enrich the match) - Specialized
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  getJobDetails: async (jobId: string) => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return apiClient.get<any>(`/jobs/${jobId}`);
  },

  /**
   * Helper: Get Enriched Matches (Frontend Ready)
   */
  getEnrichedMatches: async (resumeId: string): Promise<EnrichedJobMatch[]> => {
    // 1. Get Matches
    const matches = await apiClient.getMatchesForResume(resumeId);

    // 2. Fetch details for each job parallelly
    const enriched = await Promise.all(matches.map(async (match) => {
      try {
        const jobRes = await apiClient.getJobDetails(match.job_id);

        return {
          id: match.job_id,
          title: jobRes.title,
          company: jobRes.company,
          location: jobRes.location || 'Remote',
          salary: '$120k - $160k', // Mock default
          matchScore: Math.round(match.final_score * 100),
          semanticScore: Math.round(match.semantic_score * 100),
          skillScore: Math.round(match.skill_score * 100),
          experienceScore: Math.round((match.semantic_score + match.skill_score) / 2 * 90), // Mock derived score
          clearance: 'Secret', // Default for now
          matchedSkills: match.explainability.matched_skills,
          missingSkills: match.explainability.missing_required_skills,
          isRemote: jobRes.location?.toLowerCase().includes('remote') || false
        };
      } catch (e) {
        console.error(`Failed to enrich job ${match.job_id}`, e);
        return null;
      }
    }));

    return enriched.filter((j): j is EnrichedJobMatch => j !== null);
  }
};
