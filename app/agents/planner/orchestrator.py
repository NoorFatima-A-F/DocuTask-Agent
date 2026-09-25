"""
Planning Orchestrator Subsystem.
"""

from typing import Optional
from app.agents.planner.context import PlannerRequest
from app.agents.planner.engine import PlanningEngine
from app.agents.planning.contracts import Plan


class PlanningOrchestrator:
    """Orchestrates end-to-end planning workflows across multiple goals."""

    def __init__(self, engine: Optional[PlanningEngine] = None):
        self.engine = engine or PlanningEngine()

    async def orchestrate_plan(self, request: PlannerRequest) -> Plan:
        return await self.engine.generate_plan(request)
