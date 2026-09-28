/**
 * Document Domain & Ingestion Models
 * Strictly typed against FastAPI backend /api/v1/documents schemas.
 */

export type DocumentStatus = 'PENDING' | 'PROCESSED' | 'FAILED' | 'ARCHIVED';

export type JobStatus = 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED';

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

export interface LineItem {
  id: string;
  description: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  confidence: number;
}

export interface StructuredField<T = string | number> {
  value: T;
  confidence: number;
  source_page?: number;
  bbox?: [number, number, number, number];
  is_verified_by_human?: boolean;
}

export interface StructuredInvoiceData {
  invoice_number: StructuredField<string>;
  vendor_name: StructuredField<string>;
  invoice_date: StructuredField<string>;
  due_date: StructuredField<string>;
  subtotal: StructuredField<number>;
  tax_amount: StructuredField<number>;
  total_amount: StructuredField<number>;
  currency: StructuredField<string>;
  payment_terms?: StructuredField<string>;
  line_items: LineItem[];
}

export interface DocumentJob {
  id: string;
  document_id: string;
  document_name: string;
  file_size: string;
  mime_type: string;
  status: JobStatus;
  progress: number;
  current_step: string;
  worker_name?: string;
  created_at: string;
  updated_at: string;
  preview_url?: string;
  requires_hitl?: boolean;
  overall_confidence?: number;
  extracted_data?: StructuredInvoiceData;
}
