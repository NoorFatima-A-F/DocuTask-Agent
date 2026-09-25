"""
Coordination Memory Adapter.
Queries and stores episodic coordination records and shared memory references in the Memory Subsystem.
"""

from typing import Any, Dict, List, Optional


class CoordinationMemoryAdapter:
    """Adapter bridging coordination sessions to long-term memory."""

    def __init__(self, memory_manager: Optional[Any] = None):
        self._memory_manager = memory_manager

    async def retrieve_relevant_episodes(self, query: str) -> List[Dict[str, Any]]:
        """Retrieves prior multi-agent collaboration episodes from Memory."""
        if self._memory_manager and hasattr(self._memory_manager, "query"):
            return await self._memory_manager.query(query)
        return []
