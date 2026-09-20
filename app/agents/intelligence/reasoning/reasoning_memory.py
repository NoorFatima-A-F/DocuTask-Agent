"""
Reasoning Memory for LLM Semantic Reasoning Engine.
Maintains deductive premises, hypotheses, intermediate derivations, and confidence scores
during complex multi-step reasoning cycles.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)


class PremiseType(str, Enum):
    GOAL_OBJECTIVE = "goal_objective"
    DOCUMENT_MODALITY = "document_modality"
    SCHEMA_CONSTRAINT = "schema_constraint"
    REGULATORY_RULE = "regulatory_rule"
    EPISODIC_PRIOR = "episodic_prior"
    INTERMEDIATE_DEDUCTION = "intermediate_deduction"


@dataclass
class ReasoningPremise:
    """A single factual or inferred premise used in the reasoning chain."""

    premise_id: UUID = field(default_factory=uuid4)
    premise_type: PremiseType = PremiseType.GOAL_OBJECTIVE
    statement: str = ""
    source: str = ""
    confidence: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "premise_id": str(self.premise_id),
            "premise_type": self.premise_type.value,
            "statement": self.statement,
            "source": self.source,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class Hypothesis:
    """A candidate explanation, plan direction, or classification under evaluation."""

    hypothesis_id: UUID = field(default_factory=uuid4)
    description: str = ""
    supporting_premises: List[UUID] = field(default_factory=list)
    counter_evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5
    validated: bool = False
    rejected: bool = False
    rejection_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis_id": str(self.hypothesis_id),
            "description": self.description,
            "supporting_premises": [str(p) for p in self.supporting_premises],
            "counter_evidence": self.counter_evidence,
            "confidence": self.confidence,
            "validated": self.validated,
            "rejected": self.rejected,
            "rejection_reason": self.rejection_reason,
        }


class ReasoningMemory:
    """In-memory cognitive ledger for tracking deductions during a single reasoning session."""

    def __init__(self, session_id: str = "") -> None:
        self.session_id = session_id or str(uuid4())
        self._premises: Dict[UUID, ReasoningPremise] = {}
        self._hypotheses: Dict[UUID, Hypothesis] = {}
        self._deduction_trail: List[str] = []

    def add_premise(
        self,
        statement: str,
        premise_type: PremiseType = PremiseType.GOAL_OBJECTIVE,
        source: str = "user",
        confidence: float = 1.0,
    ) -> ReasoningPremise:
        """Registers a new premise in the deductive ledger."""
        p = ReasoningPremise(
            premise_type=premise_type,
            statement=statement,
            source=source,
            confidence=max(0.0, min(1.0, confidence)),
        )
        self._premises[p.premise_id] = p
        self._deduction_trail.append(f"PREMISE: [{premise_type.value}] {statement} (conf: {p.confidence:.2f})")
        logger.debug("Added premise %s: %s", p.premise_id, statement)
        return p

    def create_hypothesis(
        self,
        description: str,
        supporting_premises: Optional[List[UUID]] = None,
        initial_confidence: float = 0.5,
    ) -> Hypothesis:
        """Proposes a candidate hypothesis for evaluation."""
        h = Hypothesis(
            description=description,
            supporting_premises=supporting_premises or [],
            confidence=max(0.0, min(1.0, initial_confidence)),
        )
        self._hypotheses[h.hypothesis_id] = h
        self._deduction_trail.append(f"HYPOTHESIS CREATED: {description}")
        return h

    def validate_hypothesis(self, hypothesis_id: UUID, final_confidence: float = 0.95) -> Optional[Hypothesis]:
        """Marks a hypothesis as validated after reasoning."""
        h = self._hypotheses.get(hypothesis_id)
        if h:
            h.validated = True
            h.rejected = False
            h.confidence = final_confidence
            self._deduction_trail.append(f"HYPOTHESIS VALIDATED: {h.description} (conf: {final_confidence:.2f})")
            # Automatically add as intermediate deduction premise
            self.add_premise(
                statement=f"Validated conclusion: {h.description}",
                premise_type=PremiseType.INTERMEDIATE_DEDUCTION,
                source="reasoning_engine",
                confidence=final_confidence,
            )
        return h

    def reject_hypothesis(self, hypothesis_id: UUID, reason: str) -> Optional[Hypothesis]:
        """Rejects a hypothesis with an explanation."""
        h = self._hypotheses.get(hypothesis_id)
        if h:
            h.rejected = True
            h.validated = False
            h.rejection_reason = reason
            h.confidence = 0.0
            self._deduction_trail.append(f"HYPOTHESIS REJECTED: {h.description} (reason: {reason})")
        return h

    def get_validated_hypotheses(self) -> List[Hypothesis]:
        return [h for h in self._hypotheses.values() if h.validated]

    def get_all_premises(self) -> List[ReasoningPremise]:
        return list(self._premises.values())

    def get_summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "total_premises": len(self._premises),
            "total_hypotheses": len(self._hypotheses),
            "validated_count": len(self.get_validated_hypotheses()),
            "trail": list(self._deduction_trail),
        }
