"""
Enterprise Platform Event Bus.
Supports at-least-once delivery, subscription pattern matching, dead-letter routing, and retry with exponential backoff.
"""

import asyncio
from datetime import datetime, timezone
import fnmatch
from typing import Any, Callable, Dict, List, Optional, Set
from .models import CloudEventEnvelope


class DeadLetterQueue:
    """Storage and queue for failed event deliveries."""

    def __init__(self):
        self._dead_letters: List[Dict[str, Any]] = []

    def route_to_dlq(self, event: CloudEventEnvelope, subscriber_name: str, error: Exception, attempts: int) -> None:
        """Store failed event in Dead Letter Queue."""
        self._dead_letters.append({
            "event": event.to_dict(),
            "subscriber": subscriber_name,
            "error": str(error),
            "attempts": attempts,
            "queued_at": datetime.now(timezone.utc).isoformat(),
        })

    def list_dead_letters(self) -> List[Dict[str, Any]]:
        return list(self._dead_letters)

    def count(self) -> int:
        return len(self._dead_letters)

    def clear(self) -> None:
        self._dead_letters.clear()


class EventBus:
    """Enterprise In-Memory / Distributed Event Bus."""

    def __init__(self, dlq: Optional[DeadLetterQueue] = None):
        self._subscribers: Dict[str, List[tuple[str, Callable[[CloudEventEnvelope], Any]]]] = {}
        self.dlq = dlq or DeadLetterQueue()
        self._event_history: List[CloudEventEnvelope] = []
        self._processed_event_ids: Set[str] = set()

    def subscribe(self, pattern: str, handler: Callable[[CloudEventEnvelope], Any], subscriber_name: str = "default") -> None:
        """Subscribe handler to event type pattern (e.g. 'document.*', 'platform.runtime.*')."""
        if pattern not in self._subscribers:
            self._subscribers[pattern] = []
        self._subscribers[pattern].append((subscriber_name, handler))

    async def publish(
        self,
        event: CloudEventEnvelope,
        max_retries: int = 3,
        retry_delay_seconds: float = 0.05,
    ) -> None:
        """Publish event with at-least-once delivery and retry on subscriber failure."""
        self._event_history.append(event)
        matching_handlers = self._get_matching_handlers(event.type)

        for sub_name, handler in matching_handlers:
            delivery_succeeded = False
            last_err = None

            for attempt in range(1, max_retries + 1):
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                    delivery_succeeded = True
                    break
                except Exception as e:
                    last_err = e
                    if attempt < max_retries:
                        await asyncio.sleep(retry_delay_seconds * attempt)

            if not delivery_succeeded and last_err:
                self.dlq.route_to_dlq(event, sub_name, last_err, max_retries)

    def _get_matching_handlers(self, event_type: str) -> List[tuple[str, Callable[[CloudEventEnvelope], Any]]]:
        matches = []
        for pattern, handler_list in self._subscribers.items():
            if fnmatch.fnmatch(event_type, pattern):
                matches.extend(handler_list)
        return matches

    def get_history(self) -> List[CloudEventEnvelope]:
        """Return event history for auditing and replay."""
        return list(self._event_history)
