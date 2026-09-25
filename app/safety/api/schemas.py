"""API Request and Response Schemas for Safety Control Plane."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from ..gateway.context import SourceTrustLevel, KnowledgeChunk
from ..gateway.decision import SafetyStatus, ViolationSeverity, SafetyCategory, SafetyViolation
from ..incidents.lifecycle import IncidentLifecycleState


class GuardInputRequest(BaseModel):
    tenant_id: str
    raw_input: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    source_trust: SourceTrustLevel = SourceTrustLevel.USER
    model_id: Optional[str] = None
    knowledge_chunks: List[KnowledgeChunk] = Field(default_factory=list)


class GuardInputResponse(BaseModel):
    decision_id: str
    is_allowed: bool
    status: SafetyStatus
    sanitized_input: Optional[str] = None
    composite_risk_score: float
    violations: List[SafetyViolation] = Field(default_factory=list)
    explanation: Optional[str] = None


class GuardOutputRequest(BaseModel):
    tenant_id: str
    generated_output: str
    system_prompt: Optional[str] = None
    knowledge_chunks: List[KnowledgeChunk] = Field(default_factory=list)


class GuardOutputResponse(BaseModel):
    decision_id: str
    is_allowed: bool
    status: SafetyStatus
    sanitized_output: Optional[str] = None
    composite_risk_score: float
    violations: List[SafetyViolation] = Field(default_factory=list)
    explanation: Optional[str] = None


class ValidateToolRequest(BaseModel):
    tenant_id: str
    tool_name: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    user_role: str = "user"
    is_dry_run: bool = False


class ValidateToolResponse(BaseModel):
    is_allowed: bool
    status: SafetyStatus
    violations: List[SafetyViolation] = Field(default_factory=list)
    explanation: Optional[str] = None


class VerifyGroundingRequest(BaseModel):
    output_text: str
    knowledge_chunks: List[KnowledgeChunk] = Field(default_factory=list)


class VerifyGroundingResponse(BaseModel):
    is_grounded: bool
    grounding_score: float
    total_claims: int
    grounded_claims: int
    citations_mapped: List[str] = Field(default_factory=list)


class IncidentCreateRequest(BaseModel):
    tenant_id: str
    title: str
    description: str
    category: SafetyCategory
    severity: ViolationSeverity
    context_id: Optional[str] = None
    user_id: Optional[str] = None
    agent_id: Optional[str] = None


class IncidentTransitionRequest(BaseModel):
    new_state: IncidentLifecycleState
    actor: str
    notes: Optional[str] = None
