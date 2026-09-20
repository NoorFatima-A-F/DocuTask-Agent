"""Audit Event Core Domain Models and Enumerations."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class ActorType(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"
    SERVICE = "SERVICE"
    API_CLIENT = "API_CLIENT"
    ADMIN = "ADMIN"
    AUTOMATION = "AUTOMATION"


class AuditSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class OutcomeType(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    DENIED = "DENIED"
    ERROR = "ERROR"
    PARTIAL = "PARTIAL"


class EventCategory(str, Enum):
    AUTHENTICATION = "AUTHENTICATION"
    AUTHORIZATION = "AUTHORIZATION"
    AI = "AI"
    WORKFLOW = "WORKFLOW"
    DATA = "DATA"
    GOVERNANCE = "GOVERNANCE"
    SAFETY = "SAFETY"
    SYSTEM = "SYSTEM"


class AuditEvent(BaseModel):
    """Universal immutable enterprise audit record."""
    event_id: str = Field(default_factory=lambda: f"aud_evt_{uuid.uuid4().hex[:12]}")
    event_type: str
    category: EventCategory = EventCategory.SYSTEM
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Tenancy & Boundaries
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    environment: str = "production"
    
    # Actor Context
    actor_id: str
    actor_type: ActorType = ActorType.USER
    actor_name: Optional[str] = None
    actor_role: Optional[str] = None
    
    # Action & Target Resource
    action: str
    resource_type: str
    resource_id: str
    resource_name: Optional[str] = None
    
    # Correlation & Provenance Hierarchy
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    
    # Execution & Risk Assessment
    severity: AuditSeverity = AuditSeverity.INFO
    outcome: OutcomeType = OutcomeType.SUCCESS
    status_code: Optional[int] = 200
    duration_ms: Optional[float] = None
    risk_score: float = 0.0
    
    # Governance & Evidence References
    policy_decision: Optional[str] = None
    compliance_controls: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    
    # Detailed Payloads & Metadata
    payload_summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Cryptographic Tamper-Evidence
    integrity_hash: Optional[str] = None
    previous_hash: Optional[str] = None
    signature: Optional[str] = None
