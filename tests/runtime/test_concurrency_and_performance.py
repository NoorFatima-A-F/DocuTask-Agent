"""
Concurrency, Throughput & Stress Test Suite for Platform Runtime.
Validates:
- High-concurrency IoC container resolutions across threads/coroutines
- High-throughput parallel session spawning and tree tracking
- High-load scheduler dispatch across multiple concurrent worker nodes
- Multi-threaded lease contention in leader election
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
import pytest
from app.agents.runtime.dependency_container import DependencyContainer
from app.agents.runtime.enterprise.distributed_scheduler import DistributedScheduler
from app.agents.runtime.enterprise.leader_election import LeaderElectionCoordinator
from app.agents.runtime.enterprise.scheduler_state import JobPriority, ScheduledJob
from app.agents.runtime.runtime_session import RuntimeSession


class HeavyService:
    def __init__(self) -> None:
        self.instance_id = uuid4()


@pytest.mark.asyncio
async def test_concurrent_container_resolutions():
    container = DependencyContainer()
    container.register_singleton(HeavyService, HeavyService)

    async def resolve_task():
        await asyncio.sleep(0.001)
        return container.resolve(HeavyService)

    results = await asyncio.gather(*[resolve_task() for _ in range(100)])
    first = results[0]
    assert len(results) == 100
    assert all(r is first for r in results)


@pytest.mark.asyncio
async def test_concurrent_session_spawning():
    root = RuntimeSession()

    async def spawn_child(idx: int):
        child = root.spawn_child_session(agent_id=f"agent-{idx}", execution_id=f"exec-{idx}")
        await asyncio.sleep(0.001)
        return child.close(status="COMPLETED")

    children = await asyncio.gather(*[spawn_child(i) for i in range(50)])
    assert len(children) == 50
    assert len({c.session_id for c in children}) == 50
    assert all(c.parent_session_id == root.session_id for c in children)
    assert all(c.status == "COMPLETED" for c in children)


@pytest.mark.asyncio
async def test_high_throughput_scheduler_dispatch():
    scheduler = DistributedScheduler()

    # Enqueue 150 jobs with mixed priorities
    for i in range(150):
        pri = JobPriority.CRITICAL if i % 3 == 0 else JobPriority.NORMAL
        scheduler.submit_job(ScheduledJob(name=f"job-{i}", priority=pri))

    dispatched = []
    workers = [f"worker-{w}" for w in range(5)]

    async def worker_loop(worker_id: str):
        count = 0
        while True:
            job = scheduler.poll_next_job(worker_id)
            if not job:
                break
            count += 1
            scheduler.complete_job(job.job_id)
            await asyncio.sleep(0.0001)
        return count

    worker_counts = await asyncio.gather(*[worker_loop(w) for w in workers])
    total_processed = sum(worker_counts)

    assert total_processed == 150
    assert len(scheduler.list_jobs()) == 150


def test_multithreaded_leader_contention():
    coord = LeaderElectionCoordinator(lease_duration_seconds=1.0)
    winners = []

    def try_acquire(node_id: str):
        if coord.try_acquire_leadership(node_id):
            winners.append(node_id)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(try_acquire, f"node-{i}") for i in range(20)]
        for f in futures:
            f.result()

    # Exactly one node must have won the initial acquisition
    assert len(winners) == 1
    assert coord.get_leader() == winners[0]
