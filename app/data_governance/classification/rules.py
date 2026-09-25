"""Data Classification Rules & Thresholds (Phase 8B)."""

from __future__ import annotations

from typing import List, Set
from pydantic import BaseModel, Field
from app.data_governance.registry.models import ClassificationLevel, SensitivityCategory


class ClassificationRule(BaseModel):
    """Rule mapping sensitivity categories and patterns to a classification tier."""
    classification_level: ClassificationLevel
    required_sensitivity: Set[SensitivityCategory] = Field(default_factory=set)
    keywords: List[str] = Field(default_factory=list)
    description: str = ""


DEFAULT_CLASSIFICATION_RULES: List[ClassificationRule] = [
    ClassificationRule(
        classification_level=ClassificationLevel.HIGHLY_RESTRICTED,
        required_sensitivity={SensitivityCategory.CREDENTIALS, SensitivityCategory.HEALTHCARE},
        keywords=["top secret", "phi", "password", "private key", "ssn", "social security", "cardholder"],
        description="Credentials, Private Keys, Medical Records, or Cardholder Data",
    ),
    ClassificationRule(
        classification_level=ClassificationLevel.RESTRICTED,
        required_sensitivity={SensitivityCategory.FINANCIAL, SensitivityCategory.LEGAL},
        keywords=["nda", "confidential settlement", "salary", "compensation", "audit report", "bank account", "wire transfer", "restricted"],
        description="Confidential Legal, Payroll, or Sensitive Financial Data",
    ),
    ClassificationRule(
        classification_level=ClassificationLevel.CONFIDENTIAL,
        required_sensitivity={SensitivityCategory.PII, SensitivityCategory.INTELLECTUAL_PROPERTY},
        keywords=["internal only", "proprietary", "invoice", "customer list", "contract", "confidential"],
        description="Customer PII, Invoices, Contracts, and Proprietary IP",
    ),
    ClassificationRule(
        classification_level=ClassificationLevel.INTERNAL,
        required_sensitivity={SensitivityCategory.GENERAL},
        keywords=["company internal", "team update", "roadmap", "meeting notes"],
        description="General internal company documentation",
    ),
]
