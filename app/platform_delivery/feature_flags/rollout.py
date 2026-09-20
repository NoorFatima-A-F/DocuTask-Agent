"""Feature Flag Rollout Engine Decoupled from Deployment (Req 50)."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib


@dataclass
class FlagEvaluationContext:
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    region: Optional[str] = None
    environment: str = "production"


class FeatureFlagRolloutEngine:
    """Evaluates percentage rollouts, tenant targeting, and emergency kill switches."""

    def __init__(self):
        self._flags: Dict[str, Dict[str, Any]] = {}

    def register_flag(
        self,
        key: str,
        enabled: bool = False,
        percentage: int = 100,
        allowed_tenants: Optional[List[str]] = None,
        allowed_regions: Optional[List[str]] = None,
        kill_switch: bool = False,
    ) -> None:
        self._flags[key] = {
            "enabled": enabled,
            "percentage": max(0, min(100, percentage)),
            "allowed_tenants": allowed_tenants or [],
            "allowed_regions": allowed_regions or [],
            "kill_switch": kill_switch,
        }

    def evaluate(self, key: str, context: FlagEvaluationContext) -> bool:
        flag = self._flags.get(key)
        if not flag or flag["kill_switch"] or not flag["enabled"]:
            return False

        if flag["allowed_tenants"] and context.tenant_id not in flag["allowed_tenants"]:
            return False

        if flag["allowed_regions"] and context.region not in flag["allowed_regions"]:
            return False

        if flag["percentage"] < 100:
            seed = f"{key}:{context.user_id or context.tenant_id or 'anon'}"
            bucket = int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16) % 100
            return bucket < flag["percentage"]

        return True
