"""
Memory Feedback Contracts.
Produces Memory Update Requests and feedback for promoting, consolidating, or pruning memories.
Reflection never updates Memory directly.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.learning_artifact import LearningArtifact


class MemoryUpdateRequest(BaseModel):
    """Explicit request payload for Memory Subsystem to promote an artifact to long-term memory."""
    request_id: UUID = Field(default_factory=uuid4)
    target_tier: str = "REFLECTION"  # WORKING, EPISODIC, SEMANTIC, PROCEDURAL, REFLECTION
    artifact: LearningArtifact
    promotion_rationale: str
    relevance_tags: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class MemoryFeedback(BaseModel):
    """Structured feedback directed to Memory Manager regarding consolidation and retention."""
    feedback_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    update_requests: List[MemoryUpdateRequest] = Field(default_factory=list)
    items_to_prune: List[str] = Field(default_factory=list)
    context_efficiency_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}
