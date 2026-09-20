"""Jailbreak Probability Classifier."""

import re
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from .patterns import JailbreakPatternRegistry


class JailbreakClassification(BaseModel):
    is_jailbreak: bool
    probability: float
    matched_strategies: List[str] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)


class JailbreakClassifier:
    """Computes an adversarial jailbreak likelihood score across multiple attack strategies."""

    def __init__(self):
        self.registry = JailbreakPatternRegistry()

    def classify(self, text: str) -> JailbreakClassification:
        if not text:
            return JailbreakClassification(is_jailbreak=False, probability=0.0)

        matched_strategies: List[str] = []
        score = 0.0

        # Check persona patterns
        for pattern, name, _ in self.registry.PERSONA_PATTERNS:
            if re.search(pattern, text):
                matched_strategies.append(f"Persona: {name}")
                score += 0.45

        # Check hypothetical patterns
        for pattern, name, _ in self.registry.HYPOTHETICAL_PATTERNS:
            if re.search(pattern, text):
                matched_strategies.append(f"Hypothetical: {name}")
                score += 0.35

        # Check encoding patterns
        for pattern, name, _ in self.registry.ENCODING_PATTERNS:
            if re.search(pattern, text):
                matched_strategies.append(f"Encoding: {name}")
                score += 0.30

        # Check compliance patterns
        for pattern, name, _ in self.registry.COMPLIANCE_PATTERNS:
            if re.search(pattern, text):
                matched_strategies.append(f"ComplianceSuppression: {name}")
                score += 0.40

        # Bound probability to [0.0, 1.0]
        probability = min(1.0, score)
        is_jailbreak = probability >= 0.45 or len(matched_strategies) >= 2

        return JailbreakClassification(
            is_jailbreak=is_jailbreak,
            probability=probability,
            matched_strategies=matched_strategies,
            details={"match_count": len(matched_strategies)},
        )
