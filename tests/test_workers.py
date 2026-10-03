"""
Unit and Integration Tests for Asynchronous Workers & Queue Subsystem.
"""

import shutil
import tempfile
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.repositories.document_repository import DocumentRepository
from app.repositories.processing_job_repository import ProcessingJobRepository
from app.repositories.user_repository import UserRepository
from app.services.document_service import DocumentService
from app.storage.local import LocalStorageProvider
from app.workers.dispatcher import JobDispatcher
from app.workers.exceptions import DuplicateJobException
from app.workers.jobs import JobState, JobTask
from app.workers.queue import AsyncInMemoryJobQueue
from app.workers.worker import AsyncWorkerEngine


@pytest.fixture
def temp_storage_dir():
    """Temporary storage fixture."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_async_in_memory_job_queue():
    """Tests AsyncInMemoryJobQueue enqueue, dequeue, size, and cancellation."""
    queue = AsyncInMemoryJobQueue()
    job_id = uuid.uuid4()
    doc_id = uuid.uuid4()

    task = JobTask(job_id=job_id, document_id=doc_id)
    await queue.enqueue(task)
    assert await queue.get_queue_size() == 1

    # Dequeue task
    dequeued = await queue.dequeue()
    assert dequeued is not None
    assert dequeued.job_id == job_id
    queue.task_done()

    # Test cancellation
    cancel_task = JobTask(job_id=uuid.uuid4(), document_id=doc_id)
    await queue.enqueue(cancel_task)
    await queue.cancel(cancel_task.job_id)

    # Cancelled task is skipped on dequeue
    skipped = await queue.dequeue()
    assert skipped is None


@pytest.mark.asyncio
async def test_job_dispatcher_duplicate_prevention(db_session: AsyncSession, temp_storage_dir: str):
    """Tests JobDispatcher enqueueing and active job duplicate prevention."""
    user_repo = UserRepository(db_session)
    doc_repo = DocumentRepository(db_session)
    job_repo = ProcessingJobRepository(db_session)
    storage = LocalStorageProvider(base_directory=temp_storage_dir)

    doc_service = DocumentService(document_repo=doc_repo, storage_provider=storage)
    queue = AsyncInMemoryJobQueue()
    dispatcher = JobDispatcher(job_repo=job_repo, doc_repo=doc_repo, queue_provider=queue)

    user = await user_repo.create({"email": "disp_user@example.com", "username": "dispuser", "hashed_password": "p"})

    from PIL import Image
    import io
    img = Image.new("RGB", (50, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    up_res = await doc_service.upload_document(buf.getvalue(), "doc.png", "image/png", user)
    doc_id = up_res.document.id

    # 1. Enqueue Job
    job_res = await dispatcher.enqueue_document_pipeline(doc_id, user, document_type="invoice")
    assert job_res.status == JobState.QUEUED.value
    assert job_res.progress == 0.0

    # 2. Duplicate Enqueue Attempt Fails
    with pytest.raises(DuplicateJobException):
        await dispatcher.enqueue_document_pipeline(doc_id, user, document_type="invoice")

    # 3. Ownership Isolation Check
    user2 = await user_repo.create({"email": "other@example.com", "username": "other", "hashed_password": "p"})
    with pytest.raises(ResourceNotFoundException):
        await dispatcher.get_job_status(job_res.id, user2)


@pytest.mark.asyncio
async def test_worker_engine_execution(db_session: AsyncSession, temp_storage_dir: str):
    """Tests AsyncWorkerEngine task execution and status/progress updates."""
    user_repo = UserRepository(db_session)
    doc_repo = DocumentRepository(db_session)
    job_repo = ProcessingJobRepository(db_session)
    storage = LocalStorageProvider(base_directory=temp_storage_dir)

    doc_service = DocumentService(document_repo=doc_repo, storage_provider=storage)
    queue = AsyncInMemoryJobQueue()
    dispatcher = JobDispatcher(job_repo=job_repo, doc_repo=doc_repo, queue_provider=queue)

    user = await user_repo.create({"email": "worker_user@example.com", "username": "workeruser", "hashed_password": "p"})

    from PIL import Image
    import io
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    up_res = await doc_service.upload_document(buf.getvalue(), "scan.png", "image/png", user)
    doc_id = up_res.document.id

    # Enqueue job
    job_res = await dispatcher.enqueue_document_pipeline(doc_id, user, document_type="receipt")

    # Run worker single execution step manually
    worker = AsyncWorkerEngine(queue_provider=queue, worker_name="TestWorker")
    task = await queue.dequeue(timeout=1.0)
    assert task is not None
    await worker._execute_task(task)

    # Check updated job status in DB
    updated_job = await job_repo.get_by_id(job_res.id)
    assert updated_job is not None
    assert updated_job.status == JobState.COMPLETED.value
    assert updated_job.progress == 100.0


@pytest.mark.asyncio
async def test_jobs_api_full_workflow(client: AsyncClient):
    """Verifies Job HTTP API endpoints via AsyncClient."""

    # 1. Register & Login User
    reg = await client.post("/api/v1/auth/register", json={
        "email": "job_api_user@example.com",
        "username": "jobapiuser",
        "password": "Password123!"
    })
    assert reg.status_code == 201

    login = await client.post("/api/v1/auth/login", json={
        "username_or_email": "jobapiuser",
        "password": "Password123!"
    })
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload Document
    from PIL import Image
    import io
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    files = {"file": ("async_doc.png", buf.getvalue(), "image/png")}
    up_res = await client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert up_res.status_code == 201
    doc_id = up_res.json()["data"]["document"]["id"]

    # 3. POST /jobs/extract/{document_id} -> 202 Accepted
    job_req = {"document_type": "contract", "priority": 2}
    enqueue_res = await client.post(f"/api/v1/jobs/extract/{doc_id}", json=job_req, headers=headers)
    assert enqueue_res.status_code == 202
    body = enqueue_res.json()
    assert body["success"] is True
    job_id = body["data"]["id"]
    assert body["data"]["status"] == "QUEUED"

    # 4. GET /jobs/{job_id}
    status_res = await client.get(f"/api/v1/jobs/{job_id}", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["data"]["id"] == job_id

    # 5. GET /jobs (List)
    list_res = await client.get("/api/v1/jobs", headers=headers)
    assert list_res.status_code == 200
    assert list_res.json()["data"]["total"] >= 1

    # 6. DELETE /jobs/{job_id} (Cancel)
    cancel_res = await client.delete(f"/api/v1/jobs/{job_id}", headers=headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["data"]["status"] == "CANCELLED"
