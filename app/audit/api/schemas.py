"""API Request and Response Schemas for Audit Control Plane."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from ..core.events import ActorType, AuditSeverity, OutcomeType, EventCategory
from ..compliance.frameworks import ComplianceFramework
from ..evidence.artifacts import EvidenceType
from ..investigations.cases import CaseLifecycleState


class CreateEventRequest(BaseModel):
    event_type: str
    category: EventCategory = EventCategory.SYSTEM
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    environment: str = "production"
    
    actor_id: str
    actor_type: ActorType = ActorType.USER
    actor_name: Optional[str] = None
    
    action: str
    resource_type: str
    resource_id: str
    
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    
    severity: AuditSeverity = AuditSeverity.INFO
    outcome: OutcomeType = OutcomeType.SUCCESS
    risk_score: float = 0.0
    payload_summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VerifyIntegrityRequest(BaseModel):
    tenant_id: str


class CreateArtifactRequest(BaseModel):
    tenant_id: str
    name: str
    evidence_type: EvidenceType
    source: str
    content: str
    related_event_ids: List[str] = Field(default_factory=list)
    classification: str = "CONFIDENTIAL"


class CreateBundleRequest(BaseModel):
    tenant_id: str
    title: str
    purpose: str
    generated_by: str = "compliance_officer"
    correlation_id: Optional[str] = None
    event_ids: Optional[List[str]] = None
    artifact_ids: Optional[List[str]] = None


class EvaluateComplianceRequest(BaseModel):
    tenant_id: str
    framework: ComplianceFramework


class CreateInvestigationCaseRequest(BaseModel):
    tenant_id: str
    title: str
    summary: str
    severity: str = "HIGH"
    assigned_to: Optional[str] = None
    event_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)


class TransitionCaseRequest(BaseModel):
    new_state: CaseLifecycleState
    actor: str
    notes: Optional[str] = None
