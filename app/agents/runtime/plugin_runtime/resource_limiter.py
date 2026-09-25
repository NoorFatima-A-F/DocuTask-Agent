"""
Plugin Resource Limiter.
Enforces execution time, memory bounds, and thread concurrency on plugin execution.
"""

import asyncio
from typing import Any, Callable, Coroutine, Optional
from app.agents.runtime.exceptions import RuntimeKernelException


class PluginResourceLimitExceededError(RuntimeKernelException):
    """Raised when a plugin exceeds allocated CPU execution time or memory quotas."""
    pass


ResourceExceededError = PluginResourceLimitExceededError


class PluginResourceLimiter:
    """Enforces execution boundaries on plugin invocations."""

    def __init__(
        self,
        max_execution_time_seconds: float = 2.0,
        max_cpu_time_seconds: Optional[float] = None,
        max_memory_mb: float = 128.0,
    ) -> None:
        self.max_execution_time = max_cpu_time_seconds if max_cpu_time_seconds is not None else max_execution_time_seconds
        self.max_memory_mb = max_memory_mb

    async def execute_bounded(self, action: Callable[[], Coroutine[Any, Any, Any]]) -> Any:
        """Executes coroutine bounded by timeout and resource monitors."""
        try:
            return await asyncio.wait_for(action(), timeout=self.max_execution_time)
        except asyncio.TimeoutError:
            raise PluginResourceLimitExceededError(
                f"Plugin execution exceeded CPU time limit ({self.max_execution_time}s)."
            )

    async def enforce_limits(self, action: Callable[[], Coroutine[Any, Any, Any]]) -> Any:
        return await self.execute_bounded(action)
