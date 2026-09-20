"""
In-Memory Domain Event Bus with Audit Dispatching
"""
from typing import Dict, List, Callable, Optional
from app.platform_verification.domain.events import VerificationDomainEvent
from app.platform_verification.domain.interfaces import EventBusInterface

class VerificationEventBus(EventBusInterface):
    def __init__(self):
        self._handlers: Dict[str, List[Callable[[VerificationDomainEvent], None]]] = {}
        self._event_log: List[VerificationDomainEvent] = []

    def subscribe(self, event_type: str, handler: Callable[[VerificationDomainEvent], None]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: VerificationDomainEvent) -> None:
        self._event_log.append(event)
        handlers = self._handlers.get(event.event_type, [])
        for h in handlers:
            try:
                h(event)
            except Exception as e:
                print(f"[EventBus Error] Failed to handle {event.event_type}: {e}")
        for h in self._handlers.get("*", []):
            try:
                h(event)
            except Exception as e:
                print(f"[EventBus Error] Wildcard handler failed: {e}")

    def get_event_log(self, run_id: Optional[str] = None) -> List[VerificationDomainEvent]:
        if run_id:
            return [e for e in self._event_log if e.run_id == run_id]
        return list(self._event_log)

verification_event_bus = VerificationEventBus()
