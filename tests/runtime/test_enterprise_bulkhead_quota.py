"""
Enterprise Bulkhead Isolation & Tenant Quota Test Suite.
Validates:
- Bulkhead concurrency bounds and isolation
- Bulkhead queue saturation and BulkheadCapacityExceededError rejection
- Tenant QuotaManager token limits and rate enforcement
- TenantIsolationViolationError on quota breach
- Usage reset
"""

import asyncio
import pytest
from app.agents.runtime.enterprise.quota_manager import QuotaManager, TenantQuota
from app.agents.runtime.enterprise.resource_isolation import (
    Bulkhead,
    BulkheadCapacityExceededError,
)
from app.agents.runtime.exceptions import TenantIsolationViolationError


@pytest.mark.asyncio
async def test_bulkhead_concurrency_bounding():
    # Max 2 concurrent tasks
    bulkhead = Bulkhead("agent_tools", max_concurrent=2, max_queue=5)

    concurrent_peaks = []
    active = 0

    async def worker():
        nonlocal active
        active += 1
        concurrent_peaks.append(active)
        await asyncio.sleep(0.05)
        active -= 1
        return "done"

    tasks = [bulkhead.execute(worker) for _ in range(4)]
    results = await asyncio.gather(*tasks)

    assert len(results) == 4
    assert all(r == "done" for r in results)
    assert max(concurrent_peaks) <= 2
    assert bulkhead.active_count == 0


@pytest.mark.asyncio
async def test_bulkhead_queue_saturation_rejects():
    # Concurrency 1, queue 1 -> 3rd simultaneous task should be rejected
    bulkhead = Bulkhead("constrained_service", max_concurrent=1, max_queue=1)

    blocker = asyncio.Event()

    async def blocking_task():
        await blocker.wait()

    # Slot 1: active task
    t1 = asyncio.create_task(bulkhead.execute(blocking_task))
    await asyncio.sleep(0.01)

    # Slot 2: waiting in queue
    t2 = asyncio.create_task(bulkhead.execute(blocking_task))
    await asyncio.sleep(0.01)

    # Slot 3: exceeds max_queue of 1 -> rejected
    with pytest.raises(BulkheadCapacityExceededError) as exc_info:
        await bulkhead.execute(blocking_task)
    assert "queue is full" in str(exc_info.value)

    # Unblock
    blocker.set()
    await asyncio.gather(t1, t2)


def test_tenant_quota_enforcement():
    qm = QuotaManager()
    qm.set_quota(
        "tenant_finance",
        TenantQuota(max_tokens_per_minute=5000),
    )

    # Consume 3000 tokens -> OK
    assert qm.consume_tokens("tenant_finance", 3000)
    quota = qm.get_quota("tenant_finance")
    assert quota.tokens_consumed == 3000

    # Consume 1500 tokens -> OK (total 4500)
    assert qm.consume_tokens("tenant_finance", 1500)
    assert quota.tokens_consumed == 4500

    # Consume 1000 tokens -> exceeds 5000 -> raises TenantIsolationViolationError
    with pytest.raises(TenantIsolationViolationError) as exc_info:
        qm.consume_tokens("tenant_finance", 1000)
    assert "exceeded token quota" in str(exc_info.value)

    # Reset usage
    qm.reset_usage("tenant_finance")
    assert quota.tokens_consumed == 0
    assert qm.consume_tokens("tenant_finance", 1000)
