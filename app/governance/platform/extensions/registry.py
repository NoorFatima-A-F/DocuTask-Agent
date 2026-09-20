"""Extension Registry and Lifecycle Platform."""

from datetime import datetime, timezone
import secrets
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from .validators import ExtensionValidator


class ExtensionRecord(BaseModel):
    """Catalog record for a registered governance extension."""

    extension_id: str
    name: str
    version: str
    owner: str
    tenant_id: str
    capabilities: List[str]
    permissions: Set[str] = Field(default_factory=set)
    is_enabled: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExtensionRegistry:
    """Multi-tenant catalogue and registry for governance extensions."""

    def __init__(self) -> None:
        self._records: Dict[str, ExtensionRecord] = {}
        self._instances: Dict[str, Any] = {}

    def register_extension(
        self,
        extension_obj: Any,
        name: str,
        version: str,
        owner: str,
        tenant_id: str,
        capabilities: List[str],
        permissions: Optional[Set[str]] = None,
    ) -> ExtensionRecord:
        """Validate and register a new governance extension."""
        ExtensionValidator.validate_extension(extension_obj, capabilities)

        extension_id = f"ext_{secrets.token_hex(8)}"
        record = ExtensionRecord(
            extension_id=extension_id,
            name=name,
            version=version,
            owner=owner,
            tenant_id=tenant_id,
            capabilities=capabilities,
            permissions=permissions or {"governance:extension:read"},
            is_enabled=True,
        )

        self._records[extension_id] = record
        self._instances[extension_id] = extension_obj
        return record

    def get_extension(self, extension_id: str) -> Optional[ExtensionRecord]:
        return self._records.get(extension_id)

    def get_extension_instance(self, extension_id: str) -> Optional[Any]:
        return self._instances.get(extension_id)

    def enable_extension(self, extension_id: str) -> Optional[ExtensionRecord]:
        rec = self._records.get(extension_id)
        if rec:
            rec.is_enabled = True
            rec.updated_at = datetime.now(timezone.utc)
            return rec
        return None

    def disable_extension(self, extension_id: str) -> Optional[ExtensionRecord]:
        rec = self._records.get(extension_id)
        if rec:
            rec.is_enabled = False
            rec.updated_at = datetime.now(timezone.utc)
            return rec
        return None

    def remove_extension(self, extension_id: str) -> bool:
        if extension_id in self._records:
            del self._records[extension_id]
            self._instances.pop(extension_id, None)
            return True
        return False

    def list_extensions(
        self,
        tenant_id: Optional[str] = None,
        capability: Optional[str] = None,
        only_enabled: bool = False,
    ) -> List[ExtensionRecord]:
        results = list(self._records.values())
        if tenant_id:
            results = [r for r in results if r.tenant_id == tenant_id]
        if capability:
            results = [r for r in results if capability in r.capabilities]
        if only_enabled:
            results = [r for r in results if r.is_enabled]
        return results
