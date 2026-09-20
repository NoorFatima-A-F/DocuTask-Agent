"""Tests for Immutable Audit Store, Immutability Invariant, and Partitioning."""

import pytest
from app.audit.core.events import AuditEvent
from app.audit.storage.immutable_store import ImmutableAuditStore
from app.audit.storage.partitions import AuditPartitionManager
from app.audit.storage.repository import AuditRepository


def test_partition_key_generation():
    key = AuditPartitionManager.get_partition_key(
        tenant_id="tenant_fin",
        category="WORKFLOW",
    )
    assert key.startswith("tenant_fin/")
    assert "/WORKFLOW" in key


def test_immutable_store_append_and_rejection_of_duplicates():
    store = ImmutableAuditStore()
    ev = AuditEvent(
        event_id="evt_unique_1",
        event_type="auth.login",
        tenant_id="tenant_sec",
        actor_id="usr_1",
        action="login",
        resource_type="auth",
        resource_id="sess_1",
    )
    appended = store.append(ev)
    assert appended.integrity_hash is not None
    assert appended.signature is not None

    # Overwrite attempt should be strictly rejected
    with pytest.raises(ValueError, match="Immutability violation"):
        store.append(ev)


def test_audit_repository_multi_key_lookups():
    repo = AuditRepository()
    for i in range(4):
        repo.record(
            AuditEvent(
                event_id=f"repo_evt_{i}",
                event_type="agent.step",
                tenant_id="tenant_repo",
                actor_id=f"agent_{i%2}",
                action="step",
                resource_type="agent",
                resource_id=f"agent_res_{i%2}",
                correlation_id="corr_shared_100",
                request_id=f"req_{i}",
            )
        )

    # 1. By ID
    assert repo.get_by_id("repo_evt_0", tenant_id="tenant_repo") is not None
    assert repo.get_by_id("repo_evt_0", tenant_id="wrong_tenant") is None

    # 2. By Correlation
    correlated = repo.find_by_correlation("corr_shared_100", tenant_id="tenant_repo")
    assert len(correlated) == 4

    # 3. By Resource
    res_events = repo.find_by_resource("agent", "agent_res_0", tenant_id="tenant_repo")
    assert len(res_events) == 2
