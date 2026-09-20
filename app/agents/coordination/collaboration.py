"""
Collaboration Engine and Patterns.
Supports supervisor-led, peer-to-peer, hierarchical, and pipeline collaboration patterns.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.collaboration_context import CollaborationContext
from app.agents.coordination.collaboration_session import CollaborationSession


class CollaborationPattern(str, Enum):
    """Architectural patterns for multi-agent collaboration."""
    SUPERVISOR_WORKER = "SUPERVISOR_WORKER"
    PEER_TO_PEER = "PEER_TO_PEER"
    SEQUENTIAL_PIPELINE = "SEQUENTIAL_PIPELINE"
    HIERARCHICAL_DELEGATION = "HIERARCHICAL_DELEGATION"
    SWARM_CONSENSUS = "SWARM_CONSENSUS"


class CollaborationManager:
    """Manages active collaboration sessions and context synchronization."""

    def __init__(self):
        self._sessions: Dict[UUID, CollaborationSession] = {}

    def create_session(
        self,
        goal: str,
        initiator_id: UUID,
        participants: List[UUID]
    ) -> CollaborationSession:
        """Initializes a new collaboration session."""
        session_id = uuid4()
        context = CollaborationContext(session_id=session_id)
        session = CollaborationSession(
            session_id=session_id,
            goal=goal,
            initiator_agent_id=initiator_id,
            participating_agent_ids=participants,
            context=context
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: UUID) -> Optional[CollaborationSession]:
        """Retrieves session by UUID."""
        return self._sessions.get(session_id)
