"""Feature Flag Evaluation Engine."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib


@dataclass
class FlagEvaluationContext:
    """Evaluation context for feature flag checks."""
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    environment: str = "prod"
    attributes: Dict[str, Any] = field(default_factory=dict)


class FlagEvaluator:
    """Evaluates multi-variable targeting rules and consistent hash percentage rollouts."""

    @classmethod
    def evaluate_percentage(cls, key: str, entity_id: str, percentage: int) -> bool:
        """Determines inclusion in percentage rollout using deterministic SHA-256 hash."""
        if percentage <= 0:
            return False
        if percentage >= 100:
            return True

        hash_input = f"{key}:{entity_id}".encode("utf-8")
        digest = hashlib.sha256(hash_input).hexdigest()
        # Take first 8 chars as hex integer modulo 100
        bucket = int(digest[:8], 16) % 100
        return bucket < percentage

    @classmethod
    def evaluate_rule(
        cls,
        flag_key: str,
        enabled: bool,
        kill_switched: bool,
        allowed_tenants: List[str],
        allowed_environments: List[str],
        rollout_percentage: int,
        context: FlagEvaluationContext,
    ) -> bool:
        """Evaluates whether feature flag is enabled for the provided context."""
        # 1. Kill switch immediately disables flag
        if kill_switched:
            return False

        # 2. Master boolean toggle
        if not enabled:
            return False

        # 3. Environment filtering
        if allowed_environments and context.environment.lower() not in [e.lower() for e in allowed_environments]:
            return False

        # 4. Tenant allowlist
        if allowed_tenants:
            if not context.tenant_id or context.tenant_id not in allowed_tenants:
                return False

        # 5. Rollout percentage (hash on tenant_id or user_id)
        if rollout_percentage < 100:
            entity_id = context.user_id or context.tenant_id or "anonymous"
            return cls.evaluate_percentage(flag_key, entity_id, rollout_percentage)

        return True
