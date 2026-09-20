"""
Configuration Observability & Audit Trail Service.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ConfigAuditEvent:
    event_id: str = field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:8]}")
    event_type: str = "CONFIG_ACTIVATED"
    actor: str = "system"
    environment: str = "PRODUCTION"
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ConfigurationObservabilityService:
    def __init__(self):
        self._events: List[ConfigAuditEvent] = []

    def record_event(
        self,
        event_type: str,
        actor: str,
        environment: str,
        details: Optional[Dict[str, Any]] = None
    ) -> ConfigAuditEvent:
        ev = ConfigAuditEvent(
            event_type=event_type,
            actor=actor,
            environment=environment,
            details=details or {}
        )
        self._events.append(ev)
        return ev

    def query_events(self, event_type: Optional[str] = None, environment: Optional[str] = None) -> List[ConfigAuditEvent]:
        res = self._events
        if event_type:
            res = [e for e in res if e.event_type == event_type]
        if environment:
            res = [e for e in res if e.environment == environment]
        return list(res)


config_observability = ConfigurationObservabilityService()
