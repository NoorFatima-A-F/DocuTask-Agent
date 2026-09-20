"""
DocuTask Agent - Event Publisher Helper
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, Any, Optional
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem, EventSeverity
from app.runtime.events.models.event_metadata import EventActor


class EventPublisher:
    """
    Publisher interface for emitting structured domain events to the EventBus.
    """

    def __init__(self, bus: Any, default_subsystem: EventSubsystem, default_component: str):
        self.bus = bus
        self.subsystem = default_subsystem
        self.component = default_component

    async def emit(
        self,
        event_type: DomainEventType,
        mission_id: str,
        payload: Dict[str, Any],
        actor_id: str = "system",
        actor_type: str = "SYSTEM",
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        causation_id: Optional[str] = None,
        severity: EventSeverity = EventSeverity.INFO,
    ) -> DomainEvent:
        """Constructs and publishes a domain event."""
        event = DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            causation_id=causation_id or f"cause-{event_type.value.lower()}",
            actor=EventActor(actor_id=actor_id, actor_type=actor_type),
            subsystem=self.subsystem,
            component=self.component,
            event_type=event_type,
            payload=payload,
            severity=severity,
        )
        await self.bus.publish(event)
        return event
