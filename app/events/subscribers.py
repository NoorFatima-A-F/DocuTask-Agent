"""
Event Subscriber and Idempotent Consumer Helpers.
"""

from functools import wraps
from typing import Any, Callable, Set
from .models import CloudEventEnvelope


class IdempotentConsumer:
    """Wrapper that guarantees each event is processed exactly once by tracking processed event IDs."""

    def __init__(self):
        self._processed_ids: Set[str] = set()

    def is_processed(self, event_id: str) -> bool:
        return event_id in self._processed_ids

    def mark_processed(self, event_id: str) -> None:
        self._processed_ids.add(event_id)

    def wrap(self, handler: Callable[[CloudEventEnvelope], Any]) -> Callable[[CloudEventEnvelope], Any]:
        """Decorator for making event handlers idempotent."""
        @wraps(handler)
        async def async_wrapper(event: CloudEventEnvelope) -> Any:
            if self.is_processed(event.id):
                return None
            result = await handler(event)
            self.mark_processed(event.id)
            return result

        @wraps(handler)
        def sync_wrapper(event: CloudEventEnvelope) -> Any:
            if self.is_processed(event.id):
                return None
            result = handler(event)
            self.mark_processed(event.id)
            return result

        import asyncio
        if asyncio.iscoroutinefunction(handler):
            return async_wrapper
        return sync_wrapper
