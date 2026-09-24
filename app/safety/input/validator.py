"""Input Safety Validator."""

from typing import List, Tuple
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from .classifier import InputIntentClassifier
from .detectors import MaliciousPatternDetector


class InputSafetyValidator:
    """Validates input payload size, encoding, structural integrity, and safety boundaries."""

    def __init__(self, max_length: int = 100_000):
        self.max_length = max_length
        self.classifier = InputIntentClassifier()
        self.detector = MaliciousPatternDetector()

    def validate(self, text: str) -> Tuple[bool, List[SafetyViolation]]:
        violations: List[SafetyViolation] = []

        if not text:
            return True, violations

        # Length check (Anti-DoS / Buffer overflow defense)
        if len(text) > self.max_length:
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.MALICIOUS_INPUT,
                    severity=ViolationSeverity.HIGH,
                    message=f"Input exceeds maximum allowed length ({len(text)} > {self.max_length})",
                    location="input",
                    rule_id="INP-LEN-001",
                )
            )

        # Null-byte / control character injection
        if "\x00" in text:
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.MALICIOUS_INPUT,
                    severity=ViolationSeverity.CRITICAL,
                    message="Null byte detected in input stream",
                    location="input",
                    rule_id="INP-NULL-001",
                    evidence="\\x00 byte present",
                )
            )

        # Malicious pattern scanner
        pattern_violations = self.detector.scan(text)
        violations.extend(pattern_violations)

        is_valid = not any(v.severity in [ViolationSeverity.HIGH, ViolationSeverity.CRITICAL] for v in violations)
        return is_valid, violations
