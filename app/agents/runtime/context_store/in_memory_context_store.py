"""
In-Memory Persistent Context Store.
Thread-safe and async-safe implementation with snapshot history and TTL eviction.
"""

import asyncio
import copy
import time
from typing import Any, Dict, List, Optional
from app.agents.runtime.context_store.context_store import ContextStore, CheckpointRecord
from app.agents.runtime.runtime_context import RuntimeContext


class InMemoryContextStore(ContextStore):
    """In-memory reference context store with full versioned history and TTL support."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._contexts: Dict[str, RuntimeContext] = {}
        self._context_expirations: Dict[str, float] = {}
        # runtime_id -> {version: CheckpointRecord}
        self._checkpoints: Dict[str, Dict[int, CheckpointRecord]] = {}

    async def save_context(self, context: RuntimeContext, ttl_seconds: Optional[int] = None) -> None:
        async with self._lock:
            self._contexts[context.runtime_id] = context
            if ttl_seconds is not None:
                self._context_expirations[context.runtime_id] = time.time() + ttl_seconds
            elif context.runtime_id in self._context_expirations:
                del self._context_expirations[context.runtime_id]

    async def load_context(self, runtime_id: str) -> Optional[RuntimeContext]:
        async with self._lock:
            if runtime_id not in self._contexts:
                return None
            if runtime_id in self._context_expirations:
                if time.time() > self._context_expirations[runtime_id]:
                    # Expired
                    del self._contexts[runtime_id]
                    del self._context_expirations[runtime_id]
                    self._checkpoints.pop(runtime_id, None)
                    return None
            return self._contexts.get(runtime_id)

    async def checkpoint_context(
        self,
        runtime_id: str,
        state_snapshot: Dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> int:
        async with self._lock:
            if runtime_id not in self._checkpoints:
                self._checkpoints[runtime_id] = {}

            history = self._checkpoints[runtime_id]
            current_version = max(history.keys(), default=0)

            if expected_version is not None and current_version != expected_version:
                raise ValueError(
                    f"Concurrency conflict: expected version {expected_version} but current is {current_version}"
                )

            next_version = current_version + 1
            ctx = self._contexts.get(runtime_id)
            metadata = ctx.model_dump() if ctx else {}

            record = CheckpointRecord(
                runtime_id=runtime_id,
                version=next_version,
                state_snapshot=copy.deepcopy(state_snapshot),
                context_metadata=metadata,
            )
            history[next_version] = record
            return next_version

    async def restore_context(
        self,
        runtime_id: str,
        version: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        async with self._lock:
            history = self._checkpoints.get(runtime_id)
            if not history:
                return None

            if version is None:
                version = max(history.keys())

            record = history.get(version)
            if not record:
                return None
            return copy.deepcopy(record.state_snapshot)

    async def list_checkpoints(self, runtime_id: str) -> List[int]:
        async with self._lock:
            history = self._checkpoints.get(runtime_id, {})
            return sorted(history.keys())

    async def delete_context(self, runtime_id: str) -> bool:
        async with self._lock:
            existed = runtime_id in self._contexts or runtime_id in self._checkpoints
            self._contexts.pop(runtime_id, None)
            self._context_expirations.pop(runtime_id, None)
            self._checkpoints.pop(runtime_id, None)
            return existed
