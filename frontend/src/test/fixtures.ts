import type { ConfidenceDetails, Extraction, Job, ReviewDetail } from '../api/types';

export const job = (overrides: Partial<Job> = {}): Job => ({
  id: '11111111-1111-1111-1111-111111111111',
  document_id: '22222222-2222-2222-2222-222222222222',
  document_type: 'invoice',
  status: 'QUEUED',
  attempts: 0,
  max_attempts: 4,
  error_code: null,
  last_error: null,
  started_at: null,
  completed_at: null,
  created_at: '2026-11-08T10:00:00Z',
  updated_at: '2026-11-08T10:00:00Z',
  ...overrides,
});

export const details: ConfidenceDetails = {
  score: 0.62,
  fields: {
    vendor_name: { value: 'Northwind Traders', grounded: false, score: 40, required: true },
    total_amount: { value: 1250, grounded: true, score: 100, required: true },
    notes: { value: null, grounded: null, score: null, required: false },
  },
  required_missing: [],
  required_ungrounded: ['vendor_name'],
  checks: [{ name: 'line_items_sum', passed: false, detail: 'items sum 1200 != total 1250' }],
  failed_checks: ['line_items_sum'],
  ocr_confidence: 0.93,
};

export const extraction = (status: Extraction['result']['status'] = 'NEEDS_REVIEW'): Extraction => ({
  id: '33333333-3333-3333-3333-333333333333',
  metadata: {
    document_id: '22222222-2222-2222-2222-222222222222',
    document_type: 'invoice',
    provider: 'gemini',
    model: 'gemini-3.8-flash',
    created_at: '2026-11-08T10:00:05Z',
  },
  statistics: { processing_time_ms: 2100, estimated_cost: null },
  result: {
    status,
    structured_json: { vendor_name: 'Northwind Traders', total_amount: 1250, notes: null },
    final_json: status === 'COMPLETED' ? { vendor_name: 'Contoso Ltd', total_amount: 1250, notes: null } : null,
    confidence: 0.62,
    confidence_details: details,
    error_code: null,
    error_message: null,
  },
});

export const reviewDetail = (): ReviewDetail => ({
  extraction_id: '33333333-3333-3333-3333-333333333333',
  document_id: '22222222-2222-2222-2222-222222222222',
  document_type: 'invoice',
  status: 'NEEDS_REVIEW',
  confidence: 0.62,
  created_at: '2026-11-08T10:00:05Z',
  structured_json: { vendor_name: 'Northwind Traders', total_amount: 1250, notes: null },
  final_json: null,
  confidence_details: details,
  error_code: null,
  ocr_text: 'INVOICE\nContoso Ltd\nTotal 1,250.00',
  document_filename: 'inv.png',
  document_download_url: '/api/v1/reviews/33333333-3333-3333-3333-333333333333/document',
});
