"""Input Intent Classifier."""

from enum import Enum
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from .detectors import MaliciousPatternDetector


class InputIntent(str, Enum):
    BENIGN_QUERY = "BENIGN_QUERY"
    BENIGN_INSTRUCTION = "BENIGN_INSTRUCTION"
    SUSPICIOUS_PROBING = "SUSPICIOUS_PROBING"
    MALICIOUS_EXPLOIT = "MALICIOUS_EXPLOIT"
    POLICY_VIOLATING = "POLICY_VIOLATING"


class IntentClassificationResult(BaseModel):
    intent: InputIntent
    confidence: float
    risk_score: float
    detected_indicators: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InputIntentClassifier:
    """Classifies user request intent into safety categories."""

    def __init__(self):
        self.malicious_detector = MaliciousPatternDetector()

    def classify(self, text: str) -> IntentClassificationResult:
        if not text or not text.strip():
            return IntentClassificationResult(
                intent=InputIntent.BENIGN_QUERY,
                confidence=1.0,
                risk_score=0.0,
            )

        violations = self.malicious_detector.scan(text)
        if violations:
            return IntentClassificationResult(
                intent=InputIntent.MALICIOUS_EXPLOIT,
                confidence=0.95,
                risk_score=0.95,
                detected_indicators=[v.message for v in violations],
            )

        # Probing heuristics
        probing_terms = [
            "system prompt", "reveal your instructions", "what are your guidelines",
            "show internal configuration", "who programmed you", "ignore restrictions"
        ]
        text_lower = text.lower()
        probing_hits = [term for term in probing_terms if term in text_lower]

        if probing_hits:
            return IntentClassificationResult(
                intent=InputIntent.SUSPICIOUS_PROBING,
                confidence=0.85,
                risk_score=0.60,
                detected_indicators=probing_hits,
            )

        # Default benign classification
        if any(w in text_lower for w in ["extract", "summarize", "analyze", "parse", "process", "find", "get", "calculate"]):
            return IntentClassificationResult(
                intent=InputIntent.BENIGN_INSTRUCTION,
                confidence=0.90,
                risk_score=0.05,
            )

        return IntentClassificationResult(
            intent=InputIntent.BENIGN_QUERY,
            confidence=0.88,
            risk_score=0.02,
        )
