"""
Thread-Safe Handler & Subscriber Registries.
"""

import asyncio
from typing import Callable, Coroutine, Dict, List
from app.agents.messaging.events import DomainEvent
from app.agents.messaging.handlers import CommandHandler, QueryHandler


class HandlerRegistry:
    """Thread-safe registry for Command, Query, and Event handlers."""

    def __init__(self):
        self._command_handlers: Dict[str, CommandHandler] = {}
        self._query_handlers: Dict[str, QueryHandler] = {}
        self._event_subscribers: Dict[str, List[Callable[[DomainEvent], Coroutine]]] = {}
        self._lock = asyncio.Lock()

    async def register_command_handler(self, command_type: str, handler: CommandHandler) -> None:
        async with self._lock:
            self._command_handlers[command_type] = handler

    async def get_command_handler(self, command_type: str) -> CommandHandler:
        async with self._lock:
            return self._command_handlers.get(command_type)

    async def register_query_handler(self, query_type: str, handler: QueryHandler) -> None:
        async with self._lock:
            self._query_handlers[query_type] = handler

    async def get_query_handler(self, query_type: str) -> QueryHandler:
        async with self._lock:
            return self._query_handlers.get(query_type)

    async def subscribe_event(self, event_type: str, handler: Callable[[DomainEvent], Coroutine]) -> None:
        async with self._lock:
            if event_type not in self._event_subscribers:
                self._event_subscribers[event_type] = []
            self._event_subscribers[event_type].append(handler)

    async def get_event_subscribers(self, event_type: str) -> List[Callable[[DomainEvent], Coroutine]]:
        async with self._lock:
            return list(self._event_subscribers.get(event_type, []))
