"""
Tests for Replication Streams, Lag Metrics, Sync Coordination, and Conflict Resolution.
"""

from datetime import datetime, timezone, timedelta
import pytest

from app.infrastructure.replication.models import (
    ReplicationLagMetric,
    ReplicationMode,
    ReplicationStream,
)
from app.infrastructure.replication.replication_manager import (
    ReplicationManager,
)
from app.infrastructure.replication.sync import (
    SyncCoordinator,
)
from app.infrastructure.replication.conflict_resolution import (
    ConflictResolutionStrategy,
    ConflictResolver,
    ReplicationConflict,
    ResolutionResult,
)


def test_replication_manager_and_lag_tracking():
    mgr = ReplicationManager()
    stream = mgr.register_stream(
        stream_id="stream-db-sync",
        source_region="us-east-1",
        target_region="us-west-2",
        dataset_name="documents_db",
        mode=ReplicationMode.ASYNCHRONOUS,
        max_acceptable_lag_seconds=30.0,
    )

    assert stream.stream_id == "stream-db-sync"
    assert stream.mode == ReplicationMode.ASYNCHRONOUS

    # Record normal lag
    mgr.record_lag("stream-db-sync", lag_seconds=5.0, byte_lag=1024, unapplied_mutations=2)
    assert mgr.is_stream_in_sla("stream-db-sync")

    # Record excessive lag exceeding SLA
    mgr.record_lag("stream-db-sync", lag_seconds=45.0)
    assert not mgr.is_stream_in_sla("stream-db-sync")


def test_sync_coordinator_batches_and_locks():
    coordinator = SyncCoordinator()

    # Test lock acquisition
    assert coordinator.acquire_sync_lock("stream-db-sync", lock_ttl_seconds=10.0)
    assert not coordinator.acquire_sync_lock("stream-db-sync", lock_ttl_seconds=10.0)  # Locked

    coordinator.release_sync_lock("stream-db-sync")
    assert coordinator.acquire_sync_lock("stream-db-sync", lock_ttl_seconds=10.0)

    # Test batch creation
    items = [{"doc_id": "1", "action": "INSERT"}, {"doc_id": "2", "action": "UPDATE"}]
    batch = coordinator.create_batch(batch_id="batch-001", stream_id="stream-db-sync", items=items)

    assert batch.mutation_count == 2
    assert batch.sequence_start == 1
    assert batch.sequence_end == 2
    assert not batch.applied

    assert coordinator.apply_batch("batch-001")
    assert batch.applied
    assert len(coordinator.list_unapplied_batches("stream-db-sync")) == 0


def test_conflict_resolver_last_write_wins():
    resolver = ConflictResolver()
    now = datetime.now(timezone.utc)

    conflict = ReplicationConflict(
        conflict_id="conf-01",
        entity_id="doc-123",
        local_value={"title": "Local Title"},
        remote_value={"title": "Remote Title"},
        local_timestamp=now - timedelta(seconds=10),
        remote_timestamp=now,  # Remote is more recent
    )

    res = resolver.resolve(conflict, strategy=ConflictResolutionStrategy.LAST_WRITE_WINS)
    assert res.resolved_value == {"title": "Remote Title"}
    assert not res.requires_manual_intervention


def test_conflict_resolver_vector_clocks():
    resolver = ConflictResolver()
    now = datetime.now(timezone.utc)

    # Local dominates: local={'node1': 2, 'node2': 1}, remote={'node1': 1, 'node2': 1}
    conflict_local_win = ReplicationConflict(
        conflict_id="conf-vc-01",
        entity_id="doc-456",
        local_value="Local Version",
        remote_value="Remote Version",
        local_timestamp=now,
        remote_timestamp=now,
        local_vector_clock={"node1": 2, "node2": 1},
        remote_vector_clock={"node1": 1, "node2": 1},
    )

    res = resolver.resolve(conflict_local_win, strategy=ConflictResolutionStrategy.VECTOR_CLOCK)
    assert res.resolved_value == "Local Version"


def test_conflict_resolver_quorum():
    resolver = ConflictResolver()
    now = datetime.now(timezone.utc)

    conflict_quorum = ReplicationConflict(
        conflict_id="conf-q-01",
        entity_id="doc-789",
        local_value="Val A",
        remote_value="Val B",
        local_timestamp=now,
        remote_timestamp=now,
        quorum_votes={"node-1": "Val B", "node-2": "Val B", "node-3": "Val A"},
    )

    res = resolver.resolve(conflict_quorum, strategy=ConflictResolutionStrategy.QUORUM_BASED)
    assert res.resolved_value == "Val B"
    assert not res.requires_manual_intervention
