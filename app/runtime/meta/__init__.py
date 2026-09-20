"""
AMRS-RSIP Phase 13.9 - Autonomous Meta-Reasoning, Strategic Planning & Recursive Self-Improvement Platform
"""

from app.runtime.meta.events import *
from app.runtime.meta.observation import *
from app.runtime.meta.reasoning import *
from app.runtime.meta.reflection import *
from app.runtime.meta.strategy import *
from app.runtime.meta.experiments import *
from app.runtime.meta.capabilities import *
from app.runtime.meta.policies import *
from app.runtime.meta.architecture import *
from app.runtime.meta.self_improvement import *
from app.runtime.meta.governance import *
from app.runtime.meta.runtime import *

__all__ = [
    # Events
    "ReflectionTier",
    "ImprovementStatus",
    "MetaBaseEvent",
    "StrategicObservationRecorded",
    "MetaReasoningInitiated",
    "BottleneckDetected",
    "RecursiveReflectionCompleted",
    "StrategicPlanGenerated",
    "ExperimentScheduled",
    "ExperimentConcluded",
    "CapabilityDiscovered",
    "PolicyEvolutionProposed",
    "ArchitectureOptimized",
    "SelfImprovementCycleCompleted",
    "GovernanceApproved",
    "GovernanceRejected",
    "RollbackExecuted",
    # Observation
    "StrategicEvidenceNode",
    "StrategicEvidenceEdge",
    "StrategicEvidenceGraph",
    "StrategicObservationLayer",
    # Reasoning
    "StrategicBottleneck",
    "StrategicAlternative",
    "MetaReasoningGraph",
    "MetaReasoningEngine",
    # Reflection
    "ReflectionNode",
    "RecursiveReflectionTree",
    "RecursiveReflectionEngine",
    # Strategy
    "StrategicMilestone",
    "StrategicRoadmap",
    "StrategicPlanner",
    # Experiments
    "ReplayExperimentResult",
    "AutonomousExperimentationEngine",
    # Capabilities
    "SynthesizedCapability",
    "CapabilityDiscoveryEngine",
    # Policies
    "PolicyEvolutionProposal",
    "PolicyEvolutionEngine",
    # Architecture
    "ArchitectureOptimizationProposal",
    "ArchitectureOptimizer",
    # Self-Improvement
    "SelfImprovementCycle",
    "RecursiveSelfImprovementEngine",
    # Governance
    "StrategicApprovalRecord",
    "StrategicGovernanceEngine",
    # Runtime
    "MetaRuntime",
    "get_meta_runtime",
]
