/**
 * TypeScript definitions for the DocuTask Governance SDK.
 */

export type DecisionType = "ALLOW" | "DENY" | "APPROVAL_REQUIRED" | "WARN";
export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface GovernanceDecision {
  decision_id: string;
  decision: DecisionType;
  allowed: boolean;
  reason: string;
  policies_applied: string[];
  risk_level: RiskLevel;
  evaluation_time_ms: number;
  timestamp: string;
}

export interface GovernancePolicy {
  policy_id: string;
  name: string;
  description: string;
  policy_type: string;
  severity: string;
  rules: Record<string, any>[];
  enforcement_action: string;
  status: string;
  version: string;
  tenant_id: string;
  created_at: string;
  updated_at: string;
}

export interface EvaluateRequest {
  action: string;
  resource: string;
  context?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface GovernanceReport {
  tenant_id: string;
  report_type: string;
  governance_health_score: number;
  summary: Record<string, any>;
  generated_at: string;
}

export interface WebhookSubscription {
  webhook_id: string;
  tenant_id: string;
  url: string;
  events: string[];
  is_active: boolean;
  created_at: string;
}
