"""
Workflow Manager.
Coordinates workflow instance creation, lifecycle transitions, persistence, and domain event publishing.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from app.agents.workflow.context import WorkflowContext
from app.agents.workflow.events import (
    WorkflowCancelledEvent,
    WorkflowCompletedEvent,
    WorkflowCreatedEvent,
    WorkflowFailedEvent,
    WorkflowPausedEvent,
    WorkflowResumedEvent,
    WorkflowStartedEvent,
)
from app.agents.workflow.exceptions import WorkflowException
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.metadata import WorkflowIdentity
from app.agents.workflow.metrics import WorkflowMetricsCollector
from app.agents.workflow.workflow_instance import WorkflowInstance
from app.agents.workflow.workflow_repository import (
    IWorkflowRepository,
    InMemoryWorkflowRepository,
)
from app.agents.workflow.workflow_state import WorkflowState
from app.agents.workflow.workflow_version import WorkflowVersion

logger = logging.getLogger(__name__)


class WorkflowManager:
    """Manages workflow instance lifecycle, state persistence, and event telemetry."""

    def __init__(
        self,
        repository: Optional[IWorkflowRepository] = None,
        event_bus: Optional[Any] = None,
        metrics: Optional[WorkflowMetricsCollector] = None,
    ) -> None:
        self.repository = repository or InMemoryWorkflowRepository()
        self.event_bus = event_bus
        self.metrics = metrics or WorkflowMetricsCollector()

    async def create_instance(
        self,
        definition_id: UUID,
        version: Optional[WorkflowVersion] = None,
        context: Optional[WorkflowContext] = None,
        input_data: Optional[Dict[str, Any]] = None,
    ) -> WorkflowInstance:
        """Instantiates a new workflow instance in CREATED state."""
        instance_id = uuid4()
        identity = WorkflowIdentity(
            instance_id=instance_id,
            definition_id=definition_id,
            version=version or WorkflowVersion(major=1, minor=0, patch=0),
        )
        initial_state = WorkflowState(variables=dict(input_data or {}))
        instance = WorkflowInstance(
            identity=identity,
            definition_id=definition_id,
            state=WorkflowLifecycleState.CREATED,
            workflow_state=initial_state,
        )

        await self.repository.save_instance(instance)
        await self._publish_event(
            WorkflowCreatedEvent(
                execution_id=str(instance_id),
                payload={"definition_id": str(definition_id)},
            )
        )
        return instance

    async def start_instance(self, instance_id: UUID) -> WorkflowInstance:
        """Transitions instance from CREATED -> READY -> RUNNING."""
        instance = await self._get_or_raise(instance_id)
        ready_instance = instance.transition_to(WorkflowLifecycleState.READY)
        running_instance = ready_instance.transition_to(WorkflowLifecycleState.RUNNING)
        await self.repository.save_instance(running_instance)

        self.metrics.record_workflow_started()
        await self._publish_event(
            WorkflowStartedEvent(
                execution_id=str(instance_id),
                payload={"state": running_instance.state.value},
            )
        )
        return running_instance

    async def pause_instance(self, instance_id: UUID) -> WorkflowInstance:
        """Transitions a running or waiting workflow to PAUSED state."""
        instance = await self._get_or_raise(instance_id)
        paused_instance = instance.transition_to(WorkflowLifecycleState.PAUSED)
        await self.repository.save_instance(paused_instance)

        self.metrics.record_workflow_paused()
        await self._publish_event(
            WorkflowPausedEvent(
                execution_id=str(instance_id),
                payload={"state": paused_instance.state.value},
            )
        )
        return paused_instance

    async def resume_instance(self, instance_id: UUID) -> WorkflowInstance:
        """Resumes a paused workflow back to RUNNING state."""
        instance = await self._get_or_raise(instance_id)
        resumed_instance = instance.transition_to(WorkflowLifecycleState.RUNNING)
        await self.repository.save_instance(resumed_instance)

        self.metrics.record_workflow_resumed()
        await self._publish_event(
            WorkflowResumedEvent(
                execution_id=str(instance_id),
                payload={"state": resumed_instance.state.value},
            )
        )
        return resumed_instance

    async def cancel_instance(self, instance_id: UUID, reason: str = "User requested") -> WorkflowInstance:
        """Transitions instance to CANCELLED state."""
        instance = await self._get_or_raise(instance_id)
        cancelled_instance = instance.transition_to(WorkflowLifecycleState.CANCELLED)
        await self.repository.save_instance(cancelled_instance)

        self.metrics.record_workflow_cancelled()
        await self._publish_event(
            WorkflowCancelledEvent(
                execution_id=str(instance_id),
                payload={"reason": reason},
            )
        )
        return cancelled_instance

    async def complete_instance(
        self,
        instance_id: UUID,
        outputs: Optional[Dict[str, Any]] = None,
        duration_ms: float = 100.0,
    ) -> WorkflowInstance:
        """Transitions instance to COMPLETED state."""
        instance = await self._get_or_raise(instance_id)
        completed_instance = instance.transition_to(WorkflowLifecycleState.COMPLETED)
        if outputs:
            updated_state = completed_instance.workflow_state
            for k, v in outputs.items():
                updated_state = updated_state.set_variable(k, v)
            completed_instance = completed_instance.model_copy(update={"workflow_state": updated_state})

        await self.repository.save_instance(completed_instance)
        self.metrics.record_workflow_completed(duration_ms)
        await self._publish_event(
            WorkflowCompletedEvent(
                execution_id=str(instance_id),
                payload={"outputs": outputs or {}},
            )
        )
        return completed_instance

    async def fail_instance(
        self,
        instance_id: UUID,
        error: str,
    ) -> WorkflowInstance:
        """Transitions instance to FAILED state."""
        instance = await self._get_or_raise(instance_id)
        failed_instance = instance.transition_to(WorkflowLifecycleState.FAILED)
        failed_instance = failed_instance.model_copy(update={"errors": [*failed_instance.errors, error]})
        await self.repository.save_instance(failed_instance)

        self.metrics.record_workflow_failed()
        await self._publish_event(
            WorkflowFailedEvent(
                execution_id=str(instance_id),
                payload={"error": error},
            )
        )
        return failed_instance

    async def get_instance(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        return await self.repository.get_instance(instance_id)

    async def _get_or_raise(self, instance_id: UUID) -> WorkflowInstance:
        instance = await self.repository.get_instance(instance_id)
        if not instance:
            raise WorkflowException(f"Workflow instance {instance_id} not found.", workflow_id=instance_id)
        return instance

    async def _publish_event(self, event: Any) -> None:
        if self.event_bus and hasattr(self.event_bus, "publish"):
            try:
                await self.event_bus.publish(event)
            except Exception as e:
                logger.warning(f"Failed to publish event {type(event).__name__}: {e}")
