"""
AMRS-RSIP Phase 13.9 - Comprehensive Pytest Test Suite
Verifies all 10 core subsystems:
1. Strategic Observation Layer & Evidence Graph
2. Meta-Reasoning Engine & Strategic Bottleneck Detection
3. Recursive Multi-Tier Reflection Engine (7 Tiers)
4. Strategic Planner & Long-Horizon Roadmap Formulation
5. Replay-Based Autonomous Experimentation Engine
6. Capability Synthesis & Dynamic Tool Discovery
7. Autonomous Policy Evolution Engine
8. Continuous Architectural Optimizer & Pipeline Refactoring
9. Closed-Loop Recursive Self-Improvement Coordinator
10. Cryptographic Strategic Governance, Safety Guardrails & REST APIs
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.runtime.meta import (
    get_meta_runtime,
    StrategicObservationLayer,
    StrategicEvidenceNode,
    StrategicEvidenceEdge,
    MetaReasoningEngine,
    RecursiveReflectionEngine,
    ReflectionTier,
    StrategicPlanner,
    AutonomousExperimentationEngine,
    CapabilityDiscoveryEngine,
    PolicyEvolutionEngine,
    ArchitectureOptimizer,
    RecursiveSelfImprovementEngine,
    StrategicGovernanceEngine,
    ImprovementStatus,
)


@pytest.fixture
def client():
    return TestClient(app)


def test_strategic_observation_layer():
    """Verify strategic observation ingestion, graph updates, and anomaly detection."""
    obs = StrategicObservationLayer()

    # Record telemetry observations
    obs_record = obs.record_observation(
        observation_type="LATENCY_SPIKE",
        target_subsystem="OCR_WORKER_POOL",
        metric_name="task_queue_wait_ms",
        observed_value=350.0,
        baseline_value=120.0,
        metadata={"cause": "Heavy 50-page PDF table density"},
    )
    assert obs_record["observation_id"].startswith("obs-")
    assert obs_record["deviation_pct"] > 0

    recent = obs.get_recent_observations()
    assert len(recent) >= 1

    anomalies = obs.detect_systemic_anomalies()
    assert len(anomalies) >= 1

    summary = obs.evidence_graph.get_summary()
    assert summary["total_nodes"] >= 3
    assert summary["total_edges"] >= 2

    # Query neighbors
    neighbors = obs.evidence_graph.get_neighbors("obs_node_planner")
    assert len(neighbors) >= 1


def test_meta_reasoning_engine():
    """Verify bottleneck detection, counterfactual synthesis, and reasoning graph creation."""
    engine = MetaReasoningEngine()
    
    graph = engine.analyze_goal_and_synthesize(
        goal_description="Process 1000 High-Complexity Invoices with Zero Error and Under 25s Latency",
        execution_context={"historical_success_rate": 0.992},
    )

    assert graph.graph_id.startswith("mrg-")
    assert len(graph.identified_bottlenecks) >= 1
    assert len(graph.proposed_alternatives) >= 1
    assert graph.reasoning_confidence > 0.90
    assert graph.graph_signature != ""

    all_graphs = engine.get_all_reasoning_graphs()
    assert len(all_graphs) >= 1

    bottlenecks = engine.get_bottlenecks()
    assert len(bottlenecks) >= 1


def test_recursive_reflection_engine():
    """Verify 7-tier recursive reflection generation and Merkle root calculation."""
    engine = RecursiveReflectionEngine()

    tree = engine.execute_recursive_reflection(
        subject="ENTERPRISE_MISSION_AND_SWARM_OPERATIONS",
        max_depth=7,
    )

    assert tree.tree_id.startswith("rrt-")
    assert len(tree.nodes) == 7
    assert tree.merkle_tree_hash != ""

    # Verify all 7 tiers are represented
    tiers_present = {node.tier for node in tree.nodes.values()}
    assert ReflectionTier.LEVEL_1_MISSION in tiers_present
    assert ReflectionTier.LEVEL_2_PLANNER in tiers_present
    assert ReflectionTier.LEVEL_3_SWARM in tiers_present
    assert ReflectionTier.LEVEL_4_LEARNING in tiers_present
    assert ReflectionTier.LEVEL_5_ARCHITECTURE in tiers_present
    assert ReflectionTier.LEVEL_6_POLICY in tiers_present
    assert ReflectionTier.LEVEL_7_SELF in tiers_present

    all_trees = engine.get_all_trees()
    assert len(all_trees) >= 1


def test_strategic_planner():
    """Verify long-horizon roadmap generation, milestones, and Pareto front matrix."""
    planner = StrategicPlanner()

    roadmap = planner.generate_strategic_roadmap(
        title="Autonomous Sub-200ms Platform Optimization Roadmap",
        horizon_scope="MULTI_WEEK",
        primary_goal="Maximize Document Throughput and Guarantee Mathematical Invariants",
    )

    assert roadmap.roadmap_id.startswith("rdm-")
    assert len(roadmap.milestones) == 3
    assert roadmap.strategy_matrix["optimal_strategy"] != ""
    assert roadmap.roadmap_signature != ""

    all_roadmaps = planner.get_all_roadmaps()
    assert len(all_roadmaps) >= 1


def test_experimentation_engine():
    """Verify A/B replay experiment formulation, trials execution, and statistical validation."""
    engine = AutonomousExperimentationEngine()

    res = engine.run_replay_ab_test(
        name="Dynamic DAG Fan-Out vs Sequential Baseline",
        control_strategy="GREEDY_SEQUENTIAL_DAG",
        treatment_strategy="DYNAMIC_FANOUT_DAG",
        historical_sample_size=80,
        control_latency=400.0,
        treatment_latency=220.0,
        control_cost=0.05,
        treatment_cost=0.035,
    )

    assert res.experiment_id.startswith("exp-")
    assert res.is_significant is True
    assert res.p_value < 0.05
    assert res.performance_gain_pct == 45.0
    assert res.winning_strategy == "DYNAMIC_FANOUT_DAG"

    all_exps = engine.get_all_experiments()
    assert len(all_exps) >= 1


def test_capability_discovery_engine():
    """Verify capability gap detection and dynamic tool synthesis."""
    engine = CapabilityDiscoveryEngine()

    cap = engine.synthesize_capability(
        name="HighDensityTableReconciler",
        category="WORKFLOW_TEMPLATE",
        description="Autonomous sub-DAG template for merging multi-page balance sheets.",
        synthesized_from=["vision_transformer", "sha256_verifier", "matrix_splitter"],
        reusability_score=0.975,
    )

    assert cap.capability_id.startswith("cap-")
    assert cap.name == "HighDensityTableReconciler"
    assert cap.reusability_score == 0.975

    all_caps = engine.get_all_capabilities()
    assert len(all_caps) >= 1


def test_policy_evolution_engine():
    """Verify policy proposal creation, SHA-256 hash generation, and lifecycle."""
    engine = PolicyEvolutionEngine()

    proposal = engine.propose_policy_upgrade(
        policy_name="DynamicMemoryConcurrencyQuota",
        category="RESOURCE_ALLOCATION",
        current_rule="Limit worker pool concurrency to 4 simultaneous tasks.",
        proposed_rule="Dynamically scale concurrency up to 16 tasks when memory usage is < 50%.",
        rationale="Eliminates unnecessary queuing during off-peak and high-RAM execution phases.",
        evidence_backing=["obs-latency-spike-ocr", "exp-dynamic-fanout"],
        predicted_impact={"latency_reduction_pct": 35.0, "risk_delta": "NEGLIGIBLE"},
    )

    assert proposal.proposal_id.startswith("pol-prop-")
    assert proposal.status == "PENDING_APPROVAL"
    assert proposal.sha256_proposal_hash != ""

    all_props = engine.get_all_proposals()
    assert len(all_props) >= 1


def test_architecture_optimizer():
    """Verify structural architectural optimization proposals and savings estimation."""
    optimizer = ArchitectureOptimizer()

    proposal = optimizer.propose_optimization(
        target_subsystem="EVENT_BUS_AND_DAG_SCHEDULER",
        optimization_type="COMMUNICATION_TOPOLOGY_FLATTENING",
        description="Replace serial point-to-point task routing with pub-sub multi-cast channels.",
        latency_saving_ms=150.0,
        memory_delta_mb=-20.0,
        confidence_score=0.985,
    )

    assert proposal.optimization_id.startswith("arch-opt-")
    assert proposal.estimated_latency_saving_ms == 150.0

    all_opts = optimizer.get_all_proposals()
    assert len(all_opts) >= 1


def test_recursive_self_improvement_engine():
    """Verify closed-loop self-improvement cycle state transitions."""
    engine = RecursiveSelfImprovementEngine()

    cycle = engine.initiate_improvement_cycle(
        target_area="OCR_DAG_PARALLELIZATION",
        reflection_tree_id="rrt-test-01",
        hypothesis="Parallel chunk fan-out in DAG execution reduces latency by >= 35%.",
        experiment_id="exp-test-01",
        proposal_id="pol-prop-test-01",
    )

    assert cycle.cycle_id.startswith("sic-")
    assert cycle.status == ImprovementStatus.IN_EXPERIMENT
    assert cycle.checkpoint_merkle_root != ""

    # Promote
    ok_promote = engine.verify_and_promote_cycle(cycle.cycle_id, measured_gain_pct=42.5)
    assert ok_promote is True
    assert cycle.status == ImprovementStatus.GOVERNANCE_PENDING

    # Approve
    ok_approve = engine.mark_approved(cycle.cycle_id)
    assert ok_approve is True
    assert cycle.status == ImprovementStatus.DEPLOYED
    assert cycle.governance_approved is True

    # Rollback
    ok_rollback = engine.rollback_cycle(cycle.cycle_id, reason="Operator requested verification rollback")
    assert ok_rollback is True
    assert cycle.status == ImprovementStatus.ROLLED_BACK


def test_strategic_governance_engine_and_audit():
    """Verify cryptographic signatures, approval workflow, and audit trails."""
    gov = StrategicGovernanceEngine()

    ok, record, msg = gov.review_and_approve(
        target_proposal_id="pol-prop-test-02",
        proposal_type="POLICY_UPGRADE",
        approver_role="EXECUTIVE_DIRECTOR",
        decision="APPROVED",
        rationale="Empirically verified via replay A/B testing with p < 0.01.",
    )

    assert ok is True
    assert record.approval_id.startswith("appr-")
    assert record.decision == "APPROVED"
    assert record.cryptographic_signature != ""

    approvals = gov.list_approvals()
    assert len(approvals) >= 1

    audit_trail = gov.get_audit_trail()
    assert len(audit_trail) >= 1


def test_meta_runtime_and_rest_endpoints(client):
    """Verify complete MetaRuntime aggregation and all REST API endpoints."""
    runtime = get_meta_runtime()
    overview = runtime.get_meta_overview()
    assert overview["status"] == "META_COGNITION_ACTIVE"
    assert overview["total_reasoning_graphs"] >= 1
    assert overview["active_bottlenecks"] >= 1
    assert overview["reflection_trees"] >= 1

    # Test GET /api/v1/meta/overview
    resp = client.get("/api/v1/meta/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "META_COGNITION_ACTIVE"

    # Test GET /api/v1/meta/reasoning
    resp = client.get("/api/v1/meta/reasoning")
    assert resp.status_code == 200
    res_data = resp.json()
    assert "graphs" in res_data
    assert "bottlenecks" in res_data

    # Test POST /api/v1/meta/reason
    resp = client.post("/api/v1/meta/reason", json={
        "goal_description": "Process 500 Enterprise Financial Reports within 20s SLA",
        "execution_context": {"high_priority": True},
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "REASONING_COMPLETED"

    # Test GET /api/v1/meta/reflections
    resp = client.get("/api/v1/meta/reflections")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

    # Test POST /api/v1/meta/reflect
    resp = client.post("/api/v1/meta/reflect", json={
        "subject": "TEST_SUBJECT",
        "max_depth": 7,
    })
    assert resp.status_code == 200
    refl_res = resp.json()
    assert refl_res["status"] == "REFLECTION_COMPLETED"
    assert len(refl_res["nodes"]) == 7

    # Test GET /api/v1/meta/strategies
    resp = client.get("/api/v1/meta/strategies")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Test GET /api/v1/meta/experiments
    resp = client.get("/api/v1/meta/experiments")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Test POST /api/v1/meta/experiment
    resp = client.post("/api/v1/meta/experiment", json={
        "name": "Speculative Token Cache vs Cold Embedding",
        "control_strategy": "COLD_EMBEDDING",
        "treatment_strategy": "SPECULATIVE_TOKEN_CACHE",
        "historical_sample_size": 60,
        "control_latency": 320.0,
        "treatment_latency": 180.0,
        "control_cost": 0.04,
        "treatment_cost": 0.025,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "EXPERIMENT_CONCLUDED"

    # Test GET /api/v1/meta/capabilities
    resp = client.get("/api/v1/meta/capabilities")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Test GET /api/v1/meta/policies
    resp = client.get("/api/v1/meta/policies")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Test POST /api/v1/meta/evolve-policy
    resp = client.post("/api/v1/meta/evolve-policy", json={
        "policy_name": "Adaptive Batch Sizing",
        "category": "PLANNER_CONCURRENCY",
        "current_rule": "batch_size = 5",
        "proposed_rule": "batch_size = 20",
        "rationale": "High throughput mode for bulk PDF uploads",
        "evidence_backing": ["exp-batch-test"],
        "predicted_impact": {"latency_reduction_pct": 28.0},
    })
    assert resp.status_code == 200
    pol_id = resp.json()["proposal"]["proposal_id"]

    # Test GET /api/v1/meta/architecture
    resp = client.get("/api/v1/meta/architecture")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Test POST /api/v1/meta/propose-architecture
    resp = client.post("/api/v1/meta/propose-architecture", json={
        "target_subsystem": "MEMORY_CACHE",
        "optimization_type": "LOCK_FREE_READ",
        "description": "Lock-free concurrent memory hash table",
        "latency_saving_ms": 75.0,
        "memory_delta_mb": -5.0,
        "confidence_score": 0.99,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "PROPOSED"

    # Test GET /api/v1/meta/self-improvement
    resp = client.get("/api/v1/meta/self-improvement")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
    cycle_id = resp.json()[0]["cycle_id"]

    # Test GET /api/v1/meta/history
    resp = client.get("/api/v1/meta/history")
    assert resp.status_code == 200
    assert "observations" in resp.json()
    assert "governance_audit" in resp.json()

    # Test POST /api/v1/meta/approve
    resp = client.post("/api/v1/meta/approve", json={
        "target_proposal_id": pol_id,
        "proposal_type": "POLICY_UPGRADE",
        "approver_role": "EXECUTIVE_DIRECTOR",
        "decision": "APPROVED",
        "rationale": "Approved after comprehensive empirical verification.",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "APPROVED"

    # Test POST /api/v1/meta/rollback
    resp = client.post("/api/v1/meta/rollback", json={
        "cycle_id": cycle_id,
        "reason": "Test endpoint rollback",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ROLLED_BACK"
