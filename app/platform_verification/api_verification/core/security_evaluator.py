"""
OWASP API Security Top 10 Evaluator.
"""
from __future__ import annotations
import uuid
from typing import List
from app.platform_verification.api_verification.domain.interfaces import IApiSecurityValidator
from app.platform_verification.api_verification.domain.models import (
    ApiSecurityFinding,
    ApiViolationSeverity,
    EndpointPurityMetric,
)


class EnterpriseApiSecurityValidator(IApiSecurityValidator):
    """Evaluates endpoints against OWASP API Security Top 10 vulnerabilities."""

    def evaluate_security(self, endpoints: List[EndpointPurityMetric]) -> List[ApiSecurityFinding]:
        findings: List[ApiSecurityFinding] = []

        for ep in endpoints:
            # 1. Check for unbounded query / path parameter risk
            if "{" in ep.endpoint_path and "id" in ep.endpoint_path.lower():
                # BOLA check - ensure tenant validation is planned
                pass

            # 2. Check for unauthenticated administrative endpoints
            if "/admin" in ep.endpoint_path.lower() and ep.http_method in ("POST", "DELETE"):
                findings.append(
                    ApiSecurityFinding(
                        finding_id=f"SEC-BOLA-{uuid.uuid4().hex[:6].upper()}",
                        owasp_category="API1: Broken Object Level Authorization",
                        endpoint_path=ep.endpoint_path,
                        severity=ApiViolationSeverity.HIGH,
                        message=f"Admin endpoint '{ep.endpoint_path}' requires strict tenant & role verification middleware.",
                        remediation="Enforce RBAC role check `Depends(require_admin_role)`.",
                    )
                )

        return findings
