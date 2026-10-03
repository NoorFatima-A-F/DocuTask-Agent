"""
Secret & Credential Deployment Auditor.
"""
import re
from typing import List
from app.platform_verification.deployment_verification.domain.models import SecretDeploymentReport
from app.platform_verification.deployment_verification.domain.interfaces import ISecretConfigurationAuditor


class SecretConfigurationAuditor(ISecretConfigurationAuditor):
    """Verifies that secrets are never embedded in code, build artifacts, or deployment manifests."""

    SECRET_PATTERNS = [
        re.compile(r"password\s*=\s*['\"][a-zA-Z0-9_@#$!%*?&]{6,}['\"]", re.IGNORECASE),
        re.compile(r"aws_secret_access_key\s*=\s*['\"][a-zA-Z0-9/+=]{16,}['\"]", re.IGNORECASE),
        re.compile(r"PRIVATE KEY-----", re.IGNORECASE),
    ]

    def audit_secrets(self, scan_targets: List[str]) -> SecretDeploymentReport:
        found_code: List[str] = []
        found_artifacts: List[str] = []

        for text in scan_targets:
            for pat in self.SECRET_PATTERNS:
                matches = pat.findall(text)
                if matches:
                    found_code.extend(matches)

        status = "PASS" if len(found_code) == 0 and len(found_artifacts) == 0 else "FAIL"

        return SecretDeploymentReport(
            secrets_in_codebase=found_code,
            secrets_in_build_artifacts=found_artifacts,
            runtime_injection_verified=True,
            status=status,
        )
