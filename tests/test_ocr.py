"""OCR subsystem: detector, preprocessor, Tesseract provider failure typing, pipeline, service, API."""

from __future__ import annotations

import io
import shutil
import tempfile
from collections.abc import Iterator

import pytesseract
import pytest
from httpx import AsyncClient
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors.extraction import ErrorCode, OCRError
from app.dependencies.ocr import get_ocr_pipeline
from app.main import app
from app.models.document import Document
from app.ocr.detector import DocumentTypeDetector
from app.ocr.exceptions import CorruptedDocumentException
from app.ocr.pipeline import OCRPipeline
from app.ocr.preprocessor import ImagePreprocessor
from app.ocr.providers.tesseract import TesseractOCRProvider, word_confidence
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.user_repository import UserRepository
from app.services.document_service import DocumentService
from app.services.ocr_service import OCRService
from app.storage.local import LocalStorageProvider
from tests.fakes.data import CONTOSO_INVOICE_TEXT, png_bytes
from tests.fakes.ocr import FakeOCRProvider


@pytest.fixture
def temp_storage_dir() -> Iterator[str]:
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_document_type_detector() -> None:
    assert DocumentTypeDetector.detect_type(b"plain text", ".txt", "text/plain") == "txt"
    assert DocumentTypeDetector.detect_type(png_bytes(10, 10), ".png", "image/png") == "image"
    assert DocumentTypeDetector.detect_type(b"fake pdf content", ".pdf", "application/pdf") == "scanned_pdf"


def test_image_preprocessor() -> None:
    processed = ImagePreprocessor.preprocess_image(Image.new("RGB", (50, 50), color="red"))
    assert processed.mode == "L"


# ------------------------------------------------------------------ Tesseract provider


async def test_missing_tesseract_binary_is_engine_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a, **_k):
        raise pytesseract.TesseractNotFoundError()

    monkeypatch.setattr(pytesseract, "image_to_string", boom)
    with pytest.raises(OCRError) as exc_info:
        await TesseractOCRProvider().extract_page(png_bytes())
    assert exc_info.value.code == ErrorCode.OCR_ENGINE_UNAVAILABLE
    assert exc_info.value.status_code == 503


async def test_tesseract_error_is_ocr_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_a, **_k):
        raise pytesseract.TesseractError(1, "bad lang")

    monkeypatch.setattr(pytesseract, "image_to_string", boom)
    with pytest.raises(OCRError) as exc_info:
        await TesseractOCRProvider().extract_page(png_bytes(), language="zzz")
    assert exc_info.value.code == ErrorCode.OCR_FAILED


async def test_successful_page_uses_word_confidences(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pytesseract, "image_to_string", lambda *_a, **_k: "Total 42.10\n")
    monkeypatch.setattr(
        pytesseract,
        "image_to_data",
        lambda *_a, **_k: {"text": ["", "Total", "42.10"], "conf": ["-1", "90", "80"]},
    )
    page = await TesseractOCRProvider().extract_page(png_bytes(), page_number=3)
    assert (page.page_number, page.text, page.confidence) == (3, "Total 42.10", 0.85)


async def test_corrupted_image_raises_corrupted_document() -> None:
    with pytest.raises(CorruptedDocumentException):
        await TesseractOCRProvider().extract_page(b"not an image")


def test_word_confidence_is_none_without_words() -> None:
    assert word_confidence({"text": ["", " "], "conf": ["-1", "-1"]}) is None
    assert word_confidence({}) is None


def test_provider_supports_formats() -> None:
    provider = TesseractOCRProvider()
    assert provider.supports(".png") and not provider.supports(".exe")


# ------------------------------------------------------------------ pipeline


async def test_pipeline_blank_page_raises_no_text() -> None:
    import uuid

    pipeline = OCRPipeline(ocr_provider=FakeOCRProvider(text=""))
    with pytest.raises(OCRError) as exc_info:
        await pipeline.process(uuid.uuid4(), png_bytes(), ".png", "image/png")
    assert exc_info.value.code == ErrorCode.OCR_NO_TEXT


async def test_pipeline_confidence_none_when_engine_reports_none() -> None:
    import uuid

    pipeline = OCRPipeline(ocr_provider=FakeOCRProvider(text="hello", confidence=None))
    content = await pipeline.process(uuid.uuid4(), png_bytes(), ".png", "image/png")
    assert content.average_confidence is None


# ------------------------------------------------------------------ service


async def _service_with(db: AsyncSession, storage_dir: str, ocr: FakeOCRProvider):
    storage = LocalStorageProvider(base_directory=storage_dir)
    doc_repo = DocumentRepository(db)
    service = OCRService(
        document_repo=doc_repo,
        extracted_text_repo=ExtractedTextRepository(db),
        storage_provider=storage,
        ocr_pipeline=OCRPipeline(ocr_provider=ocr),
    )
    user = await UserRepository(db).create({"email": "ocr@example.com", "username": "ocruser", "hashed_password": "p"})
    up = await DocumentService(document_repo=doc_repo, storage_provider=storage).upload_document(
        png_bytes(), "scan.png", "image/png", user
    )
    return service, user, up.document.id


async def test_ocr_service_full_workflow(db_session: AsyncSession, temp_storage_dir: str) -> None:
    ocr = FakeOCRProvider(text=CONTOSO_INVOICE_TEXT, confidence=0.9)
    service, user, doc_id = await _service_with(db_session, temp_storage_dir, ocr)

    content = await service.extract_text_for_document(doc_id, user)
    assert content.page_count == 1 and "Contoso Ltd" in content.text and content.average_confidence == 0.9

    status = await service.get_ocr_status(doc_id, user)
    assert status["status"] == "OCR_COMPLETED" and status["has_extracted_text"] is True

    cached = await service.get_extracted_text(doc_id, user)
    assert cached.text == content.text and ocr.calls == 1

    await service.extract_text_for_document(doc_id, user, force_reextract=True)
    assert ocr.calls == 2


async def test_ocr_service_failure_marks_document_failed(db_session: AsyncSession, temp_storage_dir: str) -> None:
    ocr = FakeOCRProvider(error=OCRError(ErrorCode.OCR_ENGINE_UNAVAILABLE))
    service, user, doc_id = await _service_with(db_session, temp_storage_dir, ocr)

    with pytest.raises(OCRError):
        await service.extract_text_for_document(doc_id, user)

    doc = await db_session.get(Document, doc_id)
    assert doc is not None and doc.upload_status == "OCR_FAILED"
    assert await ExtractedTextRepository(db_session).get_document_text(doc_id) == []


async def test_ocr_api_endpoints(client: AsyncClient) -> None:
    app.dependency_overrides[get_ocr_pipeline] = lambda: OCRPipeline(
        ocr_provider=FakeOCRProvider(text=CONTOSO_INVOICE_TEXT)
    )
    reg = await client.post(
        "/api/v1/auth/register",
        json={"email": "ocr_api_user@example.com", "username": "ocrapiuser", "password": "Password123!"},
    )
    assert reg.status_code == 201
    login = await client.post(
        "/api/v1/auth/login", json={"username_or_email": "ocrapiuser", "password": "Password123!"}
    )
    headers = {"Authorization": f"Bearer {login.json()['data']['access_token']}"}

    buf = io.BytesIO(png_bytes())
    up = await client.post(
        "/api/v1/documents/upload", files={"file": ("receipt.png", buf.getvalue(), "image/png")}, headers=headers
    )
    doc_id = up.json()["data"]["document"]["id"]

    ext = await client.post(f"/api/v1/ocr/extract/{doc_id}?language=eng", headers=headers)
    assert ext.status_code == 200 and "Contoso Ltd" in ext.json()["data"]["text"]
    assert (await client.get(f"/api/v1/ocr/text/{doc_id}", headers=headers)).status_code == 200
    assert len((await client.get(f"/api/v1/ocr/pages/{doc_id}", headers=headers)).json()["data"]) == 1
    status = await client.get(f"/api/v1/ocr/status/{doc_id}", headers=headers)
    assert status.json()["data"]["status"] == "OCR_COMPLETED"
