/**
 * TypeScript domain models for Document Intelligence, Extraction, and HITL Review.
 */

export interface ExtractedField {
  value: string | number | null;
  confidence: number; // 0.0 to 1.0
  source_page?: number;
  bbox?: [number, number, number, number]; // [ymin, xmin, ymax, xmax]
  is_verified_by_human?: boolean;
}

export interface LineItem {
  id: string;
  description: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  confidence: number;
}

export interface StructuredInvoiceData {
  invoice_number: ExtractedField;
  vendor_name: ExtractedField;
  invoice_date: ExtractedField;
  due_date: ExtractedField;
  subtotal: ExtractedField;
  tax_amount: ExtractedField;
  total_amount: ExtractedField;
  currency: ExtractedField;
  payment_terms: ExtractedField;
  line_items: LineItem[];
}

export type JobStatus = 'PENDING' | 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'RETRYING' | 'CANCELLED';

export interface DocumentJob {
  id: string;
  document_id: string;
  document_name: string;
  file_size: string;
  mime_type: string;
  status: JobStatus;
  progress: number; // 0 to 100
  current_step: string;
  worker_name?: string;
  created_at: string;
  updated_at: string;
  overall_confidence?: number;
  extracted_data?: StructuredInvoiceData;
  raw_ocr_text?: string;
  preview_url?: string;
  requires_hitl: boolean;
  error_message?: string;
}
