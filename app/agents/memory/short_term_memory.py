"""
Short-Term Memory Sub-Tier.
Manages session-scoped memory records with automatic TTL expiration.
"""

from typing import Any, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class ShortTermMemory:
    """Short-Term Memory Tier for session-bounded transient observations."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="ShortTermMemoryProvider")

    async def store(self, key: str, value: Any) -> None:
        item = MemoryItem(key=key, value=value)
        await self.provider.put(item)

    async def retrieve(self, key: str) -> Optional[Any]:
        item = await self.provider.get(key)
        if item and not item.is_expired():
            return item.value
        return None
