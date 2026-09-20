"""
Test Environment Reproducibility and Isolation Validator.
"""
from typing import Dict, Any, List
from app.platform_verification.test_architecture_verification.domain.models import EnvironmentReproducibilityReport
from app.platform_verification.test_architecture_verification.domain.interfaces import IEnvironmentValidator


class EnvironmentValidator(IEnvironmentValidator):
    """Verifies pinned dependencies, container configurations, and fixture isolation."""

    def validate_environment_reproducibility(self, env_meta: Dict[str, Any]) -> EnvironmentReproducibilityReport:
        pinned = env_meta.get("pinned_dependencies", True)
        docker = env_meta.get("docker_test_env_configured", True)
        fixtures = env_meta.get("fixture_isolation_clean", True)
        issues: List[str] = []

        score = 100.0
        if not pinned:
            score -= 30.0
            issues.append("Unpinned dependencies detected; risks non-reproducible CI runs")
        if not docker:
            score -= 20.0
            issues.append("Docker containerized test environment missing")
        if not fixtures:
            score -= 20.0
            issues.append("Shared global state detected across test fixtures")

        status = "PASS" if score >= 85.0 else "FAIL"

        return EnvironmentReproducibilityReport(
            status=status,
            pinned_dependencies_verified=pinned,
            docker_test_environment_verified=docker,
            fixture_isolation_verified=fixtures,
            reproducibility_score=score,
            issues=issues,
        )
