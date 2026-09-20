"""
Event Density for Phase 13.4.
Calculates event frequency buckets along mission replay timeline.
"""

from typing import Dict, Any, List


class EventDensityCalculator:
    """
    Computes time-bucketed event densities for timeline histograms.
    """

    @classmethod
    def calculate_density(
        cls,
        events: List[Dict[str, Any]],
        bucket_count: int = 10,
    ) -> List[Dict[str, Any]]:
        if not events:
            return []

        chunk_size = max(1, len(events) // bucket_count)
        buckets = []

        for i in range(0, len(events), chunk_size):
            chunk = events[i : i + chunk_size]
            buckets.append({
                "bucket_index": len(buckets),
                "start_cursor": i,
                "end_cursor": min(len(events) - 1, i + len(chunk) - 1),
                "event_count": len(chunk),
                "subsystems": list({e.get("event_type", "").split(".")[0] for e in chunk if "." in e.get("event_type", "")}),
            })

        return buckets
