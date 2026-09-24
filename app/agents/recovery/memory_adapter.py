"""
Memory Adapter for Recovery Subsystem.
Queries MemoryManager for historical remediation patterns and past incident solutions.
"""

from typing import Any, Dict, List
from app.agents.memory.manager import MemoryManager


class RecoveryMemoryAdapter:
    """Read-only adapter retrieving historical failure resolutions from memory."""

    def __init__(self, memory_manager: MemoryManager | None = None):
        self.memory_manager = memory_manager

    async def get_historical_remediations(self, failure_type: str) -> List[Dict[str, Any]]:
        if not self.memory_manager:
            return []
        items = await self.memory_manager.search(failure_type, top_k=3)
        return [{"key": item.key, "value": item.value} for item in items]
