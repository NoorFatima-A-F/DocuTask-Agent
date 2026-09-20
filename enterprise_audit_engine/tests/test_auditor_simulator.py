"""Tests for Multi-Persona Auditor Simulation Framework."""

import pytest
from enterprise_audit_engine.auditor_simulator.simulation_engine import (
    AuditorSimulator,
    AuditorSimulationReport,
)
from enterprise_audit_engine.auditor_simulator.personas import AuditorPersonas


def test_auditor_simulation_full_pass():
    evidence = [
        {"id": "EV-TEST-1", "category": "AutomatedTesting", "classification": "VERIFIED"},
        {"id": "EV-SEC-1", "category": "SecurityAndCompliance", "classification": "VERIFIED"},
    ]
    rep = AuditorSimulator.run_simulation(evidence, {}, target_system="DocuTask Agent", target_version="v1.0.0")

    assert isinstance(rep, AuditorSimulationReport)
    assert rep.consensus_passed is True
    assert rep.status == "AUDITOR_CONSENSUS_APPROVED"
    assert rep.consensus_score >= 85.0
    assert "PrincipalEngineer" in rep.persona_reviews
    assert "SecurityAuditor" in rep.persona_reviews
    assert "CTOReviewer" in rep.persona_reviews
    assert "DueDiligenceTeam" in rep.persona_reviews


def test_auditor_simulation_blocks_on_missing_security():
    evidence = [
        {"id": "EV-TEST-1", "category": "AutomatedTesting", "classification": "VERIFIED"}
    ]
    rep = AuditorSimulator.run_simulation(evidence, {}, target_system="DocuTask Agent", target_version="v1.0.0")

    assert rep.consensus_passed is False
    assert rep.status == "AUDITOR_REVIEW_BLOCKED"
    assert "Zero Known Vulnerabilities" in rep.all_blocked_claims
    assert rep.persona_reviews["SecurityAuditor"].passed is False
