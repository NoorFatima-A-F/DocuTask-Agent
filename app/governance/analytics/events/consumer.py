"""Governance Event Consumer for batch ingestion and stream handling."""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone
from .normalizers import GovernanceAnalyticsEvent, AnalyticsEventType, EventNormalizer
from .processors import EventProcessor


class GovernanceEventConsumer:
    """Consumes, buffers, and routes governance analytics events to downstream pipelines."""

    def __init__(self, processor: Optional[EventProcessor] = None):
        self.processor = processor or EventProcessor()
        self._handlers: List[Callable[[GovernanceAnalyticsEvent], None]] = []
        self._event_store: List[GovernanceAnalyticsEvent] = []

    def subscribe(self, handler: Callable[[GovernanceAnalyticsEvent], None]) -> None:
        self._handlers.append(handler)

    def ingest(self, raw_or_event: Any, event_type: Optional[AnalyticsEventType] = None) -> GovernanceAnalyticsEvent:
        """Ingests a single raw event or GovernanceAnalyticsEvent object."""
        if isinstance(raw_or_event, GovernanceAnalyticsEvent):
            event = raw_or_event
        elif isinstance(raw_or_event, dict):
            event = EventNormalizer.normalize_dict(raw_or_event, event_type=event_type)
        else:
            # Pydantic or object with model_dump or __dict__
            d = raw_or_event.model_dump() if hasattr(raw_or_event, "model_dump") else getattr(raw_or_event, "__dict__", {})
            event = EventNormalizer.normalize_dict(d, event_type=event_type)

        processed = self.processor.process(event)
        self._event_store.append(processed)

        for handler in self._handlers:
            handler(processed)

        return processed

    def ingest_batch(self, events: List[Any]) -> List[GovernanceAnalyticsEvent]:
        return [self.ingest(e) for e in events]

    def get_events(
        self,
        tenant_id: Optional[str] = None,
        event_type: Optional[AnalyticsEventType] = None,
        limit: int = 1000,
    ) -> List[GovernanceAnalyticsEvent]:
        res = self._event_store
        if tenant_id and tenant_id != "*":
            res = [e for e in res if e.tenant_id == tenant_id]
        if event_type:
            res = [e for e in res if e.event_type == event_type]
        return res[-limit:]
