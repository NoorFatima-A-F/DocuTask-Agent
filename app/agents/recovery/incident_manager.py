"""
Incident Manager.
Creates, updates, and routes operational incidents.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.recovery.failure import Failure, FailureSeverity
from app.agents.recovery.incident import Incident, IncidentSeverity, IncidentStatus


class IncidentManager:
    """Manages creation, tracking, and resolution of escalated incidents."""

    def __init__(self):
        self._incidents: Dict[UUID, Incident] = {}

    def create_incident(self, failure: Failure, title: str, description: str) -> Incident:
        sev_map = {
            FailureSeverity.CRITICAL: IncidentSeverity.SEV1,
            FailureSeverity.HIGH: IncidentSeverity.SEV2,
            FailureSeverity.MEDIUM: IncidentSeverity.SEV3,
            FailureSeverity.LOW: IncidentSeverity.SEV4
        }
        incident = Incident(
            execution_id=failure.identity.execution_id,
            failure_id=failure.identity.failure_id,
            title=title,
            description=description,
            severity=sev_map.get(failure.severity, IncidentSeverity.SEV3)
        )
        self._incidents[incident.incident_id] = incident
        return incident

    def get_incident(self, incident_id: UUID) -> Optional[Incident]:
        return self._incidents.get(incident_id)

    def list_open_incidents(self) -> List[Incident]:
        return [inc for inc in self._incidents.values() if inc.status == IncidentStatus.OPEN]
