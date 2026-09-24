"""
Escalation Engine.
Manages progressive escalation from Automatic Recovery -> Planner Re-entry -> Human Approval -> Incident.
"""

from enum import Enum
from app.agents.recovery.failure import Failure
from app.agents.recovery.incident_manager import IncidentManager


class EscalationLevel(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    PLANNER_RE_ENTRY = "PLANNER_RE_ENTRY"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    INCIDENT = "INCIDENT"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"


class EscalationEngine:
    """Evaluates escalation thresholds and triggers human handoff or incident creation."""

    def __init__(self, incident_manager: IncidentManager | None = None):
        self.incident_manager = incident_manager or IncidentManager()

    def escalate(self, failure: Failure, current_level: EscalationLevel) -> EscalationLevel:
        """Determines the next escalation tier."""
        if current_level == EscalationLevel.AUTOMATIC:
            return EscalationLevel.PLANNER_RE_ENTRY
        elif current_level == EscalationLevel.PLANNER_RE_ENTRY:
            return EscalationLevel.HUMAN_APPROVAL
        elif current_level == EscalationLevel.HUMAN_APPROVAL:
            # Trigger Incident
            self.incident_manager.create_incident(
                failure,
                title=f"Unrecoverable failure on execution {failure.identity.execution_id}",
                description=failure.evidence.error_message
            )
            return EscalationLevel.INCIDENT
        return EscalationLevel.PERMANENT_FAILURE
