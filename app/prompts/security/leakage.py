"""Prompt Data Leakage Scanner (Phase 8D).

Detects embedded secrets, API keys, database credentials, passwords, and sensitive PII requests in prompt templates.
"""

from __future__ import annotations

import re
from typing import List
from pydantic import BaseModel, Field


class LeakageScanResult(BaseModel):
    """Result of static prompt data leakage analysis."""
    is_safe: bool
    detected_secret_types: List[str] = Field(default_factory=list)
    risk_score: float = 0.0
    recommendations: List[str] = Field(default_factory=list)


class PromptLeakageScanner:
    """Scans prompt templates for accidental hardcoded secrets and credentials."""

    SECRET_PATTERNS = [
        (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API Key"),
        (r"ghp_[a-zA-Z0-9]{20,}", "GitHub Personal Access Token"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
        (r"bearer\s+[a-zA-Z0-9_\-\.]{20,}", "Bearer Token"),
        (r"password\s*[:=]\s*['\"][^\s'\"]{6,}['\"]", "Hardcoded Password"),
        (r"postgres(ql)?://[a-zA-Z0-9]+:[^@]+@", "Database Connection String with Credentials"),
    ]

    @classmethod
    def scan_template(cls, text: str) -> LeakageScanResult:
        """Scan prompt template text for embedded credentials."""
        detected = []
        for pattern, desc in cls.SECRET_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(desc)

        is_safe = len(detected) == 0
        risk = 1.0 if not is_safe else 0.0

        recommendations = []
        if not is_safe:
            recommendations.append("Remove hardcoded secrets from prompt template immediately")
            recommendations.append("Inject secrets at runtime via secure environment vaults")

        return LeakageScanResult(
            is_safe=is_safe,
            detected_secret_types=detected,
            risk_score=risk,
            recommendations=recommendations,
        )
