"""
Reflection Session Container.
Maintains stateful operational context, trace references, and staged learning artifacts during a reflection lifecycle.
"""

from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.lifecycle import ReflectionLifecycleState
from app.agents.reflection.metadata import ReflectionIdentity, ReflectionStatistics
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope


class ReflectionSession(BaseModel):
    """Encapsulates active state and staged artifacts for a running reflection job."""
    session_id: UUID = Field(default_factory=uuid4)
    identity: ReflectionIdentity
    trace: ExecutionTraceEnvelope
    lifecycle_state: ReflectionLifecycleState = Field(default=ReflectionLifecycleState.PENDING)
    staged_artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    staged_recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    staged_proposals: List[Dict[str, Any]] = Field(default_factory=list)
    evaluation_results: Dict[str, Any] = Field(default_factory=dict)
    critique_results: Dict[str, Any] = Field(default_factory=dict)
    feedback_payloads: Dict[str, Any] = Field(default_factory=dict)
    statistics: ReflectionStatistics = Field(default_factory=ReflectionStatistics)
    history: List[str] = Field(default_factory=list)

    def transition_to(self, new_state: ReflectionLifecycleState, reason: str = "") -> None:
        """Records state transition in session history."""
        self.history.append(f"Transitioned from {self.lifecycle_state.value} to {new_state.value}: {reason}")
        object.__setattr__(self, "lifecycle_state", new_state)

    def add_artifact(self, artifact_data: Dict[str, Any]) -> None:
        """Stages a newly generated learning artifact."""
        self.staged_artifacts.append(artifact_data)

    def add_recommendation(self, rec_data: Dict[str, Any]) -> None:
        """Stages an evidence-backed recommendation."""
        self.staged_recommendations.append(rec_data)
