/**
 * Phase 13.17: AI Operations Types & Interfaces
 * Enterprise Agent Observability, Evaluation, Optimization & Controlled Self-Improvement.
 */

export type SpanType =
  | 'AGENT_RUN'
  | 'LLM_CALL'
  | 'TOOL_EXECUTION'
  | 'RETRIEVAL'
  | 'REASONING_STEP'
  | 'EVALUATION'
  | 'GUARDRAIL_CHECK';

export type SpanStatus = 'OK' | 'ERROR' | 'TIMEOUT' | 'CANCELLED';

export type AgentHealthStatus = 'HEALTHY' | 'DEGRADED' | 'CRITICAL' | 'OFFLINE';

export type FailureCategory =
  | 'TOOL_TIMEOUT'
  | 'TOOL_SCHEMA_VIOLATION'
  | 'RECURSIVE_LOOP'
  | 'CONTEXT_WINDOW_OVERFLOW'
  | 'CONFIDENCE_DECAY'
  | 'HALLUCINATION_DETECTED'
  | 'PII_POLICY_VIOLATION'
  | 'RATE_LIMIT_EXCEEDED'
  | 'UNSPECIFIED_RUNTIME_ERROR';

export type ModelTier =
  | 'gemini-2.0-flash-lite'
  | 'gemini-2.0-flash'
  | 'gemini-1.5-pro'
  | 'gemini-omni-1.1-flash'
  | 'local-granite-embed';

export type ProposalStatus =
  | 'DRAFT'
  | 'CANARY_TESTING'
  | 'PENDING_HITL_APPROVAL'
  | 'APPROVED'
  | 'REJECTED'
  | 'DEPLOYED'
  | 'ROLLED_BACK';

export type ExperimentStatus =
  | 'QUEUED'
  | 'RUNNING'
  | 'COMPLETED'
  | 'FAILED'
  | 'STOPPED_EARLY';

export interface Span {
  span_id: string;
  trace_id: string;
  parent_span_id?: string | null;
  name: string;
  span_type: SpanType;
  agent_id: string;
  start_time: string;
  end_time?: string | null;
  duration_ms: number;
  status: SpanStatus;
  inputs?: Record<string, any>;
  outputs?: Record<string, any>;
  metadata?: Record<string, any>;
  token_usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
  cost_usd: number;
  error_message?: string | null;
}

export interface ExecutionTrace {
  trace_id: string;
  session_id: string;
  agent_id: string;
  root_span_name: string;
  start_time: string;
  end_time?: string | null;
  total_duration_ms: number;
  status: SpanStatus;
  spans: Span[];
  total_prompt_tokens: number;
  total_completion_tokens: number;
  total_cost_usd: number;
  tags?: Record<string, string>;
}

export interface AgentTelemetry {
  agent_id: string;
  agent_name: string;
  role: string;
  version: string;
  health_status: AgentHealthStatus;
  uptime_seconds: number;
  active_invocations: number;
  total_invocations: number;
  success_rate: number;
  error_rate: number;
  avg_latency_ms: number;
  p95_latency_ms: number;
  p99_latency_ms: number;
  total_tokens_consumed: number;
  total_cost_usd: number;
  last_active: string;
  resource_utilization?: {
    cpu_pct: number;
    memory_mb: number;
  };
}

export interface MetricScore {
  metric_name: string;
  score: number;
  passed: boolean;
  threshold: number;
  confidence: number;
  details?: Record<string, any>;
}

export interface EvaluationResult {
  eval_id: string;
  trace_id?: string | null;
  agent_id: string;
  timestamp: string;
  task_success_score: number;
  accuracy_score: number;
  grounding_score: number;
  hallucination_index: number;
  safety_score: number;
  tool_efficiency_score: number;
  cost_efficiency_score: number;
  llm_judge_score: number;
  composite_quality_score: number;
  status: string;
  metrics: MetricScore[];
  judge_critique?: string | null;
}

export interface FailureAnalysisResult {
  analysis_id: string;
  trace_id: string;
  agent_id: string;
  category: FailureCategory;
  root_cause_summary: string;
  failing_span_id?: string | null;
  critical_path: string[];
  confidence: number;
  suggested_remediation: string;
  timestamp: string;
}

export interface ModelRouteDecision {
  decision_id: string;
  task_id: string;
  selected_model: string;
  selected_tier: ModelTier;
  estimated_cost_usd: number;
  estimated_latency_ms: number;
  estimated_quality_score: number;
  pareto_score: number;
  weights: {
    quality: number;
    latency: number;
    cost: number;
  };
  fallback_models: string[];
  timestamp: string;
}

export interface PromptVersion {
  prompt_id: string;
  version: string;
  agent_id: string;
  system_instruction: string;
  few_shot_examples?: Array<{ input: string; output: string }>;
  active: boolean;
  average_score: number;
  created_at: string;
  created_by: string;
  mutation_notes?: string | null;
}

export interface ImprovementProposal {
  proposal_id: string;
  target_agent_id: string;
  title: string;
  description: string;
  proposal_type: string;
  status: ProposalStatus;
  proposed_changes: Record<string, any>;
  diff_summary: string;
  expected_quality_delta: number;
  expected_latency_delta_ms: number;
  expected_cost_delta_pct: number;
  experiment_id?: string | null;
  created_at: string;
  approved_by?: string | null;
  approved_at?: string | null;
  rejection_reason?: string | null;
}

export interface ExperimentRecord {
  experiment_id: string;
  name: string;
  agent_id: string;
  control_version: string;
  candidate_version: string;
  sample_size: number;
  control_success_rate: number;
  candidate_success_rate: number;
  control_avg_latency_ms: number;
  candidate_avg_latency_ms: number;
  control_avg_cost_usd: number;
  candidate_avg_cost_usd: number;
  p_value: number;
  effect_size_cohen_d: number;
  statistically_significant: boolean;
  status: ExperimentStatus;
  started_at: string;
  completed_at?: string | null;
}

export interface GovernanceAuditRecord {
  audit_id: string;
  timestamp: string;
  event_type: string;
  actor: string;
  agent_id?: string | null;
  action_summary: string;
  compliance_passed: boolean;
  pii_detected: boolean;
  pii_types_redacted: string[];
  policy_name?: string | null;
  signature_hash: string;
}

export interface OperationsOverview {
  total_agents: number;
  healthy_agents: number;
  degraded_agents: number;
  critical_agents: number;
  fleet_health_score: number;
  total_invocations: number;
  mean_fleet_latency_ms: number;
  mean_fleet_error_rate: number;
  total_tokens_consumed: number;
  total_cost_usd: number;
  sla_compliance_pct: number;
  timestamp: string;
}
