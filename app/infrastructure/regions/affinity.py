"""Tenant Affinity & Isolation Management across Multi-Region topology."""

import threading
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TenantAffinityRule(BaseModel):
    """Configuration mapping a tenant to allowed/pinned regions."""

    tenant_id: str
    allowed_region_ids: List[str] = Field(default_factory=list)
    pinned_region_id: Optional[str] = None  # Hard-pinned primary region
    exclusive: bool = False  # Tenant has exclusive residency constraints
    required_jurisdiction: Optional[str] = None  # e.g. "EU", "US"
    disallowed_region_ids: List[str] = Field(default_factory=list)


class TenantAffinityManager:
    """Manages tenant isolation, pinning, and region routing constraints."""

    def __init__(self):
        self._rules: Dict[str, TenantAffinityRule] = {}
        self._lock = threading.RLock()

    def set_tenant_affinity(self, rule: TenantAffinityRule) -> TenantAffinityRule:
        """Register or update tenant affinity rule."""
        with self._lock:
            self._rules[rule.tenant_id] = rule
            return rule

    def get_tenant_affinity(self, tenant_id: str) -> Optional[TenantAffinityRule]:
        """Retrieve tenant affinity configuration."""
        with self._lock:
            return self._rules.get(tenant_id)

    def is_region_allowed_for_tenant(self, tenant_id: str, region_id: str) -> bool:
        """Evaluate if tenant can execute in the target region."""
        with self._lock:
            rule = self._rules.get(tenant_id)
            if not rule:
                # Default open multi-tenant policy
                return True

            if region_id in rule.disallowed_region_ids:
                return False

            if rule.pinned_region_id and region_id != rule.pinned_region_id:
                return False

            if rule.allowed_region_ids and region_id not in rule.allowed_region_ids:
                return False

            return True

    def remove_tenant_affinity(self, tenant_id: str) -> bool:
        """Remove tenant affinity rule."""
        with self._lock:
            if tenant_id in self._rules:
                del self._rules[tenant_id]
                return True
            return False
