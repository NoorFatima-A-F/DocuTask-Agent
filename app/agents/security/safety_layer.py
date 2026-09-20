"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - AI Safety Layer.
Provides runtime defense against prompt injections, indirect injections,
jailbreak attempts, PII exposure, and tool abuse.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class SafetyScanResult:
    """Findings and risk scoring from an AI safety inspection."""
    is_safe: bool = True
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    detected_threats: List[str] = field(default_factory=list)
    sanitized_content: str = ""
    pii_detected_count: int = 0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "risk_level": self.risk_level,
            "detected_threats": self.detected_threats,
            "sanitized_content": self.sanitized_content,
            "pii_detected_count": self.pii_detected_count,
            "timestamp": self.timestamp.isoformat(),
        }


class AISafetyLayer:
    """
    Enterprise Safety Layer enforcing guardrails across input prompts,
    retrieved knowledge, generated plans, tool invocations, and model outputs.
    """

    # Common injection & jailbreak heuristic patterns
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"system\s+override",
        r"you\s+are\s+now\s+in\s+developer\s+mode",
        r"bypass\s+(all\s+)?safety\s+filters",
        r"disregard\s+all\s+rules",
        r"jailbreak",
        r"reveal\s+(the\s+)?system\s+prompt",
        r"dan\s+mode",
    ]

    # PII Regex Patterns
    EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    PHONE_PATTERN = r"\b\+?[0-9]{1,3}?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b"
    API_KEY_PATTERN = r"\b(sk-[a-zA-Z0-9]{20,}|AIzaSy[a-zA-Z0-9_-]{33}|ghp_[a-zA-Z0-9]{36})\b"

    def scan_input(self, text: str) -> SafetyScanResult:
        """
        Scans incoming prompts or retrieved document content for prompt injection
        and jailbreak attempts.
        """
        threats: List[str] = []
        text_lower = text.lower()

        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                threats.append(f"Prompt injection pattern detected: '{pattern}'")

        is_safe = len(threats) == 0
        risk_level = "LOW"
        if len(threats) >= 2:
            risk_level = "CRITICAL"
        elif len(threats) == 1:
            risk_level = "HIGH"

        if not is_safe:
            logger.warning(f"AISafetyLayer flagged unsafe input: {threats}")

        return SafetyScanResult(
            is_safe=is_safe,
            risk_level=risk_level,
            detected_threats=threats,
            sanitized_content=text if is_safe else "[REDACTED UNSAFE PROMPT]",
        )

    def mask_pii(self, text: str) -> str:
        """Masks detected PII items (emails, phone numbers, API keys)."""
        masked = re.sub(self.EMAIL_PATTERN, "[REDACTED_EMAIL]", text)
        masked = re.sub(self.PHONE_PATTERN, "[REDACTED_PHONE]", masked)
        masked = re.sub(self.API_KEY_PATTERN, "[REDACTED_SECRET]", masked)
        return masked

    def scan_output(self, text: str, auto_mask_pii: bool = True) -> SafetyScanResult:
        """
        Scans model output for sensitive data leakage, PII, and unsafe content.
        """
        threats: List[str] = []
        pii_count = 0

        # Count PII matches
        emails = re.findall(self.EMAIL_PATTERN, text)
        phones = re.findall(self.PHONE_PATTERN, text)
        keys = re.findall(self.API_KEY_PATTERN, text)
        pii_count = len(emails) + len(phones) + len(keys)

        if keys:
            threats.append("Secret / API key exposure detected in output")

        sanitized = self.mask_pii(text) if auto_mask_pii else text
        is_safe = len(threats) == 0
        risk_level = "CRITICAL" if keys else ("MEDIUM" if pii_count > 0 else "LOW")

        return SafetyScanResult(
            is_safe=is_safe,
            risk_level=risk_level,
            detected_threats=threats,
            sanitized_content=sanitized,
            pii_detected_count=pii_count,
        )
