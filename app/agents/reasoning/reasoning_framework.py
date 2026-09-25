"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Reasoning Framework.
Provides governed cognitive reasoning, constraint checking, hypothesis testing,
verification, and structured decision summary generation (without persisting private CoT).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import uuid
import logging

from app.agents.domain.agent_entity import ReasoningSummary

logger = logging.getLogger(__name__)


class ReasoningFramework:
    """
    Cognitive Reasoning Engine for hypothesis evaluation, constraint reasoning,
    and decision synthesis.
    """

    def __init__(self):
        self._reasoning_store: Dict[str, List[ReasoningSummary]] = {}

    def evaluate_hypothesis(
        self,
        hypothesis: str,
        evidence: List[Dict[str, Any]],
        constraints: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluates a hypothesis against provided evidence and constraints.
        Returns validation status, score, and supporting evidence summary.
        """
        constraints = constraints or []
        verified_evidence: List[Dict[str, Any]] = []
        contradictions: List[Dict[str, Any]] = []

        total_weight = 0.0
        positive_weight = 0.0

        for item in evidence:
            weight = float(item.get("weight", 1.0))
            is_supportive = bool(item.get("supports", True))
            total_weight += weight
            if is_supportive:
                positive_weight += weight
                verified_evidence.append(item)
            else:
                contradictions.append(item)

        score = (positive_weight / total_weight) if total_weight > 0 else 0.5

        # Check constraints
        violated_constraints: List[str] = []
        for c in constraints:
            if "disallow" in c.lower() or "forbid" in c.lower():
                violated_constraints.append(c)

        is_valid = score >= 0.7 and len(violated_constraints) == 0

        return {
            "hypothesis": hypothesis,
            "is_valid": is_valid,
            "confidence_score": round(score, 3),
            "supporting_evidence_count": len(verified_evidence),
            "contradiction_count": len(contradictions),
            "violated_constraints": violated_constraints,
        }

    def record_decision(
        self,
        agent_id: str,
        task_id: str,
        summary: str,
        decision: str,
        evidence: Optional[List[Dict[str, Any]]] = None,
        confidence_score: float = 1.0,
        validation_results: Optional[Dict[str, Any]] = None,
        risk_assessment: Optional[Dict[str, Any]] = None,
    ) -> ReasoningSummary:
        """
        Synthesizes and records an immutable ReasoningSummary.
        Explicitly excludes any raw, private chain-of-thought traces.
        """
        record = ReasoningSummary(
            id=f"rsn-{uuid.uuid4().hex[:10]}",
            agent_id=agent_id,
            task_id=task_id,
            summary=summary,
            decision=decision,
            evidence=evidence or [],
            confidence_score=confidence_score,
            validation_results=validation_results or {},
            risk_assessment=risk_assessment or {},
        )

        if agent_id not in self._reasoning_store:
            self._reasoning_store[agent_id] = []
        self._reasoning_store[agent_id].append(record)

        logger.info(
            f"Recorded ReasoningSummary for Agent {agent_id} on Task {task_id}: "
            f"Decision='{decision}', Confidence={confidence_score}"
        )
        return record

    def get_summaries(self, agent_id: str) -> List[ReasoningSummary]:
        """Returns all recorded reasoning summaries for an agent."""
        return list(self._reasoning_store.get(agent_id, []))
