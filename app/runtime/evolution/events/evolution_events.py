"""
Phase 13.13: Autonomous Self-Evolution, Architecture Optimization & Recursive Improvement Platform (ASEAORIP)
Domain Events, Enums, and Reactive Evolution Event Bus.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List
import uuid


class EvolutionStage(str, Enum):
    OBSERVING = "OBSERVING"
    PROFILING = "PROFILING"
    DIAGNOSING = "DIAGNOSING"
    DISCOVERING = "DISCOVERING"
    OPTIMIZING = "OPTIMIZING"
    MUTATING = "MUTATING"
    BENCHMARKING = "BENCHMARKING"
    SIMULATING = "SIMULATING"
    GOVERNING = "GOVERNING"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    DEPLOYING = "DEPLOYING"
    DEPLOYED = "DEPLOYED"
    COMPLETED = "COMPLETED"
    ROLLED_BACK = "ROLLED_BACK"


class MutationType(str, Enum):
    MODULE_REFACTORING = "MODULE_REFACTORING"
    PLANNER_REDESIGN = "PLANNER_REDESIGN"
    WORKFLOW_RESTRUCTURING = "WORKFLOW_RESTRUCTURING"
    AGENT_SPECIALIZATION = "AGENT_SPECIALIZATION"
    AGENT_MERGING = "AGENT_MERGING"
    AGENT_MERGE = "AGENT_MERGING"
    AGENT_SPLITTING = "AGENT_SPLITTING"
    AGENT_SPLIT = "AGENT_SPLITTING"
    DEPENDENCY_INVERSION = "DEPENDENCY_INVERSION"
    PLUGIN_CREATION = "PLUGIN_CREATION"
    SCHEMA_EVOLUTION = "SCHEMA_EVOLUTION"
    STORAGE_OPTIMIZATION = "STORAGE_OPTIMIZATION"
    CACHE_REDESIGN = "CACHE_REDESIGN"
    API_REDESIGN = "API_REDESIGN"
    RUNTIME_SCHEDULING = "RUNTIME_SCHEDULING"
    ROUTING_REFACTOR = "ROUTING_REFACTOR"
    PROMPT_REFACTOR = "PROMPT_REFACTOR"
    MEMORY_TOPOLOGY_CHANGE = "MEMORY_TOPOLOGY_CHANGE"
    EXECUTION_POLICY_CHANGE = "EXECUTION_POLICY_CHANGE"
    HYPERPARAMETER_TUNING = "HYPERPARAMETER_TUNING"


class OptimizationObjective(str, Enum):
    MINIMIZE_LATENCY = "MINIMIZE_LATENCY"
    LATENCY_REDUCTION = "LATENCY_REDUCTION"
    MINIMIZE_MEMORY_FOOTPRINT = "MINIMIZE_MEMORY_FOOTPRINT"
    MINIMIZE_TOKEN_WASTE = "MINIMIZE_TOKEN_WASTE"
    TOKEN_EFFICIENCY = "TOKEN_EFFICIENCY"
    MINIMIZE_COST = "MINIMIZE_COST"
    COST_MINIMIZATION = "COST_MINIMIZATION"
    MAXIMIZE_THROUGHPUT = "MAXIMIZE_THROUGHPUT"
    THROUGHPUT_SCALING = "THROUGHPUT_SCALING"
    MAXIMIZE_ACCURACY = "MAXIMIZE_ACCURACY"
    ACCURACY_MAXIMIZATION = "MAXIMIZE_ACCURACY"
    MAXIMIZE_RELIABILITY = "MAXIMIZE_RELIABILITY"
    SAFETY_COMPLIANCE = "SAFETY_COMPLIANCE"
    MAXIMIZE_DECOUPLING = "MAXIMIZE_DECOUPLING"


class ArchitectureHealth(str, Enum):
    EXCELLENT = "EXCELLENT"
    OPTIMAL = "OPTIMAL"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    CRITICAL_BOTTLENECK = "CRITICAL_BOTTLENECK"
    CRITICAL = "CRITICAL_BOTTLENECK"
    EVOLUTION_RECOMMENDED = "EVOLUTION_RECOMMENDED"


class DeploymentState(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    CANARY = "CANARY"
    CANARY_ACTIVE = "CANARY_ACTIVE"
    PROMOTING = "PROMOTING"
    PROMOTED = "PROMOTED"
    BLUE_GREEN_PROMOTED = "BLUE_GREEN_PROMOTED"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    RETIRED = "RETIRED"


class CapabilityState(str, Enum):
    ACTIVE = "ACTIVE"
    PROPOSED = "PROPOSED"
    EXPANDED = "EXPANDED"
    DEPRECATED = "DEPRECATED"
    DUPLICATE = "DUPLICATE"


class BenchmarkStatus(str, Enum):
    PASSED = "PASSED"
    PASSED_SUPERIOR = "PASSED_SUPERIOR"
    PASSED_PARITY = "PASSED_PARITY"
    FAILED = "FAILED"
    REGRESSED = "REGRESSED"
    RUNNING = "RUNNING"
    INCONCLUSIVE = "INCONCLUSIVE"


class ImprovementConfidence(str, Enum):
    DEFINITIVE_PROOF = "DEFINITIVE_PROOF"
    HIGH_EMPIRICAL = "HIGH_EMPIRICAL"
    PROVISIONAL_SIMULATION = "PROVISIONAL_SIMULATION"
    SPECULATIVE = "SPECULATIVE"


@dataclass
class EvolutionDomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: Any = "EVOLUTION_EVENT"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_component: str = "evolution_runtime"
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": str(self.event_type.value if isinstance(self.event_type, Enum) else self.event_type),
            "timestamp": self.timestamp,
            "source_component": self.source_component,
            "payload": self.payload,
            "metadata": self.metadata,
        }


# 30+ Domain Event Dataclasses
@dataclass
class ArchitectureWeaknessDetected(EvolutionDomainEvent):
    event_type: Any = "ArchitectureWeaknessDetected"


@dataclass
class CapabilityGapDetected(EvolutionDomainEvent):
    event_type: Any = "CapabilityGapDetected"


@dataclass
class PerformanceRegressionDetected(EvolutionDomainEvent):
    event_type: Any = "PerformanceRegressionDetected"


@dataclass
class OptimizationCandidateCreated(EvolutionDomainEvent):
    event_type: Any = "OptimizationCandidateCreated"


OptimizationCandidateGenerated = OptimizationCandidateCreated
ArchitectureOptimizationProposed = OptimizationCandidateCreated


@dataclass
class OptimizationAccepted(EvolutionDomainEvent):
    event_type: Any = "OptimizationAccepted"


@dataclass
class OptimizationRejected(EvolutionDomainEvent):
    event_type: Any = "OptimizationRejected"


@dataclass
class ArchitectureMutationCreated(EvolutionDomainEvent):
    event_type: Any = "ArchitectureMutationCreated"


MutationProposed = ArchitectureMutationCreated


@dataclass
class MutationValidated(EvolutionDomainEvent):
    event_type: Any = "MutationValidated"


@dataclass
class MutationRolledBack(EvolutionDomainEvent):
    event_type: Any = "MutationRolledBack"


DeploymentRolledBack = MutationRolledBack


@dataclass
class BenchmarkCompleted(EvolutionDomainEvent):
    event_type: Any = "BenchmarkCompleted"


@dataclass
class ArchitectureComparisonCompleted(EvolutionDomainEvent):
    event_type: Any = "ArchitectureComparisonCompleted"


@dataclass
class CapabilityExpanded(EvolutionDomainEvent):
    event_type: Any = "CapabilityExpanded"


@dataclass
class CapabilityDeprecated(EvolutionDomainEvent):
    event_type: Any = "CapabilityDeprecated"


@dataclass
class SelfImprovementStarted(EvolutionDomainEvent):
    event_type: Any = "SelfImprovementStarted"


@dataclass
class SelfImprovementCompleted(EvolutionDomainEvent):
    event_type: Any = "SelfImprovementCompleted"


@dataclass
class EvolutionCycleStarted(EvolutionDomainEvent):
    event_type: Any = "EvolutionCycleStarted"


EvolutionCycleInitiated = EvolutionCycleStarted


@dataclass
class EvolutionCycleFinished(EvolutionDomainEvent):
    event_type: Any = "EvolutionCycleFinished"


EvolutionCycleCompleted = EvolutionCycleFinished


@dataclass
class DeploymentCandidateCreated(EvolutionDomainEvent):
    event_type: Any = "DeploymentCandidateCreated"


@dataclass
class GovernanceApprovedEvolution(EvolutionDomainEvent):
    event_type: Any = "GovernanceApprovedEvolution"


GovernanceApprovalGranted = GovernanceApprovedEvolution


@dataclass
class GovernanceRejectedEvolution(EvolutionDomainEvent):
    event_type: Any = "GovernanceRejectedEvolution"


@dataclass
class SafetyConstraintTriggered(EvolutionDomainEvent):
    event_type: Any = "SafetyConstraintTriggered"


@dataclass
class RiskThresholdExceeded(EvolutionDomainEvent):
    event_type: Any = "RiskThresholdExceeded"


@dataclass
class ArchitectureMerged(EvolutionDomainEvent):
    event_type: Any = "ArchitectureMerged"


@dataclass
class ArchitectureForked(EvolutionDomainEvent):
    event_type: Any = "ArchitectureForked"


@dataclass
class ArchitectureRetired(EvolutionDomainEvent):
    event_type: Any = "ArchitectureRetired"


@dataclass
class CanaryRolloutUpdated(EvolutionDomainEvent):
    event_type: Any = "CanaryRolloutUpdated"


DeploymentProgressed = CanaryRolloutUpdated
DeploymentCompleted = CanaryRolloutUpdated


@dataclass
class DigitalTwinSimulationFinished(EvolutionDomainEvent):
    event_type: Any = "DigitalTwinSimulationFinished"


SimulationCompleted = DigitalTwinSimulationFinished


@dataclass
class ChaosInjectionExecuted(EvolutionDomainEvent):
    event_type: Any = "ChaosInjectionExecuted"


@dataclass
class RollbackCheckpointCreated(EvolutionDomainEvent):
    event_type: Any = "RollbackCheckpointCreated"


RollbackSnapshotCreated = RollbackCheckpointCreated


@dataclass
class SystemProfilingCompleted(EvolutionDomainEvent):
    event_type: Any = "SystemProfilingCompleted"


class EvolutionEventBus:
    """Reactive in-memory domain event bus for Phase 13.13 Self-Evolution."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[EvolutionDomainEvent], None]]] = {}
        self._history: List[EvolutionDomainEvent] = []

    def subscribe(self, event_type: Any, handler: Callable[[EvolutionDomainEvent], None]) -> None:
        key = event_type.value if isinstance(event_type, Enum) else str(event_type)
        self._handlers.setdefault(key, []).append(handler)

    def publish(self, event: EvolutionDomainEvent) -> None:
        self._history.append(event)
        key = event.event_type.value if isinstance(event.event_type, Enum) else str(event.event_type)
        for handler in self._handlers.get(key, []):
            try:
                handler(event)
            except Exception:
                pass

    def get_history(self, limit: int = 100) -> List[EvolutionDomainEvent]:
        return self._history[-limit:]
