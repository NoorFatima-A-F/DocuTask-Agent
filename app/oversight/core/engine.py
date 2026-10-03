"""Central Human Oversight Engine orchestrating policies, reviews, workflows, escalations, and overrides."""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
import uuid

from .context import OversightContext
from .decisions import HumanDecision, DecisionOutcome, FeedbackAssessment
from .exceptions import (
    OversightException,
    UnauthorizedReviewerError,
    InvalidOverrideError,
    EscalationTimeoutError,
    ApprovalPolicyViolationError,
)
from ..approvals.models import (
    ApprovalPolicyType,
    ApprovalStrategy,
    ApprovalChain,
    ApprovalStep,
    StepExecutionStatus,
)
from ..approvals.policies import ApprovalPolicy, ApprovalPolicyEngine
from ..approvals.lifecycle import ApprovalLifecycleState
from ..approvals.service import ApprovalService
from ..reviews.requests import ReviewRequest, ReviewPriority
from ..reviews.evidence import ReviewEvidencePackage
from ..reviews.comments import ReviewComment
from ..reviews.assignments import (
    Reviewer,
    ReviewerAuthority,
    ReviewerAssignmentEngine,
)
from ..workflows.state_machine import ApprovalStateMachine
from ..workflows.approval_flow import ApprovalWorkflowEngine
from ..escalation.rules import EscalationRule, EscalationLevel
from ..escalation.handlers import EscalationHandler, EscalationEvent
from ..escalation.engine import EscalationEngine
from ..overrides.policies import OverridePolicy
from ..overrides.validation import OverrideValidator
from ..overrides.service import OverrideService, HumanOverrideRecord
from ..notifications.channels import NotificationChannel, NotificationEventType
from ..notifications.dispatcher import NotificationDispatcher
from ..analytics.metrics import OversightMetricsCollector, OversightAnalyticsSummary


class HumanOversightEngine:
    """Master human oversight control plane for DocuTask Agent platform."""

    def __init__(
        self,
        policy_engine: Optional[ApprovalPolicyEngine] = None,
        approval_service: Optional[ApprovalService] = None,
        assignment_engine: Optional[ReviewerAssignmentEngine] = None,
        workflow_engine: Optional[ApprovalWorkflowEngine] = None,
        state_machine: Optional[ApprovalStateMachine] = None,
        escalation_engine: Optional[EscalationEngine] = None,
        override_service: Optional[OverrideService] = None,
        dispatcher: Optional[NotificationDispatcher] = None,
        metrics_collector: Optional[OversightMetricsCollector] = None,
    ):
        self.policy_engine = policy_engine or ApprovalPolicyEngine()
        self.approval_service = approval_service or ApprovalService(policy_engine=self.policy_engine)
        self.assignment_engine = assignment_engine or ReviewerAssignmentEngine()
        self.workflow_engine = workflow_engine or ApprovalWorkflowEngine()
        self.state_machine = state_machine or ApprovalStateMachine()
        self.escalation_engine = escalation_engine or EscalationEngine()
        self.override_service = override_service or OverrideService()
        self.dispatcher = dispatcher or NotificationDispatcher()
        self.metrics = metrics_collector or OversightMetricsCollector()

        # In-memory stores
        self._reviews: Dict[str, ReviewRequest] = {}
        self._evidence_packages: Dict[str, ReviewEvidencePackage] = {}
        self._comments: Dict[str, List[ReviewComment]] = {}
        self._decisions: Dict[str, List[HumanDecision]] = {}

    def evaluate_context(self, context: OversightContext) -> Tuple[bool, Optional[ApprovalPolicy], str]:
        """Evaluates whether an action requires human review."""
        return self.policy_engine.evaluate(context)

    def create_review_request(
        self,
        context: OversightContext,
        evidence: Optional[ReviewEvidencePackage] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: ReviewPriority = ReviewPriority.MEDIUM,
    ) -> Tuple[ReviewRequest, ApprovalChain]:
        """Creates an approval chain, review request, attaches evidence, and assigns a reviewer."""
        requires_approval, matching_policy, reason = self.evaluate_context(context)

        # Generate approval chain
        chain = self.approval_service.generate_chain_for_context(context, matching_policy)
        self.workflow_engine.initialize_chain_execution(chain)

        # Determine required roles
        req_roles = matching_policy.required_roles if matching_policy else ["reviewer"]

        # Determine priority based on risk
        if context.risk_score >= 0.8 or context.business_impact == "CRITICAL":
            priority = ReviewPriority.CRITICAL
        elif context.risk_score >= 0.6 or context.business_impact == "HIGH":
            priority = ReviewPriority.HIGH

        review = ReviewRequest(
            review_id=f"rev_{uuid.uuid4().hex[:10]}",
            request_id=context.request_id,
            tenant_id=context.tenant_id,
            title=title or f"Human Review Required: {context.action_type} on {context.resource_id}",
            description=description or reason,
            status=ApprovalLifecycleState.PENDING_REVIEW,
            priority=priority,
            resource_type=context.resource_type,
            resource_id=context.resource_id,
            action_type=context.action_type,
            chain_id=chain.chain_id,
            required_roles=req_roles,
            deadline=context.deadline,
            metadata={"risk_score": context.risk_score, "policy_id": matching_policy.policy_id if matching_policy else None},
        )

        self._reviews[review.review_id] = review
        self.state_machine.transition(
            review_id=review.review_id,
            current_state=ApprovalLifecycleState.CREATED,
            target_state=ApprovalLifecycleState.PENDING_REVIEW,
            actor_id="system",
            reason=reason,
        )

        # Attach evidence package if provided
        if evidence:
            evidence.review_id = review.review_id
            self._evidence_packages[review.review_id] = evidence

        # Attempt reviewer assignment
        assigned_reviewer = self.assignment_engine.assign_reviewer(review, context)
        if assigned_reviewer:
            self.state_machine.transition(
                review_id=review.review_id,
                current_state=ApprovalLifecycleState.PENDING_REVIEW,
                target_state=ApprovalLifecycleState.ASSIGNED,
                actor_id="system",
                reason=f"Assigned to reviewer {assigned_reviewer.name} ({assigned_reviewer.user_id})",
            )
            review.status = ApprovalLifecycleState.ASSIGNED

            # Dispatch notification
            self.dispatcher.dispatch(
                event_type=NotificationEventType.REVIEW_ASSIGNED,
                recipient_id=assigned_reviewer.user_id,
                title=f"Review Assigned: {review.title}",
                body=f"You have been assigned review {review.review_id} for {review.action_type}.",
                review_id=review.review_id,
            )
        else:
            self.dispatcher.dispatch(
                event_type=NotificationEventType.REVIEW_REQUIRED,
                recipient_id=context.tenant_id,
                title=f"Review Pending Assignment: {review.title}",
                body=f"Review {review.review_id} is waiting for available reviewers.",
                review_id=review.review_id,
            )

        self.metrics.record_review(review)
        return review, chain

    def get_review_request(self, review_id: str) -> Optional[ReviewRequest]:
        return self._reviews.get(review_id)

    def list_review_requests(
        self,
        tenant_id: Optional[str] = None,
        status: Optional[ApprovalLifecycleState] = None,
        reviewer_id: Optional[str] = None,
    ) -> List[ReviewRequest]:
        results = list(self._reviews.values())
        if tenant_id:
            results = [r for r in results if r.tenant_id == tenant_id]
        if status:
            results = [r for r in results if r.status == status]
        if reviewer_id:
            results = [r for r in results if reviewer_id in r.assigned_reviewers]
        return results

    def submit_decision(
        self,
        review_id: str,
        reviewer_id: str,
        outcome: DecisionOutcome,
        reason: str,
        reviewer_role: Optional[str] = None,
        feedback: Optional[FeedbackAssessment] = None,
        modified_parameters: Optional[Dict[str, Any]] = None,
        context: Optional[OversightContext] = None,
    ) -> HumanDecision:
        """Processes a human decision and updates approval chain and lifecycle states."""
        review = self._reviews.get(review_id)
        if not review:
            raise OversightException(f"Review request '{review_id}' not found")

        # Verify reviewer profile & authority
        reviewer = self.assignment_engine.get_reviewer(reviewer_id)
        actual_role = reviewer_role or (reviewer.roles[0] if reviewer and reviewer.roles else "reviewer")

        if reviewer and context:
            authorized, auth_reason = self.assignment_engine.verify_authority(reviewer, context)
            if not authorized:
                raise UnauthorizedReviewerError(f"Reviewer lacks authority: {auth_reason}")

        decision = HumanDecision(
            review_id=review_id,
            tenant_id=review.tenant_id,
            reviewer_id=reviewer_id,
            reviewer_role=actual_role,
            outcome=outcome,
            reason=reason,
            feedback=feedback,
            modified_parameters=modified_parameters,
        )

        if review_id not in self._decisions:
            self._decisions[review_id] = []
        self._decisions[review_id].append(decision)

        # Update approval chain if exists
        chain = self.approval_service.get_chain(review.chain_id) if review.chain_id else None
        chain_completed = False
        final_chain_outcome = None

        if chain:
            chain_completed, final_chain_outcome = self.workflow_engine.process_decision(
                chain, decision
            )

        # Transition lifecycle state
        from_state = review.status
        if outcome == DecisionOutcome.REJECTED or final_chain_outcome == DecisionOutcome.REJECTED:
            target_state = ApprovalLifecycleState.REJECTED
            review.status = target_state
            review.closed_at = datetime.now(timezone.utc)
            review.decision_id = decision.decision_id
            self.state_machine.transition(
                review_id=review_id,
                current_state=from_state,
                target_state=target_state,
                actor_id=reviewer_id,
                reason=reason,
            )
            for assigned in review.assigned_reviewers:
                self.assignment_engine.release_reviewer(assigned)
        elif outcome == DecisionOutcome.APPROVED:
            if chain_completed or not chain:
                target_state = ApprovalLifecycleState.APPROVED
                review.status = target_state
                review.closed_at = datetime.now(timezone.utc)
                review.decision_id = decision.decision_id
                self.state_machine.transition(
                    review_id=review_id,
                    current_state=from_state,
                    target_state=target_state,
                    actor_id=reviewer_id,
                    reason=reason,
                )
                for assigned in review.assigned_reviewers:
                    self.assignment_engine.release_reviewer(assigned)
            else:
                # Still in progress across subsequent steps
                if review.status != ApprovalLifecycleState.IN_REVIEW:
                    self.state_machine.transition(
                        review_id=review_id,
                        current_state=from_state,
                        target_state=ApprovalLifecycleState.IN_REVIEW,
                        actor_id=reviewer_id,
                        reason="Step approved; advancing to subsequent approval step",
                    )
                    review.status = ApprovalLifecycleState.IN_REVIEW

        # Dispatch decision event
        self.dispatcher.dispatch(
            event_type=NotificationEventType.DECISION_SUBMITTED,
            recipient_id=review.tenant_id,
            title=f"Decision Submitted for {review.title}: {outcome.value}",
            body=f"Reviewer {reviewer_id} marked review as {outcome.value}. Reason: {reason}",
            review_id=review_id,
        )

        self.metrics.record_decision(decision)
        return decision

    def execute_override(
        self,
        review_id: str,
        reviewer_id: str,
        reviewer_role: str,
        original_ai_decision: Any,
        overridden_human_decision: Any,
        justification: str,
        context: OversightContext,
        policy: Optional[OverridePolicy] = None,
    ) -> HumanOverrideRecord:
        """Executes a controlled human override."""
        review = self._reviews.get(review_id)
        if not review:
            raise OversightException(f"Review request '{review_id}' not found")

        record = self.override_service.execute_override(
            review_id=review_id,
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            original_ai_decision=original_ai_decision,
            overridden_human_decision=overridden_human_decision,
            justification=justification,
            context=context,
            policy=policy,
        )

        # Mark review as approved via manual override
        decision = self.submit_decision(
            review_id=review_id,
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            outcome=DecisionOutcome.MODIFIED,
            reason=f"Controlled Override Executed: {justification}",
            feedback=FeedbackAssessment.AI_INCORRECT,
            context=context,
        )

        self.metrics.record_override(record)
        self.dispatcher.dispatch(
            event_type=NotificationEventType.HUMAN_OVERRIDE_EXECUTED,
            recipient_id=review.tenant_id,
            title=f"Human Override Executed: {review.title}",
            body=f"Reviewer {reviewer_id} overrode decision. Reason: {justification}",
            review_id=review_id,
        )
        return record

    def check_escalations(self, current_time: Optional[datetime] = None) -> List[EscalationEvent]:
        """Scans all active review requests and triggers escalations where applicable."""
        events: List[EscalationEvent] = []
        for review in self._reviews.values():
            escalated, event = self.escalation_engine.check_and_escalate(review, current_time)
            if escalated and event:
                events.append(event)
                # Dispatch notification
                self.dispatcher.dispatch(
                    event_type=NotificationEventType.REVIEW_ESCALATED,
                    recipient_id=review.tenant_id,
                    title=f"Review Escalated: {review.title} (Level {event.to_level.value})",
                    body=f"Review {review.review_id} escalated due to SLA breach. Reason: {event.reason}",
                    review_id=review.review_id,
                )
        return events

    def add_comment(
        self,
        review_id: str,
        author_id: str,
        author_name: str,
        author_role: str,
        text: str,
        is_internal: bool = False,
    ) -> ReviewComment:
        review = self._reviews.get(review_id)
        if not review:
            raise OversightException(f"Review request '{review_id}' not found")

        comment = ReviewComment(
            review_id=review_id,
            tenant_id=review.tenant_id,
            author_id=author_id,
            author_name=author_name,
            author_role=author_role,
            text=text,
            is_internal=is_internal,
        )
        if review_id not in self._comments:
            self._comments[review_id] = []
        self._comments[review_id].append(comment)
        return comment

    def get_comments(self, review_id: str) -> List[ReviewComment]:
        return self._comments.get(review_id, [])

    def get_evidence(self, review_id: str) -> Optional[ReviewEvidencePackage]:
        return self._evidence_packages.get(review_id)

    def get_analytics(self, tenant_id: str = "*") -> OversightAnalyticsSummary:
        return self.metrics.compute_summary(tenant_id)
