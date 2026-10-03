"""
Comprehensive Pytest Suite for Phase 13.22 Enterprise Cognitive Intelligence & Autonomous Organizational Learning Platform (ECIAOLP)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.platform_cognitive.runtime.cognitive_master_orchestrator import cognitive_orchestrator

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_cognitive():
    tenant = "test-tenant-cog"
    cognitive_orchestrator.graph_engine.seed_default_cognitive_graph(tenant)
    cognitive_orchestrator.goal_alignment.get_alignments(tenant)
    yield

def test_cognitive_graph_and_causal_reasoning():
    tenant = "test-tenant-cog"
    overview = cognitive_orchestrator.graph_engine.get_overview(tenant)
    assert overview["total_nodes"] >= 4
    assert overview["total_edges"] >= 3
    
    start_id = overview["nodes"][0]["id"]
    path = cognitive_orchestrator.graph_engine.query_causal_path(tenant, start_id, max_depth=3)
    assert len(path["nodes"]) >= 1
    assert "root_node_id" in path

def test_cross_agent_experience_memory():
    tenant = "test-tenant-cog"
    entry = cognitive_orchestrator.experience_memory.store_experience(
        tenant_id=tenant,
        task_fingerprint="invoice_ocr_reconciliation_sap",
        agent_id="agent-01",
        input_pattern="vendor invoice PDF exceeding $50k",
        successful_trace=["OCR parsed", "PO validated", "VP threshold verified"],
        metrics={"latency_ms": 142.0, "cost_usd": 0.002, "quality_score": 0.99},
        reusable_knowledge="Always extract VAT code before PO matching"
    )
    assert entry.id is not None
    assert entry.reuse_count == 0
    
    # Query experience
    results = cognitive_orchestrator.experience_memory.query_experience(tenant, "invoice_ocr")
    assert len(results) >= 1
    assert results[0].reuse_count == 1
    assert "Always extract VAT code" in results[0].reusable_knowledge

def test_process_discovery_and_bottlenecks():
    tenant = "test-tenant-cog"
    proc = cognitive_orchestrator.process_discovery.discover_from_logs(tenant, [{"event": "step1"}])
    assert proc.process_name != ""
    assert len(proc.reconstructed_steps) >= 4
    assert len(proc.bottlenecks) >= 1
    assert proc.automation_opportunity_score > 0.8

def test_decision_intelligence_tracking_and_calibration():
    tenant = "test-tenant-cog"
    dec = cognitive_orchestrator.decision_intelligence.record_decision(
        tenant_id=tenant,
        topic="Switch Document OCR to Parallel Engine",
        chosen_action="Deploy Parallel OCR Worker Fleet",
        alternatives=["Keep Sequential", "Increase Timeout"],
        rationale="Parallel processing reduces cycle time by 42%",
        confidence=0.94,
        expected_outcome={"latency_reduction_pct": 40.0}
    )
    assert dec.id is not None
    assert dec.outcome_matched is None
    
    resolved = cognitive_orchestrator.decision_intelligence.resolve_actual_outcome(
        decision_id=dec.id,
        tenant_id=tenant,
        actual_outcome={"latency_reduction_pct": 42.5},
        matched=True
    )
    assert resolved.outcome_matched is True
    assert resolved.resolved_at is not None

def test_hypothesis_generation_and_simulation():
    tenant = "test-tenant-cog"
    hyps = cognitive_orchestrator.hypothesis_engine.generate_hypotheses(tenant)
    assert len(hyps) >= 2
    assert hyps[0].confidence_score > 0.8
    assert hyps[0].suggested_action != ""

    sim = cognitive_orchestrator.simulation_engine.simulate_scenario(
        tenant_id=tenant,
        scenario_name="Switch to Flash OCR",
        overrides={"model": "gemini-1.5-flash"}
    )
    assert sim.projected_latency_change_pct < 0
    assert sim.projected_roi_factor > 1.0

def test_autonomous_optimization_and_goal_alignment():
    tenant = "test-tenant-cog"
    opps = cognitive_orchestrator.optimization_engine.discover_opportunities(tenant)
    assert len(opps) >= 1
    
    applied = cognitive_orchestrator.optimization_engine.apply_optimization(opps[0].id, tenant)
    assert applied["status"] == "APPLIED_SUCCESSFULLY"

    alignments = cognitive_orchestrator.goal_alignment.get_alignments(tenant)
    assert len(alignments) >= 2
    assert "Operating Efficiency" in alignments[0].corporate_kpi

def test_fastapi_cognitive_endpoints():
    tenant = "test-tenant-cog"
    # 1. Executive insights
    resp = client.get(f"/api/v1/cognitive/executive-insights?tenant_id={tenant}")
    assert resp.status_code == 200
    data = resp.json()
    assert "cognitive_health_index" in data
    assert len(data["strategic_recommendations"]) >= 1

    # 2. Recommendations
    resp = client.get(f"/api/v1/cognitive/recommendations?tenant_id={tenant}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    # 3. Learning insights
    resp = client.get(f"/api/v1/cognitive/learning/insights?tenant_id={tenant}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # 4. Simulation endpoint
    sim_payload = {
        "tenant_id": tenant,
        "scenario_name": "Model Switch Simulation",
        "parameter_overrides": {"model": "gemini-1.5-flash"}
    }
    resp = client.post("/api/v1/cognitive/simulate", json=sim_payload)
    assert resp.status_code == 200
    assert resp.json()["projected_roi_factor"] > 0

    # 5. Health
    resp = client.get(f"/api/v1/cognitive/health?tenant_id={tenant}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "OPERATIONAL"
