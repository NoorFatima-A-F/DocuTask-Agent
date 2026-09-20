"""
Event & Command Consumers.
"""

from typing import Callable, Coroutine
from app.agents.messaging.bus import EventBus
from app.agents.messaging.events import DomainEvent


class EventConsumer:
    """Consumer subscribing to EventBus events."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def consume(self, event_type: str, handler: Callable[[DomainEvent], Coroutine]) -> None:
        await self.event_bus.subscribe(event_type, handler)
