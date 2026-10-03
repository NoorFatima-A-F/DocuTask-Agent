"""Tests for Release Lifecycle, SemVer Compatibility, and Approval Gates."""

import pytest
from app.infrastructure.deployment.releases import (
    ReleaseVersion,
    ApprovalDecision,
    ReleaseApprovalGate,
    ReleaseLifecycleStatus,
    ReleaseManager,
)


def test_semver_parsing_and_backward_compatibility() -> None:
    v1 = ReleaseVersion.parse("1.2.0")
    v1_patch = ReleaseVersion.parse("1.2.1")
    v2 = ReleaseVersion.parse("2.0.0-rc.1+build.10")

    assert str(v1) == "1.2.0"
    assert str(v2) == "2.0.0-rc.1+build.10"
    assert v1_patch.is_backward_compatible_with(v1) is True
    assert v2.is_backward_compatible_with(v1) is False


def test_release_approval_gate_and_lifecycle() -> None:
    gate = ReleaseApprovalGate()
    mgr = ReleaseManager(approval_gate=gate)

    rel = mgr.create_release(
        version="1.3.0",
        components_changed=["ocr-service", "gateway"],
        artifact_ids=["art-1", "art-2"],
        changelog="Added GPU OCR acceleration",
    )
    assert rel.status == ReleaseLifecycleStatus.CREATED

    # Advance to VALIDATED
    mgr.transition_status(rel.release_id, ReleaseLifecycleStatus.VALIDATED)

    # Attempting to RELEASE without required approvals fails
    with pytest.raises(PermissionError, match="without mandatory stakeholder approvals"):
        mgr.transition_status(rel.release_id, ReleaseLifecycleStatus.RELEASED)

    # Record required approvals: governance, security, sre
    gate.record_decision(rel.release_id, "auditor-01", "governance", ApprovalDecision.APPROVED)
    gate.record_decision(rel.release_id, "sec-lead", "security", ApprovalDecision.APPROVED)
    gate.record_decision(rel.release_id, "sre-lead", "sre", ApprovalDecision.APPROVED)

    assert gate.is_release_approved(rel.release_id) is True

    # Transition to RELEASED and COMPLETED
    mgr.transition_status(rel.release_id, ReleaseLifecycleStatus.RELEASED)
    assert rel.status == ReleaseLifecycleStatus.RELEASED
    assert rel.released_at is not None

    mgr.transition_status(rel.release_id, ReleaseLifecycleStatus.COMPLETED)
    assert rel.status == ReleaseLifecycleStatus.COMPLETED
