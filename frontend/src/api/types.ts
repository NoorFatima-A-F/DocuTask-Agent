// Mirrors the backend response schemas (app/schemas, app/ai/schemas.py, app/api/v1/endpoints/reviews.py).

export interface Envelope<T> {
  success: boolean;
  message: string;
  data: T;
  errors?: { error_code?: string } & Record<string, unknown>;
}

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages?: number;
}

export interface User {
  id: string;
  email: string;
  username: string;
  role: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface Tokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface DocumentRecord {
  id: string;
  original_filename: string;
  mime_type: string;
  file_size: number;
  upload_status: string;
  created_at: string;
}

export interface UploadResult {
  document: DocumentRecord;
  is_duplicate: boolean;
  message: string;
}

export type JobStatus = 'QUEUED' | 'RUNNING' | 'RETRYING' | 'COMPLETED' | 'NEEDS_REVIEW' | 'FAILED';
export const FINISHED_JOB_STATUSES: readonly JobStatus[] = ['COMPLETED', 'NEEDS_REVIEW', 'FAILED'];

export interface Job {
  id: string;
  document_id: string;
  document_type: string;
  status: JobStatus;
  attempts: number;
  max_attempts: number;
  error_code: string | null;
  last_error: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface FieldEvidence {
  value: unknown;
  grounded: boolean | null;
  score: number | null;
  required: boolean;
}

export interface ConfidenceDetails {
  score: number;
  fields: Record<string, FieldEvidence>;
  required_missing: string[];
  required_ungrounded: string[];
  checks: { name: string; passed: boolean; detail: string }[];
  failed_checks: string[];
  ocr_confidence: number | null;
}

export type ExtractionStatus = 'COMPLETED' | 'NEEDS_REVIEW' | 'FAILED';

export interface ExtractionResult {
  status: ExtractionStatus;
  structured_json: Record<string, unknown> | null;
  final_json: Record<string, unknown> | null;
  confidence: number | null;
  confidence_details: ConfidenceDetails | null;
  error_code: string | null;
  error_message: string | null;
}

export interface Extraction {
  id: string;
  metadata: { document_id: string; document_type: string; provider: string; model: string; created_at: string };
  statistics: { processing_time_ms: number; estimated_cost: number | null };
  result: ExtractionResult;
}

export interface ReviewSummary {
  extraction_id: string;
  document_id: string;
  document_type: string;
  status: string;
  confidence: number | null;
  created_at: string;
}

export interface ReviewDetail extends ReviewSummary {
  structured_json: Record<string, unknown> | null;
  final_json: Record<string, unknown> | null;
  confidence_details: ConfidenceDetails | null;
  error_code: string | null;
  ocr_text: string;
  document_filename: string | null;
  document_download_url: string;
}

export const DOCUMENT_TYPES = [
  'invoice',
  'receipt',
  'purchase_order',
  'bank_statement',
  'utility_bill',
  'contract',
  'resume',
  'passport',
  'driver_license',
  'national_id',
  'medical_report',
  'insurance_form',
  'research_paper',
  'generic',
] as const;
