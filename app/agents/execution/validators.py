"""
Execution Request and Plan Graph Fail-Fast Validators.
"""

from app.agents.execution.context import ExecutionRequest
from app.agents.execution.exceptions import ExecutionException


class ExecutionRequestValidator:
    """Fail-fast validator for execution requests."""

    @staticmethod
    def validate_request(request: ExecutionRequest) -> None:
        if not request.plan:
            raise ExecutionException("ExecutionRequest must contain a valid Plan.")
        if not request.plan.graph.nodes:
            raise ExecutionException("Cannot execute a Plan with an empty PlanGraph.")
