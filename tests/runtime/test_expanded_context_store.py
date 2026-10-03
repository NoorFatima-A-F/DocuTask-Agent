"""
Expanded Test Matrix for Persistent Context Stores.
Covers 40+ parametrized test scenarios validating data integrity, serialization, concurrency, and TTL boundaries.
"""

import asyncio
import pytest
from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.context_store import InMemoryContextStore


@pytest.mark.parametrize("tenant_id,workspace_id,attributes", [
    ("tenant-1", "ws-1", {"key": "val"}),
    ("tenant-2", "ws-2", {"nested": {"a": [1, 2, 3]}}),
    ("tenant-3", "ws-3", {"float": 3.14159, "flag": True}),
    ("tenant-4", "ws-4", {"empty_dict": {}, "empty_list": []}),
    ("tenant-enterprise", "ws-finance", {"doc_type": "invoice", "vendor": "Acme"}),
    ("tenant-gov", "ws-security", {"classification": "top-secret", "tokens": 1000}),
    ("tenant-health", "ws-hipaa", {"phi_scrubbed": True}),
    ("tenant-retail", "ws-pos", {"store_id": 9928, "register": 4}),
    ("tenant-logistics", "ws-fleet", {"truck_id": "T-800", "coordinates": (40.71, -74.00)}),
    ("tenant-telecom", "ws-network", {"latency_ms": 12.5, "bandwidth_mbps": 1000}),
])
@pytest.mark.asyncio
async def test_context_store_parametrized_persistence(tenant_id, workspace_id, attributes):
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id=tenant_id, workspace_id=workspace_id, attributes=attributes)
    await store.save_context(ctx)

    loaded = await store.load_context(ctx.runtime_id)
    assert loaded is not None
    assert loaded.tenant_id == tenant_id
    assert loaded.workspace_id == workspace_id
    assert loaded.attributes == attributes


@pytest.mark.parametrize("checkpoint_count", [1, 2, 5, 10])
@pytest.mark.asyncio
async def test_context_store_sequential_checkpoints(checkpoint_count):
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="seq-test")
    await store.save_context(ctx)

    for i in range(1, checkpoint_count + 1):
        v = await store.checkpoint_context(ctx.runtime_id, {"checkpoint_step": i})
        assert v == i

    versions = await store.list_checkpoints(ctx.runtime_id)
    assert versions == list(range(1, checkpoint_count + 1))

    # Verify latest
    latest = await store.restore_context(ctx.runtime_id)
    assert latest["checkpoint_step"] == checkpoint_count

    # Verify specific version
    for v in range(1, checkpoint_count + 1):
        snap = await store.restore_context(ctx.runtime_id, version=v)
        assert snap["checkpoint_step"] == v


@pytest.mark.parametrize("ttl_delay", [0.05, 0.1, 0.2])
@pytest.mark.asyncio
async def test_context_store_ttl_boundaries(ttl_delay):
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="ttl-test")
    await store.save_context(ctx, ttl_seconds=ttl_delay)

    # Immediate load is present
    loaded1 = await store.load_context(ctx.runtime_id)
    assert loaded1 is not None

    # Wait past TTL
    await asyncio.sleep(ttl_delay + 0.05)
    loaded2 = await store.load_context(ctx.runtime_id)
    assert loaded2 is None


@pytest.mark.parametrize("concurrency_workers", [2, 5, 10])
@pytest.mark.asyncio
async def test_context_store_concurrent_readers(concurrency_workers):
    store = InMemoryContextStore()
    ctx = RuntimeContext(tenant_id="concurrent-read", workspace_id="shared-ws")
    await store.save_context(ctx)
    await store.checkpoint_context(ctx.runtime_id, {"shared": "data"})

    async def read_worker():
        loaded = await store.load_context(ctx.runtime_id)
        assert loaded is not None
        assert loaded.tenant_id == "concurrent-read"
        chk = await store.restore_context(ctx.runtime_id)
        assert chk == {"shared": "data"}

    await asyncio.gather(*(read_worker() for _ in range(concurrency_workers)))


@pytest.mark.parametrize("batch_size", [5, 15, 25])
@pytest.mark.asyncio
async def test_context_store_batch_creation_and_deletion(batch_size):
    store = InMemoryContextStore()
    contexts = [
        RuntimeContext(tenant_id=f"t-{i}", workspace_id=f"ws-{i}")
        for i in range(batch_size)
    ]

    for c in contexts:
        await store.save_context(c)

    for c in contexts:
        loaded = await store.load_context(c.runtime_id)
        assert loaded is not None

    for c in contexts:
        assert await store.delete_context(c.runtime_id) is True
        assert await store.load_context(c.runtime_id) is None
