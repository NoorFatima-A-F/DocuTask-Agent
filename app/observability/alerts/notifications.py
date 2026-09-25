"""Alert Routing and Multi-Channel Notification Dispatcher."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .engine import ActiveAlert
from .rules import AlertSeverity


class ChannelType(str, Enum):
    SLACK = "SLACK"
    PAGERDUTY = "PAGERDUTY"
    WEBHOOK = "WEBHOOK"
    EMAIL = "EMAIL"
    INTERNAL = "INTERNAL"


@dataclass
class NotificationChannel:
    channel_id: str
    name: str
    channel_type: ChannelType
    endpoint: str
    min_severity: AlertSeverity = AlertSeverity.WARNING
    enabled: bool = True


@dataclass
class NotificationDispatchRecord:
    channel_id: str
    alert_id: str
    alert_name: str
    severity: str
    dispatched_at: float = field(default_factory=time.time)
    success: bool = True
    error_message: Optional[str] = None


class AlertRouter:
    """Dispatches firing alerts to appropriate notification channels based on severity and rules."""

    def __init__(self):
        self._channels: Dict[str, NotificationChannel] = {}
        self._dispatch_log: List[NotificationDispatchRecord] = []

    def register_channel(self, channel: NotificationChannel) -> None:
        self._channels[channel.channel_id] = channel

    def remove_channel(self, channel_id: str) -> bool:
        if channel_id in self._channels:
            del self._channels[channel_id]
            return True
        return False

    def list_channels(self) -> List[NotificationChannel]:
        return list(self._channels.values())

    def dispatch(self, alert: ActiveAlert) -> List[NotificationDispatchRecord]:
        """Dispatch alert to all matching active channels."""
        dispatched: List[NotificationDispatchRecord] = []
        severity_ranks = {
            AlertSeverity.INFO: 1,
            AlertSeverity.WARNING: 2,
            AlertSeverity.ERROR: 3,
            AlertSeverity.CRITICAL: 4,
        }
        alert_rank = severity_ranks.get(alert.severity, 1)

        for ch in self._channels.values():
            if not ch.enabled:
                continue

            ch_min_rank = severity_ranks.get(ch.min_severity, 1)
            if alert_rank >= ch_min_rank:
                # Simulated dispatch record
                rec = NotificationDispatchRecord(
                    channel_id=ch.channel_id,
                    alert_id=alert.alert_id,
                    alert_name=alert.name,
                    severity=alert.severity.value,
                    dispatched_at=time.time(),
                    success=True,
                )
                self._dispatch_log.append(rec)
                dispatched.append(rec)

        return dispatched

    def get_dispatch_log(self, limit: int = 100) -> List[NotificationDispatchRecord]:
        return self._dispatch_log[-limit:]
