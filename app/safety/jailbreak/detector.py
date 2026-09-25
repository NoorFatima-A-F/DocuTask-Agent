"""Multi-Strategy Jailbreak Detector."""

import re
from typing import List, Tuple
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from .patterns import JailbreakPatternRegistry
from .classifier import JailbreakClassifier


class JailbreakDetector:
    """Orchestrates comprehensive jailbreak scanning against prompt inputs."""

    def __init__(self):
        self.registry = JailbreakPatternRegistry()
        self.classifier = JailbreakClassifier()

    def detect(self, text: str) -> Tuple[bool, List[SafetyViolation]]:
        violations: List[SafetyViolation] = []
        if not text:
            return False, violations

        all_pattern_groups = [
            self.registry.PERSONA_PATTERNS,
            self.registry.HYPOTHETICAL_PATTERNS,
            self.registry.ENCODING_PATTERNS,
            self.registry.COMPLIANCE_PATTERNS,
        ]

        for group in all_pattern_groups:
            for pattern, desc, severity in group:
                match = re.search(pattern, text)
                if match:
                    violations.append(
                        SafetyViolation(
                            category=SafetyCategory.JAILBREAK,
                            severity=severity,
                            message=f"Jailbreak attempt detected: {desc}",
                            location="input",
                            rule_id="JB-DET-001",
                            evidence=match.group(0)[:120],
                        )
                    )

        # Also run classifier
        classification = self.classifier.classify(text)
        if classification.is_jailbreak and not violations:
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.JAILBREAK,
                    severity=ViolationSeverity.HIGH,
                    message=f"Statistical jailbreak pattern detected (Score: {classification.probability:.2f})",
                    location="input",
                    rule_id="JB-STAT-001",
                    details={"matched_strategies": classification.matched_strategies},
                )
            )

        return len(violations) > 0, violations
