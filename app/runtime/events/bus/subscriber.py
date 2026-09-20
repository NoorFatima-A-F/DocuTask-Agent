"""
DocuTask Agent - Event Subscriber Interface
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

import asyncio
from typing import Callable, Awaitable, Optional, Set
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem

EventHandler = Callable[[DomainEvent], Awaitable[None]]


class EventSubscriber:
    """
    Asynchronous Event Subscriber.
    Receives filtered DomainEvents and processes them in FIFO order.
    """

    def __init__(
        self,
        subscriber_id: str,
        handler: EventHandler,
        event_types: Optional[Set[DomainEventType]] = None,
        subsystems: Optional[Set[EventSubsystem]] = None,
        max_queue_size: int = 1000,
    ):
        self.subscriber_id = subscriber_id
        self.handler = handler
        self.event_types = event_types
        self.subsystems = subsystems
        self.queue: asyncio.Queue[DomainEvent] = asyncio.Queue(maxsize=max_queue_size)
        self._is_running = False
        self._worker_task: Optional[asyncio.Task] = None
        self.delivered_count = 0

    def matches(self, event: DomainEvent) -> bool:
        """Determines if the event matches this subscriber's filter criteria."""
        if self.event_types and event.event_type not in self.event_types:
            return False
        if self.subsystems and event.subsystem not in self.subsystems:
            return False
        return True

    async def enqueue(self, event: DomainEvent) -> bool:
        """Enqueues an event for asynchronous processing."""
        if not self.matches(event):
            return False
        try:
            self.queue.put_nowait(event)
            return True
        except asyncio.QueueFull:
            return False

    async def start(self) -> None:
        """Starts the background worker queue consumer."""
        if self._is_running:
            return
        self._is_running = True
        self._worker_task = asyncio.create_task(self._process_queue())

    async def stop(self) -> None:
        """Gracefully stops the worker."""
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def _process_queue(self) -> None:
        while self._is_running:
            try:
                event = await self.queue.get()
                await self.handler(event)
                self.delivered_count += 1
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception:
                # Log error or send to dead-letter in production
                pass
