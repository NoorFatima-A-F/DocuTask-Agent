/**
 * Scientific Metric Provenance & Runtime Intelligence TypeScript Domain Types
 */

export interface MetricDefinitionData {
  id: string;
  name: string;
  description: string;
  category: string;
  formula_id: string;
  formula_expression: string;
  formula_latex: string;
  required_events: string[];
  variables: string[];
  aggregation_type: string;
  unit: string;
  minimum_sample_size: number;
  confidence_level: number;
  version: string;
  tags: string[];
  is_zero_trust_validated: boolean;
}

export interface StatisticalSummaryData {
  sample_size: number;
  mean: number;
  median: number;
  mode: number | null;
  variance: number;
  standard_deviation: number;
  standard_error: number;
  min_value: number;
  max_value: number;
  p50: number;
  p90: number;
  p95: number;
  p99: number;
  confidence_interval_95: [number, number];
  margin_of_error_95: number;
  distribution_model: string;
}

export interface MetricProvenanceRecordData {
  metric_id: string;
  metric_name: string;
  metric_version: string;
  value: any;
  formatted_value: string;
  unit: string;
  formula_id: string;
  formula_expression: string;
  formula_latex: string;
  variables_used: Record<string, any>;
  raw_event_ids: string[];
  sample_size: number;
  observation_window: {
    start_utc?: string;
    end_utc?: string;
    duration_seconds: number;
    event_count?: number;
  };
  statistical_summary: StatisticalSummaryData | null;
  merkle_events_root_sha256: string;
  calculated_at_utc: string;
  sentinel_state: string | null;
  tags: string[];
}

export interface EvidenceSignalData {
  source_name: string;
  category: string;
  observed_score: number;
  sample_size: number;
  reliability_coefficient: number;
  description: string;
  sha256_digest?: string;
  sentinel_state?: string | null;
}

export interface BayesianConfidenceResultData {
  posterior_confidence: number;
  prior_confidence: number;
  log_odds_delta: number;
  confidence_interval_95: [number, number];
  sample_size_total: number;
  signals: EvidenceSignalData[];
  signal_weights: Record<string, number>;
  log_likelihood_ratios: Record<string, number>;
  is_sentinel_active: boolean;
  sentinel_reason: string | null;
  derivation_formula: string;
  derivation_latex: string;
}

export interface ReplayStepDiffData {
  mission_id: string;
  step_a: number;
  step_b: number;
  snapshot_a: Record<string, any>;
  snapshot_b: Record<string, any>;
  delta_completed_tasks: string[];
  delta_running_tasks: string[];
  delta_agent_states: Record<string, [string, string]>;
  delta_confidence: number;
  delta_evidence_count: number;
  delta_memory_count: number;
  delta_tokens: number;
  delta_cost_usd: number;
  intermediate_events: any[];
  total_duration_between_steps_ms: number;
}

export interface TraceSpanData {
  span_id: string;
  trace_id: string;
  parent_span_id: string | null;
  event_id: string;
  event_type: string;
  agent_id: string | null;
  worker_id: string | null;
  timestamp: string;
  duration_ms: number;
  status: string;
  payload: Record<string, any>;
  children: TraceSpanData[];
}

export interface TraceTreeData {
  trace_id: string;
  root_spans: TraceSpanData[];
  total_spans: number;
  total_duration_ms: number;
  critical_path_ms: number;
}
