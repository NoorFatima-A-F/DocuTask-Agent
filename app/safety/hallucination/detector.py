"""Hallucination Detector for Unsupported Claims & Numeric Inconsistencies."""

import re
from typing import List, Tuple
from ..gateway.context import KnowledgeChunk
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from .grounding import GroundingVerifier
from .confidence import GroundingReport


class HallucinationDetector:
    """Detects hallucinations, invented numeric figures, and unsupported statements."""

    def __init__(self, grounding_verifier: GroundingVerifier = None):
        self.grounding_verifier = grounding_verifier or GroundingVerifier()

    def check_numeric_hallucinations(
        self,
        output_text: str,
        knowledge_chunks: List[KnowledgeChunk],
    ) -> List[SafetyViolation]:
        """Detects numbers/currencies in output that do not appear in source documents."""
        violations: List[SafetyViolation] = []
        if not output_text or not knowledge_chunks:
            return violations

        combined_chunk_text = " ".join([c.content for c in knowledge_chunks])
        
        # Extract currency amounts and distinct numbers
        output_numbers = re.findall(r"\$?\b\d+(?:,\d{3})*(?:\.\d+)?\b", output_text)
        chunk_numbers = set(re.findall(r"\$?\b\d+(?:,\d{3})*(?:\.\d+)?\b", combined_chunk_text))

        for num in output_numbers:
            # Skip trivial numbers (0, 1, 2)
            if num in ["0", "1", "2"]:
                continue
            if num not in chunk_numbers:
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.HALLUCINATION,
                        severity=ViolationSeverity.HIGH,
                        message=f"Invented numeric figure '{num}' not found in source documents",
                        location="output",
                        rule_id="HAL-NUM-001",
                        evidence=num,
                    )
                )

        return violations

    def detect(
        self,
        output_text: str,
        knowledge_chunks: List[KnowledgeChunk],
    ) -> Tuple[bool, List[SafetyViolation], GroundingReport]:
        violations: List[SafetyViolation] = []

        if not knowledge_chunks:
            # Nothing to ground against
            return False, violations, GroundingReport(is_grounded=True, grounding_score=1.0, total_claims=0, grounded_claims=0)

        # 1. Check numeric hallucinations
        num_violations = self.check_numeric_hallucinations(output_text, knowledge_chunks)
        violations.extend(num_violations)

        # 2. Grounding verification
        report = self.grounding_verifier.verify_grounding(output_text, knowledge_chunks)
        if not report.is_grounded:
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.GROUNDING_FAILURE,
                    severity=ViolationSeverity.HIGH,
                    message=f"Output grounding failure: score {report.grounding_score:.2f} is below 0.70 threshold ({report.grounded_claims}/{report.total_claims} claims grounded)",
                    location="output",
                    rule_id="HAL-GRND-001",
                    details={"grounding_score": report.grounding_score, "ungrounded_claims": [c.claim_text for c in report.ungrounded_claims]},
                )
            )

        is_hallucinated = len(violations) > 0
        return is_hallucinated, violations, report
