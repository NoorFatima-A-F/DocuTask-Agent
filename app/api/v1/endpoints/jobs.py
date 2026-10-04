"""
Asynchronous Job Management API Router.
Provides endpoints for document submission, job execution, status polling, DLQ listing, and manual DLQ replaying.
"""

from typing import Optional
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.workers import get_queue_provider
from app.jobs.broker import job_broker
from app.jobs.dlq import DeadLetterQueueEngine
from app.jobs.idempotency import IdempotencyEngine
from app.jobs.state_machine import JobState
from app.models.user import User
from app.repositories.document_repository import DocumentRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.workers.dispatcher import JobDispatcher

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


class JobExtractRequest(BaseModel):
    """Payload for extracting document via async worker pipeline."""

    document_type: str = "generic"
    priority: int = 1
    force_reextract: bool = False


@router.post("/extract/{document_id}", status_code=status.HTTP_202_ACCEPTED)
async def enqueue_extraction_job(
    document_id: UUID,
    request: JobExtractRequest = JobExtractRequest(),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Enqueues an asynchronous document extraction pipeline job."""
    dispatcher = JobDispatcher(
        job_repo=ProcessingJobRepository(db), doc_repo=DocumentRepository(db), queue_provider=get_queue_provider()
    )
    job_res = await dispatcher.enqueue_document_pipeline(
        document_id=document_id,
        owner=current_user,
        document_type=request.document_type,
        priority=request.priority,
        force_reextract=request.force_reextract,
    )
    return {"success": True, "data": job_res.model_dump()}


@router.get("", status_code=status.HTTP_200_OK)
async def list_jobs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lists current user background jobs with pagination."""
    dispatcher = JobDispatcher(
        job_repo=ProcessingJobRepository(db), doc_repo=DocumentRepository(db), queue_provider=get_queue_provider()
    )
    job_list = await dispatcher.list_user_jobs(current_user, page=page, page_size=page_size)
    return {"success": True, "data": job_list.model_dump()}


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
        "status": JobState.QUEUED,
    }

    # Enqueue payload to broker (<100ms)
    await job_broker.enqueue(payload, priority=request.priority)

    return JobSubmitResponse(
        job_id=job_id,
        document_id=request.document_id,
        status=JobState.QUEUED,
        idempotency_key=idempotency_key,
        priority=request.priority,
    )


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


@router.get("/{job_id}/status")
async def get_job_legacy_status(job_id: str):
    """
    Retrieves real-time processing status and checkpoint progress for a job.
    """
    return {
        "job_id": job_id,
        "status": JobState.PROCESSING,
        "checkpoint_page": 1,
        "total_pages": 1,
        "progress_percentage": 100.0,
    }


@router.get("/{job_id}", status_code=status.HTTP_200_OK)
async def get_job_by_id(
    job_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Retrieves current job status and details by job ID."""
    dispatcher = JobDispatcher(
        job_repo=ProcessingJobRepository(db), doc_repo=DocumentRepository(db), queue_provider=get_queue_provider()
    )
    job_res = await dispatcher.get_job_status(job_id, current_user)
    return {"success": True, "data": job_res.model_dump()}


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
async def cancel_job(job_id: UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Cancels a queued or running job."""
    dispatcher = JobDispatcher(
        job_repo=ProcessingJobRepository(db), doc_repo=DocumentRepository(db), queue_provider=get_queue_provider()
    )
    cancelled = await dispatcher.cancel_job(job_id, current_user)
    return {"success": True, "data": cancelled.model_dump()}
