/**
 * Autonomous Planning Operating System Domain Types for DocuTask Agent.
 */

export type StrategyArchetype = 'ALPHA_FAST' | 'BETA_ACCURATE' | 'GAMMA_COST' | 'DELTA_PARETO';

export type DAGNodeStatus = 'PENDING' | 'SCHEDULED' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'RETRYING' | 'MUTATED' | 'BYPASSED';

export type DAGMutationType = 'NODE_SPLIT' | 'NODE_MERGE' | 'NODE_CLONE' | 'NODE_RETRY' | 'NODE_REPLACE' | 'BRANCH_INSERT' | 'BRANCH_PRUNE' | 'DEPENDENCY_REWIRE';

export interface StrategyStep {
  step_id: string;
  objective_id: string;
  name: string;
  capability_id: string;
  provider: string;
  estimated_latency_ms: number;
  estimated_cost_usd: number;
  estimated_accuracy: number;
  failure_probability: number;
  parallel_group?: number;
  fallback_capability_id?: string;
}

export interface CandidateStrategy {
  strategy_id: string;
  archetype: StrategyArchetype;
  name: string;
  description: string;
  mission_id: string;
  steps: StrategyStep[];
  concurrency_level: number;
  estimated_total_latency_ms: number;
  estimated_critical_path_ms: number;
  estimated_total_cost_usd: number;
  estimated_accuracy: number;
  estimated_risk_score: number;
  token_estimate: number;
  is_pareto_optimal: boolean;
  constraint_compliance: {
    is_valid: boolean;
    violations: string[];
    soft_penalty: number;
  };
  rationale: string;
  created_at: string;
}

export interface StrategyComparisonEntry {
  strategy_id: string;
  archetype: string;
  name: string;
  rank: number;
  utility_score: number;
  accuracy: number;
  critical_path_ms: number;
  total_cost_usd: number;
  risk_score: number;
  token_estimate: number;
  is_pareto_optimal: boolean;
  is_valid: boolean;
  violations: string[];
  rejection_reason?: string;
}

export interface StrategyComparisonMatrix {
  mission_id: string;
  entries: StrategyComparisonEntry[];
  pareto_frontier_strategy_ids: string[];
  selected_strategy_id: string;
  version: string;
}

export interface UtilityWeights {
  w_accuracy: number;
  w_latency: number;
  w_cost: number;
  w_risk: number;
  w_memory: number;
  w_satisfaction: number;
}

export interface UtilityScore {
  strategy_id: string;
  total_utility: number;
  accuracy_term: number;
  latency_penalty_term: number;
  cost_penalty_term: number;
  risk_penalty_term: number;
  memory_bonus_term: number;
  satisfaction_bonus_term: number;
  soft_constraint_penalty: number;
  raw_accuracy: number;
  normalized_latency: number;
  normalized_cost: number;
  raw_risk: number;
  weights: UtilityWeights;
  equation: string;
  version: string;
}

export interface CounterfactualExplanation {
  query_type: string;
  target_strategy_id?: string;
  summary_explanation: string;
  algebraic_proof: string;
  tipping_point?: {
    parameter: string;
    current_value: number;
    tipping_threshold: number;
    condition: string;
  };
  alternative_ranking?: Array<{
    strategy_id: string;
    name: string;
    archetype: string;
    new_utility: number;
  }>;
  version: string;
}

export interface DAGNode {
  node_id: string;
  name: string;
  capability_id: string;
  provider: string;
  status: DAGNodeStatus;
  retry_count: number;
  max_retries: number;
  timeout_ms: number;
  payload: Record<string, any>;
  output?: Record<string, any>;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  metadata: Record<string, any>;
}

export interface DAGEdge {
  edge_id: string;
  source_id: string;
  target_id: string;
  condition?: string;
  edge_type: string;
}

export interface DAGMutationRecord {
  mutation_id: string;
  timestamp: string;
  mutation_type: DAGMutationType;
  target_node_id?: string;
  rationale: string;
  diff_summary: string;
  applied_by: string;
}

export interface MutableExecutionDAG {
  dag_id: string;
  mission_id: string;
  strategy_id: string;
  nodes: Record<string, DAGNode>;
  edges: DAGEdge[];
  mutation_history: DAGMutationRecord[];
  version: number;
  created_at: string;
}

export interface WorkerLease {
  lease_id: string;
  worker_id: string;
  mission_id: string;
  step_id: string;
  capability_id: string;
  priority: number;
  leased_at: string;
  expires_at_epoch: number;
  is_active: boolean;
  preempted: boolean;
}

export interface SchedulerClusterStatus {
  total_workers: number;
  idle_workers: number;
  busy_workers: number;
  utilization_pct: number;
  queue_depth: number;
  active_leases_count: number;
  active_leases: WorkerLease[];
}

export interface ExpectedVsActual {
  predicted_latency_ms: number;
  actual_latency_ms: number;
  latency_delta_ms: number;
  latency_error_pct: number;
  predicted_cost_usd: number;
  actual_cost_usd: number;
  cost_delta_usd: number;
  cost_error_pct: number;
  predicted_accuracy: number;
  actual_accuracy: number;
  accuracy_delta: number;
  predicted_risk_score: number;
  actual_failure_occurred: boolean;
}

export interface PlanCalibrationMetric {
  calibration_id: string;
  mission_id: string;
  strategy_id: string;
  comparison: ExpectedVsActual;
  overall_calibration_score: number;
  root_causes: string[];
  tuning_recommendations: Record<string, string>;
  timestamp: string;
}

export interface MissionPlanResult {
  mission_id: string;
  goal_graph: any;
  constraint_set: any;
  candidate_strategies: CandidateStrategy[];
  selection_record: {
    selected_strategy_id: string;
    selected_archetype: string;
    selection_rationale: string;
    rejection_reasons: Record<string, string>;
    comparison_matrix: StrategyComparisonMatrix;
    utility_breakdown: UtilityScore;
  };
  selected_dag: MutableExecutionDAG;
  simulations: Record<string, any>;
  cost_predictions: Record<string, any>;
  latency_predictions: Record<string, any>;
  risk_profiles: Record<string, any>;
  counterfactual_explanations: CounterfactualExplanation[];
}
