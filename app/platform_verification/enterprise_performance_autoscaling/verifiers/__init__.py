"""Verifier registry for Phase 3J.8 Enterprise Autoscaling & Elastic Capacity."""

from app.platform_verification.enterprise_performance_autoscaling.verifiers.architecture_verifier import (
    AutoscalingArchitectureVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scaling_metrics_verifier import (
    ScalingMetricsVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.worker_scaling_verifier import (
    WorkerScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.queue_autoscaling_verifier import (
    QueueAutoscalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.api_scaling_verifier import (
    APIScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scaling_policy_verifier import (
    ScalingPolicyVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scale_up_verifier import (
    ScaleUpVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scale_down_safety_verifier import (
    ScaleDownSafetyVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.database_scaling_limit_verifier import (
    DatabaseScalingImpactVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.ai_scaling_verifier import (
    AIScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.kubernetes_scaling_readiness_verifier import (
    K8sScalingReadinessVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.cloud_scaling_compatibility_verifier import (
    CloudScalingCompatibilityVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.cost_scaling_verifier import (
    CostScalingVerifier,
)
from app.platform_verification.enterprise_performance_autoscaling.verifiers.scaling_failure_verifier import (
    ScalingFailureSimulationVerifier,
)


def get_all_verifiers():
    """Return ordered list of all 14 Phase 3J.8 verifier instances."""
    return [
        AutoscalingArchitectureVerifier(),         # 3J.8.1
        ScalingMetricsVerifier(),                  # 3J.8.2
        WorkerScalingVerifier(),                   # 3J.8.3
        QueueAutoscalingVerifier(),                # 3J.8.4
        APIScalingVerifier(),                      # 3J.8.5
        ScalingPolicyVerifier(),                   # 3J.8.6
        ScaleUpVerifier(),                         # 3J.8.7
        ScaleDownSafetyVerifier(),                 # 3J.8.8
        DatabaseScalingImpactVerifier(),           # 3J.8.9
        AIScalingVerifier(),                       # 3J.8.10
        K8sScalingReadinessVerifier(),             # 3J.8.11
        CloudScalingCompatibilityVerifier(),       # 3J.8.12
        CostScalingVerifier(),                     # 3J.8.13
        ScalingFailureSimulationVerifier(),        # 3J.8.14
    ]
