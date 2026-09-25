"""
Verifiers package for Phase 3J.4 Resource Utilization & Capacity Engineering.
"""

from typing import List

from ..domain.interfaces import IResourceVerifier
from .ai_resource_profile_verifier import AIResourceProfileVerifier
from .autoscaling_readiness_verifier import AutoscalingReadinessVerifier
from .capacity_modeling_verifier import CapacityModelingVerifier
from .container_resource_policy_verifier import ContainerResourcePolicyVerifier
from .cpu_utilization_verifier import CPUUtilizationVerifier
from .database_capacity_verifier import DatabaseCapacityVerifier
from .memory_leak_verifier import MemoryLeakVerifier
from .queue_capacity_verifier import QueueCapacityVerifier
from .resource_alerting_verifier import ResourceAlertingVerifier
from .resource_profiling_verifier import ResourceProfilingVerifier
from .worker_capacity_verifier import WorkerCapacityVerifier


def get_all_verifiers() -> List[IResourceVerifier]:
    """Returns an instantiated list of all 11 verifiers covering Phase 3J.4."""
    return [
        ResourceProfilingVerifier(),
        ContainerResourcePolicyVerifier(),
        CPUUtilizationVerifier(),
        MemoryLeakVerifier(),
        WorkerCapacityVerifier(),
        QueueCapacityVerifier(),
        DatabaseCapacityVerifier(),
        AIResourceProfileVerifier(),
        CapacityModelingVerifier(),
        AutoscalingReadinessVerifier(),
        ResourceAlertingVerifier(),
    ]


__all__ = [
    "ResourceProfilingVerifier",
    "ContainerResourcePolicyVerifier",
    "CPUUtilizationVerifier",
    "MemoryLeakVerifier",
    "WorkerCapacityVerifier",
    "QueueCapacityVerifier",
    "DatabaseCapacityVerifier",
    "AIResourceProfileVerifier",
    "CapacityModelingVerifier",
    "AutoscalingReadinessVerifier",
    "ResourceAlertingVerifier",
    "get_all_verifiers",
]
