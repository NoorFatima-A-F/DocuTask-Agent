"""
Phase 3J.12: Continuous Performance Engineering & Regression Intelligence — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from .models import (
    BenchmarkExecutionReport,
    ChangeImpactAnalysisReport,
    CICDPerformancePipelineReport,
    ContinuousPerformanceArchitectureReport,
    MultiEnvironmentComparisonReport,
    PerformanceBaselineReport,
    PerformanceDashboardReport,
    PerformanceExperimentReport,
    PerformanceGateReport,
    PerformanceKnowledgeReport,
    PerformanceRegressionReport,
    PerformanceTrendReport,
)


class IContinuousPerformanceVerifier(ABC):
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


class IContinuousPerformanceArchitectureVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ContinuousPerformanceArchitectureReport: pass


class IPerformanceBaselineVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceBaselineReport: pass


class IBenchmarkExecutionVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> BenchmarkExecutionReport: pass


class IPerformanceRegressionEngineVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport: pass


class IChangeImpactAnalysisVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ChangeImpactAnalysisReport: pass


class IPerformanceQualityGatesVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceGateReport: pass


class IMultiEnvironmentComparisonVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> MultiEnvironmentComparisonReport: pass


class IPerformanceKnowledgeRepositoryVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceKnowledgeReport: pass


class IPerformanceTrendAnalysisVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceTrendReport: pass


class IContinuousPerformanceDashboardVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceDashboardReport: pass


class ICICDPerformanceIntegrationVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CICDPerformancePipelineReport: pass


class IPerformanceExperimentTrackingVerifier(IContinuousPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceExperimentReport: pass
