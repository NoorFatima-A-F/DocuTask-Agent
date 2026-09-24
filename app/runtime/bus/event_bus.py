# Asynchronous Runtime Event Bus
from __future__ import annotations
import asyncio
import logging
from typing import Any, Callable, Coroutine, Dict, Optional
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.persistence import EventStore
from app.runtime.events.subscriptions import EventSubscription

logger = logging.getLogger(__name__)
AsyncSubscriber = Callable[[RuntimeEvent], Coroutine[Any, Any, None]]

class RuntimeEventBus:
    def __init__(self, store: Optional[EventStore] = None):
        self.store = store or EventStore()
        self._subscribers: Dict[str, tuple[EventSubscription, AsyncSubscriber]] = {}
        self._queues: Dict[str, asyncio.Queue[RuntimeEvent]] = {}
        self._lock = asyncio.Lock()
        self._global_event_count = 0

    async def publish(self, event: RuntimeEvent):
        await self.store.append(event)
        self._global_event_count += 1
        async with self._lock:
            subs = list(self._subscribers.items())
            queues = list(self._queues.items())
        for q_id, q in queues:
            try:
                q.put_nowait(event)
            except Exception:
                pass
        tasks = []
        for sub_id, (sub, callback) in subs:
            if sub.matches(event):
                tasks.append(self._invoke_subscriber(sub_id, callback, event))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _invoke_subscriber(self, sub_id: str, callback: AsyncSubscriber, event: RuntimeEvent):
        try:
            await callback(event)
        except Exception as e:
            logger.error(f'Error in subscriber {sub_id}: {e}')

    async def subscribe(self, sub: EventSubscription, callback: AsyncSubscriber):
        async with self._lock:
            self._subscribers[sub.subscription_id] = (sub, callback)
            return sub.subscription_id

    async def unsubscribe(self, subscription_id: str):
        async with self._lock:
            self._subscribers.pop(subscription_id, None)

    async def create_stream_queue(self, queue_id: str, max_size: int = 1000):
        q: asyncio.Queue[RuntimeEvent] = asyncio.Queue(maxsize=max_size)
        async with self._lock:
            self._queues[queue_id] = q
        return q

    async def remove_stream_queue(self, queue_id: str):
        async with self._lock:
            self._queues.pop(queue_id, None)

_GLOBAL_EVENT_BUS: Optional[RuntimeEventBus] = None

def get_global_event_bus():
    global _GLOBAL_EVENT_BUS
    if _GLOBAL_EVENT_BUS is None:
        _GLOBAL_EVENT_BUS = RuntimeEventBus()
    return _GLOBAL_EVENT_BUS
