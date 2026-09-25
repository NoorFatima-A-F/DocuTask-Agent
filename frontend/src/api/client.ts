/**
 * Axios HTTP Client with JWT Token Interceptors & Error Envelope Handling.
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Storage token key constants
export const ACCESS_TOKEN_KEY = 'docutask_access_token';
export const REFRESH_TOKEN_KEY = 'docutask_refresh_token';

// Request interceptor for Bearer Token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for Token Refresh and Centralized Errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

      if (refreshToken) {
        try {
          const res = await axios.post<{ data: { access_token: string; refresh_token: string } }>(
            `${API_BASE_URL}/auth/refresh`,
            { refresh_token: refreshToken }
          );

          const { access_token, refresh_token } = res.data.data;
          localStorage.setItem(ACCESS_TOKEN_KEY, access_token);
          localStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);

          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
          }
          return apiClient(originalRequest);
        } catch {
          // Token refresh failed -> purge stored session
          localStorage.removeItem(ACCESS_TOKEN_KEY);
          localStorage.removeItem(REFRESH_TOKEN_KEY);
        }
      }
    }

    return Promise.reject(error);
  }
);
