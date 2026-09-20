"""
AWM-PSDTIP Phase 13.10 - Comprehensive Pytest Test Suite
Verifies all 12 core subsystems:
1. World State Modeling Engine & State Snapshots
2. Enterprise Digital Twin & Synchronization Fidelity
3. Predictive Simulation Engine & 95% Confidence Intervals
4. Counterfactual Reasoning Engine ("What-If" Interventions)
5. Causal Reasoning Engine & do-calculus Interventions
6. Bayesian Belief Engine & Evidence Accumulation
7. Multi-Horizon Probabilistic Forecasting
8. Risk Prediction Engine & Composite Scorecards
9. Opportunity Discovery Engine & Synergies
10. Temporal Knowledge Graph & Future Projections
11. Predictive Planning Engine & Monte Carlo Candidate Selection
12. Predictive Governance, Rollback & REST API Endpoints
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.runtime.world import (
    get_world_runtime,
    WorldModelEngine,
    DigitalTwinEngine,
    PredictiveSimulationEngine,
    CounterfactualEngine,
    CausalReasoningEngine,
    CausalRelationType,
    BayesianBeliefEngine,
    ForecastingEngine,
    HorizonScope,
    RiskPredictionEngine,
    RiskLevel,
    OpportunityDiscoveryEngine,
    TemporalKnowledgeGraph,
    PredictivePlanningEngine,
    PredictiveGovernanceEngine,
    ScenarioType,
    SimulationMode,
)


@pytest.fixture
def client():
    return TestClient(app)


def test_world_model_synchronization_and_snapshots():
    """Verify entity state management, snapshot creation, and historical time-travel."""
    engine = WorldModelEngine()

    # Update entity
    entity = engine.update_entity(
        entity_id="test-agent-99",
        entity_type="AGENT",
        name="Test Worker Agent",
        attributes={"concurrency": 4, "qps": 20},
        health_score=0.99,
        status="ACTIVE",
    )
    assert entity.entity_id == "test-agent-99"
    assert entity.health_score == 0.99

    # Fetch entity
    fetched = engine.get_entity("test-agent-99")
    assert fetched is not None
    assert fetched.name == "Test Worker Agent"

    # Create snapshot
    snapshot = engine.create_snapshot()
    assert snapshot.snapshot_id.startswith("wss-")
    assert snapshot.state_sha256_hash != ""
    assert snapshot.sequence_number >= 1

    # Time travel query
    time_traveled = engine.time_travel_query(snapshot.snapshot_id)
    assert time_traveled is not None
    assert time_traveled.snapshot_id == snapshot.snapshot_id

    # Summary
    summary = engine.get_current_state_summary()
    assert summary["total_entities"] >= 4
    assert summary["total_snapshots"] >= 2


def test_digital_twin_mirror_fidelity():
    """Verify digital twin synchronization and zero-divergence fidelity."""
    world_model = WorldModelEngine()
    engine = DigitalTwinEngine(world_model)

    twin = engine.synchronize_twin()
    assert twin.twin_id.startswith("dtwin-")
    assert twin.fidelity_score >= 0.99
    assert twin.sync_latency_ms < 50.0
    assert len(twin.mirrored_subsystems) >= 5
    assert twin.state_fingerprint != ""
    assert twin.active_divergence is False

    latest = engine.get_latest_twin()
    assert latest is not None
    assert latest.twin_id == twin.twin_id

    history = engine.get_sync_history()
    assert len(history) >= 1


def test_predictive_simulation_engine_and_confidence_intervals():
    """Verify scenario generation, simulation execution, and 95% confidence intervals."""
    engine = PredictiveSimulationEngine()

    scenario = engine.create_scenario(
        name="High Volume Financial Ingestion",
        scenario_type=ScenarioType.BURST_TRAFFIC,
        mode=SimulationMode.MONTE_CARLO,
        parameters={"traffic_multiplier": 2.5},
        concurrency=12,
    )
    assert scenario.scenario_id.startswith("scen-")

    result = engine.run_simulation(scenario.scenario_id, trials_count=100)
    assert result.result_id.startswith("sres-")
    assert result.expected_latency_ms > 0
    assert len(result.latency_ci_95) == 2
    assert result.latency_ci_95[0] <= result.expected_latency_ms <= result.latency_ci_95[1]
    assert len(result.cost_ci_95) == 2
    assert result.cost_ci_95[0] <= result.expected_cost_usd <= result.cost_ci_95[1]
    assert result.simulation_fingerprint != ""


def test_counterfactual_reasoning_what_if():
    """Verify counterfactual hypothesis evaluation without live disruption."""
    engine = CounterfactualEngine()

    outcome = engine.evaluate_what_if(
        premise="What if worker concurrency is scaled up to 32 agents?",
        altered_variables={"swarm_size": 32, "cache_enabled": True},
        target_objectives=["LATENCY", "COST", "SAFETY"],
    )

    assert outcome.outcome_id.startswith("cfo-")
    assert outcome.predicted_latency_delta_pct < 0  # Speedup
    assert outcome.confidence_score > 0.90
    assert len(outcome.alternative_dag_path) > 0
    assert outcome.evaluation_hash != ""


def test_causal_reasoning_graph_and_interventions():
    """Verify structural causal model creation, causal link evaluation, and interventions."""
    engine = CausalReasoningEngine()

    # Add custom causal link
    v1 = engine.add_variable("OCR_BATCH_SIZE", "SCHEDULER", "Number of pages batched per task", baseline_value=8.0)
    v2 = engine.add_variable("GPU_MEMORY_USAGE", "RESOURCE", "VRAM consumed in MB", baseline_value=2048.0)

    edge = engine.link_causality(v1.node_id, v2.node_id, CausalRelationType.DIRECT_CAUSE, 120.0, confidence=0.99)
    assert edge.edge_id.startswith("cedge-")
    assert edge.empirical_proof != ""

    # Simulate intervention: do(OCR_BATCH_SIZE = 16.0)
    intervention = engine.simulate_intervention("OCR_BATCH_SIZE", 16.0)
    assert "intervention" in intervention
    assert len(intervention["downstream_impacts"]) >= 1
    impact = intervention["downstream_impacts"][0]
    assert impact["target_variable"] == "GPU_MEMORY_USAGE"
    assert impact["predicted_delta"] == (16.0 - 8.0) * 120.0


def test_bayesian_belief_engine_and_evidence_accumulation():
    """Verify prior, likelihood, and posterior probability updates under Bayes theorem."""
    engine = BayesianBeliefEngine()

    belief = engine.register_belief(
        hypothesis="P(Zero Fault Invariant | Chaos Fault Injection) >= 0.99",
        domain="RELIABILITY",
        initial_prior=0.90,
    )
    assert belief.belief_id.startswith("bel-")
    assert belief.posterior_probability == 0.90

    # Accumulate positive evidence
    updated = engine.update_belief_with_evidence(
        belief_id=belief.belief_id,
        evidence_source="chaos_drill_001",
        supports_hypothesis=True,
    )
    assert updated.posterior_probability > 0.90
    assert updated.evidence_count == 1
    assert len(updated.confidence_interval) == 2


def test_forecasting_engine_multi_horizon():
    """Verify multi-horizon probabilistic time-series forecasting."""
    engine = ForecastingEngine()

    forecast = engine.generate_forecast(
        target_metric="LATENCY_MS",
        horizon=HorizonScope.LONG_TERM,
        baseline_value=175.0,
        historical_variance=10.0,
    )

    assert forecast.forecast_id.startswith("fcst-")
    assert forecast.horizon == HorizonScope.LONG_TERM
    assert len(forecast.confidence_interval_95) == 2
    assert len(forecast.forecast_points) == 24
    assert forecast.forecast_points[0]["predicted_value"] > 0


def test_risk_prediction_engine_and_deadlocks():
    """Verify operational risk ranking, impact scoring, and composite scorecard."""
    engine = RiskPredictionEngine()

    risk = engine.evaluate_risk(
        risk_type="DEADLOCK_CASCADE",
        severity=RiskLevel.HIGH,
        probability=0.08,
        impact_score=0.85,
        description="High concurrency deadlock on shared lock buffer.",
        affected_components=["LOCK_MANAGER"],
        mitigation="Switch to lock-free atomic CAS instructions.",
    )

    assert risk.risk_id.startswith("risk-")
    assert risk.severity == RiskLevel.HIGH

    scorecard = engine.get_risk_scorecard()
    assert scorecard["total_active_risks"] >= 1
    assert "composite_risk_index" in scorecard
    assert "overall_status" in scorecard


def test_opportunity_discovery_engine():
    """Verify latent capability discovery and workflow reuse recommendations."""
    engine = OpportunityDiscoveryEngine()

    opp = engine.register_opportunity(
        title="Predictive Schema Embedding Cache",
        category="CACHING_OPTIMIZATION",
        description="Pre-populate token embeddings based on scheduled batch ingestion.",
        latency_gain_pct=32.0,
        cost_saving_pct=18.0,
        confidence=0.988,
        directive="Deploy cache warm-up worker 5 minutes before scheduled batch jobs.",
    )

    assert opp.opportunity_id.startswith("opp-")
    assert opp.potential_latency_gain_pct == 32.0

    all_opps = engine.list_opportunities()
    assert len(all_opps) >= 1


def test_temporal_knowledge_graph_traversal():
    """Verify time-aware node insertions, historical point-in-time queries, and future projections."""
    graph = TemporalKnowledgeGraph()

    # Add historical and future projected nodes
    n_past = graph.add_node(
        label="V1 Sequential DAG",
        entity_type="MISSION_STATE",
        valid_from="2026-09-01T00:00:00Z",
        valid_to="2026-09-10T00:00:00Z",
    )
    n_future = graph.add_node(
        label="V3 Autonomous Neural DAG",
        entity_type="PREDICTED_FUTURE",
        valid_from="2026-09-20T00:00:00Z",
        is_projected_future=True,
    )

    graph.add_edge(n_past.node_id, n_future.node_id, "PREDICTS")

    # Point in time query
    active_in_past = graph.query_state_at_time("2026-09-05T00:00:00Z")
    assert any(n.node_id == n_past.node_id for n in active_in_past)

    projections = graph.get_future_projections()
    assert len(projections) >= 1
    assert any(p.node_id == n_future.node_id for p in projections)


def test_predictive_planning_monte_carlo():
    """Verify Monte Carlo plan evaluation and Pareto optimality selection."""
    engine = PredictivePlanningEngine()

    candidates = engine.evaluate_candidate_plans("Process 1000 High-Volume Legal Dossiers", sample_trials=500)
    assert len(candidates) == 3

    selected = next(c for c in candidates if c.is_selected)
    assert selected.pareto_optimality_score >= 0.95
    assert selected.predicted_success_rate >= 0.99
    assert selected.plan_signature != ""


def test_predictive_governance_and_rest_endpoints(client):
    """Verify cryptographic governance authorizations, rollbacks, and all REST endpoints."""
    runtime = get_world_runtime()
    overview = runtime.get_world_overview()
    assert overview["status"] == "WORLD_MODEL_ACTIVE"

    # Test GET /api/v1/world/overview
    resp = client.get("/api/v1/world/overview")
    assert resp.status_code == 200
    assert resp.json()["status"] == "WORLD_MODEL_ACTIVE"

    # Test GET /api/v1/world/model
    resp = client.get("/api/v1/world/model")
    assert resp.status_code == 200
    assert "summary" in resp.json()
    assert "entities" in resp.json()

    # Test GET /api/v1/world/digital-twin
    resp = client.get("/api/v1/world/digital-twin")
    assert resp.status_code == 200
    assert "latest_twin" in resp.json()

    # Test GET /api/v1/world/predictions
    resp = client.get("/api/v1/world/predictions")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    # Test POST /api/v1/world/predict
    resp = client.post("/api/v1/world/predict", json={
        "mission_goal": "Process 500 Enterprise Invoice Documents",
        "sample_trials": 200,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "PREDICTION_COMPLETED"
    plan_id = resp.json()["selected_plan"]["candidate_id"]

    # Test GET /api/v1/world/simulations
    resp = client.get("/api/v1/world/simulations")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    # Test POST /api/v1/world/simulate
    resp = client.post("/api/v1/world/simulate", json={
        "name": "API Burst Simulation",
        "scenario_type": "BURST_TRAFFIC",
        "mode": "MONTE_CARLO",
        "parameters": {"traffic_multiplier": 2.0},
        "concurrency": 8,
        "trials_count": 50,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "SIMULATION_COMPLETED"

    # Test GET /api/v1/world/counterfactuals
    resp = client.get("/api/v1/world/counterfactuals")
    assert resp.status_code == 200
    assert "outcomes" in resp.json()

    # Test POST /api/v1/world/counterfactual
    resp = client.post("/api/v1/world/counterfactual", json={
        "premise": "What if cache TTL is extended to 1 hour?",
        "altered_variables": {"cache_ttl_sec": 3600},
        "target_objectives": ["LATENCY", "COST"],
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "COUNTERFACTUAL_EVALUATED"

    # Test GET /api/v1/world/forecasts
    resp = client.get("/api/v1/world/forecasts")
    assert resp.status_code == 200

    # Test POST /api/v1/world/forecast
    resp = client.post("/api/v1/world/forecast", json={
        "target_metric": "THROUGHPUT_QPS",
        "horizon": "SHORT_TERM",
        "baseline_value": 45.0,
        "historical_variance": 3.0,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "FORECAST_GENERATED"

    # Test GET /api/v1/world/risks
    resp = client.get("/api/v1/world/risks")
    assert resp.status_code == 200
    assert "scorecard" in resp.json()

    # Test POST /api/v1/world/analyze-risk
    resp = client.post("/api/v1/world/analyze-risk", json={
        "risk_type": "LATENCY_DEGRADATION",
        "severity": "LOW",
        "probability": 0.05,
        "impact_score": 0.25,
        "description": "Minor serialization on large batches",
        "affected_components": ["DAG_SCHEDULER"],
        "mitigation": "Increase pre-fetch queue depth",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "RISK_RECORDED"

    # Test GET /api/v1/world/opportunities
    resp = client.get("/api/v1/world/opportunities")
    assert resp.status_code == 200

    # Test POST /api/v1/world/discover-opportunities
    resp = client.post("/api/v1/world/discover-opportunities", json={
        "title": "Batch Vector Search Parallelism",
        "category": "COST_REDUCTION",
        "description": "Parallelize embedding similarity searches across worker cores",
        "latency_gain_pct": 24.0,
        "cost_saving_pct": 14.0,
        "confidence": 0.99,
        "directive": "Enable multi-threaded vector indexing",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "OPPORTUNITY_REGISTERED"

    # Test GET /api/v1/world/causal-graph
    resp = client.get("/api/v1/world/causal-graph")
    assert resp.status_code == 200
    assert "total_nodes" in resp.json()

    # Test GET /api/v1/world/beliefs
    resp = client.get("/api/v1/world/beliefs")
    assert resp.status_code == 200

    # Test GET /api/v1/world/temporal-graph
    resp = client.get("/api/v1/world/temporal-graph")
    assert resp.status_code == 200

    # Test POST /api/v1/world/approve
    resp = client.post("/api/v1/world/approve", json={
        "target_prediction_id": plan_id,
        "target_type": "PLAN_EXECUTION",
        "approver_role": "EXECUTIVE_DIRECTOR",
        "decision": "APPROVED",
        "rationale": "Empirically validated via Monte Carlo simulation with 99.9% success rate.",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "APPROVED"

    # Test POST /api/v1/world/rollback
    resp = client.post("/api/v1/world/rollback", json={
        "target_id": plan_id,
        "reason": "Test rollback API endpoint",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ROLLED_BACK"
