"""Governance Analytics Event Normalization and Canonical Schemas."""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid


class AnalyticsEventType(str, Enum):
    GOVERNANCE_DECISION_CREATED = "GovernanceDecisionCreated"
    POLICY_VIOLATION = "PolicyViolation"
    ACCESS_DENIED = "AccessDenied"
    APPROVAL_REQUIRED = "ApprovalRequired"
    RISK_DETECTED = "RiskDetected"
    AUDIT_CREATED = "AuditCreated"
    MODEL_INVOCATION = "ModelInvocation"
    PROMPT_EVALUATION = "PromptEvaluation"
    SAFETY_INCIDENT = "SafetyIncident"
    HUMAN_OVERRIDE = "HumanOverride"
    WORKFLOW_EXECUTION = "WorkflowExecution"


class GovernanceAnalyticsEvent(BaseModel):
    """Universal canonical analytics event schema for AI governance telemetry."""
    event_id: str = Field(default_factory=lambda: f"gev_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    organization_id: str = "org_default"
    workspace_id: str = "workspace_default"
    
    # Event Classification
    event_type: AnalyticsEventType
    source_system: str = "governance_control_plane"
    entity_type: str = "SYSTEM"
    entity_id: str = "default_entity"
    
    # Actors & Governance Identifiers
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    policy_id: Optional[str] = None
    
    # Risk, Severity, and Performance Metrics
    risk_level: str = "LOW"            # LOW, MEDIUM, HIGH, CRITICAL
    severity: str = "INFO"             # INFO, WARNING, HIGH, CRITICAL
    risk_score: float = 0.0            # 0.0 to 1.0 (or 0 to 100)
    confidence_score: Optional[float] = None
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    is_success: bool = True
    
    # Timing & Metadata
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EventNormalizer:
    """Transforms heterogeneous governance events into unified analytics events."""

    @staticmethod
    def normalize_dict(raw: Dict[str, Any], event_type: Optional[AnalyticsEventType] = None) -> GovernanceAnalyticsEvent:
        # Determine event type
        t_str = raw.get("event_type") or raw.get("type")
        if event_type:
            resolved_type = event_type
        elif t_str:
            try:
                resolved_type = AnalyticsEventType(t_str)
            except ValueError:
                resolved_type = AnalyticsEventType.GOVERNANCE_DECISION_CREATED
        else:
            resolved_type = AnalyticsEventType.GOVERNANCE_DECISION_CREATED

        return GovernanceAnalyticsEvent(
            event_id=raw.get("event_id") or f"gev_{uuid.uuid4().hex[:12]}",
            tenant_id=raw.get("tenant_id", "default_tenant"),
            organization_id=raw.get("organization_id", "org_default"),
            workspace_id=raw.get("workspace_id", "workspace_default"),
            event_type=resolved_type,
            source_system=raw.get("source_system", "governance_control_plane"),
            entity_type=raw.get("entity_type", "SYSTEM"),
            entity_id=str(raw.get("entity_id", "entity_default")),
            user_id=raw.get("user_id") or raw.get("actor_id"),
            agent_id=raw.get("agent_id"),
            workflow_id=raw.get("workflow_id"),
            model_id=raw.get("model_id"),
            prompt_id=raw.get("prompt_id"),
            policy_id=raw.get("policy_id"),
            risk_level=str(raw.get("risk_level", "LOW")).upper(),
            severity=str(raw.get("severity", "INFO")).upper(),
            risk_score=float(raw.get("risk_score", 0.0)),
            confidence_score=float(raw.get("confidence_score")) if raw.get("confidence_score") is not None else None,
            cost_usd=float(raw.get("cost_usd", 0.0)),
            latency_ms=float(raw.get("latency_ms", 0.0)),
            is_success=bool(raw.get("is_success", True)),
            timestamp=raw.get("timestamp") if isinstance(raw.get("timestamp"), datetime) else datetime.now(timezone.utc),
            metadata=raw.get("metadata", {}),
        )
