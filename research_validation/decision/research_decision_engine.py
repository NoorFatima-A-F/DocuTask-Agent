"""
Research Decision Engine (Phase 91C)
====================================
Evaluates proposed experiments and empirical evidence to make autonomous
decisions regarding execution, replication, rejection, or statistical escalation.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional

from research_validation.decision.decision_rules import ResearchAction, ResearchDecision
from research_validation.hypothesis.hypothesis_model import ScientificHypothesis
from research_validation.provenance.hashing import hash_canonical_json


class ResearchDecisionEngine:
    """
    Automated scientific decision-maker evaluating statistical power, risk, and feasibility.
    """

    def __init__(
        self,
        min_statistical_power: float = 0.80,
        max_acceptable_risk: float = 0.85,
    ):
        self.min_power = min_statistical_power
        self.max_risk = max_acceptable_risk

    def evaluate_hypothesis(
        self,
        hypothesis: ScientificHypothesis,
        available_datasets: List[str],
        known_failure_match: bool = False,
    ) -> ResearchDecision:
        """Evaluates whether to execute, reject, or request more data for a hypothesis."""
        blocking: List[str] = []
        adjustments: Dict[str, Any] = {}

        # 1. Known catastrophic failure check
        if known_failure_match:
            blocking.append("Hypothesis matches known historical failure pattern.")
            payload = {"action": ResearchAction.REJECT_EXPERIMENT.value, "target": hypothesis.hypothesis_id}
            return ResearchDecision(
                action=ResearchAction.REJECT_EXPERIMENT,
                target_id=hypothesis.hypothesis_id,
                confidence_score=0.95,
                rationale="Candidate configuration matches recorded failure memory.",
                blocking_factors=blocking,
                decision_digest_sha256=hash_canonical_json(payload),
            )

        # 2. Risk check
        if hypothesis.risk_score > self.max_risk:
            blocking.append(f"Risk score {hypothesis.risk_score:.2f} exceeds threshold {self.max_risk:.2f}.")
            payload = {"action": ResearchAction.NEED_REVIEWER_ATTENTION.value, "target": hypothesis.hypothesis_id}
            return ResearchDecision(
                action=ResearchAction.NEED_REVIEWER_ATTENTION,
                target_id=hypothesis.hypothesis_id,
                confidence_score=0.90,
                rationale="Excessive operational or divergence risk.",
                blocking_factors=blocking,
                decision_digest_sha256=hash_canonical_json(payload),
            )

        # 3. Dataset availability check
        missing = [d for d in hypothesis.required_datasets if d not in available_datasets]
        if missing:
            blocking.append(f"Missing required datasets: {', '.join(missing)}")
            adjustments["missing_datasets"] = missing
            payload = {"action": ResearchAction.NEED_MORE_DATASETS.value, "target": hypothesis.hypothesis_id}
            return ResearchDecision(
                action=ResearchAction.NEED_MORE_DATASETS,
                target_id=hypothesis.hypothesis_id,
                confidence_score=1.0,
                rationale="Required datasets are not present locally.",
                blocking_factors=blocking,
                suggested_adjustments=adjustments,
                decision_digest_sha256=hash_canonical_json(payload),
            )

        # 4. Statistical power & sample size check
        if hypothesis.estimated_runtime_sec < 5.0 and hypothesis.confidence_level < 0.60:
            adjustments["suggested_repetitions"] = 5
            payload = {"action": ResearchAction.NEED_MORE_REPETITIONS.value, "target": hypothesis.hypothesis_id}
            return ResearchDecision(
                action=ResearchAction.NEED_MORE_REPETITIONS,
                target_id=hypothesis.hypothesis_id,
                confidence_score=0.85,
                rationale="Low runtime and low prior confidence suggest multiple repetitions.",
                suggested_adjustments=adjustments,
                decision_digest_sha256=hash_canonical_json(payload),
            )

        # Approved for execution
        payload = {"action": ResearchAction.RUN_EXPERIMENT.value, "target": hypothesis.hypothesis_id}
        return ResearchDecision(
            action=ResearchAction.RUN_EXPERIMENT,
            target_id=hypothesis.hypothesis_id,
            confidence_score=hypothesis.confidence_level,
            rationale="Hypothesis satisfies feasibility, safety, and dataset availability requirements.",
            decision_digest_sha256=hash_canonical_json(payload),
        )
