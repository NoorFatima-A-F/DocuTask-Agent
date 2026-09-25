"""
Distributed Execution Orchestrator.
Orchestrates multi-plan and distributed worker workflow execution.
"""

from typing import List, Optional
from app.agents.execution.context import ExecutionRequest, ExecutionResult
from app.agents.execution.engine import ExecutionEngine


class DistributedExecutionOrchestrator:
    """Orchestrates distributed execution across multiple plan graphs and clusters."""

    def __init__(self, engine: Optional[ExecutionEngine] = None):
        self.engine = engine or ExecutionEngine()

    async def orchestrate(self, requests: List[ExecutionRequest]) -> List[ExecutionResult]:
        results = []
        for req in requests:
            res = await self.engine.execute(req)
            results.append(res)
        return results
