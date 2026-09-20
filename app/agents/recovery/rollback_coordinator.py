"""
Rollback Coordinator.
Coordinates node, subtree, and workflow rollbacks with the Execution subsystem.
"""

from typing import List
from uuid import UUID
from app.agents.recovery.compensation import CompensatingAction, CompensationEngine


class RollbackCoordinator:
    """Coordinates compensation actions and orders reverse topological rollback."""

    def __init__(self, compensation_engine: CompensationEngine | None = None):
        self.compensation_engine = compensation_engine or CompensationEngine()

    def coordinate_rollback_plan(self, completed_nodes: List[str]) -> List[CompensatingAction]:
        """Plans compensating actions in reverse topological order."""
        actions = []
        for nid in reversed(completed_nodes):
            action = self.compensation_engine.plan_compensation(nid, "TASK")
            actions.append(action)
        return actions
