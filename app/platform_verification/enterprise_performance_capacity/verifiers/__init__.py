"""Verifiers registry for Phase 3J.5 Enterprise Performance Baseline & Capacity Verification."""

from typing import List

from app.platform_verification.enterprise_performance_capacity.domain.interfaces import (
    IEnterprisePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.ai_workload_verifier import (
    AIWorkloadVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.bottleneck_analysis_verifier import (
    BottleneckAnalysisVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.capacity_planning_verifier import (
    CapacityPlanningVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.database_performance_verifier import (
    DatabasePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.endurance_testing_verifier import (
    EnduranceTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.latency_breakdown_verifier import (
    LatencyBreakdownVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.load_testing_verifier import (
    LoadTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.performance_baseline_verifier import (
    PerformanceBaselineVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.performance_regression_verifier import (
    PerformanceRegressionVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.queue_performance_verifier import (
    QueuePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.resource_utilization_verifier import (
    ResourceUtilizationVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.spike_testing_verifier import (
    SpikeTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.storage_performance_verifier import (
    StoragePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.stress_testing_verifier import (
    StressTestingVerifier,
)
from app.platform_verification.enterprise_performance_capacity.verifiers.throughput_capacity_verifier import (
    ThroughputCapacityVerifier,
)

__all__ = [
    "PerformanceBaselineVerifier",
    "LatencyBreakdownVerifier",
    "ThroughputCapacityVerifier",
    "LoadTestingVerifier",
    "StressTestingVerifier",
    "SpikeTestingVerifier",
    "EnduranceTestingVerifier",
    "AIWorkloadVerifier",
    "QueuePerformanceVerifier",
    "DatabasePerformanceVerifier",
    "StoragePerformanceVerifier",
    "ResourceUtilizationVerifier",
    "BottleneckAnalysisVerifier",
    "CapacityPlanningVerifier",
    "PerformanceRegressionVerifier",
    "get_all_verifiers",
]


def get_all_verifiers() -> List[IEnterprisePerformanceVerifier]:
    """Returns an instantiated list of all 15 Phase 3J.5 verifiers in sequential order."""
    return [
        PerformanceBaselineVerifier(),       # 3J.5.1
        LatencyBreakdownVerifier(),          # 3J.5.2
        ThroughputCapacityVerifier(),        # 3J.5.3
        LoadTestingVerifier(),               # 3J.5.4 & 3J.5.5
        StressTestingVerifier(),             # 3J.5.6
        SpikeTestingVerifier(),              # 3J.5.7
        EnduranceTestingVerifier(),          # 3J.5.8
        AIWorkloadVerifier(),                # 3J.5.9
        QueuePerformanceVerifier(),          # 3J.5.10
        DatabasePerformanceVerifier(),       # 3J.5.11
        StoragePerformanceVerifier(),        # 3J.5.12
        ResourceUtilizationVerifier(),       # 3J.5.13
        BottleneckAnalysisVerifier(),        # 3J.5.14
        CapacityPlanningVerifier(),          # 3J.5.15
        PerformanceRegressionVerifier(),     # 3J.5.16
    ]
