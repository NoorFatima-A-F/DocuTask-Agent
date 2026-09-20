/**
 * TypeScript Type Definitions for Phase 13.13 (ASEAORIP)
 * Autonomous Self-Evolution, Architecture Optimization & Recursive Improvement Platform
 */

export interface ExecutiveSummaryPayload {
  platform_version: string;
  composite_health_score: number;
  architecture_health: string;
  active_diagnoses_count: number;
  discovered_capability_gaps: number;
  pareto_optimal_candidates: number;
  total_mutation_proposals: number;
  total_simulations_conducted: number;
  total_benchmarks_completed: number;
  governance_snapshots_stored: number;
  active_deployments: number;
  completed_evolution_cycles: number;
  node_count: number;
  edge_count: number;
}

export interface PlatformHealthSnapshotPayload {
  snapshot_id: string;
  timestamp: string;
  cpu_utilization_pct: number;
  memory_usage_mb: number;
  memory_utilization_pct: number;
  memory_fragmentation_pct: number;
  gpu_utilization_pct: number;
  token_waste_rate: number;
  latency_p50_ms: number;
  latency_p95_ms: number;
  latency_p99_ms: number;
  cost_per_1k_operations_usd: number;
  throughput_qps: number;
  cache_hit_rate: number;
  queue_saturation_pct: number;
  agent_utilization_pct: number;
  event_bus_saturation_pct: number;
  health_grade: string;
  health_status: string;
  composite_health_score: number;
  active_bottlenecks: string[];
}

export interface WeaknessDiagnosisPayload {
  diagnosis_id: string;
  subsystem: string;
  title: string;
  severity: string;
  root_cause: string;
  empirical_evidence_ids: string[];
  remediation_proposal: string;
  impact_factor: number;
  diagnosed_at: string;
}

export interface CapabilityDescriptorPayload {
  capability_id: string;
  name: string;
  domain: string;
  description: string;
  maturity_level: string;
  state: string;
  is_gap: boolean;
  gap_rationale: string;
  redundancy_source_id: string | null;
  efficiency_score: number;
  accuracy_score: number;
  latency_ms: number;
  cost_per_invocation: number;
  discovered_at: string;
}

export interface ArchitectureNodePayload {
  node_id: string;
  name: string;
  subsystem: string;
  component_type: string;
  complexity_score: number;
  afferent_coupling: number;
  efferent_coupling: number;
  health_status: string;
}

export interface ArchitectureEdgePayload {
  edge_id: string;
  source_node_id: string;
  target_node_id: string;
  interaction_type: string;
  weight_qps: number;
  latency_overhead_ms: number;
}

export interface ArchitectureTopologyPayload {
  node_count: number;
  edge_count: number;
  average_complexity: number;
  total_internal_qps: number;
  nodes: ArchitectureNodePayload[];
  edges: ArchitectureEdgePayload[];
}

export interface ArchitectureImprovementPlanPayload {
  plan_id: string;
  title: string;
  target_subsystems: string[];
  action_type: string;
  rationale: string;
  expected_coupling_reduction: number;
  expected_latency_gain_pct: number;
  status: string;
  created_at: string;
}

export interface OptimizationCandidatePayload {
  candidate_id: string;
  target_subsystem: string;
  objective: string;
  hyperparameters: Record<string, any>;
  pareto_rank: number;
  fitness_score: number;
  estimated_risk: number;
  expected_gain_pct: number;
  mathematical_proof: string;
  status: string;
  created_at: string;
}

export interface ArchitectureMutationProposalPayload {
  mutation_id: string;
  title: string;
  mutation_type: string;
  target_components: string[];
  code_diff_spec: string;
  rationale: string;
  safety_analysis: string;
  confidence_score: number;
  status: string;
  sha256_hash: string;
  created_at: string;
}

export interface BenchmarkComparisonPayload {
  comparison_id: string;
  baseline_version: string;
  candidate_version: string;
  mutation_id: string | null;
  test_cases_run: number;
  baseline_latency_p95: number;
  candidate_latency_p95: number;
  baseline_token_cost: number;
  candidate_token_cost: number;
  baseline_accuracy: number;
  candidate_accuracy: number;
  improvement_score_pct: number;
  regression_detected: boolean;
  safety_compliance_score: number;
  status: string;
  created_at: string;
}

export interface SimulationReportPayload {
  simulation_id: string;
  mutation_id: string | null;
  simulation_mode: string;
  traces_replayed: number;
  success_rate: number;
  error_rate: number;
  chaos_resilience_score: number;
  safety_invariant_violations: number;
  verified_safe: boolean;
  stability_confidence: number;
  execution_notes: string;
  created_at: string;
}

export interface EvolutionGovernanceReviewPayload {
  review_id: string;
  mutation_id: string;
  candidate_id: string | null;
  risk_level: string;
  formal_verification_passed: boolean;
  simulation_verified: boolean;
  benchmark_verified: boolean;
  human_override_required: boolean;
  approval_status: string;
  reviewer_agent_id: string;
  cryptographic_signature: string;
  rollback_snapshot_id: string | null;
  created_at: string;
}

export interface RollbackSnapshotPayload {
  snapshot_id: string;
  platform_version: string;
  sha256_seal: string;
  created_at: string;
}

export interface DeploymentRecordPayload {
  deployment_id: string;
  mutation_id: string;
  target_version: string;
  deployment_state: string;
  canary_traffic_pct: number;
  live_p95_latency_ms: number;
  live_error_rate: number;
  auto_rollback_latency_threshold_ms: number;
  auto_rollback_error_threshold: number;
  rollback_snapshot_id: string | null;
  deployed_at: string;
}

export interface EvolutionCycleResultPayload {
  cycle_id: string;
  target_subsystem: string;
  objective: string;
  stage: string;
  health_score_before: number;
  health_score_after: number;
  diagnosis_count: number;
  capability_gaps_found: number;
  candidate_id: string;
  mutation_id: string;
  simulation_verified: boolean;
  benchmark_improvement_pct: number;
  governance_approved: boolean;
  deployment_state: string;
  started_at: string;
  completed_at: string;
}

export interface PlatformGenomePayload {
  genome_id: string;
  version: string;
  architecture_nodes: ArchitectureNodePayload[];
  capabilities: CapabilityDescriptorPayload[];
  pareto_candidates: OptimizationCandidatePayload[];
  active_proposals: ArchitectureMutationProposalPayload[];
  rollback_snapshots: RollbackSnapshotPayload[];
  timestamp: string;
}
