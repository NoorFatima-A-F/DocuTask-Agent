"""Service Identity and SPIFFE Identity Management."""

from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass(frozen=True)
class SPIFFEIdentity:
    """SPIFFE ID representation following standard spiffe://<trust_domain>/ns/<namespace>/sa/<service>."""
    trust_domain: str = "docutask.internal"
    namespace: str = "default"
    service_name: str = "anonymous"

    @property
    def uri(self) -> str:
        return f"spiffe://{self.trust_domain}/ns/{self.namespace}/sa/{self.service_name}"

    @classmethod
    def parse(cls, spiffe_uri: str) -> SPIFFEIdentity:
        pattern = r"^spiffe://([^/]+)/ns/([^/]+)/sa/([^/]+)$"
        match = re.match(pattern, spiffe_uri)
        if not match:
            raise ValueError(f"Invalid SPIFFE URI format: {spiffe_uri}")
        trust_domain, namespace, service_name = match.groups()
        return cls(trust_domain=trust_domain, namespace=namespace, service_name=service_name)


@dataclass
class WorkloadIdentity:
    identity_id: str
    spiffe_id: SPIFFEIdentity
    tenant_id: str = "system"
    roles: Set[str] = field(default_factory=lambda: {"service"})
    claims: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 86400.0)
    revoked: bool = False

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired


class ServiceIdentityManager:
    """Manages service identity provisioning, registration, and trust validation."""

    def __init__(self, default_trust_domain: str = "docutask.internal"):
        self.default_trust_domain = default_trust_domain
        self._identities: Dict[str, WorkloadIdentity] = {}

    def mint_identity(
        self,
        service_name: str,
        namespace: str = "default",
        tenant_id: str = "system",
        roles: Optional[Set[str]] = None,
        ttl_seconds: float = 86400.0,
        claims: Optional[Dict[str, Any]] = None,
    ) -> WorkloadIdentity:
        """Issue a new verified workload identity."""
        spiffe_id = SPIFFEIdentity(
            trust_domain=self.default_trust_domain,
            namespace=namespace,
            service_name=service_name,
        )
        ident = WorkloadIdentity(
            identity_id=f"id-{uuid.uuid4().hex[:12]}",
            spiffe_id=spiffe_id,
            tenant_id=tenant_id,
            roles=roles or {"service"},
            claims=claims or {},
            created_at=time.time(),
            expires_at=time.time() + ttl_seconds,
        )
        self._identities[ident.spiffe_id.uri] = ident
        return ident

    def get_identity(self, spiffe_uri: str) -> Optional[WorkloadIdentity]:
        return self._identities.get(spiffe_uri)

    def validate_identity(self, spiffe_uri: str) -> bool:
        """Validate an identity's existence, expiration, and revocation status."""
        ident = self.get_identity(spiffe_uri)
        if not ident:
            return False
        return ident.is_valid

    def revoke_identity(self, spiffe_uri: str) -> bool:
        """Revoke a workload identity immediately."""
        ident = self._identities.get(spiffe_uri)
        if ident:
            ident.revoked = True
            return True
        return False

    def list_identities(self, namespace: Optional[str] = None) -> List[WorkloadIdentity]:
        if namespace:
            return [i for i in self._identities.values() if i.spiffe_id.namespace == namespace]
        return list(self._identities.values())
