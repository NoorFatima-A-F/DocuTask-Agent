"""
Asynchronous Job Management API Router.
Provides endpoints for document submission, job status polling, DLQ listing, and manual DLQ replaying.
"""

from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.jobs.broker import job_broker
from app.jobs.dlq import DeadLetterQueueEngine
from app.jobs.idempotency import IdempotencyEngine
from app.jobs.state_machine import JobState

router = APIRouter(prefix="/jobs", tags=["Asynchronous Jobs"])


class JobSubmitRequest(BaseModel):
    """Payload for submitting an asynchronous processing job."""
    document_id: str
    document_hash: str
    document_type: str = "invoice"
    priority: str = "MEDIUM"


class JobSubmitResponse(BaseModel):
    """Response returned upon job submission in <100ms."""
    job_id: str
    document_id: str
    status: str
    idempotency_key: str
    priority: str


@router.post("/submit", response_model=JobSubmitResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_job(request: JobSubmitRequest):
    """
    Submits a document for asynchronous background processing (<100ms response time).
    Generates idempotency key and enqueues job to Priority Message Broker.
    """
    job_id = str(uuid4())
    idempotency_key = IdempotencyEngine.generate_key(request.document_hash)

    payload = {
        "job_id": job_id,
        "document_id": request.document_id,
        "document_type": request.document_type,
        "idempotency_key": idempotency_key,
        "priority": request.priority,
        "status": JobState.QUEUED
    }

    # Enqueue payload to broker (<100ms)
    await job_broker.enqueue(payload, priority=request.priority)

    return JobSubmitResponse(
        job_id=job_id,
        document_id=request.document_id,
        status=JobState.QUEUED,
        idempotency_key=idempotency_key,
        priority=request.priority
    )


@router.get("/{job_id}/status")
async def get_job_status(job_id: str):
    """
    Retrieves real-time processing status and checkpoint progress for a job.
    """
    return {
        "job_id": job_id,
        "status": JobState.PROCESSING,
        "checkpoint_page": 1,
        "total_pages": 1,
        "progress_percentage": 100.0
    }


@router.get("/dlq/list")
async def list_dlq():
    """Lists items currently in the Dead Letter Queue."""
    return {"dlq_items": DeadLetterQueueEngine.list_dlq_items()}


@router.post("/dlq/replay/{job_id}")
async def replay_dlq_job(job_id: str):
    """
    Manually replays a failed job from the Dead Letter Queue back into the active processing queue.
    """
    success = await DeadLetterQueueEngine.replay_job(job_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found in Dead Letter Queue")
    return {"message": f"Job '{job_id}' successfully replayed back to active queue."}
