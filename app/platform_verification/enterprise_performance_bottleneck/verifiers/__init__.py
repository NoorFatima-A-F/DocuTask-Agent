"""Verifier registry for Phase 3J.7 Enterprise Performance Bottleneck Discovery."""

from app.platform_verification.enterprise_performance_bottleneck.verifiers.architecture_profiling_verifier import (
    PerformanceArchitectureVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.resource_saturation_verifier import (
    ResourceSaturationVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.application_bottleneck_verifier import (
    ApplicationBottleneckVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.database_bottleneck_verifier import (
    DatabaseBottleneckVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.queue_bottleneck_verifier import (
    QueueBottleneckVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.worker_capacity_verifier import (
    WorkerCapacityVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.ai_provider_verifier import (
    AIProviderPerformanceVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.regression_detection_verifier import (
    PerformanceRegressionVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.capacity_boundary_verifier import (
    CapacityBoundaryVerifier,
)
from app.platform_verification.enterprise_performance_bottleneck.verifiers.optimization_recommendations_verifier import (
    OptimizationRecommendationsVerifier,
)


def get_all_verifiers():
    """Return ordered list of all 10 Phase 3J.7 verifier instances."""
    return [
        PerformanceArchitectureVerifier(),     # 3J.7.1
        ResourceSaturationVerifier(),          # 3J.7.2
        ApplicationBottleneckVerifier(),       # 3J.7.3
        DatabaseBottleneckVerifier(),          # 3J.7.4
        QueueBottleneckVerifier(),             # 3J.7.5
        WorkerCapacityVerifier(),              # 3J.7.6
        AIProviderPerformanceVerifier(),       # 3J.7.7
        PerformanceRegressionVerifier(),       # 3J.7.8
        CapacityBoundaryVerifier(),            # 3J.7.9
        OptimizationRecommendationsVerifier(), # 3J.7.10
    ]
