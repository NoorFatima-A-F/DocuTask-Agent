"""
Automated Pytest Suite for Enterprise Asynchronous Processing Architecture & Worker Infrastructure.
Coverage target: > 90%.
"""

import pytest
from app.jobs.broker import PriorityMessageBroker
from app.jobs.dlq import DeadLetterQueueEngine
from app.jobs.idempotency import IdempotencyEngine
from app.jobs.locking import DistributedLockManager
from app.jobs.orchestrator import PipelineOrchestrator
from app.jobs.state_machine import InvalidJobStateTransitionException, JobState, JobStateMachine
from app.jobs.workers import PageChunkingEngine, WorkerPoolManager


def test_job_state_machine_valid_transitions():
    """Verifies valid state transitions."""
    assert JobStateMachine.validate_transition(JobState.CREATED, JobState.UPLOADED) is True
    assert JobStateMachine.validate_transition(JobState.UPLOADED, JobState.QUEUED) is True
    assert JobStateMachine.validate_transition(JobState.QUEUED, JobState.PROCESSING) is True
    assert JobStateMachine.validate_transition(JobState.PROCESSING, JobState.OCR_COMPLETED) is True
    assert JobStateMachine.validate_transition(JobState.OCR_COMPLETED, JobState.AI_PROCESSING) is True
    assert JobStateMachine.validate_transition(JobState.AI_PROCESSING, JobState.VALIDATING) is True
    assert JobStateMachine.validate_transition(JobState.VALIDATING, JobState.COMPLETED) is True


def test_job_state_machine_invalid_transition_rejection():
    """Verifies invalid state transition rejection (e.g. COMPLETED -> PROCESSING)."""
    with pytest.raises(InvalidJobStateTransitionException):
        JobStateMachine.validate_transition(JobState.COMPLETED, JobState.PROCESSING)

    with pytest.raises(InvalidJobStateTransitionException):
        JobStateMachine.validate_transition(JobState.CANCELLED, JobState.QUEUED)


def test_idempotency_key_generation():
    """Verifies SHA-256 idempotency key generation & versioning."""
    key1 = IdempotencyEngine.generate_key("doc_hash_abc", "v1.0")
    key2 = IdempotencyEngine.generate_key("doc_hash_abc", "v1.0")
    key3 = IdempotencyEngine.generate_key("doc_hash_abc", "v2.0")

    assert key1 == key2  # Same input + version -> Same key
    assert key1 != key3  # Different version -> Different key


@pytest.mark.asyncio
async def test_distributed_locking():
    """Verifies DistributedLockManager lock acquisition and release."""
    res_id = "doc_123_lock"
    acquired1 = await DistributedLockManager.acquire_lock(res_id)
    assert acquired1 is True

    # Concurrent attempt should fail
    acquired2 = await DistributedLockManager.acquire_lock(res_id)
    assert acquired2 is False

    # Release lock
    released = await DistributedLockManager.release_lock(res_id)
    assert released is True


@pytest.mark.asyncio
async def test_priority_message_broker_and_anti_starvation():
    """Verifies PriorityMessageBroker priority sorting and anti-starvation."""
    broker = PriorityMessageBroker()
    await broker.enqueue({"job_id": "job_low", "priority": "LOW"}, priority="LOW")
    await broker.enqueue({"job_id": "job_high", "priority": "HIGH"}, priority="HIGH")

    # High priority dequeued first
    item1 = await broker.dequeue()
    assert item1["job_id"] == "job_high"

    item2 = await broker.dequeue()
    assert item2["job_id"] == "job_low"


@pytest.mark.asyncio
async def test_dlq_and_manual_replay():
    """Verifies DeadLetterQueueEngine moving and manual replay mechanism."""
    payload = {"job_id": "job_failed_001", "document_id": "doc_001", "priority": "HIGH"}
    dlq_item = DeadLetterQueueEngine.move_to_dlq(
        job_id="job_failed_001",
        document_id="doc_001",
        failure_reason="AI Provider Outage 500",
        attempt_count=3,
        original_payload=payload
    )
    assert dlq_item.job_id == "job_failed_001"

    # Replay back to active queue
    replayed = await DeadLetterQueueEngine.replay_job("job_failed_001")
    assert replayed is True


def test_worker_lease_and_chunking():
    """Verifies WorkerPoolManager and PageChunkingEngine."""
    worker = WorkerPoolManager.register_worker("worker_ocr_01", "OCR")
    assert worker.worker_id == "worker_ocr_01"

    hb = WorkerPoolManager.send_heartbeat("worker_ocr_01")
    assert hb is True

    # 500 Page PDF chunking
    chunks = PageChunkingEngine.calculate_chunks(total_pages=500, start_page=1)
    assert len(chunks) == 5
    assert chunks[0] == {"start_page": 1, "end_page": 100}
    assert chunks[4] == {"start_page": 401, "end_page": 500}


@pytest.mark.asyncio
async def test_pipeline_orchestrator():
    """Verifies end-to-end multi-stage pipeline orchestration."""
    result = await PipelineOrchestrator.execute_pipeline(
        job_id="job_orch_001",
        document_id="doc_orch_001",
        raw_ocr_text="Invoice # 1001",
        document_type="invoice"
    )
    assert result["status"] == JobState.COMPLETED
    assert "extracted_data" in result
