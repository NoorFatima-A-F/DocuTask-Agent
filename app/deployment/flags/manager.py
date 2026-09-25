"""Enterprise Feature Flag Management Platform."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from ..core.exceptions import FlagException
from .evaluation import FlagEvaluationContext, FlagEvaluator


@dataclass
class FeatureFlag:
    """Feature flag definition and rollout rule set."""
    key: str
    name: str
    description: str = ""
    enabled: bool = False
    kill_switched: bool = False
    allowed_tenants: List[str] = field(default_factory=list)
    allowed_environments: List[str] = field(default_factory=list)
    rollout_percentage: int = 100
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes feature flag to dictionary."""
        return {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "kill_switched": self.kill_switched,
            "allowed_tenants": self.allowed_tenants,
            "allowed_environments": self.allowed_environments,
            "rollout_percentage": self.rollout_percentage,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }


class FeatureFlagManager:
    """Central repository and evaluation gateway for platform feature flags."""

    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}
        self._evaluation_counts: Dict[str, int] = {}

    def create_flag(
        self,
        key: str,
        name: str,
        description: str = "",
        enabled: bool = False,
        allowed_tenants: Optional[List[str]] = None,
        allowed_environments: Optional[List[str]] = None,
        rollout_percentage: int = 100,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> FeatureFlag:
        """Registers a new feature flag."""
        if key in self._flags:
            raise FlagException(f"Feature flag with key '{key}' already exists")

        flag = FeatureFlag(
            key=key,
            name=name,
            description=description,
            enabled=enabled,
            allowed_tenants=allowed_tenants or [],
            allowed_environments=allowed_environments or [],
            rollout_percentage=max(0, min(100, rollout_percentage)),
            tags=tags or [],
            metadata=metadata or {},
        )
        self._flags[key] = flag
        return flag

    def get_flag(self, key: str) -> Optional[FeatureFlag]:
        """Retrieves feature flag by key."""
        return self._flags.get(key)

    def list_flags(self, tag: Optional[str] = None) -> List[FeatureFlag]:
        """Lists all feature flags, optionally filtered by tag."""
        flags = list(self._flags.values())
        if tag:
            flags = [f for f in flags if tag in f.tags]
        return sorted(flags, key=lambda f: f.key)

    def update_flag(
        self,
        key: str,
        enabled: Optional[bool] = None,
        rollout_percentage: Optional[int] = None,
        allowed_tenants: Optional[List[str]] = None,
        allowed_environments: Optional[List[str]] = None,
    ) -> FeatureFlag:
        """Updates feature flag configuration."""
        flag = self.get_flag(key)
        if not flag:
            raise FlagException(f"Feature flag '{key}' not found")

        if enabled is not None:
            flag.enabled = enabled
        if rollout_percentage is not None:
            flag.rollout_percentage = max(0, min(100, rollout_percentage))
        if allowed_tenants is not None:
            flag.allowed_tenants = allowed_tenants
        if allowed_environments is not None:
            flag.allowed_environments = allowed_environments

        flag.updated_at = datetime.now(timezone.utc)
        return flag

    def delete_flag(self, key: str) -> bool:
        """Deletes feature flag."""
        if key in self._flags:
            del self._flags[key]
            return True
        return False

    def activate_kill_switch(self, key: str, reason: str = "Emergency disable") -> FeatureFlag:
        """Instantly disables feature flag via kill switch."""
        flag = self.get_flag(key)
        if not flag:
            raise FlagException(f"Feature flag '{key}' not found")
        flag.kill_switched = True
        flag.metadata["kill_switch_reason"] = reason
        flag.metadata["kill_switch_activated_at"] = datetime.now(timezone.utc).isoformat()
        flag.updated_at = datetime.now(timezone.utc)
        return flag

    def deactivate_kill_switch(self, key: str) -> FeatureFlag:
        """Deactivates kill switch restoring normal rule evaluation."""
        flag = self.get_flag(key)
        if not flag:
            raise FlagException(f"Feature flag '{key}' not found")
        flag.kill_switched = False
        flag.metadata.pop("kill_switch_reason", None)
        flag.updated_at = datetime.now(timezone.utc)
        return flag

    def is_enabled(
        self,
        key: str,
        context: Optional[FlagEvaluationContext] = None,
        default: bool = False,
    ) -> bool:
        """Evaluates flag status against given context."""
        flag = self.get_flag(key)
        if not flag:
            return default

        self._evaluation_counts[key] = self._evaluation_counts.get(key, 0) + 1
        ctx = context or FlagEvaluationContext()

        return FlagEvaluator.evaluate_rule(
            flag_key=flag.key,
            enabled=flag.enabled,
            kill_switched=flag.kill_switched,
            allowed_tenants=flag.allowed_tenants,
            allowed_environments=flag.allowed_environments,
            rollout_percentage=flag.rollout_percentage,
            context=ctx,
        )

    def export_flags(self) -> Dict[str, Any]:
        """Exports all flag definitions to dictionary."""
        return {key: flag.to_dict() for key, flag in self._flags.items()}

    def import_flags(self, flags_data: Dict[str, Any]) -> int:
        """Imports flag definitions from dictionary."""
        count = 0
        for key, data in flags_data.items():
            self._flags[key] = FeatureFlag(
                key=key,
                name=data.get("name", key),
                description=data.get("description", ""),
                enabled=data.get("enabled", False),
                kill_switched=data.get("kill_switched", False),
                allowed_tenants=data.get("allowed_tenants", []),
                allowed_environments=data.get("allowed_environments", []),
                rollout_percentage=data.get("rollout_percentage", 100),
                tags=data.get("tags", []),
                metadata=data.get("metadata", {}),
            )
            count += 1
        return count
