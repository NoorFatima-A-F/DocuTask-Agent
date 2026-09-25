"""
Master Enterprise Timeline Engine.
Reconstructs complete chronological timeline histories purely from raw immutable events.
"""

from typing import Dict, List, Optional
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.timeline.timeline_index import TimelineEntry, TimelineIndex
from app.runtime.timeline.timeline_renderer import TimelineRenderer


class MasterTimelineEngine:
    """Singleton service for reconstructing timelines from event logs."""

    def __init__(self):
        self._timelines: Dict[str, List[TimelineEntry]] = {}
        self._indices: Dict[str, TimelineIndex] = {}

    def build_timeline_from_events(self, mission_id: str, events: List[RuntimeEvent]) -> List[TimelineEntry]:
        sorted_events = sorted(events, key=lambda e: (e.sequence_number, e.timestamp, e.event_id))
        index = TimelineIndex()
        entries: List[TimelineEntry] = []

        for idx, event in enumerate(sorted_events):
            entry = TimelineRenderer.render_event_to_entry(event, idx)
            entries.append(entry)
            index.index_entry(entry)

        self._timelines[mission_id] = entries
        self._indices[mission_id] = index
        return entries

    def get_timeline(self, mission_id: str) -> List[TimelineEntry]:
        return list(self._timelines.get(mission_id, []))

    def get_index(self, mission_id: str) -> Optional[TimelineIndex]:
        return self._indices.get(mission_id)
