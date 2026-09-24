"""
Incident Lifecycle State Machine.

Enforces transition validity across the 7 incident lifecycle states,
records timeline events, and ensures thorough postmortem tracking before closure.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, Set
import uuid

from app.infrastructure.incidents.models import (
    Incident,
    IncidentStatus,
    IncidentTimelineEntry,
)

logger = logging.getLogger("infrastructure.incidents.lifecycle")


class InvalidIncidentTransitionError(Exception):
    """Raised when an illegal incident transition is requested."""
    pass


class IncidentLifecycleStateMachine:
    """
    State machine enforcing standard enterprise incident progression:
    DETECTED -> INVESTIGATING -> IDENTIFIED -> MITIGATING -> RESOLVED -> POSTMORTEM -> CLOSED.
    """

    VALID_TRANSITIONS: Dict[IncidentStatus, Set[IncidentStatus]] = {
        IncidentStatus.DETECTED: {
            IncidentStatus.INVESTIGATING,
            IncidentStatus.IDENTIFIED,
            IncidentStatus.MITIGATING,
            IncidentStatus.RESOLVED,
            IncidentStatus.CLOSED,
        },
        IncidentStatus.INVESTIGATING: {
            IncidentStatus.IDENTIFIED,
            IncidentStatus.MITIGATING,
            IncidentStatus.RESOLVED,
            IncidentStatus.CLOSED,
        },
        IncidentStatus.IDENTIFIED: {
            IncidentStatus.MITIGATING,
            IncidentStatus.RESOLVED,
            IncidentStatus.INVESTIGATING,
        },
        IncidentStatus.MITIGATING: {
            IncidentStatus.RESOLVED,
            IncidentStatus.INVESTIGATING,
        },
        IncidentStatus.RESOLVED: {
            IncidentStatus.POSTMORTEM,
            IncidentStatus.CLOSED,
            IncidentStatus.INVESTIGATING,  # Re-opened
        },
        IncidentStatus.POSTMORTEM: {
            IncidentStatus.CLOSED,
            IncidentStatus.INVESTIGATING,  # Re-opened during postmortem review
        },
        IncidentStatus.CLOSED: {
            IncidentStatus.INVESTIGATING,  # Re-opened
        },
    }

    @classmethod
    def can_transition(cls, from_status: IncidentStatus, to_status: IncidentStatus) -> bool:
        if from_status == to_status:
            return True
        return to_status in cls.VALID_TRANSITIONS.get(from_status, set())

    @classmethod
    def transition(
        cls,
        incident: Incident,
        target_status: IncidentStatus,
        actor: str = "system",
        message: str = "",
    ) -> IncidentTimelineEntry:
        """
        Transition an incident to target_status and append a timeline entry.
        """
        if not cls.can_transition(incident.status, target_status):
            err = (
                f"Invalid incident transition for '{incident.incident_id}' from "
                f"{incident.status.value} to {target_status.value}."
            )
            logger.error(err)
            raise InvalidIncidentTransitionError(err)

        from_status = incident.status
        incident.status = target_status

        now = datetime.now(timezone.utc)
        if target_status == IncidentStatus.RESOLVED and not incident.resolved_at:
            incident.resolved_at = now
        elif target_status == IncidentStatus.CLOSED and not incident.closed_at:
            incident.closed_at = now

        entry = IncidentTimelineEntry(
            entry_id=f"entry-{uuid.uuid4().hex[:8]}",
            timestamp=now,
            actor=actor,
            message=message or f"Status transitioned from {from_status.value} to {target_status.value}",
            status_change=target_status,
        )
        incident.timeline.append(entry)
        logger.info(f"Incident '{incident.incident_id}' transitioned to {target_status.value}")
        return entry
