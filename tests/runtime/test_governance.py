"""
Unit and Integration Tests for Governance Gates & Multi-Stage Approvals (ASVSP Pillar 9).
"""

import pytest
from app.runtime.certification import (
    GovernanceGateManager,
    CertificationPackageBuilder,
)


def test_governance_gate_workflow():
    gate_mgr = GovernanceGateManager()
    pkg_id = "CERT-TEST-001"

    s1 = gate_mgr.record_signoff(
        package_id=pkg_id,
        stage="AUTOMATED_CHECKS",
        approver_role="CI_BOT",
        approver_identity="ci-agent",
        comments="All tests green",
    )
    assert s1.stage == "AUTOMATED_CHECKS"

    status = gate_mgr.get_package_approval_status(pkg_id)
    assert status["is_fully_approved"] is False
    assert len(status["stages_passed"]) == 1

    # Final signoff
    gate_mgr.record_signoff(
        package_id=pkg_id,
        stage="DEPLOYED",
        approver_role="RELEASE_MANAGER",
        approver_identity="lead-eng",
        comments="Approved for production",
    )
    status_final = gate_mgr.get_package_approval_status(pkg_id)
    assert status_final["is_fully_approved"] is True
