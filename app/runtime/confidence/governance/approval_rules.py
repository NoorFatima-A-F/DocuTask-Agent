"""
Approval Rules Engine for Phase 13.3 (ASCE-CGP).
Determines autonomous approval vs human-in-the-loop review routing.
"""

from typing import Dict, Any


class ApprovalRulesEngine:
    """
    Decides whether a mission can proceed autonomously or requires human escalation.
    """

    @classmethod
    def evaluate_approval(cls, confidence_score: float, uncertainty: float) -> Dict[str, Any]:
        # High confidence & low uncertainty -> Full Autonomous Pass
        if confidence_score >= 0.95 and uncertainty <= 0.03:
            return {
                "decision": "AUTONOMOUS_APPROVED",
                "escalation_required": False,
                "reason": "Confidence exceeds 95% threshold with tight uncertainty interval.",
                "human_review_priority": "NONE",
            }
        elif confidence_score >= 0.85:
            return {
                "decision": "CONDITIONAL_APPROVAL",
                "escalation_required": False,
                "reason": "Confidence satisfies standard threshold; flagged for asynchronous quality audit.",
                "human_review_priority": "LOW",
            }
        else:
            return {
                "decision": "HUMAN_REVIEW_REQUIRED",
                "escalation_required": True,
                "reason": "Confidence below 85% safety boundary; routed to Human Review Inbox.",
                "human_review_priority": "HIGH",
            }
