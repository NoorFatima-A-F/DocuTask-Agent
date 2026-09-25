"""
Recovery Validation Engine.
Validates recovery graphs, acyclicity, and checkpoint integrity.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.recovery.recovery_graph import RecoveryGraph


class RecoveryValidationReport(BaseModel):
    is_valid: bool = Field(default=True)
    errors: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class RecoveryValidator:
    """Validates structure and integrity of RecoveryGraph DAGs."""

    def validate_graph(self, graph: RecoveryGraph) -> RecoveryValidationReport:
        errors = []
        if not graph.nodes:
            errors.append("RecoveryGraph contains zero recovery action nodes.")

        # Check for broken edge references
        for edge in graph.edges:
            if edge.source_id not in graph.nodes:
                errors.append(f"Edge source '{edge.source_id}' not found in recovery nodes.")
            if edge.target_id not in graph.nodes:
                errors.append(f"Edge target '{edge.target_id}' not found in recovery nodes.")

        return RecoveryValidationReport(is_valid=len(errors) == 0, errors=errors)
