"""Safety Event Definitions & Event Publisher."""

from typing import Dict, Any, List, Callable, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from ..gateway.decision import SafetyDecision, SafetyViolation, ViolationSeverity


class SafetyBaseEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    event_type: str
    tenant_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)


class PromptInjectionDetectedEvent(SafetyBaseEvent):
    event_type: str = "safety.injection.detected"


class JailbreakAttemptEvent(SafetyBaseEvent):
    event_type: str = "safety.jailbreak.detected"


class PIILeakageBlockedEvent(SafetyBaseEvent):
    event_type: str = "safety.privacy.pii_blocked"


class ToolSafetyViolationEvent(SafetyBaseEvent):
    event_type: str = "safety.tool.violation"


class HallucinationDetectedEvent(SafetyBaseEvent):
    event_type: str = "safety.hallucination.detected"


class SafetyIncidentCreatedEvent(SafetyBaseEvent):
    event_type: str = "safety.incident.created"


class SafetyGatewayDecisionEvent(SafetyBaseEvent):
    event_type: str = "safety.gateway.decision"


class SafetyEventPublisher:
    """Dispatches safety events to registered subscribers and maintains an audit log."""

    def __init__(self):
        self._subscribers: List[Callable[[SafetyBaseEvent], None]] = []
        self._event_log: List[SafetyBaseEvent] = []

    def subscribe(self, callback: Callable[[SafetyBaseEvent], None]) -> None:
        self._subscribers.append(callback)

    def publish(self, event: SafetyBaseEvent) -> None:
        self._event_log.append(event)
        for sub in self._subscribers:
            try:
                sub(event)
            except Exception:
                pass  # Do not let subscriber failures disrupt safety pipeline

    def get_events(self, tenant_id: Optional[str] = None, event_type: Optional[str] = None) -> List[SafetyBaseEvent]:
        events = self._event_log
        if tenant_id:
            events = [e for e in events if e.tenant_id == tenant_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events
