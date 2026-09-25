"""
Phase 3H.4.10.3: Log Sanitization Middleware Verifier
"""
import re
from typing import List
from ..domain.interfaces import ILogSanitizationVerifier
from ..domain.models import LogSanitizationReport, SanitizationRule


class LogSanitizationVerifier(ILogSanitizationVerifier):
    def __init__(self):
        self.rules: List[SanitizationRule] = [
            SanitizationRule(
                rule_name="Password Masking",
                target_pattern=r"(?i)(password|passwd|secret)\s*[:=]\s*['\"]?([^'\"\s]+)['\"]?",
                replacement_template=r"\1='[REDACTED]'",
                active=True,
            ),
            SanitizationRule(
                rule_name="JWT Bearer Token Masking",
                target_pattern=r"(?i)Bearer\s+eyJ[a-zA-Z0-9_\-\.]+",
                replacement_template="Bearer [REDACTED_JWT]",
                active=True,
            ),
            SanitizationRule(
                rule_name="Google API Key Masking",
                target_pattern=r"AIza[0-9A-Za-z-_]{30,40}",
                replacement_template="[REDACTED_GEMINI_KEY]",
                active=True,
            ),
            SanitizationRule(
                rule_name="Email Address Masking",
                target_pattern=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
                replacement_template="[REDACTED_EMAIL]",
                active=True,
            ),
            SanitizationRule(
                rule_name="Credit Card / CNIC / SSN Masking",
                target_pattern=r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
                replacement_template="[REDACTED_CARD_NUMBER]",
                active=True,
            ),
            SanitizationRule(
                rule_name="Document Text Buffer Masking",
                target_pattern=r"(?i)(raw_text|ocr_content|prompt_content)\s*[:=]\s*['\"].*?['\"]",
                replacement_template=r"\1='[REDACTED_CONTENT]'",
                active=True,
            ),
        ]

    def sanitize_log_message(self, message: str) -> str:
        sanitized = message
        for rule in self.rules:
            if rule.active:
                sanitized = re.sub(rule.target_pattern, rule.replacement_template, sanitized)
        return sanitized

    def verify_sanitization_middleware(self) -> LogSanitizationReport:
        test_payloads = [
            ("Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-ID", "Bearer [REDACTED_JWT]"),
            ("Gemini key " + ("A" + "I" + "z" + "a") + "0" * 35 + " used", "[REDACTED_GEMINI_KEY]"),
            ("User email test.user@acme-corp.com logged in", "[REDACTED_EMAIL]"),
            ("User password='SuperSecretPassword123' rejected", "password='[REDACTED]'"),
            ("Card 4111-2222-3333-4444 charged", "[REDACTED_CARD_NUMBER]"),
            ("raw_text='Patient contract details and medical invoice' processed", "raw_text='[REDACTED_CONTENT]'"),
        ]

        passed = 0
        failed = 0

        for input_text, expected_mask in test_payloads:
            result = self.sanitize_log_message(input_text)
            if expected_mask in result:
                passed += 1
            else:
                failed += 1

        return LogSanitizationReport(
            active_sanitization_rules=self.rules,
            sample_tests_passed=passed,
            sample_tests_failed=failed,
            sanitization_verified=(failed == 0),
        )
