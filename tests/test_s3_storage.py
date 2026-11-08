"""S3 storage: round trip, confinement to the prefix, config validation, readiness, and the
API/worker split (the worker reads what the API stored, with no shared disk)."""

from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import app.database.session as app_session
from app.api.v1.endpoints.jobs import get_job_enqueuer
from app.core.config import Settings, settings
from app.core.exceptions import ValidationAppException
from app.dependencies.ocr import get_ocr_provider
from app.dependencies.storage import build_storage_provider, get_storage_provider
from app.jobs.runner import JobDependencies, execute_job
from app.main import app
from app.ocr.pipeline import OCRPipeline
from app.storage.s3 import S3StorageProvider
from tests.fakes.data import CONTOSO_INVOICE_JSON, CONTOSO_INVOICE_TEXT, png_bytes
from tests.fakes.llm import FakeLLMProvider
from tests.fakes.ocr import FakeOCRProvider
from tests.fakes.s3 import FakeS3Client
from tests.test_reviews import _user


def _s3(client: FakeS3Client | None = None, bucket: str = "docs") -> S3StorageProvider:
    return S3StorageProvider(bucket, "documents/", client=client or FakeS3Client())


async def test_round_trip_and_delete() -> None:
    fake = FakeS3Client()
    storage = _s3(fake)
    stored, key, location = await storage.save(b"%PDF-1.7 data", "Invoice.PDF")
    assert key.startswith("documents/") and key.endswith(stored) and stored.endswith(".pdf")
    assert location == f"s3://docs/{key}"
    assert fake.objects[("docs", key)]["ServerSideEncryption"] == "AES256"
    assert fake.objects[("docs", key)]["ContentType"] == "application/pdf"
    assert await storage.read(key) == b"%PDF-1.7 data"
    assert await storage.exists(key)
    assert await storage.delete(key) is True
    assert not await storage.exists(key)
    assert await storage.delete(key) is False


async def test_missing_object_raises_the_same_error_as_local_storage() -> None:
    with pytest.raises(ValidationAppException, match="does not exist"):
        await _s3().read("documents/2026/01/01/nope.png")


@pytest.mark.parametrize("key", ["other/secret.png", "documents/../other/secret.png", "/documents/x.png"])
async def test_keys_outside_the_prefix_are_refused(key: str) -> None:
    fake = FakeS3Client()
    fake.objects[("docs", "other/secret.png")] = {"Body": b"secret"}
    storage = _s3(fake)
    with pytest.raises(ValidationAppException, match="Access denied"):
        await storage.read(key)
    assert await storage.exists(key) is False


async def test_check_reports_unreachable_bucket() -> None:
    assert await _s3().check() is None
    problem = await _s3(bucket="missing").check()
    assert problem is not None and "missing" in problem


def test_s3_backend_requires_a_bucket() -> None:
    with pytest.raises(ValidationError, match="S3_BUCKET"):
        Settings(ENVIRONMENT="test", STORAGE_BACKEND="s3")
    assert Settings(ENVIRONMENT="test", STORAGE_BACKEND="s3", S3_BUCKET="b").S3_BUCKET == "b"


def test_backend_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.storage.local import LocalStorageProvider

    assert isinstance(build_storage_provider(), LocalStorageProvider)
    monkeypatch.setattr(settings, "STORAGE_BACKEND", "s3")
    monkeypatch.setattr(settings, "S3_BUCKET", "docs")
    monkeypatch.setattr(settings, "S3_REGION", "us-east-1")
    provider = build_storage_provider()
    assert isinstance(provider, S3StorageProvider) and provider.bucket == "docs"


async def test_readyz_reports_storage_unavailable(client: AsyncClient) -> None:
    app.dependency_overrides[get_ocr_provider] = lambda: FakeOCRProvider()
    app.dependency_overrides[get_storage_provider] = lambda: _s3(bucket="missing")
    res = await client.get("/readyz")
    assert res.status_code == 503
    assert any(r.startswith("STORAGE_UNAVAILABLE") for r in res.json()["reasons"])


async def test_worker_reads_what_the_api_stored_in_s3(client: AsyncClient, db_session: AsyncSession) -> None:
    """API process and worker process share only the bucket (separate provider instances)."""
    bucket = FakeS3Client()
    app.dependency_overrides[get_storage_provider] = lambda: _s3(bucket)
    app.dependency_overrides[get_job_enqueuer] = lambda: lambda job_id: None
    owner = await _user(client, db_session, "s3owner")
    up = await client.post(
        f"{settings.API_V1_STR}/documents/upload", files={"file": ("inv.png", png_bytes(), "image/png")}, headers=owner
    )
    assert up.status_code == 201, up.text
    assert up.json()["data"]["document"]["relative_path"].startswith("documents/")
    doc_id = up.json()["data"]["document"]["id"]
    job = await client.post(
        f"{settings.API_V1_STR}/jobs", json={"document_id": doc_id, "document_type": "invoice"}, headers=owner
    )
    job_id = uuid.UUID(job.json()["data"]["id"])

    worker_deps = JobDependencies(
        ocr_pipeline=OCRPipeline(ocr_provider=FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)),
        llm_provider=FakeLLMProvider(CONTOSO_INVOICE_JSON),
        storage=_s3(bucket),  # a different provider instance, same bucket
    )
    status = await execute_job(job_id, app_session.AsyncSessionLocal, worker_deps, final_attempt=False)
    assert status == "COMPLETED"


async def test_review_download_is_served_from_s3(client: AsyncClient, db_session: AsyncSession) -> None:
    from tests.test_reviews import HALLUCINATED, _extract

    bucket = FakeS3Client()
    app.dependency_overrides[get_storage_provider] = lambda: _s3(bucket)
    owner = await _user(client, db_session, "s3owner2")
    reviewer = await _user(client, db_session, "s3rev2", role="reviewer")
    _, data = await _extract(client, owner, HALLUCINATED)
    res = await client.get(f"{settings.API_V1_STR}/reviews/{data['id']}/document", headers=reviewer)
    assert res.status_code == 200 and res.content == png_bytes()
    assert res.headers["content-type"] == "image/png"
    assert "attachment" in res.headers["content-disposition"]

    bucket.objects.clear()  # object gone -> 404, not 500
    res = await client.get(f"{settings.API_V1_STR}/reviews/{data['id']}/document", headers=reviewer)
    assert res.status_code == 404
