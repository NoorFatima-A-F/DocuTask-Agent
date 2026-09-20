"""
Phase 3I.2: Enterprise Logging Infrastructure Verification — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    ArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AgentLoggingReport,
    SecurityReport,
    PerformanceReport,
    FailureTestReport,
    CertificationReport,
)


class ILoggingArchitectureVerifier(ABC):
    @abstractmethod
    def verify_logging_architecture(self) -> ArchitectureReport:
        pass


class IStructuredLoggingVerifier(ABC):
    @abstractmethod
    def verify_structured_logging(self) -> StructuredLoggingReport:
        pass


class ICorrelationVerifier(ABC):
    @abstractmethod
    def verify_correlation(self) -> CorrelationReport:
        pass


class IAgentExecutionLoggingVerifier(ABC):
    @abstractmethod
    def verify_agent_execution_logging(self) -> AgentLoggingReport:
        pass


class ILoggingSecurityVerifier(ABC):
    @abstractmethod
    def verify_security(self) -> SecurityReport:
        pass


class ILoggingPerformanceVerifier(ABC):
    @abstractmethod
    def verify_performance(self) -> PerformanceReport:
        pass


class IFailureSimulationLoggingVerifier(ABC):
    @abstractmethod
    def verify_failure_simulation_logging(self) -> FailureTestReport:
        pass


class ILoggingQualityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: ArchitectureReport,
        struct_report: StructuredLoggingReport,
        corr_report: CorrelationReport,
        agent_report: AgentLoggingReport,
        sec_report: SecurityReport,
        perf_report: PerformanceReport,
        failure_report: FailureTestReport,
    ) -> CertificationReport:
        pass


class ILoggingEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: ArchitectureReport,
        struct_report: StructuredLoggingReport,
        corr_report: CorrelationReport,
        agent_report: AgentLoggingReport,
        sec_report: SecurityReport,
        perf_report: PerformanceReport,
        failure_report: FailureTestReport,
        certification_report: CertificationReport,
    ) -> Dict[str, Any]:
        pass
