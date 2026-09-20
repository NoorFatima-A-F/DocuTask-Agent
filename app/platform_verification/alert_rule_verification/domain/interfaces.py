"""Abstract interfaces for Enterprise Alert Rule Verification sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    ArchitectureReport,
    TaxonomyReport,
    CriticalAlertReport,
    WarningAlertReport,
    ConditionTestReport,
    SeverityReport,
    MessageQualityReport,
    RoutingReport,
    FatigueReport,
    FailureTestReport,
    PerformanceReport,
    AlertQualityScorecard,
)


class IAlertArchitectureVerifier(ABC):
    """Interface for verifying alert architecture and lifecycle (3H.4.5.1)."""

    @abstractmethod
    def verify_architecture(self) -> ArchitectureReport:
        pass


class IAlertTaxonomyVerifier(ABC):
    """Interface for verifying 5-category alert taxonomy (3H.4.5.2)."""

    @abstractmethod
    def verify_taxonomy(self) -> TaxonomyReport:
        pass


class ICriticalAlertVerifier(ABC):
    """Interface for verifying business-critical failure alerts (3H.4.5.3)."""

    @abstractmethod
    def verify_critical_alerts(self) -> CriticalAlertReport:
        pass


class IWarningAlertVerifier(ABC):
    """Interface for verifying early degradation warning alerts (3H.4.5.4)."""

    @abstractmethod
    def verify_warning_alerts(self) -> WarningAlertReport:
        pass


class IAlertConditionVerifier(ABC):
    """Interface for testing false -> true -> resolved transitions (3H.4.5.5)."""

    @abstractmethod
    def verify_conditions(self) -> ConditionTestReport:
        pass


class IAlertSeverityVerifier(ABC):
    """Interface for verifying severity-to-impact alignment (3H.4.5.6)."""

    @abstractmethod
    def verify_severity(self) -> SeverityReport:
        pass


class IAlertMessageVerifier(ABC):
    """Interface for verifying actionable alert messages & runbooks (3H.4.5.7)."""

    @abstractmethod
    def verify_messages(self) -> MessageQualityReport:
        pass


class IAlertRoutingVerifier(ABC):
    """Interface for verifying alert routing & escalation paths (3H.4.5.8)."""

    @abstractmethod
    def verify_routing(self) -> RoutingReport:
        pass


class IAlertFatigueVerifier(ABC):
    """Interface for verifying deduplication, grouping & suppression (3H.4.5.10)."""

    @abstractmethod
    def verify_fatigue_prevention(self) -> FatigueReport:
        pass


class IFailureInjectionVerifier(ABC):
    """Interface for executing controlled failure injection tests (3H.4.5.11)."""

    @abstractmethod
    def verify_failure_injection(self) -> FailureTestReport:
        pass


class IAlertPerformanceVerifier(ABC):
    """Interface for measuring MTTD, MTTR, Precision & Recall (3H.4.5.12)."""

    @abstractmethod
    def verify_performance(self) -> PerformanceReport:
        pass


class IAlertQualityScorer(ABC):
    """Interface for 6-category weighted quality scoring (3H.4.5.14)."""

    @abstractmethod
    def score_alerts(
        self,
        arch_rep: ArchitectureReport,
        tax_rep: TaxonomyReport,
        crit_rep: CriticalAlertReport,
        warn_rep: WarningAlertReport,
        cond_rep: ConditionTestReport,
        sev_rep: SeverityReport,
        msg_rep: MessageQualityReport,
        route_rep: RoutingReport,
        fatigue_rep: FatigueReport,
        fail_rep: FailureTestReport,
        perf_rep: PerformanceReport,
    ) -> AlertQualityScorecard:
        pass


class IAlertEvidenceExporter(ABC):
    """Interface for exporting structured alert compliance manifests (3H.4.5.15)."""

    @abstractmethod
    def export_all(
        self,
        arch_rep: ArchitectureReport,
        tax_rep: TaxonomyReport,
        crit_rep: CriticalAlertReport,
        warn_rep: WarningAlertReport,
        cond_rep: ConditionTestReport,
        sev_rep: SeverityReport,
        msg_rep: MessageQualityReport,
        route_rep: RoutingReport,
        fatigue_rep: FatigueReport,
        fail_rep: FailureTestReport,
        perf_rep: PerformanceReport,
        scorecard: AlertQualityScorecard,
    ) -> Dict[str, str]:
        pass
