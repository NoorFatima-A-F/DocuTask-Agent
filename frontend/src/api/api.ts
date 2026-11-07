import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY, apiClient, clearTokens } from './client';
import type {
  DocumentRecord,
  Envelope,
  Extraction,
  Job,
  Page,
  ReviewDetail,
  ReviewSummary,
  Tokens,
  UploadResult,
  User,
} from './types';

const data = <T>(p: Promise<{ data: Envelope<T> }>): Promise<T> => p.then((r) => r.data.data);

export const api = {
  async login(usernameOrEmail: string, password: string): Promise<void> {
    const tokens = await data<Tokens>(
      apiClient.post('/auth/login', { username_or_email: usernameOrEmail, password }),
    );
    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
  },
  register: (email: string, username: string, password: string) =>
    data<User>(apiClient.post('/auth/register', { email, username, password })),
  me: () => data<User>(apiClient.get('/auth/me')),
  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
    try {
      // The access token is attached by the request interceptor; logout requires it.
      if (refreshToken) await apiClient.post('/auth/logout', { refresh_token: refreshToken });
    } finally {
      clearTokens();
    }
  },

  upload(file: File): Promise<UploadResult> {
    const form = new FormData();
    form.append('file', file, file.name);
    return data<UploadResult>(apiClient.post('/documents/upload', form));
  },
  documents: () => data<Page<DocumentRecord>>(apiClient.get('/documents', { params: { page_size: 50 } })),

  createJob: (documentId: string, documentType: string) =>
    data<Job>(apiClient.post('/jobs', { document_id: documentId, document_type: documentType })),
  jobs: () => data<Page<Job>>(apiClient.get('/jobs', { params: { page_size: 50 } })),
  job: (jobId: string) => data<Job>(apiClient.get(`/jobs/${jobId}`)),
  retryJob: (jobId: string) => data<Job>(apiClient.post(`/jobs/${jobId}/retry`)),

  extraction: (documentId: string) => data<Extraction>(apiClient.get(`/ai/result/${documentId}`)),

  reviews: () => data<Page<ReviewSummary>>(apiClient.get('/reviews', { params: { status: 'pending' } })),
  review: (extractionId: string) => data<ReviewDetail>(apiClient.get(`/reviews/${extractionId}`)),
  approve: (extractionId: string, corrections: Record<string, unknown> | null) =>
    data<unknown>(apiClient.post(`/reviews/${extractionId}/approve`, corrections ? { corrections } : {})),
  reject: (extractionId: string, reason: string) =>
    data<unknown>(apiClient.post(`/reviews/${extractionId}/reject`, { reason })),
  async documentBlob(downloadUrl: string): Promise<Blob> {
    const res = await apiClient.get(downloadUrl.replace(/^\/api\/v1/, ''), { responseType: 'blob' });
    return res.data as Blob;
  },
};
