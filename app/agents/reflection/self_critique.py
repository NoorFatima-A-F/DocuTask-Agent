"""
Self-Critique Domain Models.
Defines models capturing introspective critique, discovered errors, reasoning gaps, and opportunities.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CritiqueFinding(BaseModel):
    """An individual critical finding regarding planner, reasoning, or execution behavior."""
    finding_id: UUID = Field(default_factory=uuid4)
    category: str  # HALLUCINATION, INCONSISTENCY, SUBOPTIMAL_PLAN, RESOURCE_WASTE, UNCHECKED_ASSUMPTION, BIAS
    severity: str = Field(default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    evidence: List[str] = Field(default_factory=list)
    impact: str = Field(default="")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    suggested_correction: Optional[str] = None

    model_config = {"frozen": True}


class SelfCritique(BaseModel):
    """Structured introspection and critique output produced by the reflection engine."""
    critique_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    findings: List[CritiqueFinding] = Field(default_factory=list)
    missed_opportunities: List[str] = Field(default_factory=list)
    improvement_opportunities: List[str] = Field(default_factory=list)
    confidence_explanation: str = Field(default="")
    uncertainty_analysis: Dict[str, Any] = Field(default_factory=dict)
    overall_critique_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
