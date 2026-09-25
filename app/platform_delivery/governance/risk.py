"""Release Risk Assessment Engine (Req 53)."""
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ReleaseRiskEvaluator:
    """Evaluates multi-variable risk metrics to determine approval rigor."""

    @classmethod
    def evaluate_risk(
        cls,
        has_database_migration: bool = False,
        has_auth_changes: bool = False,
        has_agent_autonomy_changes: bool = False,
        has_model_provider_changes: bool = False,
        test_coverage_pct: float = 95.0,
        historical_failure_rate: float = 0.02,
        components_changed_count: int = 1,
    ) -> RiskLevel:
        score = 0
        if has_database_migration:
            score += 3
        if has_auth_changes:
            score += 4
        if has_agent_autonomy_changes:
            score += 3
        if has_model_provider_changes:
            score += 2
        if test_coverage_pct < 90.0:
            score += 2
        if historical_failure_rate > 0.05:
            score += 2
        if components_changed_count > 3:
            score += 2

        if score >= 7:
            return RiskLevel.CRITICAL
        elif score >= 4:
            return RiskLevel.HIGH
        elif score >= 2:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
