"""
Timeline Renderer.
Transforms raw RuntimeEvents into structured TimelineEntry items with duration metrics and hash badges.
"""

from app.runtime.observability.schemas import RuntimeEvent, EventCategory
from app.runtime.timeline.timeline_index import TimelineEntry


class TimelineRenderer:
    @staticmethod
    def render_event_to_entry(event: RuntimeEvent, index: int) -> TimelineEntry:
        cat_str = event.category.value if hasattr(event.category, "value") else str(event.category)
        type_str = event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)

        summary = event.payload.get("summary", event.payload.get("message", f"Event '{type_str}' in stage '{event.stage}'"))
        dur = float(event.payload["duration_ms"]) if "duration_ms" in event.payload else None
        cost = float(event.payload.get("cost_usd", event.payload.get("amount", 0.0))) if ("cost_usd" in event.payload or "amount" in event.payload) else None

        is_milestone = (
            event.category == EventCategory.MISSION
            or "mutation" in type_str.lower()
            or "failed" in type_str.lower()
            or "recovery" in type_str.lower()
            or "human" in cat_str.lower()
        )

        return TimelineEntry(
            entry_id=f"tl_{event.mission_id}_{index}",
            mission_id=event.mission_id,
            event_id=event.event_id,
            sequence_number=event.sequence_number,
            stage=event.stage,
            category=cat_str,
            event_type=type_str,
            summary=summary,
            timestamp=str(event.timestamp),
            duration_ms=dur,
            cost_usd=cost,
            worker_id=event.worker_id,
            hash=event.hash,
            is_milestone=is_milestone,
            error=event.payload.get("error"),
        )
