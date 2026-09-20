"""Marketplace Tenant Isolation Engine (ESP-MOOS).

Ensures marketplace resources (connectors, agent templates, knowledge packs) are installed
and customized strictly in tenant-scoped environments without mutating global catalog definitions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TenantInstalledResource(BaseModel):
    """Tenant-scoped installation of a global marketplace asset."""
    installation_id: str
    organization_id: str
    workspace_id: str
    marketplace_resource_id: str
    resource_type: str  # CONNECTOR, AGENT_TEMPLATE, KNOWLEDGE_PACK
    version: str
    tenant_configuration: Dict[str, Any] = Field(default_factory=dict)
    is_enabled: bool = True


class MarketplaceTenantIsolation:
    """Manages tenant isolation for marketplace packages and plugins."""

    def __init__(self):
        self._installations: Dict[str, TenantInstalledResource] = {}

    def install_resource(
        self,
        installation_id: str,
        organization_id: str,
        workspace_id: str,
        marketplace_resource_id: str,
        resource_type: str,
        version: str,
        tenant_configuration: Optional[Dict[str, Any]] = None,
    ) -> TenantInstalledResource:
        """Install a global marketplace resource into a specific tenant workspace."""
        installed = TenantInstalledResource(
            installation_id=installation_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            marketplace_resource_id=marketplace_resource_id,
            resource_type=resource_type,
            version=version,
            tenant_configuration=tenant_configuration or {},
            is_enabled=True,
        )
        self._installations[installation_id] = installed
        return installed

    def get_installation(
        self, installation_id: str, organization_id: Optional[str] = None
    ) -> Optional[TenantInstalledResource]:
        """Retrieve installation ensuring organization ownership."""
        inst = self._installations.get(installation_id)
        if inst and organization_id and inst.organization_id != organization_id:
            return None
        return inst

    def list_installations(self, organization_id: str, workspace_id: Optional[str] = None) -> List[TenantInstalledResource]:
        """List all marketplace installations within an organization."""
        return [
            inst for inst in self._installations.values()
            if inst.organization_id == organization_id and (workspace_id is None or inst.workspace_id == workspace_id)
        ]
