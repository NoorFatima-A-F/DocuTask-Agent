"""Event Processing, Deduplication, and Rate Throttling."""

from __future__ import annotations

import hashlib
import time
from typing import Dict, List, Optional

from ..core.events import EventCategory, PlatformEvent, EventStream


class EventProcessor:
    """Processes incoming platform events, deduplicates repetitive storms, and buffers streams."""

    def __init__(self, event_stream: Optional[EventStream] = None, dedup_window_seconds: float = 10.0):
        self.event_stream = event_stream or EventStream()
        self.dedup_window_seconds = dedup_window_seconds
        # dedup_key -> (first_seen, last_seen, count, event)
        self._dedup_cache: Dict[str, Dict[str, Any]] = {}

    def process(self, event: PlatformEvent) -> Optional[PlatformEvent]:
        """Ingest event, apply deduplication, and publish if new or threshold reached."""
        dedup_key = self._calculate_dedup_key(event)
        now = time.time()

        if dedup_key in self._dedup_cache:
            entry = self._dedup_cache[dedup_key]
            if (now - entry["first_seen"]) < self.dedup_window_seconds:
                entry["count"] += 1
                entry["last_seen"] = now
                # Suppress duplicate storm
                return None
            else:
                # Window expired, reset
                del self._dedup_cache[dedup_key]

        # New event or new window
        self._dedup_cache[dedup_key] = {
            "first_seen": now,
            "last_seen": now,
            "count": 1,
            "event": event,
        }
        self.event_stream.publish(event)
        return event

    def _calculate_dedup_key(self, event: PlatformEvent) -> str:
        raw = f"{event.category.value}:{event.name}:{event.severity}:{event.source}:{event.context.service_name}:{event.context.tenant_id}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def get_dedup_stats(self) -> Dict[str, int]:
        return {k: v["count"] for k, v in self._dedup_cache.items()}
