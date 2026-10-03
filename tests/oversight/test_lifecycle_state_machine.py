"""Tests for Approval Lifecycle State Machine Transitions."""

import pytest
from app.oversight.approvals.lifecycle import ApprovalLifecycleState
from app.oversight.workflows.state_machine import ApprovalStateMachine
from app.oversight.core.exceptions import OversightException


def test_valid_lifecycle_transitions():
    sm = ApprovalStateMachine()
    review_id = "rev_lifecycle_100"

    # CREATED -> PENDING_REVIEW
    e1 = sm.transition(
        review_id=review_id,
        current_state=ApprovalLifecycleState.CREATED,
        target_state=ApprovalLifecycleState.PENDING_REVIEW,
        actor_id="system",
        reason="Triggered review policy",
    )
    assert e1.to_state == ApprovalLifecycleState.PENDING_REVIEW

    # PENDING_REVIEW -> ASSIGNED
    e2 = sm.transition(
        review_id=review_id,
        current_state=ApprovalLifecycleState.PENDING_REVIEW,
        target_state=ApprovalLifecycleState.ASSIGNED,
        actor_id="system",
        reason="Assigned to reviewer",
    )
    assert e2.to_state == ApprovalLifecycleState.ASSIGNED

    # ASSIGNED -> IN_REVIEW
    e3 = sm.transition(
        review_id=review_id,
        current_state=ApprovalLifecycleState.ASSIGNED,
        target_state=ApprovalLifecycleState.IN_REVIEW,
        actor_id="usr_reviewer",
        reason="Reviewer opened item",
    )
    assert e3.to_state == ApprovalLifecycleState.IN_REVIEW

    # IN_REVIEW -> APPROVED
    e4 = sm.transition(
        review_id=review_id,
        current_state=ApprovalLifecycleState.IN_REVIEW,
        target_state=ApprovalLifecycleState.APPROVED,
        actor_id="usr_reviewer",
        reason="Decision approved",
    )
    assert e4.to_state == ApprovalLifecycleState.APPROVED

    # APPROVED -> ARCHIVED
    e5 = sm.transition(
        review_id=review_id,
        current_state=ApprovalLifecycleState.APPROVED,
        target_state=ApprovalLifecycleState.ARCHIVED,
        actor_id="system",
        reason="Retained and archived",
    )
    assert e5.to_state == ApprovalLifecycleState.ARCHIVED

    history = sm.get_history(review_id)
    assert len(history) == 5


def test_invalid_lifecycle_transition_raises_error():
    sm = ApprovalStateMachine()
    review_id = "rev_invalid_01"

    with pytest.raises(OversightException) as exc_info:
        # Invalid: CREATED cannot directly transition to APPROVED
        sm.transition(
            review_id=review_id,
            current_state=ApprovalLifecycleState.CREATED,
            target_state=ApprovalLifecycleState.APPROVED,
            actor_id="bad_actor",
        )
    assert "Invalid lifecycle transition" in str(exc_info.value)
