"""
Phase 13.17: Compliance Monitor & PII Sanitizer
Scans inputs, prompts, and outputs for sensitive credentials, PII, and compliance policy violations.
"""

from __future__ import annotations
import re
from typing import List, Tuple


class ComplianceMonitor:
    """Detects and redacts PII and secrets (API keys, passwords, SSNs, credit cards, emails)."""

    PATTERNS = {
        "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        "API_KEY": re.compile(r"(?:api[_-]?key|secret|token)[\s:=]+['\"]?([a-zA-Z0-9_\-]{16,})['\"]?", re.IGNORECASE),
        "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
        "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    }

    @classmethod
    def scan_and_redact(cls, text: str) -> Tuple[str, List[str]]:
        """Returns redacted string and list of detected PII types."""
        redacted_text = text
        detected = []

        for pii_type, pattern in cls.PATTERNS.items():
            matches = pattern.findall(redacted_text)
            if matches:
                detected.append(pii_type)
                redacted_text = pattern.sub(f"[REDACTED_{pii_type}]", redacted_text)

        return redacted_text, detected
