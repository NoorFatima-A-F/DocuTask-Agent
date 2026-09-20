"""
Asynchronous In-Memory Event Bus with Dead Letter Queue and Filters.
"""
import asyncio
from typing import Callable, Dict, List, Type, Any
from app.platform_verification.shared_kernel.events import BaseEvent

EventHandler = Callable[[BaseEvent], None]

class EnterpriseEventBus:
    def __init__(self):
        self._handlers: Dict[Type[BaseEvent], List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []
        self._dead_letter_queue: List[Dict[str, Any]] = []
        self._event_history: List[BaseEvent] = []

    def subscribe(self, event_type: Type[BaseEvent], handler: EventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def subscribe_all(self, handler: EventHandler) -> None:
        self._global_handlers.append(handler)

    def publish(self, event: BaseEvent) -> None:
        self._event_history.append(event)
        
        # Specific handlers
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                self._dead_letter_queue.append({
                    "event": event,
                    "handler": str(handler),
                    "error": str(e)
                })

        # Global handlers
        for gh in self._global_handlers:
            try:
                gh(event)
            except Exception as e:
                self._dead_letter_queue.append({
                    "event": event,
                    "handler": str(gh),
                    "error": str(e)
                })

    def get_history(self) -> List[BaseEvent]:
        return list(self._event_history)

    def get_dead_letters(self) -> List[Dict[str, Any]]:
        return list(self._dead_letter_queue)

verification_event_bus = EnterpriseEventBus()
