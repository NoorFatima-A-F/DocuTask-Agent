"""
Timeline Index Subsystem.
Provides O(1) indexed lookup of timeline records by timestamp, stage, and event ID.
"""

from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field


class TimelineEntry(BaseModel):
    entry_id: str
    mission_id: str
    event_id: str
    sequence_number: int
    stage: str
    category: str
    event_type: str
    summary: str
    timestamp: str
    duration_ms: Optional[float] = None
    cost_usd: Optional[float] = None
    worker_id: Optional[str] = None
    hash: Optional[str] = None
    is_milestone: bool = False
    error: Optional[str] = None


class TimelineIndex:
    """Multi-dimensional index for fast timeline queries."""

    def __init__(self):
        self._entries_by_id: Dict[str, TimelineEntry] = {}
        self._entries_by_event_id: Dict[str, TimelineEntry] = {}
        self._entries_by_stage: Dict[str, List[str]] = {}  # stage -> List[entry_id]

    def index_entry(self, entry: TimelineEntry) -> None:
        self._entries_by_id[entry.entry_id] = entry
        self._entries_by_event_id[entry.event_id] = entry
        self._entries_by_stage.setdefault(entry.stage, []).append(entry.entry_id)

    def get_by_entry_id(self, entry_id: str) -> Optional[TimelineEntry]:
        return self._entries_by_id.get(entry_id)

    def get_by_event_id(self, event_id: str) -> Optional[TimelineEntry]:
        return self._entries_by_event_id.get(event_id)

    def get_by_stage(self, stage: str) -> List[TimelineEntry]:
        ids = self._entries_by_stage.get(stage, [])
        return [self._entries_by_id[eid] for eid in ids if eid in self._entries_by_id]
