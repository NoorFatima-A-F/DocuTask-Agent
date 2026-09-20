"""Safety Incident Lifecycle States & Incident Entities."""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation


class IncidentLifecycleState(str, Enum):
    """FSM Lifecycle states for AI Safety incidents."""
    DETECTED = "DETECTED"
    CLASSIFIED = "CLASSIFIED"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class SafetyIncidentAuditEntry(BaseModel):
    entry_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:8]}")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str
    action: str
    previous_state: Optional[IncidentLifecycleState] = None
    new_state: Optional[IncidentLifecycleState] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SafetyIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    title: str
    description: str
    category: SafetyCategory
    severity: ViolationSeverity
    state: IncidentLifecycleState = IncidentLifecycleState.DETECTED
    context_id: Optional[str] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    violations: List[SafetyViolation] = Field(default_factory=list)
    audit_trail: List[SafetyIncidentAuditEntry] = Field(default_factory=list)
    mitigation_plan: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
