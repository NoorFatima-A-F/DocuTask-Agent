"""
Workflow Engine.
Implements IWorkflowEngine; serves as the central orchestration facade for workflow execution, signaling, and query.
"""

import logging
from typing import Any, Dict, Optional
from uuid import UUID
from app.agents.workflow.approval_workflow import ApprovalWorkflowEngine
from app.agents.workflow.context import WorkflowRequest, WorkflowResult
from app.agents.workflow.exceptions import UnsupportedWorkflowDefinitionError, WorkflowException
from app.agents.workflow.interfaces import IWorkflowEngine
from app.agents.workflow.manager import WorkflowManager
from app.agents.workflow.orchestrator import WorkflowOrchestrator
from app.agents.workflow.signal_manager import SignalManager
from app.agents.workflow.timer_manager import TimerManager
from app.agents.workflow.workflow_instance import WorkflowInstance
from app.agents.workflow.workflow_registry import WorkflowRegistry

logger = logging.getLogger(__name__)


class WorkflowEngine(IWorkflowEngine):
    """Central engine orchestrating long-running, multi-agent, and distributed workflows."""

    def __init__(
        self,
        manager: Optional[WorkflowManager] = None,
        orchestrator: Optional[WorkflowOrchestrator] = None,
        registry: Optional[WorkflowRegistry] = None,
        signal_manager: Optional[SignalManager] = None,
        approval_engine: Optional[ApprovalWorkflowEngine] = None,
        timer_manager: Optional[TimerManager] = None,
    ) -> None:
        self.manager = manager or WorkflowManager()
        self.orchestrator = orchestrator or WorkflowOrchestrator()
        self.registry = registry or WorkflowRegistry()
        self.signal_manager = signal_manager or SignalManager()
        self.approval_engine = approval_engine or ApprovalWorkflowEngine()
        self.timer_manager = timer_manager or TimerManager()

    async def start_workflow(self, request: WorkflowRequest) -> WorkflowResult:
        """Instantiates and executes a workflow requested by definition ID."""
        definition = self.registry.get_definition(request.definition_id)
        if not definition:
            raise UnsupportedWorkflowDefinitionError(
                f"Workflow definition {request.definition_id} not registered in registry."
            )

        # Create instance
        instance = await self.manager.create_instance(
            definition_id=request.definition_id,
            version=definition.version,
            context=request.context,
            input_data=request.input_data,
        )
        self.registry.register_instance(instance)

        # Orchestrate execution
        result = await self.orchestrator.orchestrate(definition, instance)

        # Update repository and registry
        latest_instance = await self.manager.get_instance(instance.instance_id)
        if latest_instance:
            self.registry.register_instance(latest_instance)

        return result

    async def signal_workflow(self, instance_id: UUID, signal_name: str, payload: Any) -> None:
        """Sends an external signal to a workflow instance."""
        payload_dict = payload if isinstance(payload, dict) else {"payload": payload}
        self.signal_manager.send_signal(instance_id, signal_name, payload_dict)

    async def get_workflow_status(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        """Retrieves current state and status of a workflow instance."""
        return await self.manager.get_instance(instance_id)

    async def pause_workflow(self, instance_id: UUID) -> WorkflowInstance:
        """Pauses a running workflow instance."""
        instance = await self.manager.pause_instance(instance_id)
        self.registry.register_instance(instance)
        return instance

    async def resume_workflow(self, instance_id: UUID) -> WorkflowInstance:
        """Resumes a paused workflow instance."""
        instance = await self.manager.resume_instance(instance_id)
        self.registry.register_instance(instance)
        return instance

    async def cancel_workflow(self, instance_id: UUID, reason: str = "User requested") -> WorkflowInstance:
        """Cancels an in-flight workflow instance."""
        instance = await self.manager.cancel_instance(instance_id, reason=reason)
        self.registry.register_instance(instance)
        return instance
