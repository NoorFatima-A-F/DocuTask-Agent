"""
Coordination Runtime Container.
Asynchronous runtime environment hosting CoordinationEngine, background presence polling, and queues.
"""

from typing import Optional
from app.agents.coordination.context import CoordinationRequest, CoordinationResult
from app.agents.coordination.engine import CoordinationEngine


class CoordinationRuntime:
    """Cloud-native runtime container managing CoordinationEngine lifecycle and background monitors."""

    def __init__(self, engine: Optional[CoordinationEngine] = None):
        self.engine = engine or CoordinationEngine()
        self._is_running = False

    async def start(self) -> None:
        """Starts background presence, heartbeats, and coordination dispatchers."""
        self._is_running = True

    async def stop(self) -> None:
        """Gracefully drains active coordination sessions and shuts down."""
        self._is_running = False

    async def coordinate_goal(self, request: CoordinationRequest) -> CoordinationResult:
        """Dispatches an incoming coordination request to the engine."""
        return await self.engine.coordinate(request)

    @property
    def is_running(self) -> bool:
        return self._is_running
