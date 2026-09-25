"""Custom Domain Management & Verification Engine (ESP-MOOS).

Supports vanity domains (e.g. automation.company.com) with DNS verification, SSL status, and host routing.
"""

from __future__ import annotations

import uuid
from typing import Dict, Optional
from app.tenancy.core.models import CustomDomain
from app.tenancy.core.exceptions import DomainVerificationError, TenancyError


class CustomDomainManager:
    """Manages custom domain verification and tenant host routing."""

    def __init__(self):
        self._domains: Dict[str, CustomDomain] = {}
        self._domain_to_org: Dict[str, str] = {}

    def register_domain(self, organization_id: str, domain_name: str) -> CustomDomain:
        """Register a custom domain and generate verification token."""
        normalized_domain = domain_name.lower().strip()
        if normalized_domain in self._domain_to_org:
            raise TenancyError(f"Domain '{normalized_domain}' is already registered")

        domain = CustomDomain(
            domain_id=f"dom_{uuid.uuid4().hex[:8]}",
            organization_id=organization_id,
            domain_name=normalized_domain,
            verification_token=f"docutask-verify-{uuid.uuid4().hex}",
            is_verified=False,
            ssl_active=False,
        )
        self._domains[domain.domain_id] = domain
        self._domain_to_org[normalized_domain] = organization_id
        return domain

    def verify_domain(self, domain_id: str, mock_dns_verified: bool = True) -> CustomDomain:
        """Simulate DNS TXT record lookup and verify domain ownership."""
        domain = self._domains.get(domain_id)
        if not domain:
            raise TenancyError(f"Domain '{domain_id}' not found")

        if not mock_dns_verified:
            raise DomainVerificationError(f"DNS TXT record verification failed for '{domain.domain_name}'")

        domain.is_verified = True
        domain.ssl_active = True
        return domain

    def resolve_organization_by_host(self, host_header: str) -> Optional[str]:
        """Resolve organization ID from incoming HTTP Host header."""
        normalized_host = host_header.split(":")[0].lower().strip()
        return self._domain_to_org.get(normalized_host)

    def get_domain(self, domain_id: str) -> Optional[CustomDomain]:
        """Retrieve custom domain by ID."""
        return self._domains.get(domain_id)
