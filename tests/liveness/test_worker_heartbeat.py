"""
Tests for Worker Heartbeat and Zombie Detection (Parts 5 & 8).
"""
import pytest
import time
from app.platform_verification.liveness.worker.worker_heartbeat_manager import (
    WorkerHeartbeatManager,
)


def test_worker_heartbeat_healthy():
    manager = WorkerHeartbeatManager(heartbeat_timeout_seconds=30.0)
    report = manager.evaluate_worker_heartbeats()

    assert report.total_workers_tracked >= 3
    assert report.active_workers_count == report.total_workers_tracked
    assert report.zombie_workers_count == 0
    assert report.all_workers_healthy is True
    assert report.passed is True


def test_worker_zombie_detection():
    manager = WorkerHeartbeatManager(heartbeat_timeout_seconds=10.0)
    # Simulate a stale worker
    manager._workers["worker-001"]["last_heartbeat"] = time.time() - 50.0

    report = manager.evaluate_worker_heartbeats()
    assert report.zombie_workers_count == 1
    assert report.all_workers_healthy is False
    assert report.passed is False

    w01 = next(w for w in report.workers if w["worker_id"] == "worker-001")
    assert w01["status"] == "unhealthy"


def test_worker_heartbeat_registration():
    manager = WorkerHeartbeatManager()
    manager.register_heartbeat("worker-new", current_task="task_validation")
    report = manager.evaluate_worker_heartbeats()
    assert report.total_workers_tracked >= 4
    w_new = next(w for w in report.workers if w["worker_id"] == "worker-new")
    assert w_new["status"] == "alive"
