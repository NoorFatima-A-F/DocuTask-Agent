"""In-Process Event Subscription Handlers."""

from typing import Any, Callable, Dict, List, Optional
from .dispatcher import WebhookDispatcher


class GovernanceEventHandler:
    """Manages internal and external subscribers for governance events."""

    def __init__(self, dispatcher: Optional[WebhookDispatcher] = None) -> None:
        self.dispatcher = dispatcher or WebhookDispatcher()
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for a specific governance event."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish_and_notify(self, tenant_id: str, event_type: str, payload: Dict[str, Any]) -> None:
        """Deliver to local callbacks and outbound webhooks."""
        event_obj = {
            "tenant_id": tenant_id,
            "event_type": event_type,
            "payload": payload,
        }

        # 1. Local subscribers
        for handler in self._subscribers.get(event_type, []):
            try:
                handler(event_obj)
            except Exception:
                pass
        for handler in self._subscribers.get("*", []):
            try:
                handler(event_obj)
            except Exception:
                pass

        # 2. Outbound webhooks
        self.dispatcher.dispatch_event(tenant_id=tenant_id, event_type=event_type, payload=payload)
