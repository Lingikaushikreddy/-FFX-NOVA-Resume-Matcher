/**
 * User Types for FFX NOVA
 */

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  avatar_url?: string;
  clearance_level?: ClearanceLevel;
  created_at: string;
  updated_at: string;
}

export type ClearanceLevel =
  | 'none'
  | 'public_trust'
  | 'secret'
  | 'top_secret'
  | 'ts_sci';

export interface UserProfile extends User {
  phone?: string;
  location?: string;
  linkedin_url?: string;
  resume_count: number;
  saved_jobs_count: number;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}
