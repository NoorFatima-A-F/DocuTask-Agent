"""
Verifiers package for Phase 3J.3: Enterprise Performance Baseline & Capacity Verification Framework.
"""

from typing import List

from ..domain.interfaces import IPerformanceVerifier
from .ai_pipeline_performance_verifier import AIPipelinePerformanceVerifier
from .baseline_performance_verifier import BaselinePerformanceVerifier
from .capacity_model_verifier import CapacityModelVerifier
from .concurrent_load_verifier import ConcurrentLoadVerifier
from .database_performance_verifier import DatabasePerformanceVerifier
from .latency_distribution_verifier import LatencyDistributionVerifier
from .performance_architecture_verifier import PerformanceArchitectureVerifier
from .performance_failure_verifier import PerformanceFailureVerifier
from .performance_regression_verifier import PerformanceRegressionVerifier
from .queue_capacity_verifier import QueueCapacityVerifier
from .resource_utilization_verifier import ResourceUtilizationVerifier
from .worker_scaling_verifier import WorkerScalingVerifier


def get_all_verifiers() -> List[IPerformanceVerifier]:
    """Returns an instantiated list of all 12 verifiers covering Phase 3J.3."""
    return [
        PerformanceArchitectureVerifier(),
        BaselinePerformanceVerifier(),
        AIPipelinePerformanceVerifier(),
        ConcurrentLoadVerifier(),
        CapacityModelVerifier(),
        LatencyDistributionVerifier(),
        ResourceUtilizationVerifier(),
        DatabasePerformanceVerifier(),
        QueueCapacityVerifier(),
        WorkerScalingVerifier(),
        PerformanceFailureVerifier(),
        PerformanceRegressionVerifier(),
    ]


__all__ = [
    "PerformanceArchitectureVerifier",
    "BaselinePerformanceVerifier",
    "AIPipelinePerformanceVerifier",
    "ConcurrentLoadVerifier",
    "CapacityModelVerifier",
    "LatencyDistributionVerifier",
    "ResourceUtilizationVerifier",
    "DatabasePerformanceVerifier",
    "QueueCapacityVerifier",
    "WorkerScalingVerifier",
    "PerformanceFailureVerifier",
    "PerformanceRegressionVerifier",
    "get_all_verifiers",
]
