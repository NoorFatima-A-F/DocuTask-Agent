"""
Working Memory Sub-Tier.
Manages immediate active state, variables, and transient context for running agent tasks.
"""

from typing import Any, Dict, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class WorkingMemory:
    """Working Memory Tier handling active in-flight execution state."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="WorkingMemoryProvider")

    async def set_variable(self, key: str, value: Any) -> None:
        item = MemoryItem(key=key, value=value)
        await self.provider.put(item)

    async def get_variable(self, key: str) -> Optional[Any]:
        item = await self.provider.get(key)
        return item.value if item else None
