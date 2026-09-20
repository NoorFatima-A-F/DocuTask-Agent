"""
Feature Flag Governance and Evaluation Engine.
"""
from datetime import datetime, timezone
import hashlib
from typing import Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import FeatureFlag, EnvironmentTier


class FeatureFlagManager:
    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}
        self._audit_trail: List[Dict[str, Any]] = []

    def define_flag(
        self,
        flag_key: str,
        name: str,
        description: str,
        owner: str = "Platform Lead",
        is_enabled: bool = False,
        rollout_percentage: int = 100,
        enabled_environments: Optional[List[EnvironmentTier]] = None,
        allowed_tenants: Optional[List[str]] = None,
        expiration_date: Optional[str] = None
    ) -> FeatureFlag:
        flag = FeatureFlag(
            flag_key=flag_key,
            name=name,
            description=description,
            owner=owner,
            is_enabled=is_enabled,
            rollout_percentage=rollout_percentage,
            enabled_environments=enabled_environments or list(EnvironmentTier),
            allowed_tenants=allowed_tenants or [],
            expiration_date=expiration_date
        )
        self._flags[flag_key] = flag
        return flag

    def is_flag_active(
        self,
        flag_key: str,
        environment: EnvironmentTier = EnvironmentTier.PRODUCTION,
        tenant_id: Optional[str] = None,
        context_id: Optional[str] = None
    ) -> bool:
        if flag_key not in self._flags:
            return False
        flag = self._flags[flag_key]
        if not flag.is_enabled:
            return False
        if environment not in flag.enabled_environments:
            return False
        if flag.allowed_tenants and tenant_id and tenant_id not in flag.allowed_tenants:
            return False
        if flag.rollout_percentage < 100 and context_id:
            # Hash-based deterministic percentage rollout
            score = int(hashlib.md5(f"{flag_key}:{context_id}".encode("utf-8")).hexdigest(), 16) % 100
            if score >= flag.rollout_percentage:
                return False
        return True

    def set_flag_state(self, flag_key: str, is_enabled: bool, actor: str = "Admin") -> FeatureFlag:
        if flag_key not in self._flags:
            raise KeyError(f"Feature flag {flag_key} not found")
        flag = self._flags[flag_key]
        flag.is_enabled = is_enabled
        flag.updated_at = datetime.now(timezone.utc).isoformat()
        return flag

    def get_all_flags(self) -> List[FeatureFlag]:
        return list(self._flags.values())


feature_flag_manager = FeatureFlagManager()
