"""
Execution Manager.
"""

from typing import Optional
from app.agents.execution.context import ExecutionRequest, ExecutionResult
from app.agents.execution.engine import ExecutionEngine


class ExecutionManager:
    """Manager providing lifecycle management for stateful executions."""

    def __init__(self, engine: Optional[ExecutionEngine] = None):
        self.engine = engine or ExecutionEngine()

    async def start_execution(self, request: ExecutionRequest) -> ExecutionResult:
        return await self.engine.execute(request)
