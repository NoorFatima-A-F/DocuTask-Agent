"""Sensitive Data Detectors (Phase 8B).

Rule-based and heuristic pattern matchers for PII, Financial, Healthcare, and Legal content.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple
from app.data_governance.registry.models import SensitivityCategory


class SensitiveDataDetector:
    """Detects presence of sensitive information categories in raw text."""

    PATTERNS: Dict[SensitivityCategory, List[Tuple[str, re.Pattern]]] = {
        SensitivityCategory.PII: [
            ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")),
            ("phone", re.compile(r"\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")),
            ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
        ],
        SensitivityCategory.FINANCIAL: [
            ("credit_card", re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")),
            ("iban", re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")),
            ("currency_amount", re.compile(r"\$\s?[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?")),
        ],
        SensitivityCategory.HEALTHCARE: [
            ("mrn", re.compile(r"\bMRN[:\s#]+[A-Z0-9-]{6,12}\b", re.IGNORECASE)),
            ("icd_code", re.compile(r"\bICD-(?:9|10)-[A-Z0-9.]{3,7}\b", re.IGNORECASE)),
            ("patient_id", re.compile(r"\bpatient\s+(?:id|name|record)[:\s]+[A-Za-z0-9\s]+\b", re.IGNORECASE)),
        ],
        SensitivityCategory.CREDENTIALS: [
            ("api_key", re.compile(r"\b(?:api[_-]?key|secret|token)[:\s=]+['\"]?[A-Za-z0-9_-]{16,}['\"]?\b", re.IGNORECASE)),
            ("password", re.compile(r"\bpassword[:\s=]+['\"]?[^\s'\"]{6,}['\"]?\b", re.IGNORECASE)),
        ],
        SensitivityCategory.LEGAL: [
            ("contract", re.compile(r"\b(?:non-disclosure\s+agreement|confidentiality\s+agreement|settlement\s+agreement|master\s+services\s+agreement)\b", re.IGNORECASE)),
        ],
    }

    def detect(self, text: str) -> Dict[SensitivityCategory, List[str]]:
        """Scan text and return detected sensitive categories with matched snippets."""
        results: Dict[SensitivityCategory, List[str]] = {}

        for category, pattern_list in self.PATTERNS.items():
            matches = []
            for pattern_name, regex in pattern_list:
                found = regex.findall(text)
                if found:
                    for item in found[:3]:  # Capture up to 3 samples
                        matches.append(f"{pattern_name}:{str(item)[:30]}")
            if matches:
                results[category] = matches

        return results
