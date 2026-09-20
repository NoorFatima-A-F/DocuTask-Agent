/**
 * Phase 13.22 - Enterprise Cognitive Intelligence & Autonomous Organizational Learning Platform (ECIAOLP) Types
 */

export type ReasoningNodeType =
  | 'AGENT'
  | 'PROJECT'
  | 'CUSTOMER'
  | 'BUSINESS_GOAL'
  | 'KPI'
  | 'INCIDENT'
  | 'WORKFLOW'
  | 'POLICY'
  | 'RISK'
  | 'DECISION'
  | 'HYPOTHESIS';

export type ReasoningRelationType =
  | 'caused_by'
  | 'influences'
  | 'depends_on'
  | 'contradicts'
  | 'recommends'
  | 'improves'
  | 'blocked_by'
  | 'validates'
  | 'predicts';

export interface CognitiveNode {
  id: string;
  tenant_id: string;
  node_type: ReasoningNodeType;
  name: string;
  description: string;
  properties: Record<string, any>;
  confidence: number;
  created_at: string;
}

export interface CognitiveEdge {
  id: string;
  tenant_id: string;
  source_node_id: string;
  target_node_id: string;
  relation: ReasoningRelationType;
  weight: number;
  evidence: string;
  created_at: string;
}

export interface ExperienceMemoryEntry {
  id: string;
  tenant_id: string;
  task_fingerprint: string;
  agent_id: string;
  input_pattern: string;
  successful_execution_trace: string[];
  performance_metrics: Record<string, number>;
  reusable_knowledge: string;
  reuse_count: number;
  created_at: string;
}

export interface DiscoveredProcess {
  id: string;
  tenant_id: string;
  process_name: string;
  reconstructed_steps: string[];
  observed_executions_count: number;
  avg_cycle_time_seconds: number;
  bottlenecks: string[];
  automation_opportunity_score: number;
  discovered_at: string;
}

export interface DecisionRecord {
  id: string;
  tenant_id: string;
  decision_topic: string;
  chosen_action: string;
  alternatives_considered: string[];
  reasoning_rationale: string;
  risk_level: string;
  confidence_score: number;
  expected_outcome: Record<string, any>;
  actual_outcome?: Record<string, any>;
  outcome_matched?: boolean;
  decided_at: string;
  resolved_at?: string;
}

export interface Hypothesis {
  id: string;
  tenant_id: string;
  statement: string;
  supporting_evidence: string[];
  confidence_score: number;
  suggested_action: string;
  impact_area: string;
  status: string;
  created_at: string;
}

export interface SimulationScenario {
  id: string;
  tenant_id: string;
  scenario_name: string;
  parameter_overrides: Record<string, any>;
  projected_latency_change_pct: number;
  projected_cost_change_pct: number;
  projected_roi_factor: number;
  risk_assessment: string;
}

export interface OptimizationOpportunity {
  id: string;
  tenant_id: string;
  subsystem: string;
  target_resource: string;
  recommended_change: string;
  projected_savings_monthly_usd: number;
  status: string;
}

export interface GoalAlignmentNode {
  id: string;
  tenant_id: string;
  corporate_kpi: string;
  business_goal: string;
  department_goal: string;
  assigned_agents: string[];
  current_progress_pct: number;
  alignment_health: string;
}

export interface StrategicRecommendation {
  id: string;
  tenant_id: string;
  category: string;
  title: string;
  description: string;
  urgency: string;
  projected_business_impact: string;
  created_at: string;
}

export interface ExecutiveInsightReport {
  tenant_id: string;
  cognitive_health_index: number;
  active_hypotheses_count: number;
  discovered_processes_count: number;
  experience_memories_reused_count: number;
  strategic_recommendations: StrategicRecommendation[];
  active_optimizations: OptimizationOpportunity[];
  generated_at: string;
}
