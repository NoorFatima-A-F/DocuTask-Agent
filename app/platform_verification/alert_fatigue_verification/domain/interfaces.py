"""Abstract interfaces for Alert Fatigue Prevention & Signal Optimization sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    FatigueArchitectureReport,
    DeduplicationReport,
    CorrelationReport,
    SeverityOptimizationReport,
    RoutingReport,
    SuppressionReport,
    GroupingReport,
    NoiseMetricsReport,
    AlertStormReport,
    MachinePrioritizationReport,
    AlertFatigueScorecard,
)


class IFatigueArchitectureVerifier(ABC):
    """Interface for verifying signal processing pipeline architecture (3H.4.8.1)."""

    @abstractmethod
    def verify_architecture(self) -> FatigueArchitectureReport:
        pass


class IAlertDeduplicationVerifier(ABC):
    """Interface for verifying alert deduplication across services (3H.4.8.2)."""

    @abstractmethod
    def verify_deduplication(self) -> DeduplicationReport:
        pass


class IAlertCorrelationVerifier(ABC):
    """Interface for verifying dependency-aware causal alert grouping (3H.4.8.3)."""

    @abstractmethod
    def verify_correlation(self) -> CorrelationReport:
        pass


class ISeverityOptimizationVerifier(ABC):
    """Interface for verifying multi-factor severity assignment (3H.4.8.4)."""

    @abstractmethod
    def verify_severity_optimization(self) -> SeverityOptimizationReport:
        pass


class IAlertRoutingVerifier(ABC):
    """Interface for verifying team ownership and escalation routing (3H.4.8.5)."""

    @abstractmethod
    def verify_routing(self) -> RoutingReport:
        pass


class IAlertSuppressionVerifier(ABC):
    """Interface for verifying maintenance suppression and safety bypass controls (3H.4.8.6)."""

    @abstractmethod
    def verify_suppression(self) -> SuppressionReport:
        pass


class IAlertGroupingVerifier(ABC):
    """Interface for verifying high-volume symptom grouping into consolidated incidents (3H.4.8.7)."""

    @abstractmethod
    def verify_grouping(self) -> GroupingReport:
        pass


class INoiseMetricsVerifier(ABC):
    """Interface for calculating noise ratio, actionable ratio, and duplicate reduction (3H.4.8.8)."""

    @abstractmethod
    def verify_noise_metrics(self) -> NoiseMetricsReport:
        pass


class IAlertStormSimulator(ABC):
    """Interface for stress testing pipeline under 10,000-event alert storm (3H.4.8.9)."""

    @abstractmethod
    def simulate_alert_storm(self) -> AlertStormReport:
        pass


class IMachinePrioritizationVerifier(ABC):
    """Interface for validating explainable 0-100 ML-assisted priority calculations (3H.4.8.10)."""

    @abstractmethod
    def verify_machine_prioritization(self) -> MachinePrioritizationReport:
        pass


class IAlertFatigueScorer(ABC):
    """Interface for calculating 6-category weighted quality scorecard (3H.4.8.11)."""

    @abstractmethod
    def score_fatigue(
        self,
        arch_rep: FatigueArchitectureReport,
        dedup_rep: DeduplicationReport,
        corr_rep: CorrelationReport,
        sev_rep: SeverityOptimizationReport,
        route_rep: RoutingReport,
        supp_rep: SuppressionReport,
        group_rep: GroupingReport,
        noise_rep: NoiseMetricsReport,
        storm_rep: AlertStormReport,
        ml_rep: MachinePrioritizationReport,
    ) -> AlertFatigueScorecard:
        pass


class IAlertFatigueEvidenceExporter(ABC):
    """Interface for exporting structured 12-manifest compliance evidence (3H.4.8.12)."""

    @abstractmethod
    def export_all(
        self,
        arch_rep: FatigueArchitectureReport,
        dedup_rep: DeduplicationReport,
        corr_rep: CorrelationReport,
        sev_rep: SeverityOptimizationReport,
        route_rep: RoutingReport,
        supp_rep: SuppressionReport,
        group_rep: GroupingReport,
        noise_rep: NoiseMetricsReport,
        storm_rep: AlertStormReport,
        ml_rep: MachinePrioritizationReport,
        scorecard: AlertFatigueScorecard,
    ) -> Dict[str, str]:
        pass
