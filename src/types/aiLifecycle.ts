/**
 * Phase 13.20: Autonomous AI Application Lifecycle Platform (AAILP) Types.
 * Frontend TypeScript Interfaces & Enums.
 */

export type AgentLifecycleState =
  | 'DRAFT'
  | 'DEVELOPMENT'
  | 'TESTING'
  | 'SECURITY_REVIEW'
  | 'APPROVED'
  | 'DEPLOYED'
  | 'DEPRECATED'
  | 'RETIRED';

export type AgentCategory =
  | 'EXTRACTION'
  | 'RESEARCH'
  | 'CUSTOMER_SUPPORT'
  | 'AUTOMATION'
  | 'COMPLIANCE'
  | 'FINANCIAL_AUDIT'
  | 'LEGAL_ANALYSIS';

export type DeploymentEnvironment = 'STAGING' | 'CANARY' | 'PRODUCTION';
export type DeploymentStrategy = 'DIRECT' | 'BLUE_GREEN' | 'CANARY';
export type DeploymentStatus = 'BUILDING' | 'TESTING' | 'STAGING' | 'CANARY' | 'PRODUCTION' | 'ROLLBACK' | 'FAILED';
export type ApprovalStage = 'DEVELOPER_SUBMIT' | 'SECURITY_REVIEW' | 'BUSINESS_APPROVAL' | 'COMPLIANCE_SIGNOFF' | 'FINAL_RELEASE';
export type ApprovalDecision = 'PENDING' | 'APPROVED' | 'REJECTED';

export interface AgentApplication {
  agent_id: string;
  tenant_id: string;
  organization_id: string;
  workspace_id: string;
  name: string;
  slug: string;
  category: AgentCategory;
  owner_id: string;
  owner_email: string;
  description: string;
  lifecycle_state: AgentLifecycleState;
  current_version: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface AgentVersion {
  version_id: string;
  agent_id: string;
  version_tag: string;
  model_family: string;
  system_prompt: string;
  tools: string[];
  connectors: string[];
  parameters: Record<string, any>;
  changelog: string;
  accuracy_score: number;
  cost_per_execution_usd: number;
  created_at: string;
}

export interface AgentTestResult {
  test_id: string;
  agent_id: string;
  version_tag: string;
  functional_pass: boolean;
  grounding_score: number;
  accuracy_score: number;
  hallucination_rate_pct: number;
  security_checks_passed: boolean;
  latency_p95_ms: number;
  cost_estimated_usd: number;
  status: string;
  tested_at: string;
}

export interface SecurityVulnerability {
  vuln_id: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  category: string;
  description: string;
  recommendation: string;
}

export interface AgentSecurityScan {
  scan_id: string;
  agent_id: string;
  version_tag: string;
  security_score: number;
  risk_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  prompt_injection_resistance_pct: number;
  pii_leakage_detected: boolean;
  excessive_permissions: boolean;
  vulnerabilities: SecurityVulnerability[];
  scanned_at: string;
}

export interface AgentApproval {
  approval_id: string;
  agent_id: string;
  version_tag: string;
  stage: ApprovalStage;
  decision: ApprovalDecision;
  approver_id?: string | null;
  approver_email?: string | null;
  comments: string;
  timestamp: string;
}

export interface AgentDeployment {
  deployment_id: string;
  agent_id: string;
  version_tag: string;
  environment: DeploymentEnvironment;
  strategy: DeploymentStrategy;
  traffic_weight_pct: number;
  status: DeploymentStatus;
  distributed_cluster_id: string;
  active_instances_count: number;
  deployed_at: string;
}

export interface AgentDependency {
  dep_id: string;
  agent_id: string;
  dependency_type: string;
  target_resource_id: string;
  target_resource_name: string;
  is_breaking_change: boolean;
}

export interface AgentTemplate {
  template_id: string;
  name: string;
  category: AgentCategory;
  description: string;
  recommended_model: string;
  default_tools: string[];
  default_prompt: string;
}

export interface AgentMarketplaceListing {
  listing_id: string;
  agent_id: string;
  title: string;
  publisher_name: string;
  category: AgentCategory;
  description: string;
  version: string;
  rating: number;
  install_count: number;
  certified_secure: boolean;
  price_monthly_usd: number;
  tags: string[];
}

export interface AgentAnalytics {
  agent_id: string;
  name: string;
  total_executions: number;
  success_rate_pct: number;
  automation_roi_usd: number;
  developer_hours_saved: number;
  adoption_score: number;
  avg_latency_ms: number;
}

export interface AgentRetirementPlan {
  retirement_id: string;
  agent_id: string;
  target_migration_agent_id?: string | null;
  deprecation_notice: string;
  sunset_date: string;
  traffic_redirect_pct: number;
  archived: boolean;
}

export interface LifecycleOverview {
  total_managed_agents: number;
  deployed_in_production: number;
  in_review_or_testing: number;
  deprecated_or_retired: number;
  mean_security_score: number;
  total_automation_roi_usd: number;
  timestamp: string;
}
