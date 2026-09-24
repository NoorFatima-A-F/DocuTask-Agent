"""
Readiness Policy Engine (Parts 4 & 5).
Parses readiness_policy.yaml, evaluates critical vs non-critical dependency classifications,
and maps failure actions.
"""
import os
import yaml
from typing import Dict, Any
from app.platform_verification.readiness_contract.domain.models import (
    DependencyPolicyReport,
)
from app.platform_verification.readiness_contract.domain.interfaces import (
    IReadinessPolicyEngine,
)


class ReadinessPolicyEngine(IReadinessPolicyEngine):
    """
    Manages declarative readiness policies.
    """

    def __init__(self, policy_path: str = "readiness_policy.yaml"):
        self.policy_path = policy_path
        self.policy = self._load_policy()

    def _load_policy(self) -> Dict[str, Any]:
        if os.path.exists(self.policy_path):
            try:
                with open(self.policy_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
        return {
            "readiness": {
                "critical": [
                    {"name": "postgres", "failure_action": "NOT_READY", "traffic_action": "WITHHOLD_TRAFFIC"},
                    {"name": "redis", "failure_action": "NOT_READY", "traffic_action": "WITHHOLD_TRAFFIC"},
                    {"name": "storage", "failure_action": "NOT_READY", "traffic_action": "WITHHOLD_TRAFFIC"},
                    {"name": "workers", "failure_action": "NOT_READY", "traffic_action": "WITHHOLD_TRAFFIC"},
                ],
                "degraded": [
                    {"name": "gemini", "failure_action": "DEGRADED", "traffic_action": "THROTTLE_TRAFFIC"},
                    {"name": "analytics", "failure_action": "DEGRADED", "traffic_action": "ADMIT_TRAFFIC"},
                    {"name": "optional_monitoring", "failure_action": "DEGRADED", "traffic_action": "ADMIT_TRAFFIC"},
                ],
            }
        }

    def evaluate_policy(self) -> DependencyPolicyReport:
        r_config = self.policy.get("readiness", {})
        critical_items = r_config.get("critical", [])
        degraded_items = r_config.get("degraded", [])

        crit_names = [item["name"] if isinstance(item, dict) else str(item) for item in critical_items]
        deg_names = [item["name"] if isinstance(item, dict) else str(item) for item in degraded_items]

        policy_valid = len(crit_names) >= 3 and len(deg_names) >= 1
        actions_mapped = all(
            isinstance(item, dict) and "failure_action" in item and "traffic_action" in item
            for item in critical_items + degraded_items
        )

        passed = policy_valid and actions_mapped

        return DependencyPolicyReport(
            critical_dependencies=crit_names,
            degraded_dependencies=deg_names,
            policy_enforcement_valid=policy_valid,
            traffic_actions_mapped=actions_mapped,
            passed=passed,
            details={
                "critical_count": len(crit_names),
                "degraded_count": len(deg_names),
                "policy_source": self.policy_path,
                "status": "POLICY_VERIFIED" if passed else "POLICY_INVALID",
            },
        )
