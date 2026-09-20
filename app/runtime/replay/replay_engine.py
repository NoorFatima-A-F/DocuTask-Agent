"""
Master Replay Engine for Event-Sourced Mission Replay.
Provides high-level session management and API integrations.
"""

from typing import Dict, List, Optional
from app.runtime.observability.event_store import EventStore
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_runtime import ReplayRuntimeSession
from app.runtime.replay.replay_builder import ReplayStreamBuilder
from app.runtime.replay.replay_filters import ReplayFilterCriteria


class MasterReplayEngine:
    """Singleton coordinator for enterprise mission replays."""

    def __init__(self, event_store: Optional[EventStore] = None):
        self.event_store = event_store or EventStore()
        self._active_sessions: Dict[str, ReplayRuntimeSession] = {}

    async def get_or_create_session(
        self,
        mission_id: str,
        criteria: Optional[ReplayFilterCriteria] = None,
        force_reload: bool = False,
    ) -> ReplayRuntimeSession:
        """Retrieves or initializes a replay session from EventStore."""
        if not force_reload and mission_id in self._active_sessions:
            return self._active_sessions[mission_id]

        events = await ReplayStreamBuilder.build_stream_from_store(
            event_store=self.event_store,
            mission_id=mission_id,
            criteria=criteria,
        )

        session = ReplayRuntimeSession(mission_id=mission_id, events=events)
        self._active_sessions[mission_id] = session
        return session

    def create_in_memory_session(
        self,
        mission_id: str,
        events: List[RuntimeEvent],
        criteria: Optional[ReplayFilterCriteria] = None,
    ) -> ReplayRuntimeSession:
        """Initializes a replay session directly from an in-memory event list."""
        sorted_events = ReplayStreamBuilder.build_stream_from_list(events, criteria)
        session = ReplayRuntimeSession(mission_id=mission_id, events=sorted_events)
        self._active_sessions[mission_id] = session
        return session

    def close_session(self, mission_id: str) -> None:
        if mission_id in self._active_sessions:
            self._active_sessions[mission_id].pause()
            del self._active_sessions[mission_id]
