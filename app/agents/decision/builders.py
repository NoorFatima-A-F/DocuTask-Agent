"""
Fluent Builders Suite for Enterprise Decision Subsystem.
Provides DecisionBuilder, RuleBuilder, PolicyBuilder, OptimizationBuilder,
RecommendationBuilder, and ExplanationBuilder.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.decision.context import DecisionContext
from app.agents.decision.engine import DecisionRequest
from app.agents.decision.explanations import DecisionExplanation
from app.agents.decision.governance import GovernanceFramework
from app.agents.decision.optimization_targets import OptimizationMetric, OptimizationTarget
from app.agents.decision.policies import (
    ApprovalPolicy,
    CompliancePolicy,
    CostPolicy,
    SecurityPolicy,
)
from app.agents.decision.reasoning import ReasoningStep
from app.agents.decision.recommendations import Recommendation
from app.agents.decision.rules import BusinessRule
from app.agents.decision.validators import DecisionValidator


class DecisionBuilder:
    """Fluent builder for DecisionContext and DecisionRequest."""

    def __init__(self, action_type: str = "EXECUTE_TASK"):
        self._action_type = action_type
        self._document_id: Optional[UUID] = None
        self._user_id: Optional[UUID] = None
        self._estimated_cost_usd = 0.0
        self._parameters: Dict[str, Any] = {}

    def for_document(self, document_id: UUID, user_id: UUID) -> "DecisionBuilder":
        self._document_id = document_id
        self._user_id = user_id
        return self

    def with_cost(self, cost_usd: float) -> "DecisionBuilder":
        self._estimated_cost_usd = cost_usd
        return self

    def with_parameter(self, key: str, value: Any) -> "DecisionBuilder":
        self._parameters[key] = value
        return self

    def build_context(self) -> DecisionContext:
        ctx = DecisionContext(
            document_id=self._document_id,
            user_id=self._user_id,
            action_type=self._action_type,
            estimated_cost_usd=self._estimated_cost_usd,
            parameters=self._parameters
        )
        DecisionValidator.validate_context(ctx)
        return ctx

    def build_request(self) -> DecisionRequest:
        ctx = self.build_context()
        return DecisionRequest(context=ctx)


class RuleBuilder:
    """Fluent builder for BusinessRule specifications."""

    def __init__(self, rule_id: str, name: str):
        self._rule_id = rule_id
        self._name = name
        self._rule_type = "BUSINESS"
        self._action_type = "ALLOW"
        self._priority = 100

    def with_rule_type(self, rule_type: str) -> "RuleBuilder":
        self._rule_type = rule_type
        return self

    def with_action(self, action_type: str) -> "RuleBuilder":
        self._action_type = action_type
        return self

    def with_priority(self, priority: int) -> "RuleBuilder":
        self._priority = priority
        return self

    def build(self) -> BusinessRule:
        return BusinessRule(
            rule_id=self._rule_id,
            name=self._name,
            rule_type=self._rule_type,
            action_type=self._action_type,
            priority=self._priority
        )


class PolicyBuilder:
    """Fluent builder for GovernanceFramework policies."""

    def __init__(self):
        self._cost_policy = CostPolicy()
        self._security_policy = SecurityPolicy()
        self._compliance_policy = CompliancePolicy()
        self._approval_policy = ApprovalPolicy()

    def with_cost_limit(self, max_cost_usd: float) -> "PolicyBuilder":
        self._cost_policy = CostPolicy(max_cost_per_execution_usd=max_cost_usd)
        return self

    def with_approval_threshold(self, threshold_usd: float) -> "PolicyBuilder":
        self._approval_policy = ApprovalPolicy(require_human_approval_above_cost_usd=threshold_usd)
        return self

    def build(self) -> GovernanceFramework:
        return GovernanceFramework(
            cost_policy=self._cost_policy,
            security_policy=self._security_policy,
            compliance_policy=self._compliance_policy,
            approval_policy=self._approval_policy
        )


class OptimizationBuilder:
    """Fluent builder for OptimizationTarget."""

    def __init__(self, metric: OptimizationMetric = OptimizationMetric.COST):
        self._metric = metric
        self._target_value = 1.0
        self._weight = 1.0

    def with_target_value(self, value: float) -> "OptimizationBuilder":
        self._target_value = value
        return self

    def with_weight(self, weight: float) -> "OptimizationBuilder":
        self._weight = weight
        return self

    def build(self) -> OptimizationTarget:
        return OptimizationTarget(
            metric=self._metric,
            target_value=self._target_value,
            weight=self._weight
        )


class RecommendationBuilder:
    """Fluent builder for Recommendation."""

    def __init__(self, action: str, rationale: str):
        self._action = action
        self._rationale = rationale
        self._confidence = 0.9

    def with_confidence(self, confidence: float) -> "RecommendationBuilder":
        self._confidence = confidence
        return self

    def build(self) -> Recommendation:
        return Recommendation(
            action=self._action,
            rationale=self._rationale,
            confidence=self._confidence
        )


class ExplanationBuilder:
    """Fluent builder for DecisionExplanation."""

    def __init__(self, summary: str):
        self._summary = summary
        self._reasoning_steps: List[ReasoningStep] = []
        self._confidence = 1.0

    def add_step(self, step_number: int, rule_or_policy: str, outcome: str, explanation: str) -> "ExplanationBuilder":
        self._reasoning_steps.append(
            ReasoningStep(
                step_number=step_number,
                rule_or_policy=rule_or_policy,
                outcome=outcome,
                explanation=explanation
            )
        )
        return self

    def with_confidence(self, confidence: float) -> "ExplanationBuilder":
        self._confidence = confidence
        return self

    def build(self) -> DecisionExplanation:
        return DecisionExplanation(
            summary=self._summary,
            reasoning_steps=self._reasoning_steps,
            confidence_breakdown=self._confidence
        )
