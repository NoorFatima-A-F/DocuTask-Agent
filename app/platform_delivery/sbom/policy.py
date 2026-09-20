"""SBOM Security and License Compliance Policies."""
from typing import List, Set
from .generator import SBOMDocument


class SBOMPolicyEvaluator:
    """Enforces license allowlists and banned package policies."""

    DISALLOWED_LICENSES: Set[str] = {"GPL-3.0", "AGPL-3.0", "UNKNOWN"}

    @classmethod
    def evaluate_compliance(cls, sbom: SBOMDocument, allowed_licenses: Optional[Set[str]] = None) -> bool:
        disallowed = cls.DISALLOWED_LICENSES if allowed_licenses is None else set()
        for comp in sbom.components:
            if comp.license_concluded in disallowed:
                return False
            if allowed_licenses and comp.license_concluded not in allowed_licenses:
                return False
        return True
