/**
 * Phase 13.19: Enterprise Business Platform Types
 * Enterprise Process Intelligence & Autonomous Business Orchestration Platform (EPI-ABOP).
 */

export type StepType =
  | 'TASK'
  | 'GATEWAY_EXCLUSIVE'
  | 'GATEWAY_PARALLEL'
  | 'HUMAN_APPROVAL'
  | 'TIMER'
  | 'EVENT_TRIGGER'
  | 'SUBPROCESS';

export type StepStatus =
  | 'PENDING'
  | 'RUNNING'
  | 'WAITING_APPROVAL'
  | 'COMPLETED'
  | 'FAILED'
  | 'SKIPPED';

export type ProcessStatus =
  | 'DRAFT'
  | 'ACTIVE'
  | 'RUNNING'
  | 'PAUSED'
  | 'COMPLETED'
  | 'FAILED';

export type ApprovalStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'DELEGATED';

export type GoalStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'ACHIEVED' | 'AT_RISK' | 'BLOCKED';

export interface ProcessStep {
  step_id: string;
  name: string;
  step_type: StepType;
  department_id: string;
  assigned_role: string;
  status: StepStatus;
  next_steps: string[];
  condition_expr?: string | null;
  inputs?: Record<string, any>;
  outputs?: Record<string, any>;
  sla_seconds: number;
  execution_duration_sec: number;
  error_message?: string | null;
}

export interface BusinessProcess {
  process_id: string;
  title: string;
  description: string;
  owner_department: string;
  status: ProcessStatus;
  steps: ProcessStep[];
  variables: Record<string, any>;
  current_step_ids: string[];
  created_at: string;
  updated_at: string;
  completed_at?: string | null;
}

export interface Department {
  department_id: string;
  name: string;
  head_role: string;
  parent_department_id?: string | null;
  members_count: number;
  active_processes_count: number;
  operational_budget_monthly: number;
}

export interface EmployeeOrAgentRole {
  role_id: string;
  title: string;
  department_id: string;
  is_autonomous_agent: boolean;
  approval_limit_amount: number;
  assigned_capabilities: string[];
}

export interface EnterpriseSystem {
  system_id: string;
  name: string;
  system_type: string;
  status: string;
  connected_departments: string[];
}

export interface OrganizationGraph {
  departments: Department[];
  roles: EmployeeOrAgentRole[];
  systems: EnterpriseSystem[];
  approval_matrix: Record<string, string>;
}

export interface OKRKeyResult {
  kr_id: string;
  description: string;
  target_value: number;
  current_value: number;
  unit: string;
  achieved: boolean;
}

export interface BusinessGoal {
  goal_id: string;
  title: string;
  category: string;
  target_department: string;
  status: GoalStatus;
  progress_pct: number;
  key_results: OKRKeyResult[];
  aligned_process_ids: string[];
  created_at: string;
}

export interface DecisionRule {
  rule_id: string;
  rule_name: string;
  condition_expression: string;
  action_decision: string;
  priority: number;
  enabled: boolean;
}

export interface DecisionTable {
  table_id: string;
  name: string;
  rules: DecisionRule[];
}

export interface SLAContract {
  sla_id: string;
  process_id: string;
  target_turnaround_sec: number;
  warning_threshold_pct: number;
  escalation_role: string;
}

export interface SLABreachRisk {
  process_id: string;
  step_id: string;
  elapsed_sec: number;
  sla_target_sec: number;
  breach_probability: number;
  is_breached: boolean;
  escalated: boolean;
}

export interface HumanApprovalTask {
  task_id: string;
  process_id: string;
  step_id: string;
  title: string;
  description: string;
  department_id: string;
  assigned_role: string;
  amount?: number | null;
  status: ApprovalStatus;
  decision_rationale?: string | null;
  decided_by?: string | null;
  created_at: string;
  decided_at?: string | null;
}

export interface DiscoveredProcess {
  discovered_id: string;
  name: string;
  frequency: number;
  mean_duration_sec: number;
  variants_count: number;
  bottleneck_steps: string[];
  compliance_score: number;
}

export interface ProcessOptimizationRecommendation {
  recommendation_id: string;
  process_id: string;
  title: string;
  action_type: string;
  rationale: string;
  estimated_cycle_time_reduction_pct: number;
  estimated_annual_savings_usd: number;
  confidence: number;
}

export interface ProcessSimulationConfig {
  process_id: string;
  simulated_transactions_count: number;
  agent_concurrency?: number;
  human_approval_delay_mean_sec?: number;
}

export interface SimulationResult {
  simulation_id: string;
  process_id: string;
  baseline_cycle_time_sec: number;
  optimized_cycle_time_sec: number;
  baseline_cost_usd: number;
  optimized_cost_usd: number;
  cost_reduction_usd: number;
  throughput_increase_pct: number;
  simulated_at: string;
}

export interface KPIDefinition {
  kpi_id: string;
  name: string;
  department: string;
  current_value: number;
  benchmark_value: number;
  unit: string;
  trend: 'IMPROVING' | 'STABLE' | 'DECLINING';
}

export interface DigitalTwinOrgState {
  total_departments: number;
  active_human_workers: number;
  active_agent_workers: number;
  running_business_processes: number;
  pending_approvals: number;
  mean_org_sla_compliance_pct: number;
  department_workloads: Record<string, number>;
  timestamp: string;
}

export interface BusinessExecutiveOverview {
  platform_name: string;
  total_active_processes: number;
  total_human_approvals_pending: number;
  total_goals_tracked: number;
  total_annualized_savings_usd: number;
  mean_sla_compliance_pct: number;
  mean_automation_rate_pct: number;
  top_bottlenecks: string[];
  timestamp: string;
}
