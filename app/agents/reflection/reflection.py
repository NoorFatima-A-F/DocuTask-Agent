"""
Reflection Aggregate Root.
Represents the comprehensive reflection analysis entity for an individual execution.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.lifecycle import ReflectionLifecycleState
from app.agents.reflection.metadata import ReflectionIdentity, ReflectionMetadata, ReflectionStatistics


class Reflection(BaseModel):
    """
    Core Domain Aggregate for Reflection.
    Encapsulates evaluation metrics, self-critique, synthesized learning artifacts,
    recommendations, and feedback for an executed goal.
    """
    identity: ReflectionIdentity
    metadata: ReflectionMetadata = Field(default_factory=ReflectionMetadata)
    state: ReflectionLifecycleState = Field(default=ReflectionLifecycleState.PENDING)
    statistics: ReflectionStatistics = Field(default_factory=ReflectionStatistics)
    evaluation_report: Optional[Dict[str, Any]] = None
    critique_data: Optional[Dict[str, Any]] = None
    learning_artifact_ids: List[UUID] = Field(default_factory=list)
    recommendation_ids: List[UUID] = Field(default_factory=list)
    adaptation_proposal_ids: List[UUID] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    def mark_evaluating(self) -> "Reflection":
        """Transitions state to EVALUATING."""
        return self.model_copy(update={"state": ReflectionLifecycleState.EVALUATING})

    def mark_critiquing(self) -> "Reflection":
        """Transitions state to CRITIQUING."""
        return self.model_copy(update={"state": ReflectionLifecycleState.CRITIQUING})

    def mark_extracting(self) -> "Reflection":
        """Transitions state to EXTRACTING."""
        return self.model_copy(update={"state": ReflectionLifecycleState.EXTRACTING})

    def mark_recommending(self) -> "Reflection":
        """Transitions state to RECOMMENDING."""
        return self.model_copy(update={"state": ReflectionLifecycleState.RECOMMENDING})

    def mark_completed(self, stats: Optional[ReflectionStatistics] = None) -> "Reflection":
        """Marks reflection successfully completed."""
        updates: Dict[str, Any] = {"state": ReflectionLifecycleState.COMPLETED}
        if stats:
            updates["statistics"] = stats
        return self.model_copy(update=updates)

    def mark_failed(self, error: str) -> "Reflection":
        """Marks reflection as failed with error."""
        return self.model_copy(update={
            "state": ReflectionLifecycleState.FAILED,
            "errors": [*self.errors, error]
        })
