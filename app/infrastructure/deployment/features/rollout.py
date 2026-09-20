"""Feature Rollout Manager and Dynamic Flag Evaluator."""

from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import threading

from .flags import FeatureFlag, RolloutRule


class FeatureRolloutManager:
    """Manages feature flags, progressive rollouts, and instant kill switches."""

    def __init__(self) -> None:
        self._flags: Dict[str, FeatureFlag] = {}
        self._lock = threading.RLock()

    def create_flag(self, flag_key: str, name: str, description: str = "", default_enabled: bool = False) -> FeatureFlag:
        """Create a new feature flag."""
        with self._lock:
            flag = FeatureFlag(
                flag_key=flag_key,
                name=name,
                description=description,
                enabled=default_enabled,
                rules=[RolloutRule()],
            )
            self._flags[flag_key] = flag
            return flag

    def set_kill_switch(self, flag_key: str, active: bool = True) -> bool:
        """Instantly kill a feature flag globally."""
        with self._lock:
            flag = self._flags.get(flag_key)
            if flag:
                flag.kill_switch_active = active
                flag.updated_at = datetime.now(timezone.utc)
                return True
            return False

    def is_feature_enabled(
        self,
        flag_key: str,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        environment: str = "prod",
    ) -> bool:
        """Evaluate whether feature is active for the given request context."""
        with self._lock:
            flag = self._flags.get(flag_key)

        if not flag or not flag.enabled or flag.kill_switch_active:
            return False

        if not flag.rules:
            return True

        for rule in flag.rules:
            # Environment check
            if "*" not in rule.target_environments and environment not in rule.target_environments:
                continue

            # Specific user check
            if user_id and rule.target_users and user_id in rule.target_users:
                return True

            # Tenant check
            if tenant_id and "*" not in rule.target_tenants and tenant_id not in rule.target_tenants:
                continue

            # Percentage rollout bucket check
            if rule.percentage < 100.0:
                entity = tenant_id or user_id or "anonymous"
                bucket = self._hash_bucket(f"{flag_key}:{entity}")
                if bucket > rule.percentage:
                    continue

            return True

        return False

    def _hash_bucket(self, key: str) -> float:
        """Compute consistent deterministic bucket 0.0 - 100.0 for rollout partitioning."""
        h = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
        return float(h % 10000) / 100.0
