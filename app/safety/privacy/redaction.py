"""PII Redaction & Reversible Pseudonymization Engine."""

from typing import Dict, List
from pydantic import BaseModel, Field
from .pii_detector import PIIDetector, PIIType


class RedactionResult(BaseModel):
    redacted_text: str
    redacted_count: int
    pii_types_found: List[PIIType] = Field(default_factory=list)
    token_mapping: Dict[str, str] = Field(default_factory=dict)  # token -> original_value


class DataRedactor:
    """Performs full tokenized redaction and reversible pseudonymization."""

    def __init__(self, detector: PIIDetector = None):
        self.detector = detector or PIIDetector()

    def redact(
        self,
        text: str,
        pseudonymize: bool = False,
    ) -> RedactionResult:
        """
        Redacts detected PII.
        If pseudonymize=True, assigns deterministic replacement tokens (e.g. <PII_EMAIL_1>)
        that can be reversed via unredact().
        """
        if not text:
            return RedactionResult(redacted_text="", redacted_count=0)

        matches = self.detector.detect(text)
        if not matches:
            return RedactionResult(redacted_text=text, redacted_count=0)

        token_mapping: Dict[str, str] = {}
        pii_counts: Dict[str, int] = {}
        pii_types_found: List[PIIType] = []

        result = text
        for match in reversed(matches):
            if match.pii_type not in pii_types_found:
                pii_types_found.append(match.pii_type)

            if pseudonymize:
                type_name = match.pii_type.value
                pii_counts[type_name] = pii_counts.get(type_name, 0) + 1
                token = f"<{type_name}_{pii_counts[type_name]}>"
                token_mapping[token] = match.raw_value
                replacement = token
            else:
                replacement = f"[REDACTED_{match.pii_type.value}]"

            result = result[:match.start] + replacement + result[match.end:]

        return RedactionResult(
            redacted_text=result,
            redacted_count=len(matches),
            pii_types_found=pii_types_found,
            token_mapping=token_mapping,
        )

    def unredact(self, text: str, token_mapping: Dict[str, str]) -> str:
        """Reverses pseudonymized tokens back to original values."""
        if not text or not token_mapping:
            return text

        result = text
        for token, original in token_mapping.items():
            result = result.replace(token, original)
        return result
