"""
Comprehensive Test Suite for Phase 13.16:
Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP).
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.runtime.world_model.events.world_model_events import (
    ObservationSource,
    ObservationQuality,
    WorldModelEventType,
    WorldModelEvent,
    world_model_event_bus,
)
from app.runtime.world_model.observation.observation_engine import observation_engine
from app.runtime.world_model.knowledge.knowledge_fusion_engine import knowledge_fusion_engine
from app.runtime.world_model.world.world_engine import (
    WorldEntityNode,
    WorldGraphEdge,
    world_engine,
)
from app.runtime.world_model.temporal.temporal_engine import temporal_engine
from app.runtime.world_model.causal.causal_engine import causal_engine
from app.runtime.world_model.hypothesis.hypothesis_engine import hypothesis_engine
from app.runtime.world_model.scenario.scenario_engine import scenario_engine
from app.runtime.world_model.counterfactual.counterfactual_engine import counterfactual_engine
from app.runtime.world_model.forecasting.predictive_engine import predictive_engine
from app.runtime.world_model.decision.decision_engine import decision_engine
from app.runtime.world_model.uncertainty.uncertainty_engine import uncertainty_engine
from app.runtime.world_model.verification.prediction_verification_engine import prediction_verification_engine
from app.runtime.world_model.memory.memory_consolidation_engine import memory_consolidation_engine
from app.runtime.world_model.runtime.world_runtime import world_runtime


@pytest.fixture
def client():
    return TestClient(app)


def test_observation_subsystem():
    obs = observation_engine.observe_metric(
        source=ObservationSource.EXECUTION_RUNTIME,
        entity_id="test_cluster_node",
        metric_name="cpu_usage_pct",
        metric_value=45.2,
        metadata={"region": "us-east-1"},
    )
    assert obs.observation_id.startswith("obs_") or len(obs.observation_id) > 0
    assert obs.signal_to_noise_ratio > 0.0
    assert 0.0 <= obs.novelty_score <= 1.0

    summary = observation_engine.get_summary()
    assert summary["total_observations"] >= 1
    assert "average_snr_db" in summary


def test_knowledge_fusion_subsystem():
    fact = knowledge_fusion_engine.integrate_fact(
        subject="ClusterAlpha",
        predicate="hasAverageLatency",
        object_value=18.5,
        source_runtime="telemetry_engine",
        confidence=0.94,
    )
    assert fact.fact_id.startswith("fact_")
    assert fact.truth_rank >= 0.9
    assert fact.compute_freshness_score() > 0.9

    summary = knowledge_fusion_engine.get_knowledge_summary()
    assert summary["total_facts"] >= 1
    assert summary["average_freshness_score"] > 0.0


def test_world_graph_subsystem():
    node = world_engine.add_node(
        WorldEntityNode(
            entity_id="service_doc_parser",
            name="Document Parser Service",
            category="service",
            properties={"runtime": "python3.11", "replicas": 4},
            state="healthy",
            health_score=0.99,
        )
    )
    assert node.entity_id == "service_doc_parser"

    edge = world_engine.add_edge(
        WorldGraphEdge(
            source_entity_id="service_doc_parser",
            target_entity_id="k8s_prod_cluster",
            relation_type="hosted_on",
            weight=1.0,
            confidence=0.99,
        )
    )
    assert edge.edge_id.startswith("edge_")

    chk = world_engine.create_checkpoint()
    assert chk.snapshot_id.startswith("snap_")
    assert len(chk.state_signature_sha256) == 64  # SHA-256

    graph = world_engine.get_graph()
    assert "nodes" in graph
    assert "edges" in graph
    assert graph["graph_entropy"] >= 0.0


def test_temporal_reasoning_subsystem():
    patterns = temporal_engine.list_patterns()
    assert len(patterns) >= 1
    p = patterns[0]
    assert p.pattern_id.startswith("pat_")
    assert p.confidence > 0.8
    assert p.period_hours > 0.0

    summary = temporal_engine.get_summary()
    assert summary["total_patterns"] >= 1


def test_causal_reasoning_subsystem():
    edges = causal_engine.list_causal_edges()
    assert len(edges) >= 1

    intervention = causal_engine.simulate_do_intervention(
        target_variable="k8s_replicas_count",
        intervention_value=8,
    )
    assert intervention.intervention_id.startswith("do_")
    assert "observed_effects" in intervention.to_dict()
    assert intervention.confidence > 0.8


def test_hypothesis_subsystem():
    hyp = hypothesis_engine.create_hypothesis(
        title="High batch concurrency elevates queue wait times",
        explanation="Increasing document concurrency past 20 saturates parser threadpools.",
        phenomenon_observed="P99 latency increases non-linearly above 20 concurrency.",
        prior_probability=0.7,
    )
    assert hyp.hypothesis_id.startswith("hyp_")
    assert hyp.posterior_probability >= hyp.prior_probability

    hyps = hypothesis_engine.list_hypotheses()
    assert len(hyps) >= 1


def test_scenario_simulation_subsystem():
    scens = scenario_engine.generate_scenarios_for_context("Q4 Document Ingestion Surge")
    assert len(scens) >= 3
    types = {s.scenario_type for s in scens}
    assert "best_case" in types
    assert "worst_case" in types
    assert "expected_case" in types


def test_counterfactual_subsystem():
    exp = counterfactual_engine.run_counterfactual_query(
        title="What if parser caching was enabled during burst?",
        intervention="Enable LRU Cache for parsed OCR schemas",
        target_entity="service_doc_parser",
        actual_metrics={"p99_latency_ms": 65.0, "cache_hit_rate": 0.0},
    )
    assert exp.experiment_id.startswith("cf_")
    assert exp.divergence_metric > 0.0
    assert len(exp.insights) > 0


def test_predictive_forecasting_subsystem():
    pred = predictive_engine.generate_prediction(
        target_metric="document_ingestion_throughput_rps",
        predicted_value=520.0,
        horizon_hours=12.0,
        uncertainty_band=0.08,
    )
    assert pred.prediction_id.startswith("pred_")
    assert pred.confidence_interval_lower < pred.predicted_value < pred.confidence_interval_upper

    preds = predictive_engine.list_predictions()
    assert len(preds) >= 1


def test_decision_intelligence_subsystem():
    decs = decision_engine.evaluate_decision_portfolio("Maximize batch throughput while maintaining P99 latency < 50ms")
    assert len(decs) >= 1
    top = decs[0]
    assert top.decision_id.startswith("dec_")
    assert top.expected_utility > 0.0
    assert top.expected_roi_multiplier > 0.0


def test_uncertainty_quantification_subsystem():
    prof = uncertainty_engine.compute_uncertainty("batch_ocr_pipeline", observation_count=50, variance=0.08)
    assert prof.profile_id.startswith("unc_")
    assert prof.total_entropy > 0.0
    assert prof.belief_stability_index > 0.0


def test_prediction_verification_subsystem():
    pred = predictive_engine.generate_prediction("error_rate_pct", 0.02, 2.0)
    ver = prediction_verification_engine.record_ground_truth(pred.prediction_id, 0.021)
    assert ver.verification_id.startswith("ver_")
    assert ver.passed_tolerance is True
    assert ver.brier_score >= 0.0

    cal = prediction_verification_engine.get_calibration_summary()
    assert "accuracy_pct" in cal
    assert "mean_brier_score" in cal


def test_memory_consolidation_subsystem():
    mem = memory_consolidation_engine.consolidate_memory(
        tier="long_term",
        title="Optimal OCR Batch Sizing Rule",
        summary="Batch sizes between 8 and 16 maximize GPU tensor core utilization.",
        key_facts=["GPU memory optimal at 12 docs", "Latency sub-linear up to 16 docs"],
    )
    assert mem.memory_id.startswith("mem_")
    assert mem.compute_retention_probability() > 0.9

    mems = memory_consolidation_engine.list_memories()
    assert len(mems) >= 1


def test_world_runtime_full_cognitive_cycle():
    res = world_runtime.execute_cognitive_learning_cycle("Optimize OCR cluster capacity for nightly financial batch")
    assert "cycle_id" in res
    assert "observation_id" in res
    assert "fact_id" in res
    assert "checkpoint_id" in res
    assert "hypothesis_id" in res
    assert "prediction_id" in res
    assert "counterfactual_id" in res
    assert "top_recommended_decision" in res
    assert "uncertainty_entropy" in res

    overview = world_runtime.get_world_overview()
    assert overview["system_status"] == "OPERATIONAL"
    assert overview["total_nodes"] >= 1
    assert overview["total_facts"] >= 1


# FastAPI REST API Endpoints Integration Test
def test_world_model_rest_api_endpoints(client: TestClient):
    # 1. Status Overview
    res = client.get("/api/v1/world_model/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert data["phase"] == "13.16"
    assert "summary" in data

    # 2. Trigger Cognitive Cycle
    res_cyc = client.post("/api/v1/world_model/cycle", json={"goal": "API Integration Verification Cycle"})
    assert res_cyc.status_code == 200
    assert res_cyc.json()["success"] is True
    assert "cycle" in res_cyc.json()

    # 3. Observations
    res_obs = client.post(
        "/api/v1/world_model/observations",
        json={
            "source": "execution_runtime",
            "entity_id": "api_test_service",
            "metric_name": "p99_latency_ms",
            "metric_value": 35.4,
        },
    )
    assert res_obs.status_code == 200
    assert res_obs.json()["success"] is True

    res_list_obs = client.get("/api/v1/world_model/observations?limit=10")
    assert res_list_obs.status_code == 200
    assert res_list_obs.json()["count"] >= 1

    # 4. Knowledge Facts
    res_fact = client.post(
        "/api/v1/world_model/knowledge/facts",
        json={
            "subject": "APITestService",
            "predicate": "hasState",
            "object_value": "optimal",
            "source_runtime": "api_test",
        },
    )
    assert res_fact.status_code == 200
    assert res_fact.json()["success"] is True

    res_list_facts = client.get("/api/v1/world_model/knowledge/facts")
    assert res_list_facts.status_code == 200

    # 5. World Graph
    res_ent = client.post(
        "/api/v1/world_model/world/entities",
        json={
            "entity_id": "ent_api_test",
            "name": "API Test Entity",
            "category": "service",
            "health_score": 0.99,
        },
    )
    assert res_ent.status_code == 200

    res_rel = client.post(
        "/api/v1/world_model/world/relations",
        json={
            "source_entity_id": "ent_api_test",
            "target_entity_id": "k8s_prod_cluster",
            "relation_type": "hosted_on",
            "weight": 1.0,
        },
    )
    assert res_rel.status_code == 200

    res_graph = client.get("/api/v1/world_model/world/graph")
    assert res_graph.status_code == 200

    res_snap = client.post("/api/v1/world_model/world/snapshots")
    assert res_snap.status_code == 200

    # 6. Temporal Patterns
    res_tmp = client.get("/api/v1/world_model/temporal/patterns")
    assert res_tmp.status_code == 200

    # 7. Causal Reasoning & Intervention
    res_causal = client.get("/api/v1/world_model/causal/graph")
    assert res_causal.status_code == 200

    res_intv = client.post(
        "/api/v1/world_model/causal/intervene",
        json={"target_variable": "k8s_replicas_count", "intervention_value": 4},
    )
    assert res_intv.status_code == 200

    # 8. Hypotheses
    res_hyp = client.post(
        "/api/v1/world_model/hypotheses",
        json={
            "title": "API Test Hypothesis",
            "explanation": "Scaling reduces queue depth.",
            "phenomenon_observed": "Latency drops when pods increase.",
            "prior_probability": 0.8,
        },
    )
    assert res_hyp.status_code == 200

    res_list_hyps = client.get("/api/v1/world_model/hypotheses")
    assert res_list_hyps.status_code == 200

    # 9. Scenarios
    res_scen = client.post("/api/v1/world_model/scenarios/simulate", json={"context": "API Verification"})
    assert res_scen.status_code == 200

    res_list_scen = client.get("/api/v1/world_model/scenarios")
    assert res_list_scen.status_code == 200

    # 10. Counterfactuals
    res_cf = client.post(
        "/api/v1/world_model/counterfactuals/simulate",
        json={
            "title": "What if API rate limit was doubled?",
            "intervention": "Set rate_limit = 2000",
            "target_entity": "service_core_api",
            "actual_metrics": {"throughput_rps": 450.0},
        },
    )
    assert res_cf.status_code == 200

    res_list_cf = client.get("/api/v1/world_model/counterfactuals")
    assert res_list_cf.status_code == 200

    # 11. Forecasts
    res_fc = client.post(
        "/api/v1/world_model/forecasts/generate",
        json={
            "target_metric": "api_latency_ms",
            "predicted_value": 40.0,
            "horizon_hours": 24.0,
            "uncertainty_band": 0.05,
        },
    )
    assert res_fc.status_code == 200
    pred_id = res_fc.json()["prediction"]["prediction_id"]

    res_list_fc = client.get("/api/v1/world_model/forecasts")
    assert res_list_fc.status_code == 200

    # 12. Decisions
    res_dec = client.post("/api/v1/world_model/decisions/evaluate", json={"goal_context": "API Verification"})
    assert res_dec.status_code == 200

    res_list_dec = client.get("/api/v1/world_model/decisions/portfolios")
    assert res_list_dec.status_code == 200

    # 13. Uncertainty
    res_unc = client.post(
        "/api/v1/world_model/uncertainty/compute",
        json={"domain": "api_testing", "observation_count": 25, "variance": 0.05},
    )
    assert res_unc.status_code == 200

    res_list_unc = client.get("/api/v1/world_model/uncertainty")
    assert res_list_unc.status_code == 200

    # 14. Verification & Calibration
    res_ver = client.post(
        "/api/v1/world_model/verifications/record",
        json={"prediction_id": pred_id, "actual_value": 39.8},
    )
    assert res_ver.status_code == 200

    res_list_ver = client.get("/api/v1/world_model/verifications")
    assert res_list_ver.status_code == 200

    # 15. Memory Records
    res_mem = client.get("/api/v1/world_model/memory/records")
    assert res_mem.status_code == 200

    # 16. Events Stream
    res_ev = client.get("/api/v1/world_model/events?limit=50")
    assert res_ev.status_code == 200
    assert res_ev.json()["count"] >= 1
