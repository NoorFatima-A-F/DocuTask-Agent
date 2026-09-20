"""Runtime Event Emitter & Event Bus for DocuTask Execution System."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from app.runtime.events.base import RuntimeEvent
from app.runtime.events.persistence import EventStore
from app.runtime.events.dispatcher import EventDispatcher

logger = logging.getLogger(__name__)


class EventBus:
    """Singleton event bus for synchronous and asynchronous runtime events."""
    _instance: Optional[EventBus] = None

    def __init__(self, store: Optional[EventStore] = None, dispatcher: Optional[EventDispatcher] = None):
        self.store = store or EventStore()
        self.dispatcher = dispatcher or EventDispatcher()
        self._sync_handlers: List[Callable[[RuntimeEvent], None]] = []

    @classmethod
    def get_instance(cls) -> EventBus:
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance

    def subscribe_sync(self, handler: Callable[[RuntimeEvent], None]) -> None:
        self._sync_handlers.append(handler)

    def publish(self, event: RuntimeEvent) -> None:
        """Synchronously pushes event to memory store and handlers."""
        # Append to internal store sync (without blocking on async loop if not running)
        self.store._events.append(event)
        self.store._by_id[event.event_id] = event
        if event.mission_id:
            self.store._by_mission[event.mission_id].append(event)

        for handler in self._sync_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in sync event handler: {e}")

        # If event loop is running, also dispatch asynchronously
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                asyncio.create_task(self.dispatcher.dispatch(event))
        except RuntimeError:
            pass


class RuntimeEventEmitter:
    """Convenience emitter attached to workers, planners, and runtimes."""
    def __init__(self, bus: Optional[EventBus] = None, mission_id: str = ""):
        self.bus = bus or EventBus.get_instance()
        self.mission_id = mission_id

    def emit(self, event: RuntimeEvent) -> None:
        self.bus.publish(event)
