"""
Workflow Memory Adapter.
Bridges Workflow Runtime with the Memory Foundation (app.agents.memory).
Persists and retrieves cross-workflow long-term semantic context, execution summaries, and artifacts.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID


class WorkflowMemoryAdapter:
    """Adapter storing and retrieving workflow state and summaries from persistent memory."""

    def __init__(self, memory_foundation: Optional[Any] = None) -> None:
        self._memory = memory_foundation

    async def store_workflow_summary(
        self,
        workflow_id: UUID,
        summary: Dict[str, Any],
    ) -> None:
        """Stores a workflow execution summary in semantic memory."""
        if self._memory and hasattr(self._memory, "store"):
            await self._memory.store(f"workflow_summary:{workflow_id}", summary)

    async def retrieve_workflow_context(
        self,
        workflow_id: UUID,
    ) -> Dict[str, Any]:
        """Retrieves past execution context or checkpoints from memory."""
        if self._memory and hasattr(self._memory, "retrieve"):
            data = await self._memory.retrieve(f"workflow_summary:{workflow_id}")
            return data if isinstance(data, dict) else {}
        return {}
