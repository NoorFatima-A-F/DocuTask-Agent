"""Verifier registry for Phase 3J.9 Enterprise AI Performance Bottleneck."""

from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.architecture_modeling_verifier import (
    PerformanceArchitectureModelingVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.latency_profiling_verifier import (
    LatencyProfilingVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.throughput_capacity_verifier import (
    ThroughputCapacityVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.resource_bottleneck_verifier import (
    ResourceBottleneckVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.database_performance_verifier import (
    DatabasePerformanceVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.queue_capacity_verifier import (
    QueueCapacityVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.worker_scaling_verifier import (
    WorkerScalingVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.ai_model_performance_verifier import (
    AIModelPerformanceVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.performance_regression_verifier import (
    PerformanceRegressionVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.capacity_planning_verifier import (
    CapacityPlanningVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.performance_failure_verifier import (
    PerformanceFailureSimulationVerifier,
)
from app.platform_verification.enterprise_ai_performance_bottleneck.verifiers.performance_observability_verifier import (
    PerformanceObservabilityVerifier,
)


def get_all_verifiers():
    """Return ordered list of all 12 Phase 3J.9 verifier instances."""
    return [
        PerformanceArchitectureModelingVerifier(),    # 3J.9.1
        LatencyProfilingVerifier(),                    # 3J.9.2
        ThroughputCapacityVerifier(),                  # 3J.9.3
        ResourceBottleneckVerifier(),                  # 3J.9.4
        DatabasePerformanceVerifier(),                 # 3J.9.5
        QueueCapacityVerifier(),                       # 3J.9.6
        WorkerScalingVerifier(),                       # 3J.9.7
        AIModelPerformanceVerifier(),                  # 3J.9.8
        PerformanceRegressionVerifier(),               # 3J.9.9
        CapacityPlanningVerifier(),                    # 3J.9.10
        PerformanceFailureSimulationVerifier(),        # 3J.9.11
        PerformanceObservabilityVerifier(),            # 3J.9.12
    ]
