/**
 * Authentication API Service Client
 * Calls /api/v1/auth endpoints.
 */

import { apiClient, ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from './client';

export interface LoginPayload {
  username?: string;
  email?: string;
  password?: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export interface TokenData {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export const authApi = {
  login: async (payload: LoginPayload): Promise<TokenData> => {
    const res = await apiClient.post<ApiResponse<TokenData>>('/auth/login', payload);
    const { access_token, refresh_token } = res.data.data;
    localStorage.setItem(ACCESS_TOKEN_KEY, access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
    return res.data.data;
  },

  register: async (payload: RegisterPayload): Promise<UserProfile> => {
    const res = await apiClient.post<ApiResponse<UserProfile>>('/auth/register', payload);
    return res.data.data;
  },

  getCurrentUser: async (): Promise<UserProfile> => {
    const res = await apiClient.get<ApiResponse<UserProfile>>('/auth/me');
    return res.data.data;
  },

  logout: async (): Promise<void> => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
    try {
      if (refreshToken) {
        await apiClient.post('/auth/logout', { refresh_token: refreshToken });
      }
    } finally {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    }
  },
};
