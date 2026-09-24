"""
Execution Runtime Coordinator.
Wires engine, cancellation, pause/resume, and progress monitoring.
"""

from typing import Optional
from app.agents.execution.context import ExecutionRequest, ExecutionResult
from app.agents.execution.engine import ExecutionEngine


class ExecutionRuntime:
    """Runtime coordinator supervising execution engine lifecycles."""

    def __init__(self, engine: Optional[ExecutionEngine] = None):
        self.engine = engine or ExecutionEngine()

    async def run(self, request: ExecutionRequest) -> ExecutionResult:
        return await self.engine.execute(request)
