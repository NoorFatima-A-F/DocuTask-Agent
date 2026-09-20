"""Domain and DTO models for the Governance Python SDK."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GovernanceDecision(BaseModel):
    """Result of an action evaluation."""

    decision_id: str
    decision: str
    allowed: bool
    reason: str
    policies_applied: List[str] = Field(default_factory=list)
    risk_level: str = "LOW"
    evaluation_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GovernancePolicy(BaseModel):
    """Representation of an enterprise governance policy."""

    policy_id: str
    name: str
    description: str
    policy_type: str
    severity: str
    rules: List[Dict[str, Any]] = Field(default_factory=list)
    enforcement_action: str
    status: str = "ACTIVE"
    version: str = "1.0.0"
    tenant_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditRecord(BaseModel):
    """Audit log entry retrieved via SDK."""

    audit_id: str
    tenant_id: str
    event_type: str
    actor: str
    action: str
    resource: str
    decision: str
    integrity_hash: str
    previous_hash: str
    timestamp: str


class ApprovalItem(BaseModel):
    """Approval queue item."""

    request_id: str
    tenant_id: str
    action: str
    resource: str
    risk_level: str
    status: str
    reason: str
    requested_at: str
    reviewed_at: Optional[str] = None
    reviewer_id: Optional[str] = None
    decision: Optional[str] = None
    comments: Optional[str] = None


class GovernanceReport(BaseModel):
    """Governance summary report."""

    tenant_id: str
    report_type: str
    governance_health_score: float
    summary: Dict[str, Any]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WebhookSubscription(BaseModel):
    """Registered webhook subscription."""

    webhook_id: str
    tenant_id: str
    url: str
    events: List[str]
    is_active: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
