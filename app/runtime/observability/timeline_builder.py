"""
ARTEICP Observability - Mission Timeline Builder
Constructs high-precision chronological execution timelines directly from immutable runtime event streams.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
import time


@dataclass
class TimelineEntry:
    event_id: str
    mission_id: str
    timestamp_utc: str
    relative_time_ms: float
    category: str  # PLANNER | WORKER | RETRY | REFLECTION | MEMORY | VALIDATION | GOVERNANCE
    title: str
    summary: str
    actor: str
    duration_ms: Optional[float] = None
    confidence_score: Optional[float] = None
    cost_usd: Optional[float] = None
    evidence_ref: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TimelineBuilder:
    """Builds sub-millisecond sorted chronological execution timelines from real runtime events."""

    @classmethod
    def build_timeline_from_events(
        cls,
        mission_id: str,
        raw_events: List[Dict[str, Any]],
    ) -> List[TimelineEntry]:
        if not raw_events:
            return []

        # Sort chronologically by timestamp
        sorted_events = sorted(
            raw_events,
            key=lambda e: float(e.get("timestamp", e.get("timestamp_utc", 0.0)) if isinstance(e.get("timestamp", 0.0), (int, float)) else 0.0)
        )

        base_time = float(sorted_events[0].get("timestamp", time.time())) if sorted_events else time.time()
        timeline: List[TimelineEntry] = []

        for idx, ev in enumerate(sorted_events):
            t_val = float(ev.get("timestamp", base_time)) if isinstance(ev.get("timestamp"), (int, float)) else base_time
            rel_ms = max(0.0, round((t_val - base_time) * 1000.0, 2))

            ev_type = ev.get("event_type", ev.get("type", "RUNTIME_EVENT"))
            payload = ev.get("payload", ev.get("data", {}))

            # Determine category
            category = "WORKER"
            if "PLAN" in ev_type:
                category = "PLANNER"
            elif "RETRY" in ev_type:
                category = "RETRY"
            elif "REFLECT" in ev_type:
                category = "REFLECTION"
            elif "MEMORY" in ev_type:
                category = "MEMORY"
            elif "VALIDAT" in ev_type:
                category = "VALIDATION"
            elif "GOVERN" in ev_type or "CERT" in ev_type:
                category = "GOVERNANCE"

            entry = TimelineEntry(
                event_id=ev.get("event_id", f"ev_tm_{idx}"),
                mission_id=mission_id,
                timestamp_utc=ev.get("timestamp_utc", datetime.now(timezone.utc).isoformat()),
                relative_time_ms=rel_ms,
                category=category,
                title=ev.get("title", f"{ev_type.replace('_', ' ').title()}"),
                summary=ev.get("summary", payload.get("message", f"Executed {ev_type}")),
                actor=ev.get("actor", payload.get("worker_id", "DocuTask-Orchestrator")),
                duration_ms=payload.get("duration_ms", payload.get("latency_ms")),
                confidence_score=payload.get("confidence", payload.get("confidence_score")),
                cost_usd=payload.get("cost_usd"),
                evidence_ref=payload.get("evidence_ref", payload.get("hash")),
                payload=payload,
            )
            timeline.append(entry)

        return timeline
