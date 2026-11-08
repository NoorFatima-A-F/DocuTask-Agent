"""Celery job system: API (submit/poll/retry/failed), runner outcomes, eager-mode retries, Redis publish."""

from __future__ import annotations

import asyncio
import os
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.database.session as app_session
from app.api.v1.endpoints.jobs import get_job_enqueuer
from app.core.config import settings
from app.core.errors.extraction import ErrorCode, LLMError
from app.database.base import Base
from app.dependencies.storage import get_storage_provider
from app.jobs import tasks
from app.jobs.celery_app import celery_app
from app.jobs.runner import JobDependencies, RetryJob, execute_job
from app.main import app
from app.models.document import Document
from app.models.processing_job import JobStatus, ProcessingJob
from app.models.user import User
from app.ocr.pipeline import OCRPipeline
from app.storage.local import LocalStorageProvider
from tests.fakes.data import CONTOSO_INVOICE_JSON, CONTOSO_INVOICE_TEXT, png_bytes
from tests.fakes.llm import FakeLLMProvider
from tests.fakes.ocr import FakeOCRProvider
from tests.test_reviews import _user

RATE_LIMITED = LLMError(ErrorCode.LLM_RATE_LIMITED, retry_after=0)
JOBS = f"{settings.API_V1_STR}/jobs"


class RecordingEnqueuer:
    def __init__(self, error: Exception | None = None):
        self.ids: list[uuid.UUID] = []
        self.error = error

    def __call__(self, job_id: uuid.UUID) -> None:
        if self.error:
            raise self.error
        self.ids.append(job_id)


async def _upload(client: AsyncClient, headers: dict[str, str]) -> str:
    up = await client.post(
        f"{settings.API_V1_STR}/documents/upload",
        files={"file": ("inv.png", png_bytes(), "image/png")},
        headers=headers,
    )
    assert up.status_code in (200, 201), up.text
    return up.json()["data"]["document"]["id"]


def _deps(*llm_script) -> JobDependencies:  # type: ignore[no-untyped-def]
    return JobDependencies(
        ocr_pipeline=OCRPipeline(ocr_provider=FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)),
        llm_provider=FakeLLMProvider(*llm_script),
        storage=get_storage_provider(),
    )


# --------------------------------------------------------------------------- API


async def test_submit_poll_and_idempotent_resubmit(client: AsyncClient, db_session: AsyncSession) -> None:
    enq = RecordingEnqueuer()
    app.dependency_overrides[get_job_enqueuer] = lambda: enq
    owner = await _user(client, db_session, "jobowner1")
    doc_id = await _upload(client, owner)

    first = await client.post(JOBS, json={"document_id": doc_id, "document_type": "invoice"}, headers=owner)
    assert first.status_code == 202, first.text
    job = first.json()["data"]
    assert job["status"] == "QUEUED" and job["attempts"] == 0
    assert enq.ids == [uuid.UUID(job["id"])]

    again = await client.post(JOBS, json={"document_id": doc_id, "document_type": "invoice"}, headers=owner)
    assert again.status_code == 200
    assert again.json()["data"]["id"] == job["id"]
    assert len(enq.ids) == 1  # not re-published

    polled = await client.get(f"{JOBS}/{job['id']}", headers=owner)
    assert polled.status_code == 200 and polled.json()["data"]["status"] == "QUEUED"
    listed = await client.get(JOBS, headers=owner)
    assert [j["id"] for j in listed.json()["data"]["items"]] == [job["id"]]


async def test_idempotency_key_reuse_for_different_request_conflicts(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    app.dependency_overrides[get_job_enqueuer] = lambda: RecordingEnqueuer()
    owner = await _user(client, db_session, "jobowner2")
    doc_id = await _upload(client, owner)
    hdrs = {**owner, "Idempotency-Key": "client-key-1"}
    assert (
        await client.post(JOBS, json={"document_id": doc_id, "document_type": "invoice"}, headers=hdrs)
    ).status_code == 202
    res = await client.post(JOBS, json={"document_id": doc_id, "document_type": "receipt"}, headers=hdrs)
    assert res.status_code == 409


async def test_other_users_cannot_see_or_submit_for_a_document(client: AsyncClient, db_session: AsyncSession) -> None:
    app.dependency_overrides[get_job_enqueuer] = lambda: RecordingEnqueuer()
    owner = await _user(client, db_session, "jobowner3")
    intruder = await _user(client, db_session, "intruder3")
    doc_id = await _upload(client, owner)
    job_id = (await client.post(JOBS, json={"document_id": doc_id}, headers=owner)).json()["data"]["id"]

    assert (await client.get(f"{JOBS}/{job_id}", headers=intruder)).status_code == 404
    assert (await client.post(JOBS, json={"document_id": doc_id}, headers=intruder)).status_code == 404


async def test_unreachable_queue_fails_closed_and_persists_failure(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    app.dependency_overrides[get_job_enqueuer] = lambda: RecordingEnqueuer(ConnectionError("redis down"))
    owner = await _user(client, db_session, "jobowner4")
    doc_id = await _upload(client, owner)

    res = await client.post(JOBS, json={"document_id": doc_id}, headers=owner)
    assert res.status_code == 503
    assert res.json()["errors"]["error_code"] == "QUEUE_UNAVAILABLE"
    job = (await db_session.execute(select(ProcessingJob))).scalar_one()
    assert job.status == "FAILED" and job.error_code == "QUEUE_UNAVAILABLE"


async def test_missing_redis_url_refuses_to_enqueue(
    client: AsyncClient, db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "REDIS_URL", None)
    owner = await _user(client, db_session, "jobowner5")
    doc_id = await _upload(client, owner)
    res = await client.post(JOBS, json={"document_id": doc_id}, headers=owner)
    assert res.status_code == 503
    assert res.json()["errors"]["error_code"] == "QUEUE_UNAVAILABLE"


async def test_failed_list_is_admin_only_and_retry_requeues(client: AsyncClient, db_session: AsyncSession) -> None:
    enq = RecordingEnqueuer()
    app.dependency_overrides[get_job_enqueuer] = lambda: enq
    owner = await _user(client, db_session, "jobowner6")
    admin = await _user(client, db_session, "jobadmin6", role="admin")
    doc_id = await _upload(client, owner)
    job_id = (await client.post(JOBS, json={"document_id": doc_id}, headers=owner)).json()["data"]["id"]

    assert (await client.post(f"{JOBS}/{job_id}/retry", headers=owner)).status_code == 409  # still QUEUED

    job = await db_session.get(ProcessingJob, uuid.UUID(job_id))
    assert job is not None
    job.status, job.error_code, job.attempts = "FAILED", "LLM_TIMEOUT", 4
    await db_session.commit()

    assert (await client.get(f"{JOBS}/failed", headers=owner)).status_code == 403
    failed = (await client.get(f"{JOBS}/failed", headers=admin)).json()["data"]["items"]
    assert [(j["id"], j["error_code"]) for j in failed] == [(job_id, "LLM_TIMEOUT")]

    retried = await client.post(f"{JOBS}/{job_id}/retry", headers=owner)
    assert retried.status_code == 202
    assert retried.json()["data"]["status"] == "QUEUED" and retried.json()["data"]["attempts"] == 0
    assert enq.ids.count(uuid.UUID(job_id)) == 2


# --------------------------------------------------------------------------- runner


async def _queued_job(client: AsyncClient, db_session: AsyncSession, name: str) -> uuid.UUID:
    app.dependency_overrides[get_job_enqueuer] = lambda: RecordingEnqueuer()
    owner = await _user(client, db_session, name)
    doc_id = await _upload(client, owner)
    res = await client.post(JOBS, json={"document_id": doc_id, "document_type": "invoice"}, headers=owner)
    return uuid.UUID(res.json()["data"]["id"])


async def _job(db_session: AsyncSession, job_id: uuid.UUID) -> ProcessingJob:
    db_session.expire_all()
    job = await db_session.get(ProcessingJob, job_id)
    assert job is not None
    return job


async def test_runner_completes_grounded_extraction(client: AsyncClient, db_session: AsyncSession) -> None:
    job_id = await _queued_job(client, db_session, "runner1")
    status = await execute_job(job_id, app_session.AsyncSessionLocal, _deps(CONTOSO_INVOICE_JSON), final_attempt=False)
    assert status == "COMPLETED"
    job = await _job(db_session, job_id)
    assert (job.status, job.attempts, job.error_code) == ("COMPLETED", 1, None)
    assert job.completed_at is not None


async def test_runner_transient_failure_schedules_retry_then_fails_on_last_attempt(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    job_id = await _queued_job(client, db_session, "runner2")
    with pytest.raises(RetryJob) as info:
        await execute_job(job_id, app_session.AsyncSessionLocal, _deps(RATE_LIMITED), final_attempt=False)
    assert info.value.error_code == "LLM_RATE_LIMITED"
    job = await _job(db_session, job_id)
    assert (job.status, job.error_code, job.attempts) == ("RETRYING", "LLM_RATE_LIMITED", 1)

    status = await execute_job(job_id, app_session.AsyncSessionLocal, _deps(RATE_LIMITED), final_attempt=True)
    assert status == "FAILED"
    job = await _job(db_session, job_id)
    assert (job.status, job.error_code, job.attempts) == ("FAILED", "LLM_RATE_LIMITED", 2)


async def test_runner_permanent_failure_is_not_retried(client: AsyncClient, db_session: AsyncSession) -> None:
    job_id = await _queued_job(client, db_session, "runner3")
    deps = _deps(LLMError(ErrorCode.LLM_AUTH_FAILED))
    assert await execute_job(job_id, app_session.AsyncSessionLocal, deps, final_attempt=False) == "FAILED"
    job = await _job(db_session, job_id)
    assert job.error_code == "LLM_AUTH_FAILED" and job.last_error


async def test_runner_redelivery_of_finished_job_is_a_noop(client: AsyncClient, db_session: AsyncSession) -> None:
    job_id = await _queued_job(client, db_session, "runner4")
    await execute_job(job_id, app_session.AsyncSessionLocal, _deps(CONTOSO_INVOICE_JSON), final_attempt=False)
    deps = _deps(CONTOSO_INVOICE_JSON)
    assert await execute_job(job_id, app_session.AsyncSessionLocal, deps, final_attempt=False) == "COMPLETED"
    assert deps.llm_provider.calls == []  # type: ignore[attr-defined]
    assert (await _job(db_session, job_id)).attempts == 1


# --------------------------------------------------------------------------- Celery eager mode


def test_celery_task_retries_transient_errors_in_eager_mode(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Two rate limits then success: the real task retries via Celery and the job ends COMPLETED."""
    db_url = f"sqlite+aiosqlite:///{(tmp_path / 'jobs.db').as_posix()}"
    storage = LocalStorageProvider(base_directory=str(tmp_path / "files"))

    async def seed() -> uuid.UUID:
        engine = create_async_engine(db_url)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        stored, rel, abs_path = await storage.save(png_bytes(), "inv.png")
        async with async_sessionmaker(engine, expire_on_commit=False)() as db:
            user = User(email="e@example.com", username="eager", hashed_password="x")
            db.add(user)
            await db.flush()
            doc = Document(
                owner_id=user.id,
                original_filename="inv.png",
                stored_filename=stored,
                relative_path=rel,
                absolute_path=abs_path,
                file_extension=".png",
                mime_type="image/png",
                file_size=1,
                sha256_hash="0" * 64,
            )
            db.add(doc)
            await db.flush()
            job = ProcessingJob(document_id=doc.id, document_type="invoice", status="QUEUED", max_attempts=4)
            db.add(job)
            await db.commit()
            job_id = job.id
        await engine.dispose()
        return job_id

    async def load(job_id: uuid.UUID) -> ProcessingJob:
        engine = create_async_engine(db_url)
        async with async_sessionmaker(engine, expire_on_commit=False)() as db:
            job = await db.get(ProcessingJob, job_id)
        await engine.dispose()
        assert job is not None
        return job

    job_id = asyncio.run(seed())
    llm = FakeLLMProvider(RATE_LIMITED, RATE_LIMITED, CONTOSO_INVOICE_JSON)
    deps = JobDependencies(OCRPipeline(ocr_provider=FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)), llm, storage)
    monkeypatch.setattr(settings, "DATABASE_URL", db_url)
    monkeypatch.setattr(tasks, "build_dependencies", lambda: deps)
    monkeypatch.setattr(tasks, "retry_delay", lambda *_: 0)
    # Celery's Settings object does not support monkeypatch's setattr/delattr undo; restore explicitly.
    previous = celery_app.conf.task_always_eager
    celery_app.conf.task_always_eager = True
    try:
        tasks.run_extraction.apply(args=[str(job_id)])
    finally:
        celery_app.conf.task_always_eager = previous

    job = asyncio.run(load(job_id))
    assert (job.status, job.attempts, job.error_code) == ("COMPLETED", 3, None)
    assert len(llm.calls) == 3


def test_retry_delay_honours_retry_after_and_caps_backoff() -> None:
    assert tasks.retry_delay(0, 90) >= 90
    assert tasks.BACKOFF_BASE_SECONDS <= tasks.retry_delay(0, None) <= 2 * tasks.BACKOFF_BASE_SECONDS
    assert tasks.retry_delay(20, None) <= tasks.BACKOFF_CAP_SECONDS + tasks.BACKOFF_BASE_SECONDS


def test_celery_reliability_settings() -> None:
    conf = celery_app.conf
    assert conf.task_acks_late and conf.task_reject_on_worker_lost
    assert conf.worker_prefetch_multiplier == 1
    assert conf.task_serializer == "json" and conf.accept_content == ["json"]
    assert conf.broker_transport_options["visibility_timeout"] >= 3600
    assert tasks.run_extraction.max_retries == 3


# --------------------------------------------------------------------------- Redis integration


@pytest.mark.skipif(not os.environ.get("REDIS_URL"), reason="needs a Redis server (REDIS_URL)")
def test_enqueue_publishes_to_redis(monkeypatch: pytest.MonkeyPatch) -> None:
    import redis

    from app.services.job_service import celery_enqueuer

    url = os.environ["REDIS_URL"]
    monkeypatch.setattr(settings, "REDIS_URL", url)
    celery_app.conf.broker_url = url
    client = redis.Redis.from_url(url)
    client.delete("extraction")
    job_id = uuid.uuid4()
    celery_enqueuer(job_id)
    messages = client.lrange("extraction", 0, -1)
    assert len(messages) == 1 and str(job_id).encode() in messages[0]
    client.delete("extraction")


def test_job_status_values_are_the_documented_set() -> None:
    assert {s.value for s in JobStatus} == {"QUEUED", "RUNNING", "RETRYING", "COMPLETED", "NEEDS_REVIEW", "FAILED"}
