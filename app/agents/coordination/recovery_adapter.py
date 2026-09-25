"""
Coordination Recovery Adapter.
Delegates failed agent recovery and self-healing to the Autonomous Recovery Engine.
"""

from typing import Any, Optional
from uuid import UUID


class CoordinationRecoveryAdapter:
    """Adapter invoking Recovery Engine when an agent fails or hangs."""

    def __init__(self, recovery_engine: Optional[Any] = None):
        self._recovery_engine = recovery_engine

    async def report_agent_failure(self, agent_id: UUID, error: str) -> bool:
        """Notifies Recovery Engine of an agent-level failure."""
        if self._recovery_engine and hasattr(self._recovery_engine, "recover"):
            await self._recovery_engine.recover(error)
            return True
        return True
