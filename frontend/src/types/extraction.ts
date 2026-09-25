/**
 * Extraction & Human-In-The-Loop Schema Models
 * Strictly typed extraction entities, bounding boxes, and confidence thresholds.
 */

export interface BoundingBox {
  page: number;
  x_min: number; // Normalized coordinate [0.0, 1.0]
  y_min: number;
  x_max: number;
  y_max: number;
}

export type ConfidenceTier = 'HIGH' | 'MEDIUM' | 'LOW';

export interface ExtractedField<T = string | number> {
  key: string;
  label: string;
  value: T;
  confidence: number; // 0.0 - 1.0
  boundingBox?: BoundingBox;
  validationRegex?: string;
  isModified?: boolean;
  operatorCorrection?: T;
}

export interface InvoiceLineItem {
  id: string;
  description: ExtractedField<string>;
  quantity: ExtractedField<number>;
  unit_price: ExtractedField<number>;
  total_price: ExtractedField<number>;
}

export interface InvoiceExtractionSchema {
  document_id: string;
  invoice_number: ExtractedField<string>;
  vendor_name: ExtractedField<string>;
  vendor_tax_id: ExtractedField<string>;
  invoice_date: ExtractedField<string>;
  due_date: ExtractedField<string>;
  subtotal: ExtractedField<number>;
  tax_amount: ExtractedField<number>;
  total_amount: ExtractedField<number>;
  currency: ExtractedField<string>;
  line_items: InvoiceLineItem[];
  overall_confidence: number;
}

export interface HumanFeedbackPayload {
  mission_id?: string;
  document_id: string;
  field_name: string;
  original_value: string;
  corrected_value: string;
  distillation_type: 'RULE' | 'FEW_SHOT' | 'FINE_TUNE';
  operator_notes?: string;
}

export function getConfidenceTier(confidence: number): ConfidenceTier {
  if (confidence >= 0.90) return 'HIGH';
  if (confidence >= 0.70) return 'MEDIUM';
  return 'LOW';
}
