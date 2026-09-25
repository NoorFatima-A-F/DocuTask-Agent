"""
Phase 3J.4: Resource Utilization & Capacity Engineering Verification Framework.

Enterprise resource profiling, container policy enforcement, CPU saturation analysis,
72-hour memory endurance verification, worker sizing optimization, queue drain velocity,
PostgreSQL capacity, AI component cost breakdown, capacity modeling, autoscaling, and alerting.
"""

from .api.resource_capacity_api import router
from .domain.interfaces import (
    IResourceCollector,
    IResourceExporter,
    IResourceRuntime,
    IResourceScorer,
    IResourceVerifier,
)
from .domain.models import (
    AIPipelineStageCost,
    AIResourceProfileReport,
    AlertRuleVerification,
    AutoscalingReadinessReport,
    BaseVerificationReport,
    CapacityModelReport,
    CategoryScore,
    CheckResult,
    ContainerLimitSpec,
    ContainerResourcePolicyReport,
    CPUCapacityReport,
    CPUWorkloadBenchmark,
    DatabaseCapacityReport,
    MemoryLeakReport,
    MemoryTimelinePoint,
    PerformanceCertificationReport,
    QueueCapacityReport,
    ResourceAlertReport,
    ResourceBottleneckComponent,
    ResourceCapacityCertificationReport,
    ResourceCertificationTier,
    ResourceProfileReport,
    ScalingTriggerSignal,
    ServiceResourceProfile,
    VerificationStatus,
    WorkerCapacityReport,
    WorkerScalingCurvePoint,
)
from .exporter.resource_capacity_exporter import ResourceCapacityExporter
from .runtime.resource_capacity_runtime import ResourceCapacityRuntime
from .scoring.resource_capacity_scorer import ResourceCapacityScorer
from .verifiers import get_all_verifiers

__all__ = [
    "router",
    "IResourceCollector",
    "IResourceVerifier",
    "IResourceScorer",
    "IResourceExporter",
    "IResourceRuntime",
    "VerificationStatus",
    "ResourceCertificationTier",
    "CheckResult",
    "BaseVerificationReport",
    "ServiceResourceProfile",
    "ResourceProfileReport",
    "ContainerLimitSpec",
    "ContainerResourcePolicyReport",
    "CPUWorkloadBenchmark",
    "CPUCapacityReport",
    "MemoryTimelinePoint",
    "MemoryLeakReport",
    "WorkerScalingCurvePoint",
    "WorkerCapacityReport",
    "QueueCapacityReport",
    "DatabaseCapacityReport",
    "AIPipelineStageCost",
    "AIResourceProfileReport",
    "ResourceBottleneckComponent",
    "CapacityModelReport",
    "ScalingTriggerSignal",
    "AutoscalingReadinessReport",
    "AlertRuleVerification",
    "ResourceAlertReport",
    "CategoryScore",
    "ResourceCapacityCertificationReport",
    "PerformanceCertificationReport",
    "ResourceCapacityScorer",
    "ResourceCapacityExporter",
    "ResourceCapacityRuntime",
    "get_all_verifiers",
]
