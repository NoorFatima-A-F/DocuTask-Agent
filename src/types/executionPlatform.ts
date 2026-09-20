/**
 * Phase 13.15: Autonomous Real-World Execution Platform (ARWE-UTOCOP) Type Definitions.
 */

export type ToolType =
  | 'rest_api'
  | 'graphql'
  | 'grpc'
  | 'database'
  | 'cloud_sdk'
  | 'cli'
  | 'browser'
  | 'saas'
  | 'kubernetes'
  | 'cyber_physical'
  | 'custom';

export type ToolStatus = 'active' | 'degraded' | 'offline' | 'maintenance' | 'deprecated';

export type ConnectorCategory =
  | 'cloud'
  | 'database'
  | 'communication'
  | 'code_repository'
  | 'crm_erp'
  | 'infrastructure'
  | 'payment_finance'
  | 'browser_vision'
  | 'custom_api';

export type ConnectorStatus = 'connected' | 'disconnected' | 'authenticating' | 'error' | 'rate_limited';

export type MissionStatus =
  | 'draft'
  | 'planning'
  | 'validating'
  | 'simulating'
  | 'awaiting_approval'
  | 'executing'
  | 'verifying'
  | 'completed'
  | 'failed'
  | 'compensating'
  | 'rolled_back'
  | 'cancelled';

export type StepStatus =
  | 'pending'
  | 'running'
  | 'simulated'
  | 'success'
  | 'failed'
  | 'skipped'
  | 'compensating'
  | 'compensated';

export type RiskLevel = 'minimal' | 'low' | 'medium' | 'high' | 'critical';

export type PolicyDecision = 'allow' | 'deny' | 'require_approval' | 'require_simulation';

export type CredentialType =
  | 'api_key'
  | 'bearer_token'
  | 'oauth2'
  | 'mutual_tls'
  | 'ssh_key'
  | 'aws_iam'
  | 'gcp_adc'
  | 'vault_secret';

export interface ToolParameter {
  name: string;
  param_type: string;
  description: string;
  required: boolean;
  default?: any;
  enum_values?: string[];
  validation_regex?: string;
}

export interface ToolDefinition {
  tool_id: string;
  name: string;
  version: string;
  description: string;
  tool_type: ToolType;
  category: string;
  parameters: ToolParameter[];
  output_schema: Record<string, any>;
  rate_limit_per_min: number;
  timeout_seconds: number;
  concurrency_limit: number;
  risk_level: RiskLevel;
  requires_approval: boolean;
  is_idempotent: boolean;
  supports_compensation: boolean;
  compensation_tool_id?: string;
  tags: string[];
  status: ToolStatus;
  health_score: number;
  total_calls: number;
  successful_calls: number;
  failed_calls: number;
  average_latency_ms: number;
  created_at: string;
  updated_at: string;
}

export interface ConnectorConfig {
  connector_id: string;
  name: string;
  category: ConnectorCategory;
  protocol: string;
  endpoint_url: string;
  credential_id?: string;
  status: ConnectorStatus;
  health_score: number;
  latency_ms: number;
  rate_limit_rpm: number;
  rpm_used: number;
  max_concurrency: number;
  active_connections: number;
  metadata: Record<string, any>;
  last_health_check: string;
  created_at: string;
}

export interface BrowserAction {
  action_id: string;
  action_type: string;
  selector?: string;
  value?: string;
  timeout_ms: number;
  status: string;
  result_data?: Record<string, any>;
  screenshot_ref?: string;
  executed_at?: string;
}

export interface BrowserSession {
  session_id: string;
  user_agent: string;
  viewport_width: number;
  viewport_height: number;
  current_url: string;
  page_title: string;
  dom_elements_count: number;
  cookies_count: number;
  actions_count: number;
  is_active: boolean;
  created_at: string;
  last_activity: string;
}

export interface WorkflowStep {
  step_id: string;
  name: string;
  tool_id: string;
  inputs: Record<string, any>;
  depends_on: string[];
  condition?: string;
  status: StepStatus;
  retry_count: number;
  max_retries: number;
  timeout_seconds: number;
  output?: Record<string, any>;
  error?: string;
  is_compensable: boolean;
  compensation_tool_id?: string;
  compensation_inputs: Record<string, any>;
  started_at?: string;
  completed_at?: string;
  duration_ms: number;
}

export interface WorkflowDefinition {
  workflow_id: string;
  name: string;
  description: string;
  mode: string;
  steps: WorkflowStep[];
  variables: Record<string, any>;
  risk_level: RiskLevel;
  created_at: string;
  updated_at: string;
}

export interface PlannedStepNode {
  step_id: string;
  tool_id: string;
  name: string;
  estimated_duration_ms: number;
  risk_level: RiskLevel;
  early_start: number;
  early_finish: number;
  late_start: number;
  late_finish: number;
  slack: number;
  is_critical_path: boolean;
  contingency_step_id?: string;
}

export interface ExecutionPlan {
  plan_id: string;
  mission_goal: string;
  workflow_id: string;
  nodes: PlannedStepNode[];
  total_estimated_duration_ms: number;
  critical_path_steps: string[];
  overall_risk: RiskLevel;
  created_at: string;
}

export interface CredentialRecord {
  credential_id: string;
  name: string;
  cred_type: CredentialType;
  target_system: string;
  scopes: string[];
  masked_value: string;
  is_active: boolean;
  expires_at?: string;
  last_rotated: string;
  created_at: string;
}

export interface PolicyRule {
  rule_id: string;
  name: string;
  description: string;
  target_tools: string[];
  condition_expression: string;
  decision: PolicyDecision;
  risk_level: RiskLevel;
  requires_simulation: boolean;
  is_active: boolean;
}

export interface ApprovalRequest {
  approval_id: string;
  mission_id: string;
  step_id: string;
  tool_id: string;
  requester: string;
  risk_level: RiskLevel;
  reason: string;
  status: 'pending' | 'approved' | 'rejected';
  approver?: string;
  decision_timestamp?: string;
  created_at: string;
}

export interface SimulatedStepResult {
  step_id: string;
  tool_id: string;
  status: StepStatus;
  predicted_duration_ms: number;
  predicted_cost_usd: number;
  state_mutations_predicted: string[];
  simulated_output: Record<string, any>;
  can_compensate: boolean;
  compensation_rehearsal_passed: boolean;
  risk_score: number;
}

export interface SimulationReport {
  simulation_id: string;
  workflow_id: string;
  total_steps: number;
  step_results: SimulatedStepResult[];
  total_predicted_duration_ms: number;
  total_predicted_cost_usd: number;
  blast_radius_scope: string;
  simulation_passed: boolean;
  rehearsal_errors: string[];
  created_at: string;
}

export interface VerificationCheck {
  check_id: string;
  name: string;
  target_resource: string;
  expected_condition: string;
  actual_condition: string;
  passed: boolean;
  evidence: Record<string, any>;
  checked_at: string;
}

export interface VerificationCertificate {
  certificate_id: string;
  mission_id: string;
  step_id: string;
  tool_id: string;
  passed: boolean;
  checks: VerificationCheck[];
  state_signature_sha256: string;
  verified_at: string;
}

export interface CompensationStepRecord {
  compensation_id: string;
  original_step_id: string;
  tool_id: string;
  compensation_tool_id: string;
  status: StepStatus;
  inputs: Record<string, any>;
  output?: Record<string, any>;
  error?: string;
  executed_at?: string;
}

export interface RollbackSession {
  rollback_id: string;
  mission_id: string;
  trigger_reason: string;
  steps_to_compensate: CompensationStepRecord[];
  status: 'pending' | 'executing' | 'completed' | 'failed';
  completed_compensations: number;
  failed_compensations: number;
  started_at: string;
  completed_at?: string;
}

export interface AnomalyAlert {
  alert_id: string;
  target_component: string;
  metric_name: string;
  severity: 'warning' | 'critical' | 'emergency';
  threshold_value: number;
  observed_value: number;
  description: string;
  is_resolved: boolean;
  detected_at: string;
}

export interface SystemTelemetrySnapshot {
  timestamp: string;
  total_executions_24h: number;
  success_rate_percentage: number;
  avg_latency_ms: number;
  active_connectors: number;
  active_browser_sessions: number;
  open_anomalies: number;
  sla_compliance_score: number;
}

export interface AuditEntry {
  entry_id: string;
  mission_id: string;
  step_id?: string;
  tool_id?: string;
  action_type: string;
  actor: string;
  risk_level: RiskLevel;
  payload_summary: Record<string, any>;
  prev_hash: string;
  hash_signature: string;
  timestamp: string;
}

export interface MissionExecution {
  mission_id: string;
  goal: string;
  workflow_id: string;
  status: MissionStatus;
  context_variables: Record<string, any>;
  steps: WorkflowStep[];
  risk_level: RiskLevel;
  initiated_by: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  total_execution_time_ms: number;
  error_message?: string;
}

export interface ExecutionPlatformOverview {
  system_status: string;
  autonomous_mode: string;
  total_tools: number;
  active_tools: number;
  total_connectors: number;
  connected_count: number;
  total_missions: number;
  completed_missions: number;
  failed_missions: number;
  active_browser_sessions: number;
  total_plans: number;
  active_policy_rules: number;
  pending_approvals: number;
  total_rollbacks: number;
  audit_ledger_integrity: boolean;
  telemetry: SystemTelemetrySnapshot;
}
