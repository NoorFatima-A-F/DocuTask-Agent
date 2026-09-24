"""Incident Timeline and Action Log Tracking."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TimelineEventType(str, Enum):
    DETECTION = "DETECTION"
    STATUS_CHANGE = "STATUS_CHANGE"
    MITIGATION_ACTION = "MITIGATION_ACTION"
    NOTE = "NOTE"
    METRIC_SPIKE = "METRIC_SPIKE"


@dataclass
class TimelineEntry:
    entry_id: str
    timestamp: float
    author: str
    event_type: TimelineEventType
    message: str


class IncidentTimeline:
    """Manages chronological timeline records during active incidents and postmortems."""

    def __init__(self):
        self._entries: List[TimelineEntry] = []

    def add_entry(
        self,
        author: str,
        event_type: TimelineEventType,
        message: str,
        timestamp: Optional[float] = None,
    ) -> TimelineEntry:
        entry = TimelineEntry(
            entry_id=f"tl-{uuid.uuid4().hex[:8]}",
            timestamp=timestamp or time.time(),
            author=author,
            event_type=event_type,
            message=message,
        )
        self._entries.append(entry)
        self._entries.sort(key=lambda e: e.timestamp)
        return entry

    def list_entries(self) -> List[TimelineEntry]:
        return list(self._entries)

    def to_markdown(self) -> str:
        lines = ["### Incident Chronology", "| Time (UTC) | Author | Type | Description |", "|---|---|---|---|"]
        for e in self._entries:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(e.timestamp))
            lines.append(f"| {time_str} | {e.author} | `{e.event_type.value}` | {e.message} |")
        return "\n".join(lines)
