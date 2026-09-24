"""
Event Sampling and Windowing Engine for Runtime Metrics.
Provides deterministic window slicing: sliding count, sliding time, tumbling, and session windows.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from app.runtime.events.base import RuntimeEvent
from app.runtime.metrics.definitions import SamplingRule


class EventSampler:
    """
    Samples and filters RuntimeEvents according to explicit SamplingRules.
    """

    @staticmethod
    def sample_events(
        events: List[RuntimeEvent],
        rule: SamplingRule,
        reference_time: Optional[datetime] = None,
    ) -> List[RuntimeEvent]:
        """
        Applies filtering and windowing to raw event stream.
        """
        if not events:
            return []

        # 1. Filter by event type if specified
        filtered = events
        if rule.filter_event_types:
            filtered = [e for e in filtered if e.event_type in rule.filter_event_types]

        # 2. Filter by agent ID if specified
        if rule.filter_agent_ids:
            filtered = [
                e for e in filtered
                if e.agent_id in rule.filter_agent_ids or e.worker_id in rule.filter_agent_ids
            ]

        if not filtered:
            return []

        # Sort chronologically by sequence number
        sorted_events = sorted(filtered, key=lambda e: (e.timestamp, e.sequence_number))

        # 3. Apply windowing
        if rule.window_type == "SLIDING_COUNT":
            return sorted_events[-rule.window_size:]

        elif rule.window_type == "SLIDING_TIME":
            now = reference_time or (
                sorted_events[-1].timestamp if sorted_events else datetime.now(timezone.utc)
            )
            cutoff = now - timedelta(seconds=rule.window_size)
            return [e for e in sorted_events if e.timestamp >= cutoff]

        elif rule.window_type == "TUMBLING":
            # Tumbling window bucket based on sequence number batches
            batch_size = max(1, rule.window_size)
            rem = len(sorted_events) % batch_size
            start_idx = max(0, len(sorted_events) - (batch_size if rem == 0 else rem))
            return sorted_events[start_idx:]

        # ALL_SESSION / default
        return sorted_events

    @staticmethod
    def get_observation_window(events: List[RuntimeEvent]) -> Dict[str, Any]:
        """
        Returns exact start, end, and duration_seconds for a sampled event list.
        """
        if not events:
            return {
                "start_utc": None,
                "end_utc": None,
                "duration_seconds": 0.0,
                "event_count": 0,
            }

        sorted_by_time = sorted(events, key=lambda e: e.timestamp)
        start_t = sorted_by_time[0].timestamp
        end_t = sorted_by_time[-1].timestamp
        delta = (end_t - start_t).total_seconds()

        return {
            "start_utc": start_t.isoformat(),
            "end_utc": end_t.isoformat(),
            "duration_seconds": max(0.001, delta),
            "event_count": len(events),
        }
