"""Automated Metadata Extractor (Phase 8B)."""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional
from app.data_governance.metadata.schemas import (
    TechnicalMetadata,
    BusinessMetadata,
    AIMetadata,
    ComplianceMetadata,
    ComprehensiveAssetMetadata,
)
from app.data_governance.registry.models import ClassificationLevel


class MetadataExtractor:
    """Automatically extracts technical, business, AI, and compliance metadata from artifacts."""

    def extract_from_content(
        self,
        asset_id: str,
        content: str | bytes,
        owner_id: str,
        department: str = "General",
        location_uri: str = "memory://",
        format_name: str = "text/plain",
        classification: ClassificationLevel = ClassificationLevel.INTERNAL,
        ai_context: Optional[Dict[str, Any]] = None,
    ) -> ComprehensiveAssetMetadata:
        """Extract comprehensive 4D metadata from raw content."""
        raw_bytes = content.encode("utf-8") if isinstance(content, str) else content
        checksum = hashlib.sha256(raw_bytes).hexdigest()
        size_bytes = len(raw_bytes)

        technical = TechnicalMetadata(
            format=format_name,
            size_bytes=size_bytes,
            checksum_sha256=checksum,
            location_uri=location_uri,
        )

        business = BusinessMetadata(
            department=department,
            owner_user_id=owner_id,
        )

        ai_meta = None
        if ai_context:
            ai_meta = AIMetadata(
                embedding_model=ai_context.get("embedding_model"),
                embedding_dimensions=ai_context.get("embedding_dimensions"),
                model_version=ai_context.get("model_version"),
                prompt_version=ai_context.get("prompt_version"),
                agent_id=ai_context.get("agent_id"),
                workflow_id=ai_context.get("workflow_id"),
                retrieval_sources=ai_context.get("retrieval_sources", []),
                confidence_score=ai_context.get("confidence_score"),
            )

        compliance = ComplianceMetadata(
            classification=classification,
        )

        return ComprehensiveAssetMetadata(
            asset_id=asset_id,
            technical=technical,
            business=business,
            ai=ai_meta,
            compliance=compliance,
        )
