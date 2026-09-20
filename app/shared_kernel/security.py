"""
Platform Security Primitives, Cryptographic Hasher, and HMAC Signer.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Set, Optional
import hashlib
import hmac

@dataclass(frozen=True)
class PermissionContract:
    resource: str
    action: str

    def __str__(self) -> str:
        return f"{self.resource}:{self.action}"

@dataclass(frozen=True)
class RoleContract:
    name: str
    permissions: Set[PermissionContract] = field(default_factory=set)

@dataclass(frozen=True)
class PrincipalContract:
    id: str
    roles: Set[str] = field(default_factory=set)
    tenant_id: str = "default-tenant"

@dataclass(frozen=True)
class SecurityContext:
    principal: Optional[PrincipalContract] = None
    is_authenticated: bool = False
    scopes: Set[str] = field(default_factory=set)

class AuthorizationPolicyContract(ABC):
    @abstractmethod
    def authorize(self, context: SecurityContext, required_permission: PermissionContract) -> bool:
        pass

class Hasher:
    """Deterministic cryptographic SHA-256 and SHA-512 hasher."""
    @staticmethod
    def sha256(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def sha512(data: str) -> str:
        return hashlib.sha512(data.encode("utf-8")).hexdigest()

    @staticmethod
    def sha256_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def hmac_sha256(key: str, data: str) -> str:
        return hmac.new(key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).hexdigest()

class HmacSigner:
    def __init__(self, secret_key: str):
        self._key = secret_key

    def sign(self, payload: str) -> str:
        return Hasher.hmac_sha256(self._key, payload)

    def verify(self, payload: str, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)
