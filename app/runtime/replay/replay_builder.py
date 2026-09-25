"""
Replay Stream Builder.
Assembles raw immutable event logs from EventStore into ordered, indexed replay streams.
"""

from typing import List, Optional
from app.runtime.observability.event_store import EventStore
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.replay.replay_filters import ReplayFilterCriteria, ReplayFilterEngine


class ReplayStreamBuilder:
    """Constructs sorted, filtered event logs for deterministic replay."""

    @staticmethod
    async def build_stream_from_store(
        event_store: EventStore,
        mission_id: str,
        criteria: Optional[ReplayFilterCriteria] = None,
    ) -> List[RuntimeEvent]:
        """Loads events for a mission from EventStore and sorts by sequence and timestamp."""
        if hasattr(event_store, "get_events_by_mission"):
            res = event_store.get_events_by_mission(mission_id)
        elif hasattr(event_store, "get_events_for_mission"):
            res = event_store.get_events_for_mission(mission_id)
        else:
            res = []
        import inspect
        if inspect.iscoroutine(res):
            raw_events = await res
        else:
            raw_events = res
        # Ensure chronological and sequence index ordering
        sorted_events = sorted(
            raw_events,
            key=lambda e: (e.sequence_number, e.timestamp, e.event_id),
        )
        return ReplayFilterEngine.apply_filters(sorted_events, criteria)

    @staticmethod
    def build_stream_from_list(
        events: List[RuntimeEvent],
        criteria: Optional[ReplayFilterCriteria] = None,
    ) -> List[RuntimeEvent]:
        """Prepares a list of in-memory events for deterministic replay."""
        sorted_events = sorted(
            events,
            key=lambda e: (e.sequence_number, e.timestamp, e.event_id),
        )
        return ReplayFilterEngine.apply_filters(sorted_events, criteria)
