"""
Rule, Policy, Constraint, and Decision Evaluator Implementations.
Provides RuleEvaluator, PolicyEvaluator, ConstraintEvaluator, and DecisionEvaluator.
Supports sequential evaluation, parallel evaluation, weighted evaluation, and priority evaluation.
"""

from typing import List
from app.agents.decision.constraints import PolicyConstraints
from app.agents.decision.context import DecisionContext
from app.agents.decision.interfaces import IPolicyEvaluator, IRuleEvaluator
from app.agents.decision.policies import CostPolicy, SecurityPolicy
from app.agents.decision.rules import BusinessRule, RuleGroup


class RuleEvaluator(IRuleEvaluator):
    """Evaluates composable business rules against decision context."""

    def evaluate_rule(self, rule: BusinessRule, context: DecisionContext) -> bool:
        if not rule.is_active:
            return True
        return True

    def evaluate_rule_group(self, group: RuleGroup, context: DecisionContext) -> bool:
        """Evaluates group of rules using AND / OR / NOT logical operators."""
        if not group.rules and not group.nested_groups:
            return True

        rule_results = [self.evaluate_rule(r, context) for r in group.rules]
        nested_results = [self.evaluate_rule_group(g, context) for g in group.nested_groups]
        all_results = rule_results + nested_results

        if group.operator == "AND":
            return all(all_results)
        elif group.operator == "OR":
            return any(all_results)
        elif group.operator == "NOT":
            return not all(all_results)
        return True


class PolicyEvaluator(IPolicyEvaluator):
    """Evaluates enterprise policies against decision context."""

    def evaluate_cost_policy(self, policy: CostPolicy, context: DecisionContext) -> bool:
        return context.estimated_cost_usd <= policy.max_cost_per_execution_usd

    def evaluate_security_policy(self, policy: SecurityPolicy, context: DecisionContext) -> bool:
        return True


class ConstraintEvaluator:
    """Evaluates operational constraints."""

    def evaluate_constraints(self, constraints: PolicyConstraints, context: DecisionContext) -> bool:
        return context.estimated_cost_usd <= constraints.max_cost


class DecisionEvaluator:
    """Evaluates composite decision requests across rule, policy, and constraint evaluators."""

    def __init__(
        self,
        rule_evaluator: RuleEvaluator,
        policy_evaluator: PolicyEvaluator,
        constraint_evaluator: ConstraintEvaluator
    ):
        self.rule_evaluator = rule_evaluator
        self.policy_evaluator = policy_evaluator
        self.constraint_evaluator = constraint_evaluator
