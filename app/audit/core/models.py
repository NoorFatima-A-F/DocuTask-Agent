"""Specific Domain Context Models for Actors, Resources, AI Contexts, and Policies."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .events import ActorType


class AuditActor(BaseModel):
    actor_id: str
    actor_type: ActorType = ActorType.USER
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditResource(BaseModel):
    resource_type: str  # e.g., "workflow", "model", "prompt", "document", "policy"
    resource_id: str
    name: Optional[str] = None
    version: Optional[str] = None
    data_classification: Optional[str] = "INTERNAL"


class PolicyContext(BaseModel):
    policy_id: Optional[str] = None
    policy_name: Optional[str] = None
    rule_evaluated: Optional[str] = None
    decision: str = "ALLOW"  # ALLOW, BLOCK, REQUIRE_HUMAN, REDACT
    reason: Optional[str] = None


class AIExecutionAuditContext(BaseModel):
    model_id: str
    model_version: Optional[str] = None
    prompt_id: Optional[str] = None
    prompt_version: Optional[str] = None
    temperature: Optional[float] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_cost_usd: Optional[float] = None
    latency_ms: Optional[float] = None
    grounding_score: Optional[float] = None
    tool_calls: List[str] = Field(default_factory=list)
    knowledge_chunk_ids: List[str] = Field(default_factory=list)


class DataAuditEventContext(BaseModel):
    asset_id: str
    operation: str  # READ, WRITE, TRANSFORM, EXPORT, DELETE
    data_classification: str = "INTERNAL"
    pii_types_detected: List[str] = Field(default_factory=list)
    row_count: Optional[int] = None
    byte_size: Optional[int] = None
