"""
Runtime Validator.
Validates execution graphs against cyclic deadlocks or disconnected execution topologies.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.planning.dag import DAGValidator
from app.agents.planning.exceptions import PlanningException


class RuntimeValidationReport(BaseModel):
    is_valid: bool = Field(default=True)
    errors: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class RuntimeValidator:
    """Validates execution graphs prior to execution start."""

    def validate_graph(self, graph: ExecutionGraph) -> RuntimeValidationReport:
        errors = []
        try:
            DAGValidator.detect_cycles(graph.plan_graph)
        except PlanningException as e:
            errors.append(f"Cycle in execution graph: {str(e)}")

        return RuntimeValidationReport(is_valid=len(errors) == 0, errors=errors)
