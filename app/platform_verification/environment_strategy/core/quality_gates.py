"""
Environment Promotion Quality Gates.
Enforces multi-tier criteria before allowing environment promotion.
"""
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.environment_strategy.domain.models import (
    EnvironmentClassification, EnvironmentQualityGateResult
)


class EnvironmentQualityGateEngine:
    def evaluate_gate(
        self,
        from_env: EnvironmentClassification,
        to_env: EnvironmentClassification,
        metrics: Dict[str, Any]
    ) -> EnvironmentQualityGateResult:
        criteria: Dict[str, bool] = {}
        blockers: List[str] = []

        if from_env == EnvironmentClassification.DEVELOPMENT:
            criteria["unit_tests_passing"] = metrics.get("unit_tests_pass_rate", 1.0) >= 1.0
            criteria["lint_static_analysis"] = metrics.get("lint_errors", 0) == 0
            if not criteria["unit_tests_passing"]:
                blockers.append("Unit tests must pass 100%")
            if not criteria["lint_static_analysis"]:
                blockers.append("Zero lint errors required")

        elif from_env == EnvironmentClassification.INTEGRATION:
            criteria["contract_tests_passed"] = metrics.get("contract_tests_passed", True)
            criteria["database_migrations_verified"] = metrics.get("migrations_verified", True)
            if not criteria["contract_tests_passed"]:
                blockers.append("Inter-service contract tests failed")

        elif from_env == EnvironmentClassification.STAGING:
            criteria["performance_latency_p95_ok"] = metrics.get("p95_latency_ms", 200.0) <= 500.0
            criteria["security_scan_clean"] = metrics.get("cve_critical_count", 0) == 0
            criteria["ai_accuracy_threshold"] = metrics.get("accuracy", 0.96) >= 0.95
            if not criteria["performance_latency_p95_ok"]:
                blockers.append("p95 Latency exceeded 500ms limit")
            if not criteria["security_scan_clean"]:
                blockers.append("Critical security vulnerabilities detected")
            if not criteria["ai_accuracy_threshold"]:
                blockers.append("AI verification accuracy below 0.95 threshold")

        is_passed = len(blockers) == 0
        score = sum(1.0 for v in criteria.values() if v) / max(1, len(criteria))

        return EnvironmentQualityGateResult(
            from_environment=from_env,
            to_environment=to_env,
            is_passed=is_passed,
            score=score,
            evaluated_criteria=criteria,
            blockers=blockers
        )


quality_gate_engine = EnvironmentQualityGateEngine()
