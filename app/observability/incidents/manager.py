"""Incident Management Platform and Lifecycle State Machine."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .timeline import IncidentTimeline, TimelineEventType


class IncidentSeverity(str, Enum):
    SEV1_CRITICAL = "SEV1_CRITICAL"
    SEV2_MAJOR = "SEV2_MAJOR"
    SEV3_MODERATE = "SEV3_MODERATE"
    SEV4_MINOR = "SEV4_MINOR"


class IncidentStatus(str, Enum):
    DETECTED = "DETECTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    POSTMORTEM = "POSTMORTEM"


@dataclass
class IncidentRecord:
    incident_id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.DETECTED
    affected_services: List[str] = field(default_factory=list)
    commander: Optional[str] = None
    responders: List[str] = field(default_factory=list)
    root_cause: Optional[str] = None
    timeline: IncidentTimeline = field(default_factory=IncidentTimeline)
    created_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
    tags: List[str] = field(default_factory=list)


class IncidentManager:
    """Manages active enterprise incidents, status progression, and SRE responder coordination."""

    def __init__(self):
        self._incidents: Dict[str, IncidentRecord] = {}

    def create_incident(
        self,
        title: str,
        description: str,
        severity: IncidentSeverity,
        affected_services: Optional[List[str]] = None,
        author: str = "System Detector",
    ) -> IncidentRecord:
        inc_id = f"inc-{uuid.uuid4().hex[:8]}"
        timeline = IncidentTimeline()
        timeline.add_entry(author, TimelineEventType.DETECTION, f"Incident created: {title}")

        record = IncidentRecord(
            incident_id=inc_id,
            title=title,
            description=description,
            severity=severity,
            status=IncidentStatus.DETECTED,
            affected_services=affected_services or [],
            timeline=timeline,
        )
        self._incidents[inc_id] = record
        return record

    def get_incident(self, incident_id: str) -> Optional[IncidentRecord]:
        return self._incidents.get(incident_id)

    def transition_status(
        self,
        incident_id: str,
        new_status: IncidentStatus,
        actor: str,
        note: str = "",
    ) -> bool:
        inc = self._incidents.get(incident_id)
        if not inc:
            return False

        old_status = inc.status
        inc.status = new_status
        msg = f"Status transitioned from {old_status.value} to {new_status.value}. {note}".strip()
        inc.timeline.add_entry(actor, TimelineEventType.STATUS_CHANGE, msg)

        if new_status == IncidentStatus.RESOLVED:
            inc.resolved_at = time.time()

        return True

    def assign_commander(self, incident_id: str, commander: str, actor: str) -> bool:
        inc = self._incidents.get(incident_id)
        if not inc:
            return False
        inc.commander = commander
        if commander not in inc.responders:
            inc.responders.append(commander)
        inc.timeline.add_entry(actor, TimelineEventType.NOTE, f"Assigned incident commander: {commander}")
        return True

    def record_mitigation_action(self, incident_id: str, actor: str, action: str) -> bool:
        inc = self._incidents.get(incident_id)
        if not inc:
            return False
        inc.timeline.add_entry(actor, TimelineEventType.MITIGATION_ACTION, action)
        return True

    def list_incidents(
        self,
        status: Optional[IncidentStatus] = None,
        severity: Optional[IncidentSeverity] = None,
    ) -> List[IncidentRecord]:
        results = list(self._incidents.values())
        if status:
            results = [i for i in results if i.status == status]
        if severity:
            results = [i for i in results if i.severity == severity]
        return results
