"""
Consensus Evaluator for Multi-Critic Reflection System.
Combines multiple critic evaluations into a single unified reflection score and actionable repair directives.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.reflection.critics.historical_critic import HistoricalCritic
from app.agents.reflection.critics.llm_critic import LLMCritic
from app.agents.reflection.critics.rule_critic import CritiqueFeedback, RuleCritic

logger = logging.getLogger(__name__)


@dataclass
class ConsensusCritiqueResult:
    """Consolidated critique evaluation across all critics."""

    overall_score: float
    passed: bool
    critic_scores: Dict[str, float] = field(default_factory=dict)
    all_issues: List[str] = field(default_factory=list)
    actionable_repair_instructions: List[str] = field(default_factory=list)
    needs_replanning: bool = False
    needs_human_escalation: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_score": round(self.overall_score, 4),
            "passed": self.passed,
            "critic_scores": {k: round(v, 4) for k, v in self.critic_scores.items()},
            "all_issues": self.all_issues,
            "actionable_repair_instructions": self.actionable_repair_instructions,
            "needs_replanning": self.needs_replanning,
            "needs_human_escalation": self.needs_human_escalation,
        }


class MultiCriticConsensusEvaluator:
    """Synthesizes individual critiques from deterministic, semantic, and historical critics."""

    def __init__(
        self,
        rule_critic: Optional[RuleCritic] = None,
        llm_critic: Optional[LLMCritic] = None,
        historical_critic: Optional[HistoricalCritic] = None,
        weight_rule: float = 0.40,
        weight_llm: float = 0.35,
        weight_historical: float = 0.25,
        pass_threshold: float = 0.90,
        human_escalation_threshold: float = 0.70,
    ) -> None:
        self.rule_critic = rule_critic or RuleCritic()
        self.llm_critic = llm_critic or LLMCritic()
        self.historical_critic = historical_critic or HistoricalCritic()
        self.weight_rule = weight_rule
        self.weight_llm = weight_llm
        self.weight_historical = weight_historical
        self.pass_threshold = pass_threshold
        self.human_escalation_threshold = human_escalation_threshold

    async def evaluate_extraction(
        self,
        extracted_data: Dict[str, Any],
        raw_text_context: Optional[str] = None,
        goal_description: str = "",
    ) -> ConsensusCritiqueResult:
        """Executes full multi-critic evaluation suite and synthesizes consensus result."""
        # 1. Rule evaluation
        rule_feedback = self.rule_critic.evaluate(extracted_data)

        # 2. LLM Semantic evaluation
        llm_feedback = await self.llm_critic.evaluate(
            extracted_data=extracted_data,
            raw_text_context=raw_text_context,
            goal_description=goal_description,
        )

        # 3. Historical evaluation
        hist_feedback = self.historical_critic.evaluate(extracted_data)

        # 4. Weighted Consensus Formula
        overall_score = (
            self.weight_rule * rule_feedback.score
            + self.weight_llm * llm_feedback.score
            + self.weight_historical * hist_feedback.score
        )
        overall_score = max(0.0, min(1.0, overall_score))

        all_issues: List[str] = []
        repair_instructions: List[str] = []
        for fb in [rule_feedback, llm_feedback, hist_feedback]:
            all_issues.extend(fb.issues)
            repair_instructions.extend(fb.suggestions)

        passed = overall_score >= self.pass_threshold and len(rule_feedback.issues) == 0
        needs_replanning = not passed and overall_score >= self.human_escalation_threshold
        needs_human_escalation = overall_score < self.human_escalation_threshold

        logger.info(
            "MultiCritic Consensus: score=%.3f (Rule: %.2f, LLM: %.2f, Hist: %.2f) passed=%s",
            overall_score,
            rule_feedback.score,
            llm_feedback.score,
            hist_feedback.score,
            passed,
        )

        return ConsensusCritiqueResult(
            overall_score=overall_score,
            passed=passed,
            critic_scores={
                "RuleCritic": rule_feedback.score,
                "LLMCritic": llm_feedback.score,
                "HistoricalCritic": hist_feedback.score,
            },
            all_issues=all_issues,
            actionable_repair_instructions=repair_instructions,
            needs_replanning=needs_replanning,
            needs_human_escalation=needs_human_escalation,
        )
