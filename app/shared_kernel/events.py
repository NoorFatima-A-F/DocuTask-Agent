"""
Domain & Integration Event Primitives and Event Bus.
Enables asynchronous, decoupled cross-bounded-context communication.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Callable, Awaitable, Type, TypeVar, Optional, Generic
import uuid
import inspect

@dataclass(frozen=True)
class EventMetadata:
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:16]}")
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1

@dataclass
class BaseEvent:
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:16]}")
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1

@dataclass
class DomainEvent(BaseEvent):
    """Event representing a state change inside a single Bounded Context."""
    pass

@dataclass
class ApplicationEvent(BaseEvent):
    """Event representing an application use case lifecycle event."""
    pass

@dataclass
class IntegrationEvent(BaseEvent):
    """Event published across bounded contexts or external systems."""
    pass

@dataclass
class SystemEvent(BaseEvent):
    """Event representing platform infrastructure state transitions."""
    pass

E = TypeVar("E", bound=BaseEvent)

class EventHandlerContract(ABC, Generic[E]):
    @abstractmethod
    async def handle(self, event: E) -> None:
        pass

class EventBusContract(ABC):
    @abstractmethod
    def subscribe(self, event_cls: Type[E], handler: Callable[[E], Awaitable[None]]) -> None:
        pass

    @abstractmethod
    async def publish(self, event: BaseEvent) -> None:
        pass

class EventBus(EventBusContract):
    """In-memory asynchronous Domain & Integration Event Bus."""
    def __init__(self):
        self._handlers: Dict[Type[Any], List[Callable[[Any], Awaitable[None]]]] = {}
        self._event_history: List[BaseEvent] = []

    def subscribe(self, event_cls: Type[E], handler: Callable[[E], Awaitable[None]]) -> None:
        if event_cls not in self._handlers:
            self._handlers[event_cls] = []
        self._handlers[event_cls].append(handler)

    async def publish(self, event: BaseEvent) -> None:
        self._event_history.append(event)
        event_cls = type(event)
        handlers = self._handlers.get(event_cls, [])
        for handler in handlers:
            if inspect.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)

    def get_published_events(self) -> List[BaseEvent]:
        return list(self._event_history)

    def clear(self) -> None:
        self._event_history.clear()

_global_event_bus = EventBus()

def get_event_bus() -> EventBus:
    return _global_event_bus
