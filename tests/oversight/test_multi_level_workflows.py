"""Tests for Sequential, Parallel, and Threshold Multi-Level Approval Workflows."""

from app.oversight.approvals.models import (
    ApprovalChain,
    ApprovalStep,
    ApprovalStrategy,
    StepExecutionStatus,
)
from app.oversight.core.decisions import HumanDecision, DecisionOutcome
from app.oversight.workflows.approval_flow import ApprovalWorkflowEngine


def test_sequential_approval_workflow():
    workflow = ApprovalWorkflowEngine()
    step1 = ApprovalStep(step_id="s1", order=1, name="Tier 1", required_roles=["analyst"])
    step2 = ApprovalStep(step_id="s2", order=2, name="Tier 2", required_roles=["manager"])
    chain = ApprovalChain(
        tenant_id="t1",
        name="2-Tier Sequential Chain",
        strategy=ApprovalStrategy.SEQUENTIAL,
        steps=[step1, step2],
    )
    workflow.initialize_chain_execution(chain)

    assert step1.status == StepExecutionStatus.IN_PROGRESS
    assert step2.status == StepExecutionStatus.PENDING

    # Step 1 approved
    d1 = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="usr_analyst",
        reviewer_role="analyst",
        outcome=DecisionOutcome.APPROVED,
        reason="Approved tier 1",
    )
    complete, outcome = workflow.process_decision(chain, d1)
    assert complete is False
    assert step1.status == StepExecutionStatus.APPROVED
    assert step2.status == StepExecutionStatus.IN_PROGRESS

    # Step 2 approved
    d2 = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="usr_mgr",
        reviewer_role="manager",
        outcome=DecisionOutcome.APPROVED,
        reason="Approved tier 2",
    )
    complete, outcome = workflow.process_decision(chain, d2)
    assert complete is True
    assert outcome == DecisionOutcome.APPROVED
    assert step2.status == StepExecutionStatus.APPROVED


def test_sequential_rejection_fail_fast():
    workflow = ApprovalWorkflowEngine()
    step1 = ApprovalStep(step_id="s1", order=1, name="Tier 1", required_roles=["analyst"])
    step2 = ApprovalStep(step_id="s2", order=2, name="Tier 2", required_roles=["manager"])
    chain = ApprovalChain(
        tenant_id="t1",
        name="2-Tier Sequential Chain",
        strategy=ApprovalStrategy.SEQUENTIAL,
        steps=[step1, step2],
    )
    workflow.initialize_chain_execution(chain)

    d_reject = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="usr_analyst",
        reviewer_role="analyst",
        outcome=DecisionOutcome.REJECTED,
        reason="Detected fraudulent line items.",
    )
    complete, outcome = workflow.process_decision(chain, d_reject)
    assert complete is True
    assert outcome == DecisionOutcome.REJECTED
    assert step1.status == StepExecutionStatus.REJECTED


def test_parallel_approval_workflow():
    workflow = ApprovalWorkflowEngine()
    step1 = ApprovalStep(step_id="s1", order=1, name="Security Check", required_roles=["secops"])
    step2 = ApprovalStep(step_id="s2", order=1, name="Legal Check", required_roles=["legal"])
    chain = ApprovalChain(
        tenant_id="t1",
        name="Parallel Chain",
        strategy=ApprovalStrategy.PARALLEL,
        steps=[step1, step2],
    )
    workflow.initialize_chain_execution(chain)

    assert step1.status == StepExecutionStatus.IN_PROGRESS
    assert step2.status == StepExecutionStatus.IN_PROGRESS

    # SecOps approves
    d_sec = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="usr_sec",
        reviewer_role="secops",
        outcome=DecisionOutcome.APPROVED,
        reason="SecOps cleared",
    )
    complete, _ = workflow.process_decision(chain, d_sec)
    assert complete is False
    assert step1.status == StepExecutionStatus.APPROVED
    assert step2.status == StepExecutionStatus.IN_PROGRESS

    # Legal approves
    d_leg = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="usr_leg",
        reviewer_role="legal",
        outcome=DecisionOutcome.APPROVED,
        reason="Legal cleared",
    )
    complete, outcome = workflow.process_decision(chain, d_leg)
    assert complete is True
    assert outcome == DecisionOutcome.APPROVED
    assert step2.status == StepExecutionStatus.APPROVED


def test_threshold_m_of_n_workflow():
    workflow = ApprovalWorkflowEngine()
    # 2 of 3 required
    step = ApprovalStep(
        step_id="s1",
        order=1,
        name="Committee 2-of-3",
        required_roles=["committee_member"],
        min_approvals_required=2,
    )
    chain = ApprovalChain(
        tenant_id="t1",
        name="Threshold Chain",
        strategy=ApprovalStrategy.THRESHOLD,
        steps=[step],
    )
    workflow.initialize_chain_execution(chain)

    d1 = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="member_1",
        reviewer_role="committee_member",
        outcome=DecisionOutcome.APPROVED,
        reason="Vote yes",
    )
    complete, _ = workflow.process_decision(chain, d1)
    assert complete is False

    d2 = HumanDecision(
        review_id="rev_1",
        tenant_id="t1",
        reviewer_id="member_2",
        reviewer_role="committee_member",
        outcome=DecisionOutcome.APPROVED,
        reason="Vote yes",
    )
    complete, outcome = workflow.process_decision(chain, d2)
    assert complete is True
    assert outcome == DecisionOutcome.APPROVED
