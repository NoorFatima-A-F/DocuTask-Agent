"""Simulation package exports."""

from .ai_failure_simulator import AIFailureSimulator
from .failure_scenarios import (
    ProviderUnavailableScenario,
    LatencyInjectionScenario,
    InvalidResponseScenario,
    QuotaExhaustionScenario,
    AuthenticationFailureScenario,
    NetworkFailureScenario,
    QualityDegradationScenario,
)

__all__ = [
    "AIFailureSimulator",
    "ProviderUnavailableScenario",
    "LatencyInjectionScenario",
    "InvalidResponseScenario",
    "QuotaExhaustionScenario",
    "AuthenticationFailureScenario",
    "NetworkFailureScenario",
    "QualityDegradationScenario",
]
