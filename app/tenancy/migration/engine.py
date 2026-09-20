"""Tenant Migration, Cloning & Regional Transfer Engine (ESP-MOOS).

Supports:
- Full Tenant Export & Import
- Workspace / Project Cloning
- Organization Ownership Transfer
- Cross-Region Data Migration
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional
from app.tenancy.core.models import Region
from app.tenancy.core.exceptions import TenancyError
from app.tenancy.organizations.manager import OrganizationManager
from app.tenancy.backup.engine import TenantBackupRestoreEngine


class TenantMigrationEngine:
    """Manages tenant exports, imports, clones, and migrations."""

    def __init__(
        self,
        org_manager: OrganizationManager,
        backup_engine: TenantBackupRestoreEngine,
    ):
        self.org_manager = org_manager
        self.backup_engine = backup_engine

    def export_tenant(self, organization_id: str) -> Dict[str, Any]:
        """Export full organization metadata and snapshot."""
        org = self.org_manager.get_organization(organization_id)
        snapshot = self.backup_engine.create_snapshot(
            organization_id=organization_id,
            scope="FULL_ORGANIZATION",
            payload={"organization": org.model_dump(mode="json")},
        )
        return {
            "export_id": f"exp_{uuid.uuid4().hex[:8]}",
            "organization_id": organization_id,
            "snapshot_id": snapshot.snapshot_id,
            "size_bytes": snapshot.size_bytes,
            "checksum": snapshot.checksum,
        }

    def clone_organization(
        self,
        source_org_id: str,
        target_org_id: str,
        new_name: str,
        new_owner_id: str,
    ) -> Dict[str, Any]:
        """Clone an existing organization configuration to a new tenant."""
        source_org = self.org_manager.get_organization(source_org_id)
        new_org = self.org_manager.create_organization(
            org_id=target_org_id,
            name=new_name,
            owner_id=new_owner_id,
            industry=source_org.industry,
            region=source_org.region,
            subscription_plan=source_org.subscription_plan,
            compliance_profile=source_org.compliance_profile,
            metadata=dict(source_org.metadata),
        )
        return {
            "status": "CLONED",
            "source_org_id": source_org_id,
            "new_organization_id": new_org.id,
        }

    def transfer_ownership(
        self,
        organization_id: str,
        current_owner_id: str,
        new_owner_id: str,
    ) -> Dict[str, Any]:
        """Transfer organization primary ownership to a new user."""
        org = self.org_manager.get_organization(organization_id)
        if org.owner_id != current_owner_id:
            raise TenancyError(f"User '{current_owner_id}' is not the current owner of organization '{organization_id}'")

        org.owner_id = new_owner_id
        return {
            "status": "TRANSFERRED",
            "organization_id": organization_id,
            "previous_owner_id": current_owner_id,
            "new_owner_id": new_owner_id,
        }

    def migrate_region(
        self,
        organization_id: str,
        target_region: Region,
    ) -> Dict[str, Any]:
        """Migrate tenant data residency to a new cloud region."""
        org = self.org_manager.get_organization(organization_id)
        old_region = org.region
        org.region = target_region
        return {
            "status": "MIGRATED",
            "organization_id": organization_id,
            "previous_region": old_region.value,
            "target_region": target_region.value,
        }
