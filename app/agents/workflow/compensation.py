"""
Compensation Coordinator.
Coordinates reverse-order compensation transactions for distributed Sagas upon workflow or step failure.
"""

import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.workflow.exceptions import MissingCompensationPathError, WorkflowException

logger = logging.getLogger(__name__)


class CompensationStep(BaseModel):
    """A record of an executed forward step that may need compensation."""
    node_id: str
    action_name: str
    compensating_handler: Optional[str] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)


class CompensationCoordinator:
    """Manages the registration and backward execution of compensation steps."""

    def __init__(self, strict_mode: bool = False) -> None:
        self.strict_mode = strict_mode
        self._compensation_journal: Dict[UUID, List[CompensationStep]] = {}

    def record_step(
        self,
        workflow_id: UUID,
        node_id: str,
        action_name: str,
        compensating_handler: Optional[str],
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
    ) -> None:
        """Records a successful forward step in the compensation journal."""
        step = CompensationStep(
            node_id=node_id,
            action_name=action_name,
            compensating_handler=compensating_handler,
            input_data=input_data,
            output_data=output_data,
        )
        self._compensation_journal.setdefault(workflow_id, []).append(step)

    def get_journal(self, workflow_id: UUID) -> List[CompensationStep]:
        """Returns the recorded forward steps for the workflow."""
        return list(self._compensation_journal.get(workflow_id, []))

    async def execute_compensation(
        self,
        workflow_id: UUID,
        handler_resolver: Callable[[str], Optional[Callable[[Dict[str, Any]], Coroutine[Any, Any, Any]]]],
    ) -> List[Dict[str, Any]]:
        """
        Executes compensation in reverse order (LIFO) for all recorded steps.
        Returns a list of compensation outcomes.
        """
        steps = self._compensation_journal.get(workflow_id, [])
        results: List[Dict[str, Any]] = []

        # Reverse order execution (N to 1)
        for step in reversed(steps):
            if not step.compensating_handler:
                if self.strict_mode:
                    raise MissingCompensationPathError(
                        f"Step '{step.node_id}' failed and has no registered compensating action.",
                        workflow_id=workflow_id,
                    )
                logger.warning(
                    f"Workflow {workflow_id}: Step '{step.node_id}' has no compensating handler. Skipping."
                )
                continue

            handler = handler_resolver(step.compensating_handler)
            if not handler:
                raise WorkflowException(
                    f"Compensating handler '{step.compensating_handler}' could not be resolved.",
                    workflow_id=workflow_id,
                )

            logger.info(
                f"Workflow {workflow_id}: Executing compensation '{step.compensating_handler}' for node '{step.node_id}'"
            )
            try:
                outcome = await handler({"input": step.input_data, "output": step.output_data})
                results.append({"node_id": step.node_id, "status": "COMPENSATED", "result": outcome})
            except Exception as ex:
                logger.error(
                    f"Workflow {workflow_id}: Compensation for node '{step.node_id}' failed: {ex}"
                )
                results.append({"node_id": step.node_id, "status": "FAILED", "error": str(ex)})
                raise

        # Clean journal after successful compensation
        self._compensation_journal.pop(workflow_id, None)
        return results
