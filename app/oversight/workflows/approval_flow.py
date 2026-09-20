"""Approval Workflow Engine supporting Sequential, Parallel, and Threshold Execution."""

from typing import Dict, Any, List, Optional, Tuple
from ..approvals.models import (
    ApprovalChain,
    ApprovalStep,
    ApprovalStrategy,
    StepExecutionStatus,
)
from ..core.decisions import HumanDecision, DecisionOutcome
from ..core.exceptions import OversightException


class ApprovalWorkflowEngine:
    """Orchestrates multi-level approval chains and evaluates step progression."""

    def initialize_chain_execution(self, chain: ApprovalChain) -> None:
        """Sets initial step statuses based on the chain's execution strategy."""
        if not chain.steps:
            return

        if chain.strategy == ApprovalStrategy.SEQUENTIAL:
            chain.steps[0].status = StepExecutionStatus.IN_PROGRESS
            for step in chain.steps[1:]:
                step.status = StepExecutionStatus.PENDING
        else:
            # Parallel & Threshold: All steps open concurrently
            for step in chain.steps:
                step.status = StepExecutionStatus.IN_PROGRESS

    def process_decision(
        self, chain: ApprovalChain, decision: HumanDecision
    ) -> Tuple[bool, Optional[DecisionOutcome]]:
        """
        Applies a reviewer decision to the active chain.
        Returns: (is_chain_complete, final_outcome)
        """
        reviewer = decision.reviewer_id

        if decision.outcome == DecisionOutcome.REJECTED:
            # Rejection in any step immediately fails the chain (fail-fast security principle)
            for step in chain.steps:
                if step.status == StepExecutionStatus.IN_PROGRESS:
                    if reviewer not in step.rejected_by:
                        step.rejected_by.append(reviewer)
                    step.status = StepExecutionStatus.REJECTED
            return True, DecisionOutcome.REJECTED

        if decision.outcome != DecisionOutcome.APPROVED:
            # ESCALATED / MODIFIED are handled at the review level
            return False, None

        # Process APPROVAL
        if chain.strategy == ApprovalStrategy.SEQUENTIAL:
            return self._process_sequential(chain, decision)
        elif chain.strategy == ApprovalStrategy.PARALLEL:
            return self._process_parallel(chain, decision)
        elif chain.strategy == ApprovalStrategy.THRESHOLD:
            return self._process_threshold(chain, decision)

        return False, None

    def _process_sequential(
        self, chain: ApprovalChain, decision: HumanDecision
    ) -> Tuple[bool, Optional[DecisionOutcome]]:
        reviewer = decision.reviewer_id
        current_step = next(
            (s for s in chain.steps if s.status == StepExecutionStatus.IN_PROGRESS),
            None,
        )
        if not current_step:
            return True, DecisionOutcome.APPROVED

        if reviewer not in current_step.approved_by:
            current_step.approved_by.append(reviewer)

        if len(current_step.approved_by) >= current_step.min_approvals_required:
            current_step.status = StepExecutionStatus.APPROVED

            # Advance to next step if exists
            next_step = next(
                (s for s in chain.steps if s.status == StepExecutionStatus.PENDING),
                None,
            )
            if next_step:
                next_step.status = StepExecutionStatus.IN_PROGRESS
                return False, None
            else:
                # All steps completed
                return True, DecisionOutcome.APPROVED

        return False, None

    def _process_parallel(
        self, chain: ApprovalChain, decision: HumanDecision
    ) -> Tuple[bool, Optional[DecisionOutcome]]:
        reviewer = decision.reviewer_id
        role = decision.reviewer_role

        for step in chain.steps:
            if step.status == StepExecutionStatus.IN_PROGRESS:
                role_matches = not step.required_roles or (role in step.required_roles)
                user_matches = reviewer in step.assigned_reviewers

                if role_matches or user_matches:
                    if reviewer not in step.approved_by:
                        step.approved_by.append(reviewer)
                    if len(step.approved_by) >= step.min_approvals_required:
                        step.status = StepExecutionStatus.APPROVED

        all_approved = all(s.status == StepExecutionStatus.APPROVED for s in chain.steps)
        if all_approved:
            return True, DecisionOutcome.APPROVED
        return False, None

    def _process_threshold(
        self, chain: ApprovalChain, decision: HumanDecision
    ) -> Tuple[bool, Optional[DecisionOutcome]]:
        reviewer = decision.reviewer_id
        # For threshold, aggregate unique approvals across all active steps
        total_unique_approvers = set()
        for step in chain.steps:
            if reviewer not in step.approved_by:
                step.approved_by.append(reviewer)
            total_unique_approvers.update(step.approved_by)

        min_required = sum(s.min_approvals_required for s in chain.steps)
        if len(total_unique_approvers) >= min_required:
            for step in chain.steps:
                step.status = StepExecutionStatus.APPROVED
            return True, DecisionOutcome.APPROVED

        return False, None
