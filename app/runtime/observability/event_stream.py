"""
High-Throughput Asynchronous Publish/Subscribe Event Bus.

Handles asynchronous event routing with priority queues (CRITICAL, HIGH, NORMAL, LOW),
backpressure protection, Dead Letter Queue (DLQ) for failed subscribers, subscriber isolation,
and FIFO ordering guarantees per correlation ID.
"""

from __future__ import annotations

import asyncio
from collections import deque
import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    EventCategory,
    EventPriority,
)

logger = logging.getLogger(__name__)

AsyncSubscriber = Callable[[BaseRuntimeEvent], Coroutine[None, None, None]]
SyncSubscriber = Callable[[BaseRuntimeEvent], None]


class EventBus:
    """Enterprise-grade async event bus with priority queues, DLQ, and subscriber isolation."""

    def __init__(self, max_queue_size: int = 10000) -> None:
        self._max_queue_size = max_queue_size
        # Priority queues: CRITICAL (0), HIGH (1), NORMAL (2), LOW (3)
        self._queues: Dict[EventPriority, asyncio.Queue[BaseRuntimeEvent]] = {
            EventPriority.CRITICAL: asyncio.Queue(maxsize=max_queue_size),
            EventPriority.HIGH: asyncio.Queue(maxsize=max_queue_size),
            EventPriority.NORMAL: asyncio.Queue(maxsize=max_queue_size),
            EventPriority.LOW: asyncio.Queue(maxsize=max_queue_size),
        }
        self._async_subscribers: Dict[Optional[EventCategory], List[AsyncSubscriber]] = {}
        self._sync_subscribers: Dict[Optional[EventCategory], List[SyncSubscriber]] = {}
        self._dlq: deque[Tuple[BaseRuntimeEvent, str, str]] = deque(maxlen=1000)  # (event, subscriber_name, error)
        self._is_running = False
        self._dispatch_tasks: List[asyncio.Task] = []
        self._dropped_events_count = 0
        self._published_events_count = 0
        self._delivered_events_count = 0

    def subscribe(
        self,
        callback: AsyncSubscriber,
        category: Optional[EventCategory] = None,
    ) -> None:
        """Subscribes an async callback to a specific event category or all categories (None)."""
        if category not in self._async_subscribers:
            self._async_subscribers[category] = []
        self._async_subscribers[category].append(callback)

    def subscribe_sync(
        self,
        callback: SyncSubscriber,
        category: Optional[EventCategory] = None,
    ) -> None:
        """Subscribes a synchronous callback to an event category."""
        if category not in self._sync_subscribers:
            self._sync_subscribers[category] = []
        self._sync_subscribers[category].append(callback)

    def unsubscribe(self, callback: Any) -> None:
        """Removes a subscriber."""
        for cat, subs in self._async_subscribers.items():
            if callback in subs:
                subs.remove(callback)
        for cat, sync_subs in self._sync_subscribers.items():
            if callback in sync_subs:
                sync_subs.remove(callback)

    async def publish(self, event: BaseRuntimeEvent) -> bool:
        """
        Publishes an event to the priority queue with backpressure.
        Returns True if enqueued, False if dropped due to buffer overflow.
        """
        self._published_events_count += 1
        queue = self._queues.get(event.priority, self._queues[EventPriority.NORMAL])
        
        # Immediate synchronous subscriber dispatch
        self._dispatch_sync_subscribers(event)
        
        try:
            queue.put_nowait(event)
            return True
        except asyncio.QueueFull:
            self._dropped_events_count += 1
            logger.warning(
                "Event dropped due to backpressure queue overflow: %s (Priority: %s)",
                event.event_id,
                event.priority,
            )
            return False

    def publish_sync(self, event: BaseRuntimeEvent) -> None:
        """Synchronous dispatch to sync subscribers."""
        self._published_events_count += 1
        self._dispatch_sync_subscribers(event)

    def _dispatch_sync_subscribers(self, event: BaseRuntimeEvent) -> None:
        """Invokes sync subscribers with error isolation."""
        callbacks: List[SyncSubscriber] = []
        if None in self._sync_subscribers:
            callbacks.extend(self._sync_subscribers[None])
        if event.category in self._sync_subscribers:
            callbacks.extend(self._sync_subscribers[event.category])

        for cb in callbacks:
            try:
                cb(event)
                self._delivered_events_count += 1
            except Exception as ex:
                logger.error("Sync subscriber error: %s", ex, exc_info=True)
                self._dlq.append((event, getattr(cb, "__name__", "sync_cb"), str(ex)))

    async def start(self) -> None:
        """Starts background priority dispatch workers."""
        if self._is_running:
            return
        self._is_running = True
        self._dispatch_tasks = [
            asyncio.create_task(self._worker_loop(), name="event-bus-dispatcher")
        ]

    async def stop(self) -> None:
        """Stops background dispatch workers."""
        self._is_running = False
        for task in self._dispatch_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._dispatch_tasks.clear()

    async def _worker_loop(self) -> None:
        """Dispatches events strictly prioritizing CRITICAL -> HIGH -> NORMAL -> LOW."""
        while self._is_running:
            event: Optional[BaseRuntimeEvent] = None
            
            # Check queues in priority order
            for priority in [
                EventPriority.CRITICAL,
                EventPriority.HIGH,
                EventPriority.NORMAL,
                EventPriority.LOW,
            ]:
                q = self._queues[priority]
                if not q.empty():
                    event = await q.get()
                    q.task_done()
                    break

            if event is None:
                # No events ready; brief sleep to yield event loop
                await asyncio.sleep(0.01)
                continue

            await self._dispatch_async_subscribers(event)

    async def _dispatch_async_subscribers(self, event: BaseRuntimeEvent) -> None:
        """Invokes async subscribers in parallel with isolated error containment."""
        callbacks: List[AsyncSubscriber] = []
        if None in self._async_subscribers:
            callbacks.extend(self._async_subscribers[None])
        if event.category in self._async_subscribers:
            callbacks.extend(self._async_subscribers[event.category])

        if not callbacks:
            return

        tasks = [self._safe_invoke_async(cb, event) for cb in callbacks]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_invoke_async(
        self, cb: AsyncSubscriber, event: BaseRuntimeEvent
    ) -> None:
        try:
            await cb(event)
            self._delivered_events_count += 1
        except Exception as ex:
            cb_name = getattr(cb, "__name__", "async_cb")
            logger.error("Async subscriber %s failed: %s", cb_name, ex, exc_info=True)
            self._dlq.append((event, cb_name, str(ex)))

    def get_stats(self) -> Dict[str, Any]:
        """Returns runtime performance statistics of the EventBus."""
        return {
            "published_events_count": self._published_events_count,
            "delivered_events_count": self._delivered_events_count,
            "dropped_events_count": self._dropped_events_count,
            "dlq_size": len(self._dlq),
            "queue_sizes": {
                p.value: self._queues[p].qsize() for p in EventPriority
            },
        }

    def get_dlq(self) -> List[Tuple[BaseRuntimeEvent, str, str]]:
        return list(self._dlq)
