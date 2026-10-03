"""Audit Schemas for Request/Response Validation."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .events import ActorType, AuditSeverity, OutcomeType, EventCategory, AuditEvent


class AuditEventCreate(BaseModel):
    event_type: str
    category: EventCategory = EventCategory.SYSTEM
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    environment: str = "production"
    
    actor_id: str
    actor_type: ActorType = ActorType.USER
    actor_name: Optional[str] = None
    actor_role: Optional[str] = None
    
    action: str
    resource_type: str
    resource_id: str
    resource_name: Optional[str] = None
    
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    
    severity: AuditSeverity = AuditSeverity.INFO
    outcome: OutcomeType = OutcomeType.SUCCESS
    status_code: Optional[int] = 200
    duration_ms: Optional[float] = None
    risk_score: float = 0.0
    
    policy_decision: Optional[str] = None
    compliance_controls: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    
    payload_summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditEventRead(AuditEvent):
    pass
