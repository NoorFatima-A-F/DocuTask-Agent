"""
Unit and integration tests for AIExtractionService business logic layer.
"""

import io
import shutil
import tempfile
from PIL import Image
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import ExtractionRequest
from app.ocr.pipeline import OCRPipeline
from app.ocr.providers.tesseract import TesseractOCRProvider
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.document_repository import DocumentRepository
from app.repositories.extracted_text_repository import ExtractedTextRepository
from app.repositories.user_repository import UserRepository
from app.services.ai_extraction_service import AIExtractionService
from app.services.document_service import DocumentService
from app.services.ocr_service import OCRService
from app.storage.local import LocalStorageProvider


@pytest.fixture
def temp_storage_dir():
    """Temporary storage directory fixture."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.asyncio
async def test_ai_extraction_service_workflow(db_session: AsyncSession, temp_storage_dir: str):
    """Tests AIExtractionService full extraction, caching, and history workflow."""
    user_repo = UserRepository(db_session)
    doc_repo = DocumentRepository(db_session)
    text_repo = ExtractedTextRepository(db_session)
    ai_repo = AIExtractionRepository(db_session)
    storage = LocalStorageProvider(base_directory=temp_storage_dir)

    doc_service = DocumentService(document_repo=doc_repo, storage_provider=storage)
    ocr_pipeline = OCRPipeline(ocr_provider=TesseractOCRProvider())
    ocr_service = OCRService(
        document_repo=doc_repo,
        extracted_text_repo=text_repo,
        storage_provider=storage,
        ocr_pipeline=ocr_pipeline
    )
    ai_service = AIExtractionService(
        document_repo=doc_repo,
        ai_extraction_repo=ai_repo,
        ocr_service=ocr_service
    )

    user = await user_repo.create({"email": "ai_user@example.com", "username": "aiuser", "hashed_password": "p"})

    # Upload test document
    img = Image.new("RGB", (100, 50), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    up_res = await doc_service.upload_document(buf.getvalue(), "invoice.png", "image/png", user)
    doc_id = up_res.document.id

    # 1. Trigger extraction
    req = ExtractionRequest(document_type="invoice", force_reextract=False)
    res = await ai_service.extract_structured_data(doc_id, user, req)

    assert res.metadata.document_id == doc_id
    assert res.metadata.document_type == "invoice"
    assert res.metadata.provider == "gemini"
    assert "structured_json" in res.result.model_dump()

    # 2. Check extraction status
    status_data = await ai_service.get_extraction_status(doc_id, user)
    assert status_data["status"] == "EXTRACTION_COMPLETED"
    assert status_data["has_extraction"] is True

    # 3. Retrieve latest result (Cached)
    latest = await ai_service.get_latest_result(doc_id, user)
    assert latest.id == res.id

    # 4. Retrieve extraction history
    history = await ai_service.get_extraction_history(doc_id, user)
    assert len(history) >= 1
