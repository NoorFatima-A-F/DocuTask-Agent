"""Tier 1: Short-Term Memory (Scratchpad).

Provides fast, in-memory volatile storage for intermediate calculation variables,
step payloads, raw OCR tokens, and transient execution scratchpads.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ScratchpadEntry:
    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    ttl_seconds: Optional[float] = None

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self.ttl_seconds is None:
            return False
        current = now or time.time()
        return (current - self.created_at) > self.ttl_seconds


class ShortTermMemory:
    """Ephemeral scratchpad for current execution steps."""

    def __init__(self, max_entries: int = 1000) -> None:
        self.max_entries = max_entries
        self._store: Dict[str, ScratchpadEntry] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        if len(self._store) >= self.max_entries:
            self._evict_oldest()
        self._store[key] = ScratchpadEntry(key=key, value=value, ttl_seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.is_expired():
            del self._store[key]
            return None
        return entry.value

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self) -> None:
        self._store.clear()

    def list_keys(self) -> List[str]:
        now = time.time()
        return [k for k, v in self._store.items() if not v.is_expired(now)]

    def _evict_oldest(self) -> None:
        if not self._store:
            return
        oldest_key = min(self._store.keys(), key=lambda k: self._store[k].created_at)
        del self._store[oldest_key]
