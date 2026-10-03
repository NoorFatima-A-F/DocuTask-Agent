"""
Enterprise Notification & Alerting Service.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional
import uuid
from app.platform_verification.reporting_audit.domain.interfaces import INotificationService
from app.platform_verification.reporting_audit.domain.models import (
    NotificationAlert,
    NotificationEventType,
    UserRole,
)


class EnterpriseNotificationService(INotificationService):
    """Emits alerts and monitors stakeholder notifications."""

    def __init__(self):
        self._alerts: List[NotificationAlert] = []

    def send_alert(
        self,
        event_type: NotificationEventType,
        severity: str,
        title: str,
        message: str,
        roles: List[UserRole],
    ) -> NotificationAlert:
        alert = NotificationAlert(
            alert_id=f"ALT-{uuid.uuid4().hex[:8].upper()}",
            event_type=event_type,
            severity=severity,
            title=title,
            message=message,
            recipient_roles=roles,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._alerts.insert(0, alert)
        return alert

    def list_alerts(self, role: Optional[UserRole] = None) -> List[NotificationAlert]:
        if role:
            return [a for a in self._alerts if role in a.recipient_roles]
        return list(self._alerts)
