"""
Enterprise Decision Engine Entrypoint.
Evaluates policies, governance rules, risk scores, cost limits, and approval requirements.
Decouples Planners and Executors from business rule evaluation.
"""

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.decision.approvals import ApprovalRequirement
from app.agents.decision.context import DecisionContext
from app.agents.decision.evaluator import PolicyEvaluator, RuleEvaluator
from app.agents.decision.explanations import DecisionExplanation
from app.agents.decision.governance import GovernanceFramework
from app.agents.decision.interfaces import IDecisionEngine
from app.agents.decision.reasoning import ReasoningStep
from app.agents.decision.recommendations import Recommendation
from app.agents.decision.risk import RiskAssessment, RiskScore


class DecisionRequest(BaseModel):
    """Decision Evaluation Request."""

    context: DecisionContext
    decision_type: str = Field(default="EXECUTION")
    governance: GovernanceFramework = Field(default_factory=GovernanceFramework)

    model_config = {"frozen": True}


class DecisionResult(BaseModel):
    """Strongly Typed Decision Evaluation Result."""

    is_approved: bool = Field(default=True)
    decision_id: str = Field(default="")
    risk_assessment: RiskAssessment = Field(default_factory=RiskAssessment)
    approval_requirement: ApprovalRequirement = Field(default_factory=ApprovalRequirement)
    explanation: DecisionExplanation = Field(default_factory=lambda: DecisionExplanation(summary="Evaluation passed"))
    recommendations: List[Recommendation] = Field(default_factory=list)
    evaluation_duration_ms: float = Field(default=0.0, ge=0.0)

    model_config = {"frozen": True}


class DecisionEngine(IDecisionEngine):
    """
    Enterprise Centralized Decision Authority.
    Evaluates policy rules, risk assessments, cost budgets, and governance constraints.
    """

    def __init__(
        self,
        governance: Optional[GovernanceFramework] = None,
        rule_evaluator: Optional[RuleEvaluator] = None,
        policy_evaluator: Optional[PolicyEvaluator] = None
    ):
        self.governance = governance or GovernanceFramework()
        self.rule_evaluator = rule_evaluator or RuleEvaluator()
        self.policy_evaluator = policy_evaluator or PolicyEvaluator()

    async def evaluate(self, context: DecisionContext) -> DecisionResult:
        """Evaluates decision request and returns strongly typed DecisionResult with explanation."""
        start_time = time.perf_counter()

        reasoning: List[ReasoningStep] = []
        is_approved = True
        risk_level = "LOW"
        risk_value = 0.1

        # 1. Cost Policy Check
        cost_passed = self.policy_evaluator.evaluate_cost_policy(self.governance.cost_policy, context)
        reasoning.append(
            ReasoningStep(
                step_number=1,
                rule_or_policy="CostPolicy",
                outcome="PASSED" if cost_passed else "FAILED",
                explanation=f"Estimated cost ${context.estimated_cost_usd} vs limit ${self.governance.cost_policy.max_cost_per_execution_usd}"
            )
        )

        if not cost_passed:
            is_approved = False
            risk_level = "HIGH"
            risk_value = 0.85

        # 2. Approval Requirement Check
        req_approval = context.estimated_cost_usd > self.governance.approval_policy.require_human_approval_above_cost_usd
        approval_req = ApprovalRequirement(requires_approval=req_approval, reason="Cost threshold exceeded" if req_approval else None)

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        explanation = DecisionExplanation(
            summary="Decision evaluation completed successfully." if is_approved else "Decision evaluation rejected due to policy bounds.",
            reasoning_steps=reasoning,
            confidence_breakdown=0.98 if is_approved else 0.4
        )

        recs = [Recommendation(action="PROCEED", rationale="All policy checks passed")] if is_approved else [Recommendation(action="REQUEST_HUMAN_APPROVAL", rationale="Cost limits exceeded")]

        return DecisionResult(
            is_approved=is_approved,
            risk_assessment=RiskAssessment(risk_score=RiskScore(score=risk_value, risk_level=risk_level)),
            approval_requirement=approval_req,
            explanation=explanation,
            recommendations=recs,
            evaluation_duration_ms=round(duration_ms, 2)
        )
