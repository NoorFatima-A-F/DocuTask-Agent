"""Verifiers registry for Phase 3J.6 Enterprise Performance Infrastructure Verification."""

from typing import List

from app.platform_verification.enterprise_performance_infrastructure.domain.interfaces import (
    IEnterprisePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.test_architecture_verifier import (
    PerformanceTestArchitectureVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.workload_modeling_verifier import (
    WorkloadModelingVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.api_performance_verifier import (
    APIPerformanceVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.e2e_workflow_verifier import (
    E2EWorkflowVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.throughput_scaling_verifier import (
    ThroughputScalingVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.database_performance_verifier import (
    DatabasePerformanceVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.queue_capacity_verifier import (
    QueueCapacityVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.worker_efficiency_verifier import (
    WorkerEfficiencyVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.resource_utilization_verifier import (
    ResourceUtilizationVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.memory_stability_verifier import (
    MemoryStabilityVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.degradation_analysis_verifier import (
    DegradationAnalysisVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.capacity_boundary_verifier import (
    CapacityBoundaryVerifier,
)
from app.platform_verification.enterprise_performance_infrastructure.verifiers.monitoring_integration_verifier import (
    MonitoringIntegrationVerifier,
)

__all__ = [
    "PerformanceTestArchitectureVerifier",
    "WorkloadModelingVerifier",
    "APIPerformanceVerifier",
    "E2EWorkflowVerifier",
    "ThroughputScalingVerifier",
    "DatabasePerformanceVerifier",
    "QueueCapacityVerifier",
    "WorkerEfficiencyVerifier",
    "ResourceUtilizationVerifier",
    "MemoryStabilityVerifier",
    "DegradationAnalysisVerifier",
    "CapacityBoundaryVerifier",
    "MonitoringIntegrationVerifier",
    "get_all_verifiers",
]


def get_all_verifiers() -> List[IEnterprisePerformanceVerifier]:
    """Returns an instantiated list of all 13 Phase 3J.6 verifiers in sequential order."""
    return [
        PerformanceTestArchitectureVerifier(),   # 3J.6.1
        WorkloadModelingVerifier(),              # 3J.6.2
        APIPerformanceVerifier(),                # 3J.6.3
        E2EWorkflowVerifier(),                   # 3J.6.4
        ThroughputScalingVerifier(),             # 3J.6.5
        DatabasePerformanceVerifier(),           # 3J.6.6
        QueueCapacityVerifier(),                 # 3J.6.7
        WorkerEfficiencyVerifier(),              # 3J.6.8
        ResourceUtilizationVerifier(),           # 3J.6.9
        MemoryStabilityVerifier(),               # 3J.6.10
        DegradationAnalysisVerifier(),           # 3J.6.11
        CapacityBoundaryVerifier(),              # 3J.6.12
        MonitoringIntegrationVerifier(),         # 3J.6.13
    ]
