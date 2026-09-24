"""
Unit and Integration Tests for Persistent Runtime Context Stores.
Verifies context persistence, TTL expiration, versioned checkpointing, and concurrency safety.
"""

import asyncio
import pytest
from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.context_store import (
    InMemoryContextStore,
    RedisContextStore,
    PostgresContextStore,
)


@pytest.mark.asyncio
async def test_in_memory_context_store_save_load():
    store = InMemoryContextStore()
    ctx = RuntimeContext(
        tenant_id="tenant-alpha",
        workspace_id="ws-123",
        workflow_id="wf-456",
        attributes={"plan_id": "p-1"}
    )
    await store.save_context(ctx)

    loaded = await store.load_context(ctx.runtime_id)
    assert loaded is not None
    assert loaded.tenant_id == "tenant-alpha"
    assert loaded.workspace_id == "ws-123"
    assert loaded.workflow_id == "wf-456"
    assert loaded.attributes["plan_id"] == "p-1"


@pytest.mark.asyncio
async def test_in_memory_context_store_ttl_expiration():
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="tenant-expiring")
    await store.save_context(ctx, ttl_seconds=1)

    loaded1 = await store.load_context(ctx.runtime_id)
    assert loaded1 is not None

    # Wait for TTL to pass
    await asyncio.sleep(1.05)
    loaded2 = await store.load_context(ctx.runtime_id)
    assert loaded2 is None


@pytest.mark.asyncio
async def test_in_memory_context_store_checkpoint_and_restore():
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="tenant-chk")
    await store.save_context(ctx)

    v1 = await store.checkpoint_context(ctx.runtime_id, {"step": "ocr_completed", "tokens": 150})
    assert v1 == 1

    v2 = await store.checkpoint_context(ctx.runtime_id, {"step": "extraction_completed", "tokens": 300})
    assert v2 == 2

    versions = await store.list_checkpoints(ctx.runtime_id)
    assert versions == [1, 2]

    # Restore latest
    latest_state = await store.restore_context(ctx.runtime_id)
    assert latest_state == {"step": "extraction_completed", "tokens": 300}

    # Restore v1
    v1_state = await store.restore_context(ctx.runtime_id, version=1)
    assert v1_state == {"step": "ocr_completed", "tokens": 150}


@pytest.mark.asyncio
async def test_in_memory_context_store_concurrency_conflict():
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="tenant-conflict")
    await store.save_context(ctx)

    v1 = await store.checkpoint_context(ctx.runtime_id, {"data": 1})
    assert v1 == 1

    # Expecting v0 when current is v1 should raise ValueError
    with pytest.raises(ValueError, match="Concurrency conflict"):
        await store.checkpoint_context(ctx.runtime_id, {"data": 2}, expected_version=0)


@pytest.mark.asyncio
async def test_in_memory_context_store_delete():
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="tenant-del")
    await store.save_context(ctx)
    await store.checkpoint_context(ctx.runtime_id, {"data": "test"})

    deleted = await store.delete_context(ctx.runtime_id)
    assert deleted is True

    assert await store.load_context(ctx.runtime_id) is None
    assert await store.list_checkpoints(ctx.runtime_id) == []


class FakeRedis:
    def __init__(self):
        self.data = {}
        self.zsets = {}

    async def set(self, key, value):
        self.data[key] = value

    async def setex(self, key, seconds, value):
        self.data[key] = value

    async def get(self, key):
        return self.data.get(key)

    async def zadd(self, key, mapping):
        if key not in self.zsets:
            self.zsets[key] = {}
        for member, score in mapping.items():
            self.zsets[key][member] = score

    async def zrange(self, key, start, stop):
        z = self.zsets.get(key, {})
        sorted_members = sorted(z.keys(), key=lambda m: z[m])
        return sorted_members

    async def zrevrange(self, key, start, stop):
        z = self.zsets.get(key, {})
        sorted_members = sorted(z.keys(), key=lambda m: z[m], reverse=True)
        return sorted_members[: stop - start + 1 if stop >= 0 else None]

    async def delete(self, *keys):
        count = 0
        for k in keys:
            if k in self.data:
                del self.data[k]
                count += 1
            if k in self.zsets:
                del self.zsets[k]
                count += 1
        return count


@pytest.mark.asyncio
async def test_redis_context_store():
    fake_redis = FakeRedis()
    store = RedisContextStore(redis_client=fake_redis, key_prefix="test:ctx")
    ctx = RuntimeContext(tenant_id="tenant-redis", workspace_id="ws-redis")
    await store.save_context(ctx)

    loaded = await store.load_context(ctx.runtime_id)
    assert loaded is not None
    assert loaded.tenant_id == "tenant-redis"

    v1 = await store.checkpoint_context(ctx.runtime_id, {"checkpoint": 1})
    assert v1 == 1

    versions = await store.list_checkpoints(ctx.runtime_id)
    assert versions == [1]

    restored = await store.restore_context(ctx.runtime_id)
    assert restored == {"checkpoint": 1}

    deleted = await store.delete_context(ctx.runtime_id)
    assert deleted is True


class FakeSqlDb:
    def __init__(self):
        self.contexts = {}
        self.checkpoints = {}

    async def execute(self, query, params):
        if "INSERT INTO runtime_contexts" in query:
            self.contexts[params["runtime_id"]] = params["context_data"]
        elif "INSERT INTO runtime_checkpoints" in query:
            self.checkpoints[(params["runtime_id"], params["version"])] = (
                params["state_snapshot"],
                params["context_metadata"],
            )
        elif "DELETE FROM runtime_checkpoints" in query:
            r_id = params["runtime_id"]
            self.checkpoints = {k: v for k, v in self.checkpoints.items() if k[0] != r_id}
        elif "DELETE FROM runtime_contexts" in query:
            self.contexts.pop(params["runtime_id"], None)

    async def fetch_one(self, query, params):
        if "SELECT context_data FROM runtime_contexts" in query:
            data = self.contexts.get(params["runtime_id"])
            return (data,) if data else None
        elif "SELECT MAX(version)" in query:
            r_id = params["runtime_id"]
            vers = [k[1] for k in self.checkpoints if k[0] == r_id]
            max_v = max(vers) if vers else None
            return (max_v,)
        elif "SELECT state_snapshot" in query:
            r_id = params["runtime_id"]
            if "AND version = :version" in query:
                ver = params["version"]
                rec = self.checkpoints.get((r_id, ver))
                return (rec[0],) if rec else None
            else:
                vers = [k[1] for k in self.checkpoints if k[0] == r_id]
                if not vers:
                    return None
                max_v = max(vers)
                rec = self.checkpoints.get((r_id, max_v))
                return (rec[0],) if rec else None
        return None

    async def fetch_all(self, query, params):
        if "SELECT version FROM runtime_checkpoints" in query:
            r_id = params["runtime_id"]
            vers = sorted([k[1] for k in self.checkpoints if k[0] == r_id])
            return [(v,) for v in vers]
        return []


@pytest.mark.asyncio
async def test_postgres_context_store():
    fake_db = FakeSqlDb()
    store = PostgresContextStore(db_executor=fake_db)
    ctx = RuntimeContext(tenant_id="tenant-sql", workspace_id="ws-sql")
    await store.save_context(ctx)

    loaded = await store.load_context(ctx.runtime_id)
    assert loaded is not None
    assert loaded.tenant_id == "tenant-sql"

    v1 = await store.checkpoint_context(ctx.runtime_id, {"sql_step": 1})
    assert v1 == 1

    versions = await store.list_checkpoints(ctx.runtime_id)
    assert versions == [1]

    restored = await store.restore_context(ctx.runtime_id)
    assert restored == {"sql_step": 1}

    deleted = await store.delete_context(ctx.runtime_id)
    assert deleted is True
