"""Report Truth Validation & Claim Verification Engine."""

from typing import List, Dict, Any, Tuple
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceSourceType,
    AuditFinding,
)


class UnsupportedClaimError(Exception):
    """Raised when an audit claim lacks backing evidence or exceeds allowable evidence strength."""
    pass


class ClaimValidator:
    """Validates that every claim and finding is strictly justified by verified evidence."""

    DISALLOWED_UNPROVEN_TERMS = [
        "100% secure",
        "zero vulnerabilities guaranteed",
        "production verified without tests",
        "fully autonomous without human review",
    ]

    @classmethod
    def validate_claim(cls, finding: AuditFinding, records: List[EvidenceRecord]) -> Tuple[bool, str]:
        """Validates a single finding against the pool of evidence records."""
        # 1. Check for banned marketing hype
        for term in cls.DISALLOWED_UNPROVEN_TERMS:
            if term in finding.claim.lower():
                return False, f"Unsupported claim contains unprovable assertion: '{term}'"

        # 2. Check evidence IDs exist
        matching_records = [r for r in records if r.id in finding.evidence_ids]
        if not matching_records:
            return False, f"Finding '{finding.finding_id}' references non-existent evidence IDs: {finding.evidence_ids}"

        # 3. Production Ready rule: Cannot be VERIFIED_BY_EXECUTION without runtime evidence
        if finding.classification == EvidenceClassification.VERIFIED_BY_EXECUTION:
            has_runtime = any(r.source_type == EvidenceSourceType.RUNTIME_EXECUTION for r in matching_records)
            if not has_runtime:
                return False, f"Finding '{finding.finding_id}' claims VERIFIED_BY_EXECUTION without RUNTIME_EXECUTION evidence."

        # 4. Claim Promotion rule: Cannot claim VERIFIED if all backing records are EVIDENCE_INSUFFICIENT or NOT_VERIFIED
        verified_classes = {
            EvidenceClassification.VERIFIED,
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
            EvidenceClassification.VERIFIED_BY_EXECUTION,
        }
        insufficient_classes = {
            EvidenceClassification.EVIDENCE_INSUFFICIENT,
            EvidenceClassification.NOT_VERIFIED,
            EvidenceClassification.DOCUMENTATION_ONLY,
            EvidenceClassification.UNKNOWN,
        }
        if finding.classification in verified_classes:
            if all(r.classification in insufficient_classes for r in matching_records):
                return False, f"Finding '{finding.finding_id}' claims '{finding.classification.value}' but backing evidence is insufficient."

        return True, "Valid"

    @classmethod
    def validate_all_findings(cls, findings: List[AuditFinding], records: List[EvidenceRecord]) -> Dict[str, Any]:
        """Validates all findings before allowing report generation."""
        violations: List[str] = []

        for f in findings:
            is_valid, msg = cls.validate_claim(f, records)
            if not is_valid:
                violations.append(msg)

        if violations:
            raise UnsupportedClaimError(f"Report generation blocked due to unsupported claims:\n" + "\n".join(violations))

        return {
            "valid": True,
            "total_findings_validated": len(findings),
            "status": "CLAIMS_FULLY_EVIDENCED",
        }
