"""
Reflection Manager.
Manages reflection sessions, cache lookups, persistent storage, and lifecycle tracking.
"""

from typing import Dict, Optional
from uuid import UUID, uuid4
from app.agents.reflection.cache import ReflectionCache
from app.agents.reflection.metadata import ReflectionIdentity
from app.agents.reflection.reflection import Reflection
from app.agents.reflection.reflection_context import ExecutionTraceEnvelope
from app.agents.reflection.reflection_session import ReflectionSession
from app.agents.reflection.repository import InMemoryReflectionRepository, IReflectionRepository


class ReflectionManager:
    """Manages reflection lifecycle, caching, and repository operations."""

    def __init__(
        self,
        repository: Optional[IReflectionRepository] = None,
        cache: Optional[ReflectionCache] = None
    ):
        self.repository = repository or InMemoryReflectionRepository()
        self.cache = cache or ReflectionCache()
        self._active_sessions: Dict[UUID, ReflectionSession] = {}

    def create_session(self, trace: ExecutionTraceEnvelope) -> ReflectionSession:
        """Creates and tracks a new reflection session for a trace."""
        session = ReflectionSession(
            session_id=uuid4(),
            identity=ReflectionIdentity(execution_id=trace.execution_id),
            trace=trace
        )
        self._active_sessions[session.session_id] = session
        return session

    def get_session(self, session_id: UUID) -> Optional[ReflectionSession]:
        """Retrieves active session by id."""
        return self._active_sessions.get(session_id)

    async def persist_reflection(self, reflection: Reflection) -> None:
        """Persists reflection aggregate and caches by execution_id."""
        await self.repository.save(reflection)
        self.cache.put(str(reflection.identity.execution_id), reflection)

    async def get_by_execution_id(self, execution_id: UUID) -> Optional[Reflection]:
        """Retrieves reflection with cache fallback."""
        cached = self.cache.get(str(execution_id))
        if cached:
            return cached
        if isinstance(self.repository, InMemoryReflectionRepository):
            return await self.repository.get_by_execution_id(execution_id)
        return None
