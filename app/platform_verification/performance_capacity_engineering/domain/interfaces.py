"""
Phase 3J.1: Performance Infrastructure Verification — Domain Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from app.platform_verification.performance_capacity_engineering.domain.models import (
    PerformanceArchitectureReport,
    BaselinePerformanceReport,
    WorkloadModelingReport,
    ControlledLoadTestReport,
    CapacityReport,
    BottleneckAnalysisReport,
    PerformanceRegressionReport,
    AIPipelinePerformanceReport,
    DatabasePerformanceReport,
    QueuePerformanceReport,
    PerformanceCertificationReport,
)


class IPerformanceArchitectureVerifier(ABC):
    @abstractmethod
    def verify(self) -> PerformanceArchitectureReport:
        """Verify performance testing architecture and tool integration."""
        pass


class IBaselinePerformanceVerifier(ABC):
    @abstractmethod
    def verify(self) -> BaselinePerformanceReport:
        """Measure baseline latency percentiles, throughput, and resource utilization."""
        pass


class IWorkloadModelingVerifier(ABC):
    @abstractmethod
    def verify(self) -> WorkloadModelingReport:
        """Verify realistic workload modeling across Normal, Heavy, Peak, and AI-Heavy classes."""
        pass


class IControlledLoadTestVerifier(ABC):
    @abstractmethod
    def verify(self) -> ControlledLoadTestReport:
        """Execute 4-stage controlled load testing: Smoke, Normal, Capacity, and Breaking Point."""
        pass


class ICapacityModelingVerifier(ABC):
    @abstractmethod
    def verify(self) -> CapacityReport:
        """Verify SLI/SLO compliance and multi-stage automated performance pipeline execution."""
        pass


class IBottleneckAnalysisVerifier(ABC):
    @abstractmethod
    def verify(self) -> BottleneckAnalysisReport:
        """Identify bottlenecks across API, Database, Queue, Workers, and AI Provider."""
        pass


class IPerformanceRegressionVerifier(ABC):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport:
        """Compare current vs previous version and enforce regression gate (>20%)."""
        pass


class IAIPipelinePerformanceVerifier(ABC):
    @abstractmethod
    def verify(self) -> AIPipelinePerformanceReport:
        """Break down AI pipeline latencies across OCR, Gemini LLM, validation, and tokens."""
        pass


class IDatabasePerformanceVerifier(ABC):
    @abstractmethod
    def verify(self) -> DatabasePerformanceReport:
        """Verify database connection pool scaling (10, 100, 500) and query latency."""
        pass


class IQueuePerformanceVerifier(ABC):
    @abstractmethod
    def verify(self) -> QueuePerformanceReport:
        """Verify queue stress with 10,000 documents and zero message loss."""
        pass


class IPerformanceCertificationScorer(ABC):
    @abstractmethod
    def compute_certification(self, verification_results: Dict[str, Any]) -> PerformanceCertificationReport:
        """Compute the 6-category weighted score and generate the certification report."""
        pass


class IPerformanceVerificationExporter(ABC):
    @abstractmethod
    def export(self, verification_results: Dict[str, Any], certification_report: PerformanceCertificationReport) -> Dict[str, str]:
        """Export all verification manifests and signed metadata.json."""
        pass
