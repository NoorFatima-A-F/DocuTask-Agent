"""Data & System Prompt Leakage Detector."""

import re
from typing import List, Tuple, Optional
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from ..privacy.pii_detector import PIIDetector


class DataLeakageDetector:
    """Detects leaked system instructions, DB connection strings, credentials, and sensitive assets in AI output."""

    LEAKAGE_PATTERNS: List[Tuple[re.Pattern, str, ViolationSeverity]] = [
        # Database URIs
        (re.compile(r"\b(postgres(?:ql)?|mongodb(?:\+srv)?|mysql|redis)://[^\s:]+:[^\s@]+@[^\s/]+/[^\s]+", re.IGNORECASE), "Database connection URI with credentials leaked", ViolationSeverity.CRITICAL),
        # Cloud Private Keys & Certs
        (re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"), "Cryptographic private key leaked", ViolationSeverity.CRITICAL),
        # Internal IP / Endpoint
        (re.compile(r"\b(https?://)?(?:10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}(?::\d+)?\b"), "Internal RFC-1918 private IP address leaked", ViolationSeverity.HIGH),
        # System Prompt Leakage signatures
        (re.compile(r"(?i)\b(my\s+system\s+instructions\s+are|I\s+was\s+instructed\s+to\s+always|the\s+hidden\s+prompt\s+is)\s*:"), "System prompt leakage statement", ViolationSeverity.HIGH),
    ]

    def __init__(self, pii_detector: PIIDetector = None):
        self.pii_detector = pii_detector or PIIDetector()

    def scan(
        self,
        output_text: str,
        system_prompt: Optional[str] = None,
    ) -> Tuple[bool, List[SafetyViolation]]:
        violations: List[SafetyViolation] = []
        if not output_text:
            return False, violations

        # 1. Check regex leakage patterns
        for pattern, desc, severity in self.LEAKAGE_PATTERNS:
            match = pattern.search(output_text)
            if match:
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.SECRET_LEAKAGE,
                        severity=severity,
                        message=desc,
                        location="output",
                        rule_id="LEAK-PAT-001",
                        evidence=match.group(0)[:80],
                    )
                )

        # 2. Check PII in output
        pii_matches = self.pii_detector.detect(output_text)
        for pii in pii_matches:
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.PII_LEAKAGE,
                    severity=ViolationSeverity.HIGH,
                    message=f"PII of type '{pii.pii_type.value}' leaked in model output",
                    location="output",
                    rule_id="LEAK-PII-001",
                    evidence=pii.raw_value[:50],
                )
            )

        # 3. Verbatim system prompt echoing check
        if system_prompt and len(system_prompt.strip()) > 30:
            sys_clean = " ".join(system_prompt.strip().split()[:15]).lower()
            if sys_clean in output_text.lower():
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.SECRET_LEAKAGE,
                        severity=ViolationSeverity.CRITICAL,
                        message="Direct system prompt verbatim regurgitation detected",
                        location="output",
                        rule_id="LEAK-SYS-001",
                    )
                )

        is_leaking = len(violations) > 0
        return is_leaking, violations
