# Runtime Event Dispatcher
from __future__ import annotations
import asyncio
import logging
from typing import Any, Callable, Coroutine, Dict
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.subscriptions import EventSubscription

logger = logging.getLogger(__name__)
HandlerFunc = Callable[[RuntimeEvent], Coroutine[Any, Any, None]]

class EventDispatcher:
    def __init__(self):
        self._handlers: Dict[str, tuple[EventSubscription, HandlerFunc]] = {}
        self._lock = asyncio.Lock()

    async def register(self, sub: EventSubscription, handler: HandlerFunc):
        async with self._lock:
            self._handlers[sub.subscription_id] = (sub, handler)

    async def unregister(self, subscription_id: str):
        async with self._lock:
            self._handlers.pop(subscription_id, None)

    async def dispatch(self, event: RuntimeEvent):
        tasks = []
        for sub_id, (sub, handler) in list(self._handlers.items()):
            if sub.matches(event):
                tasks.append(self._safe_invoke(sub_id, handler, event))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_invoke(self, sub_id: str, handler: HandlerFunc, event: RuntimeEvent):
        try:
            await handler(event)
        except Exception as e:
            logger.error(f'Error in subscriber {sub_id}: {e}')
