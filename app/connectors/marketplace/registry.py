"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Marketplace.
Provides catalog browsing, package installation, version upgrades, and review management.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.core.models import Connector, ConnectorCategory, ConnectorStatus
from app.connectors.registry.connector_registry import ConnectorRegistry

logger = logging.getLogger(__name__)


class ConnectorPackageManifest(BaseModel):
    """Manifest describing an installable connector package in the marketplace."""
    package_id: str
    name: str
    vendor: str
    version: str = "1.0.0"
    category: ConnectorCategory = ConnectorCategory.CUSTOM
    description: str = ""
    capabilities: List[str] = Field(default_factory=list)
    permissions_required: List[str] = Field(default_factory=list)
    certified: bool = True
    author_email: str = "partner@docutask.io"
    download_url: Optional[str] = None
    rating: float = 5.0
    downloads_count: int = 0


class MarketplaceRegistry:
    """
    Catalog of discoverable, installable, and community connector packages.
    """

    def __init__(self, connector_registry: Optional[ConnectorRegistry] = None):
        self._connector_registry = connector_registry or ConnectorRegistry()
        self._packages: Dict[str, ConnectorPackageManifest] = {}
        self._installed_packages: Dict[str, str] = {}  # package_id -> installed_version
        self._seed_marketplace()

    def _seed_marketplace(self) -> None:
        """Populates common marketplace packages."""
        pkgs = [
            ConnectorPackageManifest(
                package_id="pkg-gmail-enterprise",
                name="Gmail Enterprise",
                vendor="Google",
                version="2.1.0",
                category=ConnectorCategory.COMMUNICATION,
                description="Enterprise Gmail integration supporting OAuth2, threading, and attachments.",
                capabilities=["email.send", "email.read", "email.watch"],
                permissions_required=["mail.send", "mail.read"],
                certified=True,
                rating=4.9,
                downloads_count=12400,
            ),
            ConnectorPackageManifest(
                package_id="pkg-slack-collaboration",
                name="Slack Workspace",
                vendor="Slack",
                version="1.8.0",
                category=ConnectorCategory.COMMUNICATION,
                description="Real-time messaging, interactive blocks, and channel management.",
                capabilities=["message.send", "message.read", "channel.create"],
                permissions_required=["chat.write", "channels.read"],
                certified=True,
                rating=4.8,
                downloads_count=18200,
            ),
            ConnectorPackageManifest(
                package_id="pkg-s3-storage",
                name="AWS S3 Storage",
                vendor="Amazon Web Services",
                version="3.0.0",
                category=ConnectorCategory.STORAGE,
                description="High-durability cloud object storage and presigned URL generator.",
                capabilities=["storage.upload", "storage.download", "storage.list"],
                permissions_required=["s3:PutObject", "s3:GetObject"],
                certified=True,
                rating=4.9,
                downloads_count=21000,
            ),
            ConnectorPackageManifest(
                package_id="pkg-salesforce-crm",
                name="Salesforce CRM",
                vendor="Salesforce",
                version="2.4.0",
                category=ConnectorCategory.CRM,
                description="Lead, contact, and opportunity synchronizer via REST and Bulk APIs.",
                capabilities=["crm.contact.create", "crm.contact.get", "crm.lead.sync"],
                permissions_required=["api.read", "api.write"],
                certified=True,
                rating=4.7,
                downloads_count=8900,
            ),
        ]
        for p in pkgs:
            self._packages[p.package_id] = p

    def publish_package(self, manifest: ConnectorPackageManifest) -> None:
        """Publishes a new connector package to the marketplace catalog."""
        self._packages[manifest.package_id] = manifest
        logger.info(f"Published marketplace package '{manifest.package_id}' v{manifest.version}")

    def browse(
        self,
        category: Optional[ConnectorCategory] = None,
        search_query: Optional[str] = None,
        certified_only: bool = False,
    ) -> List[ConnectorPackageManifest]:
        """Lists available marketplace packages with optional filters."""
        results = list(self._packages.values())

        if category:
            results = [p for p in results if p.category == category]

        if certified_only:
            results = [p for p in results if p.certified]

        if search_query:
            q = search_query.lower()
            results = [
                p for p in results
                if q in p.name.lower() or q in p.vendor.lower() or q in p.description.lower() or any(q in c.lower() for c in p.capabilities)
            ]

        return results

    def install(self, package_id: str, organization_id: str = "org-default") -> Connector:
        """
        Installs a marketplace package into the platform connector registry.
        """
        pkg = self._packages.get(package_id)
        if not pkg:
            raise KeyError(f"Marketplace package '{package_id}' not found")

        connector = Connector(
            id=pkg.package_id.replace("pkg-", "conn-"),
            name=pkg.name,
            vendor=pkg.vendor,
            version=pkg.version,
            category=pkg.category,
            capabilities=pkg.capabilities,
            status=ConnectorStatus.INSTALLED,
            owner=organization_id,
            documentation=pkg.description,
        )

        self._connector_registry.register(connector)
        self._installed_packages[pkg.package_id] = pkg.version
        pkg.downloads_count += 1
        logger.info(f"Installed connector '{connector.id}' from marketplace package '{package_id}'")
        return connector

    def upgrade(self, package_id: str) -> Optional[Connector]:
        """Upgrades an installed connector to the latest marketplace version."""
        pkg = self._packages.get(package_id)
        if not pkg or package_id not in self._installed_packages:
            return None

        conn_id = package_id.replace("pkg-", "conn-")
        connector = self._connector_registry.get(conn_id)
        connector.version = pkg.version
        connector.status = ConnectorStatus.UPDATING
        self._installed_packages[package_id] = pkg.version
        logger.info(f"Upgraded connector '{conn_id}' to v{pkg.version}")
        return connector
