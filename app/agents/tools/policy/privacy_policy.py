"""
Privacy Policy and PII Masking Engine for Advanced Tool Policy.
Detects, redacts, and tokenizes personally identifiable information (PII) and protected health information (PHI).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Pattern


@dataclass
class PIIMaskResult:
    """Result of privacy data scrubbing."""

    sanitized_text: str
    detected_pii_types: List[str] = field(default_factory=list)
    replacement_count: int = 0
    token_mapping: Dict[str, str] = field(default_factory=dict)


class PrivacyPolicy:
    """Identifies and scrubs sensitive personal entities from tool inputs."""

    # High-precision regular expressions for sensitive entities
    PATTERNS: Dict[str, Pattern] = {
        "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "CREDIT_CARD": re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b"),
        "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
        "PHONE": re.compile(r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b"),
        "DOB": re.compile(r"\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/(?:19|20)\d{2}\b"),
    }

    @classmethod
    def mask_pii(cls, text: str, salt: str = "TOKEN") -> PIIMaskResult:
        """Replaces all detected PII entities with deterministic synthetic tokens."""
        sanitized = text
        detected: List[str] = []
        token_map: Dict[str, str] = {}
        counter = 0

        for pii_type, regex in cls.PATTERNS.items():
            matches = list(regex.finditer(sanitized))
            if matches:
                detected.append(pii_type)
                for m in reversed(matches):  # reverse order to preserve string indices
                    val = m.group(0)
                    if val not in token_map:
                        counter += 1
                        token = f"[{pii_type}_{salt}_{counter}]"
                        token_map[val] = token
                    else:
                        token = token_map[val]
                    sanitized = sanitized[:m.start()] + token + sanitized[m.end():]

        return PIIMaskResult(
            sanitized_text=sanitized,
            detected_pii_types=detected,
            replacement_count=counter,
            token_mapping=token_map,
        )

    @classmethod
    def contains_pii(cls, text: str) -> bool:
        """Fast check for existence of any PII."""
        return any(regex.search(text) is not None for regex in cls.PATTERNS.values())
