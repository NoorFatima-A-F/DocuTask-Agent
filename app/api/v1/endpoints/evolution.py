"""FastAPI REST Endpoints for Autonomous Cognitive Evolution & Phase 13.13 (ASEAORIP).

Provides APIs for:
1. Legacy Strategy Discovery, Planner Self-Evolution, Digital Twin Simulation, Structural Causal Reasoning, Deliberation Council.
2. Phase 13.13 Autonomous Architecture Profiling, Diagnostics, Capability Gaps, Pareto Optimization, Non-Destructive Mutations, Benchmarking, Simulation, Cryptographic Governance, Progressive Canary Deployments, and Closed-Loop Evolution Cycles.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

# Legacy Phase 11.x imports
from app.runtime.strategy_discovery.graph_synthesis import HTNGraphSynthesizer, SynthesizedDAG
from app.runtime.strategy_discovery.mutation import EvolutionaryGraphMutator, MutationResult
from app.runtime.strategy_discovery.evaluation import StrategyEvaluator, StrategyEvaluationReport
from app.runtime.strategy_discovery.repository import StrategyRepository, SynthesizedStrategyRecord
from app.runtime.evolution.planner_evolution_engine import PlannerSelfEvolutionEngine, EvolutionCycleReport
from app.runtime.evolution.planner_version_registry import PlannerVersionRegistry, PlannerGeneration
from app.runtime.simulation.cluster_simulator import DigitalTwinClusterSimulator, DigitalTwinClusterReport
from app.runtime.simulation.scale_simulator import MonteCarloScaleSimulator, MonteCarloScaleReport
from app.runtime.causal.structural_causal_model import StructuralCausalModel, CausalNode
from app.runtime.causal.do_calculus import DoCalculusEngine, InterventionResult, CounterfactualResult
from app.runtime.causal.causal_discovery import CausalDiscoveryEngine, CausalDiscoveryReport
from app.runtime.deliberation.council import DeliberationCouncilCoordinator, DeliberationSessionSummary

# Phase 13.13 Subsystem Engines
from app.runtime.evolution.runtime import get_evolution_runtime, EvolutionRuntime

router = APIRouter()

# Global singletons
_synthesizer = HTNGraphSynthesizer()
_mutator = EvolutionaryGraphMutator()
_evaluator = StrategyEvaluator()
_strategy_repo = StrategyRepository()
_version_registry = PlannerVersionRegistry()
_evolution_engine = PlannerSelfEvolutionEngine(registry=_version_registry)
_cluster_sim = DigitalTwinClusterSimulator()
_scale_sim = MonteCarloScaleSimulator()
_scm = StructuralCausalModel()
_do_engine = DoCalculusEngine(scm=_scm)
_causal_disc = CausalDiscoveryEngine()
_council = DeliberationCouncilCoordinator()

# Phase 13.13 Runtime
_runtime: EvolutionRuntime = get_evolution_runtime()


# ==========================================
# Legacy Request Models
# ==========================================

class SynthesizeStrategyRequest(BaseModel):
    goal_intent: str = "extract_financial_invoice"
    branch_index: int = 0


class MutateStrategyRequest(BaseModel):
    strategy_id: Optional[str] = None
    mutation_type: Optional[str] = "OPERATOR_SWAP"


class EvolvePlannerRequest(BaseModel):
    weakness_diagnosis: str = "Elevated tail latency during multi-column table extraction bursts"
    simulated_trials: int = 1000


class RunSimulationRequest(BaseModel):
    mission_count: int = 500
    arrival_rate_per_sec: float = 10.0
    chaos_fault_rate: float = 0.02


class CausalInterventionRequest(BaseModel):
    treatment_variable: str = "worker_concurrency"
    treatment_value: float = 8.0
    outcome_variable: str = "total_latency_ms"


class DeliberationRequest(BaseModel):
    mission_id: str = "mission_delib_001"
    candidate_strategies: Optional[List[Dict[str, Any]]] = None


# ==========================================
# Phase 13.13 Request Models
# ==========================================

class RunEvolutionCycleRequest(BaseModel):
    target_subsystem: str = "llm_orchestrator"
    objective: str = "LATENCY_REDUCTION"
    auto_deploy: bool = True


class ProposeImprovementPlanRequest(BaseModel):
    title: str = "Decouple Swarm Coordination Ring"
    target_subsystems: List[str] = ["swarm_orchestrator", "shared_memory"]
    action_type: str = "DECOUPLE_ASYNC_EVENT_BUS"
    rationale: str = "Reduces lock contention under burst load."
    expected_coupling_reduction: float = 0.40
    expected_latency_gain_pct: float = 25.0


class RegisterCapabilityRequest(BaseModel):
    name: str = "Recursive Neural Layout Parser"
    domain: str = "document_intelligence"
    description: str = "High precision bounding-box token grouping"
    maturity_level: str = "EXPERIMENTAL"
    accuracy_score: float = 0.96
    latency_ms: float = 18.5
    cost_per_invocation: float = 0.0012


class GenerateCandidateRequest(BaseModel):
    target_subsystem: str = "llm_cognition"
    objective: str = "TOKEN_EFFICIENCY"
    hyperparameters: Optional[Dict[str, Any]] = None
    custom_risk_tolerance: float = 0.20


class ProposeMutationRequest(BaseModel):
    title: str = "Lock-Free Async Ring Buffer"
    mutation_type: str = "ROUTING_REFACTOR"
    target_components: List[str] = ["event_bus", "swarm_orchestrator"]
    code_diff_spec: str = "--- a/app/runtime/events.py\n+++ b/app/runtime/events.py\n@@ -1,3 +1,3 @@\n-lock.acquire()\n+lock_free_cas()"
    rationale: str = "Eliminates mutex bottlenecks"
    safety_analysis: str = "Non-blocking verified"
    confidence_score: float = 0.95


class RunBenchmarkRequest(BaseModel):
    baseline_version: str = "v13.12-prod"
    candidate_version: Optional[str] = None
    mutation_id: Optional[str] = None
    test_case_count: int = 500


class RunSandboxSimulationRequest(BaseModel):
    mutation_id: Optional[str] = None
    simulation_mode: str = "SHADOW_REPLAY"
    traces_count: int = 1500


class SubmitGovernanceReviewRequest(BaseModel):
    mutation_id: str
    candidate_id: Optional[str] = None
    risk_level: str = "LOW"
    formal_verification_passed: bool = True
    simulation_verified: bool = True
    benchmark_verified: bool = True


class LaunchDeploymentRequest(BaseModel):
    mutation_id: str
    target_version: str = "v13.13.0"
    initial_traffic_pct: float = 10.0
    rollback_snapshot_id: Optional[str] = None


class AdvanceCanaryRequest(BaseModel):
    deployment_id: str
    target_traffic_pct: float = 50.0


class TriggerRollbackRequest(BaseModel):
    deployment_id: str
    reason: str = "Manual operator or SLA trigger"


# ==========================================
# Legacy Endpoints (Maintained for Backward Compatibility)
# ==========================================

@router.post("/strategy/synthesize", response_model=SynthesizedStrategyRecord, summary="Synthesize Strategy via HTN")
async def synthesize_strategy(req: SynthesizeStrategyRequest) -> SynthesizedStrategyRecord:
    """Synthesizes a new execution DAG using Hierarchical Task Network (HTN) decomposition."""
    dag = _synthesizer.synthesize_dag(goal_intent=req.goal_intent, branch_index=req.branch_index)
    eval_report = _evaluator.evaluate_strategy(dag)
    record = _strategy_repo.register_strategy(dag, eval_report)
    return record


@router.post("/strategy/mutate", response_model=MutationResult, summary="Mutate Strategy Graph")
async def mutate_strategy(req: MutateStrategyRequest) -> MutationResult:
    """Applies evolutionary mutations (operator swap, node insertion, parallel split) to explore novel DAGs."""
    base_dag = _synthesizer.synthesize_dag()
    return _mutator.mutate_dag(base_dag, mutation_type=req.mutation_type)


@router.post("/planner/evolve", response_model=EvolutionCycleReport, summary="Trigger Planner Self-Evolution")
async def evolve_planner(req: EvolvePlannerRequest) -> EvolutionCycleReport:
    """Runs a closed-loop self-evolution cycle, generating a new planner generation."""
    return _evolution_engine.run_evolution_cycle(
        weakness_diagnosis=req.weakness_diagnosis,
        target_simulated_trials=req.simulated_trials,
    )


@router.get("/planner/generations", response_model=List[PlannerGeneration], summary="List Planner Generations")
async def list_planner_generations() -> List[PlannerGeneration]:
    """Retrieves immutable genealogy of planner versions."""
    return _version_registry.list_generations()


@router.post("/simulation/run", response_model=DigitalTwinClusterReport, summary="Run Digital Twin Cluster Simulation")
async def run_digital_twin_simulation(req: RunSimulationRequest) -> DigitalTwinClusterReport:
    """Simulates 1,000+ virtual worker nodes under synthetic arrival workloads and chaos faults."""
    return _cluster_sim.simulate_mission_workload(
        mission_count=req.mission_count,
        arrival_rate_per_sec=req.arrival_rate_per_sec,
        chaos_fault_rate=req.chaos_fault_rate,
    )


@router.get("/causal/model", response_model=List[CausalNode], summary="Get SCM Causal Graph Topology")
async def get_causal_model() -> List[CausalNode]:
    """Returns nodes and structural equation topology of the Structural Causal Model."""
    return _scm.list_nodes()


@router.post("/causal/intervene", response_model=InterventionResult, summary="Execute Pearl's Do-Calculus Intervention")
async def evaluate_causal_intervention(req: CausalInterventionRequest) -> InterventionResult:
    """Evaluates P(Y | do(X = x)) via graph surgery and backdoor adjustment."""
    return _do_engine.evaluate_do_intervention(
        treatment_var=req.treatment_variable,
        treatment_val=req.treatment_value,
        outcome_var=req.outcome_variable,
    )


@router.post("/deliberation/session", response_model=DeliberationSessionSummary, summary="Convene Multi-Agent Deliberation Council")
async def convene_council_deliberation(req: DeliberationRequest) -> DeliberationSessionSummary:
    """Convenes the 8-agent council for dialectic debate, Borda voting, and resource auctioning."""
    return _council.convene_deliberation_session(
        mission_id=req.mission_id,
        candidate_strategies=req.candidate_strategies,
    )


# ==========================================
# Phase 13.13 Advanced Self-Evolution Endpoints
# ==========================================

@router.get("/executive-summary", summary="Phase 13.13 Executive Summary KPIs")
async def get_executive_summary() -> Dict[str, Any]:
    """Returns platform health, architecture metrics, candidate counts, and deployment status."""
    return _runtime.get_executive_summary()


@router.get("/genome", summary="Get Platform Architecture Genome")
async def get_platform_genome() -> Dict[str, Any]:
    """Returns full platform genome including components, capabilities, active mutations, and rollback snapshots."""
    return _runtime.get_platform_genome()


@router.post("/cycle/run", summary="Run Closed-Loop Self-Evolution Cycle")
async def run_evolution_cycle(req: RunEvolutionCycleRequest) -> Dict[str, Any]:
    """Executes closed-loop 10-stage recursive self-improvement cycle."""
    res = _runtime.run_full_evolution_cycle(
        target_subsystem=req.target_subsystem,
        objective=req.objective,
        auto_deploy=req.auto_deploy,
    )
    return res.to_dict()


@router.get("/cycle/history", summary="List Historical Self-Evolution Cycles")
async def list_cycle_history() -> List[Dict[str, Any]]:
    return [c.to_dict() for c in _runtime.cycle_history]


# --- Profiler & Health ---

@router.get("/profiler/snapshots", summary="List Runtime Telemetry Snapshots")
async def list_profiler_snapshots() -> List[Dict[str, Any]]:
    return [s.to_dict() for s in _runtime.profiler.list_snapshots()]


@router.post("/profiler/collect", summary="Collect Real-time Health Snapshot")
async def collect_profiler_snapshot() -> Dict[str, Any]:
    snapshot = _runtime.profiler.collect_snapshot()
    return snapshot.to_dict()


# --- Diagnostics ---

@router.get("/diagnostics", summary="List Architectural Diagnoses & Bottlenecks")
async def list_diagnoses() -> List[Dict[str, Any]]:
    return [d.to_dict() for d in _runtime.diagnostics.list_diagnoses()]


@router.post("/diagnostics/run", summary="Run Bottleneck Diagnostics")
async def run_diagnostics() -> List[Dict[str, Any]]:
    snapshot = _runtime.profiler.collect_snapshot()
    diagnoses = _runtime.diagnostics.diagnose_weaknesses(snapshot)
    return [d.to_dict() for d in diagnoses]


# --- Capability Engine ---

@router.get("/capabilities", summary="List Registered Subsystem Capabilities")
async def list_capabilities() -> List[Dict[str, Any]]:
    return [c.to_dict() for c in _runtime.capability.list_capabilities()]


@router.post("/capabilities/discover", summary="Discover Missing Capabilities & Gaps")
async def discover_capabilities() -> List[Dict[str, Any]]:
    gaps = _runtime.capability.discover_capability_gaps()
    return [g.to_dict() for g in gaps]


@router.post("/capabilities/register", summary="Register or Update Capability")
async def register_capability(req: RegisterCapabilityRequest) -> Dict[str, Any]:
    cap = _runtime.capability.register_capability(
        name=req.name,
        domain=req.domain,
        description=req.description,
        maturity_level=req.maturity_level,
        accuracy_score=req.accuracy_score,
        latency_ms=req.latency_ms,
        cost_per_invocation=req.cost_per_invocation,
    )
    return cap.to_dict()


# --- Architecture Engine ---

@router.get("/architecture/topology", summary="Get Architectural Dependency Topology")
async def get_architecture_topology() -> Dict[str, Any]:
    return _runtime.architecture.get_topology()


@router.get("/architecture/plans", summary="List Architecture Improvement Plans")
async def list_architecture_plans() -> List[Dict[str, Any]]:
    return [p.to_dict() for p in _runtime.architecture.list_improvement_plans()]


@router.post("/architecture/plans", summary="Propose Architectural Improvement Plan")
async def propose_architecture_plan(req: ProposeImprovementPlanRequest) -> Dict[str, Any]:
    plan = _runtime.architecture.generate_improvement_plan(
        title=req.title,
        target_subsystems=req.target_subsystems,
        action_type=req.action_type,
        rationale=req.rationale,
        expected_coupling_reduction=req.expected_coupling_reduction,
        expected_latency_gain_pct=req.expected_latency_gain_pct,
    )
    return plan.to_dict()


# --- Optimizer Engine ---

@router.get("/optimizer/candidates", summary="List Multi-Objective Candidates")
async def list_optimization_candidates() -> List[Dict[str, Any]]:
    return [c.to_dict() for c in _runtime.optimizer.list_candidates()]


@router.get("/optimizer/pareto", summary="Get Pareto Frontier Candidates")
async def get_pareto_frontier() -> List[Dict[str, Any]]:
    return [c.to_dict() for c in _runtime.optimizer.compute_pareto_frontier()]


@router.post("/optimizer/candidates", summary="Generate Multi-Objective Candidate")
async def generate_optimization_candidate(req: GenerateCandidateRequest) -> Dict[str, Any]:
    c = _runtime.optimizer.generate_candidate(
        target_subsystem=req.target_subsystem,
        objective=req.objective,
        hyperparameters=req.hyperparameters,
        custom_risk_tolerance=req.custom_risk_tolerance,
    )
    return c.to_dict()


# --- Self-Modification & Mutations ---

@router.get("/mutations", summary="List Architectural Mutation Proposals")
async def list_mutations() -> List[Dict[str, Any]]:
    return [m.to_dict() for m in _runtime.mutation.list_proposals()]


@router.post("/mutations/propose", summary="Propose Non-Destructive Code Mutation")
async def propose_mutation(req: ProposeMutationRequest) -> Dict[str, Any]:
    mutation = _runtime.mutation.propose_mutation(
        title=req.title,
        mutation_type=req.mutation_type,
        target_components=req.target_components,
        code_diff_spec=req.code_diff_spec,
        rationale=req.rationale,
        safety_analysis=req.safety_analysis,
        confidence_score=req.confidence_score,
    )
    return mutation.to_dict()


# --- Benchmarks ---

@router.get("/benchmarks", summary="List Empirical Benchmark Comparisons")
async def list_benchmarks() -> List[Dict[str, Any]]:
    return [b.to_dict() for b in _runtime.benchmark.list_benchmarks()]


@router.post("/benchmarks/run", summary="Run Side-by-Side Empirical Benchmark")
async def run_benchmark(req: RunBenchmarkRequest) -> Dict[str, Any]:
    res = _runtime.benchmark.run_benchmark(
        baseline_version=req.baseline_version,
        candidate_version=req.candidate_version,
        mutation_id=req.mutation_id,
        test_case_count=req.test_case_count,
    )
    return res.to_dict()


# --- Simulations & Digital Twin Sandbox ---

@router.get("/simulations", summary="List Digital Twin Replay Simulations")
async def list_simulations() -> List[Dict[str, Any]]:
    return [s.to_dict() for s in _runtime.simulation.list_simulations()]


@router.post("/simulations/run", summary="Run Digital Twin Sandbox Simulation")
async def run_simulation(req: RunSandboxSimulationRequest) -> Dict[str, Any]:
    rep = _runtime.simulation.run_simulation(
        mutation_id=req.mutation_id,
        simulation_mode=req.simulation_mode,
        traces_count=req.traces_count,
    )
    return rep.to_dict()


# --- Governance & Cryptographic Rollback ---

@router.get("/governance/reviews", summary="List Governance Reviews")
async def list_governance_reviews() -> List[Dict[str, Any]]:
    return [r.to_dict() for r in _runtime.governance.list_reviews()]


@router.post("/governance/reviews", summary="Submit Mutation for Governance Review")
async def submit_governance_review(req: SubmitGovernanceReviewRequest) -> Dict[str, Any]:
    review = _runtime.governance.submit_for_review(
        mutation_id=req.mutation_id,
        candidate_id=req.candidate_id,
        risk_level=req.risk_level,
        formal_verification_passed=req.formal_verification_passed,
        simulation_verified=req.simulation_verified,
        benchmark_verified=req.benchmark_verified,
    )
    return review.to_dict()


@router.post("/governance/approve/{review_id}", summary="Approve Mutation Review")
async def approve_governance_review(review_id: str) -> Dict[str, Any]:
    review = _runtime.governance.approve_review(review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Governance review not found")
    return review.to_dict()


@router.post("/governance/reject/{review_id}", summary="Reject Mutation Review")
async def reject_governance_review(review_id: str, reason: str = Query("Rejected by policy")) -> Dict[str, Any]:
    review = _runtime.governance.reject_review(review_id, reason=reason)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Governance review not found")
    return review.to_dict()


@router.get("/governance/snapshots", summary="List Immutable Rollback Snapshots")
async def list_rollback_snapshots() -> List[Dict[str, Any]]:
    return [s.to_dict() for s in _runtime.governance.list_snapshots()]


# --- Deployment & Progressive Rollout ---

@router.get("/deployments", summary="List Deployments")
async def list_deployments() -> List[Dict[str, Any]]:
    return [d.to_dict() for d in _runtime.deployment.list_deployments()]


@router.post("/deployments/launch", summary="Launch Progressive Canary Deployment")
async def launch_deployment(req: LaunchDeploymentRequest) -> Dict[str, Any]:
    record = _runtime.deployment.launch_deployment(
        mutation_id=req.mutation_id,
        target_version=req.target_version,
        initial_traffic_pct=req.initial_traffic_pct,
        rollback_snapshot_id=req.rollback_snapshot_id,
    )
    return record.to_dict()


@router.post("/deployments/advance", summary="Advance Canary Traffic Percentage")
async def advance_canary_traffic(req: AdvanceCanaryRequest) -> Dict[str, Any]:
    record = _runtime.deployment.advance_canary(req.deployment_id, req.target_traffic_pct)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deployment record not found")
    return record.to_dict()


@router.post("/deployments/rollback", summary="Trigger Automated Rollback")
async def rollback_deployment(req: TriggerRollbackRequest) -> Dict[str, Any]:
    record = _runtime.deployment.trigger_rollback(req.deployment_id, req.reason)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deployment record not found")
    return record.to_dict()
