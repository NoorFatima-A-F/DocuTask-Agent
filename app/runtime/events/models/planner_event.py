"""
DocuTask Agent - Planner Event Factory Builders
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any, Optional
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem, EventSeverity
from app.runtime.events.models.event_metadata import EventActor


class PlannerEventFactory:
    """Factory for generating standardized Planner Domain Events."""

    @staticmethod
    def started(
        mission_id: str,
        goal: str,
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            actor=EventActor(actor_id="AutonomousPlanner", actor_type="PLANNER", role="CHIEF_PLANNER"),
            subsystem=EventSubsystem.PLANNER,
            component="DynamicPlannerEngine",
            event_type=DomainEventType.PLANNER_STARTED,
            payload={"goal": goal, "strategy": "DYNAMIC_DAG_SYNTHESIS"},
            severity=EventSeverity.INFO,
        )

    @staticmethod
    def finished(
        mission_id: str,
        task_count: int,
        estimated_cost_usd: float,
        critical_path_latency_ms: float,
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            actor=EventActor(actor_id="AutonomousPlanner", actor_type="PLANNER", role="CHIEF_PLANNER"),
            subsystem=EventSubsystem.PLANNER,
            component="DynamicPlannerEngine",
            event_type=DomainEventType.PLANNER_FINISHED,
            payload={
                "generated_task_count": task_count,
                "estimated_cost_usd": estimated_cost_usd,
                "critical_path_latency_ms": critical_path_latency_ms,
            },
            severity=EventSeverity.INFO,
        )

    @staticmethod
    def replanned(
        mission_id: str,
        reason: str,
        mutated_nodes: List[str],
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            actor=EventActor(actor_id="AutonomousPlanner", actor_type="PLANNER", role="CHIEF_PLANNER"),
            subsystem=EventSubsystem.PLANNER,
            component="DynamicPlannerEngine",
            event_type=DomainEventType.PLANNER_REPLANNED,
            payload={
                "replan_reason": reason,
                "mutated_node_ids": mutated_nodes,
            },
            severity=EventSeverity.WARNING,
        )
