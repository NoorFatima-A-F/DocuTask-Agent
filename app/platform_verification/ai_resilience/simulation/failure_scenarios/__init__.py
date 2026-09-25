"""Scenarios package exports."""

from .provider_unavailable import ProviderUnavailableScenario
from .latency_injection import LatencyInjectionScenario
from .invalid_response import InvalidResponseScenario
from .quota_exhaustion import QuotaExhaustionScenario
from .authentication_failure import AuthenticationFailureScenario
from .network_failure import NetworkFailureScenario
from .quality_degradation import QualityDegradationScenario

__all__ = [
    "ProviderUnavailableScenario",
    "LatencyInjectionScenario",
    "InvalidResponseScenario",
    "QuotaExhaustionScenario",
    "AuthenticationFailureScenario",
    "NetworkFailureScenario",
    "QualityDegradationScenario",
]
