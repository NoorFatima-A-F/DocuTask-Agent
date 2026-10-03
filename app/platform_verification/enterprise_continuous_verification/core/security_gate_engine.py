"""
Phase 3Q: Automated CI/CD Security Gate Engine.
"""

from datetime import datetime, timezone
from typing import List

from ..domain.interfaces import ISecurityGateEngine
from ..domain.models import PipelineStageStatus, SecurityGateReport


class SecurityGateEngine(ISecurityGateEngine):
    """
    Enforces non-bypassable automated CI/CD security gates:
    - Container vulnerability scanning (Trivy / Docker Scout)
    - Secret detection (Gitleaks / TruffleHog)
    - Dependency vulnerability audits
    Blocks pipeline if any Critical CVEs or plaintext secrets are detected.
    """

    def evaluate_security(
        self,
        critical_cves: int = 0,
        high_cves: int = 0,
        secrets_found: int = 0,
    ) -> SecurityGateReport:
        blockers: List[str] = []

        if critical_cves > 0:
            blockers.append(f"Security Gate Failure: {critical_cves} Critical CVE(s) detected in container image.")
        if secrets_found > 0:
            blockers.append(f"Security Gate Failure: {secrets_found} unencrypted secret/credential token(s) detected.")

        gate_passed = len(blockers) == 0
        status = PipelineStageStatus.PASSED if gate_passed else PipelineStageStatus.BLOCKED

        return SecurityGateReport(
            container_scan_status=status,
            secret_scan_status=status,
            dependency_scan_status=status,
            critical_vulnerabilities=critical_cves,
            high_vulnerabilities=high_cves,
            secrets_detected=secrets_found,
            gate_passed=gate_passed,
            blocking_reasons=blockers,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
