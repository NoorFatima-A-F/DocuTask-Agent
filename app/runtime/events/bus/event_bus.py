"""
DocuTask Agent - Asynchronous Publish-Subscribe Event Bus
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

import asyncio
from typing import Dict, List, Set, Optional, Callable, Awaitable
import time
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem
from app.runtime.events.bus.subscriber import EventSubscriber, EventHandler


class AsyncDomainEventBus:
    """
    Central Asynchronous Publish-Subscribe Event Bus.
    Routes all domain events between emitters, storage append-logs,
    read projections, and real-time streaming sockets.
    """

    def __init__(self):
        self._subscribers: Dict[str, EventSubscriber] = {}
        self._published_count = 0
        self._delivered_count = 0
        self._lock = asyncio.Lock()
        self._history: List[DomainEvent] = []
        self._max_in_memory_history = 1000

    def subscribe(
        self,
        subscriber_id: str,
        handler: EventHandler,
        event_types: Optional[Set[DomainEventType]] = None,
        subsystems: Optional[Set[EventSubsystem]] = None,
        max_queue_size: int = 1000,
    ) -> EventSubscriber:
        """Registers a new event subscriber."""
        subscriber = EventSubscriber(
            subscriber_id=subscriber_id,
            handler=handler,
            event_types=event_types,
            subsystems=subsystems,
            max_queue_size=max_queue_size,
        )
        self._subscribers[subscriber_id] = subscriber
        return subscriber

    def unsubscribe(self, subscriber_id: str) -> bool:
        """Removes a registered subscriber."""
        if subscriber_id in self._subscribers:
            del self._subscribers[subscriber_id]
            return True
        return False

    async def publish(self, event: DomainEvent) -> None:
        """Publishes a domain event to all matching subscribers."""
        async with self._lock:
            self._published_count += 1
            self._history.append(event)
            if len(self._history) > self._max_in_memory_history:
                self._history.pop(0)

        # Distribute concurrently to all subscribers
        tasks = []
        for sub in list(self._subscribers.values()):
            tasks.append(self._dispatch_to_subscriber(sub, event))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _dispatch_to_subscriber(self, sub: EventSubscriber, event: DomainEvent) -> None:
        if sub.matches(event):
            try:
                # If subscriber is running in queue mode, enqueue
                if sub._is_running:
                    await sub.enqueue(event)
                else:
                    # Direct async handler execution
                    await sub.handler(event)
                self._delivered_count += 1
            except Exception:
                # Protect bus from failing subscriber handlers
                pass

    def get_bus_stats(self) -> Dict[str, Any]:
        """Returns runtime performance statistics of the event bus."""
        return {
            "total_published": self._published_count,
            "total_delivered": self._delivered_count,
            "active_subscribers_count": len(self._subscribers),
            "subscribers": [
                {
                    "id": sub.subscriber_id,
                    "event_types": [et.value for et in sub.event_types] if sub.event_types else "ALL",
                    "subsystems": [ss.value for ss in sub.subsystems] if sub.subsystems else "ALL",
                    "delivered_count": sub.delivered_count,
                }
                for sub in self._subscribers.values()
            ],
            "buffered_history_count": len(self._history),
            "timestamp_utc": time.time(),
        }

    def publish_sync(self, event: DomainEvent) -> None:
        """Synchronously records event to in-memory history and increments count."""
        self._published_count += 1
        self._history.append(event)
        if len(self._history) > self._max_in_memory_history:
            self._history.pop(0)


# Global singleton domain event bus
domain_event_bus = AsyncDomainEventBus()


def get_global_event_bus() -> AsyncDomainEventBus:
    """Returns the global singleton domain event bus."""
    return domain_event_bus
