"""Platform Event Stream and Structured Event Taxonomy."""

from __future__ import annotations

import fnmatch
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .context import ObservabilityContext, get_current_context


class EventCategory(str, Enum):
    INFRASTRUCTURE = "INFRASTRUCTURE"
    RUNTIME = "RUNTIME"
    WORKFLOW = "WORKFLOW"
    AGENT = "AGENT"
    AI = "AI"
    SECURITY = "SECURITY"
    SRE = "SRE"


@dataclass
class PlatformEvent:
    event_id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:10]}")
    name: str = "platform.heartbeat"
    category: EventCategory = EventCategory.RUNTIME
    severity: str = "INFO"
    source: str = "docutask-runtime"
    payload: Dict[str, Any] = field(default_factory=dict)
    context: ObservabilityContext = field(default_factory=get_current_context)
    timestamp: float = field(default_factory=time.time)


class EventStream:
    """Pub-Sub event bus for operational and runtime platform events."""

    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self._history: List[PlatformEvent] = []
        # list of (pattern, handler)
        self._subscribers: List[tuple[str, Callable[[PlatformEvent], None]]] = []

    def subscribe(self, pattern: str, handler: Callable[[PlatformEvent], None]) -> None:
        """Subscribe to events matching a glob pattern (e.g. 'agent.*', 'ai.model.*', '*')."""
        self._subscribers.append((pattern, handler))

    def publish(self, event: PlatformEvent) -> None:
        """Publish an event to all matching subscribers and buffer in history."""
        self._history.append(event)
        if len(self._history) > self.max_history:
            self._history.pop(0)

        for pattern, handler in self._subscribers:
            if fnmatch.fnmatch(event.name, pattern):
                try:
                    handler(event)
                except Exception:
                    pass

    def get_history(
        self,
        category: Optional[EventCategory] = None,
        severity: Optional[str] = None,
        limit: int = 100,
    ) -> List[PlatformEvent]:
        """Query recent events matching filters."""
        results: List[PlatformEvent] = []
        for ev in reversed(self._history):
            if category and ev.category != category:
                continue
            if severity and ev.severity != severity:
                continue
            results.append(ev)
            if len(results) >= limit:
                break
        return results

    def clear(self) -> None:
        self._history.clear()
