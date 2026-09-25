"""Data Classification Engine (Phase 8B)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, Set
from pydantic import BaseModel, Field
from app.data_governance.registry.models import ClassificationLevel, SensitivityCategory
from app.data_governance.classification.rules import DEFAULT_CLASSIFICATION_RULES, ClassificationRule
from app.data_governance.classification.detectors import SensitiveDataDetector


class ClassificationResult(BaseModel):
    """Result from automated data classification."""
    classification: ClassificationLevel
    confidence_score: float
    detected_sensitivities: Set[SensitivityCategory]
    evidence_snippets: List[str]
    detection_method: str = "RULE_AND_HEURISTIC"
    reviewer_id: Optional[str] = None
    classified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DataClassificationEngine:
    """Classifies unstructured and structured data into governed tiers."""

    def __init__(
        self,
        detector: Optional[SensitiveDataDetector] = None,
        rules: Optional[List[ClassificationRule]] = None,
    ):
        self.detector = detector or SensitiveDataDetector()
        self.rules = rules or DEFAULT_CLASSIFICATION_RULES

    def classify_text(self, text: str) -> ClassificationResult:
        """Analyze text and determine classification tier and sensitivity tags."""
        detected = self.detector.detect(text)
        detected_categories = set(detected.keys())

        evidence: List[str] = []
        for cat, samples in detected.items():
            evidence.extend(samples)

        # Keyword matching
        text_lower = text.lower()
        matched_rule = None

        for rule in self.rules:
            # Check required sensitivity intersection
            if rule.required_sensitivity and (rule.required_sensitivity & detected_categories):
                matched_rule = rule
                break
            # Check keywords
            if any(kw in text_lower for kw in rule.keywords):
                matched_rule = rule
                break

        if matched_rule:
            level = matched_rule.classification_level
            confidence = 0.90 if detected_categories else 0.75
        else:
            level = ClassificationLevel.INTERNAL if len(text.strip()) > 0 else ClassificationLevel.PUBLIC
            confidence = 0.60

        return ClassificationResult(
            classification=level,
            confidence_score=confidence,
            detected_sensitivities=detected_categories,
            evidence_snippets=evidence[:10],
            detection_method="RULE_AND_HEURISTIC",
        )
