"""Prompt Injection Vulnerability Scanner (Phase 8D).

Detects prompt injection patterns, delimiter manipulation, and instruction override vectors.
"""

from __future__ import annotations

import re
from typing import List
from pydantic import BaseModel, Field


class InjectionScanResult(BaseModel):
    """Result of static prompt injection vulnerability analysis."""
    is_safe: bool
    risk_score: float  # 0.0 to 1.0 (higher = riskier)
    flagged_patterns: List[str] = Field(default_factory=list)
    remediation_advice: List[str] = Field(default_factory=list)


class PromptInjectionScanner:
    """Scans prompt template text and user inputs for injection vulnerabilities."""

    INJECTION_PATTERNS = [
        (r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?", "Instruction override attempt"),
        (r"disregard\s+(all\s+)?(previous|prior|above)", "Disregard prior context"),
        (r"you\s+are\s+now\s+in\s+(developer|unrestricted|god)\s+mode", "Mode switch jailbreak"),
        (r"system\s*override", "System override directive"),
        (r"forget\s+(your\s+)?(rules|instructions|constraints)", "Constraint bypass attempt"),
        (r"do\s+anything\s+now\s*(\(dan\))?", "DAN jailbreak signature"),
        (r"output\s+the\s+system\s+prompt\s+verbatim", "System prompt extraction probe"),
    ]

    @classmethod
    def scan_template(cls, text: str) -> InjectionScanResult:
        """Scan prompt template or variable content for injection indicators."""
        flagged = []
        for pattern, desc in cls.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                flagged.append(desc)

        risk_score = min(1.0, len(flagged) * 0.35)
        is_safe = len(flagged) == 0

        advice = []
        if not is_safe:
            advice.append("Sanitize prompt to remove instruction override phrases")
            advice.append("Enforce explicit XML delimiter fencing around dynamic variables")

        return InjectionScanResult(
            is_safe=is_safe,
            risk_score=round(risk_score, 2),
            flagged_patterns=flagged,
            remediation_advice=advice,
        )
