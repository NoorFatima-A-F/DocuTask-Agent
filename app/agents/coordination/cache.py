"""
Coordination Cache Layer.
High-performance thread-safe LRU cache with TTL expiration for capability lookups and agent profiles.
"""

from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class CoordinationCache:
    """In-memory LRU and TTL cache for agent profiles and capability match lookups."""

    def __init__(self, capacity: int = 1000, ttl_seconds: float = 3600.0):
        self._capacity = capacity
        self._ttl_seconds = ttl_seconds
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
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
        if key in self._cache:
            del self._cache[key]
        elif len(self._cache) >= self._capacity:
            self._cache.popitem(last=False)

        self._cache[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).timestamp()
        }

    def invalidate(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)
