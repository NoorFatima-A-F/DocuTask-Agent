/**
 * ConfidenceScore Component Contract & Model
 * 
 * Supports rigorous scientific reporting: empirical sample size (n),
 * uncertainty bounds, p-value, and zero-fabrication sentinels.
 */

export type ZeroFabricationSentinel =
  | 'UNKNOWN'
  | 'NOT_AVAILABLE'
  | 'NOT_COLLECTED'
  | 'NOT_EXECUTED'
  | 'INSUFFICIENT_CONTEXT'
  | 'INSUFFICIENT_EVIDENCE'
  | 'CAPABILITY_UNAVAILABLE'
  | 'DATASET_UNAVAILABLE'
  | 'RESOURCE_UNAVAILABLE'
  | 'PENDING_DISCOVERY';

export interface StatisticalUncertainty {
  sampleSize: number;
  standardError: number;
  confidenceLevel: number; // e.g. 0.95
  marginOfError: number;
  pValue?: number;
  statisticalPower?: number; // e.g. 0.80
}

export interface ConfidenceScoreModel {
  metricName: string;
  value?: number; // 0.0 to 1.0 (undefined if sentinel active)
  sentinelState?: ZeroFabricationSentinel;
  uncertainty?: StatisticalUncertainty;
  methodology?: string;
  sourceEvidenceId?: string;
}

export interface ConfidenceScoreProps {
  score: ConfidenceScoreModel;
  variant?: 'gauge' | 'bar' | 'compact' | 'detailed';
  showUncertaintyBounds?: boolean;
  showSampleSize?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}
