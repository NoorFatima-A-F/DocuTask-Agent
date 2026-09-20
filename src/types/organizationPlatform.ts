/**
 * Phase 13.14 - Autonomous AI Organization, Multi-Agent Enterprise Governance & Mission Execution Platform (AAO-MAGEMEP)
 * TypeScript Domain Definitions
 */

export type OrganizationState =
  | 'CREATED'
  | 'PLANNING'
  | 'EXECUTING'
  | 'OPTIMIZING'
  | 'PAUSED'
  | 'FAILED'
  | 'COMPLETED'
  | 'ARCHIVED';

export type MissionPriority = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'EXPERIMENTAL';

export type AgentRoleType =
  | 'CEO_AGENT'
  | 'CTO_AGENT'
  | 'RESEARCH_AGENT'
  | 'ENGINEERING_AGENT'
  | 'ANALYST_AGENT'
  | 'SECURITY_AGENT'
  | 'FINANCE_AGENT'
  | 'OPERATIONS_AGENT'
  | 'CUSTOMER_AGENT';

export type DecisionConfidence = 'VERY_LOW' | 'LOW' | 'MEDIUM' | 'HIGH' | 'VERY_HIGH';

export type PerformanceState = 'EXCEEDING' | 'OPTIMAL' | 'WARNING' | 'DEGRADED' | 'FAILED';

export type ConflictStatus = 'DETECTED' | 'IN_NEGOTIATION' | 'RESOLVED' | 'ESCALATED' | 'DEADLOCKED';

export type GovernanceVerdict = 'PENDING' | 'APPROVED' | 'REJECTED' | 'CONDITIONAL' | 'ESCALATED_TO_HUMAN';

export type SimulationType = 'DIGITAL_TWIN' | 'MONTE_CARLO' | 'HISTORICAL_REPLAY' | 'CHAOS_STRESS';

export interface MissionMetric {
  metric_id: string;
  name: string;
  baseline_value: number;
  current_value: number;
  target_value: number;
  unit: string;
  direction: string;
}

export interface MissionConstraint {
  constraint_id: string;
  description: string;
  constraint_type: string;
  threshold_value: number;
  unit: string;
  is_strict: boolean;
}

export interface MissionObjective {
  objective_id: string;
  title: string;
  description: string;
  target_metric: string;
  target_value: number;
  current_value: number;
  weight: number;
  status: string;
  progress_percent: number;
}

export interface Mission {
  mission_id: string;
  title: string;
  raw_goal: string;
  priority: MissionPriority;
  state: OrganizationState;
  timeline_days: number;
  required_capabilities: string[];
  assigned_roles: AgentRoleType[];
  objectives: MissionObjective[];
  constraints: MissionConstraint[];
  metrics: MissionMetric[];
  strategic_alignment_score: number;
  confidence: DecisionConfidence;
  created_at: number;
  validated_at?: number;
  metadata?: Record<string, any>;
}

export interface StrategyAction {
  action_id: string;
  title: string;
  target_department: string;
  required_roles: AgentRoleType[];
  estimated_cost_usd: number;
  expected_utility: number;
  timeline_weeks: number;
  status: string;
}

export interface StrategyRisk {
  risk_id: string;
  description: string;
  severity: string;
  probability: number;
  mitigation_strategy: string;
}

export interface StrategyPlan {
  strategy_id: string;
  mission_id: string;
  title: string;
  rationale: string;
  objectives: string[];
  actions: StrategyAction[];
  required_agent_roles: AgentRoleType[];
  timeline_weeks: number;
  expected_roi_multiplier: number;
  total_estimated_cost_usd: number;
  risk_score: number;
  confidence: DecisionConfidence;
  fallback_strategy_id?: string;
  simulation_pass_rate: number;
  is_selected: boolean;
  created_at: number;
  metadata?: Record<string, any>;
}

export interface VirtualTeam {
  team_id: string;
  name: string;
  lead_role: AgentRoleType;
  member_roles: AgentRoleType[];
  member_agent_ids: string[];
  mission_scope: string;
  active_task_count: number;
  productivity_score: number;
}

export interface VirtualDepartment {
  department_id: string;
  name: string;
  head_role: AgentRoleType;
  teams: VirtualTeam[];
  budget_allocated_usd: number;
  budget_spent_usd: number;
  health_score: number;
  active_projects_count: number;
  capabilities: string[];
}

export interface VirtualOrganization {
  org_id: string;
  name: string;
  mission_id: string;
  strategy_id: string;
  state: OrganizationState;
  departments: VirtualDepartment[];
  executive_board: AgentRoleType[];
  span_of_control: number;
  operational_efficiency: number;
  created_at: number;
  updated_at: number;
}

export interface SkillProfile {
  skill_name: string;
  proficiency_level: number;
  verified_tasks_count: number;
  last_evaluated_at: number;
}

export interface AgentEmployee {
  agent_id: string;
  name: string;
  role: AgentRoleType;
  department_id: string;
  skills: SkillProfile[];
  current_workload_percent: number;
  productivity_score: number;
  reliability_score: number;
  hourly_cost_usd: number;
  tasks_completed: number;
  status: 'ACTIVE' | 'BUSY' | 'IDLE' | 'RETIRED';
  learning_level: number;
  joined_at: number;
}

export interface VirtualTask {
  task_id: string;
  title: string;
  description: string;
  assigned_agent_id: string;
  assigned_role: AgentRoleType;
  estimated_days: number;
  actual_days: number;
  status: 'TODO' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';
  dependencies: string[];
  is_critical_path: boolean;
  progress_percent: number;
}

export interface ProjectMilestone {
  milestone_id: string;
  title: string;
  due_week: number;
  status: 'PENDING' | 'ACHIEVED' | 'DELAYED';
  target_tasks: string[];
}

export interface VirtualProject {
  project_id: string;
  mission_id: string;
  title: string;
  description: string;
  lead_agent_id: string;
  tasks: VirtualTask[];
  milestones: ProjectMilestone[];
  total_progress_percent: number;
  is_on_schedule: boolean;
  critical_path_duration_days: number;
  status: 'PLANNING' | 'ACTIVE' | 'COMPLETED' | 'PAUSED' | 'BLOCKED';
  created_at: number;
  updated_at: number;
}

export interface ResourcePool {
  compute_slots_total: number;
  compute_slots_used: number;
  token_budget_monthly: number;
  tokens_consumed: number;
  memory_gb_total: number;
  memory_gb_used: number;
  dollar_budget_total_usd: number;
  dollar_budget_spent_usd: number;
  utilization_rate: number;
}

export interface DepartmentResourceQuota {
  department_id: string;
  department_name: string;
  compute_slots: number;
  token_quota_monthly: number;
  memory_gb: number;
  budget_allocated_usd: number;
  priority_weight: number;
}

export interface ResourceAllocationPlan {
  plan_id: string;
  quotas: DepartmentResourceQuota[];
  overall_efficiency_score: number;
  is_pareto_optimal: boolean;
  created_at: number;
  metadata?: Record<string, any>;
}

export interface AgentScorecard {
  agent_id: string;
  agent_name: string;
  role: AgentRoleType;
  accuracy_rate: number;
  productivity_score: number;
  reliability_score: number;
  cost_efficiency: number;
  state: PerformanceState;
}

export interface TeamScorecard {
  team_id: string;
  team_name: string;
  collaboration_score: number;
  completion_rate: number;
  knowledge_sharing_index: number;
  state: PerformanceState;
}

export interface OrganizationScorecard {
  org_id: string;
  overall_roi_multiplier: number;
  annual_growth_rate_pct: number;
  innovation_index: number;
  operational_efficiency: number;
  composite_health_score: number;
  agent_scorecards: AgentScorecard[];
  team_scorecards: TeamScorecard[];
  evaluated_at: number;
}

export interface CostForecast {
  horizon_months: number;
  projected_spend_usd: number;
  projected_savings_usd: number;
  net_budget_impact_usd: number;
  confidence_level: number;
}

export interface ROIProjection {
  baseline_cost_per_1k_docs_usd: number;
  optimized_cost_per_1k_docs_usd: number;
  savings_percentage: number;
  cumulative_savings_ytd_usd: number;
  projected_annual_roi_multiplier: number;
  break_even_timeline_days: number;
}

export interface FinancialSummary {
  total_monthly_burn_usd: number;
  compute_spend_usd: number;
  agent_workforce_equivalent_usd: number;
  infrastructure_overhead_usd: number;
  revenue_impact_monthly_usd: number;
  net_operating_margin_pct: number;
  active_roi_multiplier: number;
  cost_forecast: CostForecast;
  roi_projection: ROIProjection;
  evaluated_at: number;
}

export interface NegotiationProposal {
  proposal_id: string;
  proposing_role: AgentRoleType;
  requested_resource: string;
  requested_units: number;
  rationale: string;
  utility_expected: number;
  timestamp_utc: number;
}

export interface CounterProposal {
  counter_id: string;
  responding_role: AgentRoleType;
  offered_units: number;
  compromise_conditions: string[];
  utility_expected: number;
  timestamp_utc: number;
}

export interface NegotiationAgreement {
  agreement_id: string;
  negotiation_id: string;
  parties: AgentRoleType[];
  settled_units: number;
  compromise_summary: string;
  nash_product_score: number;
  is_pareto_optimal: boolean;
  agreed_at: number;
}

export interface AgentNegotiation {
  negotiation_id: string;
  topic: string;
  initiating_role: AgentRoleType;
  responding_role: AgentRoleType;
  status: ConflictStatus;
  proposals: NegotiationProposal[];
  counter_proposals: CounterProposal[];
  agreement?: NegotiationAgreement;
  created_at: number;
  updated_at: number;
}

export interface GovernanceReview {
  review_id: string;
  decision_title: string;
  proposing_role: AgentRoleType;
  decision_payload: Record<string, any>;
  ethical_review_passed: boolean;
  security_review_passed: boolean;
  financial_review_passed: boolean;
  strategic_review_passed: boolean;
  simulation_verified: boolean;
  verdict: GovernanceVerdict;
  confidence_score: number;
  rejection_reason?: string;
  cryptographic_seal_sha256: string;
  reviewed_at: number;
}

export interface OrganizationSimulationReport {
  report_id: string;
  scenario_name: string;
  simulation_type: SimulationType;
  runs_completed: number;
  success_rate: number;
  mean_roi_multiplier: number;
  p95_latency_ms: number;
  cost_variance_pct: number;
  risk_index: number;
  resilience_score: number;
  simulated_at: number;
  metadata?: Record<string, any>;
}

export interface OrganizationCycleSummary {
  cycle_id: string;
  mission_id: string;
  strategy_id: string;
  org_id: string;
  project_id: string;
  governance_review_id: string;
  simulation_report_id: string;
  composite_health_score: number;
  roi_multiplier: number;
  status: string;
  duration_ms: number;
  completed_at: number;
}

export interface OrganizationOverview {
  organization_name: string;
  state: OrganizationState;
  composite_health_score: number;
  overall_roi_multiplier: number;
  monthly_burn_rate_usd: number;
  active_missions_count: number;
  active_projects_count: number;
  active_workforce_count: number;
  compute_utilization_pct: number;
  governance_approval_rate: number;
  total_cycles_executed: number;
  latest_cycle?: OrganizationCycleSummary;
}
