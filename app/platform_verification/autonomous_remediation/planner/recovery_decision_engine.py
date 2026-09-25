"""Automated Recovery Decision Engine (3H.4.3.4).

Takes failure diagnosis and RCA context, evaluates confidence thresholds,
selects the optimal remediation policy, and produces an actionable decision plan.
"""

from typing import Optional
import uuid
from ..domain.models import (
    FailureContext,
    RemediationDecision,
    ActionLevel,
    ExecutionApproval,
)
from ..domain.interfaces import IRecoveryDecisionEngine
from ..policies.remediation_policy_engine import RemediationPolicyEngine
from ..classifier.action_classifier import ActionClassifier


class RecoveryDecisionEngine(IRecoveryDecisionEngine):
    """Engine responsible for autonomous remediation decision planning."""

    def __init__(
        self,
        policy_engine: Optional[RemediationPolicyEngine] = None,
        classifier: Optional[ActionClassifier] = None,
        min_confidence_threshold: float = 0.85,
    ):
        self.policy_engine = policy_engine or RemediationPolicyEngine()
        self.classifier = classifier or ActionClassifier()
        self.min_confidence_threshold = min_confidence_threshold

    def make_decision(self, context: FailureContext) -> RemediationDecision:
        """Evaluates failure context and produces a structured RemediationDecision."""
        decision_id = f"DEC-{uuid.uuid4().hex[:8].upper()}"
        policy = self.policy_engine.find_policy_for_condition(context.root_cause)

        if not policy:
            return RemediationDecision(
                decision_id=decision_id,
                failure_id=context.failure_id,
                selected_action="escalate_unrecognized_failure",
                action_level=ActionLevel.LEVEL_3,
                approval=ExecutionApproval.PENDING_HUMAN,
                confidence_threshold_met=False,
                rationale=f"No approved automated policy for root cause: {context.root_cause}",
                parameters={},
            )

        self.classifier.classify_action(policy.action)
        confidence_met = context.confidence >= self.min_confidence_threshold

        if not confidence_met:
            approval = ExecutionApproval.PENDING_HUMAN
            rationale = (
                f"Diagnostic confidence ({context.confidence:.2f}) is below the required "
                f"threshold ({self.min_confidence_threshold:.2f}). Human verification required."
            )
        elif policy.action_level == ActionLevel.LEVEL_3:
            approval = ExecutionApproval.PENDING_HUMAN
            rationale = f"Action {policy.action} is classified as Level 3 (High Risk) requiring human approval."
        else:
            approval = ExecutionApproval.AUTOMATIC
            rationale = (
                f"Policy matched for '{context.root_cause}' with high confidence ({context.confidence:.2f}). "
                f"Selected {policy.action_level.value} action: {policy.action}."
            )

        return RemediationDecision(
            decision_id=decision_id,
            failure_id=context.failure_id,
            selected_action=policy.action,
            action_level=policy.action_level,
            approval=approval,
            confidence_threshold_met=confidence_met,
            rationale=rationale,
            parameters={
                "target": policy.target_component,
                "blast_radius": policy.blast_radius,
                "max_attempts": policy.max_attempts,
                "cooldown_seconds": policy.cooldown_seconds,
            },
            estimated_duration_seconds=1.5 if policy.action_level == ActionLevel.LEVEL_1 else 3.0,
        )
