/**
 * Document Domain & Ingestion Models
 * Strictly typed against FastAPI backend /api/v1/documents schemas.
 */

export type DocumentStatus = 'PENDING' | 'PROCESSED' | 'FAILED' | 'ARCHIVED';

export interface DocumentResponse {
  id: string;
  original_filename: string;
  file_hash: string;
  mime_type: string;
  file_size_bytes: number;
  status: DocumentStatus;
  storage_path: string;
  created_at: string;
  updated_at: string;
}

export interface UploadResponse {
  id: string;
  filename: string;
  file_hash: string;
  file_size: number;
  mime_type: string;
  status: DocumentStatus;
  message: string;
}

export interface DocumentListResponse {
  items: DocumentResponse[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface DocumentValidationResult {
  isValid: boolean;
  error?: string;
  detectedMimeType?: string;
  sizeBytes: number;
  sha256Hex?: string;
}
