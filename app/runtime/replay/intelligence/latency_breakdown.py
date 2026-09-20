"""
Latency Breakdown for Phase 13.4.
Decomposes mission latency by subsystem, worker, and task execution stage.
"""

from typing import Dict, Any, List


class LatencyBreakdownEngine:
    """
    Computes latency distributions across subsystems during replay.
    """

    @classmethod
    def analyze_latencies(cls, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        breakdown: Dict[str, float] = {}
        total = 0.0

        for ev in events:
            payload = ev.get("payload", {})
            dur = float(payload.get("duration_ms", 0.0))
            if dur > 0:
                sub = payload.get("subsystem") or ev.get("event_type", "").split(".")[0] or "core"
                breakdown[sub] = breakdown.get(sub, 0.0) + dur
                total += dur

        proportions = {}
        for sub, dur in breakdown.items():
            proportions[sub] = round((dur / total * 100) if total > 0 else 0.0, 1)

        return {
            "total_duration_ms": round(total, 2),
            "subsystem_latencies_ms": {k: round(v, 2) for k, v in breakdown.items()},
            "subsystem_proportions_pct": proportions,
        }
