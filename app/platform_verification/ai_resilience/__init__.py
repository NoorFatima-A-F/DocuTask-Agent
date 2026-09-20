"""Phase 3H.3.10 - AI Failure Simulation & Resilience Verification Framework."""

from .domain.models import (
    ChaosScenarioType,
    CircuitBreakerState,
    TaskResilienceStatus,
    AIResilienceTier,
    FallbackProviderType,
    FailureInjectionScenario,
    OutageSimulationReport,
    LatencyChaosReport,
    MalformedResponseReport,
    AuthFailureReport,
    QuotaExhaustionReport,
    NetworkFailureReport,
    QualityDegradationReport,
    FallbackVerificationReport,
    TaskPreservationReport,
    CircuitBreakerReport,
    ChaosExperimentResult,
    RecoveryMetricsReport,
    AIResilienceScorecard,
)
from .runtime.ai_resilience_runtime import AIResilienceRuntime
from .api.ai_resilience_api import router as ai_resilience_router

__all__ = [
    "ChaosScenarioType",
    "CircuitBreakerState",
    "TaskResilienceStatus",
    "AIResilienceTier",
    "FallbackProviderType",
    "FailureInjectionScenario",
    "OutageSimulationReport",
    "LatencyChaosReport",
    "MalformedResponseReport",
    "AuthFailureReport",
    "QuotaExhaustionReport",
    "NetworkFailureReport",
    "QualityDegradationReport",
    "FallbackVerificationReport",
    "TaskPreservationReport",
    "CircuitBreakerReport",
    "ChaosExperimentResult",
    "RecoveryMetricsReport",
    "AIResilienceScorecard",
    "AIResilienceRuntime",
    "ai_resilience_router",
]
