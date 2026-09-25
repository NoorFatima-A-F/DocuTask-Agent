"""Escalation Engine for monitoring SLAs and triggering escalation policies."""

from typing import List, Optional, Tuple
from datetime import datetime, timezone

from .rules import EscalationLevel, EscalationRule
from .handlers import EscalationHandler, EscalationEvent
from ..reviews.requests import ReviewRequest
from ..approvals.lifecycle import ApprovalLifecycleState


class EscalationEngine:
    """Evaluates timeouts and manages hierarchical human escalation."""

    DEFAULT_RULES: List[EscalationRule] = [
        EscalationRule(
            rule_id="esc_l1",
            name="Tier 1 SLA Breach Escalation",
            target_level=EscalationLevel.LEVEL_1_TEAM_LEAD,
            timeout_seconds=1800,  # 30 min
            target_roles=["team_lead", "senior_reviewer"],
        ),
        EscalationRule(
            rule_id="esc_l2",
            name="Tier 2 Stalled Review Escalation",
            target_level=EscalationLevel.LEVEL_2_DEPARTMENT_HEAD,
            timeout_seconds=3600,  # 1 hour
            target_roles=["compliance_officer", "department_head"],
        ),
        EscalationRule(
            rule_id="esc_l3",
            name="Tier 3 Critical Executive Escalation",
            target_level=EscalationLevel.LEVEL_3_EXECUTIVE,
            timeout_seconds=7200,  # 2 hours
            target_roles=["executive", "ciso"],
        ),
    ]

    def __init__(
        self,
        rules: Optional[List[EscalationRule]] = None,
        handler: Optional[EscalationHandler] = None,
    ):
        self.rules = list(rules or self.DEFAULT_RULES)
        self.handler = handler or EscalationHandler()

    def add_rule(self, rule: EscalationRule) -> EscalationRule:
        self.rules.append(rule)
        return rule

    def check_and_escalate(
        self, request: ReviewRequest, current_time: Optional[datetime] = None
    ) -> Tuple[bool, Optional[EscalationEvent]]:
        """Checks if a review request has breached timeout thresholds and escalates."""
        if request.status in {
            ApprovalLifecycleState.APPROVED,
            ApprovalLifecycleState.REJECTED,
            ApprovalLifecycleState.CANCELLED,
            ApprovalLifecycleState.ARCHIVED,
            ApprovalLifecycleState.EXPIRED,
        }:
            return False, None

        now = current_time or datetime.now(timezone.utc)
        elapsed_seconds = (now - request.created_at).total_seconds()
        current_level = request.escalation_level

        # Find candidate rule higher than current level whose timeout has passed
        candidate_rules = sorted(
            [
                r
                for r in self.rules
                if int(r.target_level) > current_level
                and (r.tenant_id == "*" or r.tenant_id == request.tenant_id)
                and elapsed_seconds >= r.timeout_seconds
            ],
            key=lambda r: int(r.target_level),
            reverse=True,
        )

        if candidate_rules:
            rule_to_apply = candidate_rules[0]
            reason = f"Review SLA exceeded ({elapsed_seconds:.0f}s elapsed >= {rule_to_apply.timeout_seconds}s threshold)"
            event = self.handler.handle_escalation(request, rule_to_apply, reason)
            request.status = ApprovalLifecycleState.ESCALATED
            return True, event

        return False, None
