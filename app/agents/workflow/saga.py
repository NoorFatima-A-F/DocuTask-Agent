"""
Saga Orchestrator.
Orchestrates distributed Saga transactions across steps and coordinates rollback compensations upon step failure.
"""

import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional
from uuid import UUID
from app.agents.workflow.compensation import CompensationCoordinator
from app.agents.workflow.interfaces import ISagaOrchestrator
from app.agents.workflow.workflow_node import WorkflowNode

logger = logging.getLogger(__name__)


class SagaOrchestrator(ISagaOrchestrator):
    """Coordinates Saga forward execution and compensation rollbacks."""

    def __init__(self, coordinator: Optional[CompensationCoordinator] = None) -> None:
        self.coordinator = coordinator or CompensationCoordinator()
        self._handlers: Dict[str, Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]] = {}

    def register_handler(
        self,
        name: str,
        handler: Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]],
    ) -> None:
        """Registers an action or compensating handler."""
        self._handlers[name] = handler

    async def execute_saga_step(
        self,
        workflow_id: UUID,
        node: WorkflowNode,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Executes a forward Saga step and records it in the compensation journal.
        If the forward step fails, compensation is automatically triggered.
        """
        handler = self._handlers.get(node.handler)
        if not handler:
            raise KeyError(f"Handler '{node.handler}' not registered for Saga node '{node.node_id}'")

        try:
            result = await handler(input_data)
            output_dict = result if isinstance(result, dict) else {"result": result}
            self.coordinator.record_step(
                workflow_id=workflow_id,
                node_id=node.node_id,
                action_name=node.handler,
                compensating_handler=node.compensating_handler,
                input_data=input_data,
                output_data=output_dict,
            )
            return output_dict
        except Exception as exc:
            logger.error(
                f"Saga forward step '{node.node_id}' failed: {exc}. Initiating rollback compensation."
            )
            await self.execute_compensation(workflow_id)
            raise

    async def execute_compensation(
        self,
        workflow_id: UUID,
    ) -> List[Dict[str, Any]]:
        """Executes backward compensation for all executed steps in reverse order."""
        return await self.coordinator.execute_compensation(
            workflow_id=workflow_id,
            handler_resolver=lambda name: self._handlers.get(name),
        )
