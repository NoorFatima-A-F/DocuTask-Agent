"""
Phase 3J.2: Performance Stress Verification & Capacity Boundary Analysis Framework.

Enterprise performance stress testing, capacity profiling, horizontal scaling,
deadlock detection, AI provider resilience, soak stability, recovery MTTR,
and regression gating for DocuTask Agent.
"""

from .api.performance_stress_api import router
from .domain.interfaces import (
    IPerformanceExporter,
    IPerformanceRuntime,
    IPerformanceScorer,
    IPerformanceVerifier,
)
from .domain.models import (
    AIProviderStressReport,
    BaselineStressReport,
    CapacityBoundaryReport,
    CertificationReport,
    CertificationTier,
    DatabasePerformanceReport,
    EnvironmentIsolationReport,
    MemoryStabilityReport,
    OverloadStressReport,
    ProgressiveLoadReport,
    RecoveryReport,
    RegressionReport,
    VerificationStatus,
    WorkerScalingReport,
)
from .exporter.performance_stress_exporter import PerformanceStressExporter
from .runtime.performance_stress_runtime import PerformanceStressRuntime
from .scoring.performance_stress_scorer import PerformanceStressScorer
from .verifiers import get_all_verifiers

__all__ = [
    "router",
    "IPerformanceVerifier",
    "IPerformanceScorer",
    "IPerformanceExporter",
    "IPerformanceRuntime",
    "CertificationTier",
    "VerificationStatus",
    "EnvironmentIsolationReport",
    "BaselineStressReport",
    "ProgressiveLoadReport",
    "OverloadStressReport",
    "CapacityBoundaryReport",
    "WorkerScalingReport",
    "DatabasePerformanceReport",
    "AIProviderStressReport",
    "MemoryStabilityReport",
    "RecoveryReport",
    "RegressionReport",
    "CertificationReport",
    "PerformanceStressScorer",
    "PerformanceStressExporter",
    "PerformanceStressRuntime",
    "get_all_verifiers",
]
