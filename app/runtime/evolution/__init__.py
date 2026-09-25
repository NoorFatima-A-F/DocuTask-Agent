"""
Phase 13.13 — Autonomous Self-Evolution, Architecture Optimization & Recursive Improvement Platform (ASEAORIP).
"""

# Legacy Phase 11.x exports for backwards compatibility
from app.runtime.evolution.genetic_optimizer import (
    PlannerChromosome,
    GeneticPlannerOptimizer,
)
from app.runtime.evolution.bayesian_optimizer import (
    ParameterEvaluationPoint,
    BayesianPlannerOptimizer,
)
from app.runtime.evolution.planner_version_registry import (
    PlannerGeneration,
    PlannerVersionRegistry,
)
from app.runtime.evolution.planner_evolution_engine import (
    EvolutionCycleReport,
    PlannerSelfEvolutionEngine,
)

# Phase 13.13 Advanced Autonomous Self-Evolution Subsystems
from app.runtime.evolution.events import (
    EvolutionEventBus,
    EvolutionStage,
    MutationType,
    OptimizationObjective,
    ArchitectureHealth,
    DeploymentState,
    CapabilityState,
    BenchmarkStatus,
    ImprovementConfidence,
)
from app.runtime.evolution.profiler import (
    ProfilerEngine,
    PlatformHealthSnapshot,
)
from app.runtime.evolution.diagnostics import (
    DiagnosticEngine,
    WeaknessDiagnosis,
)
from app.runtime.evolution.capability import (
    CapabilityEngine,
    CapabilityDescriptor,
)
from app.runtime.evolution.architecture import (
    ArchitectureEngine,
    ArchitectureGraphNode,
    ArchitectureGraphEdge,
    ArchitectureImprovementPlan,
)
from app.runtime.evolution.optimizer import (
    OptimizerEngine,
    OptimizationCandidate,
)
from app.runtime.evolution.self_modification import (
    MutationEngine,
    ArchitectureMutationProposal,
)
from app.runtime.evolution.benchmark import (
    BenchmarkEngine,
    BenchmarkComparison,
)
from app.runtime.evolution.simulation import (
    SimulationEngine,
    SimulationReport,
)
from app.runtime.evolution.governance import (
    GovernanceEngine,
    EvolutionGovernanceReview,
    RollbackSnapshot,
)
from app.runtime.evolution.deployment import (
    DeploymentEngine,
    DeploymentRecord,
)
from app.runtime.evolution.runtime import (
    EvolutionRuntime,
    EvolutionCycleResult,
    get_evolution_runtime,
)

__all__ = [
    # Legacy
    "PlannerChromosome",
    "GeneticPlannerOptimizer",
    "ParameterEvaluationPoint",
    "BayesianPlannerOptimizer",
    "PlannerGeneration",
    "PlannerVersionRegistry",
    "EvolutionCycleReport",
    "PlannerSelfEvolutionEngine",
    # Phase 13.13
    "EvolutionEventBus",
    "EvolutionStage",
    "MutationType",
    "OptimizationObjective",
    "ArchitectureHealth",
    "DeploymentState",
    "CapabilityState",
    "BenchmarkStatus",
    "ImprovementConfidence",
    "ProfilerEngine",
    "PlatformHealthSnapshot",
    "DiagnosticEngine",
    "WeaknessDiagnosis",
    "CapabilityEngine",
    "CapabilityDescriptor",
    "ArchitectureEngine",
    "ArchitectureGraphNode",
    "ArchitectureGraphEdge",
    "ArchitectureImprovementPlan",
    "OptimizerEngine",
    "OptimizationCandidate",
    "MutationEngine",
    "ArchitectureMutationProposal",
    "BenchmarkEngine",
    "BenchmarkComparison",
    "SimulationEngine",
    "SimulationReport",
    "GovernanceEngine",
    "EvolutionGovernanceReview",
    "RollbackSnapshot",
    "DeploymentEngine",
    "DeploymentRecord",
    "EvolutionRuntime",
    "EvolutionCycleResult",
    "get_evolution_runtime",
]
