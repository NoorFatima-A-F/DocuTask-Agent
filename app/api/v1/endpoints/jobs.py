"""Background extraction jobs (Celery + Redis).

Clients submit a job, then poll ``GET /jobs/{id}`` until the status is COMPLETED,
NEEDS_REVIEW or FAILED. Resubmitting the same document/type (or the same
``Idempotency-Key``) returns the existing job with 200 instead of 202.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import RoleChecker, get_current_active_user
from app.models.user import User
from app.schemas.job import JobCreateRequest, JobListResponse, JobResponse
from app.schemas.response import APIResponse
from app.services.job_service import Enqueuer, JobService, celery_enqueuer

router = APIRouter(prefix="/jobs", tags=["Jobs"], dependencies=[Depends(get_current_active_user)])

require_admin = RoleChecker(["admin"])


def get_job_enqueuer() -> Enqueuer:
    """Queue publisher. Tests override this dependency."""
    return celery_enqueuer


def get_job_service(db: AsyncSession = Depends(get_db), enqueue: Enqueuer = Depends(get_job_enqueuer)) -> JobService:
    return JobService(db, enqueue)


@router.post(
    "",
    response_model=APIResponse[JobResponse],
    status_code=status.HTTP_202_ACCEPTED,
    responses={200: {"description": "Existing job returned (idempotent resubmission)"}},
)
async def create_job(
    body: JobCreateRequest,
    response: Response,
    idempotency_key: str | None = Header(default=None, max_length=200),
    user: User = Depends(get_current_active_user),
    jobs: JobService = Depends(get_job_service),
):
    job, created = await jobs.submit(user, body.document_id, body.document_type, idempotency_key)
    if not created:
        response.status_code = status.HTTP_200_OK
    return APIResponse.success_response(data=job, message="Job queued" if created else "Existing job")


@router.get("", response_model=APIResponse[JobListResponse])
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_active_user),
    jobs: JobService = Depends(get_job_service),
):
    return APIResponse.success_response(data=await jobs.list_for_owner(user, page, page_size))


@router.get("/failed", response_model=APIResponse[JobListResponse])
async def list_failed_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    _admin: User = Depends(require_admin),
    jobs: JobService = Depends(get_job_service),
):
    """All FAILED jobs with their error codes (admin only)."""
    return APIResponse.success_response(data=await jobs.list_failed(page, page_size))


@router.get("/{job_id}", response_model=APIResponse[JobResponse])
async def get_job(
    job_id: UUID, user: User = Depends(get_current_active_user), jobs: JobService = Depends(get_job_service)
):
    return APIResponse.success_response(data=await jobs.get(user, job_id))


@router.post("/{job_id}/retry", response_model=APIResponse[JobResponse], status_code=status.HTTP_202_ACCEPTED)
async def retry_job(
    job_id: UUID, user: User = Depends(get_current_active_user), jobs: JobService = Depends(get_job_service)
):
    """Re-queue a FAILED job."""
    return APIResponse.success_response(data=await jobs.retry(user, job_id), message="Job re-queued")
