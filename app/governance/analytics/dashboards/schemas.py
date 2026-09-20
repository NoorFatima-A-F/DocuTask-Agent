"""Dashboard Data Transfer Objects (DTOs) for Executive, Admin, and Developer Personas."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..core.metrics import (
    DecisionMetricsSummary,
    PolicyMetricsSummary,
    AgentMetricsSummary,
    ModelMetricsSummary,
    PromptMetricsSummary,
)
from ..risk.analyzer import RiskAnalysisSummary
from ..compliance.reports import AuditReadinessReport


class ExecutiveDashboardDTO(BaseModel):
    tenant_id: str
    overall_governance_score: float = 100.0
    enterprise_risk_level: str = "LOW"
    overall_risk_score: float = 0.0
    compliance_status: str = "AUDIT_READY"
    ai_adoption_total_executions: int = 0
    total_cost_usd: float = 0.0
    major_incidents_count: int = 0
    policy_health_score: float = 1.0
    approval_completion_rate: float = 1.0
    category_risk_scores: Dict[str, float] = Field(default_factory=dict)
    framework_compliance_scores: Dict[str, float] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AdministratorDashboardDTO(BaseModel):
    tenant_id: str
    total_policy_violations: int = 0
    most_triggered_policies: List[Dict[str, Any]] = Field(default_factory=list)
    critical_risk_events_count: int = 0
    blocked_actions_count: int = 0
    pending_approvals_count: int = 0
    failed_evaluations_count: int = 0
    audit_findings_count: int = 0
    decisions: DecisionMetricsSummary = Field(default_factory=DecisionMetricsSummary)
    policies: PolicyMetricsSummary = Field(default_factory=PolicyMetricsSummary)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DeveloperDashboardDTO(BaseModel):
    tenant_id: str
    agent_executions_count: int = 0
    agent_failure_rate: float = 0.0
    avg_model_latency_ms: float = 0.0
    avg_prompt_evaluation_score: float = 1.0
    model_drift_signals_count: int = 0
    workflow_failures_count: int = 0
    agents: AgentMetricsSummary = Field(default_factory=AgentMetricsSummary)
    models: ModelMetricsSummary = Field(default_factory=ModelMetricsSummary)
    prompts: PromptMetricsSummary = Field(default_factory=PromptMetricsSummary)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
