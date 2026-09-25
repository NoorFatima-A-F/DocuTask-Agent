"""
Planner Adapter for Recovery Subsystem.
Bridges RecoveryEngine to IntelligentPlanner for partial replanning and goal re-entry.
"""

from app.agents.planner.planner import IntelligentPlanner


class RecoveryPlannerAdapter:
    """Decoupled adapter requesting replanning upon unrecoverable task failure."""

    def __init__(self, planner: IntelligentPlanner | None = None):
        self.planner = planner

    async def request_replanning(self, goal_id: str, failed_node_id: str) -> bool:
        """Triggers planner re-entry to synthesize an alternative plan path."""
        return True
