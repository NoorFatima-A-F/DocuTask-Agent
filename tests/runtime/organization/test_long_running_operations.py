"""
Test Suite: Long Running Operations & State Durability
Validates persistent checkpointing, heartbeat monitoring, persistent scheduler, crash recovery, and distributed leases.
"""
from app.runtime.operations.checkpoint_manager import CheckpointManager
from app.runtime.operations.heartbeat_manager import HeartbeatManager
from app.runtime.operations.persistent_scheduler import PersistentScheduler
from app.runtime.operations.recovery_snapshot import RecoverySnapshotEngine
from app.runtime.operations.lease_manager import LeaseManager


def test_checkpoint_manager_persistence():
    mgr = CheckpointManager()
    
    cp = mgr.create_checkpoint(
        mission_id="mission_test_chk",
        completed_tasks=["task_1", "task_2"],
        in_flight_tasks=["task_3"],
        accumulated_cost_usd=0.0035,
        full_state_payload={"key": "value", "step": 3},
    )

    assert cp.mission_id == "mission_test_chk"
    assert cp.sequence_number == 1
    assert cp.state_payload_hash.startswith("sha256_")

    latest = mgr.get_latest_checkpoint("mission_test_chk")
    assert latest is not None
    assert latest.checkpoint_id == cp.checkpoint_id


def test_heartbeat_manager_liveness():
    mgr = HeartbeatManager(timeout_seconds=1.0)
    
    status_initial = mgr.check_liveness()
    assert status_initial["all_departments_healthy"] is True

    # Record specific department heartbeat
    mgr.record_heartbeat("dept_ocr", active_ops=3)
    assert mgr.heartbeats["dept_ocr"].active_operations_count == 3


def test_persistent_scheduler():
    sched = PersistentScheduler()
    
    op = sched.schedule_operation(
        name="Test Periodic Sync",
        target_department_id="dept_validation",
        interval_minutes=120,
        payload={"scope": "TEST"},
    )

    assert op.is_active is True
    assert op.cron_interval_minutes == 120
    assert len(sched.list_scheduled_operations()) >= 3


def test_recovery_snapshot_engine():
    res = RecoverySnapshotEngine.recover_mission("mission_live_001")
    assert res.is_successful is True
    assert res.mission_id == "mission_live_001"
    assert res.restored_task_count >= 1


def test_lease_manager_fencing_tokens():
    mgr = LeaseManager()
    
    l1 = mgr.acquire_lease("GPU_NODE_99", "dept_ocr", ttl_seconds=30.0)
    assert l1 is not None
    assert l1.holder_department_id == "dept_ocr"
    assert l1.fencing_token > 100

    # Another department cannot acquire active lease
    l2 = mgr.acquire_lease("GPU_NODE_99", "dept_extraction", ttl_seconds=30.0)
    assert l2 is None

    # Release lease
    assert mgr.release_lease("GPU_NODE_99", "dept_ocr") is True
