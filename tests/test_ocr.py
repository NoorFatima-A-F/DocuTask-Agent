"""
Unit and Integration Tests for OCR Subsystem (OCR Engine & Text Extraction Pipeline).
"""

import io
import shutil
import tempfile
from PIL import Image
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.ocr.detector import DocumentTypeDetector
from app.ocr.pipeline import OCRPipeline
from app.ocr.preprocessor import ImagePreprocessor
from app.ocr.providers.tesseract import TesseractOCRProvider
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.user_repository import UserRepository
from app.services.document_service import DocumentService
from app.services.ocr_service import OCRService
from app.storage.local import LocalStorageProvider


@pytest.fixture
def temp_storage_dir():
    """Temporary storage fixture."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_document_type_detector():
    """Verifies DocumentTypeDetector format classification logic."""
    # 1. TXT
    assert DocumentTypeDetector.detect_type(b"plain text", ".txt", "text/plain") == "txt"

    # 2. Image
    img = Image.new("RGB", (10, 10), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    assert DocumentTypeDetector.detect_type(buf.getvalue(), ".png", "image/png") == "image"

    # 3. Scanned PDF fallback for empty/binary
    assert DocumentTypeDetector.detect_type(b"fake pdf content", ".pdf", "application/pdf") == "scanned_pdf"


def test_image_preprocessor():
    """Verifies ImagePreprocessor image transformations."""
    img = Image.new("RGB", (50, 50), color="red")
    processed = ImagePreprocessor.preprocess_image(img)
    assert processed is not None
    assert processed.mode == "L"  # Grayscale


@pytest.mark.asyncio
async def test_ocr_provider_methods():
    """Verifies TesseractOCRProvider execution, health check, and confidence metrics."""
    provider = TesseractOCRProvider()
    assert await provider.health_check() is True
    assert provider.supports(".png") is True
    assert provider.supports(".exe") is False

    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    text = await provider.extract_text(img_bytes, language="eng")
    assert isinstance(text, str)

    confidence = await provider.get_confidence(img_bytes)
    assert 0.0 <= confidence <= 1.0


@pytest.mark.asyncio
async def test_ocr_service_full_workflow(db_session: AsyncSession, temp_storage_dir: str):
    """Tests OCRService full workflow, status transitions, and caching."""
    user_repo = UserRepository(db_session)
    doc_repo = DocumentRepository(db_session)
    text_repo = ExtractedTextRepository(db_session)
    storage = LocalStorageProvider(base_directory=temp_storage_dir)

    doc_service = DocumentService(document_repo=doc_repo, storage_provider=storage)
    ocr_pipeline = OCRPipeline(ocr_provider=TesseractOCRProvider())
    ocr_service = OCRService(
        document_repo=doc_repo,
        extracted_text_repo=text_repo,
        storage_provider=storage,
        ocr_pipeline=ocr_pipeline
    )

    user = await user_repo.create({"email": "ocr_user@example.com", "username": "ocruser", "hashed_password": "p"})

    # Upload test image document
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    up_res = await doc_service.upload_document(buf.getvalue(), "scan.png", "image/png", user)
    doc_id = up_res.document.id

    # 1. Trigger extraction
    content1 = await ocr_service.extract_text_for_document(doc_id, user, force_reextract=False, language="eng")
    assert content1.document_id == doc_id
    assert content1.page_count == 1
    assert content1.average_confidence >= 0.0

    # 2. Check OCR status
    status_data = await ocr_service.get_ocr_status(doc_id, user)
    assert status_data["status"] == "OCR_COMPLETED"
    assert status_data["page_count"] == 1
    assert status_data["has_extracted_text"] is True

    # 3. Retrieve cached text
    cached_content = await ocr_service.get_extracted_text(doc_id, user)
    assert cached_content.document_id == doc_id
    assert cached_content.page_count == 1

    # 4. Force re-extraction
    content_re = await ocr_service.extract_text_for_document(doc_id, user, force_reextract=True)
    assert content_re.document_id == doc_id


@pytest.mark.asyncio
async def test_ocr_api_endpoints(client: AsyncClient):
    """Verifies OCR HTTP endpoints via AsyncClient."""
    # 1. Register & Login User
    reg = await client.post("/api/v1/auth/register", json={
        "email": "ocr_api_user@example.com",
        "username": "ocrapiuser",
        "password": "Password123!"
    })
    assert reg.status_code == 201

    login = await client.post("/api/v1/auth/login", json={
        "username_or_email": "ocrapiuser",
        "password": "Password123!"
    })
    token = login.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload Document
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    files = {"file": ("receipt.png", buf.getvalue(), "image/png")}
    up_res = await client.post("/api/v1/documents/upload", files=files, headers=headers)
    assert up_res.status_code == 201
    doc_id = up_res.json()["data"]["document"]["id"]

    # 3. POST /ocr/extract/{document_id}
    ext_res = await client.post(f"/api/v1/ocr/extract/{doc_id}?language=eng", headers=headers)
    assert ext_res.status_code == 200
    body = ext_res.json()
    assert body["success"] is True
    assert body["data"]["document_id"] == doc_id

    # 4. GET /ocr/text/{document_id}
    text_res = await client.get(f"/api/v1/ocr/text/{doc_id}", headers=headers)
    assert text_res.status_code == 200
    assert text_res.json()["data"]["document_id"] == doc_id

    # 5. GET /ocr/pages/{document_id}
    pages_res = await client.get(f"/api/v1/ocr/pages/{doc_id}", headers=headers)
    assert pages_res.status_code == 200
    assert len(pages_res.json()["data"]) >= 1

    # 6. GET /ocr/status/{document_id}
    status_res = await client.get(f"/api/v1/ocr/status/{doc_id}", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["data"]["status"] == "OCR_COMPLETED"
