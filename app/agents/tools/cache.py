"""
Tool Cache Subsystem.
Provides caching for capability resolution queries, provider metadata, and tool selection results.
Future-compatible with Redis / Cloud MemoryStore.
"""

from typing import Any, Dict, Optional


class ToolCache:
    """In-memory cache for tool resolution and selection results."""

    def __init__(self):
        self._store: Dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached item by key."""
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        """Stores item in cache."""
        self._store[key] = value

    def clear(self) -> None:
        """Flushes all cached entries."""
        self._store.clear()
