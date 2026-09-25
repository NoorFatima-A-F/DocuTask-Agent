"""
Incident Management & Notification Subsystem.
"""

from app.infrastructure.incidents.models import (
    Incident,
    IncidentStatus,
    IncidentTimelineEntry,
)
from app.infrastructure.incidents.lifecycle import (
    IncidentLifecycleStateMachine,
    InvalidIncidentTransitionError,
)
from app.infrastructure.incidents.notifications import (
    IncidentNotifier,
    NotificationChannel,
    NotificationMessage,
)
from app.infrastructure.incidents.manager import (
    IncidentManager,
)

__all__ = [
    "Incident",
    "IncidentLifecycleStateMachine",
    "IncidentManager",
    "IncidentNotifier",
    "IncidentStatus",
    "IncidentTimelineEntry",
    "InvalidIncidentTransitionError",
    "NotificationChannel",
    "NotificationMessage",
]
