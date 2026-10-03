"""
Infrastructure as Code (IaC) Validator.
"""
from typing import List, Dict, Any
from app.platform_verification.deployment_verification.domain.models import IacValidationReport
from app.platform_verification.deployment_verification.domain.interfaces import IIacValidator


class IacValidator(IIacValidator):
    """Validates declarative IaC definitions (Docker Compose, Terraform, K8s)."""

    def validate_iac(self, iac_manifests: List[Dict[str, Any]]) -> IacValidationReport:
        issues: List[str] = []
        idempotent = True

        for m in iac_manifests:
            framework = m.get("framework", "docker_compose")
            if not m.get("has_networking", True):
                issues.append(f"{framework}: networking definition missing")
            if not m.get("has_healthcheck", True):
                issues.append(f"{framework}: healthcheck definition missing")
            if not m.get("idempotent_recreation", True):
                idempotent = False

        status = "PASS" if len(issues) == 0 and idempotent else "FAIL"

        return IacValidationReport(
            framework="Multi-IaC (Compose/K8s/Terraform)",
            is_valid=(len(issues) == 0),
            idempotent_recreation_verified=idempotent,
            validation_issues=issues,
            status=status,
        )
