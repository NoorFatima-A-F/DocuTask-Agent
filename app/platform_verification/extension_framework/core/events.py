"""
Plugin Event Publisher & Telemetry Bus.
"""
from typing import Callable, Dict, List
from app.platform_verification.extension_framework.domain.models import PluginEvent


class PluginEventPublisher:
    def __init__(self):
        self._subscribers: List[Callable[[PluginEvent], None]] = []
        self._event_history: List[PluginEvent] = []

    def subscribe(self, handler: Callable[[PluginEvent], None]) -> None:
        self._subscribers.append(handler)

    def publish(self, event: PluginEvent) -> None:
        self._event_history.append(event)
        for handler in self._subscribers:
            try:
                handler(event)
            except Exception:
                pass

    def get_history(self, plugin_id: Optional[str] = None) -> List[PluginEvent]:
        if plugin_id:
            return [e for e in self._event_history if e.plugin_id == plugin_id]
        return list(self._event_history)


plugin_event_publisher = PluginEventPublisher()
