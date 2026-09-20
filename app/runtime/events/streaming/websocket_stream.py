"""
DocuTask Agent - WebSocket Event Streaming Protocol
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, Any, List
import asyncio
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.bus.event_bus import domain_event_bus


class WebSocketStreamManager:
    """
    Manages active WebSocket client subscriptions for real-time live event pushes.
    """

    def __init__(self):
        self._active_connections: List[Any] = []

    def register(self, connection: Any) -> None:
        self._active_connections.append(connection)

    def unregister(self, connection: Any) -> None:
        if connection in self._active_connections:
            self._active_connections.remove(connection)

    @property
    def active_connections_count(self) -> int:
        return len(self._active_connections)


websocket_stream_manager = WebSocketStreamManager()
