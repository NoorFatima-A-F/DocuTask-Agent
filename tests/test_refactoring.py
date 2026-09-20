"""
Automated Pytest Suite for Enterprise Architecture Refactoring & Infrastructure Hardening.
"""

import pytest
from app.core.security import validate_secret_key_strength
from app.models.vector import DocumentEmbedding
from app.ocr.providers import (
    AzureDocIntelligenceOCRProvider,
    DocumentAIOCRProvider,
    PaddleOCRProvider,
    TesseractOCRProvider,
    TextractOCRProvider,
)


def test_secret_management_validation():
    """Verifies secret key strength validator enforcing >= 32 chars and rejecting weak strings."""
    valid_key = "a_very_secure_and_long_jwt_secret_key_string_32_chars_min"
    assert validate_secret_key_strength(valid_key) is True

    # Short secret rejection
    with pytest.raises(ValueError):
        validate_secret_key_strength("short_key_123")

    # Prohibited key rejection
    with pytest.raises(ValueError):
        validate_secret_key_strength("changeme")


@pytest.mark.asyncio
async def test_ocr_provider_plugin_suite():
    """Verifies pluggable OCR provider strategy implementations."""
    providers = [
        TesseractOCRProvider(),
        DocumentAIOCRProvider(),
        TextractOCRProvider(),
        AzureDocIntelligenceOCRProvider(),
        PaddleOCRProvider()
    ]

    for provider in providers:
        res = await provider.extract_text(b"file_bytes", "test_invoice.pdf")
        assert res["provider"] == provider.provider_name
        assert "confidence_score" in res
        assert "text" in res


def test_vector_search_orm_model():
    """Verifies DocumentEmbedding ORM entity fields."""
    emb = DocumentEmbedding(
        chunk_index=0,
        chunk_text="Invoice Text Chunk",
        embedding_provider="gemini",
        embedding_model="text-embedding-004",
        embedding_dim=768,
        vector_payload="[0.12, 0.45, -0.89]"
    )
    assert emb.embedding_provider == "gemini"
    assert emb.embedding_dim == 768
