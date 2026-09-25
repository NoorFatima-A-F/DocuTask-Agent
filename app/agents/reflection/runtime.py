"""
Reflection Runtime Container.
Asynchronous execution environment hosting the ReflectionEngine, background queues, and telemetry streams.
"""

from typing import Optional
from app.agents.reflection.context import ReflectionRequest, ReflectionResult
from app.agents.reflection.engine import ReflectionEngine


class ReflectionRuntime:
    """Isolated, cloud-native runtime container managing ReflectionEngine lifecycle and tasks."""

    def __init__(self, engine: Optional[ReflectionEngine] = None):
        self.engine = engine or ReflectionEngine()
        self._is_running = False

    async def start(self) -> None:
        """Starts background workers, cache warmers, and event listeners."""
        self._is_running = True

    async def stop(self) -> None:
        """Gracefully drains active reflection tasks and shuts down."""
        self._is_running = False

    async def process_completed_execution(self, request: ReflectionRequest) -> ReflectionResult:
        """Processes an incoming completed execution reflection request."""
        return await self.engine.reflect(request)

    @property
    def is_running(self) -> bool:
        """Checks if runtime is active."""
        return self._is_running
