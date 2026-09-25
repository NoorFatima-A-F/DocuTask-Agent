"""Internal Governance Event Dispatching and Ingestion Bridge."""

from datetime import datetime, timezone
import secrets
from typing import Any, Callable, Dict, List, Optional
from ...gateway.authentication import APIRequestContext


class InternalEventBridge:
    """High-throughput in-memory event dispatch and fanout for internal services."""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self._event_log: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register an in-process listener for internal event streams."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event_type: str, tenant_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch event to all subscribed listeners and record in event log."""
        event_id = f"evt_{secrets.token_hex(8)}"
        event_record = {
            "event_id": event_id,
            "event_type": event_type,
            "tenant_id": tenant_id,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._event_log.append(event_record)

        # Notify specific listeners
        for handler in self._handlers.get(event_type, []):
            try:
                handler(event_record)
            except Exception:
                pass

        # Notify wildcard listeners
        for handler in self._handlers.get("*", []):
            try:
                handler(event_record)
            except Exception:
                pass

        return event_record

    def get_events(self, tenant_id: Optional[str] = None, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Query logged events."""
        events = self._event_log
        if tenant_id:
            events = [e for e in events if e.get("tenant_id") == tenant_id]
        if event_type:
            events = [e for e in events if e.get("event_type") == event_type]
        return list(events)


internal_event_bridge = InternalEventBridge()


def handle_internal_publish_event(ctx: APIRequestContext, body: Dict[str, Any]) -> Dict[str, Any]:
    event_type = body.get("event_type", "GENERIC_INTERNAL_EVENT")
    payload = body.get("payload", {})
    return internal_event_bridge.publish(event_type, ctx.tenant_id, payload)
