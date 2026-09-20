"""Safety Incident Lifecycle Manager."""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from .lifecycle import IncidentLifecycleState, SafetyIncident, SafetyIncidentAuditEntry


class SafetyIncidentManager:
    """Manages creation, state machine transitions, and audit tracking for safety incidents."""

    # Valid transitions
    VALID_TRANSITIONS: Dict[IncidentLifecycleState, List[IncidentLifecycleState]] = {
        IncidentLifecycleState.DETECTED: [IncidentLifecycleState.CLASSIFIED, IncidentLifecycleState.CLOSED],
        IncidentLifecycleState.CLASSIFIED: [IncidentLifecycleState.INVESTIGATING, IncidentLifecycleState.MITIGATED, IncidentLifecycleState.CLOSED],
        IncidentLifecycleState.INVESTIGATING: [IncidentLifecycleState.MITIGATED, IncidentLifecycleState.CLOSED],
        IncidentLifecycleState.MITIGATED: [IncidentLifecycleState.RESOLVED, IncidentLifecycleState.INVESTIGATING],
        IncidentLifecycleState.RESOLVED: [IncidentLifecycleState.CLOSED, IncidentLifecycleState.INVESTIGATING],
        IncidentLifecycleState.CLOSED: [],
    }

    def __init__(self):
        self._incidents: Dict[str, SafetyIncident] = {}

    def create_incident(
        self,
        tenant_id: str,
        title: str,
        description: str,
        category: SafetyCategory,
        severity: ViolationSeverity,
        context_id: Optional[str] = None,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        violations: Optional[List[SafetyViolation]] = None,
        actor: str = "system",
    ) -> SafetyIncident:
        incident = SafetyIncident(
            tenant_id=tenant_id,
            title=title,
            description=description,
            category=category,
            severity=severity,
            context_id=context_id,
            user_id=user_id,
            agent_id=agent_id,
            violations=violations or [],
            state=IncidentLifecycleState.DETECTED,
        )

        # Record creation in audit trail
        incident.audit_trail.append(
            SafetyIncidentAuditEntry(
                actor=actor,
                action="INCIDENT_CREATED",
                new_state=IncidentLifecycleState.DETECTED,
                notes=f"Initial safety incident created with severity {severity.value}",
            )
        )

        self._incidents[incident.incident_id] = incident
        return incident

    def get_incident(self, incident_id: str, tenant_id: Optional[str] = None) -> Optional[SafetyIncident]:
        incident = self._incidents.get(incident_id)
        if not incident:
            return None
        if tenant_id and incident.tenant_id != tenant_id:
            return None
        return incident

    def list_incidents(
        self,
        tenant_id: str,
        state: Optional[IncidentLifecycleState] = None,
        severity: Optional[ViolationSeverity] = None,
    ) -> List[SafetyIncident]:
        results: List[SafetyIncident] = []
        for inc in self._incidents.values():
            if inc.tenant_id != tenant_id:
                continue
            if state and inc.state != state:
                continue
            if severity and inc.severity != severity:
                continue
            results.append(inc)
        return results

    def transition_state(
        self,
        incident_id: str,
        new_state: IncidentLifecycleState,
        actor: str,
        notes: Optional[str] = None,
        tenant_id: Optional[str] = None,
    ) -> SafetyIncident:
        incident = self.get_incident(incident_id, tenant_id)
        if not incident:
            raise ValueError(f"Incident '{incident_id}' not found")

        current_state = incident.state
        if new_state not in self.VALID_TRANSITIONS.get(current_state, []):
            raise ValueError(f"Invalid state transition from '{current_state.value}' to '{new_state.value}'")

        incident.state = new_state
        incident.updated_at = datetime.now(timezone.utc)
        if new_state in [IncidentLifecycleState.RESOLVED, IncidentLifecycleState.CLOSED]:
            incident.resolved_at = datetime.now(timezone.utc)

        incident.audit_trail.append(
            SafetyIncidentAuditEntry(
                actor=actor,
                action=f"STATE_TRANSITION_{new_state.value}",
                previous_state=current_state,
                new_state=new_state,
                notes=notes,
            )
        )

        return incident

    def add_investigation_note(
        self,
        incident_id: str,
        actor: str,
        notes: str,
        tenant_id: Optional[str] = None,
    ) -> SafetyIncident:
        incident = self.get_incident(incident_id, tenant_id)
        if not incident:
            raise ValueError(f"Incident '{incident_id}' not found")

        incident.audit_trail.append(
            SafetyIncidentAuditEntry(
                actor=actor,
                action="NOTE_ADDED",
                notes=notes,
            )
        )
        incident.updated_at = datetime.now(timezone.utc)
        return incident
