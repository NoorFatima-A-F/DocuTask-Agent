"""Declarative Certification Policy Engine."""

from typing import Dict, Any, List, Optional
from enterprise_audit_engine.certification_authority.domain.models import (
    CertificationRecord,
    EQIBreakdown,
)


class CertificationPolicyEngine:
    """Evaluates audit results against configurable declarative certification policies."""

    DEFAULT_POLICIES: Dict[str, Dict[str, Any]] = {
        "enterprise_grade": {
            "minimum_confidence": "HIGH",
            "required_domains": ["runtime", "security", "testing", "reproducibility"],
            "forbidden_critical_findings": True,
            "minimum_eqi": 85.0,
            "max_unsupported_claims": 0,
        },
        "standard_grade": {
            "minimum_confidence": "MEDIUM",
            "required_domains": ["security", "testing"],
            "forbidden_critical_findings": True,
            "minimum_eqi": 70.0,
            "max_unsupported_claims": 0,
        },
        "strict_regulated": {
            "minimum_confidence": "VERY_HIGH",
            "required_domains": ["runtime", "security", "testing", "reproducibility", "governance"],
            "forbidden_critical_findings": True,
            "minimum_eqi": 92.0,
            "max_unsupported_claims": 0,
        },
    }

    @classmethod
    def evaluate_policy(
        cls,
        policy_name: str,
        overall_confidence: str,
        overall_classification: str,
        critical_findings: List[str],
        eqi: EQIBreakdown,
        is_reproducible: bool,
        active_domains: List[str],
        unsupported_claims_count: int = 0,
        custom_policy: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        policy = custom_policy or cls.DEFAULT_POLICIES.get(policy_name, cls.DEFAULT_POLICIES["enterprise_grade"])
        violations: List[str] = []

        # 1. Critical findings check
        if policy.get("forbidden_critical_findings", True) and (len(critical_findings) > 0 or overall_classification == "CRITICAL_FINDING"):
            violations.append(f"Forbidden critical findings detected ({len(critical_findings)} findings).")

        # 2. Minimum EQI check
        min_eqi = policy.get("minimum_eqi", 80.0)
        if eqi.total_eqi < min_eqi:
            violations.append(f"EQI score {eqi.total_eqi} is below policy minimum {min_eqi}.")

        # 3. Reproducibility check
        if "reproducibility" in policy.get("required_domains", []) and not is_reproducible:
            violations.append("Reproducibility is required by policy but audit runs are non-deterministic.")

        # 4. Required domains check (case-insensitive substring match against collected categories)
        for req_dom in policy.get("required_domains", []):
            if req_dom != "reproducibility":
                matches = any(req_dom.lower() in d.lower() for d in active_domains)
                if not matches:
                    violations.append(f"Required domain '{req_dom}' missing from verified audit evidence.")

        # 5. Unsupported claims check
        max_unsupported = policy.get("max_unsupported_claims", 0)
        if unsupported_claims_count > max_unsupported:
            violations.append(f"Found {unsupported_claims_count} unsupported claims (policy max allowed: {max_unsupported}).")

        passed = len(violations) == 0
        return {
            "policy_name": policy_name,
            "passed": passed,
            "violations_count": len(violations),
            "violations": violations,
            "policy_rules": policy,
        }
