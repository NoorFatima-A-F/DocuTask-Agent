"""
Phase 13.18: Comprehensive Test Suite for Autonomous Cloud Runtime & Distributed Agent Fabric (ACR-DAF)
Tests Distributed Queues, Priority Scheduler, Worker Fleet, Durable Workflows, Distributed Locks,
Autoscaling, Multi-Region Fabric, Model Gateway, Disaster Recovery, and REST APIs.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.runtime.distributed import (
    DistributedQueueChannel,
    QueueManager,
    FairnessAllocator,
    DistributedScheduler,
    WorkerFleetManager,
    ExecutionFabric,
    CheckpointEngine,
    DurableWorkflowEngine,
    DistributedLockManager,
    AutoscalingEngine,
    RegionRouter,
    DistributedCache,
    ModelGateway,
    DisasterRecoveryEngine,
    DistributedRuntime,
    WorkerStatus,
    JobPriority,
    JobState,
    RegionName,
    ScalingAction,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def runtime():
    return DistributedRuntime()


# -----------------------------------------------------------------------------
# 1. Distributed Queue & DLQ Tests
# -----------------------------------------------------------------------------

def test_distributed_queue_priorities_and_dlq():
    channel = DistributedQueueChannel("test_channel")
    from app.runtime.distributed.models.schemas import ScheduledJob

    j_norm = ScheduledJob(workflow_id="wf_1", agent_id="a1", task_name="Norm", priority=JobPriority.NORMAL)
    j_crit = ScheduledJob(workflow_id="wf_2", agent_id="a2", task_name="Crit", priority=JobPriority.CRITICAL)
    j_high = ScheduledJob(workflow_id="wf_3", agent_id="a3", task_name="High", priority=JobPriority.HIGH)
    j_batch = ScheduledJob(workflow_id="wf_4", agent_id="a4", task_name="Batch", priority=JobPriority.BATCH)

    # Enqueue in arbitrary order
    channel.enqueue(j_norm)
    channel.enqueue(j_batch)
    channel.enqueue(j_crit)
    channel.enqueue(j_high)

    # Dequeue should strictly follow priority: CRITICAL -> HIGH -> NORMAL -> BATCH
    d1 = channel.dequeue()
    assert d1 is not None and d1.priority == JobPriority.CRITICAL
    d2 = channel.dequeue()
    assert d2 is not None and d2.priority == JobPriority.HIGH
    d3 = channel.dequeue()
    assert d3 is not None and d3.priority == JobPriority.NORMAL
    d4 = channel.dequeue()
    assert d4 is not None and d4.priority == JobPriority.BATCH

    # DLQ
    channel.send_to_dlq(j_batch, "Max retries exceeded")
    metrics = channel.get_metrics()
    assert metrics["dlq_depth"] == 1
    assert len(channel.list_dlq()) == 1


# -----------------------------------------------------------------------------
# 2. Distributed Scheduler & Fairness Allocator Tests
# -----------------------------------------------------------------------------

def test_fairness_allocator_quotas():
    alloc = FairnessAllocator(tenant_max_concurrent=2)
    assert alloc.can_tenant_execute("tenant_a") is True
    alloc.increment_tenant("tenant_a")
    alloc.increment_tenant("tenant_a")
    assert alloc.can_tenant_execute("tenant_a") is False
    alloc.decrement_tenant("tenant_a")
    assert alloc.can_tenant_execute("tenant_a") is True


def test_distributed_scheduler_submit_and_schedule():
    scheduler = DistributedScheduler()
    job = scheduler.submit_job(
        workflow_id="wf_sched_01",
        agent_id="agent_chief_architect",
        task_name="Refactor DAG",
        priority=JobPriority.CRITICAL,
    )
    assert job.job_id.startswith("job_")
    assert job.priority == JobPriority.CRITICAL

    scheduled = scheduler.schedule_next_job()
    assert scheduled is not None
    assert scheduled.state == JobState.SCHEDULED

    scheduler.complete_job(job.job_id, duration_ms=145.0)
    completed = scheduler.get_job(job.job_id)
    assert completed.state == JobState.COMPLETED
    assert completed.execution_duration_ms == 145.0


# -----------------------------------------------------------------------------
# 3. Worker Fleet Manager & Crash Detection Tests
# -----------------------------------------------------------------------------

def test_worker_fleet_registration_and_heartbeats():
    fleet = WorkerFleetManager()
    node = fleet.register_worker(hostname="worker-test-01.internal", region=RegionName.US_EAST)
    assert node.worker_id.startswith("node_")
    assert node.status == WorkerStatus.ONLINE

    ok = fleet.record_heartbeat(node.worker_id, cpu_pct=35.0, memory_pct=40.0)
    assert ok is True
    assert node.capacity.cpu_utilization_pct == 35.0

    fleet.drain_worker(node.worker_id)
    assert node.status == WorkerStatus.DRAINING


def test_heartbeat_timeout_crash_detection():
    fleet = WorkerFleetManager()
    fleet.heartbeat_timeout_sec = 0  # Force immediate timeout
    crashed = fleet.check_heartbeats()
    assert len(crashed) > 0


# -----------------------------------------------------------------------------
# 4. Load Balancer & Execution Fabric Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_load_balancer_and_fabric_dispatch():
    fleet = WorkerFleetManager()
    fabric = ExecutionFabric(fleet_manager=fleet)

    from app.runtime.distributed.models.schemas import ScheduledJob
    job = ScheduledJob(
        workflow_id="wf_disp_01",
        agent_id="agent_scientist",
        task_name="Run Simulation",
        target_region=RegionName.US_EAST,
    )
    dispatched = await fabric.dispatch_job(job)
    assert dispatched is True
    assert job.assigned_worker_id is not None
    assert job.state == JobState.RUNNING


# -----------------------------------------------------------------------------
# 5. Durable Workflow Engine & Checkpointing Tests
# -----------------------------------------------------------------------------

def test_durable_workflow_lifecycle_and_migration():
    engine = DurableWorkflowEngine()
    wf = engine.create_workflow(title="Autonomous Extraction Pipeline", agent_id="agent_doc_extractor", total_steps=4)
    assert wf.workflow_id.startswith("wf_")

    # Create checkpoint
    chk = CheckpointEngine.create_checkpoint(
        workflow=wf,
        step_index=0,
        step_name="OCR Step",
        inputs={"file": "test.pdf"},
        outputs={"text": "hello"},
        variables={"status": "OK"},
        memory={"tenant": "t1"},
        fencing_token=1,
    )
    assert chk.checkpoint_id.startswith("chk_")
    assert wf.current_step_index == 1
    assert len(wf.checkpoints) == 1

    # Pause & Resume
    engine.pause_workflow(wf.workflow_id)
    assert wf.state == JobState.PAUSED

    engine.resume_workflow(wf.workflow_id, new_worker_id="node_us_east_02")
    assert wf.state == JobState.RUNNING
    assert wf.assigned_worker_id == "node_us_east_02"

    # Crash migration
    migrated = engine.migrate_workflow_on_crash(
        crashed_worker_id="node_us_east_02",
        target_worker_id="node_eu_central_01",
    )
    assert len(migrated) == 1
    assert migrated[0].assigned_worker_id == "node_eu_central_01"


# -----------------------------------------------------------------------------
# 6. Distributed Lock Manager Tests
# -----------------------------------------------------------------------------

def test_distributed_lock_acquisition_and_fencing():
    dlm = DistributedLockManager()
    lease1 = dlm.acquire_lock("resource_agent_dag", holder_id="worker_01", lease_duration_sec=10)
    assert lease1 is not None
    assert lease1.fencing_token == 1
    assert dlm.is_locked("resource_agent_dag") is True

    # Duplicate acquisition by other worker should fail
    lease2 = dlm.acquire_lock("resource_agent_dag", holder_id="worker_02", lease_duration_sec=10)
    assert lease2 is None

    # Release
    released = dlm.release_lock("resource_agent_dag", holder_id="worker_01")
    assert released is True
    assert dlm.is_locked("resource_agent_dag") is False

    # Second acquisition gets higher fencing token
    lease3 = dlm.acquire_lock("resource_agent_dag", holder_id="worker_02", lease_duration_sec=10)
    assert lease3 is not None
    assert lease3.fencing_token == 2


# -----------------------------------------------------------------------------
# 7. Autoscaling Engine Tests
# -----------------------------------------------------------------------------

def test_autoscaling_evaluation():
    fleet = WorkerFleetManager()
    queue = QueueManager()
    autoscaler = AutoscalingEngine(fleet_manager=fleet, queue_manager=queue)

    # Idle evaluation
    decision_idle = autoscaler.evaluate_scaling()
    assert decision_idle["action"] in [ScalingAction.STABLE.value, ScalingAction.SCALE_DOWN.value]

    # Pressure evaluation: enqueue 20 jobs
    from app.runtime.distributed.models.schemas import ScheduledJob
    for i in range(20):
        queue.get_channel("agent_tasks").enqueue(
            ScheduledJob(workflow_id=f"wf_{i}", agent_id="a", task_name="t")
        )
    decision_pressure = autoscaler.evaluate_scaling()
    assert decision_pressure["action"] == ScalingAction.SCALE_UP.value
    assert decision_pressure["desired_workers"] >= decision_pressure["current_workers"]


# -----------------------------------------------------------------------------
# 8. Region Router & Latency Matrix Tests
# -----------------------------------------------------------------------------

def test_region_router_latencies():
    lat_intra = RegionRouter.get_latency(RegionName.US_EAST, RegionName.US_EAST)
    assert lat_intra < 15.0
    lat_cross = RegionRouter.get_latency(RegionName.US_EAST, RegionName.ASIA_EAST)
    assert lat_cross > 100.0

    topology = RegionRouter.get_region_topology()
    assert len(topology) >= 4


# -----------------------------------------------------------------------------
# 9. Model Gateway & Distributed Cache Tests
# -----------------------------------------------------------------------------

def test_model_gateway_and_cache():
    cache = DistributedCache()
    cache.set("k1", "v1", ttl_sec=60)
    assert cache.get("k1") == "v1"

    gateway = ModelGateway(cache=cache)
    # First invocation -> simulated dispatch & cache set
    res1 = gateway.invoke_model("gemini-2.0-flash", "What is the architecture?")
    assert res1["source"] == "MODEL_GATEWAY_DISPATCH"

    # Second identical invocation -> cache hit
    res2 = gateway.invoke_model("gemini-2.0-flash", "What is the architecture?")
    assert res2["source"] == "CACHE_HIT"
    assert res2["latency_ms"] < 10.0


# -----------------------------------------------------------------------------
# 10. Disaster Recovery Engine Tests
# -----------------------------------------------------------------------------

def test_disaster_recovery_snapshots_and_drills():
    dr = DisasterRecoveryEngine()
    snap = dr.create_snapshot(source_region=RegionName.US_EAST, workflow_count=30, checkpoint_count=120)
    assert snap.snapshot_id.startswith("snap_")
    assert snap.status == "REPLICATED"

    drill_res = dr.execute_failover_drill(
        failed_region=RegionName.US_EAST,
        target_failover_region=RegionName.EU_CENTRAL,
    )
    assert drill_res["status"] == "PASSED"
    assert drill_res["data_loss_detected"] is False
    assert drill_res["rpo_achieved_sec"] <= 2.0


# -----------------------------------------------------------------------------
# 11. End-to-End Distributed Runtime Cycle Test
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_distributed_runtime_cycle(runtime):
    cycle = await runtime.execute_distributed_cycle()
    assert cycle["cycle_status"] == "COMPLETED"
    assert "autoscaling_decision" in cycle

    overview = runtime.get_cluster_overview()
    assert overview.total_workers >= 4
    assert overview.status == "HEALTHY"


# -----------------------------------------------------------------------------
# 12. FastAPI Endpoints Integration Tests
# -----------------------------------------------------------------------------

def test_api_cluster_overview_and_workers(client):
    res_ov = client.get("/api/v1/distributed/cluster/overview")
    assert res_ov.status_code == 200
    assert "total_workers" in res_ov.json()

    res_w = client.get("/api/v1/distributed/workers")
    assert res_w.status_code == 200
    workers = res_w.json()
    assert len(workers) >= 4

    wid = workers[0]["worker_id"]
    res_hb = client.post(f"/api/v1/distributed/workers/{wid}/heartbeat", json={"cpu_pct": 20.0, "memory_pct": 25.0})
    assert res_hb.status_code == 200
    assert res_hb.json()["status"] == "HEARTBEAT_ACK"


def test_api_scheduler_and_workflows(client):
    job_req = {
        "workflow_id": "wf_api_test_01",
        "agent_id": "agent_chief_architect",
        "task_name": "API Task",
        "priority": "HIGH",
    }
    res_job = client.post("/api/v1/distributed/scheduler/jobs", json=job_req)
    assert res_job.status_code == 200
    assert res_job.json()["priority"] == "HIGH"

    res_wf = client.get("/api/v1/distributed/workflows/durable")
    assert res_wf.status_code == 200
    wfs = res_wf.json()
    assert len(wfs) > 0

    wfid = wfs[0]["workflow_id"]
    res_pause = client.post(f"/api/v1/distributed/workflows/{wfid}/pause")
    assert res_pause.status_code == 200
    assert res_pause.json()["state"] == "PAUSED"

    res_resume = client.post(f"/api/v1/distributed/workflows/{wfid}/resume")
    assert res_resume.status_code == 200
    assert res_resume.json()["state"] == "RUNNING"


def test_api_autoscaling_chaos_and_dr(client):
    res_auto = client.post("/api/v1/distributed/autoscaling/evaluate")
    assert res_auto.status_code == 200
    assert "action" in res_auto.json()

    res_reg = client.get("/api/v1/distributed/regions")
    assert res_reg.status_code == 200
    assert len(res_reg.json()) >= 4

    # Chaos Injection
    res_w = client.get("/api/v1/distributed/workers")
    wid = res_w.json()[0]["worker_id"]
    res_chaos = client.post("/api/v1/distributed/chaos/inject-failure", json={"worker_id": wid})
    assert res_chaos.status_code == 200
    assert res_chaos.json()["status"] == "CHAOS_INJECTED"

    # DR Drill
    res_drill = client.post(
        "/api/v1/distributed/disaster-recovery/drill",
        json={"failed_region": "us-east-1", "target_failover_region": "eu-central-1"},
    )
    assert res_drill.status_code == 200
    assert res_drill.json()["status"] == "PASSED"

    # Cycle
    res_cycle = client.post("/api/v1/distributed/runtime/cycle")
    assert res_cycle.status_code == 200
    assert res_cycle.json()["cycle_status"] == "COMPLETED"
