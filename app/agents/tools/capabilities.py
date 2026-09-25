"""
Capability Resolution Domain Models.
Provides Capability, CapabilityRequirement, CapabilityScore, and CapabilityMatch models for evaluating tool candidates.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Capability(BaseModel):
    """Specific capability specification."""
    name: str
    category: str = Field(default="GENERAL")
    level: str = Field(default="STANDARD")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class CapabilityRequirement(BaseModel):
    """Planner capability requirement query."""
    capability_name: str
    document_type: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None)
    min_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    max_cost_usd: Optional[float] = Field(default=None)
    max_latency_ms: Optional[float] = Field(default=None)
    preferred_provider: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class CapabilityScore(BaseModel):
    """Calculated fitness score for a capability match."""
    overall_score: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    cost_score: float = Field(default=1.0, ge=0.0, le=1.0)
    latency_score: float = Field(default=1.0, ge=0.0, le=1.0)
    health_score: float = Field(default=1.0, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class CapabilityMatch(BaseModel):
    """Ranked tool candidate matching a capability requirement."""
    tool_id: str
    tool_name: str
    provider_name: str
    score: CapabilityScore
    reasons: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
