"""Domain Interfaces for Phase 6: AI System Evaluation, Benchmarking & Portfolio Certification Framework."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .models import (
    AgentEvaluationReport,
    AICapabilityBenchmarkReport,
    CostBusinessReport,
    ExplainabilityReport,
    HumanExperienceReport,
    LLMEvaluationReport,
    PerformanceBenchmarkReport,
    PlatformCertificationScore,
    PortfolioShowcaseReport,
    RAGEvaluationReport,
    ReliabilityEvaluationReport,
    SecurityEvaluationReport,
)


class IBaseEvaluator(ABC):
    @property
    @abstractmethod
    def evaluator_id(self) -> str:
        """Unique evaluator identifier."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable evaluator name."""
        ...

    @abstractmethod
    def evaluate(self) -> Any:
        """Execute evaluation logic and return typed report."""
        ...


class IAICapabilityBenchmarker(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> AICapabilityBenchmarkReport: ...


class ILLMEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> LLMEvaluationReport: ...


class IAgentEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> AgentEvaluationReport: ...


class IRAGEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> RAGEvaluationReport: ...


class IPerformanceBenchmarker(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> PerformanceBenchmarkReport: ...


class ICostBusinessEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> CostBusinessReport: ...


class IReliabilityEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> ReliabilityEvaluationReport: ...


class ISecurityEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> SecurityEvaluationReport: ...


class IExplainabilityEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> ExplainabilityReport: ...


class IHumanExperienceEvaluator(IBaseEvaluator):
    @abstractmethod
    def evaluate(self) -> HumanExperienceReport: ...


class IPortfolioCertificationScorer(ABC):
    @abstractmethod
    def calculate_score(self, reports: Dict[str, Any]) -> PlatformCertificationScore:
        """Calculate weighted 6-pillar portfolio intelligence certification score."""
        ...


class IPortfolioEvidenceGenerator(ABC):
    @abstractmethod
    def export(
        self,
        report: PortfolioShowcaseReport,
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """Generate case studies, whitepapers, dashboards, and SHA-256 manifest."""
        ...


class IEvaluationRuntime(ABC):
    @abstractmethod
    def execute_all(self, output_dir: Optional[str] = None) -> PortfolioShowcaseReport:
        """Execute all evaluators, calculate intelligence score, and generate portfolio evidence."""
        ...
