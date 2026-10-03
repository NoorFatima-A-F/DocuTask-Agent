"""
Automated Specialized Evaluation Agents (Accuracy, Security, Quality, Performance, AI Quality).
"""
from __future__ import annotations
from typing import Any, Dict, List
from app.platform_verification.evaluation_engine.domain.models import (
    MetricResult,
    MetricCategory,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IEvaluationAgent
from app.platform_verification.evaluation_engine.core.metric_registry import MetricRegistry
from app.platform_verification.evaluation_engine.core.calculators import (
    FunctionalCorrectnessCalculator,
    AiQualityCalculator,
    PerformanceCalculator,
    ReliabilityCalculator,
    SecurityCalculator,
)


class AccuracyEvaluatorAgent(IEvaluationAgent):
    """Evaluates functional accuracy and extraction correctness."""

    def __init__(self, registry: MetricRegistry):
        self.registry = registry
        self.calculator = FunctionalCorrectnessCalculator()

    @property
    def agent_name(self) -> str:
        return "AccuracyEvaluatorAgent"

    def evaluate(self, execution_data: Dict[str, Any]) -> List[MetricResult]:
        metrics = self.registry.list_by_category(MetricCategory.FUNCTIONAL_CORRECTNESS)
        return [self.calculator.calculate(execution_data, m) for m in metrics]


class PerformanceEvaluatorAgent(IEvaluationAgent):
    """Evaluates latency, throughput, and SLA compliance."""

    def __init__(self, registry: MetricRegistry):
        self.registry = registry
        self.calculator = PerformanceCalculator()

    @property
    def agent_name(self) -> str:
        return "PerformanceEvaluatorAgent"

    def evaluate(self, execution_data: Dict[str, Any]) -> List[MetricResult]:
        metrics = self.registry.list_by_category(MetricCategory.PERFORMANCE)
        return [self.calculator.calculate(execution_data, m) for m in metrics]


class SecurityEvaluatorAgent(IEvaluationAgent):
    """Evaluates security vulnerabilities, prompt injection resistance, and data leaks."""

    def __init__(self, registry: MetricRegistry):
        self.registry = registry
        self.calculator = SecurityCalculator()

    @property
    def agent_name(self) -> str:
        return "SecurityEvaluatorAgent"

    def evaluate(self, execution_data: Dict[str, Any]) -> List[MetricResult]:
        metrics = self.registry.list_by_category(MetricCategory.SECURITY)
        return [self.calculator.calculate(execution_data, m) for m in metrics]


class ReliabilityEvaluatorAgent(IEvaluationAgent):
    """Evaluates uptime, failure rates, and recovery success."""

    def __init__(self, registry: MetricRegistry):
        self.registry = registry
        self.calculator = ReliabilityCalculator()

    @property
    def agent_name(self) -> str:
        return "ReliabilityEvaluatorAgent"

    def evaluate(self, execution_data: Dict[str, Any]) -> List[MetricResult]:
        metrics = self.registry.list_by_category(MetricCategory.RELIABILITY)
        return [self.calculator.calculate(execution_data, m) for m in metrics]


class AiQualityEvaluatorAgent(IEvaluationAgent):
    """Evaluates generative AI faithfulness, grounding, and hallucination rates."""

    def __init__(self, registry: MetricRegistry):
        self.registry = registry
        self.calculator = AiQualityCalculator()

    @property
    def agent_name(self) -> str:
        return "AiQualityEvaluatorAgent"

    def evaluate(self, execution_data: Dict[str, Any]) -> List[MetricResult]:
        metrics = self.registry.list_by_category(MetricCategory.AI_QUALITY)
        return [self.calculator.calculate(execution_data, m) for m in metrics]
