"""
Execution Memory Sub-Tier.
Stores step execution outputs, job status logs, and task outputs.
"""

from typing import Any, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class ExecutionMemory:
    """Execution Memory Tier for task execution outputs."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="ExecutionMemoryProvider")

    async def record_output(self, task_id: str, output: Any) -> None:
        item = MemoryItem(key=f"exec:{task_id}", value=output)
        await self.provider.put(item)
