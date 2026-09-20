/**
 * Autonomous Decision Intelligence Platform (ADIP)
 * Domain Types and Interfaces
 */

export interface BetaBeliefPayload {
  variable: string;
  alpha: number;
  beta: number;
  mean: number;
  variance: number;
  credible_interval_95: [number, number];
  shannon_entropy_bits: number;
  description: string;
}

export interface KalmanBeliefPayload {
  variable: string;
  state_estimate: number;
  error_covariance: number;
  process_noise: number;
  measurement_noise: number;
  shannon_entropy_bits: number;
  description: string;
}

export interface BeliefSummaryResponse {
  total_variables: number;
  total_entropy_bits: number;
  variables: Record<string, BetaBeliefPayload>;
  kalman_variables: Record<string, KalmanBeliefPayload>;
  timestamp: string;
}

export interface BayesianUpdateRequest {
  variable: string;
  successes: number;
  failures: number;
  evidence_type: string;
  source: string;
}

export interface BayesianUpdateResponse {
  variable: string;
  prior_mean: number;
  posterior_mean: number;
  prior_variance: number;
  posterior_variance: number;
  entropy_delta_bits: number;
  credible_interval_95: [number, number];
  evidence_hash: string;
  timestamp: string;
}

export interface WorldStateHorizonPayload {
  horizon_minutes: number;
  predicted_gpu_utilization: number;
  predicted_queue_depth: number;
  predicted_token_burn_velocity: number;
  predicted_budget_exhaustion_probability: number;
  confidence_interval_lower: number;
  confidence_interval_upper: number;
}

export interface WorldForecastResponse {
  horizons: Record<string, WorldStateHorizonPayload>;
  generated_at: string;
}

export interface SensingActionPayload {
  action_id: string;
  target_variable: string;
  execution_delay_sec: number;
  cost_usd: number;
  expected_variance_reduction: number;
}

export interface SensingActionRecommendation {
  action_id: string;
  target_variable: string;
  expected_information_gain_bits: number;
  expected_utility_gain: number;
  delay_penalty: number;
  net_evoi: number;
  recommended: boolean;
  scientific_rationale: string;
}

export interface EVOIResponse {
  current_system_entropy: number;
  recommendations: SensingActionRecommendation[];
  evaluated_at: string;
}

export interface MetaCritiqueResponse {
  mission_id: string;
  critic_score: number;
  suboptimality_gap: number;
  regret: {
    expected_regret: number;
    counterfactual_optimal_utility: number;
    attribution: string;
  };
  recommendations: string[];
}

export interface FormalVerificationProof {
  plan_id: string;
  verified: boolean;
  violation_count: number;
  checks: Record<string, boolean>;
  smt_solver_status: string;
  timestamp: string;
}

export interface DecisionProvenanceNode {
  node_id: string;
  step_name: string;
  timestamp: string;
  inputs: Record<string, any>;
  output: Record<string, any>;
  parent_hash?: string;
  hash_sha256: string;
}

export interface BenchmarkScore {
  planner_id: string;
  name: string;
  utility_score: number;
  brier_score: number;
  expected_calibration_error: number;
  execution_time_ms: number;
  entropy_reduction_rate: number;
}

export interface BenchmarkSuiteResponse {
  planners: BenchmarkScore[];
  winner: string;
  trial_count: number;
  evaluated_at: string;
}
