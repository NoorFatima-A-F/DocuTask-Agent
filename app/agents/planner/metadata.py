"""
Planner Metadata, Evidence, and Candidate Models.
Provides strongly typed immutable models for planning traces, candidate plans, and decision evidence.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4
from pydantic import BaseModel, Field
from app.agents.planning.contracts import Plan


class PlanningEvidence(BaseModel):
    """Supporting evidence gathered from memory, tool capabilities, or decision evaluations."""
    evidence_id: str = Field(default_factory=lambda: str(uuid4()))
    source: str = Field(default="TOOL_REGISTRY")  # TOOL_REGISTRY, MEMORY, DECISION_ENGINE, LLM
    description: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    data: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class RejectedAlternative(BaseModel):
    """Candidate plan alternative that was evaluated and rejected."""
    plan_name: str
    rejection_reason: str
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class CandidatePlan(BaseModel):
    """Candidate plan generated during multi-strategy planning."""
    candidate_id: str = Field(default_factory=lambda: str(uuid4()))
    plan: Plan
    strategy_used: str = Field(default="HIERARCHICAL")
    rank_score: float = Field(default=0.5, ge=0.0, le=1.0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    estimated_duration_seconds: float = Field(default=0.0, ge=0.0)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class PlanningTrace(BaseModel):
    """Detailed audit trace of cognitive planning decisions."""
    trace_id: str = Field(default_factory=lambda: uuid4().hex)
    goal_id: str
    selected_strategy: str = Field(default="HIERARCHICAL")
    candidate_count: int = Field(default=1, ge=1)
    evidences: List[PlanningEvidence] = Field(default_factory=list)
    rejected_alternatives: List[RejectedAlternative] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"frozen": True}
