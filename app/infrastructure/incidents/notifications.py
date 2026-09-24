from __future__ import annotations
"""
Incident Notifier & Alert Dispatcher.

Dispatches multi-channel notifications (Webhook, Slack, Email, PagerDuty, Event Bus)
with deduplication and rate limiting.
"""


import enum
import logging
from app.core.security import sanitize_log_input
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.reliability.models import SeverityLevel

logger = logging.getLogger("infrastructure.incidents.notifications")


class NotificationChannel(str, enum.Enum):
    """Supported alerting channels."""
    WEBHOOK = "WEBHOOK"
    SLACK = "SLACK"
    EMAIL = "EMAIL"
    PAGERDUTY = "PAGERDUTY"
    EVENT_BUS = "EVENT_BUS"


class NotificationMessage(BaseModel):
    """Structured incident notification message."""
    message_id: str
    incident_id: str
    channel: NotificationChannel
    severity: SeverityLevel
    title: str
    content: str
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    delivered: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IncidentNotifier:
    """
    Multi-channel notification dispatcher with deduplication and delivery tracking.
    """

    def __init__(self, rate_limit_cooldown_seconds: float = 10.0) -> None:
        self.rate_limit_cooldown_seconds = rate_limit_cooldown_seconds
        self._sent_messages: List[NotificationMessage] = []
        self._last_sent_time: Dict[str, float] = {}  # key (incident_id:channel) -> timestamp
        self._channel_handlers: Dict[NotificationChannel, Callable[[NotificationMessage], bool]] = {}

    def register_channel_handler(
        self,
        channel: NotificationChannel,
        handler: Callable[[NotificationMessage], bool],
    ) -> None:
        self._channel_handlers[channel] = handler

    def dispatch(
        self,
        message_id: str,
        incident_id: str,
        channel: NotificationChannel,
        severity: SeverityLevel,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[NotificationMessage]:
        """
        Dispatch notification with deduplication rate limiting.
        """
        rate_key = f"{incident_id}:{channel.value}"
        now = time.time()
        last_sent = self._last_sent_time.get(rate_key, 0.0)

        if (now - last_sent) < self.rate_limit_cooldown_seconds and severity != SeverityLevel.CATASTROPHIC:
            logger.info(f"Notification suppressed by rate-limit for {sanitize_log_input(rate_key)}")
            return None

        msg = NotificationMessage(
            message_id=message_id,
            incident_id=incident_id,
            channel=channel,
            severity=severity,
            title=title,
            content=content,
            metadata=metadata or {},
        )

        handler = self._channel_handlers.get(channel)
        if handler:
            try:
                msg.delivered = handler(msg)
            except Exception as e:
                logger.error(f"Error executing notification handler for {channel.value}: {e}")
                msg.delivered = False
        else:
            # Default simulated delivery
            msg.delivered = True

        self._sent_messages.append(msg)
        self._last_sent_time[rate_key] = now
        logger.info(f"Dispatched {channel.value} notification for incident '{sanitize_log_input(incident_id)}' (severity={severity.value})")
        return msg

    def list_dispatched_messages(self, incident_id: Optional[str] = None) -> List[NotificationMessage]:
        if incident_id:
            return [m for m in self._sent_messages if m.incident_id == incident_id]
        return list(self._sent_messages)
