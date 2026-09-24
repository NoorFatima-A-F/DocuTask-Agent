"""
Learning Artifact Domain Models.
Defines immutable learning artifacts synthesized by reflection for memory promotion.
Reflection never updates Memory directly; it outputs immutable LearningArtifacts.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class LearningArtifactType(str, Enum):
    """Classification of learned knowledge artifacts."""
    DECOMPOSITION_STRATEGY = "DECOMPOSITION_STRATEGY"
    SCHEDULING_RECOMMENDATION = "SCHEDULING_RECOMMENDATION"
    TOOL_SELECTION = "TOOL_SELECTION"
    RETRY_POLICY = "RETRY_POLICY"
    PLANNER_HEURISTIC = "PLANNER_HEURISTIC"
    EXECUTION_STRATEGY = "EXECUTION_STRATEGY"
    FAILURE_AVOIDANCE_RULE = "FAILURE_AVOIDANCE_RULE"


class LearningArtifact(BaseModel):
    """
    Immutable learning artifact representing distilled procedural or declarative knowledge.
    Stored and provided as candidates for Memory promotion.
    """
    artifact_id: UUID = Field(default_factory=uuid4)
    artifact_type: LearningArtifactType
    title: str
    description: str
    heuristic_content: Dict[str, Any] = Field(default_factory=dict)
    conditions: List[str] = Field(default_factory=list)
    confidence_score: float = Field(default=0.9, ge=0.0, le=1.0)
    source_execution_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}  # Strictly immutable
