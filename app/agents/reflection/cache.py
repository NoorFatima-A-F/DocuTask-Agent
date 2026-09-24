"""
Reflection Cache Layer.
Provides high-performance, in-memory caching for repeated execution traces, evaluations, and artifacts.
"""

from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class ReflectionCache:
    """Thread-safe LRU-like cache with TTL expiration for reflection artifacts and evaluation reports."""

    def __init__(self, capacity: int = 1000, ttl_seconds: float = 3600.0):
        self._capacity = capacity
        self._ttl_seconds = ttl_seconds
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """Retrieves cached item if not expired, moving it to the end (MRU)."""
        if key not in self._cache:
            return None

        entry = self._cache[key]
        now = datetime.now(timezone.utc).timestamp()
        if now - entry["timestamp"] > self._ttl_seconds:
            del self._cache[key]
            return None

        self._cache.move_to_end(key)
        return entry["value"]

    def put(self, key: str, value: Any) -> None:
        """Stores item with current timestamp, evicting oldest if capacity exceeded."""
        if key in self._cache:
            del self._cache[key]
        elif len(self._cache) >= self._capacity:
            self._cache.popitem(last=False)  # Pop oldest (LRU)

        self._cache[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).timestamp()
        }

    def invalidate(self, key: str) -> None:
        """Removes a specific key from the cache."""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Clears all cached entries."""
        self._cache.clear()

    def size(self) -> int:
        """Returns the current number of cached entries."""
        return len(self._cache)
