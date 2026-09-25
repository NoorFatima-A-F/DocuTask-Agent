"""
Runtime Repository.
Provides storage abstraction and in-memory implementation for runtime sessions, states, and telemetry logs.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID
from app.agents.runtime.runtime_session import RuntimeSession
from app.agents.runtime.runtime_state import RuntimeState


class IRuntimeRepository(ABC):
    """Abstract storage for runtime execution sessions and kernel state."""

    @abstractmethod
    async def save_session(self, session: RuntimeSession) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_session(self, session_id: UUID) -> Optional[RuntimeSession]:
        raise NotImplementedError

    @abstractmethod
    async def list_active_sessions(self) -> List[RuntimeSession]:
        raise NotImplementedError

    @abstractmethod
    async def save_state(self, state: RuntimeState) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_state(self) -> Optional[RuntimeState]:
        raise NotImplementedError


class InMemoryRuntimeRepository(IRuntimeRepository):
    """In-memory storage for development, testing, and single-node runtime execution."""

    def __init__(self) -> None:
        self._sessions: Dict[UUID, RuntimeSession] = {}
        self._state: Optional[RuntimeState] = None

    async def save_session(self, session: RuntimeSession) -> None:
        self._sessions[session.session_id] = session

    async def get_session(self, session_id: UUID) -> Optional[RuntimeSession]:
        return self._sessions.get(session_id)

    async def list_active_sessions(self) -> List[RuntimeSession]:
        return [s for s in self._sessions.values() if s.status == "ACTIVE"]

    async def save_state(self, state: RuntimeState) -> None:
        self._state = state

    async def get_state(self) -> Optional[RuntimeState]:
        return self._state
