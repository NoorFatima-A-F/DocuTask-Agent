"""
Runtime Cache.
Bounded LRU and TTL memory cache for fast runtime metadata, tenant queries, and module lookups.
"""

import time
from collections import OrderedDict
from typing import Any, Optional, Tuple


class RuntimeCache:
    """Thread-safe LRU and TTL cache for platform runtime entities."""

    def __init__(self, capacity: int = 1000, default_ttl_seconds: float = 3600.0) -> None:
        self.capacity = capacity
        self.default_ttl = default_ttl_seconds
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """Retrieves item if present and unexpired; marks as MRU."""
        if key not in self._cache:
            return None
        val, expires_at = self._cache[key]
        if time.time() > expires_at:
            del self._cache[key]
            return None
        self._cache.move_to_end(key)
        return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        """Stores item with expiration, evicting oldest item if capacity is reached."""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expires_at = time.time() + ttl
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = (value, expires_at)
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)

    def evict(self, key: str) -> bool:
        """Removes a key from cache."""
        return bool(self._cache.pop(key, None))

    def clear(self) -> None:
        """Clears all cached entries."""
        self._cache.clear()

    def size(self) -> int:
        """Current number of cached entries."""
        return len(self._cache)
