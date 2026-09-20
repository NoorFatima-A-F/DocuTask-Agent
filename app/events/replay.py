"""
Event Replay Engine.
Replays past events from event history/store through the Event Bus.
"""

from typing import List, Optional
from .bus import EventBus
from .models import CloudEventEnvelope


class EventReplayEngine:
    """Replays historical events with optional type or tenant filtering."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def replay(
        self,
        event_type_filter: Optional[str] = None,
        tenant_filter: Optional[str] = None,
    ) -> int:
        """Replay stored events matching filters. Returns count of replayed events."""
        history = self.event_bus.get_history()
        count = 0
        for event in history:
            if event_type_filter and event.type != event_type_filter:
                continue
            if tenant_filter and event.tenant != tenant_filter:
                continue
            await self.event_bus.publish(event)
            count += 1
        return count
