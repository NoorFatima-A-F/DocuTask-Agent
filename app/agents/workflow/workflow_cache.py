"""
Workflow Cache.
High-throughput LRU and TTL memory cache for workflow definitions, graph topologies, and instance state lookups.
"""

import time
from collections import OrderedDict
from typing import Any, Optional, Tuple


class WorkflowCache:
    """Bounded LRU and TTL cache for compiled workflow definitions and metadata."""

    def __init__(self, capacity: int = 1000, default_ttl_seconds: float = 3600.0) -> None:
        self.capacity = capacity
        self.default_ttl = default_ttl_seconds
        # maps key -> (value, expire_timestamp)
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """Retrieves item if present and not expired; moves to MRU position."""
        if key not in self._cache:
            return None
        val, expires_at = self._cache[key]
        if time.time() > expires_at:
            del self._cache[key]
            return None
        self._cache.move_to_end(key)
        return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        """Stores item with TTL, evicting oldest item if capacity is exceeded."""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expires_at = time.time() + ttl
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = (value, expires_at)
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def evict(self, key: str) -> bool:
        """Evicts an item from cache."""
        return bool(self._cache.pop(key, None))

    def clear(self) -> None:
        """Clears all cached items."""
        self._cache.clear()

    def size(self) -> int:
        """Current number of items in cache."""
        return len(self._cache)
