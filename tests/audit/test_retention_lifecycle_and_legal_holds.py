"""Tests for Retention Policies, Lifecycle Archival, and Legal Holds."""

from datetime import datetime, timezone, timedelta
from app.audit.storage.repository import AuditRepository
from app.audit.core.events import AuditEvent
from app.audit.retention.policies import RetentionPolicy, RetentionAction
from app.audit.retention.lifecycle import RetentionLifecycleManager


def test_retention_lifecycle_evaluation():
    repo = AuditRepository()
    manager = RetentionLifecycleManager(repository=repo)

    tenant_id = "tenant_retention"

    # Old event (400 days old)
    old_time = datetime.now(timezone.utc) - timedelta(days=400)
    repo.record(
        AuditEvent(
            event_id="ev_old",
            event_type="doc.read",
            tenant_id=tenant_id,
            actor_id="user_1",
            action="read",
            resource_type="doc",
            resource_id="doc_1",
            timestamp=old_time,
        )
    )

    # Recent event (10 days old)
    recent_time = datetime.now(timezone.utc) - timedelta(days=10)
    repo.record(
        AuditEvent(
            event_id="ev_recent",
            event_type="doc.read",
            tenant_id=tenant_id,
            actor_id="user_1",
            action="read",
            resource_type="doc",
            resource_id="doc_2",
            timestamp=recent_time,
        )
    )

    # Configure 365-day archive policy
    manager.add_policy(
        RetentionPolicy(
            tenant_id=tenant_id,
            name="1 Year Archive",
            action=RetentionAction.ARCHIVE,
            retention_days=365,
        )
    )

    result = manager.evaluate_retention(tenant_id=tenant_id)
    assert result.total_events == 2
    assert "ev_old" in result.eligible_for_archive
    assert "ev_recent" not in result.eligible_for_archive


def test_legal_hold_locks_prevent_archival_and_deletion():
    repo = AuditRepository()
    manager = RetentionLifecycleManager(repository=repo)

    tenant_id = "tenant_litigation"
    old_time = datetime.now(timezone.utc) - timedelta(days=500)
    
    repo.record(
        AuditEvent(
            event_id="ev_subpoena",
            event_type="financial.transfer",
            tenant_id=tenant_id,
            actor_id="finance_user",
            action="transfer",
            resource_type="account",
            resource_id="acc_001",
            timestamp=old_time,
        )
    )

    # Place legal hold lock
    hold = manager.apply_legal_hold(
        tenant_id=tenant_id,
        reason="Court subpoena case #2026-CV-8891",
        applied_by="legal_counsel",
        event_ids=["ev_subpoena"],
    )
    assert hold.is_active is True

    # Evaluate retention
    manager.add_policy(
        RetentionPolicy(
            tenant_id=tenant_id,
            name="Purge Old",
            action=RetentionAction.DELETE_AFTER_PERIOD,
            retention_days=90,
        )
    )

    result = manager.evaluate_retention(tenant_id=tenant_id)
    assert "ev_subpoena" in result.locked_by_legal_hold
    assert "ev_subpoena" not in result.eligible_for_deletion
