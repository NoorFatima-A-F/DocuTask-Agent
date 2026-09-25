"""
Event & Command Publishers.
"""

from app.agents.messaging.bus import EventBus
from app.agents.messaging.events import DomainEvent


class EventPublisher:
    """Publisher publishing events to EventBus."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def publish(self, event: DomainEvent) -> None:
        await self.event_bus.publish(event)
