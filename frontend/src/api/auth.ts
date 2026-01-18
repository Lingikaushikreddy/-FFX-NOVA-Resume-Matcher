/**
 * Authentication API
 */

import { apiClient } from './client';
import type { AuthTokens, LoginCredentials, RegisterData, User } from '../types';

export const authApi = {
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const tokens = await apiClient.post<AuthTokens>('/auth/login', credentials);
    apiClient.setAccessToken(tokens.access_token);
    apiClient.setRefreshToken(tokens.refresh_token);
    return tokens;
  },

  async register(data: RegisterData): Promise<User> {
    return apiClient.post<User>('/auth/register', data);
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      apiClient.clearTokens();
    }
  },

  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me');
  },

  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    return apiClient.post<AuthTokens>('/auth/refresh', { refresh_token: refreshToken });
  },

  async forgotPassword(email: string): Promise<void> {
    return apiClient.post('/auth/forgot-password', { email });
  },

  async resetPassword(token: string, password: string): Promise<void> {
    return apiClient.post('/auth/reset-password', { token, password });
  },
};

export default authApi;
