"""Tests for Reproducibility Engine, Snapshot Manager, and Replay Reproducer."""

from app.runtime.reproducibility.environment_capture import (
    DependencyCapture,
    EnvironmentCapture,
)
from app.runtime.reproducibility.reproducer import Reproducer
from app.runtime.reproducibility.snapshot_manager import SnapshotManager


def test_environment_and_dependency_capture():
    env = EnvironmentCapture.capture_current()
    assert env.python_version is not None
    assert len(env.environment_hash) == 64
    assert env.hardware_concurrency > 0

    deps = DependencyCapture.capture_manifest()
    assert deps.total_packages > 0
    assert len(deps.manifest_digest) == 64
    assert any(p.package_name == "fastapi" for p in deps.packages)


def test_snapshot_creation_and_diff():
    mgr = SnapshotManager()
    s1 = mgr.create_snapshot(
        snapshot_id="snap-01",
        mission_id="mission-1",
        step_index=1,
        random_seed=42,
        model_configs={"model": "gemini-2.5-flash"},
        dag_topology={"nodes": ["a", "b"]},
        memory_state_digest="mem-hash-1",
        input_digest="in-hash-1",
        output_digest="out-hash-1",
    )
    assert s1.snapshot_hash is not None
    assert mgr.get_snapshot("snap-01") is not None

    mgr.create_snapshot(
        snapshot_id="snap-02",
        mission_id="mission-1",
        step_index=1,
        random_seed=42,
        model_configs={"model": "gemini-2.5-flash"},
        dag_topology={"nodes": ["a", "b"]},
        memory_state_digest="mem-hash-1",
        input_digest="in-hash-1",
        output_digest="out-hash-1",
    )

    diff = mgr.diff_snapshots("snap-01", "snap-02")
    assert diff["seed_match"] is True
    assert diff["env_match"] is True
    assert diff["input_match"] is True


def test_reproducer_deterministic_replay():
    mgr = SnapshotManager()
    mgr.create_snapshot(
        snapshot_id="snap-replay-test",
        mission_id="mission-replay",
        step_index=1,
        random_seed=1337,
        model_configs={"model": "gemini-2.5-flash"},
        dag_topology={"nodes": ["ocr"]},
        memory_state_digest="mem-replay-001",
        input_digest="in-replay-001",
        output_digest="out-replay-001",
    )

    reproducer = Reproducer(snapshot_mgr=mgr)
    result = reproducer.reproduce("snap-replay-test")

    assert result.is_reproduced is True
    assert result.fidelity_score == 1.0
    assert result.bit_for_bit_match is True
    assert len(result.verification_log) > 0
    assert len(reproducer.get_history()) == 1
