"""
Verifiers package for Performance Stress Verification & Capacity Boundary Analysis (Phase 3J.2).
"""

from typing import List

from ..domain.interfaces import IPerformanceVerifier
from .ai_provider_stress_verifier import AIProviderStressVerifier
from .baseline_stress_verifier import BaselineStressVerifier
from .capacity_boundary_verifier import CapacityBoundaryVerifier
from .database_stress_verifier import DatabaseStressVerifier
from .memory_stability_verifier import MemoryStabilityVerifier
from .overload_stress_verifier import OverloadStressVerifier
from .performance_environment_verifier import PerformanceEnvironmentVerifier
from .performance_recovery_verifier import PerformanceRecoveryVerifier
from .performance_regression_gate_verifier import PerformanceRegressionGateVerifier
from .progressive_load_verifier import ProgressiveLoadVerifier
from .worker_scaling_verifier import WorkerScalingVerifier


def get_all_verifiers() -> List[IPerformanceVerifier]:
    """Returns a newly instantiated list of all 10 verifier modules (covering all 15 sub-phases)."""
    return [
        PerformanceEnvironmentVerifier(),
        BaselineStressVerifier(),
        ProgressiveLoadVerifier(),
        OverloadStressVerifier(),
        CapacityBoundaryVerifier(),
        WorkerScalingVerifier(),
        DatabaseStressVerifier(),
        AIProviderStressVerifier(),
        MemoryStabilityVerifier(),
        PerformanceRecoveryVerifier(),
        PerformanceRegressionGateVerifier(),
    ]


__all__ = [
    "PerformanceEnvironmentVerifier",
    "BaselineStressVerifier",
    "ProgressiveLoadVerifier",
    "OverloadStressVerifier",
    "CapacityBoundaryVerifier",
    "WorkerScalingVerifier",
    "DatabaseStressVerifier",
    "AIProviderStressVerifier",
    "MemoryStabilityVerifier",
    "PerformanceRecoveryVerifier",
    "PerformanceRegressionGateVerifier",
    "get_all_verifiers",
]
