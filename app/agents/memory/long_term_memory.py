"""
Long-Term Memory Sub-Tier.
Manages persistent, high-importance memory records retained across execution sessions.
"""

from typing import Any, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class LongTermMemory:
    """Long-Term Memory Tier for cross-session persistent records."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="LongTermMemoryProvider")

    async def store(self, key: str, value: Any) -> None:
        item = MemoryItem(key=key, value=value)
        await self.provider.put(item)

    async def retrieve(self, key: str) -> Optional[Any]:
        item = await self.provider.get(key)
        return item.value if item else None
