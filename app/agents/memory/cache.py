"""
Memory Cache Subsystem.
In-memory cache for memory item queries.
"""

from typing import Dict, Optional
from app.agents.memory.repository import MemoryItem


class MemoryCache:
    """In-memory cache for fast memory retrieval."""

    def __init__(self):
        self._cache: Dict[str, MemoryItem] = {}

    def get(self, key: str) -> Optional[MemoryItem]:
        return self._cache.get(key)

    def set(self, key: str, item: MemoryItem) -> None:
        self._cache[key] = item

    def clear(self) -> None:
        self._cache.clear()
