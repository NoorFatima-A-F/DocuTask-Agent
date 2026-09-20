"""Enterprise Data Governance SDK (Phase 8B)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.data_governance.registry.models import (
    DataAsset,
    AssetType,
    ClassificationLevel,
    DataOwnership,
)
from app.data_governance.registry.service import DataGovernanceRegistryService
from app.data_governance.classification.classifier import DataClassificationEngine, ClassificationResult
from app.data_governance.lineage.tracker import LineageTracker
from app.data_governance.lineage.graph import LineageGraphEngine
from app.data_governance.provenance.history import ProvenanceHistoryEngine
from app.data_governance.provenance.source import ProvenanceSourceRecord
from app.data_governance.catalog.search import EnterpriseDataCatalog
from app.data_governance.quality.scoring import DataQualityScorer, DataQualityReport
from app.data_governance.retention.scheduler import RetentionAndLegalHoldEngine
from app.data_governance.privacy.masking import PrivacyMaskingEngine
from app.data_governance.access.tracking import DataAccessTracker, DataActionType


class DataGovernanceSDK:
    """Unified Developer SDK for Data Governance, Lineage, and Provenance."""

    def __init__(
        self,
        registry: Optional[DataGovernanceRegistryService] = None,
        classifier: Optional[DataClassificationEngine] = None,
        lineage: Optional[LineageTracker] = None,
        provenance: Optional[ProvenanceHistoryEngine] = None,
        catalog: Optional[EnterpriseDataCatalog] = None,
        quality: Optional[DataQualityScorer] = None,
        retention: Optional[RetentionAndLegalHoldEngine] = None,
        privacy: Optional[PrivacyMaskingEngine] = None,
        access: Optional[DataAccessTracker] = None,
    ):
        self.registry = registry or DataGovernanceRegistryService()
        self.classifier = classifier or DataClassificationEngine()
        self.lineage = lineage or LineageTracker()
        self.provenance = provenance or ProvenanceHistoryEngine()
        self.catalog = catalog or EnterpriseDataCatalog(self.registry.repository)
        self.quality = quality or DataQualityScorer()
        self.retention = retention or RetentionAndLegalHoldEngine()
        self.privacy = privacy or PrivacyMaskingEngine()
        self.access = access or DataAccessTracker()

    def register(
        self,
        asset_id: str,
        organization_id: str,
        workspace_id: str,
        name: str,
        source: str,
        owner_id: str,
        asset_type: AssetType = AssetType.DOCUMENT,
        classification: ClassificationLevel = ClassificationLevel.INTERNAL,
        content_for_checksum: Optional[str | bytes] = None,
    ) -> DataAsset:
        """Register a new governed data asset."""
        owner = DataOwnership(owner_user_id=owner_id, responsible_team="Data Team", department="Engineering")
        return self.registry.register_asset(
            asset_id=asset_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            name=name,
            asset_type=asset_type,
            source=source,
            location_uri=f"governed://{asset_id}",
            owner=owner,
            creator_id=owner_id,
            classification=classification,
            content_for_checksum=content_for_checksum,
        )

    def classify(self, text: str) -> ClassificationResult:
        """Automatically classify text payload."""
        return self.classifier.classify_text(text)

    def mask(self, text: str) -> str:
        """Mask sensitive PII in text."""
        return self.privacy.mask(text)

    def record_access(
        self,
        asset_id: str,
        organization_id: str,
        user_id: str,
        action: DataActionType = DataActionType.READ,
    ):
        """Record data access event."""
        return self.access.record_access(
            asset_id=asset_id,
            organization_id=organization_id,
            user_id=user_id,
            action=action,
        )
