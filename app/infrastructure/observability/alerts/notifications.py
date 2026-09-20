"""
Alert Dispatcher & Notification Sender.

Dispatches routed alerts to physical and virtual notification channels with deduplication
and cooldown throttling.
"""

from __future__ import annotations

import logging
import time
from typing import Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.observability.alerts.models import AlertInstance, AlertSeverity
from app.infrastructure.observability.alerts.routing import AlertRouter

logger = logging.getLogger("infrastructure.observability.alerts.notifications")


class DispatchedAlertNotification(BaseModel):
    """Record of a dispatched alert notification."""
    notification_id: str
    alert_id: str
    channel: str
    severity: AlertSeverity
    message: str
    delivered: bool = True
    dispatched_at: float = Field(default_factory=time.time)


class AlertDispatcher:
    """
    Coordinates alert routing, throttling, and channel delivery.
    """

    def __init__(self, router: Optional[AlertRouter] = None, cooldown_seconds: float = 30.0) -> None:
        self.router = router or AlertRouter()
        self.cooldown_seconds = cooldown_seconds
        self._last_dispatched: Dict[str, float] = {}  # key (fingerprint:channel) -> timestamp
        self._history: List[DispatchedAlertNotification] = []
        self._handlers: Dict[str, Callable[[AlertInstance, str], bool]] = {}

    def register_channel_handler(self, channel: str, handler: Callable[[AlertInstance, str], bool]) -> None:
        self._handlers[channel] = handler

    def dispatch(self, alert: AlertInstance) -> List[DispatchedAlertNotification]:
        """Route and dispatch alert to appropriate channels."""
        channels = self.router.route_alert(alert)
        dispatches: List[DispatchedAlertNotification] = []
        now = time.time()

        for ch in channels:
            key = f"{alert.fingerprint}:{ch}"
            last_time = self._last_dispatched.get(key, 0.0)

            # Suppress if within cooldown, unless EMERGENCY
            if (now - last_time) < self.cooldown_seconds and alert.severity != AlertSeverity.EMERGENCY:
                logger.info(f"Alert notification suppressed by cooldown for {key}")
                continue

            handler = self._handlers.get(ch)
            delivered = True
            if handler:
                try:
                    delivered = handler(alert, ch)
                except Exception as e:
                    logger.error(f"Error executing alert handler for channel '{ch}': {e}")
                    delivered = False

            record = DispatchedAlertNotification(
                notification_id=f"notif-{len(self._history) + 1}",
                alert_id=alert.alert_id,
                channel=ch,
                severity=alert.severity,
                message=alert.message,
                delivered=delivered,
                dispatched_at=now,
            )
            self._history.append(record)
            self._last_dispatched[key] = now
            dispatches.append(record)

        return dispatches

    def get_history(self) -> List[DispatchedAlertNotification]:
        return list(self._history)
