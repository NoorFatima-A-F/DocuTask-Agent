"""Toxicity & Harmful Content Detector."""

import re
from enum import Enum
from typing import List, Tuple, Dict, Any
from pydantic import BaseModel, Field
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation


class ToxicityCategory(str, Enum):
    HATE_SPEECH = "HATE_SPEECH"
    HARASSMENT = "HARASSMENT"
    VIOLENCE = "VIOLENCE"
    SELF_HARM = "SELF_HARM"
    SEXUAL = "SEXUAL"
    PROFANITY = "PROFANITY"
    DANGEROUS_CONTENT = "DANGEROUS_CONTENT"


class ToxicityDetector:
    """Detects toxic, harmful, or policy-violating content in AI-generated responses."""

    TOXICITY_PATTERNS: List[Tuple[re.Pattern, ToxicityCategory, ViolationSeverity, str]] = [
        # Self-harm
        (re.compile(r"(?i)\b(how\s+to\s+(kill|harm|cut)\s+yourself|commit\s+suicide|suicide\s+methods)\b"), ToxicityCategory.SELF_HARM, ViolationSeverity.CRITICAL, "Self-harm instructional content"),
        # Violence & Weapons
        (re.compile(r"(?i)\b(how\s+to\s+build\s+a\s+bomb|synthesize\s+(ricin|sarin|anthrax|explosive)|manufacture\s+weapons)\b"), ToxicityCategory.DANGEROUS_CONTENT, ViolationSeverity.CRITICAL, "CBRN / weapons manufacturing instruction"),
        (re.compile(r"(?i)\b(kill\s+all\s+|exterminate\s+|eliminate\s+them\s+all)\b"), ToxicityCategory.VIOLENCE, ViolationSeverity.CRITICAL, "Violent threats / incitement"),
        # Hate Speech
        (re.compile(r"(?i)\b(subhuman|inferior\s+race|racial\s+slur)\b"), ToxicityCategory.HATE_SPEECH, ViolationSeverity.CRITICAL, "Hate speech and discriminatory slurs"),
        # Harassment
        (re.compile(r"(?i)\b(doxx|doxxing|swatting|harass\s+them\s+at)\b"), ToxicityCategory.HARASSMENT, ViolationSeverity.HIGH, "Harassment and doxxing directive"),
    ]

    def scan(self, text: str) -> Tuple[bool, List[SafetyViolation], float]:
        violations: List[SafetyViolation] = []
        if not text:
            return False, violations, 0.0

        max_severity_weight = 0.0

        for pattern, cat, severity, desc in self.TOXICITY_PATTERNS:
            match = pattern.search(text)
            if match:
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.TOXICITY,
                        severity=severity,
                        message=f"{desc} ({cat.value})",
                        location="output",
                        rule_id="TOX-001",
                        evidence=match.group(0)[:100],
                        details={"toxicity_category": cat.value},
                    )
                )
                if severity == ViolationSeverity.CRITICAL:
                    max_severity_weight = max(max_severity_weight, 1.0)
                elif severity == ViolationSeverity.HIGH:
                    max_severity_weight = max(max_severity_weight, 0.8)
                else:
                    max_severity_weight = max(max_severity_weight, 0.4)

        is_toxic = len(violations) > 0
        return is_toxic, violations, max_severity_weight
