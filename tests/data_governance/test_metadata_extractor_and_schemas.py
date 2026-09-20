"""Test Metadata Extractor & 4-Dimensional Metadata Schemas."""

import pytest
from app.data_governance.metadata.extractor import MetadataExtractor
from app.data_governance.metadata.manager import MetadataManager
from app.data_governance.registry.models import ClassificationLevel


def test_4d_metadata_extraction_and_management():
    """Verify technical, business, AI, and compliance metadata extraction."""
    extractor = MetadataExtractor()
    manager = MetadataManager()

    content = "Contract agreement between Alpha Corp and Beta LLC regarding AI model licenses."

    ai_context = {
        "embedding_model": "text-embedding-3-large",
        "embedding_dimensions": 3072,
        "model_version": "gemini-2.5-flash",
        "agent_id": "contract_analyzer_agent",
        "confidence_score": 0.98,
    }

    metadata = extractor.extract_from_content(
        asset_id="asset_contract_meta_1",
        content=content,
        owner_id="user_legal_head",
        department="Legal",
        location_uri="storage://contracts/alpha_beta.txt",
        format_name="text/plain",
        classification=ClassificationLevel.CONFIDENTIAL,
        ai_context=ai_context,
    )

    assert metadata.technical.size_bytes == len(content.encode("utf-8"))
    assert metadata.technical.checksum_sha256 != ""
    assert metadata.business.department == "Legal"
    assert metadata.ai.model_version == "gemini-2.5-flash"
    assert metadata.ai.confidence_score == 0.98
    assert metadata.compliance.classification == ClassificationLevel.CONFIDENTIAL

    # Save to manager
    manager.set_metadata(metadata)
    retrieved = manager.get_metadata("asset_contract_meta_1")
    assert retrieved is not None
    assert retrieved.ai.agent_id == "contract_analyzer_agent"
