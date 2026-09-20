"""PII Categories & Sensitive Entity Definitions (Phase 8B)."""

from __future__ import annotations

import enum
from typing import List
from pydantic import BaseModel


class PIIType(str, enum.Enum):
    """Specific Personally Identifiable Information types."""
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    SSN = "SSN"
    CREDIT_CARD = "CREDIT_CARD"
    IBAN = "IBAN"
    NAME = "NAME"
    IP_ADDRESS = "IP_ADDRESS"
    MEDICAL_ID = "MEDICAL_ID"


class PIISpan(BaseModel):
    """Identified PII occurrence within a string."""
    pii_type: PIIType
    start_pos: int
    end_pos: int
    raw_value: str
