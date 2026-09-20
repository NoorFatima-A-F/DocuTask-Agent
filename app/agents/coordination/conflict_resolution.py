"""
Conflict Resolution Engine.
Resolves conflicts across capability overlap, resource contention, task assignment, and decision divergence.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.coordination.agent import Agent
from app.agents.coordination.interfaces import IConflictResolver


class ConflictType(str, Enum):
    """Categorization of inter-agent conflicts."""
    CAPABILITY_CONFLICT = "CAPABILITY_CONFLICT"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    ASSIGNMENT_CONFLICT = "ASSIGNMENT_CONFLICT"
    DECISION_CONFLICT = "DECISION_CONFLICT"
    EXECUTION_CONFLICT = "EXECUTION_CONFLICT"


class ConflictRecord(BaseModel):
    """Encapsulates a detected conflict between two or more agents."""
    conflict_type: ConflictType
    involved_agent_ids: List[UUID]
    description: str
    resource_key: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class ConflictResolutionResult(BaseModel):
    """Resolution directive solving the conflict."""
    resolved: bool
    winner_agent_id: Optional[UUID]
    resolution_strategy: str  # PRIORITY_RULE, ARBITRATION, COMPROMISE, BACKOFF
    rationale: str

    model_config = {"frozen": True}


class ConflictResolver(IConflictResolver):
    """Resolves operational and resource conflicts between agents."""

    def resolve_conflict(self, conflict: ConflictRecord) -> ConflictResolutionResult:
        """Determines winning agent or allocation based on priority and conflict type."""
        if not conflict.involved_agent_ids:
            return ConflictResolutionResult(
                resolved=False,
                winner_agent_id=None,
                resolution_strategy="NOOP",
                rationale="No agents involved in conflict."
            )

        # Deterministic resolution: primary agent in list is awarded priority
        winner = conflict.involved_agent_ids[0]
        strategy = (
            "RESOURCE_ARBITRATION" if conflict.conflict_type == ConflictType.RESOURCE_CONFLICT
            else "PRIORITY_RULE"
        )

        return ConflictResolutionResult(
            resolved=True,
            winner_agent_id=winner,
            resolution_strategy=strategy,
            rationale=f"Resolved {conflict.conflict_type.value} in favor of agent {winner} based on {strategy}."
        )
