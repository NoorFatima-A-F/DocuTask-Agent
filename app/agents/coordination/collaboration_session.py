"""
Collaboration Session.
Maintains stateful operational context, participating agents, and communication channels for collaborative work.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.collaboration_context import CollaborationContext


class CollaborationSession(BaseModel):
    """Session container tracking multi-agent collaboration on a shared goal."""
    session_id: UUID = Field(default_factory=uuid4)
    goal: str
    initiator_agent_id: UUID
    participating_agent_ids: List[UUID] = Field(default_factory=list)
    context: CollaborationContext
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_participant(self, agent_id: UUID) -> "CollaborationSession":
        """Adds an agent to the collaboration session."""
        if agent_id not in self.participating_agent_ids:
            return self.model_copy(update={
                "participating_agent_ids": [*self.participating_agent_ids, agent_id]
            })
        return self

    def close_session(self) -> "CollaborationSession":
        """Closes the collaboration session."""
        return self.model_copy(update={"is_active": False})
