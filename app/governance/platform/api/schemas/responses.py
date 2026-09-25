"""Response DTOs and standard error contracts for the Governance Platform APIs."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class APIErrorDetails(BaseModel):
    """Canonical error object format."""

    code: str
    message: str
    request_id: str
    details: Optional[Dict[str, Any]] = None


class APIErrorResponse(BaseModel):
    """Wrapper response for errors."""

    error: APIErrorDetails


class PolicyResponse(BaseModel):
    """Representation of a returned policy."""

    policy_id: str
    name: str
    description: str
    policy_type: str
    severity: str
    rules: List[Dict[str, Any]]
    enforcement_action: str
    status: str = "ACTIVE"
    version: str = "1.0.0"
    tenant_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DecisionEvaluationResponse(BaseModel):
    """Response returned after evaluating an action against governance rules."""

    decision_id: str
    decision: str = Field(..., description="ALLOW, DENY, APPROVAL_REQUIRED, WARN")
    allowed: bool
    reason: str
    policies_applied: List[str] = Field(default_factory=list)
    risk_level: str = "LOW"
    evaluation_time_ms: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditRecordResponse(BaseModel):
    """Response schema for audit log entries."""

    audit_id: str
    tenant_id: str
    event_type: str
    actor: str
    action: str
    resource: str
    decision: str
    integrity_hash: str
    timestamp: datetime


class ApprovalItemResponse(BaseModel):
    """Response schema for human review requests."""

    request_id: str
    tenant_id: str
    action: str
    resource: str
    risk_level: str
    status: str
    requested_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewer_id: Optional[str] = None
    decision: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Standard container for paginated list responses."""

    items: List[Any]
    total_count: int
    page: int = 1
    page_size: int = 50
    has_next: bool = False
