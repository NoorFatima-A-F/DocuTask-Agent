"""
Planning Engine Coordinator.
"""

from typing import Optional
from app.agents.planner.context import PlannerRequest
from app.agents.planner.pipeline import PlanningPipeline
from app.agents.planning.contracts import Plan


class PlanningEngine:
    """Core coordination engine for plan synthesis."""

    def __init__(self, pipeline: Optional[PlanningPipeline] = None):
        self.pipeline = pipeline or PlanningPipeline()

    async def generate_plan(self, request: PlannerRequest) -> Plan:
        return await self.pipeline.execute_pipeline(request)
