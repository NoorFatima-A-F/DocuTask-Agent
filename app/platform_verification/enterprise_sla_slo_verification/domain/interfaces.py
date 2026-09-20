"""
Phase 3J.10: Enterprise Performance SLA, SLO & Continuous Reliability Verification — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    BaseVerificationReport,
    CIPerformanceStage,
    ContinuousMonitoringReport,
    DashboardValidationReport,
    EndurancePerformanceReport,
    ErrorBudgetReport,
    PerformanceAlertReport,
    PerformanceGovernanceReport,
    PerformanceIncidentReport,
    PerformancePipelineReport,
    PerformanceRecoveryReport,
    PerformanceRegressionReport,
    SLADefinitionReport,
    SLOConfigurationReport,
)


class ISLASLOVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str: pass

    @property
    def phase_id(self) -> str:
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3J.") or part.startswith("3j."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def verify(self) -> Any: pass


class ISLADefinitionVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> SLADefinitionReport: pass


class ISLOImplementationVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> SLOConfigurationReport: pass


class IErrorBudgetVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> ErrorBudgetReport: pass


class IContinuousMonitoringVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> ContinuousMonitoringReport: pass


class IPerformanceRegressionVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport: pass


class ILongRunningReliabilityVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> EndurancePerformanceReport: pass


class IPerformanceAlertVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> PerformanceAlertReport: pass


class IPerformanceIncidentVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> PerformanceIncidentReport: pass


class IPerformanceRecoveryVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRecoveryReport: pass


class IDashboardValidationVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> DashboardValidationReport: pass


class IPerformanceGovernanceVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> PerformanceGovernanceReport: pass


class ICICDPerformancePipelineVerifier(ISLASLOVerifier):
    @abstractmethod
    def verify(self) -> PerformancePipelineReport: pass
