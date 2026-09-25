/**
 * Document Ingestion & Storage API Service Client
 * Strictly calls /api/v1/documents endpoints.
 */

import { apiClient } from './client';
import {
  DocumentListResponse,
  DocumentResponse,
  UploadResponse,
} from '../types/document';

interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export const documentsApi = {
  /**
   * Upload binary document with SHA-256 duplicate detection
   */
  upload: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file, file.name);

    const res = await apiClient.post<ApiResponse<UploadResponse>>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data.data;
  },

  /**
   * List paginated documents
   */
  list: async (page = 1, pageSize = 20, query?: string): Promise<DocumentListResponse> => {
    const params: Record<string, unknown> = { page, page_size: pageSize };
    if (query) params.q = query;

    const res = await apiClient.get<ApiResponse<DocumentListResponse>>('/documents', {
      params,
    });
    return res.data.data;
  },

  /**
   * Retrieve single document metadata
   */
  getById: async (documentId: string): Promise<DocumentResponse> => {
    const res = await apiClient.get<ApiResponse<DocumentResponse>>(`/documents/${documentId}`);
    return res.data.data;
  },

  /**
   * Delete document by ID
   */
  delete: async (documentId: string): Promise<{ message: string }> => {
    const res = await apiClient.delete<ApiResponse<{ message: string }>>(`/documents/${documentId}`);
    return res.data.data;
  },
};
