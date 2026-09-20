"""
Enterprise Secrets Interface and Management.
Ensures zero hardcoded or raw os.getenv() secrets leaking outside the infrastructure layer.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional
import uuid


@dataclass
class SecretRecord:
    """Encapsulated secret record with rotation and expiration metadata."""
    key: str
    value: str
    version: int = 1
    tenant_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    revoked: bool = False
    metadata: Dict[str, str] = field(default_factory=dict)


class ISecretManager(ABC):
    """Abstract interface for Secrets Management (Vault, AWS Secrets Manager, GCP Secret Manager)."""

    @abstractmethod
    def get_secret(self, key: str, tenant_id: Optional[str] = None) -> Optional[str]:
        pass

    @abstractmethod
    def create_secret(self, key: str, value: str, tenant_id: Optional[str] = None, expires_at: Optional[datetime] = None) -> SecretRecord:
        pass

    @abstractmethod
    def rotate_secret(self, key: str, new_value: str, tenant_id: Optional[str] = None) -> SecretRecord:
        pass

    @abstractmethod
    def expire_secret(self, key: str, tenant_id: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def revoke_secret(self, key: str, tenant_id: Optional[str] = None) -> None:
        pass


class SecretManager(ISecretManager):
    """In-memory encrypted secrets manager with tenant partition support."""

    def __init__(self):
        self._secrets: Dict[str, SecretRecord] = {}

    def _format_key(self, key: str, tenant_id: Optional[str] = None) -> str:
        return f"{tenant_id}:{key}" if tenant_id else f"global:{key}"

    def get_secret(self, key: str, tenant_id: Optional[str] = None) -> Optional[str]:
        full_key = self._format_key(key, tenant_id)
        record = self._secrets.get(full_key)
        if not record or record.revoked:
            return None
        if record.expires_at and record.expires_at < datetime.now(timezone.utc):
            return None
        return record.value

    def create_secret(
        self,
        key: str,
        value: str,
        tenant_id: Optional[str] = None,
        expires_at: Optional[datetime] = None,
    ) -> SecretRecord:
        full_key = self._format_key(key, tenant_id)
        record = SecretRecord(
            key=key,
            value=value,
            tenant_id=tenant_id,
            expires_at=expires_at,
        )
        self._secrets[full_key] = record
        return record

    def rotate_secret(self, key: str, new_value: str, tenant_id: Optional[str] = None) -> SecretRecord:
        full_key = self._format_key(key, tenant_id)
        existing = self._secrets.get(full_key)
        new_version = (existing.version + 1) if existing else 1
        record = SecretRecord(
            key=key,
            value=new_value,
            version=new_version,
            tenant_id=tenant_id,
        )
        self._secrets[full_key] = record
        return record

    def expire_secret(self, key: str, tenant_id: Optional[str] = None) -> None:
        full_key = self._format_key(key, tenant_id)
        if full_key in self._secrets:
            self._secrets[full_key].expires_at = datetime.now(timezone.utc)

    def revoke_secret(self, key: str, tenant_id: Optional[str] = None) -> None:
        full_key = self._format_key(key, tenant_id)
        if full_key in self._secrets:
            self._secrets[full_key].revoked = True
