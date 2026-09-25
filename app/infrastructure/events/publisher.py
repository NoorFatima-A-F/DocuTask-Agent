"""Infrastructure Event Publisher and Audit Logger."""

import logging
from typing import Any, Callable, Dict, List, Optional
from .schemas import InfrastructureAuditEvent, InfrastructureEvent

logger = logging.getLogger(__name__)


class InfrastructureEventPublisher:
    """Dispatches infrastructure state change events and persists compliance audit logs."""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[InfrastructureEvent], None]]] = {}
        self._event_log: List[InfrastructureEvent] = []
        self._audit_log: List[InfrastructureAuditEvent] = []

    def subscribe(self, event_type: str, handler: Callable[[InfrastructureEvent], None]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(
        self,
        event_type: str,
        service_name: Optional[str] = None,
        resource_id: Optional[str] = None,
        environment: str = "PRODUCTION",
        payload: Optional[Dict[str, Any]] = None,
    ) -> InfrastructureEvent:
        event = InfrastructureEvent(
            event_type=event_type,
            service_name=service_name,
            resource_id=resource_id,
            environment=environment,
            payload=payload or {},
        )
        self._event_log.append(event)

        for handler in self._handlers.get(event_type, []):
            try:
                handler(event)
            except Exception as ex:
                logger.warning("Event handler error for %s: %s", event_type, ex)

        for handler in self._handlers.get("*", []):
            try:
                handler(event)
            except Exception as ex:
                logger.warning("Wildcard event handler error: %s", ex)

        return event

    def record_audit(
        self,
        actor: str,
        action: str,
        resource: str,
        environment: str,
        result: str = "SUCCESS",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> InfrastructureAuditEvent:
        audit_event = InfrastructureAuditEvent(
            actor=actor,
            action=action,
            resource=resource,
            environment=environment,
            result=result,
            metadata=metadata or {},
        )
        self._audit_log.append(audit_event)
        return audit_event

    def get_events(self, service_name: Optional[str] = None, event_type: Optional[str] = None) -> List[InfrastructureEvent]:
        events = list(self._event_log)
        if service_name:
            events = [e for e in events if e.service_name == service_name]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events

    def get_audits(self, environment: Optional[str] = None) -> List[InfrastructureAuditEvent]:
        audits = list(self._audit_log)
        if environment:
            audits = [a for a in audits if a.environment == environment]
        return audits
