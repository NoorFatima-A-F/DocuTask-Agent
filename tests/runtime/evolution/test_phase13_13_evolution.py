"""
Comprehensive Unit & Integration Test Suite for Phase 13.13 (ASEAORIP).
Validates Profiler, Diagnostics, Capability, Architecture, Optimizer, Mutations, Benchmarks, Simulation, Governance, Deployment, and closed-loop Evolution Cycles.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.runtime.evolution.events import EvolutionEventBus, OptimizationObjective
from app.runtime.evolution.profiler import ProfilerEngine, PlatformHealthSnapshot
from app.runtime.evolution.diagnostics import DiagnosticEngine
from app.runtime.evolution.capability import CapabilityEngine
from app.runtime.evolution.architecture import ArchitectureEngine
from app.runtime.evolution.optimizer import OptimizerEngine
from app.runtime.evolution.self_modification import MutationEngine
from app.runtime.evolution.benchmark import BenchmarkEngine
from app.runtime.evolution.simulation import SimulationEngine
from app.runtime.evolution.governance import GovernanceEngine
from app.runtime.evolution.deployment import DeploymentEngine
from app.runtime.evolution.runtime import EvolutionRuntime

client = TestClient(app)


# ==========================================
# Unit Tests for Phase 13.13 Subsystems
# ==========================================

def test_profiler_engine():
    event_bus = EvolutionEventBus()
    profiler = ProfilerEngine(event_bus)
    snapshot = profiler.collect_snapshot()
    
    assert snapshot.snapshot_id is not None
    assert 0.0 <= snapshot.composite_health_score <= 1.0
    assert snapshot.cpu_utilization_pct >= 0.0
    assert snapshot.memory_utilization_pct >= 0.0
    assert snapshot.latency_p95_ms > 0.0
    assert len(profiler.list_snapshots()) >= 2


def test_diagnostic_engine():
    event_bus = EvolutionEventBus()
    diagnostic = DiagnosticEngine(event_bus)
    
    mock_snapshot = PlatformHealthSnapshot(
        token_waste_rate=0.08,
        latency_p95_ms=180.0,
    )
    diagnoses = diagnostic.diagnose_weaknesses(mock_snapshot)
    assert len(diagnoses) >= 2
    assert any("Token Waste" in d.title for d in diagnoses)
    assert any("Latency" in d.title for d in diagnoses)


def test_capability_engine():
    event_bus = EvolutionEventBus()
    capability = CapabilityEngine(event_bus)
    
    gaps = capability.discover_capability_gaps()
    assert len(gaps) >= 1
    
    new_cap = capability.register_capability(
        name="Adaptive Zero-Shot OCR Rectifier",
        domain="document_intelligence",
        description="Auto-aligns warped camera scans",
    )
    assert new_cap.name == "Adaptive Zero-Shot OCR Rectifier"
    assert capability.get_capability(new_cap.capability_id) is not None


def test_architecture_engine():
    event_bus = EvolutionEventBus()
    arch = ArchitectureEngine(event_bus)
    topology = arch.get_topology()
    
    assert topology["node_count"] >= 5
    assert topology["edge_count"] >= 5
    assert topology["average_complexity"] > 0.0
    
    plan = arch.generate_improvement_plan(
        title="Decouple Cache Invalidation from Dispatch Bus",
        target_subsystems=["query_cache", "event_bus"],
        action_type="EVENT_ISOLATION",
        rationale="Eliminates lock contention",
    )
    assert plan.plan_id in [p.plan_id for p in arch.list_improvement_plans()]


def test_optimizer_engine_pareto():
    event_bus = EvolutionEventBus()
    optimizer = OptimizerEngine(event_bus)
    
    candidate = optimizer.generate_candidate(
        target_subsystem="llm_cognition",
        objective=OptimizationObjective.TOKEN_EFFICIENCY.value,
        hyperparameters={"compression_level": 3},
    )
    assert candidate.candidate_id is not None
    assert candidate.fitness_score > 0.0
    
    pareto_frontier = optimizer.compute_pareto_frontier()
    assert len(pareto_frontier) >= 1
    for p in pareto_frontier:
        assert p.pareto_rank == 1


def test_mutation_engine_and_diff():
    event_bus = EvolutionEventBus()
    mutation_eng = MutationEngine(event_bus)
    
    proposal = mutation_eng.propose_mutation(
        title="Lock-Free Async Ring Buffer Dispatch",
        mutation_type="ROUTING_REFACTOR",
        target_components=["event_bus"],
        code_diff_spec="--- a/bus.py\n+++ b/bus.py\n-lock.acquire()\n+lock_free_cas()",
        rationale="High concurrency lock elimination",
    )
    assert proposal.mutation_id is not None
    assert proposal.sha256_hash != ""
    assert proposal.status == "PROPOSED"
    
    mutation_eng.update_mutation_status(proposal.mutation_id, "APPROVED")
    assert mutation_eng.get_proposal(proposal.mutation_id).status == "APPROVED"


def test_benchmark_engine():
    event_bus = EvolutionEventBus()
    bench = BenchmarkEngine(event_bus)
    
    comp = bench.run_benchmark(
        baseline_version="v13.12-prod",
        candidate_version="v13.13-eval-test",
        test_case_count=100,
    )
    assert comp.comparison_id is not None
    assert comp.test_cases_run == 100
    assert comp.status in ["PASSED", "FAILED"]


def test_simulation_engine():
    event_bus = EvolutionEventBus()
    sim = SimulationEngine(event_bus)
    
    report = sim.run_simulation(
        simulation_mode="SHADOW_REPLAY",
        traces_count=500,
    )
    assert report.simulation_id is not None
    assert report.traces_replayed == 500
    assert 0.0 <= report.success_rate <= 1.0


def test_governance_engine_and_rollback_snapshot():
    event_bus = EvolutionEventBus()
    gov = GovernanceEngine(event_bus)
    
    snapshot = gov.create_rollback_snapshot(platform_version="v13.12.0")
    assert snapshot.snapshot_id is not None
    assert snapshot.sha256_seal != ""
    
    review = gov.submit_for_review(
        mutation_id="mut_unit_test",
        risk_level="LOW",
    )
    assert review.approval_status == "APPROVED"
    assert review.cryptographic_signature != ""
    
    # High risk review requires override
    high_review = gov.submit_for_review(
        mutation_id="mut_unit_high_risk",
        risk_level="HIGH",
    )
    assert high_review.approval_status == "PENDING"
    assert high_review.human_override_required is True
    
    approved = gov.approve_review(high_review.review_id, reviewer_agent_id="agent_human_lead")
    assert approved.approval_status == "APPROVED"


def test_deployment_engine_progressive_canary():
    event_bus = EvolutionEventBus()
    deploy = DeploymentEngine(event_bus)
    
    record = deploy.launch_deployment(
        mutation_id="mut_deploy_test",
        target_version="v13.13.1",
        initial_traffic_pct=15.0,
    )
    assert record.canary_traffic_pct == 15.0
    assert record.deployment_state == "CANARY"
    
    advanced = deploy.advance_canary(record.deployment_id, 100.0)
    assert advanced.deployment_state == "PROMOTED"
    assert deploy.current_platform_version == "v13.13.1"
    
    # Test rollback
    rolled_back = deploy.trigger_rollback(record.deployment_id, reason="SLA breach")
    assert rolled_back.deployment_state == "ROLLED_BACK"
    assert rolled_back.canary_traffic_pct == 0.0


def test_full_evolution_cycle_runtime():
    runtime = EvolutionRuntime()
    result = runtime.run_full_evolution_cycle(
        target_subsystem="llm_orchestrator",
        objective="LATENCY_REDUCTION",
        auto_deploy=True,
    )
    assert result.cycle_id is not None
    assert result.stage in ["DEPLOYED", "GOVERNANCE_REVIEW"]
    assert result.health_score_after >= result.health_score_before
    assert len(runtime.cycle_history) == 1
    
    summary = runtime.get_executive_summary()
    assert summary["completed_evolution_cycles"] == 1
    assert summary["composite_health_score"] > 0.0


# ==========================================
# REST API Integration Tests for Phase 13.13
# ==========================================

def test_api_executive_summary():
    response = client.get("/api/v1/evolution/executive-summary")
    assert response.status_code == 200
    data = response.json()
    assert "composite_health_score" in data
    assert "platform_version" in data
    assert "active_diagnoses_count" in data


def test_api_genome():
    response = client.get("/api/v1/evolution/genome")
    assert response.status_code == 200
    data = response.json()
    assert data["genome_id"] == "genome_v13_13_prime"
    assert "architecture_nodes" in data
    assert "capabilities" in data


def test_api_evolution_cycle_run():
    response = client.post("/api/v1/evolution/cycle/run", json={
        "target_subsystem": "memory_layer",
        "objective": "LATENCY_REDUCTION",
        "auto_deploy": True,
    })
    assert response.status_code == 200
    data = response.json()
    assert "cycle_id" in data
    assert data["stage"] in ["DEPLOYED", "GOVERNANCE_REVIEW"]


def test_api_profiler_and_diagnostics():
    res_snap = client.post("/api/v1/evolution/profiler/collect")
    assert res_snap.status_code == 200
    assert "composite_health_score" in res_snap.json()

    res_diag = client.post("/api/v1/evolution/diagnostics/run")
    assert res_diag.status_code == 200
    assert isinstance(res_diag.json(), list)


def test_api_capabilities():
    res_disc = client.post("/api/v1/evolution/capabilities/discover")
    assert res_disc.status_code == 200
    assert isinstance(res_disc.json(), list)

    res_reg = client.post("/api/v1/evolution/capabilities/register", json={
        "name": "Transformer Layout Tokenizer",
        "domain": "document_ai",
        "description": "High throughput OCR layout tokenizer",
    })
    assert res_reg.status_code == 200
    assert res_reg.json()["name"] == "Transformer Layout Tokenizer"


def test_api_architecture_and_optimizer():
    res_topo = client.get("/api/v1/evolution/architecture/topology")
    assert res_topo.status_code == 200
    assert "node_count" in res_topo.json()

    res_opt = client.post("/api/v1/evolution/optimizer/candidates", json={
        "target_subsystem": "llm_cognition",
        "objective": "TOKEN_EFFICIENCY",
    })
    assert res_opt.status_code == 200
    assert res_opt.json()["fitness_score"] > 0.0


def test_api_mutations_and_benchmarks():
    res_mut = client.post("/api/v1/evolution/mutations/propose", json={
        "title": "Async Task Group Validator",
        "mutation_type": "PLANNER_REDESIGN",
        "target_components": ["planner"],
        "code_diff_spec": "--- a/p.py\n+++ b/p.py\n-pass\n+await validate()",
        "rationale": "Parallel execution speedup",
    })
    assert res_mut.status_code == 200
    mut_id = res_mut.json()["mutation_id"]

    res_bench = client.post("/api/v1/evolution/benchmarks/run", json={
        "baseline_version": "v13.12-prod",
        "mutation_id": mut_id,
        "test_case_count": 50,
    })
    assert res_bench.status_code == 200
    assert res_bench.json()["status"] in ["PASSED", "FAILED"]


def test_api_governance_and_deployment():
    # Submit review
    res_gov = client.post("/api/v1/evolution/governance/reviews", json={
        "mutation_id": "mut_api_test",
        "risk_level": "LOW",
    })
    assert res_gov.status_code == 200
    res_gov.json()["review_id"]

    # Launch Canary
    res_dep = client.post("/api/v1/evolution/deployments/launch", json={
        "mutation_id": "mut_api_test",
        "target_version": "v13.13.2",
        "initial_traffic_pct": 20.0,
    })
    assert res_dep.status_code == 200
    dep_id = res_dep.json()["deployment_id"]

    # Advance Canary
    res_adv = client.post("/api/v1/evolution/deployments/advance", json={
        "deployment_id": dep_id,
        "target_traffic_pct": 100.0,
    })
    assert res_adv.status_code == 200
    assert res_adv.json()["deployment_state"] == "PROMOTED"
