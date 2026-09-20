"""
DocuTask Agent - Mission Event Factory Builders
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, Any, Optional
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem, EventSeverity
from app.runtime.events.models.event_metadata import EventActor


class MissionEventFactory:
    """Factory for generating standardized Mission Lifecycle Domain Events."""

    @staticmethod
    def created(
        mission_id: str,
        goal: str,
        document_count: int = 1,
        correlation_id: Optional[str] = None,
        actor_id: str = "MissionCommander",
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            causation_id=f"cause-init-{mission_id}",
            actor=EventActor(actor_id=actor_id, actor_type="SYSTEM", role="COMMANDER"),
            subsystem=EventSubsystem.MISSION_CONTROL,
            component="MissionLifecycleEngine",
            event_type=DomainEventType.MISSION_CREATED,
            payload={
                "goal": goal,
                "document_count": document_count,
                "status": "INITIALIZED",
            },
            severity=EventSeverity.INFO,
        )

    @staticmethod
    def completed(
        mission_id: str,
        total_tasks: int,
        duration_seconds: float,
        cost_usd: float,
        correlation_id: Optional[str] = None,
        parent_event_id: Optional[str] = None,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            actor=EventActor(actor_id="MissionCommander", actor_type="SYSTEM", role="COMMANDER"),
            subsystem=EventSubsystem.MISSION_CONTROL,
            component="MissionLifecycleEngine",
            event_type=DomainEventType.MISSION_COMPLETED,
            payload={
                "total_tasks_completed": total_tasks,
                "duration_seconds": duration_seconds,
                "total_cost_usd": cost_usd,
                "status": "SUCCESS",
            },
            severity=EventSeverity.INFO,
        )
