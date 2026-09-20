"""Privacy Masking, Redaction, Tokenization & Anonymization Engine (Phase 8B)."""

from __future__ import annotations

import hashlib
import re
from typing import Dict, List, Optional
from app.data_governance.privacy.pii import PIIType


class PrivacyMaskingEngine:
    """Provides multiple privacy-preserving data transformations."""

    EMAIL_PATTERN = re.compile(r"\b([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*(@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b")
    PHONE_PATTERN = re.compile(r"\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?(\d{4})\b")
    SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-(\d{4})\b")
    CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d{4}[ -]?){3}(\d{4})\b")

    def __init__(self):
        # token -> raw_value (vault for tokenization)
        self._token_vault: Dict[str, str] = {}

    def mask(self, text: str) -> str:
        """Partially mask sensitive strings (e.g. j***@example.com, ***-**-1234)."""
        # Mask emails: john@example.com -> j***@example.com
        result = self.EMAIL_PATTERN.sub(r"\1***\2", text)
        # Mask SSNs: 123-45-6789 -> ***-**-6789
        result = self.SSN_PATTERN.sub(r"***-**-\1", result)
        # Mask Credit Cards: 1234-5678-9012-3456 -> ****-****-****-3456
        result = self.CREDIT_CARD_PATTERN.sub(r"****-****-****-\1", result)
        # Mask Phones: (555) 123-4567 -> (***) ***-4567
        result = self.PHONE_PATTERN.sub(r"(***) ***-\1", result)
        return result

    def redact(self, text: str, replacement: str = "[REDACTED]") -> str:
        """Completely replace detected sensitive values with redaction token."""
        result = self.EMAIL_PATTERN.sub(replacement, text)
        result = self.SSN_PATTERN.sub(replacement, result)
        result = self.CREDIT_CARD_PATTERN.sub(replacement, result)
        result = self.PHONE_PATTERN.sub(replacement, result)
        return result

    def tokenize(self, text: str) -> str:
        """Replace sensitive email and SSN occurrences with reversible surrogate tokens."""
        def _replace_email(match):
            raw = match.group(0)
            token = f"TOK_EMAIL_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8]}"
            self._token_vault[token] = raw
            return token

        def _replace_ssn(match):
            raw = match.group(0)
            token = f"TOK_SSN_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8]}"
            self._token_vault[token] = raw
            return token

        result = self.EMAIL_PATTERN.sub(_replace_email, text)
        result = self.SSN_PATTERN.sub(_replace_ssn, result)
        return result

    def detokenize(self, tokenized_text: str) -> str:
        """Reconstruct original values from surrogate tokens using secure vault."""
        result = tokenized_text
        for token, raw in self._token_vault.items():
            result = result.replace(token, raw)
        return result
