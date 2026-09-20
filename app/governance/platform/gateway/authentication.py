"""Enterprise Governance API Gateway Authentication System.

Supports API Keys, Service Accounts, OAuth2 token contexts, and comprehensive
APIRequestContext generation for multi-tenant governance security boundaries.
"""

from datetime import datetime, timezone
from enum import Enum
import hashlib
import hmac
import secrets
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class AuthScheme(str, Enum):
    API_KEY = "api_key"
    SERVICE_ACCOUNT = "service_account"
    OAUTH2 = "oauth2"
    INTERNAL_SYSTEM = "internal_system"


class APIRequestContext(BaseModel):
    """Contextual metadata attached to every incoming API request."""

    request_id: str = Field(default_factory=lambda: f"req_{secrets.token_hex(12)}")
    client_id: str
    tenant_id: str
    user_id: Optional[str] = None
    service_account: Optional[str] = None
    auth_scheme: AuthScheme = AuthScheme.API_KEY
    scopes: Set[str] = Field(default_factory=set)
    ip_address: Optional[str] = "127.0.0.1"
    environment: str = "production"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def has_scope(self, required_scope: str) -> bool:
        """Check if request context contains required permission scope or admin scope."""
        if "*" in self.scopes or "admin:all" in self.scopes or "governance:admin" in self.scopes:
            return True
        return required_scope in self.scopes


class APIKeyRecord(BaseModel):
    """Persistent representation of a registered API Key."""

    key_id: str
    name: str
    key_hash: str
    tenant_id: str
    client_id: str
    scopes: Set[str] = Field(default_factory=lambda: {"governance:read", "governance:evaluate"})
    rate_limit_rpm: int = 600
    is_active: bool = True
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_used_at: Optional[datetime] = None


class ServiceAccountRecord(BaseModel):
    """Persistent representation of an Enterprise Service Account."""

    account_id: str
    name: str
    tenant_id: str
    description: str = ""
    assigned_roles: List[str] = Field(default_factory=lambda: ["governance.evaluator"])
    scopes: Set[str] = Field(default_factory=lambda: {"governance:read", "governance:evaluate"})
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuthenticationManager:
    """Central gateway authentication provider and token/key registry."""

    def __init__(self) -> None:
        self._api_keys: Dict[str, APIKeyRecord] = {}  # key_hash -> APIKeyRecord
        self._key_id_map: Dict[str, str] = {}  # key_id -> key_hash
        self._service_accounts: Dict[str, ServiceAccountRecord] = {}
        self._raw_keys_for_lookup: Dict[str, str] = {}  # plaintext -> key_hash (in-memory test helper)

    @staticmethod
    def hash_key(raw_key: str) -> str:
        """Compute secure HMAC-SHA-256 hash of plaintext key."""
        salt = b"gov_api_key_salt_v1"
        return hmac.new(salt, raw_key.encode("utf-8"), hashlib.sha256).hexdigest()

    def create_api_key(
        self,
        name: str,
        tenant_id: str,
        client_id: Optional[str] = None,
        scopes: Optional[Set[str]] = None,
        rate_limit_rpm: int = 600,
        expires_at: Optional[datetime] = None,
    ) -> tuple[str, APIKeyRecord]:
        """Generate a new API key, store its hash, and return plaintext token."""
        raw_key = f"gov_live_{secrets.token_urlsafe(32)}"
        key_id = f"key_{secrets.token_hex(8)}"
        key_hash = self.hash_key(raw_key)

        record = APIKeyRecord(
            key_id=key_id,
            name=name,
            key_hash=key_hash,
            tenant_id=tenant_id,
            client_id=client_id or f"client_{tenant_id}",
            scopes=scopes or {"governance:read", "governance:evaluate"},
            rate_limit_rpm=rate_limit_rpm,
            expires_at=expires_at,
        )

        self._api_keys[key_hash] = record
        self._key_id_map[key_id] = key_hash
        self._raw_keys_for_lookup[raw_key] = key_hash
        return raw_key, record

    def revoke_api_key(self, key_id: str) -> bool:
        """Deactivate an existing API key."""
        key_hash = self._key_id_map.get(key_id)
        if key_hash and key_hash in self._api_keys:
            self._api_keys[key_hash].is_active = False
            return True
        return False

    def register_service_account(
        self,
        name: str,
        tenant_id: str,
        description: str = "",
        roles: Optional[List[str]] = None,
        scopes: Optional[Set[str]] = None,
    ) -> ServiceAccountRecord:
        """Register an enterprise service account."""
        account_id = f"sa_{secrets.token_hex(8)}"
        record = ServiceAccountRecord(
            account_id=account_id,
            name=name,
            tenant_id=tenant_id,
            description=description,
            assigned_roles=roles or ["governance.evaluator"],
            scopes=scopes or {"governance:read", "governance:evaluate", "governance:internal"},
        )
        self._service_accounts[account_id] = record
        return record

    def authenticate_request(
        self,
        authorization_header: Optional[str] = None,
        api_key_header: Optional[str] = None,
        client_ip: Optional[str] = "127.0.0.1",
    ) -> APIRequestContext:
        """Validate credentials from incoming headers and construct an APIRequestContext."""
        raw_token: Optional[str] = None

        if authorization_header:
            parts = authorization_header.strip().split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                raw_token = parts[1]
            elif len(parts) == 1:
                raw_token = parts[0]
        elif api_key_header:
            raw_token = api_key_header.strip()

        if not raw_token:
            raise PermissionError("Missing credentials. Please provide Authorization: Bearer <key> or X-API-Key.")

        # Check internal bypass tokens
        if raw_token.startswith("gov_internal_"):
            return APIRequestContext(
                client_id="system_internal",
                tenant_id="tenant_system",
                auth_scheme=AuthScheme.INTERNAL_SYSTEM,
                scopes={"*"},
                ip_address=client_ip,
                service_account="internal_service",
            )

        # Check API key hash
        key_hash = self.hash_key(raw_token)
        record = self._api_keys.get(key_hash)

        if not record:
            raise PermissionError("Invalid API key or token.")

        if not record.is_active:
            raise PermissionError("API key has been revoked or disabled.")

        if record.expires_at and datetime.now(timezone.utc) > record.expires_at:
            raise PermissionError("API key has expired.")

        record.last_used_at = datetime.now(timezone.utc)

        return APIRequestContext(
            client_id=record.client_id,
            tenant_id=record.tenant_id,
            auth_scheme=AuthScheme.API_KEY,
            scopes=record.scopes,
            ip_address=client_ip,
        )
