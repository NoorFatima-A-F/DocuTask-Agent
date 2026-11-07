"""Extraction pipeline (OCR -> LLM -> validation -> persistence) with injected fakes.

These tests replace the old ones that passed only because the app fabricated data.
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import ExtractionRequest
from app.core.errors.extraction import ErrorCode, LLMError, OCRError
from app.core.exceptions import ResourceNotFoundException, ValidationAppException
from app.dependencies.llm import get_llm_provider
from app.dependencies.ocr import get_ocr_pipeline
from app.main import app
from app.models.ai_extraction import AIExtraction
from app.models.document import Document
from app.ocr.pipeline import OCRPipeline
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.user_repository import UserRepository
from app.services.ai_extraction_service import AIExtractionService
from app.services.document_service import DocumentService
from app.services.ocr_service import OCRService
from app.storage.local import LocalStorageProvider
from tests.fakes.data import CONTOSO_INVOICE_JSON, CONTOSO_INVOICE_TEXT, png_bytes
from tests.fakes.llm import FakeLLMProvider
from tests.fakes.ocr import FakeOCRProvider


@pytest.fixture
def storage_dir() -> Iterator[str]:
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path, ignore_errors=True)


@dataclass
class Env:
    db: AsyncSession
    service: AIExtractionService
    llm: FakeLLMProvider
    ocr: FakeOCRProvider
    user: Any
    doc_id: Any
    sleeps: list[float]


async def make_env(
    db: AsyncSession,
    storage_dir: str,
    *script: Any,
    ocr: FakeOCRProvider | None = None,
    username: str = "pipeline",
) -> Env:
    storage = LocalStorageProvider(base_directory=storage_dir)
    doc_repo = DocumentRepository(db)
    ocr = ocr or FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)
    ocr_service = OCRService(
        document_repo=doc_repo,
        extracted_text_repo=ExtractedTextRepository(db),
        storage_provider=storage,
        ocr_pipeline=OCRPipeline(ocr_provider=ocr),
    )
    llm = FakeLLMProvider(*(script or (CONTOSO_INVOICE_JSON,)))
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    service = AIExtractionService(
        document_repo=doc_repo,
        ai_extraction_repo=AIExtractionRepository(db),
        ocr_service=ocr_service,
        llm_provider=llm,
        sleep=fake_sleep,
    )
    user = await UserRepository(db).create(
        {"email": f"{username}@example.com", "username": username, "hashed_password": "p"}
    )
    uploaded = await DocumentService(document_repo=doc_repo, storage_provider=storage).upload_document(
        png_bytes(), "invoice.png", "image/png", user
    )
    return Env(db, service, llm, ocr, user, uploaded.document.id, sleeps)


async def extraction_rows(db: AsyncSession, doc_id: Any) -> list[AIExtraction]:
    result = await db.execute(select(AIExtraction).where(AIExtraction.document_id == doc_id))
    return list(result.scalars().all())


INVOICE = ExtractionRequest(document_type="invoice")
FORCE = ExtractionRequest(document_type="invoice", force_reextract=True)


async def test_success_persists_real_llm_output(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir)

    res = await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert res.result.status == "COMPLETED"
    assert res.result.structured_json["vendor_name"] == "Contoso Ltd"
    assert res.result.structured_json["total_amount"] == 42.10
    assert res.statistics.input_tokens == 100  # from the provider, not len(text)//4
    assert res.statistics.estimated_cost is None  # unknown pricing is not guessed
    assert CONTOSO_INVOICE_TEXT.strip() in env.llm.calls[0]["prompt"]


async def test_cache_returns_success_and_force_reruns(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir)
    first = await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)
    cached = await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)
    forced = await env.service.extract_structured_data(env.doc_id, env.user, FORCE)

    assert cached.id == first.id
    assert forced.id != first.id
    assert len(env.llm.calls) == 2


async def test_failed_record_is_never_served_from_cache(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir, LLMError(ErrorCode.LLM_AUTH_FAILED), CONTOSO_INVOICE_JSON)
    with pytest.raises(LLMError):
        await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    retry = await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert retry.result.status == "COMPLETED"
    assert len(env.llm.calls) == 2


@pytest.mark.parametrize(
    "code", [ErrorCode.LLM_NOT_CONFIGURED, ErrorCode.LLM_AUTH_FAILED, ErrorCode.LLM_MODEL_NOT_FOUND]
)
async def test_permanent_llm_errors_fail_without_retry(
    db_session: AsyncSession, storage_dir: str, code: ErrorCode
) -> None:
    env = await make_env(db_session, storage_dir, LLMError(code))

    with pytest.raises(LLMError) as exc_info:
        await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert exc_info.value.code == code
    assert len(env.llm.calls) == 1
    rows = await extraction_rows(db_session, env.doc_id)
    assert [(r.status, r.error_code, r.structured_json, r.confidence) for r in rows] == [
        ("FAILED", code.value, None, None)
    ]
    doc = await db_session.get(Document, env.doc_id)
    assert doc is not None and doc.upload_status == "EXTRACTION_FAILED"


async def test_transient_error_retried_with_backoff_then_succeeds(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(
        db_session,
        storage_dir,
        LLMError(ErrorCode.LLM_RATE_LIMITED, retry_after=7),
        LLMError(ErrorCode.LLM_UNAVAILABLE),
        CONTOSO_INVOICE_JSON,
    )

    res = await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert res.result.status == "COMPLETED"
    assert len(env.llm.calls) == 3
    assert 7 <= env.sleeps[0] <= 8  # honours Retry-After (+ jitter)
    assert 2 <= env.sleeps[1] <= 3  # exponential: base * 2**1 (+ jitter)


async def test_transient_error_gives_up_after_three_attempts(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir, LLMError(ErrorCode.LLM_TIMEOUT))

    with pytest.raises(LLMError) as exc_info:
        await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert exc_info.value.code == ErrorCode.LLM_TIMEOUT
    assert len(env.llm.calls) == 3
    assert (await extraction_rows(db_session, env.doc_id))[0].status == "FAILED"


async def test_schema_invalid_output_retries_with_corrective_prompt(
    db_session: AsyncSession, storage_dir: str
) -> None:
    bad = {"line_items": [{"quantity": 1}]}  # missing required description
    env = await make_env(db_session, storage_dir, bad, CONTOSO_INVOICE_JSON)

    res = await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert res.result.status == "COMPLETED"
    assert res.statistics.retry_count == 1
    assert "CORRECTION REQUIRED" in env.llm.calls[1]["prompt"]


async def test_schema_invalid_output_fails_after_two_corrections(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir, LLMError(ErrorCode.LLM_INVALID_OUTPUT))

    with pytest.raises(LLMError) as exc_info:
        await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert exc_info.value.code == ErrorCode.LLM_INVALID_OUTPUT
    assert len(env.llm.calls) == 3  # 1 + MAX_SCHEMA_RETRIES
    row = (await extraction_rows(db_session, env.doc_id))[0]
    assert row.status == "FAILED" and row.structured_json is None


async def test_ocr_engine_missing_fails_typed_and_stores_no_text(db_session: AsyncSession, storage_dir: str) -> None:
    ocr = FakeOCRProvider(error=OCRError(ErrorCode.OCR_ENGINE_UNAVAILABLE))
    env = await make_env(db_session, storage_dir, ocr=ocr)

    with pytest.raises(OCRError) as exc_info:
        await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert exc_info.value.code == ErrorCode.OCR_ENGINE_UNAVAILABLE
    assert env.llm.calls == []
    assert await ExtractedTextRepository(db_session).get_document_text(env.doc_id) == []
    row = (await extraction_rows(db_session, env.doc_id))[0]
    assert (row.status, row.error_code) == ("FAILED", "OCR_ENGINE_UNAVAILABLE")


async def test_empty_ocr_text_is_not_sent_to_llm(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir, ocr=FakeOCRProvider(text="   "))

    with pytest.raises(OCRError) as exc_info:
        await env.service.extract_structured_data(env.doc_id, env.user, INVOICE)

    assert exc_info.value.code == ErrorCode.OCR_NO_TEXT
    assert env.llm.calls == []


async def test_unsupported_provider_override_rejected(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir)
    with pytest.raises(ValidationAppException):
        await env.service.extract_structured_data(
            env.doc_id, env.user, ExtractionRequest(document_type="invoice", provider="openai")
        )


async def test_other_users_document_is_not_found(db_session: AsyncSession, storage_dir: str) -> None:
    env = await make_env(db_session, storage_dir)
    other = await UserRepository(db_session).create(
        {"email": "other@example.com", "username": "other", "hashed_password": "p"}
    )
    with pytest.raises(ResourceNotFoundException):
        await env.service.extract_structured_data(env.doc_id, other, INVOICE)
    with pytest.raises(ResourceNotFoundException):
        await env.service.get_latest_result(env.doc_id, other)


# --------------------------------------------------------------------------- HTTP


async def _login_and_upload(client: AsyncClient, name: str) -> tuple[dict[str, str], str]:
    reg = await client.post(
        "/api/v1/auth/register", json={"email": f"{name}@example.com", "username": name, "password": "Password123!"}
    )
    assert reg.status_code == 201
    login = await client.post("/api/v1/auth/login", json={"username_or_email": name, "password": "Password123!"})
    headers = {"Authorization": f"Bearer {login.json()['data']['access_token']}"}
    up = await client.post(
        "/api/v1/documents/upload", files={"file": ("invoice.png", png_bytes(), "image/png")}, headers=headers
    )
    assert up.status_code == 201
    return headers, up.json()["data"]["document"]["id"]


def _override(llm: FakeLLMProvider, ocr: FakeOCRProvider) -> None:
    app.dependency_overrides[get_llm_provider] = lambda: llm
    app.dependency_overrides[get_ocr_pipeline] = lambda: OCRPipeline(ocr_provider=ocr)


async def test_api_extraction_success_flow(client: AsyncClient) -> None:
    _override(FakeLLMProvider(CONTOSO_INVOICE_JSON), FakeOCRProvider(text=CONTOSO_INVOICE_TEXT))
    headers, doc_id = await _login_and_upload(client, "apiok")

    ext = await client.post(f"/api/v1/ai/extract/{doc_id}", json={"document_type": "invoice"}, headers=headers)
    assert ext.status_code == 200, ext.text
    assert ext.json()["data"]["result"]["structured_json"]["invoice_number"] == "A-7731"

    got = await client.get(f"/api/v1/ai/result/{doc_id}", headers=headers)
    assert got.json()["data"]["result"]["status"] == "COMPLETED"
    status = await client.get(f"/api/v1/ai/status/{doc_id}", headers=headers)
    assert status.json()["data"]["status"] == "EXTRACTION_COMPLETED"
    hist = await client.get(f"/api/v1/ai/history/{doc_id}", headers=headers)
    assert len(hist.json()["data"]) == 1
    deleted = await client.delete(f"/api/v1/ai/result/{doc_id}", headers=headers)
    assert deleted.status_code == 200


async def test_api_no_api_key_returns_503_and_persists_failed_record(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Audit regression: no key used to yield fabricated 'John Doe' data marked COMPLETED."""
    from app.ai.providers.gemini import GeminiProvider

    app.dependency_overrides[get_llm_provider] = lambda: GeminiProvider(api_key="")
    app.dependency_overrides[get_ocr_pipeline] = lambda: OCRPipeline(
        ocr_provider=FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)
    )
    headers, doc_id = await _login_and_upload(client, "nokey")

    ext = await client.post(f"/api/v1/ai/extract/{doc_id}", json={"document_type": "invoice"}, headers=headers)

    assert ext.status_code == 503
    body = ext.json()
    assert body["success"] is False
    assert body["errors"] == {"error_code": "LLM_NOT_CONFIGURED"}
    assert "structured_json" not in ext.text
    assert "John Doe" not in ext.text

    result = await client.get(f"/api/v1/ai/result/{doc_id}", headers=headers)
    data = result.json()["data"]["result"]
    assert (data["status"], data["error_code"], data["structured_json"], data["confidence"]) == (
        "FAILED",
        "LLM_NOT_CONFIGURED",
        None,
        None,
    )


async def test_api_ocr_engine_missing_returns_503(client: AsyncClient) -> None:
    _override(
        FakeLLMProvider(CONTOSO_INVOICE_JSON),
        FakeOCRProvider(error=OCRError(ErrorCode.OCR_ENGINE_UNAVAILABLE)),
    )
    headers, doc_id = await _login_and_upload(client, "noocr")

    ocr = await client.post(f"/api/v1/ocr/extract/{doc_id}", headers=headers)
    assert ocr.status_code == 503
    assert ocr.json()["errors"] == {"error_code": "OCR_ENGINE_UNAVAILABLE"}
    text = await client.get(f"/api/v1/ocr/text/{doc_id}", headers=headers)
    assert text.status_code == 404  # no placeholder text was stored

    ext = await client.post(f"/api/v1/ai/extract/{doc_id}", json={"document_type": "invoice"}, headers=headers)
    assert ext.status_code == 503
    assert ext.json()["errors"] == {"error_code": "OCR_ENGINE_UNAVAILABLE"}
