"""
Tests for Recovery Workflows, Checkpoint Manager, and Integrity Verification.
"""


from app.infrastructure.recovery.checkpoints import (
    CheckpointManager,
    CheckpointStatus,
    CheckpointType,
)
from app.infrastructure.recovery.verification import (
    RecoveryVerifier,
    VerificationStatus,
)
from app.infrastructure.recovery.workflows import (
    RecoveryStep,
    WorkflowCategory,
    build_ai_provider_fallback_workflow,
    build_database_corruption_workflow,
    build_queue_loss_workflow,
    build_region_outage_workflow,
    build_storage_loss_workflow,
)
from app.infrastructure.recovery.executor import (
    RecoveryWorkflowExecutor,
)


def test_checkpoint_lifecycle_and_verification():
    mgr = CheckpointManager()
    data = {"users": 1500, "documents": 9400, "schema_version": "v3.1"}

    cp = mgr.create_checkpoint(
        checkpoint_id="cp-db-001",
        checkpoint_type=CheckpointType.DATABASE_DUMP,
        entity_id="db-postgres-primary",
        region_id="us-east-1",
        payload_data=data,
        retention_days=7,
    )

    assert cp.status == CheckpointStatus.VERIFIED
    assert cp.size_bytes > 0
    assert mgr.get_payload("cp-db-001") == data

    # Tamper with storage
    mgr._payload_storage["cp-db-001"] = '{"tampered": true}'
    assert not mgr.verify_checkpoint("cp-db-001")
    assert cp.status == CheckpointStatus.CORRUPTED


def test_recovery_verifier():
    verifier = RecoveryVerifier()
    sample_data = {"record_1": "abc", "record_2": "def", "schema_version": "v1.0"}
    import json, hashlib
    expected_hash = hashlib.sha256(json.dumps(sample_data, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    # Successful verification
    res_valid = verifier.verify_payload_integrity(
        entity_id="doc-store",
        restored_data=sample_data,
        expected_hash=expected_hash,
        expected_count=3,
        expected_schema_version="v1.0",
    )
    assert res_valid.status == VerificationStatus.VALID
    assert res_valid.checksum_match
    assert res_valid.schema_compatible

    # Corrupted verification
    res_corrupted = verifier.verify_payload_integrity(
        entity_id="doc-store",
        restored_data={"record_1": "corrupted"},
        expected_hash=expected_hash,
    )
    assert res_corrupted.status == VerificationStatus.CORRUPTED


def test_recovery_workflows_generation():
    wf_region = build_region_outage_workflow("wf-reg", "us-east-1", "us-west-2")
    assert wf_region.category == WorkflowCategory.REGION_OUTAGE
    assert len(wf_region.steps) == 6

    wf_db = build_database_corruption_workflow("wf-db", "db-1", "cp-1")
    assert wf_db.category == WorkflowCategory.DATABASE_CORRUPTION
    assert len(wf_db.steps) == 6

    wf_storage = build_storage_loss_workflow("wf-st", "vol-1", "vol-replica-1")
    assert wf_storage.category == WorkflowCategory.STORAGE_LOSS

    wf_queue = build_queue_loss_workflow("wf-q", "q-tasks")
    assert wf_queue.category == WorkflowCategory.QUEUE_LOSS

    wf_ai = build_ai_provider_fallback_workflow("wf-ai", "gemini-primary", "gemini-secondary")
    assert wf_ai.category == WorkflowCategory.AI_PROVIDER_FALLBACK


def test_workflow_executor_success_and_rollback():
    executor = RecoveryWorkflowExecutor()
    wf = build_database_corruption_workflow("wf-db-exec", "db-main", "cp-100")

    # Step 1: Normal execution
    report_success = executor.execute_workflow(wf)
    assert report_success.success
    assert report_success.completed_steps == 6
    assert report_success.failed_steps == 0

    # Step 2: Test rollback on step failure
    wf_failing = build_database_corruption_workflow("wf-db-fail", "db-main", "cp-100")

    rollbacks_triggered = []

    def mock_rollback_quarantine(step: RecoveryStep):
        rollbacks_triggered.append(step.step_id)
        return True

    def mock_fail_fetch(step: RecoveryStep):
        return False  # Simulate fetch checkpoint failure

    executor.register_step_handler("quarantine_db", handler=lambda s: True, rollback_handler=mock_rollback_quarantine)
    executor.register_step_handler("fetch_checkpoint", handler=mock_fail_fetch)

    report_failure = executor.execute_workflow(wf_failing)
    assert not report_failure.success
    assert report_failure.failed_steps == 1
    assert report_failure.rolled_back_steps == 1
    assert rollbacks_triggered == ["quarantine_db"]
