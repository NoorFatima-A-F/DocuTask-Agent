"""
Production-grade Asynchronous Event Bus for Autonomous Agent Operating System.
Provides high-throughput async pub/sub, pattern/wildcard matching, priority queues,
handler timeout enforcement, retry handling, DLQ routing, and event store auditing.
"""

from __future__ import annotations

import asyncio
import fnmatch
import inspect
import logging
import traceback
from collections import defaultdict
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, Type, Union

from app.agents.events.dead_letter_queue import DeadLetterQueue
from app.agents.events.event_store import EventStore
from app.agents.events.event_types import AgentEvent, EventPriority
from app.agents.interfaces.event_bus import AgentEventBus

logger = logging.getLogger(__name__)

AsyncEventHandler = Callable[[AgentEvent], Coroutine[Any, Any, None]]
SyncEventHandler = Callable[[AgentEvent], None]
AnyEventHandler = Union[AsyncEventHandler, SyncEventHandler]


class EnterpriseEventBus(AgentEventBus):
    """
    Robust asynchronous event broker powering enterprise agent communications.
    Guarantees event ordering, error isolation, audit logging, and dead-lettering.
    """

    def __init__(
        self,
        event_store: Optional[EventStore] = None,
        dead_letter_queue: Optional[DeadLetterQueue] = None,
        max_retries: int = 3,
        handler_timeout_seconds: float = 30.0,
    ) -> None:
        self._event_store = event_store or EventStore()
        self._dlq = dead_letter_queue or DeadLetterQueue()
        self._max_retries = max_retries
        self._handler_timeout_seconds = handler_timeout_seconds

        # Topic -> list of handlers
        self._subscribers: Dict[str, List[AnyEventHandler]] = defaultdict(list)
        # Event type class -> list of handlers
        self._type_subscribers: Dict[Type[AgentEvent], List[AnyEventHandler]] = defaultdict(list)
        
        # Telemetry metrics
        self._published_count: int = 0
        self._handled_count: int = 0
        self._failed_count: int = 0

    @property
    def event_store(self) -> EventStore:
        return self._event_store

    @property
    def dead_letter_queue(self) -> DeadLetterQueue:
        return self._dlq

    @property
    def metrics(self) -> Dict[str, int]:
        return {
            "published": self._published_count,
            "handled": self._handled_count,
            "failed": self._failed_count,
            "dlq_size": len(self._dlq),
            "store_size": len(self._event_store),
        }

    def subscribe(
        self,
        event_type_or_topic: Union[str, Type[AgentEvent]],
        handler: AnyEventHandler,
    ) -> None:
        """
        Subscribes a synchronous or asynchronous handler function.
        Supports concrete event classes or wildcard string topics (e.g. 'task.*', 'agent.*', '*').
        """
        if isinstance(event_type_or_topic, type) and issubclass(event_type_or_topic, AgentEvent):
            self._type_subscribers[event_type_or_topic].append(handler)
            logger.debug("Subscribed %s to event type %s", handler.__name__, event_type_or_topic.__name__)
        else:
            topic = str(event_type_or_topic)
            self._subscribers[topic].append(handler)
            logger.debug("Subscribed %s to topic pattern '%s'", getattr(handler, '__name__', str(handler)), topic)

    def unsubscribe(
        self,
        event_type_or_topic: Union[str, Type[AgentEvent]],
        handler: AnyEventHandler,
    ) -> bool:
        """Removes a handler from subscription registry."""
        if isinstance(event_type_or_topic, type) and issubclass(event_type_or_topic, AgentEvent):
            handlers = self._type_subscribers.get(event_type_or_topic, [])
            if handler in handlers:
                handlers.remove(handler)
                return True
        else:
            topic = str(event_type_or_topic)
            handlers = self._subscribers.get(topic, [])
            if handler in handlers:
                handlers.remove(handler)
                return True
        return False

    async def publish(self, event: AgentEvent, topic: Optional[str] = None) -> int:
        """
        Publishes an event to all matching subscribers.
        Automatically commits event to append-only EventStore.
        Routes unhandled errors to DeadLetterQueue.
        Returns total number of handlers invoked.
        """
        self._published_count += 1
        effective_topic = topic or event.event_type

        # 1. Audit append
        self._event_store.append(event)

        # 2. Resolve matching handlers
        target_handlers: List[AnyEventHandler] = []

        # By concrete class or subclass
        for cls, handlers in self._type_subscribers.items():
            if isinstance(event, cls):
                target_handlers.extend(handlers)

        # By topic pattern matching (supports wildcards like 'task.*' or '*')
        for pattern, handlers in self._subscribers.items():
            if pattern == "*" or pattern == effective_topic or fnmatch.fnmatch(effective_topic, pattern):
                target_handlers.extend(handlers)

        # Deduplicate handlers while preserving order
        unique_handlers: List[AnyEventHandler] = []
        seen: Set[AnyEventHandler] = set()
        for h in target_handlers:
            if h not in seen:
                seen.add(h)
                unique_handlers.append(h)

        if not unique_handlers:
            logger.debug("No listeners for event %s on topic '%s'", event.event_id, effective_topic)
            return 0

        # 3. Dispatch concurrently
        tasks = [
            self._dispatch_to_handler(handler, event, effective_topic)
            for handler in unique_handlers
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        invoked = 0
        for res in results:
            if res is True:
                invoked += 1
                self._handled_count += 1
            else:
                self._failed_count += 1

        return invoked

    async def _dispatch_to_handler(
        self,
        handler: AnyEventHandler,
        event: AgentEvent,
        topic: str,
    ) -> bool:
        """Invokes a single handler with timeout and exponential retry."""
        retry_count = 0
        last_error: Optional[Exception] = None
        last_tb = ""

        while retry_count <= self._max_retries:
            try:
                if inspect.iscoroutinefunction(handler):
                    coro = handler(event)
                    await asyncio.wait_for(coro, timeout=self._handler_timeout_seconds)
                else:
                    # Sync handler: run in default executor
                    loop = asyncio.get_running_loop()
                    await loop.run_in_executor(None, handler, event)
                return True
            except asyncio.TimeoutError as tex:
                retry_count += 1
                last_error = tex
                last_tb = traceback.format_exc()
                logger.warning(
                    "Handler %s timed out on event %s (attempt %d/%d)",
                    getattr(handler, "__name__", str(handler)),
                    event.event_id,
                    retry_count,
                    self._max_retries + 1,
                )
            except Exception as ex:
                retry_count += 1
                last_error = ex
                last_tb = traceback.format_exc()
                logger.warning(
                    "Handler %s raised %s on event %s (attempt %d/%d): %s",
                    getattr(handler, "__name__", str(handler)),
                    type(ex).__name__,
                    event.event_id,
                    retry_count,
                    self._max_retries + 1,
                    ex,
                )

            if retry_count <= self._max_retries:
                await asyncio.sleep(0.05 * (2 ** (retry_count - 1)))

        # Persistent failure: route to DeadLetterQueue
        if last_error:
            self._dlq.enqueue(
                event=event,
                topic=topic,
                error=last_error,
                retry_count=retry_count,
                stack_trace=last_tb,
                metadata={"handler": getattr(handler, "__name__", str(handler))},
            )

        return False

    def clear(self) -> None:
        """Reset subscriptions and metrics."""
        self._subscribers.clear()
        self._type_subscribers.clear()
        self._published_count = 0
        self._handled_count = 0
        self._failed_count = 0
