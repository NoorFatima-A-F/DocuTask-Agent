"""Anti-Hallucination Report Protection & Claim-Evidence Matcher."""

import re
from typing import List, Dict, Any, Tuple
from enterprise_audit_engine.domain.evidence.models import EvidenceRecord


class ClaimEvidenceMatcher:
    """Guards reports against unsubstantiated claims and template hallucination."""

    PREREQUISITES: Dict[str, Dict[str, Any]] = {
        "production ready database": {
            "required_categories": ["DatabaseArchitectureAndSafety"],
            "required_source_types": ["STATIC_SOURCE_CODE"],
        },
        "enterprise security verified": {
            "required_categories": ["SecurityAndCompliance"],
            "disallowed_classifications": ["CRITICAL_FINDING"],
        },
        "ai autonomous agent verified": {
            "required_categories": ["AIEngineeringAndSafety"],
        },
    }

    BANNED_UNPROVABLE_PHRASES = [
        r"(?i)100%\s+secure",
        r"(?i)zero\s+vulnerabilities\s+guaranteed",
        r"(?i)unbreakable\s+encryption",
        r"(?i)bug-free",
        r"(?i)production\s+verified\s+without\s+tests",
    ]

    @classmethod
    def sanitize_report_text(cls, text: str, records: List[EvidenceRecord]) -> Tuple[str, List[str]]:
        """Scans report text for unproven assertions and sanitizes or flags them."""
        sanitized = text
        stripped_claims: List[str] = []
        categories = {r.category for r in records}
        {r.category: r.classification for r in records}

        # 1. Strip absolute unprovable marketing hype
        for pattern in cls.BANNED_UNPROVABLE_PHRASES:
            matches = re.findall(pattern, sanitized)
            for m in matches:
                stripped_claims.append(f"Removed banned marketing assertion: '{m}'")
                sanitized = re.sub(pattern, "[EVIDENCE_INSUFFICIENT: Unprovable Claim Removed]", sanitized)

        # 2. Check prerequisite claims
        for claim_key, rules in cls.PREREQUISITES.items():
            if claim_key in sanitized.lower():
                for req_cat in rules.get("required_categories", []):
                    if req_cat not in categories:
                        stripped_claims.append(f"Claim '{claim_key}' stripped: missing evidence category '{req_cat}'.")
                        sanitized = re.sub(
                            re.escape(claim_key),
                            f"[CLAIM_STRIPPED: Missing {req_cat} Evidence]",
                            sanitized,
                            flags=re.IGNORECASE,
                        )

        return sanitized, stripped_claims
