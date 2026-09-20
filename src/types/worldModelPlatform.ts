/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * TypeScript Type Definitions
 */

export type EntityDomain =
  | 'system'
  | 'process'
  | 'resource'
  | 'agent'
  | 'external_api'
  | 'database'
  | 'user_cohort'
  | 'workflow'
  | 'environment'
  | 'synthetic_scenario';

export type RelationType =
  | 'causes'
  | 'influences'
  | 'depends_on'
  | 'precedes'
  | 'inhibits'
  | 'correlates_with'
  | 'hosts'
  | 'produces'
  | 'consumes'
  | 'interacts_with';

export type TemporalFrequency =
  | 'realtime'
  | 'minutely'
  | 'hourly'
  | 'daily'
  | 'weekly'
  | 'aperiodic'
  | 'stochastic';

export type CausalStrength =
  | 'deterministic'
  | 'strong'
  | 'moderate'
  | 'weak'
  | 'spurious';

export type HypothesisStatus =
  | 'proposed'
  | 'testing'
  | 'confirmed'
  | 'refuted'
  | 'inconclusive';

export type ScenarioType =
  | 'baseline'
  | 'best_case'
  | 'worst_case'
  | 'expected'
  | 'black_swan';

export type PredictionHorizon =
  | 'immediate'
  | 'short_term'
  | 'medium_term'
  | 'long_term';

export type DecisionRiskProfile =
  | 'conservative'
  | 'balanced'
  | 'aggressive'
  | 'adversarial_resilient';

export type UncertaintyType =
  | 'epistemic'
  | 'aleatoric'
  | 'distributional'
  | 'algorithmic';

export type VerificationStatus =
  | 'verified'
  | 'refuted'
  | 'partial'
  | 'pending';

export type MemoryTier =
  | 'sensory'
  | 'working'
  | 'episodic'
  | 'semantic'
  | 'archival';

export type IntelligenceState =
  | 'observing'
  | 'fusing'
  | 'modeling'
  | 'hypothesizing'
  | 'simulating'
  | 'predicting'
  | 'optimizing'
  | 'verifying'
  | 'idle';

export interface WorldModelEvent {
  event_id: string;
  event_type: string;
  timestamp: string;
  severity: 'debug' | 'info' | 'warning' | 'error' | 'critical';
  source_subsystem: string;
  payload: Record<string, any>;
  correlation_id?: string;
}

export interface WorldObservation {
  observation_id: string;
  source: string;
  modality: string;
  raw_payload: Record<string, any>;
  signal_strength: number;
  noise_level: number;
  source_reliability: number;
  tags: string[];
  snr_ratio: number;
  novelty_score: number;
  is_processed: boolean;
  timestamp: string;
}

export interface FusedFact {
  fact_id: string;
  subject: string;
  predicate: string;
  object: string;
  confidence: number;
  source: string;
  evidence_ids: string[];
  truth_score: number;
  decay_rate: number;
  verification_count: number;
  created_at: string;
  last_reinforced_at: string;
}

export interface WorldEntity {
  entity_id: string;
  name: string;
  domain: EntityDomain;
  properties: Record<string, any>;
  state: Record<string, any>;
  confidence: number;
  created_at: string;
  updated_at: string;
}

export interface WorldRelation {
  relation_id: string;
  source_id: string;
  target_id: string;
  relation_type: RelationType;
  weight: number;
  confidence: number;
  properties: Record<string, any>;
  created_at: string;
}

export interface WorldGraphSnapshot {
  snapshot_id: string;
  timestamp: string;
  entity_count: number;
  relation_count: number;
  graph_hash: string;
  graph_entropy: number;
  trigger_reason: string;
}

export interface TemporalPattern {
  pattern_id: string;
  target_entity: string;
  frequency: TemporalFrequency;
  cycle_duration_seconds: number;
  confidence: number;
  description: string;
  first_observed: string;
  last_observed: string;
}

export interface CausalNode {
  node_id: string;
  name: string;
  domain: string;
  properties: Record<string, any>;
}

export interface CausalEdge {
  source_id: string;
  target_id: string;
  strength: CausalStrength;
  weight: number;
  mechanism: string;
}

export interface CausalGraph {
  graph_id: string;
  name: string;
  nodes: Record<string, CausalNode>;
  edges: CausalEdge[];
  updated_at: string;
}

export interface Hypothesis {
  hypothesis_id: string;
  statement: string;
  cause_entity: string;
  effect_entity: string;
  prior_probability: number;
  posterior_probability: number;
  evidence_count: number;
  status: HypothesisStatus;
  domain: EntityDomain;
  created_at: string;
  updated_at: string;
}

export interface ScenarioBranch {
  branch_id: string;
  base_snapshot_id: string;
  branch_type: ScenarioType;
  probability: number;
  time_horizon_seconds: number;
  state_divergence_delta: number;
  projected_state: Record<string, any>;
  critical_events: string[];
  created_at: string;
}

export interface CounterfactualWorld {
  simulation_id: string;
  base_snapshot_id: string;
  interventions: Record<string, any>;
  query_target: string;
  factual_outcome: any;
  counterfactual_outcome: any;
  divergence_score: number;
  causal_attribution: string;
  created_at: string;
}

export interface PredictionTrajectory {
  trajectory_id: string;
  target_metric: string;
  horizon: PredictionHorizon;
  horizon_seconds: number;
  expected_value: number;
  lower_bound_95: number;
  upper_bound_95: number;
  confidence_score: number;
  time_series_points: Array<{
    timestamp: string;
    expected: number;
    lower: number;
    upper: number;
  }>;
  causal_drivers: string[];
  created_at: string;
}

export interface DecisionOption {
  option_id: string;
  title: string;
  description: string;
  actions: Array<Record<string, any>>;
  expected_outcomes: Record<string, number>;
  expected_utility: number;
  risk_profile: DecisionRiskProfile;
  cost: number;
  time_horizon_seconds: number;
  created_at: string;
}

export interface DecisionPortfolio {
  portfolio_id: string;
  objective: string;
  selected_options: string[];
  total_cost: number;
  aggregate_utility: number;
  risk_profile: DecisionRiskProfile;
  created_at: string;
}

export interface UncertaintyAssessment {
  assessment_id: string;
  target_domain: string;
  observed_entropy: number;
  epistemic_component: number;
  aleatoric_component: number;
  confidence_level: number;
  total_uncertainty: number;
  created_at: string;
}

export interface VerificationOutcome {
  verification_id: string;
  prediction_id: string;
  actual_value: any;
  predicted_value: any;
  residual_error: number;
  status: VerificationStatus;
  calibration_weight: number;
  recorded_at: string;
}

export interface CognitiveMemoryRecord {
  record_id: string;
  tier: MemoryTier;
  content: Record<string, any>;
  importance_score: number;
  access_count: number;
  associations: string[];
  created_at: string;
  last_accessed: string;
}

export interface WorldModelExecutiveSummary {
  status: string;
  phase: string;
  name: string;
  state: IntelligenceState;
  summary: {
    runtime_status: {
      intelligence_state: IntelligenceState;
      total_cycles_executed: number;
      last_cycle_timestamp: string | null;
      uptime_seconds: number;
    };
    world_entities_count: number;
    world_relations_count: number;
    fused_facts_count: number;
    active_hypotheses_count: number;
    simulated_scenarios_count: number;
    predictive_trajectories_count: number;
    decisions_count: number;
    consolidated_memories_count: number;
    system_uncertainty: UncertaintyAssessment | null;
    recent_events_count: number;
  };
}
