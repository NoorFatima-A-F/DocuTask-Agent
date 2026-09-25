"""
Memory Persistence Subsystem.
Provides persistence hooks for database and object storage backends.
"""

from typing import List, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class MemoryPersistence:
    """Persistence manager backing up memory stores."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="PersistenceProvider")

    async def save_snapshot(self, items: List[MemoryItem]) -> None:
        for item in items:
            await self.provider.put(item)
