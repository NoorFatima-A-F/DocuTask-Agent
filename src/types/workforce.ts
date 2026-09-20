/**
 * Phase 13.23 - Enterprise Autonomous Agent Workforce & Digital Organization Platform (EAAWDOP) Types
 */

export type EmployeeRole = 
  | 'CEO'
  | 'VP'
  | 'DIRECTOR'
  | 'MANAGER'
  | 'PRINCIPAL_ARCHITECT'
  | 'LEAD_SPECIALIST'
  | 'SENIOR_SPECIALIST'
  | 'ASSOCIATE_SPECIALIST'
  | 'JUNIOR_WORKER'
  | 'REVIEWER'
  | 'AUDITOR'
  | 'ARBITRATOR';

export type DepartmentType = 
  | 'EXECUTIVE'
  | 'ENGINEERING'
  | 'OPERATIONS'
  | 'FINANCE'
  | 'SECURITY_COMPLIANCE'
  | 'BUSINESS_STRATEGY'
  | 'QUALITY_ASSURANCE'
  | 'CUSTOMER_SUCCESS';

export type EmployeeStatus = 
  | 'ACTIVE'
  | 'BUSY'
  | 'IN_MEETING'
  | 'ON_CALL'
  | 'STANDBY'
  | 'MAINTENANCE'
  | 'PROMOTED'
  | 'RETIRED';

export interface DigitalEmployee {
  id: string;
  tenant_id: string;
  name: string;
  role: EmployeeRole;
  department: DepartmentType;
  manager_id?: string;
  level: number;
  skills: string[];
  security_clearance: string;
  availability_status: EmployeeStatus;
  capacity_slots: number;
  assigned_tasks_count: number;
  trust_score: number;
  hourly_salary_usd: number;
  token_cost_multiplier: number;
  lifetime_tasks_completed: number;
  task_success_rate: number;
  burnout_risk_score: number;
  career_history: Array<Record<string, any>>;
  created_at: string;
}

export interface Department {
  id: string;
  tenant_id: string;
  name: string;
  dept_type: DepartmentType;
  manager_id?: string;
  headcount: number;
  monthly_budget_usd: number;
  active_projects: string[];
  okrs: string[];
  created_at: string;
}

export interface DynamicTeam {
  id: string;
  tenant_id: string;
  team_name: string;
  mission: string;
  team_lead_id: string;
  member_ids: string[];
  required_skills: string[];
  max_budget_usd: number;
  sla_hours: number;
  active_tasks: string[];
  team_health_score: number;
  created_at: string;
}

export interface TaskMarketplaceListing {
  id: string;
  tenant_id: string;
  title: string;
  description: string;
  required_skills: string[];
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  budget_max_usd: number;
  deadline: string;
  status: 'OPEN' | 'BIDDING' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED';
  assigned_employee_id?: string;
  bids: Array<{
    bid_id: string;
    employee_id: string;
    bid_cost_usd: number;
    estimated_duration_minutes: number;
    confidence_score: number;
    proposed_solution_outline?: string;
  }>;
  created_at: string;
}

export interface NegotiationSession {
  id: string;
  tenant_id: string;
  topic: string;
  participant_employee_ids: string[];
  proposals: Array<{ from: string; proposal: string }>;
  consensus_reached: boolean;
  agreed_terms: Record<string, any>;
  status: 'IN_PROGRESS' | 'AGREED' | 'DEADLOCKED' | 'ESCALATED';
  created_at: string;
}

export interface CollaborationVote {
  id: string;
  tenant_id: string;
  proposal_title: string;
  initiator_employee_id: string;
  voter_employee_ids: string[];
  votes: Record<string, string>;
  required_quorum: number;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  decided_at?: string;
  created_at: string;
}

export interface ManagerReviewRecord {
  id: string;
  tenant_id: string;
  employee_id: string;
  manager_id: string;
  review_period: string;
  performance_rating: number;
  strengths: string[];
  areas_for_growth: string[];
  workload_balance_action: string;
  promotion_recommended: boolean;
  created_at: string;
}

export interface ExecutiveCouncilProposition {
  id: string;
  tenant_id: string;
  title: string;
  summary: string;
  category: 'STRATEGIC' | 'FINANCIAL' | 'SECURITY' | 'ARCHITECTURAL' | 'COMPLIANCE';
  council_votes: Record<string, string>;
  quorum_met: boolean;
  enacted: boolean;
  impact_assessment: Record<string, any>;
  created_at: string;
}

export interface WorkforcePerformanceMetric {
  tenant_id: string;
  total_workforce_headcount: number;
  active_employees_count: number;
  workforce_utilization_rate: number;
  average_trust_score: number;
  average_task_success_rate: number;
  collaboration_index: number;
  innovation_velocity_score: number;
  workforce_burnout_risk: number;
  monthly_salary_burn_usd: number;
}

export interface EconomicResourceBudget {
  tenant_id: string;
  allocated_gpu_hours: number;
  used_gpu_hours: number;
  allocated_tokens: number;
  used_tokens: number;
  total_budget_usd: number;
  total_spent_usd: number;
  efficiency_roi_ratio: number;
  reallocation_recommendations: string[];
}

export interface HiringRequisition {
  id: string;
  tenant_id: string;
  department: DepartmentType;
  target_role: EmployeeRole;
  required_skills: string[];
  reason: string;
  status: 'DRAFT' | 'PENDING_APPROVAL' | 'APPROVED' | 'FILLED';
  candidate_profiles: Array<{ name: string; score: number; suggested_salary: number }>;
  hired_employee_id?: string;
  created_at: string;
}

export interface CareerPromotionPath {
  id: string;
  tenant_id: string;
  employee_id: string;
  current_role: EmployeeRole;
  target_role: EmployeeRole;
  eligibility_score: number;
  completed_milestones: string[];
  status: 'IN_PROGRESS' | 'READY' | 'PROMOTED';
  promoted_at?: string;
}

export interface WorkforceScheduleEntry {
  id: string;
  tenant_id: string;
  employee_id: string;
  shift_name: string;
  time_zone: string;
  start_hour: number;
  end_hour: number;
  is_active: boolean;
}

export interface CollectiveMemoryRecord {
  id: string;
  tenant_id: string;
  scope: 'TEAM' | 'DEPARTMENT' | 'EXECUTIVE' | 'ENTERPRISE';
  scope_id: string;
  title: string;
  content: string;
  tags: string[];
  author_employee_id: string;
  trust_weight: number;
  created_at: string;
}

export interface ConflictResolutionRecord {
  id: string;
  tenant_id: string;
  party_a_id: string;
  party_b_id: string;
  dispute_subject: string;
  mediator_employee_id: string;
  status: 'OPEN' | 'MEDIATING' | 'ARBITRATING' | 'RESOLVED';
  resolution_summary: string;
  binding_agreements: string[];
  resolved_at: string;
}

export interface OrganizationOverviewReport {
  tenant_id: string;
  total_employees: number;
  total_departments: number;
  active_teams: number;
  marketplace_open_tasks: number;
  council_active_propositions: number;
  average_trust_score: number;
  workforce_readiness_index: number;
  generated_at: string;
}
