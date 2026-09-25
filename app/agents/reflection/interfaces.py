"""
Interfaces for the Enterprise Reflection, Self-Critique, Evaluation & Continuous Adaptation Engine.
Defines formal abstract contracts for all reflection analyzers, evaluators, critiques, and generators.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID


class IReflectionEngine(ABC):
    """Core contract for the autonomous reflection engine."""

    @abstractmethod
    async def reflect(self, request: Any) -> Any:
        """Executes full evaluation, critique, and learning pipeline for a completed execution."""
        raise NotImplementedError


class IExecutionAnalyzer(ABC):
    """Contract for analyzing execution traces, states, and transition timelines."""

    @abstractmethod
    def analyze_execution(self, trace: Any) -> Dict[str, Any]:
        """Analyzes execution trace and returns structured diagnostic metrics."""
        raise NotImplementedError


class IPlanAnalyzer(ABC):
    """Contract for analyzing decomposition depth, task hierarchy, and dependencies."""

    @abstractmethod
    def analyze_plan(self, plan: Any, trace: Any) -> Dict[str, Any]:
        """Analyzes plan decomposition and structural efficiency."""
        raise NotImplementedError


class IReasoningAnalyzer(ABC):
    """Contract for evaluating reasoning fidelity, logic validity, and evidence linkage."""

    @abstractmethod
    def analyze_reasoning(self, reasoning_trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes cognitive steps and rationale chains."""
        raise NotImplementedError


class IToolUsageAnalyzer(ABC):
    """Contract for evaluating tool invocations, error rates, and alternative tool opportunities."""

    @abstractmethod
    def analyze_tool_usage(self, tool_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes tool invocation patterns and performance."""
        raise NotImplementedError


class IEvaluator(ABC):
    """Contract for quantitative evaluation dimensions."""

    @abstractmethod
    def evaluate(self, context: Any) -> Any:
        """Evaluates a target execution dimension and returns a dimension evaluation."""
        raise NotImplementedError


class ICritiqueEngine(ABC):
    """Contract for generating structured self-critiques across reasoning and action traces."""

    @abstractmethod
    def generate_critique(self, context: Any, evaluation_report: Any) -> Any:
        """Synthesizes strengths, weaknesses, and opportunities into a SelfCritique."""
        raise NotImplementedError


class IKnowledgeExtractor(ABC):
    """Contract for distilling generalizable heuristics and learning artifacts from traces."""

    @abstractmethod
    def extract_artifacts(self, context: Any, critique: Any) -> List[Any]:
        """Extracts immutable LearningArtifact objects."""
        raise NotImplementedError


class IRecommendationEngine(ABC):
    """Contract for synthesizing cross-subsystem actionable recommendations."""

    @abstractmethod
    def generate_recommendations(self, critique: Any, artifacts: List[Any]) -> List[Any]:
        """Generates evidence-backed recommendations for planner, execution, tools, and memory."""
        raise NotImplementedError


class IAdaptationEngine(ABC):
    """Contract for producing formal adaptation proposals requiring operational approval."""

    @abstractmethod
    def generate_proposals(self, recommendations: List[Any]) -> List[Any]:
        """Synthesizes concrete adaptation proposals from approved recommendations."""
        raise NotImplementedError


class IFeedbackGenerator(ABC):
    """Contract for formulating typed subsystem feedback payloads."""

    @abstractmethod
    def generate_feedback(self, critique: Any, recommendations: List[Any]) -> Any:
        """Synthesizes planner, execution, memory, and tool feedback bundles."""
        raise NotImplementedError


class IReflectionRepository(ABC):
    """Contract for persisting reflection sessions, evaluation reports, and learning artifacts."""

    @abstractmethod
    async def save(self, session: Any) -> None:
        """Persists a reflection session."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, reflection_id: UUID) -> Optional[Any]:
        """Retrieves a reflection session by its unique identifier."""
        raise NotImplementedError
