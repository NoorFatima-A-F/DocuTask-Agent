"""
Phase 3J.11: Intelligent Performance Optimization & Autonomous Capacity Management — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from .models import (
    AIPipelineOptimizationReport,
    AutomatedRemediationReport,
    CapacityPredictionReport,
    ContinuousOptimizationLoopReport,
    DatabaseOptimizationReport,
    OptimizationPipelineReport,
    OptimizationRecommendationReport,
    OptimizationSafetyReport,
    PerformanceAnomalyReport,
    PerformanceIntelligenceArchitectureReport,
    RootCauseAnalysisReport,
    WorkerAutoscalingReport,
)


class IOptimizationVerifier(ABC):
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


class IPerformanceIntelligenceArchitectureVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> PerformanceIntelligenceArchitectureReport: pass


class IBottleneckRootCauseVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> RootCauseAnalysisReport: pass


class IOptimizationRecommendationVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> OptimizationRecommendationReport: pass


class IIntelligentAutoscalingVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> WorkerAutoscalingReport: pass


class IDatabaseOptimizationVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> DatabaseOptimizationReport: pass


class IAIPipelineOptimizationVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> AIPipelineOptimizationReport: pass


class IPredictiveCapacityPlanningVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> CapacityPredictionReport: pass


class IPerformanceAnomalyVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> PerformanceAnomalyReport: pass


class IAutomatedRemediationVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> AutomatedRemediationReport: pass


class IOptimizationSafetyVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> OptimizationSafetyReport: pass


class IContinuousOptimizationLoopVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> ContinuousOptimizationLoopReport: pass


class ICICDOptimizationPipelineVerifier(IOptimizationVerifier):
    @abstractmethod
    def verify(self) -> OptimizationPipelineReport: pass
