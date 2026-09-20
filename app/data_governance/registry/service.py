"""Data Governance Registry Service (Phase 8B)."""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from app.data_governance.registry.models import (
    DataAsset,
    AssetType,
    ClassificationLevel,
    SensitivityCategory,
    AssetLifecycleState,
    DataOwnership,
)
from app.data_governance.assets.models import DataAssetVersion
from app.data_governance.registry.repository import DataAssetRepository


class DataGovernanceRegistryService:
    """Manages the full lifecycle and versioning of governed enterprise data assets."""

    def __init__(self, repository: Optional[DataAssetRepository] = None):
        self.repository = repository or DataAssetRepository()
        # asset_id -> List[DataAssetVersion]
        self._versions: Dict[str, List[DataAssetVersion]] = {}

    def _compute_checksum(self, content: bytes | str) -> str:
        data = content.encode("utf-8") if isinstance(content, str) else content
        return hashlib.sha256(data).hexdigest()

    def register_asset(
        self,
        asset_id: str,
        organization_id: str,
        workspace_id: str,
        name: str,
        asset_type: AssetType,
        source: str,
        location_uri: str,
        owner: DataOwnership,
        creator_id: str,
        classification: ClassificationLevel = ClassificationLevel.INTERNAL,
        sensitivity_categories: Optional[Set[SensitivityCategory]] = None,
        content_for_checksum: Optional[bytes | str] = None,
        size_bytes: int = 0,
        mime_type: str = "application/octet-stream",
        retention_policy_id: Optional[str] = None,
        compliance_tags: Optional[List[str]] = None,
        custom_metadata: Optional[Dict[str, Any]] = None,
    ) -> DataAsset:
        """Register a new data asset under enterprise governance."""
        checksum = self._compute_checksum(content_for_checksum) if content_for_checksum else ""

        asset = DataAsset(
            asset_id=asset_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            name=name,
            asset_type=asset_type,
            source=source,
            location_uri=location_uri,
            owner=owner,
            creator_id=creator_id,
            classification=classification,
            sensitivity_categories=sensitivity_categories or set(),
            version=1,
            status=AssetLifecycleState.REGISTERED,
            checksum_sha256=checksum,
            size_bytes=size_bytes,
            mime_type=mime_type,
            retention_policy_id=retention_policy_id,
            compliance_tags=compliance_tags or [],
            custom_metadata=custom_metadata or {},
        )

        self.repository.save(asset)

        # Record Initial Version
        initial_version = DataAssetVersion(
            version_id=f"ver_{asset.asset_id}_v1",
            asset_id=asset.asset_id,
            version_number=1,
            checksum_sha256=checksum,
            size_bytes=size_bytes,
            classification=classification,
            created_by=creator_id,
            change_summary="Initial registration",
        )
        self._versions[asset.asset_id] = [initial_version]
        return asset

    def get_asset(self, asset_id: str, organization_id: str) -> Optional[DataAsset]:
        """Retrieve governed asset."""
        return self.repository.get_by_id(asset_id, organization_id)

    def create_version(
        self,
        asset_id: str,
        organization_id: str,
        updated_by: str,
        change_summary: str,
        new_content_for_checksum: Optional[bytes | str] = None,
        new_size_bytes: Optional[int] = None,
        new_classification: Optional[ClassificationLevel] = None,
    ) -> DataAsset:
        """Increment asset version and store snapshot."""
        asset = self.get_asset(asset_id, organization_id)
        if not asset:
            raise ValueError(f"Asset '{asset_id}' not found in organization '{organization_id}'")

        asset.version += 1
        if new_content_for_checksum:
            asset.checksum_sha256 = self._compute_checksum(new_content_for_checksum)
        if new_size_bytes is not None:
            asset.size_bytes = new_size_bytes
        if new_classification:
            asset.classification = new_classification

        asset.status = AssetLifecycleState.UPDATED
        asset.updated_at = datetime.now(timezone.utc)
        self.repository.save(asset)

        version_record = DataAssetVersion(
            version_id=f"ver_{asset.asset_id}_v{asset.version}",
            asset_id=asset.asset_id,
            version_number=asset.version,
            checksum_sha256=asset.checksum_sha256,
            size_bytes=asset.size_bytes,
            classification=asset.classification,
            created_by=updated_by,
            change_summary=change_summary,
        )
        self._versions[asset.asset_id].append(version_record)
        return asset

    def list_versions(self, asset_id: str) -> List[DataAssetVersion]:
        """Get version history for an asset."""
        return self._versions.get(asset_id, [])
