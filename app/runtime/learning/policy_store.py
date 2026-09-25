"""
Adaptive Weight Learning - Policy Store
Version-controlled policy repository requiring explicit human sign-off before activation.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, asdict


@dataclass
class VersionedPolicy:
    version: str
    created_at_utc: str
    approved_by: Optional[str]
    weights: Dict[str, float]
    is_active: bool
    description: str


class PolicyStore:
    """Manages versioned planner policies and approval gates."""

    def __init__(self):
        self._policies: Dict[str, VersionedPolicy] = {}
        # Initial certified v1 policy
        self._policies["v1.0.0"] = VersionedPolicy(
            version="v1.0.0",
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            approved_by="System Governance Authority",
            weights={"accuracy": 0.35, "latency": 0.20, "cost": 0.15, "safety_compliance": 0.15, "reliability": 0.15},
            is_active=True,
            description="Default enterprise certified multi-objective baseline policy",
        )

    def get_active_policy(self) -> VersionedPolicy:
        for pol in self._policies.values():
            if pol.is_active:
                return pol
        return list(self._policies.values())[0]

    def register_policy(self, version: str, weights: Dict[str, float], description: str) -> VersionedPolicy:
        pol = VersionedPolicy(
            version=version,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            approved_by=None,
            weights=weights,
            is_active=False,
            description=description,
        )
        self._policies[version] = pol
        return pol

    def approve_and_activate(self, version: str, approved_by: str) -> VersionedPolicy:
        if version not in self._policies:
            raise KeyError(f"Policy version {version} does not exist.")

        # Deactivate previous
        for p in self._policies.values():
            p.is_active = False

        pol = self._policies[version]
        self._policies[version] = VersionedPolicy(
            version=pol.version,
            created_at_utc=pol.created_at_utc,
            approved_by=approved_by,
            weights=pol.weights,
            is_active=True,
            description=pol.description,
        )
        return self._policies[version]

    def list_all(self) -> List[Dict[str, Any]]:
        return [asdict(p) for p in self._policies.values()]


policy_store = PolicyStore()
