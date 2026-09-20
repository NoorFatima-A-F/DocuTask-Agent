"""
Unit and integration tests for Phase V8 — Enterprise Autonomous Agent Workforce Verification & Validation Program (EAAWVVP).
"""

import os
import json
import pytest

from app.workforce_verification import (
    PartId,
    AgentRole,
    AgentLifecycleState,
    ClearanceLevel,
    VerificationStatus,
    AgentProfile,
    TeamDefinition,
    MarketplaceBid,
    WorkforceScorer,
    EvidenceGenerator,
)
from app.workforce_verification.registry.registry_verifier import RegistryVerifier
from app.workforce_verification.capabilities.capabilities_verifier import CapabilitiesVerifier
from app.workforce_verification.hierarchy.hierarchy_verifier import HierarchyVerifier
from app.workforce_verification.teams.team_formation_verifier import TeamFormationVerifier
from app.workforce_verification.marketplace.marketplace_verifier import MarketplaceVerifier
from app.workforce_verification.negotiation.negotiation_verifier import NegotiationVerifier
from app.workforce_verification.collaboration.collaboration_verifier import CollaborationVerifier
from app.workforce_verification.management.management_verifier import ManagementVerifier
from app.workforce_verification.council.council_verifier import CouncilVerifier
from app.workforce_verification.economics.economics_verifier import EconomicsVerifier
from app.workforce_verification.hiring.hiring_verifier import HiringVerifier
from app.workforce_verification.career.career_verifier import CareerVerifier
from app.workforce_verification.scheduler.scheduler_verifier import SchedulerVerifier
from app.workforce_verification.conflict.conflict_verifier import ConflictVerifier
from app.workforce_verification.memory.memory_verifier import MemoryVerifier
from app.workforce_verification.trust.trust_verifier import TrustVerifier
from app.workforce_verification.security.security_verifier import SecurityVerifier
from app.workforce_verification.scalability.scalability_verifier import ScalabilityVerifier
from app.workforce_verification.benchmarks.benchmark_verifier import BenchmarkVerifier
from app.workforce_verification.dashboards.dashboard_verifier import DashboardVerifier


def test_domain_models():
    profile = AgentProfile(
        agent_id="agt_001",
        name="DocuExtractor-Alpha",
        role=AgentRole.SPECIALIST,
        department="Extraction",
        clearance=ClearanceLevel.LEVEL_3_CONFIDENTIAL,
        cost_per_task=0.015,
        skills=["ocr_correction", "regex_parsing"],
        state=AgentLifecycleState.ACTIVE,
    )
    d = profile.to_dict()
    assert d["agent_id"] == "agt_001"
    assert d["role"] == "SPECIALIST"
    assert d["clearance"] == 3
    assert d["state"] == "ACTIVE"
    assert "ocr_correction" in d["skills"]

    team = TeamDefinition(
        team_id="team_alpha",
        name="Tax Extraction Guild",
        lead_agent_id="agt_lead",
        member_agent_ids=["agt_001", "agt_002"],
        mission="Process Q3 corporate tax filings",
        fitness_score=0.96,
    )
    td = team.to_dict()
    assert td["team_id"] == "team_alpha"
    assert td["fitness_score"] == 0.96

    bid = MarketplaceBid(
        bid_id="bid_101",
        task_id="tsk_901",
        agent_id="agt_001",
        proposed_cost=0.05,
        estimated_duration_ms=12500.0,
        reputation_score=0.98,
        is_winning_bid=True,
    )
    bd = bid.to_dict()
    assert bd["bid_id"] == "bid_101"
    assert bd["proposed_cost"] == 0.05
    assert bd["is_winning_bid"] is True


def test_part_01_registry():
    v = RegistryVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_01_REGISTRY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_02_capabilities():
    v = CapabilitiesVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_02_CAPABILITIES
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_03_hierarchy():
    v = HierarchyVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_03_HIERARCHY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_04_teams():
    v = TeamFormationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_04_TEAMS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_05_marketplace():
    v = MarketplaceVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_05_MARKETPLACE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_06_negotiation():
    v = NegotiationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_06_NEGOTIATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_07_collaboration():
    v = CollaborationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_07_COLLABORATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_08_management():
    v = ManagementVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_08_MANAGEMENT
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_09_council():
    v = CouncilVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_09_COUNCIL
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_10_economics():
    v = EconomicsVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_10_ECONOMICS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_11_hiring():
    v = HiringVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_11_HIRING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_12_career():
    v = CareerVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_12_CAREER
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_13_scheduler():
    v = SchedulerVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_13_SCHEDULER
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_14_conflict():
    v = ConflictVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_14_CONFLICT
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_15_memory():
    v = MemoryVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_15_MEMORY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_16_trust():
    v = TrustVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_16_TRUST
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_17_security():
    v = SecurityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_17_SECURITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_18_scalability():
    v = ScalabilityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_18_SCALABILITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_19_benchmarks():
    v = BenchmarkVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_19_BENCHMARKS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_20_dashboards():
    v = DashboardVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_20_DASHBOARDS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_workforce_scorer():
    scorer = WorkforceScorer()
    scorecard = scorer.run_all()
    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.production_ready is True
    assert scorecard.total_assertions == 80
    assert scorecard.passed_assertions == 80
    assert len(scorecard.parts) == 20
    assert len(scorecard.indices) == 10


def test_evidence_generator(tmp_path):
    scorer = WorkforceScorer()
    scorecard = scorer.run_all()
    
    exporter = EvidenceGenerator(
        output_dir=str(tmp_path / "evidence"),
        report_path=str(tmp_path / "report.md")
    )
    summary = exporter.export_all(scorecard)
    
    assert os.path.exists(summary["output_dir"])
    assert os.path.exists(summary["manifest_file"])
    assert os.path.exists(summary["report_path"])
    
    with open(summary["manifest_file"], "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert len(manifest["checksums"]) == 21  # 20 parts + 1 summary
    assert "Phase V8" in manifest["verification_program"]
    assert manifest["composite_score"] == 100.0
