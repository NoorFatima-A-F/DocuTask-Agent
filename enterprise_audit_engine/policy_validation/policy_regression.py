"""Policy Regression & Downgrade Detection Engine."""

from typing import Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class PolicyRegressionReport(BaseModel):
    """Report detailing detected policy weakening or certification threshold relaxations."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    has_regression: bool
    regressions_count: int
    regressions: List[str] = Field(default_factory=list)
    status: str  # NO_REGRESSION, CRITICAL_POLICY_DOWNGRADE


class PolicyRegressionDetector:
    """Detects dangerous policy relaxations and classification downgrades."""

    CONFIDENCE_HIERARCHY = {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "VERY_HIGH": 4}

    @classmethod
    def check_policy_regression(
        cls,
        base_policy: Dict[str, Any],
        proposed_policy: Dict[str, Any],
    ) -> PolicyRegressionReport:
        regressions: List[str] = []

        # 1. Minimum Confidence Downgrade
        base_conf = base_policy.get("minimum_confidence", "HIGH")
        prop_conf = proposed_policy.get("minimum_confidence", "HIGH")
        if cls.CONFIDENCE_HIERARCHY.get(prop_conf, 0) < cls.CONFIDENCE_HIERARCHY.get(base_conf, 0):
            regressions.append(f"Minimum confidence downgraded from {base_conf} to {prop_conf}.")

        # 2. Minimum EQI Threshold Lowering
        base_eqi = base_policy.get("minimum_eqi", 85.0)
        prop_eqi = proposed_policy.get("minimum_eqi", 85.0)
        if prop_eqi < base_eqi:
            regressions.append(f"Minimum EQI score lowered from {base_eqi} to {prop_eqi}.")

        # 3. Forbidden Critical Findings Bypass
        if base_policy.get("forbidden_critical_findings", True) and not proposed_policy.get("forbidden_critical_findings", True):
            regressions.append("Forbidden critical findings constraint was disabled.")

        # 4. Required Domains Omission
        base_domains = set(base_policy.get("required_domains", []))
        prop_domains = set(proposed_policy.get("required_domains", []))
        missing_domains = base_domains - prop_domains
        if missing_domains:
            regressions.append(f"Mandatory evidence domains removed: {sorted(list(missing_domains))}")

        # 5. Max Unsupported Claims Expansion
        base_max_un = base_policy.get("max_unsupported_claims", 0)
        prop_max_un = proposed_policy.get("max_unsupported_claims", 0)
        if prop_max_un > base_max_un:
            regressions.append(f"Max allowed unsupported claims increased from {base_max_un} to {prop_max_un}.")

        has_reg = len(regressions) > 0
        return PolicyRegressionReport(
            has_regression=has_reg,
            regressions_count=len(regressions),
            regressions=regressions,
            status="CRITICAL_POLICY_DOWNGRADE" if has_reg else "NO_REGRESSION",
        )
