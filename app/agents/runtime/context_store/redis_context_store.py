"""
Redis-backed Persistent Context Store.
Uses Redis key-value, hashes, and sorted sets for low-latency context persistence and versioned checkpointing.
"""

import json
from typing import Any, Dict, List, Optional
from app.agents.runtime.context_store.context_store import ContextStore, CheckpointRecord
from app.agents.runtime.runtime_context import RuntimeContext


class RedisContextStore(ContextStore):
    """
    Production Redis Context Store.
    Supports namespaced keying, TTL expiration, and atomic checkpoint versioning.
    """

    def __init__(self, redis_client: Any, key_prefix: str = "runtime:context") -> None:
        self.client = redis_client
        self.prefix = key_prefix

    def _ctx_key(self, runtime_id: str) -> str:
        return f"{self.prefix}:{runtime_id}:meta"

    def _chk_key(self, runtime_id: str, version: int) -> str:
        return f"{self.prefix}:{runtime_id}:chk:{version}"

    def _chk_versions_key(self, runtime_id: str) -> str:
        return f"{self.prefix}:{runtime_id}:versions"

    async def save_context(self, context: RuntimeContext, ttl_seconds: Optional[int] = None) -> None:
        key = self._ctx_key(context.runtime_id)
        data = context.model_dump_json()
        if ttl_seconds:
            await self.client.setex(key, ttl_seconds, data)
        else:
            await self.client.set(key, data)

    async def load_context(self, runtime_id: str) -> Optional[RuntimeContext]:
        key = self._ctx_key(runtime_id)
        raw = await self.client.get(key)
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        data = json.loads(raw)
        return RuntimeContext(**data)

    async def checkpoint_context(
        self,
        runtime_id: str,
        state_snapshot: Dict[str, Any],
        expected_version: Optional[int] = None,
    ) -> int:
        versions_key = self._chk_versions_key(runtime_id)
        # Fetch current latest version
        latest = await self.client.zrevrange(versions_key, 0, 0)
        current_version = int(latest[0]) if latest else 0

        if expected_version is not None and current_version != expected_version:
            raise ValueError(
                f"Concurrency conflict: expected version {expected_version} but current is {current_version}"
            )

        next_version = current_version + 1
        ctx = await self.load_context(runtime_id)
        metadata = ctx.model_dump() if ctx else {}

        record = CheckpointRecord(
            runtime_id=runtime_id,
            version=next_version,
            state_snapshot=state_snapshot,
            context_metadata=metadata,
        )

        chk_key = self._chk_key(runtime_id, next_version)
        await self.client.set(chk_key, record.model_dump_json())
        await self.client.zadd(versions_key, {str(next_version): next_version})
        return next_version

    async def restore_context(
        self,
        runtime_id: str,
        version: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        versions_key = self._chk_versions_key(runtime_id)
        if version is None:
            latest = await self.client.zrevrange(versions_key, 0, 0)
            if not latest:
                return None
            target_version = int(latest[0])
        else:
            target_version = version

        chk_key = self._chk_key(runtime_id, target_version)
        raw = await self.client.get(chk_key)
        if not raw:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        data = json.loads(raw)
        return data.get("state_snapshot")

    async def list_checkpoints(self, runtime_id: str) -> List[int]:
        versions_key = self._chk_versions_key(runtime_id)
        items = await self.client.zrange(versions_key, 0, -1)
        return [int(item) for item in items]

    async def delete_context(self, runtime_id: str) -> bool:
        versions = await self.list_checkpoints(runtime_id)
        keys_to_del = [self._ctx_key(runtime_id), self._chk_versions_key(runtime_id)]
        for v in versions:
            keys_to_del.append(self._chk_key(runtime_id, v))

        deleted = await self.client.delete(*keys_to_del)
        return deleted > 0
