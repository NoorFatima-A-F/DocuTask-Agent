"""Approval Service for managing approval chains, step execution, and policy evaluation."""

from typing import Dict, List, Optional, Tuple
import uuid

from .models import (
    ApprovalChain,
    ApprovalStep,
    ApprovalStrategy,
    StepExecutionStatus,
)
from .policies import ApprovalPolicy, ApprovalPolicyEngine
from ..core.context import OversightContext


class ApprovalService:
    """Manages approval chain lifecycles and step execution state."""

    def __init__(self, policy_engine: Optional[ApprovalPolicyEngine] = None):
        self.policy_engine = policy_engine or ApprovalPolicyEngine()
        self._chains: Dict[str, ApprovalChain] = {}

    def create_chain(self, chain: ApprovalChain) -> ApprovalChain:
        self._chains[chain.chain_id] = chain
        return chain

    def get_chain(self, chain_id: str) -> Optional[ApprovalChain]:
        return self._chains.get(chain_id)

    def generate_chain_for_context(
        self, context: OversightContext, matching_policy: Optional[ApprovalPolicy] = None
    ) -> ApprovalChain:
        """Generates an approval chain dynamically configured for the given context and policy."""
        if not matching_policy:
            _, pol, _ = self.policy_engine.evaluate(context)
            matching_policy = pol

        strategy = matching_policy.approval_strategy if matching_policy else ApprovalStrategy.SEQUENTIAL
        roles = matching_policy.required_roles if matching_policy else ["approver"]
        min_approvers = matching_policy.min_approvers if matching_policy else 1

        steps: List[ApprovalStep] = []
        if strategy == ApprovalStrategy.SEQUENTIAL:
            for idx, role in enumerate(roles, start=1):
                steps.append(
                    ApprovalStep(
                        step_id=f"step_{uuid.uuid4().hex[:8]}",
                        order=idx,
                        name=f"Tier {idx} Approval ({role})",
                        required_roles=[role],
                        min_approvals_required=1,
                        status=StepExecutionStatus.PENDING,
                    )
                )
        else:
            steps.append(
                ApprovalStep(
                    step_id=f"step_{uuid.uuid4().hex[:8]}",
                    order=1,
                    name=f"Review Group ({', '.join(roles)})",
                    required_roles=roles,
                    min_approvals_required=min_approvers,
                    status=StepExecutionStatus.PENDING,
                )
            )

        chain = ApprovalChain(
            chain_id=f"chn_{uuid.uuid4().hex[:10]}",
            tenant_id=context.tenant_id,
            name=f"Chain for {context.action_type} - {context.resource_id}",
            strategy=strategy,
            steps=steps,
            metadata={
                "request_id": context.request_id,
                "policy_id": matching_policy.policy_id if matching_policy else None,
                "risk_score": context.risk_score,
            },
        )
        self.create_chain(chain)
        return chain

    def evaluate_context(self, context: OversightContext) -> Tuple[bool, Optional[ApprovalPolicy], str]:
        return self.policy_engine.evaluate(context)
