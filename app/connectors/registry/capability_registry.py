"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Capability Registry.
Implements technology-independent capability discovery (e.g. 'email.send', 'message.send')
and maps abstract intents to ranked, healthy connector providers.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional
from app.connectors.core.exceptions import CapabilityNotFoundError
from app.connectors.core.models import (
    CapabilityDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorHealth,
    ConnectorStatus,
)
from app.connectors.registry.connector_registry import ConnectorRegistry

logger = logging.getLogger(__name__)


class CapabilityRegistry:
    """
    Technology-independent capability discovery engine.
    Allows workflows and AI agents to query for abstract operations rather than specific providers.
    """

    def __init__(self, connector_registry: Optional[ConnectorRegistry] = None):
        self._connector_registry = connector_registry or ConnectorRegistry()
        self._capabilities: Dict[str, CapabilityDescriptor] = {}
        self._capability_providers: Dict[str, List[str]] = {}  # capability_name -> [connector_id, ...]
        self._initialize_standard_capabilities()

    def _initialize_standard_capabilities(self) -> None:
        """Seeds common enterprise iPaaS capability descriptors."""
        standards = [
            CapabilityDescriptor(
                name="email.send",
                category=ConnectorCategory.COMMUNICATION,
                description="Send an email message with attachments and formatting.",
                input_schema={"type": "object", "required": ["recipient", "subject", "body"]},
            ),
            CapabilityDescriptor(
                name="message.send",
                category=ConnectorCategory.COMMUNICATION,
                description="Dispatch a real-time message to a channel or direct chat.",
                input_schema={"type": "object", "required": ["channel", "text"]},
            ),
            CapabilityDescriptor(
                name="storage.upload",
                category=ConnectorCategory.STORAGE,
                description="Upload a file or binary payload to cloud storage.",
                input_schema={"type": "object", "required": ["path", "content"]},
            ),
            CapabilityDescriptor(
                name="storage.download",
                category=ConnectorCategory.STORAGE,
                description="Download a document or binary object by path/key.",
                input_schema={"type": "object", "required": ["path"]},
            ),
            CapabilityDescriptor(
                name="crm.contact.create",
                category=ConnectorCategory.CRM,
                description="Create or upsert a customer or lead record.",
                input_schema={"type": "object", "required": ["email", "name"]},
            ),
            CapabilityDescriptor(
                name="crm.contact.get",
                category=ConnectorCategory.CRM,
                description="Retrieve customer metadata by email or identifier.",
                input_schema={"type": "object", "required": ["id"]},
            ),
            CapabilityDescriptor(
                name="finance.invoice.create",
                category=ConnectorCategory.FINANCE,
                description="Create an accounts payable/receivable invoice.",
                input_schema={"type": "object", "required": ["vendor", "amount", "currency"]},
            ),
            CapabilityDescriptor(
                name="document.ocr",
                category=ConnectorCategory.DOCUMENTS,
                description="Extract structured text and key-value pairs from scanned documents.",
                input_schema={"type": "object", "required": ["document_bytes"]},
            ),
            CapabilityDescriptor(
                name="search.query",
                category=ConnectorCategory.SEARCH,
                description="Execute an enterprise search query across index records.",
                input_schema={"type": "object", "required": ["query"]},
            ),
        ]
        for cap in standards:
            self._capabilities[cap.name] = cap
            self._capability_providers[cap.name] = []

    def register_capability(self, capability: CapabilityDescriptor) -> None:
        """Registers a new abstract capability specification."""
        self._capabilities[capability.name] = capability
        if capability.name not in self._capability_providers:
            self._capability_providers[capability.name] = []

    def bind_provider(self, capability_name: str, connector_id: str) -> None:
        """Binds a connector as a viable provider for a capability."""
        if capability_name not in self._capabilities:
            self._capabilities[capability_name] = CapabilityDescriptor(
                name=capability_name,
                category=ConnectorCategory.CUSTOM,
            )
            self._capability_providers[capability_name] = []

        if connector_id not in self._capability_providers[capability_name]:
            self._capability_providers[capability_name].append(connector_id)

    def find_providers(
        self,
        capability_name: str,
        healthy_only: bool = True,
        preferred_vendor: Optional[str] = None,
    ) -> List[Connector]:
        """
        Discovers all available connector providers supporting a capability,
        filtering by health and sorting by preference.
        """
        provider_ids = self._capability_providers.get(capability_name, [])
        if not provider_ids:
            # Also check connector definitions directly in connector_registry
            for connector in self._connector_registry.list_all():
                if capability_name in connector.capabilities and connector.id not in provider_ids:
                    provider_ids.append(connector.id)

        if not provider_ids:
            raise CapabilityNotFoundError(
                f"No provider found for capability '{capability_name}'",
                details={"capability": capability_name},
            )

        connectors: List[Connector] = []
        for cid in provider_ids:
            try:
                c = self._connector_registry.get(cid)
                if healthy_only and c.health != ConnectorHealth.HEALTHY:
                    continue
                if c.status not in (ConnectorStatus.READY, ConnectorStatus.ACTIVE):
                    continue
                connectors.append(c)
            except Exception:
                continue

        if preferred_vendor:
            connectors.sort(key=lambda c: 0 if c.vendor.lower() == preferred_vendor.lower() else 1)

        return connectors

    def get_capability(self, capability_name: str) -> Optional[CapabilityDescriptor]:
        """Retrieves descriptor metadata for a capability."""
        return self._capabilities.get(capability_name)

    def list_capabilities(self, category: Optional[ConnectorCategory] = None) -> List[CapabilityDescriptor]:
        """Lists all registered capabilities, optionally filtered by category."""
        caps = list(self._capabilities.values())
        if category:
            caps = [c for c in caps if c.category == category]
        return caps
