"""Output Factuality & Consistency Checker."""

import re
from typing import List, Tuple
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation


class FactualityChecker:
    """Detects self-contradictions and internal factual inconsistencies in generated text."""

    CONTRADICTION_PATTERNS = [
        (re.compile(r"(?i)\b(is\s+true)\b.*\b(is\s+false)\b"), "Direct logical contradiction in same passage"),
        (re.compile(r"(?i)\b(total\s+is\s+\$?\d+)\b.*\b(total\s+amount\s+is\s+\$?\d+)\b"), "Conflicting totals reported"),
    ]

    def check(self, text: str) -> Tuple[bool, List[SafetyViolation]]:
        violations: List[SafetyViolation] = []
        if not text:
            return True, violations

        # Check for simple contradictory markers
        for pattern, desc in self.CONTRADICTION_PATTERNS:
            if pattern.search(text):
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.HALLUCINATION,
                        severity=ViolationSeverity.MEDIUM,
                        message=desc,
                        location="output",
                        rule_id="FACT-001",
                    )
                )

        is_consistent = len(violations) == 0
        return is_consistent, violations
