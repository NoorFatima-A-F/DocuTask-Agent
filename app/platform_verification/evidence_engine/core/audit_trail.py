"""
Immutable Audit Trail Service.
Appends cryptographically signed audit events adhering to past-tense standards.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.platform_verification.evidence_engine.domain.models import AuditEvent
from app.platform_verification.evidence_engine.domain.interfaces import AuditLoggerInterface


class ImmutableAuditTrail(AuditLoggerInterface):
    def __init__(self):
        self._events: List[AuditEvent] = []

    def record_event(
        self,
        actor: str,
        action: str,
        resource: str,
        details: Optional[Dict[str, Any]] = None,
        previous_state: Optional[str] = None,
        new_state: Optional[str] = None,
    ) -> AuditEvent:
        event = AuditEvent(
            actor=actor,
            action=action,
            resource=resource,
            details=details or {},
            previous_state=previous_state,
            new_state=new_state,
        )
        self._events.append(event)
        return event

    def get_events_for_resource(self, resource: str) -> List[AuditEvent]:
        return [e for e in self._events if e.resource == resource]

    def query_events(
        self,
        resource: Optional[str] = None,
        action: Optional[str] = None
    ) -> List[AuditEvent]:
        results = self._events
        if resource:
            results = [e for e in results if e.resource == resource]
        if action:
            results = [e for e in results if e.action == action]
        return list(results)

    def verify_audit_integrity(self) -> bool:
        for event in self._events:
            if event.compute_signature() != event.event_signature:
                return False
        return True


audit_trail = ImmutableAuditTrail()
