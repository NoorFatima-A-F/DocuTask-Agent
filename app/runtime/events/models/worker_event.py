"""
DocuTask Agent - Worker Event Factory Builders
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, Any, Optional
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType, EventSubsystem, EventSeverity
from app.runtime.events.models.event_metadata import EventActor


class WorkerEventFactory:
    """Factory for generating standardized Worker & Task Execution Domain Events."""

    @staticmethod
    def task_assigned(
        mission_id: str,
        task_id: str,
        worker_id: str,
        task_type: str,
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            actor=EventActor(actor_id=worker_id, actor_type="WORKER", role="DAG_WORKER"),
            subsystem=EventSubsystem.WORKER_POOL,
            component="WorkerPoolScheduler",
            event_type=DomainEventType.TASK_ASSIGNED,
            payload={
                "task_id": task_id,
                "worker_id": worker_id,
                "task_type": task_type,
            },
            severity=EventSeverity.INFO,
        )

    @staticmethod
    def task_completed(
        mission_id: str,
        task_id: str,
        worker_id: str,
        duration_ms: float,
        tokens_used: int = 0,
        parent_event_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id=mission_id,
            parent_event_id=parent_event_id,
            correlation_id=correlation_id or f"corr-{mission_id}",
            actor=EventActor(actor_id=worker_id, actor_type="WORKER", role="DAG_WORKER"),
            subsystem=EventSubsystem.WORKER_POOL,
            component="WorkerPoolScheduler",
            event_type=DomainEventType.TASK_COMPLETED,
            payload={
                "task_id": task_id,
                "worker_id": worker_id,
                "duration_ms": duration_ms,
                "tokens_used": tokens_used,
            },
            severity=EventSeverity.INFO,
        )

    @staticmethod
    def worker_heartbeat(
        worker_id: str,
        cpu_usage_pct: float,
        memory_mb: float,
        active_tasks: int,
    ) -> DomainEvent:
        return DomainEvent(
            mission_id="global-runtime",
            actor=EventActor(actor_id=worker_id, actor_type="WORKER", role="DAG_WORKER"),
            subsystem=EventSubsystem.WORKER_POOL,
            component="WorkerNodeSupervisor",
            event_type=DomainEventType.WORKER_HEARTBEAT,
            payload={
                "worker_id": worker_id,
                "cpu_usage_pct": cpu_usage_pct,
                "memory_mb": memory_mb,
                "active_tasks": active_tasks,
            },
            severity=EventSeverity.DEBUG,
        )
