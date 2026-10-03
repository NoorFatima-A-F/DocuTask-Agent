"""
Comprehensive Unit and Integration Test Suite for Enterprise Disaster Recovery Simulation Framework.
Part 3G.3 — Disaster Recovery Simulation & Operational Resilience Verification for DocuTask Agent.
"""
import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.disaster_recovery_simulation.domain.models import (
    DisasterScenarioType,
    ChaosExperimentType,
    ResilienceCertificationLevel,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.database_loss_scenario import (
    DatabaseLossScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.database_corruption_scenario import (
    DatabaseCorruptionScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.storage_failure_scenario import (
    StorageFailureScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.complete_destruction_scenario import (
    CompleteDestructionScenario,
)
from app.platform_verification.disaster_recovery_simulation.scenarios.cascade_failure_scenario import (
    CascadeFailureScenario,
)
from app.platform_verification.disaster_recovery_simulation.injectors.container_terminator import (
    ContainerTerminationInjector,
)
from app.platform_verification.disaster_recovery_simulation.injectors.network_partition_injector import (
    NetworkPartitionInjector,
)
from app.platform_verification.disaster_recovery_simulation.injectors.resource_exhaustion_injector import (
    ResourceExhaustionInjector,
)
from app.platform_verification.disaster_recovery_simulation.detection.incident_detector import (
    IncidentDetector,
)
from app.platform_verification.disaster_recovery_simulation.recovery.automated_recovery_orchestrator import (
    AutomatedRecoveryOrchestrator,
)
from app.platform_verification.disaster_recovery_simulation.recovery.human_tabletop_simulator import (
    HumanTabletopSimulator,
)
from app.platform_verification.disaster_recovery_simulation.validators.recovery_validation_engine import (
    RecoveryValidationEngine,
)
from app.platform_verification.disaster_recovery_simulation.metrics.resilience_metrics_engine import (
    ResilienceMetricsEngine,
)
from app.platform_verification.disaster_recovery_simulation.runbooks.runbook_catalog import (
    RunbookCatalog,
)
from app.platform_verification.disaster_recovery_simulation.runtime.dr_simulation_runtime import (
    DisasterRecoverySimulationRuntime,
)
from app.platform_verification.disaster_recovery_simulation.api.dr_simulation_api import (
    router,
)


@pytest.fixture
def app_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_scenario_database_loss():
    """Verify Scenario 1: Database Loss & automated failover."""
    scenario = DatabaseLossScenario()
    res = scenario.execute_simulation()

    assert res.scenario_type == DisasterScenarioType.DATABASE_LOSS
    assert res.simulation_passed is True
    assert res.measured_rto_seconds <= 2700.0  # <= 45 minutes
    assert res.measured_rpo_seconds <= 300.0   # <= 5 minutes
    assert res.data_consistency_passed is True
    assert res.schema_intact is True
    assert res.relations_preserved is True
    assert len(res.timeline) >= 4


def test_scenario_database_corruption():
    """Verify Scenario 2: Database Corruption & Point-in-Time Recovery (PITR)."""
    scenario = DatabaseCorruptionScenario()
    res = scenario.execute_simulation()

    assert res.scenario_type == DisasterScenarioType.DATABASE_CORRUPTION
    assert res.simulation_passed is True
    assert res.measured_rto_seconds <= 2700.0
    assert res.details["corrupted_blocks_repaired"] > 0
    assert res.details["index_rebuild_status"] == "CONCURRENT_INDEX_REBUILD_SUCCESS"
    assert res.data_consistency_passed is True


def test_scenario_storage_failure():
    """Verify Scenario 3: Storage Failure & Cryptographic Hash Parity (H_orig == H_rec)."""
    scenario = StorageFailureScenario()
    res = scenario.execute_simulation()

    assert res.scenario_type == DisasterScenarioType.STORAGE_FAILURE
    assert res.simulation_passed is True
    assert res.details["cryptographic_hash_parity_verified"] is True
    assert res.details["hash_matches_count"] == 245
    assert res.details["hash_mismatches_count"] == 0


def test_scenario_complete_destruction():
    """Verify Scenario 4: Complete Cloud Annihilation & Bare-Metal Resurrection."""
    scenario = CompleteDestructionScenario()
    res = scenario.execute_simulation()

    assert res.scenario_type == DisasterScenarioType.COMPLETE_ENVIRONMENT_DESTRUCTION
    assert res.simulation_passed is True
    assert res.measured_rto_seconds <= 2700.0  # Recreated in 14.0m
    assert len(res.details["components_reconstructed"]) >= 5
    assert res.details["synthetic_document_processed"] is True


def test_scenario_cascade_failure():
    """Verify Scenario 5: Cascade Failure, Circuit Breaking, and Zero Dropped Jobs."""
    scenario = CascadeFailureScenario()
    res = scenario.execute_simulation()

    assert res.scenario_type == DisasterScenarioType.CASCADE_DEPENDENCY_FAILURE
    assert res.simulation_passed is True
    assert res.details["circuit_breaker_behavior"] == "TRIPPED_OPEN_THEN_AUTO_RESET"
    assert res.details["dropped_jobs_count"] == 0
    assert res.details["buffered_messages_processed"] > 0


def test_chaos_container_terminator():
    """Verify Chaos 1: Worker Container abrupt termination & restart."""
    injector = ContainerTerminationInjector()
    res = injector.inject_failure()

    assert res.experiment_type == ChaosExperimentType.CONTAINER_TERMINATION
    assert res.injection_successful is True
    assert res.recovery_detected is True
    assert res.self_healing_verified is True
    assert res.details["dropped_tasks"] == 0


def test_chaos_network_partition():
    """Verify Chaos 2: API-to-DB Network Partition & Circuit Breaker self-healing."""
    injector = NetworkPartitionInjector()
    res = injector.inject_failure()

    assert res.experiment_type == ChaosExperimentType.NETWORK_PARTITION
    assert res.injection_successful is True
    assert res.recovery_detected is True
    assert res.details["circuit_breaker_status"] == "TRIPPED_AND_HEALED"


def test_chaos_resource_exhaustion():
    """Verify Chaos 3: CPU & Memory Exhaustion, HPA autoscaling."""
    injector = ResourceExhaustionInjector()
    res = injector.inject_failure()

    assert res.experiment_type == ChaosExperimentType.RESOURCE_EXHAUSTION
    assert res.injection_successful is True
    assert res.recovery_detected is True
    assert res.details["oom_killed_containers"] == 0
    assert res.details["scaled_replicas"] > res.details["initial_replicas"]


def test_incident_detection_mttd():
    """Verify Incident Detection rules and MTTD <= 5 minutes."""
    detector = IncidentDetector()
    res = detector.test_incident_detection()

    assert res.detection_successful is True
    assert res.mttd_met is True
    assert res.measured_mttd_seconds <= 300.0  # Target <= 5m (measured ~38.5s)
    assert res.details["monitored_alert_rules_count"] >= 5


def test_automated_recovery_orchestrator():
    """Verify 6-stage automated disaster recovery lifecycle."""
    orchestrator = AutomatedRecoveryOrchestrator()
    workflow = orchestrator.execute_recovery_lifecycle()

    assert workflow["passed"] is True
    assert len(workflow["stages"]) == 6
    assert workflow["automation_level"] == "FULLY_AUTOMATED_L3_ORCHESTRATION"


def test_human_tabletop_simulator():
    """Verify Human Operational Tabletop simulation and decision quality."""
    simulator = HumanTabletopSimulator()
    res = simulator.run_tabletop_exercise()

    assert res.passed is True
    assert res.incident_response_team_notified is True
    assert res.recovery_decision_time_minutes <= 5.0
    assert res.decision_quality_score >= 95.0
    assert len(res.notes) >= 4


def test_recovery_validation_engine():
    """Verify post-recovery validation checks across API, DB, Docs, and Agent workflows."""
    engine = RecoveryValidationEngine()
    report = engine.validate_post_recovery_system()

    assert report.api_health_verified is True
    assert report.workers_active is True
    assert report.frontend_reachable is True
    assert report.database_migrations_intact is True
    assert report.database_foreign_keys_intact is True
    assert report.document_hashes_matched is True
    assert report.agent_workflows_resumed is True
    assert report.overall_validation_passed is True


def test_resilience_metrics_and_scoring():
    """Verify weighted resilience scoring formula and tier certification."""
    scenarios = [
        DatabaseLossScenario().execute_simulation(),
        DatabaseCorruptionScenario().execute_simulation(),
        StorageFailureScenario().execute_simulation(),
        CompleteDestructionScenario().execute_simulation(),
        CascadeFailureScenario().execute_simulation(),
    ]
    chaos = [
        ContainerTerminationInjector().inject_failure(),
        NetworkPartitionInjector().inject_failure(),
        ResourceExhaustionInjector().inject_failure(),
    ]
    detection = IncidentDetector().test_incident_detection()
    validation = RecoveryValidationEngine().validate_post_recovery_system()
    tabletop = HumanTabletopSimulator().run_tabletop_exercise()

    metrics_engine = ResilienceMetricsEngine()
    scorecard = metrics_engine.compute_resilience_scorecard(
        scenario_results=scenarios,
        chaos_results=chaos,
        detection_result=detection,
        validation_report=validation,
        tabletop_result=tabletop,
    )

    assert scorecard.composite_score >= 95.0
    assert scorecard.certification_level == ResilienceCertificationLevel.LEVEL_4_MISSION_CRITICAL
    assert scorecard.passed is True
    assert scorecard.ci_cd_deployment_approved is True
    assert scorecard.measured_rto_minutes <= 45.0
    assert scorecard.measured_rpo_minutes <= 5.0


def test_runbook_catalog():
    """Verify 5 executable recovery runbooks generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        catalog = RunbookCatalog()
        manifests = catalog.generate_all_runbooks(output_dir=tmpdir)

        assert len(manifests) == 5
        for name, path in manifests.items():
            assert os.path.exists(path), f"Missing runbook: {path}"
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                assert len(content) > 100


def test_dr_simulation_runtime_e2e():
    """Verify master DR simulation runtime execution and dual-directory artifact export."""
    with tempfile.TemporaryDirectory() as tmpdir_cert, tempfile.TemporaryDirectory() as tmpdir_ev, tempfile.TemporaryDirectory() as tmpdir_rb:
        runtime = DisasterRecoverySimulationRuntime()
        results = runtime.execute_full_dr_program(
            cert_dir=tmpdir_cert, evidence_dir=tmpdir_ev, runbooks_dir=tmpdir_rb
        )

        assert results["passed"] is True
        assert results["ci_cd_deployment_approved"] is True
        assert results["scorecard"].composite_score >= 95.0
        assert len(results["scenarios"]) == 5
        assert len(results["chaos_experiments"]) == 3
        assert len(results["exported_manifests"]) >= 15


def test_api_endpoints(app_client):
    """Verify all FastAPI router endpoints."""
    # 1. Simulate endpoint
    resp = app_client.post("/api/v1/platform-verification/disaster-recovery/simulate")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["composite_score"] >= 95.0
    assert data["ci_cd_deployment_approved"] is True

    # 2. Scorecard endpoint
    resp = app_client.get("/api/v1/platform-verification/disaster-recovery/resilience-scorecard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["composite_score"] >= 95.0

    # 3. Scenarios endpoint
    resp = app_client.get("/api/v1/platform-verification/disaster-recovery/scenarios")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_scenarios"] == 5

    # 4. Chaos endpoint
    resp = app_client.get("/api/v1/platform-verification/disaster-recovery/chaos-results")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_experiments"] == 3

    # 5. RTO/RPO endpoint
    resp = app_client.get("/api/v1/platform-verification/disaster-recovery/rto-rpo")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sla_verdict"] == "MISSION_CRITICAL_COMPLIANT"

    # 6. Continuous schedule endpoint
    resp = app_client.get("/api/v1/platform-verification/disaster-recovery/continuous-schedule")
    assert resp.status_code == 200
    data = resp.json()
    assert data["schedule_active"] is True
