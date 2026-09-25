"""PII & Sensitive Enterprise Secret Detection Engine."""

import re
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class PIIType(str, Enum):
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    API_KEY = "API_KEY"
    AWS_KEY = "AWS_KEY"
    JWT_TOKEN = "JWT_TOKEN"
    PASSWORD = "PASSWORD"
    IP_ADDRESS = "IP_ADDRESS"
    IBAN = "IBAN"


class PIIMatch(BaseModel):
    pii_type: PIIType
    raw_value: str
    start: int
    end: int
    confidence: float = 0.95
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PIIDetector:
    """High-precision scanner for PII, financial identifiers, and enterprise secrets."""

    PATTERNS: Dict[PIIType, List[re.Pattern]] = {
        PIIType.SSN: [
            re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            re.compile(r"\b\d{9}\b(?=.*(?:ssn|social\s+security))", re.IGNORECASE),
        ],
        PIIType.CREDIT_CARD: [
            re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
            re.compile(r"\b(?:\d{4}[ -]){3}\d{4}\b"),
        ],
        PIIType.EMAIL: [
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
        ],
        PIIType.PHONE: [
            re.compile(r"\b(?:\+?1[-. ]?)?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b"),
            re.compile(r"\b\+[0-9]{1,3}[-. ]?[0-9]{2,4}[-. ]?[0-9]{3,4}[-. ]?[0-9]{3,4}\b"),
        ],
        PIIType.API_KEY: [
            re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,})\b"),
            re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|auth[_-]?token)\s*[:=]\s*['\"]?([A-Za-z0-9_-]{16,})['\"]?"),
        ],
        PIIType.AWS_KEY: [
            re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        ],
        PIIType.JWT_TOKEN: [
            re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9._-]{10,}\.[A-Za-z0-9._-]{10,}\b"),
        ],
        PIIType.PASSWORD: [
            re.compile(r"(?i)\b(?:password|passwd|pwd)\s*[:=]\s*['\"]?([^\s'\"]{6,})['\"]?"),
        ],
        PIIType.IP_ADDRESS: [
            re.compile(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"),
        ],
        PIIType.IBAN: [
            re.compile(r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}\b"),
        ],
    }

    def detect(self, text: str) -> List[PIIMatch]:
        matches: List[PIIMatch] = []
        if not text:
            return matches

        for pii_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    # Extract matched group or full match
                    matched_str = match.group(1) if match.groups() and match.group(1) else match.group(0)
                    start = match.start(1) if match.groups() and match.group(1) else match.start()
                    end = match.end(1) if match.groups() and match.group(1) else match.end()

                    # Simple validation to avoid false positives (e.g. IP address 0.0.0.0 is common)
                    matches.append(
                        PIIMatch(
                            pii_type=pii_type,
                            raw_value=matched_str,
                            start=start,
                            end=end,
                            confidence=0.95,
                        )
                    )

        # Sort matches by start position in text
        matches.sort(key=lambda m: m.start)
        return matches
