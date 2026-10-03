"""
DocuTask Agent - Production Reliability & Chaos Platform Pytest Suite (APRCORP+)
Phase 12: Autonomous Production Reliability, Chaos Engineering & Operational Resilience
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.runtime.resilience import (
    digital_twin_engine,
    chaos_orchestrator,
    recovery_marketplace,
    incident_commander,
    dependency_graph,
    blast_radius_engine,
    reliability_math_engine,
    invariant_monitor,
    production_readiness_engine,
    time_travel_engine,
    stress_arena_engine,
    certification_dossier_engine,
    NodeHealthStatus,
    ChaosFaultType,
    InjectionStatus,
    IncidentSeverity,
    IncidentState,
)


@pytest.fixture
def client():
    return TestClient(app)


# --- 1. Digital Twin Tests ---

def test_digital_twin_topology_and_health():
    state = digital_twin_engine.get_topology_dict()
    assert state["overall_health_score"] >= 0.0
    assert state["total_nodes"] >= 8
    assert state["total_edges"] >= 8
    assert any(n["node_id"] == "node-planner" for n in state["nodes"])


def test_digital_twin_heartbeat_and_mutation():
    node = digital_twin_engine.register_heartbeat("node-planner", latency_ms=15.0, error_rate=0.0, cpu_pct=10.0)
    assert node is not None
    assert node.health == NodeHealthStatus.HEALTHY

    # Mutate to failing
    mutated = digital_twin_engine.mutate_node_health("node-planner", NodeHealthStatus.FAILING, latency_ms=3000.0, error_rate=0.9)
    assert mutated is True
    assert digital_twin_engine.nodes["node-planner"].health == NodeHealthStatus.FAILING

    # Heal
    healed = digital_twin_engine.heal_node("node-planner")
    assert healed is True
    assert digital_twin_engine.nodes["node-planner"].health == NodeHealthStatus.HEALTHY


def test_digital_twin_snapshot():
    snap = digital_twin_engine.capture_snapshot(mission_id="test-mission-001")
    assert snap.snapshot_id.startswith("twin-snap-")
    assert snap.overall_health_score >= 0.0
    assert len(snap.nodes) >= 8


# --- 2. Chaos Orchestrator Tests ---

def test_chaos_scenarios_listing():
    scenarios = chaos_orchestrator.list_scenarios()
    assert len(scenarios) >= 5
    assert any(s.fault_type == ChaosFaultType.GEMINI_TIMEOUT for s in scenarios)


def test_chaos_injection_and_recovery():
    # Inject fault
    inject_res = chaos_orchestrator.inject_fault("chaos-gemini-timeout")
    assert inject_res["status"] == InjectionStatus.ACTIVE.value
    assert inject_res["target_node_id"] == "node-gemini"

    # Recover fault
    rec_res = chaos_orchestrator.recover_fault("chaos-gemini-timeout", "FAILOVER_TO_GEMINI_FLASH")
    assert rec_res["status"] == InjectionStatus.HEALED.value
    assert rec_res["recovery_latency_ms"] >= 0.0
    assert rec_res["digital_twin_health_score"] >= 90.0


def test_chaos_summary():
    summary = chaos_orchestrator.get_orchestrator_summary()
    assert summary["total_scenarios"] >= 5
    assert summary["resilience_grade"] in ["ENTERPRISE_GRADE_AAA", "DEGRADED_FAILOVER_ACTIVE"]


# --- 3. Recovery Marketplace Tests ---

def test_recovery_marketplace_strategies():
    summary = recovery_marketplace.get_marketplace_summary()
    assert summary["total_strategies"] >= 5
    assert summary["overall_recovery_success_rate_pct"] >= 95.0
    assert len(summary["strategies"]) >= 5
    assert summary["strategies"][0]["utility_score"] > 0.0


def test_recovery_execution():
    exec_res = recovery_marketplace.execute_recovery("strat-gemini-flash-fallback")
    assert exec_res.status == "SUCCESS"
    assert exec_res.duration_ms > 0.0
    assert exec_res.state_parity_achieved_pct >= 99.8


# --- 4. Incident Commander Tests ---

def test_incident_declaration_and_lifecycle():
    inc = incident_commander.declare_incident(
        title="Test Redis Partition",
        severity=IncidentSeverity.SEV2_HIGH,
        root_cause_node_id="node-storage",
        blast_radius_nodes=["node-workers"],
    )
    assert inc.incident_id.startswith("inc-")
    assert inc.current_state == IncidentState.DETECTED

    # Advance state
    adv = incident_commander.advance_incident_state(
        inc.incident_id, IncidentState.TRIAGING, "Diagnostic subagent verifying shard status"
    )
    assert adv.current_state == IncidentState.TRIAGING

    # Auto mitigate
    mit_res = incident_commander.auto_mitigate_incident(inc.incident_id)
    assert mit_res["status"] == IncidentState.RESOLVED.value
    assert mit_res["recovery_duration_ms"] > 0.0


# --- 5. Dynamic Dependency Graph & Blast Radius Tests ---

def test_dependency_topology():
    nodes = dependency_graph.list_nodes()
    assert len(nodes) >= 8
    upstream = dependency_graph.get_upstream_dependencies("planner-engine")
    assert len(upstream) >= 2


def test_blast_radius_analysis():
    analysis = blast_radius_engine.analyze_node_failure("gemini-api")
    assert analysis.failed_node_id == "gemini-api"
    assert analysis.blast_radius_pct > 0.0
    assert analysis.risk_level in ["LOW", "MEDIUM", "HIGH", "CATASTROPHIC"]

    matrix = blast_radius_engine.get_full_topology_risk_matrix()
    assert len(matrix) >= 8


# --- 6. Reliability Mathematics Tests ---

def test_reliability_math_computation():
    report = reliability_math_engine.compute_reliability_report(
        completion_rate=0.999,
        replay_parity=0.9998,
        evidence_hash_integrity=1.0,
        recovery_success_rate=0.995,
        trust_index=0.99,
        mtbf_hours=720.0,
        mttr_seconds=0.085,
    )
    assert report.composite_reliability_score >= 98.0
    assert report.operational_availability_pct >= 99.99
    assert report.resilience_tier in ["TIER_4_MISSION_CRITICAL", "TIER_3_PRODUCTION_READY"]
    assert len(report.dimensions) == 6


# --- 7. Invariants Monitor Tests ---

def test_invariant_monitor_evaluation():
    inv_eval = invariant_monitor.evaluate_all_invariants()
    assert inv_eval["total_invariants"] >= 6
    assert inv_eval["compliance_pct"] == 100.0
    assert inv_eval["violated_count"] == 0


# --- 8. Production Readiness Tests ---

def test_production_readiness_evaluation():
    report = production_readiness_engine.evaluate_readiness()
    assert report.composite_readiness_score >= 95.0
    assert report.is_launch_certified is True
    assert len(report.pillars) == 9
    assert report.readiness_grade == "GRADE_A_ENTERPRISE"


# --- 9. Time Machine Tests ---

def test_time_machine_timeline_and_rewind():
    timeline = time_travel_engine.get_mission_timeline("mission-fin-audit-001")
    assert len(timeline) >= 4

    # Rewind
    rewind_res = time_travel_engine.rewind_to_checkpoint("mission-fin-audit-001", "chk-02")
    assert rewind_res["status"] == "RESTORED_SUCCESSFULLY"
    assert rewind_res["step_index"] == 1

    # Fork
    fork_res = time_travel_engine.fork_mission_from_checkpoint("mission-fin-audit-001", "chk-02")
    assert fork_res.forked_mission_id.startswith("mission-fork-")


# --- 10. Stress Arena Tests ---

def test_stress_arena_execution():
    run = stress_arena_engine.run_stress_test(concurrency=20, total_missions=50)
    assert run.completed_missions == 50
    assert run.throughput_rps > 0.0
    assert run.p95_latency_ms > 0.0
    assert run.invariants_passed_pct == 100.0


# --- 11. Certification Dossier Tests ---

def test_certification_dossier_generation():
    dossier = certification_dossier_engine.generate_dossier()
    assert dossier.dossier_id.startswith("DOSSIER-HA-")
    assert len(dossier.cryptographic_signature) == 64  # SHA-256 length
    assert dossier.composite_reliability_score >= 95.0
    assert dossier.invariants_compliance_pct == 100.0


# --- 12. REST API Integration Tests ---

def test_api_digital_twin_endpoints(client):
    res = client.get("/api/v1/resilience/digital-twin/state")
    assert res.status_code == 200
    assert "nodes" in res.json()

    res_hb = client.post("/api/v1/resilience/digital-twin/heartbeat", json={
        "node_id": "node-workers",
        "latency_ms": 25.0,
        "error_rate": 0.01,
        "cpu_usage_pct": 30.0,
    })
    assert res_hb.status_code == 200


def test_api_chaos_endpoints(client):
    res_list = client.get("/api/v1/resilience/chaos/scenarios")
    assert res_list.status_code == 200

    res_inj = client.post("/api/v1/resilience/chaos/inject", json={"scenario_id": "chaos-redis-drop"})
    assert res_inj.status_code == 200
    assert res_inj.json()["status"] == "ACTIVE"

    res_rec = client.post("/api/v1/resilience/chaos/recover", json={"scenario_id": "chaos-redis-drop"})
    assert res_rec.status_code == 200
    assert res_rec.json()["status"] == "HEALED"


def test_api_recovery_endpoints(client):
    res = client.get("/api/v1/resilience/recovery/marketplace")
    assert res.status_code == 200

    res_exec = client.post("/api/v1/resilience/recovery/execute", json={"strategy_id": "strat-redis-inmemory-cache"})
    assert res_exec.status_code == 200
    assert res_exec.json()["status"] == "SUCCESS"


def test_api_incident_endpoints(client):
    res_dec = client.post("/api/v1/resilience/incident/declare", json={
        "title": "API Gateway Flapping",
        "severity": "SEV3_MEDIUM",
        "root_cause_node_id": "node-gemini",
    })
    assert res_dec.status_code == 200
    inc_id = res_dec.json()["incident"]["incident_id"]

    res_mit = client.post("/api/v1/resilience/incident/mitigate", json={"incident_id": inc_id})
    assert res_mit.status_code == 200
    assert res_mit.json()["status"] == "RESOLVED"


def test_api_dependency_endpoints(client):
    res = client.get("/api/v1/resilience/dependency/topology")
    assert res.status_code == 200
    res_br = client.get("/api/v1/resilience/dependency/blast-radius")
    assert res_br.status_code == 200


def test_api_reliability_and_invariants(client):
    res_rel = client.get("/api/v1/resilience/reliability/mathematics")
    assert res_rel.status_code == 200
    assert res_rel.json()["composite_reliability_score"] >= 95.0

    res_inv = client.get("/api/v1/resilience/invariants/matrix")
    assert res_inv.status_code == 200
    assert res_inv.json()["compliance_pct"] == 100.0


def test_api_production_readiness_and_dossier(client):
    res_prod = client.get("/api/v1/resilience/production-readiness")
    assert res_prod.status_code == 200
    assert res_prod.json()["is_launch_certified"] is True

    res_cert = client.post("/api/v1/resilience/certification/generate")
    assert res_cert.status_code == 200
    assert "cryptographic_signature" in res_cert.json()["dossier"]


def test_api_time_machine_and_stress(client):
    res_tm = client.get("/api/v1/resilience/time-machine/timeline?mission_id=mission-fin-audit-001")
    assert res_tm.status_code == 200

    res_rewind = client.post("/api/v1/resilience/time-machine/rewind", json={
        "mission_id": "mission-fin-audit-001",
        "checkpoint_id": "chk-03",
    })
    assert res_rewind.status_code == 200

    res_stress = client.post("/api/v1/resilience/stress/run", json={"concurrency": 15, "total_missions": 40})
    assert res_stress.status_code == 200
    assert res_stress.json()["run"]["completed_missions"] == 40
