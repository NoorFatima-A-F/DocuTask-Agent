"""
Standardized interfaces for Enterprise Verification Metrics, Evaluation & Scoring Framework.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    MetricDefinition,
    MetricResult,
    StatisticalSummary,
    ConfidenceInterval,
    BenchmarkRecord,
    OverallScore,
    QualityGateDecision,
    QualityGateRule,
    AIQualityAssessment,
    EvaluationReport,
    MetricCategory,
    ABComparisonResult,
    RegressionAlert,
    SampleSizeValidationResult,
    MetricStoreRecord,
)


class IMetricCalculator(ABC):
    @abstractmethod
    def calculate(self, data: Dict[str, Any], definition: MetricDefinition) -> MetricResult:
        pass


class IStatisticalEngine(ABC):
    @abstractmethod
    def compute_summary(self, values: List[float]) -> StatisticalSummary:
        pass

    @abstractmethod
    def compute_wilson_confidence_interval(
        self, successes: int, total: int, confidence: float = 0.95
    ) -> ConfidenceInterval:
        pass

    @abstractmethod
    def validate_sample_size(self, sample_size: int, min_required: int = 30) -> bool:
        pass


class IABTestingEngine(ABC):
    @abstractmethod
    def compare_variants(
        self, variant_a_name: str, values_a: List[float], variant_b_name: str, values_b: List[float], metric_name: str
    ) -> ABComparisonResult:
        pass


class IRegressionDetector(ABC):
    @abstractmethod
    def check_regressions(
        self, candidate_results: List[MetricResult], baseline_results: List[MetricResult]
    ) -> List[RegressionAlert]:
        pass


class ISampleSizeValidator(ABC):
    @abstractmethod
    def validate_power(
        self, sample_size: int, confidence: float = 0.95, margin_of_error: float = 0.05
    ) -> SampleSizeValidationResult:
        pass


class IBenchmarkComparator(ABC):
    @abstractmethod
    def compare(
        self, candidate_results: List[MetricResult], baseline_results: List[MetricResult], system_version: str, baseline_version: str
    ) -> List[BenchmarkRecord]:
        pass


class IScoringEngine(ABC):
    @abstractmethod
    def compute_overall_score(
        self, metric_results: List[MetricResult], custom_weights: Optional[Dict[MetricCategory, float]] = None
    ) -> OverallScore:
        pass


class IQualityGateEngine(ABC):
    @abstractmethod
    def evaluate_gate(
        self, metric_results: List[MetricResult], rules: List[QualityGateRule]
    ) -> QualityGateDecision:
        pass


class IIAIQualityEvaluator(ABC):
    @abstractmethod
    def evaluate_output(
        self, prompt: str, generated_output: str, ground_truth: Optional[str] = None, context: Optional[str] = None
    ) -> AIQualityAssessment:
        pass


class IEvaluationAgent(ABC):
    @property
    @abstractmethod
    def agent_name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, execution_data: Dict[str, Any]) -> List[MetricResult]:
        pass


class IEvaluationPipeline(ABC):
    @abstractmethod
    def run_pipeline(
        self, raw_evidence: Dict[str, Any], system_version: str, baseline_evidence: Optional[Dict[str, Any]] = None
    ) -> EvaluationReport:
        pass


class IMetricRegistry(ABC):
    @abstractmethod
    def register(self, definition: MetricDefinition) -> None:
        pass

    @abstractmethod
    def get(self, metric_id: str) -> MetricDefinition:
        pass

    @abstractmethod
    def list_by_category(self, category: MetricCategory) -> List[MetricDefinition]:
        pass


class IMetricStore(ABC):
    @abstractmethod
    def save_result(self, execution_id: str, result: MetricResult) -> MetricStoreRecord:
        pass

    @abstractmethod
    def get_history(self, metric_id: str) -> List[MetricStoreRecord]:
        pass
