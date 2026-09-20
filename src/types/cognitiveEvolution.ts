/**
 * Autonomous Cognitive Evolution Platform (ACOS)
 * TypeScript Domain Types & Interfaces
 */

export interface PrimitiveOperatorNodePayload {
  node_id: string;
  name: string;
  operator_type: string;
  inputs: string[];
  outputs: string[];
  estimated_latency_ms: number;
  estimated_cost_usd: number;
  failure_probability: number;
}

export interface SynthesizedDAGPayload {
  dag_id: string;
  goal_intent: string;
  nodes: Record<string, PrimitiveOperatorNodePayload>;
  adjacency: Record<string, string[]>;
  critical_path_ms: number;
  total_estimated_cost_usd: number;
  structural_depth: number;
  parallelism_width: number;
}

export interface StrategyEvaluationReportPayload {
  dag_id: string;
  novelty_score: number;
  structural_similarity_pct: number;
  graph_edit_distance: number;
  expected_utility: number;
  pareto_fitness_rank: number;
  summary: string;
}

export interface SynthesizedStrategyRecordPayload {
  strategy_id: string;
  dag: SynthesizedDAGPayload;
  evaluation: StrategyEvaluationReportPayload;
  parent_strategy_id?: string;
  created_at_generation: number;
  average_actual_utility: number;
}

export interface MutationResultPayload {
  mutation_id: string;
  original_dag_id: string;
  mutated_dag: SynthesizedDAGPayload;
  mutation_type: string;
  nodes_altered: string[];
  novelty_delta: number;
}

export interface PlannerGenerationPayload {
  generation_id: string;
  version_tag: string;
  parent_version?: string;
  parameters: Record<string, any>;
  benchmark_utility: number;
  brier_score: number;
  simulated_trials_count: number;
  is_active_canary: boolean;
  is_promoted_production: boolean;
  cryptographic_seal_hash: string;
  timestamp: string;
}

export interface EvolutionCycleReportPayload {
  cycle_id: string;
  detected_weakness: string;
  previous_version: string;
  candidate_version: string;
  simulated_trials: number;
  utility_gain_pct: number;
  brier_improvement_pct: number;
  is_promoted: boolean;
  rationale: string;
}

export interface DigitalTwinClusterReportPayload {
  simulation_id: string;
  total_virtual_workers: number;
  simulated_duration_sec: number;
  processed_missions_count: number;
  p50_latency_ms: number;
  p95_latency_ms: number;
  p99_latency_ms: number;
  queue_overflow_count: number;
  average_gpu_utilization_pct: number;
  total_simulated_tokens: number;
  resilience_score: number;
}

export interface CausalNodePayload {
  node_id: string;
  name: string;
  description: string;
  is_treatment: boolean;
  is_outcome: boolean;
  is_confounder: boolean;
  parents: string[];
  base_value: number;
}

export interface InterventionResultPayload {
  intervention_query: string;
  treatment_variable: string;
  treatment_value: number;
  target_outcome_variable: string;
  observational_expectation_e_y: number;
  interventional_expectation_e_y_do_x: number;
  causal_effect_ate: number;
  confounder_backdoor_set: string[];
  formula_provenance: string;
  summary: string;
}

export interface CouncilAgentVotePayload {
  agent_id: string;
  agent_role: string;
  preferred_strategy_id: string;
  strategy_rankings: string[];
  advocacy_argument: string;
  confidence_weight: number;
}

export interface DeliberationSessionSummaryPayload {
  session_id: string;
  mission_id: string;
  participating_agents: string[];
  agent_arguments: CouncilAgentVotePayload[];
  voting_tally: {
    winning_strategy_id: string;
    borda_points: Record<string, number>;
    first_choice_votes: Record<string, number>;
    consensus_entropy_bits: number;
    is_unanimous: boolean;
    deliberation_verdict: string;
  };
  resource_auctions: {
    auction_id: string;
    task_id: string;
    winning_agent_id: string;
    clearing_price_credits: number;
  }[];
  final_ratified_strategy_id: string;
  timestamp: string;
}
