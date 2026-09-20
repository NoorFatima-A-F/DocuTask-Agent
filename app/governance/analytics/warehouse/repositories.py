"""Governance Data Warehouse In-Memory OLAP Repository."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import collections

from .models import (
    DimTenant,
    DimUser,
    DimAgent,
    DimModel,
    DimPolicy,
    DimWorkflow,
    DimTime,
    FactGovernanceDecision,
    FactPolicyEvent,
    FactAIExecution,
    FactRiskEvent,
    FactComplianceEvent,
    FactApproval,
)
from .schemas import WarehouseQueryFilter, TimeBucketSummary
from ..events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType


class GovernanceDataWarehouseRepository:
    """OLAP Analytical store for enterprise AI governance intelligence."""

    def __init__(self):
        # Fact tables
        self.fact_decisions: List[FactGovernanceDecision] = []
        self.fact_policies: List[FactPolicyEvent] = []
        self.fact_ai_executions: List[FactAIExecution] = []
        self.fact_risk_events: List[FactRiskEvent] = []
        self.fact_compliance_events: List[FactComplianceEvent] = []
        self.fact_approvals: List[FactApproval] = []

        # Dimension tables
        self.dim_tenants: Dict[str, DimTenant] = {}
        self.dim_users: Dict[str, DimUser] = {}
        self.dim_agents: Dict[str, DimAgent] = {}
        self.dim_models: Dict[str, DimModel] = {}
        self.dim_policies: Dict[str, DimPolicy] = {}
        self.dim_workflows: Dict[str, DimWorkflow] = {}

    def insert_event(self, event: GovernanceAnalyticsEvent) -> None:
        """Translates and records an analytics event into appropriate fact & dimension tables."""
        t = event.timestamp

        # Register Dimensions if not present
        if event.tenant_id not in self.dim_tenants:
            self.dim_tenants[event.tenant_id] = DimTenant(
                tenant_id=event.tenant_id,
                organization_id=event.organization_id,
                workspace_id=event.workspace_id,
            )

        if event.user_id and event.user_id not in self.dim_users:
            self.dim_users[event.user_id] = DimUser(user_id=event.user_id, tenant_id=event.tenant_id)

        if event.agent_id and event.agent_id not in self.dim_agents:
            self.dim_agents[event.agent_id] = DimAgent(agent_id=event.agent_id, tenant_id=event.tenant_id, agent_name=event.agent_id)

        if event.model_id and event.model_id not in self.dim_models:
            self.dim_models[event.model_id] = DimModel(model_id=event.model_id)

        if event.policy_id and event.policy_id not in self.dim_policies:
            self.dim_policies[event.policy_id] = DimPolicy(policy_id=event.policy_id, tenant_id=event.tenant_id, policy_name=event.policy_id)

        if event.workflow_id and event.workflow_id not in self.dim_workflows:
            self.dim_workflows[event.workflow_id] = DimWorkflow(workflow_id=event.workflow_id, tenant_id=event.tenant_id, workflow_name=event.workflow_id)

        # Route to Fact Tables based on event type
        if event.event_type in {
            AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
            AnalyticsEventType.ACCESS_DENIED,
        }:
            outcome = "DENIED" if event.event_type == AnalyticsEventType.ACCESS_DENIED else ("ALLOWED" if event.is_success else "BLOCKED")
            self.fact_decisions.append(
                FactGovernanceDecision(
                    tenant_id=event.tenant_id,
                    user_id=event.user_id,
                    agent_id=event.agent_id,
                    policy_id=event.policy_id,
                    outcome=outcome,
                    risk_score=event.risk_score,
                    latency_ms=event.latency_ms,
                    timestamp=t,
                    metadata=event.metadata,
                )
            )

        elif event.event_type == AnalyticsEventType.POLICY_VIOLATION:
            self.fact_policies.append(
                FactPolicyEvent(
                    tenant_id=event.tenant_id,
                    policy_id=event.policy_id or "policy_violated",
                    severity=event.severity,
                    actor_id=event.user_id or event.agent_id,
                    timestamp=t,
                    metadata=event.metadata,
                )
            )

        elif event.event_type in {
            AnalyticsEventType.MODEL_INVOCATION,
            AnalyticsEventType.PROMPT_EVALUATION,
            AnalyticsEventType.WORKFLOW_EXECUTION,
        }:
            self.fact_ai_executions.append(
                FactAIExecution(
                    tenant_id=event.tenant_id,
                    agent_id=event.agent_id,
                    workflow_id=event.workflow_id,
                    model_id=event.model_id,
                    prompt_id=event.prompt_id,
                    cost_usd=event.cost_usd,
                    latency_ms=event.latency_ms,
                    risk_score=event.risk_score,
                    is_success=event.is_success,
                    timestamp=t,
                    metadata=event.metadata,
                )
            )

        elif event.event_type in {
            AnalyticsEventType.RISK_DETECTED,
            AnalyticsEventType.SAFETY_INCIDENT,
        }:
            cat = event.metadata.get("risk_category", "Security Risk")
            self.fact_risk_events.append(
                FactRiskEvent(
                    tenant_id=event.tenant_id,
                    category=cat,
                    severity=event.severity,
                    risk_score=event.risk_score,
                    source_system=event.source_system,
                    entity_id=event.entity_id,
                    timestamp=t,
                    metadata=event.metadata,
                )
            )

        elif event.event_type in {
            AnalyticsEventType.APPROVAL_REQUIRED,
            AnalyticsEventType.HUMAN_OVERRIDE,
        }:
            self.fact_approvals.append(
                FactApproval(
                    tenant_id=event.tenant_id,
                    review_id=event.metadata.get("review_id", f"rev_{event.event_id}"),
                    reviewer_id=event.user_id or "reviewer_auto",
                    strategy=event.metadata.get("strategy", "SEQUENTIAL"),
                    outcome=event.metadata.get("outcome", "APPROVED"),
                    turnaround_time_seconds=float(event.metadata.get("turnaround_time_seconds", 0.0)),
                    is_override=(event.event_type == AnalyticsEventType.HUMAN_OVERRIDE),
                    timestamp=t,
                    metadata=event.metadata,
                )
            )

        elif event.event_type == AnalyticsEventType.AUDIT_CREATED:
            framework = event.metadata.get("compliance_framework", "SOC2")
            control = event.metadata.get("control_id", "CC6.1")
            self.fact_compliance_events.append(
                FactComplianceEvent(
                    tenant_id=event.tenant_id,
                    framework=framework,
                    control_id=control,
                    status="COMPLIANT" if event.is_success else "NON_COMPLIANT",
                    evidence_id=event.metadata.get("evidence_id"),
                    timestamp=t,
                    metadata=event.metadata,
                )
            )

    def query_decisions(self, q: WarehouseQueryFilter) -> List[FactGovernanceDecision]:
        res = self.fact_decisions
        if q.tenant_id != "*":
            res = [r for r in res if r.tenant_id == q.tenant_id]
        if q.start_time:
            res = [r for r in res if r.timestamp >= q.start_time]
        if q.end_time:
            res = [r for r in res if r.timestamp <= q.end_time]
        return res[q.offset : q.offset + q.limit]

    def query_policy_events(self, q: WarehouseQueryFilter) -> List[FactPolicyEvent]:
        res = self.fact_policies
        if q.tenant_id != "*":
            res = [r for r in res if r.tenant_id == q.tenant_id]
        if q.policy_id:
            res = [r for r in res if r.policy_id == q.policy_id]
        return res[q.offset : q.offset + q.limit]

    def query_ai_executions(self, q: WarehouseQueryFilter) -> List[FactAIExecution]:
        res = self.fact_ai_executions
        if q.tenant_id != "*":
            res = [r for r in res if r.tenant_id == q.tenant_id]
        if q.agent_id:
            res = [r for r in res if r.agent_id == q.agent_id]
        if q.model_id:
            res = [r for r in res if r.model_id == q.model_id]
        if q.prompt_id:
            res = [r for r in res if r.prompt_id == q.prompt_id]
        return res[q.offset : q.offset + q.limit]

    def query_risk_events(self, q: WarehouseQueryFilter) -> List[FactRiskEvent]:
        res = self.fact_risk_events
        if q.tenant_id != "*":
            res = [r for r in res if r.tenant_id == q.tenant_id]
        if q.category:
            res = [r for r in res if r.category == q.category]
        return res[q.offset : q.offset + q.limit]

    def query_compliance_events(self, q: WarehouseQueryFilter) -> List[FactComplianceEvent]:
        res = self.fact_compliance_events
        if q.tenant_id != "*":
            res = [r for r in res if r.tenant_id == q.tenant_id]
        if q.framework:
            res = [r for r in res if r.framework == q.framework]
        return res[q.offset : q.offset + q.limit]

    def query_approvals(self, q: WarehouseQueryFilter) -> List[FactApproval]:
        res = self.fact_approvals
        if q.tenant_id != "*":
            res = [r for r in res if r.tenant_id == q.tenant_id]
        return res[q.offset : q.offset + q.limit]
