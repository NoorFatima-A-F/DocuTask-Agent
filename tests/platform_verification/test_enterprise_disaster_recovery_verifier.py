"""
Unit and Integration Tests for Disaster Recovery Architecture Verification (Part 3G.1).
"""
import pytest
from app.platform_verification.disaster_recovery_verification.domain.models import (
    ComponentTier,
    DRCertificationTier,
    DRMaturityLevel,
)
from app.platform_verification.disaster_recovery_verification.runtime.disaster_recovery_runtime import (
    DisasterRecoveryVerificationRuntime,
)
from app.platform_verification.disaster_recovery_verification.api.disaster_recovery_api import (
    DisasterRecoveryApiRouter,
)


@pytest.fixture
def runtime():
    return DisasterRecoveryVerificationRuntime()


def test_dr_architecture_discovery_and_criticality(runtime):
    inventory = runtime.discovery.discover_inventory()
    assert "postgres" in inventory.services
    assert "postgres" in inventory.critical_components

    criticality = runtime.discovery.classify_components()
    assert criticality["postgres"].tier == ComponentTier.TIER_0_MISSION_CRITICAL
    assert criticality["redis_queue"].tier == ComponentTier.TIER_1_CRITICAL
    assert criticality["postgres"].recovery_priority == 1

    bia = runtime.discovery.generate_bia()
    assert len(bia) >= 3
    assert any(b.business_function == "document_processing" for b in bia)


def test_recovery_dependency_graph(runtime):
    graph = runtime.dep_graph_engine.build_dependency_graph()
    assert graph.valid_order is True
    assert graph.topological_order[0] == "Infrastructure"
    assert graph.topological_order[-1] == "API"

    # Verify correct order validation
    assert runtime.dep_graph_engine.validate_recovery_order(
        ["Infrastructure", "Database", "Storage", "Queue", "Workers", "API"]
    ) is True
    # Verify incorrect order detection (Workers before Database)
    assert runtime.dep_graph_engine.validate_recovery_order(
        ["Infrastructure", "Workers", "Database", "Storage", "Queue", "API"]
    ) is False


def test_recovery_orchestration_execution(runtime):
    orch = runtime.recovery_orchestrator.execute_recovery_plan("test_scenario")
    assert orch["orchestration_status"] == "SUCCESS"
    assert orch["environment_rebuild"]["status"] == "HEALTHY"
    assert orch["database_restore"]["schema_migration_verified"] is True
    assert orch["storage_restore"]["checksum_match_percent"] == 100.0
    assert orch["validation"]["all_endpoints_healthy"] is True


def test_dr_scenario_simulations_and_rto_rpo(runtime):
    scenarios = runtime.test_harness.execute_all_scenarios()
    assert len(scenarios) == 5
    assert all(s.status == "PASS" for s in scenarios)
    assert all(not s.data_loss_detected for s in scenarios)
    assert all(s.rto_seconds <= 1200.0 for s in scenarios)
    assert all(s.rpo_seconds <= 300.0 for s in scenarios)


def test_data_recovery_integrity_and_security(runtime):
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    report = runtime.data_validator.validate_data_recovery(
        original_hash=h,
        restored_hash=h,
        expected_count=5000,
        restored_count=5000,
    )
    assert report.passed is True
    assert report.integrity_verified is True
    assert report.completeness_verified is True
    assert report.tenant_isolation_preserved is True

    sec = runtime.sec_validator.validate_dr_security()
    assert sec.passed is True
    assert sec.backup_encryption_at_rest_verified is True
    assert sec.backup_poisoning_rejected is True


def test_full_dr_scorecard_and_api(runtime):
    result = runtime.execute_full_dr_verification()
    scorecard = result["scorecard"]

    assert scorecard.composite_score >= 95.0
    assert scorecard.certification_tier == DRCertificationTier.ENTERPRISE_DR_READY
    assert scorecard.maturity_level == DRMaturityLevel.LEVEL_5_RESILIENT_ARCH
    assert scorecard.passed is True

    evidence = result["evidence"]
    assert "architecture_inventory.json" in evidence
    assert "criticality_matrix.json" in evidence
    assert "failure_scenarios.json" in evidence
    assert "recovery_dependency_graph.json" in evidence
    assert "backup_validation_report.json" in evidence
    assert "restore_test_report.json" in evidence
    assert "rto_rpo_report.json" in evidence
    assert "integrity_report.json" in evidence
    assert "security_report.json" in evidence
    assert "metadata.json" in evidence

    api = DisasterRecoveryApiRouter(runtime)
    api_resp = api.handle_run_full_dr_verification()
    assert api_resp["status"] == "SUCCESS"
    assert api_resp["certification"]["passed"] is True

    sim_resp = api.handle_simulate_scenario("DATABASE_DESTRUCTION")
    assert sim_resp["status"] == "PASS"
    assert sim_resp["data_loss_detected"] is False
