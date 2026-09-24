from __future__ import annotations
"""
Incident Manager.

Central coordination for creating, deduping, correlating, escalating,
and resolving infrastructure incidents across DocuTask Agent.
"""


import logging
from app.core.security import sanitize_log_input
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.infrastructure.incidents.lifecycle import IncidentLifecycleStateMachine
from app.infrastructure.incidents.models import (
    Incident,
    IncidentStatus,
    IncidentTimelineEntry,
)
from app.infrastructure.incidents.notifications import (
    IncidentNotifier,
    NotificationChannel,
)
from app.infrastructure.reliability.models import SeverityLevel

logger = logging.getLogger("infrastructure.incidents.manager")


class IncidentManager:
    """
    Coordinates platform incident lifecycle and multi-channel alerting.
    """

    def __init__(self, notifier: Optional[IncidentNotifier] = None) -> None:
        self.notifier = notifier or IncidentNotifier()
        self._incidents: Dict[str, Incident] = {}
        self._component_to_active_incident: Dict[str, str] = {}  # component_id -> incident_id

    def create_incident(
        self,
        incident_id: str,
        title: str,
        severity: SeverityLevel,
        impacted_components: Optional[List[str]] = None,
        impacted_tenants: Optional[List[str]] = None,
        lead_responder: Optional[str] = None,
        root_cause: Optional[str] = None,
        actor: str = "system",
    ) -> Incident:
        """Create and register a new incident, notifying configured channels."""
        components = impacted_components or []
        incident = Incident(
            incident_id=incident_id,
            title=title,
            severity=severity,
            status=IncidentStatus.DETECTED,
            impacted_components=components,
            impacted_tenants=impacted_tenants or [],
            lead_responder=lead_responder,
            root_cause=root_cause,
        )

        initial_entry = IncidentTimelineEntry(
            entry_id=f"entry-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(timezone.utc),
            actor=actor,
            message=f"Incident opened with severity {severity.value}. Title: {title}",
            status_change=IncidentStatus.DETECTED,
        )
        incident.timeline.append(initial_entry)
        self._incidents[incident_id] = incident

        for comp in components:
            self._component_to_active_incident[comp] = incident_id

        # Dispatch alerts
        self.notifier.dispatch(
            message_id=f"alert-{uuid.uuid4().hex[:8]}",
            incident_id=incident_id,
            channel=NotificationChannel.EVENT_BUS,
            severity=severity,
            title=f"[{severity.value}] {title}",
            content=f"Impacted components: {components}",
        )

        if severity in (SeverityLevel.MAJOR, SeverityLevel.CRITICAL, SeverityLevel.CATASTROPHIC):
            self.notifier.dispatch(
                message_id=f"alert-{uuid.uuid4().hex[:8]}",
                incident_id=incident_id,
                channel=NotificationChannel.PAGERDUTY,
                severity=severity,
                title=f"URGENT: [{severity.value}] {title}",
                content=f"Immediate response required for {components}",
            )

        logger.info(f"Created incident '{sanitize_log_input(incident_id)}' with severity {severity.value}")
        return incident

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self._incidents.get(incident_id)

    def transition_incident(
        self,
        incident_id: str,
        target_status: IncidentStatus,
        actor: str = "system",
        message: str = "",
    ) -> IncidentTimelineEntry:
        """Advance incident state through its lifecycle."""
        incident = self._incidents.get(incident_id)
        if not incident:
            raise KeyError(f"Incident '{incident_id}' not found.")

        entry = IncidentLifecycleStateMachine.transition(
            incident=incident,
            target_status=target_status,
            actor=actor,
            message=message,
        )

        if target_status in (IncidentStatus.RESOLVED, IncidentStatus.CLOSED):
            for comp in incident.impacted_components:
                if self._component_to_active_incident.get(comp) == incident_id:
                    del self._component_to_active_incident[comp]

        return entry

    def escalate_severity(
        self,
        incident_id: str,
        new_severity: SeverityLevel,
        actor: str = "system",
        reason: str = "",
    ) -> None:
        """Escalate severity of an existing incident."""
        incident = self._incidents.get(incident_id)
        if not incident:
            raise KeyError(f"Incident '{incident_id}' not found.")

        old_severity = incident.severity
        incident.severity = new_severity
        entry = IncidentTimelineEntry(
            entry_id=f"entry-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(timezone.utc),
            actor=actor,
            message=f"Severity escalated from {old_severity.value} to {new_severity.value}. Reason: {reason}",
        )
        incident.timeline.append(entry)

        # Notify escalation
        self.notifier.dispatch(
            message_id=f"alert-{uuid.uuid4().hex[:8]}",
            incident_id=incident_id,
            channel=NotificationChannel.PAGERDUTY,
            severity=new_severity,
            title=f"ESCALATION: [{new_severity.value}] {incident.title}",
            content=f"Severity increased: {reason}",
        )

    def list_active_incidents(self) -> List[Incident]:
        return [
            inc for inc in self._incidents.values()
            if inc.status not in (IncidentStatus.RESOLVED, IncidentStatus.CLOSED)
        ]

    def list_all_incidents(self) -> List[Incident]:
        return list(self._incidents.values())
