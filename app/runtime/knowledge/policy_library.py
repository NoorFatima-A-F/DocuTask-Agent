"""Planning Policy Library & Repository for DocuTask ADIP.

Stores compiled, versioned planning policies distilled from organizational experience.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlanningPolicy(BaseModel):
    """Compiled executable planning policy."""
    policy_id: str = Field(default_factory=lambda: f"pol_{uuid.uuid4().hex[:8]}")
    name: str
    version: str = "1.0.0"
    domain: str = "FINANCIAL_DOCUMENT_OPERATIONS"
    archetype_preference: str = "DELTA_PARETO"
    default_concurrency: int = 8
    heuristic_rule_ids: List[str] = Field(default_factory=list)
    verification_invariants: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyLibrary:
    """Versioned repository of distilled organizational policies."""

    def __init__(self) -> None:
        self._policies: Dict[str, PlanningPolicy] = {}
        self._initialize_default_policies()

    def _initialize_default_policies(self) -> None:
        self.register_policy(
            PlanningPolicy(
                policy_id="pol_default_enterprise",
                name="Enterprise Standard Pareto Policy",
                version="2.1.0",
                domain="ENTERPRISE_CORE",
                archetype_preference="DELTA_PARETO",
                default_concurrency=8,
                verification_invariants=["budget_usd <= 0.50", "sla_ms <= 10000", "accuracy >= 0.90"],
            )
        )
        self.register_policy(
            PlanningPolicy(
                policy_id="pol_strict_audit",
                name="High-Assurance Financial Compliance Policy",
                version="1.4.0",
                domain="FINANCIAL_AUDIT",
                archetype_preference="BETA_ACCURATE",
                default_concurrency=4,
                verification_invariants=["accuracy >= 0.99", "formal_smt_verified == 1.0", "zero_pii_leakage == 1.0"],
            )
        )

    def register_policy(self, policy: PlanningPolicy) -> None:
        self._policies[policy.policy_id] = policy

    def get_policy(self, policy_id: str) -> Optional[PlanningPolicy]:
        return self._policies.get(policy_id)

    def list_policies(self) -> List[PlanningPolicy]:
        return list(self._policies.values())
